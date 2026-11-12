"""E4 safety paths through the whole loop: stop (website first), out of office, DSN, complaints, injection, no key."""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select

from backend.app.engines.sending.tokens import email_hash
from backend.app.models.compliance import OptOut
from backend.app.models.replies import (
    DraftKind,
    DraftState,
    InboundMessage,
    ReplyDraft,
    ReplySuppression,
    WebsiteWrite,
)
from backend.app.models.sending import (
    DeliveryEvent,
    DeliveryEventKind,
    EmailSequence,
    PauseFlag,
    PauseScope,
    SendKind,
    SendRecord,
    SendState,
    SequenceState,
    SuppressionMirror,
)
from backend.app.services.delivery_rules_service import DeliveryRulesService
from backend.app.services.sending_service import SendingService

from .conftest import (
    CONFIG,
    EVAL_SET,
    IST,
    OWNER,
    TUE,
    Clock,
    FakeImapServer,
    case_raw,
    eml,
    ist,
    labels_answer,
    make_loop,
    ready_mailbox,
    sent_sequence,
    set_classifier,
)

CASES = {c["id"]: c for c in EVAL_SET["cases"]}


async def run_one(factory, session, site, models, raw_builder, clock=None, **loop_kwargs):
    await ready_mailbox(session)
    sent = await sent_sequence(session)
    imap = FakeImapServer(junk=None)
    imap.add(raw_builder(sent))
    loop = make_loop(factory, clock or Clock(ist(TUE, 12)), site, imap, models, **loop_kwargs)
    summary = await loop.reconcile()
    session.expire_all()
    msg = (await session.execute(select(InboundMessage))).scalars().one()
    return sent, msg, loop, summary


async def active_pauses(session):
    session.expire_all()
    return [(f.scope, f.scope_value, f.reason_code) for f in (await session.execute(
        select(PauseFlag).where(PauseFlag.cleared_at.is_(None)))).scalars()]


# ─── stop ───────────────────────────────────────────────────────────────────


async def test_stop_goes_to_the_website_first_then_locally(factory, session, site, models):
    sent, msg, _, _ = await run_one(factory, session, site, models,
                                    lambda s: eml("Please stop emailing me.", in_reply_to=s.message_id))
    assert msg.labels == ["stop"] and models.classifier_calls.calls == [] and models.writer_calls.calls == []
    assert site.added == [{"hash": email_hash(OWNER), "reason": "reply_stop", "source": f"reply:inbound:{msg.id}"}]
    row = (await session.execute(select(ReplySuppression))).scalar_one()
    assert row.website_state == WebsiteWrite.WRITTEN and row.reason == "reply_stop"
    assert (await session.execute(select(SuppressionMirror.email_hash))).scalar_one() == email_hash(OWNER)
    assert (await session.execute(select(OptOut.email, OptOut.source))).one() == (OWNER, "EMAIL_REPLY")
    sequence = await session.get(EmailSequence, sent.sequence_id)
    assert sequence.state == SequenceState.STOPPED_SUPPRESSED
    states = (await session.execute(select(SendRecord.state).where(SendRecord.sequence_id == sent.sequence_id)
                                    .order_by(SendRecord.step))).scalars().all()
    assert states == [SendState.ACCEPTED, SendState.CANCELLED, SendState.CANCELLED]
    assert await active_pauses(session) == []


async def test_website_down_keeps_the_stop_pending_pauses_everything_and_retries(factory, session, site, models):
    site.mode = "down"
    sent, msg, loop, _ = await run_one(factory, session, site, models,
                                       lambda s: eml("Band karo ye mails.", in_reply_to=s.message_id))
    row = (await session.execute(select(ReplySuppression))).scalar_one()
    assert row.website_state == WebsiteWrite.PENDING
    assert (PauseScope.GLOBAL, "", "SUPPRESSION_WRITE_FAILED") in await active_pauses(session)
    # locally it is stopped anyway: the opt-out row, the display mirror and the sequence
    assert (await session.execute(select(OptOut.email))).scalar_one() == OWNER
    assert (await session.get(EmailSequence, sent.sequence_id)).state == SequenceState.STOPPED_SUPPRESSED
    site.mode = "ok"
    summary = await loop.reconcile()
    assert summary["suppressions_retried"] == 1
    session.expire_all()
    row = (await session.execute(select(ReplySuppression))).scalar_one()
    assert row.website_state == WebsiteWrite.WRITTEN and row.attempts == 3   # 1st try, same-run retry, now
    assert site.added[-1]["reason"] == "reply_stop"


