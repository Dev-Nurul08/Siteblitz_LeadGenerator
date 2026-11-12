"""
E2 race and integrity tests (spec E2 criterion: 0 duplicate sends under retry, 0 sends after an observed
suppression, queue state recovers after a crash; launch gate 17 e failure tests). SMTP = aiosmtpd on 127.0.0.1.
"""

import asyncio
from datetime import timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.app.engines.eligibility.verification import VerifierResult
from backend.app.engines.enrichment.site_visit import SiteVisit
from backend.app.engines.sending.tokens import email_hash
from backend.app.models.eligibility import EmailEligibility, VerificationStatus
from backend.app.models.sending import (
    EmailSequence,
    PauseFlag,
    PauseScope,
    SendRecord,
    SendState,
    SequenceState,
    SuppressionMirror,
)
from backend.app.services.outreach_worker import OutreachWorker, WorkerLock
from backend.app.services.sending_service import Conflict, SendingConfig, SendingService
from backend.tests.test_eligibility.conftest import NOW as E1_NOW
from backend.tests.test_eligibility.conftest import add_business, add_capture, add_check, service as e1_service

from .conftest import (
    BEFORE,
    CONFIG,
    NEXT_TUE,
    TUE,
    Clock,
    FakeEligibility,
    add_lead,
    add_mailbox,
    admitted_sequence,
    ist,
    item,
    make_worker,
    set_ramp,
)


async def ready(session, smtp_server, **kwargs):
    await add_mailbox(session, port=smtp_server.port)
    await set_ramp(session, 1)
    await session.commit()
    return await admitted_sequence(session, **kwargs)


async def steps(session, sequence_id):
    session.expire_all()
    return (await session.execute(select(SendRecord).where(SendRecord.sequence_id == sequence_id)
                                  .order_by(SendRecord.step))).scalars().all()


async def active_reasons(session):
    session.expire_all()
    return sorted(f.reason_code for f in (await session.execute(
        select(PauseFlag).where(PauseFlag.cleared_at.is_(None)))).scalars().all())


async def test_suppression_added_between_approval_and_submission_is_not_sent(factory, session, website,
                                                                             smtp_server):
    admitted = await ready(session, smtp_server)
    website.suppressed.add(email_hash("info@glowhair.example"))   # the owner clicked unsubscribe after approval
    summary = await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert summary["cancelled"] == 1 and smtp_server.envelopes == []
    assert [r.state for r in await steps(session, admitted["sequence_id"])] == [SendState.CANCELLED] * 3
    sequence = await session.get(EmailSequence, admitted["sequence_id"])
    await session.refresh(sequence)
    assert sequence.state == SequenceState.STOPPED_SUPPRESSED
    assert FakeEligibility.calls == []        # suppression is checked before anything else costs a request


async def test_a_reply_before_a_follow_up_cancels_it(factory, session, website, smtp_server):
    admitted = await ready(session, smtp_server)
    clock = Clock(ist(TUE, 9, 1))
    await make_worker(factory, clock, website).run_once()
    service = SendingService(session, CONFIG)
    step2 = (await steps(session, admitted["sequence_id"]))[1]
    await service.approve_follow_up(step2.id, "Following up: shall I make the sample?", "founder", "t2", now=clock())
    await service.stop_sequence(admitted["sequence_id"], SequenceState.STOPPED_REPLY, "owner replied")   # E4
    await session.commit()
    clock.at(ist(NEXT_TUE, 9, 1))
    await make_worker(factory, clock, website).run_once()
    assert len(smtp_server.envelopes) == 1
    assert [r.state for r in await steps(session, admitted["sequence_id"])] == [
        SendState.ACCEPTED, SendState.CANCELLED, SendState.CANCELLED]


async def test_two_workers_on_the_same_records_submit_exactly_once(factory, session, website, smtp_server, tmp_path):
    admitted = await ready(session, smtp_server)
    second_engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'e2.db'}")
    other_factory = async_sessionmaker(second_engine, expire_on_commit=False)
    try:
        clock = Clock(ist(TUE, 9, 1))
        first, second = make_worker(factory, clock, website), make_worker(other_factory, clock, website)
        results = await asyncio.gather(first.run_once(), second.run_once())
        assert sum(r["accepted"] for r in results) == 1
        assert sum(r.get("skipped", 0) for r in results) == 1
        await first.run_once()                    # a retry of the same cycle
        await second.run_once()
    finally:
        await second_engine.dispose()
    assert len(smtp_server.envelopes) == 1
    step1 = (await steps(session, admitted["sequence_id"]))[0]
    assert step1.state == SendState.ACCEPTED and step1.attempts == 1
    session.add(SendRecord(sequence_id=step1.sequence_id, step=1, idempotency_key=step1.idempotency_key,
                           mailbox_id=step1.mailbox_id, recipient_email=step1.recipient_email,
                           recipient_hash=step1.recipient_hash, message_id="<another@send-one.example>",
                           scheduled_for=step1.scheduled_for, local_date=step1.local_date,
                           window_label=step1.window_label, window_start=step1.window_start,
                           window_end=step1.window_end))
    with pytest.raises(IntegrityError):           # the database refuses a second record for the same step
        await session.flush()


def test_only_one_worker_process_holds_the_lock(tmp_path):
    first, second = WorkerLock(tmp_path / "outreach_worker.lock"), WorkerLock(tmp_path / "outreach_worker.lock")
    assert first.acquire()
    try:
        assert not second.acquire()
        assert "pid=" in second.holder()
    finally:
        first.release()
    assert second.acquire()
    second.release()


async def test_timeout_after_data_is_uncertain_pauses_everything_and_is_never_retried(factory, session, website,
                                                                                      smtp_server):
    admitted = await ready(session, smtp_server)
    other = await admitted_sequence(session, name="Shree Coaching", email="hello@shreecoaching.example")
    smtp_server.data_delay = 2.5                  # the server answers after the client gave up
    clock = Clock(ist(TUE, 14, 10))               # first: 09:00 window missed -> moved to 14:11; other: 14:00
    worker = make_worker(factory, clock, website, smtp_timeout=1.0)
    summary = await worker.run_once()
    assert summary.get("uncertain_or_unavailable") is True
    uncertain = (await steps(session, other["sequence_id"]))[0]
    assert uncertain.state == SendState.UNCERTAIN and uncertain.attempts == 1
    uncertain_id = uncertain.id
    assert await active_reasons(session) == ["SEND_RESULT_UNKNOWN"]
    first = (await steps(session, admitted["sequence_id"]))[0]
    assert first.state == SendState.SCHEDULED and first.attempts == 0   # nothing after an unknown result
    assert smtp_server.data_started == 1          # the server had the whole message: it may have been delivered
    clock.at(ist(TUE, 14, 30))
    again = await worker.run_once()
    assert again["global_pause"] == ["SEND_RESULT_UNKNOWN"]
    assert smtp_server.data_started == 1          # exactly one submission; no automatic retry

    service = SendingService(session, CONFIG)
    flag = (await session.execute(select(PauseFlag))).scalars().one()
    with pytest.raises(Conflict):
        await service.clear_pause(flag.id, "founder", "trying to clear early")
    resolved = await service.resolve_uncertain(uncertain_id, "ACCEPTED", "founder", "found in the Sent folder")
    await session.commit()
    assert resolved["state"] == "ACCEPTED" and await active_reasons(session) == []


async def test_a_record_left_submitting_by_a_crash_becomes_uncertain(factory, session, website, smtp_server):
    admitted = await ready(session, smtp_server)
    step1 = (await steps(session, admitted["sequence_id"]))[0]
    step1.state, step1.submitted_at = SendState.SUBMITTING, ist(TUE, 9, 0)
    await session.commit()
    worker = make_worker(factory, Clock(ist(TUE, 9, 5)), website)
    assert await worker.recover() == 1
    assert (await worker.run_once())["global_pause"] == ["SEND_RESULT_UNKNOWN"]
    assert smtp_server.envelopes == []
    assert (await steps(session, admitted["sequence_id"]))[0].state == SendState.UNCERTAIN