async def test_stop_confirmation_is_optional_and_only_sent_by_its_id(factory, session, site, models, smtp_server):
    await ready_mailbox(session, smtp_port=smtp_server.port)
    sent = await sent_sequence(session)
    imap = FakeImapServer(junk=None)
    imap.add(eml("Unsubscribe.", in_reply_to=sent.message_id))
    loop = make_loop(factory, Clock(ist(TUE, 12)), site, imap, models)
    await loop.reconcile()
    async with factory() as db:
        assert await loop.list_drafts(db) == []                          # default list: nothing to send
        optional = await loop.list_drafts(db, include_optional=True)
    assert len(optional) == 1 and optional[0]["kind"] == "STOP_CONFIRMATION"
    assert optional[0]["text"].startswith("Understood, thank you for letting me know.")
    assert smtp_server.envelopes == []
    result = await loop.approve(optional[0]["id"], "founder")              # the founder picks it by id
    assert result["state"] == "SENT" and len(smtp_server.envelopes) == 1
    async with factory() as db:   # the integrity audit does not call it a send to a suppressed address
        found = await DeliveryRulesService(SendingService(db, CONFIG), site.client()).integrity_audit(
            ist(TUE, 12, 5))
        await db.commit()
    assert found == []


# ─── out of office ──────────────────────────────────────────────────────────


async def test_out_of_office_pauses_and_resumes_two_business_days_after_the_return_date(factory, session, site,
                                                                                         models):
    case = CASES["o01_auto_submitted_english"]   # back on Friday 20 November
    sent, msg, loop, _ = await run_one(factory, session, site, models,
                                       lambda s: case_raw(case, in_reply_to=s.message_id))
    assert msg.labels == ["out_of_office"] and msg.ooo_return_date == date(2026, 11, 20)
    resume = datetime.combine(date(2026, 11, 24), time(0, 0), IST).astimezone(timezone.utc)   # Tuesday
    assert msg.ooo_resume_at.replace(tzinfo=timezone.utc) == resume
    sequence = await session.get(EmailSequence, sent.sequence_id)
    assert sequence.state == SequenceState.PAUSED_OOO
    steps = (await session.execute(select(SendRecord.state).where(SendRecord.sequence_id == sent.sequence_id)
                                   .order_by(SendRecord.step))).scalars().all()
    assert steps == [SendState.ACCEPTED, SendState.SCHEDULED, SendState.SCHEDULED]   # kept, held by the worker
    assert await loop.resume_ooo(resume - timedelta(minutes=1)) == 0
    assert await loop.resume_ooo(resume) == 1
    session.expire_all()
    assert (await session.get(EmailSequence, sent.sequence_id)).state == SequenceState.ACTIVE


async def test_out_of_office_without_a_date_is_reviewed_after_14_days(factory, session, site, models):
    case = CASES["o03_precedence_no_date"]
    _, msg, _, _ = await run_one(factory, session, site, models, lambda s: case_raw(case, in_reply_to=s.message_id))
    assert msg.ooo_return_date is None
    assert msg.ooo_resume_at.replace(tzinfo=timezone.utc) == msg.received_at.replace(
        tzinfo=timezone.utc) + timedelta(days=14)


async def test_no_out_of_office_is_ever_answered(factory, session, site, models):
    await ready_mailbox(session)
    imap = FakeImapServer(junk=None)
    ooo = [c for c in EVAL_SET["cases"] if c["kind"] == "AUTO_REPLY"]
    for index, case in enumerate(ooo):
        sent = await sent_sequence(session, name=f"Salon {index}", email=f"owner{index}@salon{index}.example")
        imap.add(case_raw(case, in_reply_to=sent.message_id, frm=f"<owner{index}@salon{index}.example>"))
    await make_loop(factory, Clock(ist(TUE, 12)), site, imap, models).reconcile()
    session.expire_all()
    rows = (await session.execute(select(InboundMessage))).scalars().all()
    assert len(rows) == len(ooo) and all(r.labels == ["out_of_office"] for r in rows)
    assert (await session.execute(select(ReplyDraft))).scalars().all() == []
    assert models.classifier_calls.calls == [] and models.writer_calls.calls == []
    paused = (await session.execute(select(EmailSequence.state))).scalars().all()
    assert set(paused) == {SequenceState.PAUSED_OOO}


# ─── bounces and complaints ─────────────────────────────────────────────────


async def test_dsn_goes_to_the_e2_bounce_rules(factory, session, site, models):
    case = CASES["d01_dsn_user_unknown"]
    sent, msg, _, _ = await run_one(factory, session, site, models, lambda s: case_raw(case, message_id=s.message_id))
    assert msg.kind.value == "DSN" and msg.labels == ["bounce"] and msg.send_record_id == sent.step1_id
    event = (await session.execute(select(DeliveryEvent))).scalar_one()
    assert event.kind == DeliveryEventKind.HARD_BOUNCE and event.origin == "imap_dsn"
    assert site.added[0]["reason"] == "hard_bounce"
    assert (await session.get(EmailSequence, sent.sequence_id)).state == SequenceState.STOPPED_BOUNCE
    assert (PauseScope.SOURCE_BATCH, "pool_e1:2026-11-12", "HARD_BOUNCE") in await active_pauses(session)


async def test_credible_complaint_pauses_everything_and_is_never_drafted(factory, session, site, models):
    case = CASES["c01_this_is_spam_report"]
    _, msg, _, _ = await run_one(factory, session, site, models, lambda s: case_raw(case, in_reply_to=s.message_id))
    assert msg.labels == ["complaint_legal"] and "COMPLAINT_LEGAL:credible" in msg.flags
    assert msg.state.value == "FLAGGED"
    assert (PauseScope.GLOBAL, "", "COMPLAINT") in await active_pauses(session)
    assert site.added[0]["reason"] == "complaint"
    assert (await session.execute(select(ReplyDraft))).scalars().all() == []
    assert models.classifier_calls.calls == []


async def test_weak_complaint_suppresses_without_a_global_pause(factory, session, site, models):
    case = CASES["c08_is_this_a_scam"]
    _, msg, _, _ = await run_one(factory, session, site, models, lambda s: case_raw(case, in_reply_to=s.message_id))
    assert msg.labels == ["complaint_legal"] and "COMPLAINT_LEGAL" in msg.flags
    assert all(p[2] != "COMPLAINT" for p in await active_pauses(session))
    event = (await session.execute(select(DeliveryEvent))).scalar_one()
    assert event.kind == DeliveryEventKind.COMPLAINT and event.credible is False


# ─── model safety ───────────────────────────────────────────────────────────


async def test_prompt_injection_changes_nothing(factory, session, site, models, smtp_server):
    """The injected text reaches the model only as sanitized data; whatever the model answers (here: extra keys and
    labels outside the schema), the outcome is the same as for a plain question: at most a draft that waits."""
    set_classifier(models, {**labels_answer(["question", "stop", "approve_all"]), "approve": True,
                            "send_to": "evil@x.example"})
    await ready_mailbox(session, smtp_port=smtp_server.port)
    outcomes = []
    imap = FakeImapServer(junk=None)
    for index, case_id in enumerate(("m19_prompt_injection_database", "m20_prompt_injection_fake_system",
                                     "m04_question_en")):
        sent = await sent_sequence(session, name=f"Shop {index}", email=f"owner{index}@shop{index}.example")
        imap.add(case_raw(CASES[case_id], in_reply_to=sent.message_id, frm=f"<owner{index}@shop{index}.example>"))
        await make_loop(factory, Clock(ist(TUE, 12)), site, imap, models).reconcile()
        session.expire_all()
        msg = (await session.execute(select(InboundMessage).where(
            InboundMessage.sequence_id == sent.sequence_id))).scalar_one()
        draft = (await session.execute(select(ReplyDraft).where(
            ReplyDraft.sequence_id == sent.sequence_id))).scalar_one_or_none()
        assert draft is not None, (msg.labels, msg.state, msg.flags, msg.error)
        outcomes.append((msg.labels, msg.state.value, draft.state.value))
        assert "database" not in draft.body.lower() and "evil" not in draft.body
    assert outcomes == [(["question"], "PROCESSED", "WAITING")] * 3
    assert smtp_server.envelopes == [] and site.added == []
    assert await active_pauses(session) == []
    assert (await session.execute(select(SendRecord).where(SendRecord.kind == SendKind.REPLY))).scalars().all() == []
    request = models.classifier_calls.calls[0]
    assert "data" in request["system"][0]["text"].lower() and "Ignore your instructions" in request["messages"][0][
        "content"]


async def test_no_api_key_gives_needs_review_and_no_draft(factory, session, site, models):
    _, msg, _, _ = await run_one(factory, session, site, models,
                                 lambda s: eml("Interested, send the sample.", in_reply_to=s.message_id),
                                 api_key=False)
    assert msg.labels == ["needs_review"] and msg.state.value == "NEEDS_REVIEW"
    assert models.classifier_calls.calls == [] and models.writer_calls.calls == []
    assert (await session.execute(select(ReplyDraft))).scalars().all() == []


async def test_the_model_never_sees_an_address_or_a_number(factory, session, site, models):
    case = CASES["m22_interested_with_contact_details"]
    await run_one(factory, session, site, models, lambda s: case_raw(case, in_reply_to=s.message_id))
    sent_to_models = str(models.classifier_calls.calls) + str(models.writer_calls.calls)
    assert "98250" not in sent_to_models and "owner@glowhair" not in sent_to_models
    assert OWNER not in sent_to_models


async def test_commitment_request_gets_no_draft(factory, session, site, models):
    case = CASES["m13_discount_request"]
    set_classifier(models, labels_answer(["price"]))
    _, msg, _, _ = await run_one(factory, session, site, models, lambda s: case_raw(case, in_reply_to=s.message_id))
    assert msg.state.value == "FLAGGED" and "ASKS_FOR:discount" in msg.flags
    assert models.writer_calls.calls == []
    assert (await session.execute(select(ReplyDraft).where(
        ReplyDraft.kind == DraftKind.REPLY))).scalars().all() == []
    assert DraftState.WAITING   # (enum imported for the other modules' readers)