@pytest.mark.parametrize("mode", ["down", "unauthorized", "timeout", "refused", "garbage"])
async def test_suppression_service_unavailable_sends_nothing_and_pauses(factory, session, website, smtp_server,
                                                                        mode):
    admitted = await ready(session, smtp_server)
    website.mode = mode
    summary = await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert summary.get("uncertain_or_unavailable") is True and smtp_server.envelopes == []
    assert (await steps(session, admitted["sequence_id"]))[0].state == SendState.SCHEDULED
    assert await active_reasons(session) == ["SUPPRESSION_UNAVAILABLE"]


async def test_the_local_mirror_never_authorises_a_send(factory, session, website, smtp_server):
    """The mirror holds no entry for this address (so locally it looks 'not suppressed'), and the website is down:
    the worker must not fall back to the mirror."""
    await ready(session, smtp_server)
    assert (await session.execute(select(SuppressionMirror))).scalars().all() == []
    website.mode = "down"
    await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert smtp_server.envelopes == []


async def test_missing_timezone_or_country_is_hold_never_a_default(factory, session, website, smtp_server):
    admitted = await ready(session, smtp_server)
    sequence = await session.get(EmailSequence, admitted["sequence_id"])
    sequence.timezone = None
    await session.commit()
    await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert smtp_server.envelopes == []
    assert (await steps(session, admitted["sequence_id"]))[0].hold_reason == "TIMEZONE_MISSING"

    service = SendingService(session, CONFIG)
    no_country = await add_lead(session, name="No Country Salon", email="a@nocountry.example", country=None)
    unknown = await add_lead(session, name="Elsewhere Salon", email="b@elsewhere.example", country="XX")
    result = await service.create_sequences(TUE, [item(no_country), item(unknown)], now=BEFORE)
    assert result["admitted"] == []
    assert [r["code"] for r in result["refused"]] == ["COUNTRY_MISSING", "COUNTRY_UNKNOWN"]


async def test_blank_company_facts_are_hold(factory, session, website, smtp_server):
    admitted = await ready(session, smtp_server)
    blank = SendingConfig(**{**CONFIG.__dict__, "postal_address": "   "})
    await make_worker(factory, Clock(ist(TUE, 9, 1)), website, config=blank).run_once()
    assert smtp_server.envelopes == []
    assert (await steps(session, admitted["sequence_id"]))[0].hold_reason == "COMPANY_FACTS_MISSING"
    row = await add_lead(session, name="Second Salon", email="c@second.example")
    result = await SendingService(session, blank).create_sequences(TUE, [item(row)], now=BEFORE)
    assert result["refused"][0]["code"] == "COMPANY_FACTS_MISSING"


async def test_capacity_and_ramp_are_rechecked_at_send_time(factory, session, website, smtp_server):
    admitted = await ready(session, smtp_server)
    step1 = (await steps(session, admitted["sequence_id"]))[0]
    for n in range(25):                           # 25 campaign messages already left this mailbox today
        session.add(SendRecord(sequence_id=None, step=2, idempotency_key=f"x:{n}", mailbox_id=step1.mailbox_id,
                               recipient_email=f"r{n}@example.org", recipient_hash=email_hash(f"r{n}@example.org"),
                               message_id=f"<x{n}@send-one.example>", scheduled_for=step1.scheduled_for,
                               local_date=TUE, window_label="09:00-11:30", window_start=step1.window_start,
                               window_end=step1.window_end, state=SendState.ACCEPTED,
                               submitted_at=step1.scheduled_for, approved_at=BEFORE, approved_by="founder"))
    await session.commit()
    await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert smtp_server.envelopes == []
    assert (await steps(session, admitted["sequence_id"]))[0].hold_reason == "CAPACITY_FULL"


async def test_ramp_lowered_to_zero_holds_new_first_contacts(factory, session, website, smtp_server):
    admitted = await ready(session, smtp_server)
    await SendingService(session, CONFIG).set_ramp(0, "founder", "stop new contacts", now=BEFORE + timedelta(hours=1))
    await session.commit()
    await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert smtp_server.envelopes == []
    assert (await steps(session, admitted["sequence_id"]))[0].hold_reason == "RAMP_LIMIT_REACHED"


# ─── E1 recheck_before_send, for real ──────────────────────────────────────


class Paid:
    provider = "bouncer"

    async def verify(self, email):
        return VerifierResult("bouncer", VerificationStatus.VALID, {"status": "deliverable"})


def site_check(outcome):
    async def check(url):
        return SiteVisit(listed_url=url, outcome=outcome, note=None if outcome == "ok" else "connect")
    return check


async def site_down_sequence(session, smtp_server):
    business = await add_business(session, name="Shree Retail Showroom", website="https://shreeretail.example")
    await add_capture(session, business, "info@shreeretail.example", source_url="https://shreeretail.example/contact",
                      captured_at=E1_NOW - timedelta(days=2))
    await add_check(session, business, "failed", E1_NOW - timedelta(hours=9))
    await add_check(session, business, "failed", E1_NOW - timedelta(hours=1))
    await e1_service(session, paid=Paid()).evaluate(verify=True, now=E1_NOW)
    row = (await session.execute(select(EmailEligibility).where(
        EmailEligibility.business_id == business.id))).scalar_one()
    assert row.eligible and row.observation_type.value == "SITE_DOWN"
    await add_mailbox(session, port=smtp_server.port)
    await set_ramp(session, 1)
    result = await SendingService(session, CONFIG).create_sequences(TUE, [item(row)], now=E1_NOW)
    await session.commit()
    return result["admitted"][0]


@pytest.mark.parametrize("outcome,sent", [("failed", True), ("ok", False)])
async def test_site_down_lead_is_rechecked_by_e1_right_before_sending(factory, session, website, smtp_server,
                                                                      outcome, sent):
    admitted = await site_down_sequence(session, smtp_server)
    worker = OutreachWorker(factory, CONFIG, website.client(), password_lookup=lambda slug: None,
                            clock=Clock(ist(TUE, 9, 1)),
                            eligibility_factory=lambda s: e1_service(s, paid=Paid(), site_check=site_check(outcome)))
    await worker.run_once()
    assert (len(smtp_server.envelopes) == 1) is sent
    first = (await steps(session, admitted["sequence_id"]))[0]
    if sent:
        assert first.state == SendState.ACCEPTED
    else:
        assert first.state == SendState.CANCELLED and first.cancel_reason == "SITE_RECOVERED"
        sequence = await session.get(EmailSequence, admitted["sequence_id"])
        await session.refresh(sequence)
        assert sequence.state == SequenceState.CANCELLED


async def test_preflight_refuses_without_mailbox_or_shared_values(factory, website):
    worker = OutreachWorker(factory, SendingConfig(None, "short", "not a url", None, None, None), website.client())
    problems = await worker.preflight()
    assert any("OUTREACH_API_KEY" in p for p in problems)
    assert any("OUTREACH_SIGNING_SECRET" in p for p in problems)
    assert any("OUTREACH_PUBLIC_BASE_URL" in p for p in problems)
    assert any("no mailbox is configured" in p for p in problems)
    async with factory() as db:
        await add_mailbox(db, tls=__import__("backend.app.models.sending", fromlist=["TlsMode"]).TlsMode.STARTTLS,
                          host="smtp.send-one.example", port=587)
        await db.commit()
    worker = OutreachWorker(factory, CONFIG, website.client(), password_lookup=lambda slug: None)
    assert await worker.preflight() == ["no enabled mailbox has its MAILBOX_<SLUG>_PASSWORD set in .env"]
    worker = OutreachWorker(factory, CONFIG, website.client(), password_lookup=lambda slug: "set")
    assert await worker.preflight() == []
