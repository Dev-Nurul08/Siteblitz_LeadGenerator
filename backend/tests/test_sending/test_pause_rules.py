"""E2 automatic pause / stop rules (spec row 11): every rule, on a throw-away database, no network."""

from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import select

from backend.app.engines.sending import dsn
from backend.app.engines.sending import pause_rules as rules
from backend.app.engines.sending.tokens import email_hash
from backend.app.models.business import Business
from backend.app.models.sending import (
    DeliveryEvent,
    EmailSequence,
    PauseFlag,
    PauseLevel,
    PauseScope,
    SendRecord,
    SendState,
    SequenceState,
    SuppressionMirror,
)
from backend.app.services.delivery_rules_service import DeliveryRulesService
from backend.app.services.sending_service import SendingService

from .conftest import BEFORE, CONFIG, IST, TUE, add_lead, add_mailbox, ist, item, set_ramp

T0 = ist(TUE, 9, 0)
FIXTURES = Path(__file__).parent / "fixtures" / "dsn"


def services(session, website):
    sending = SendingService(session, CONFIG)
    return sending, DeliveryRulesService(sending, website.client())


async def sent(session, box, recipient: str, at: datetime, source="pool_e1", batch="pool_e1:2026-11-12", step=1,
               approved=True, sequence=None, state=SendState.ACCEPTED) -> SendRecord:
    if sequence is None:
        business = Business(name=recipient, normalized_name=recipient, country_code="IN")
        session.add(business)
        await session.flush()
        sequence = EmailSequence(business_id=business.id, mailbox_id=box.id, recipient_email=recipient,
                                 recipient_hash=email_hash(recipient), country="IN", timezone="Asia/Kolkata",
                                 source=source, source_batch=batch, state=SequenceState.ACTIVE)
        session.add(sequence)
        await session.flush()
    record = SendRecord(sequence_id=sequence.id, step=step, idempotency_key=f"seq:{sequence.id}:step:{step}",
                        mailbox_id=box.id, recipient_email=recipient, recipient_hash=email_hash(recipient),
                        message_id=f"<{sequence.id}-{step}@send-one.example>", subject="s", body="b",
                        scheduled_for=at, local_date=TUE, window_label="09:00-11:30", window_start=T0,
                        window_end=T0 + timedelta(hours=2, minutes=30), state=state, submitted_at=at,
                        approved_at=BEFORE if approved else None, approved_by="founder" if approved else None)
    session.add(record)
    await session.flush()
    return record


async def flags(session, active=True):
    stmt = select(PauseFlag).order_by(PauseFlag.id)
    if active:
        stmt = stmt.where(PauseFlag.cleared_at.is_(None))
    return [(f.scope.value, f.scope_value, f.level.value, f.reason_code)
            for f in (await session.execute(stmt)).scalars().all()]


async def test_first_hard_bounce_suppresses_and_pauses_the_batch_and_the_second_stops_the_source(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    r1, r2, r3 = [await sent(session, box, f"r{i}@example.org", T0 + timedelta(minutes=i)) for i in range(3)]
    result = await rules_svc.record_hard_bounce(r1, "dsn", T0 + timedelta(hours=1))
    assert website.added == [{"hash": email_hash("r0@example.org"), "reason": "hard_bounce",
                              "source": f"dsn:send_record:{r1.id}"}]
    assert await flags(session) == [("SOURCE_BATCH", "pool_e1:2026-11-12", "PAUSE", "HARD_BOUNCE")]
    assert result["actions"] == ["PAUSE SOURCE_BATCH pool_e1:2026-11-12"]
    sequence = await session.get(EmailSequence, r1.sequence_id)
    assert sequence.state == SequenceState.STOPPED_BOUNCE
    assert (await rules_svc.record_hard_bounce(r1, "dsn", T0 + timedelta(hours=2)))["duplicate"] is True
    await rules_svc.record_hard_bounce(r2, "dsn", T0 + timedelta(hours=3))
    assert ("SOURCE", "pool_e1", "STOP", "HARD_BOUNCE_RATE") in await flags(session)


async def test_hard_bounce_rate_counts_each_recipient_once(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    first = await sent(session, box, "same@example.org", T0)
    second = await sent(session, box, "same@example.org", T0 + timedelta(days=7), step=2,
                        sequence=await session.get(EmailSequence, first.sequence_id))
    await rules_svc.record_hard_bounce(first, "dsn", T0 + timedelta(hours=1))
    await rules_svc.record_hard_bounce(second, "dsn", T0 + timedelta(days=7, hours=1))
    assert ("SOURCE", "pool_e1", "STOP", "HARD_BOUNCE_RATE") not in await flags(session)
    assert rules.latest_distinct(["a", "b", "a", "c"], 2) == ["a", "b"]
    assert rules.hard_bounce_stop(["a", "b"], {"a"}) is False and rules.hard_bounce_stop(["a", "b"], {"a", "b"})


async def test_a_bounce_outside_the_latest_100_distinct_recipients_does_not_count(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    old = await sent(session, box, "old@example.org", T0 - timedelta(days=30))
    await rules_svc.record_hard_bounce(old, "dsn", T0 - timedelta(days=29))
    newer = [await sent(session, box, f"n{i}@example.org", T0 + timedelta(minutes=i)) for i in range(100)]
    await rules_svc.record_hard_bounce(newer[-1], "dsn", T0 + timedelta(hours=3))
    assert ("SOURCE", "pool_e1", "STOP", "HARD_BOUNCE_RATE") not in await flags(session)


async def test_complaints_pause_then_stop_within_30_days(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    a, b, c = [await sent(session, box, f"c{i}@example.org", T0) for i in range(3)]
    await rules_svc.record_complaint(a, a.recipient_hash, credible=False, origin="reply", now=T0 + timedelta(days=1))
    assert await flags(session) == []                                # not credible: suppression only
    assert website.added[-1]["reason"] == "complaint"
    await rules_svc.record_complaint(b, b.recipient_hash, credible=True, origin="reply", now=T0 + timedelta(days=2))
    assert await flags(session) == [("GLOBAL", "", "PAUSE", "COMPLAINT")]
    await rules_svc.record_complaint(c, c.recipient_hash, credible=True, origin="reply", now=T0 + timedelta(days=20))
    assert ("GLOBAL", "", "STOP", "COMPLAINTS_30D") in await flags(session)
    assert rules.complaint_stop([T0, T0 + timedelta(days=31)], T0 + timedelta(days=31)) is False


async def test_policy_rejections_pause_the_domain_then_stop_it_at_three_in_24_hours(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    records = [await sent(session, box, f"p{i}@example.org", T0) for i in range(4)]
    await rules_svc.record_policy_rejection(records[0], "smtp", T0)
    assert await flags(session) == [("DOMAIN", "send-one.example", "PAUSE", "POLICY_REJECTION")]
    await rules_svc.record_policy_rejection(records[1], "smtp", T0 + timedelta(hours=20))
    await rules_svc.record_policy_rejection(records[2], "smtp", T0 + timedelta(hours=30))   # first is now > 24 h old
    assert ("DOMAIN", "send-one.example", "STOP", "POLICY_REJECTIONS_24H") not in await flags(session)
    await rules_svc.record_policy_rejection(records[3], "smtp", T0 + timedelta(hours=31))
    assert ("DOMAIN", "send-one.example", "STOP", "POLICY_REJECTIONS_24H") in await flags(session)
    assert website.added == []                                     # never suppresses the address


async def test_integrity_incidents_pause_everything_once(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    await sent(session, box, "u@example.org", T0, approved=False)
    found = await rules_svc.integrity_audit(T0 + timedelta(minutes=5))
    assert found[0].startswith("UNAPPROVED_SEND") and await flags(session) == [("GLOBAL", "", "PAUSE",
                                                                                "UNAPPROVED_SEND")]
    flag = (await session.execute(select(PauseFlag))).scalars().one()
    await sending.clear_pause(flag.id, "founder", "root cause fixed, regression test added")
    assert await rules_svc.integrity_audit(T0 + timedelta(minutes=10)) == []   # the same incident is not re-raised
    assert await flags(session) == []

    one = await sent(session, box, "dup@example.org", T0)
    await sent(session, box, "dup@example.org", T0 + timedelta(minutes=1))     # a second sequence, same step
    assert any(f.startswith("DUPLICATE_SEND") for f in await rules_svc.integrity_audit(T0 + timedelta(minutes=15)))

    session.add(SuppressionMirror(email_hash=email_hash("late@example.org"), reason="unsubscribe_one_click",
                                  suppressed_at=T0, fetched_at=T0))
    await sent(session, box, "late@example.org", T0 + timedelta(minutes=30))   # submitted after we knew
    assert any(f.startswith("SUPPRESSED_SEND") for f in await rules_svc.integrity_audit(T0 + timedelta(hours=1)))
    reasons = {f[3] for f in await flags(session)}
    assert reasons == {"DUPLICATE_SEND", "SUPPRESSED_SEND"}
    assert one.integrity_flag == "DUPLICATE_SEND"


async def test_a_failed_suppression_write_blocks_everything(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    record = await sent(session, box, "w@example.org", T0)
    website.mode = "down"
    await rules_svc.record_hard_bounce(record, "dsn", T0 + timedelta(hours=1))
    assert ("GLOBAL", "", "PAUSE", "SUPPRESSION_WRITE_FAILED") in await flags(session)
    assert (await session.execute(select(SuppressionMirror.email_hash))).scalars().all() == [record.recipient_hash]


async def test_unknown_state_pauses_block_every_send(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    record = await sent(session, box, "x@example.org", T0, state=SendState.UNCERTAIN)
    await rules_svc.record_suppression_unavailable("HTTP 503", T0)
    await rules_svc.record_reconciliation_incomplete("mailbox TEST1 not read", T0)
    await rules_svc.record_send_result_unknown(record, T0)
    assert [f[3] for f in await flags(session)] == ["SUPPRESSION_UNAVAILABLE", "INBOX_NOT_RECONCILED",
                                                   "SEND_RESULT_UNKNOWN"]
    sequence = await session.get(EmailSequence, record.sequence_id)
    blocks = sending.blocking(await sending.active_pauses(), step=2, mailbox=box, sequence=sequence)
    assert len(blocks) == 3


async def test_pause_scopes_block_only_what_they_name(session, website):
    sending, _ = services(session, website)
    box = await add_mailbox(session)
    other = await add_mailbox(session, slug="TEST2", address="second.founder@send-two.example")
    record = await sent(session, box, "s@example.org", T0)
    sequence = await session.get(EmailSequence, record.sequence_id)
    await sending.raise_pause(PauseScope.DOMAIN, "POLICY_REJECTION", "send-one.example", now=T0)
    await sending.raise_pause(PauseScope.SOURCE_BATCH, "HARD_BOUNCE", "other:batch", now=T0)
    active = await sending.active_pauses()
    assert [f.reason_code for f in sending.blocking(active, step=2, mailbox=box, sequence=sequence)] == [
        "POLICY_REJECTION"]
    assert sending.blocking(active, step=2, mailbox=other, sequence=sequence) == []
    await sending.raise_pause(PauseScope.MAILBOX, "SMTP_UNAVAILABLE", str(other.id), now=T0)
    assert len(sending.blocking(await sending.active_pauses(), step=1, mailbox=other, sequence=sequence)) == 1
    again = await sending.raise_pause(PauseScope.DOMAIN, "POLICY_REJECTION", "send-one.example", now=T0)
    assert len(await sending.active_pauses()) == 3 and again.reason_code == "POLICY_REJECTION"   # not duplicated


async def test_unanswered_interested_reply_stops_new_first_contacts_only(session, website):
    sending, rules_svc = services(session, website)
    await add_mailbox(session)
    await set_ramp(session, 1)
    monday = datetime(2026, 11, 16, 10, 0, tzinfo=IST)
    assert await rules_svc.check_reply_backlog(monday, datetime(2026, 11, 17, 9, 59, tzinfo=IST)) is False
    assert await flags(session) == []
    assert await rules_svc.check_reply_backlog(monday, datetime(2026, 11, 17, 10, 1, tzinfo=IST)) is True
    assert await flags(session) == [("NEW_CONTACTS", "", "PAUSE", "REPLY_BACKLOG")]
    active = await sending.active_pauses()
    assert sending.blocking(active, step=1, mailbox=None, sequence=None)
    assert sending.blocking(active, step=2, mailbox=None, sequence=None) == []   # follow-ups still go out
    row = await add_lead(session, name="Backlog Salon", email="d@backlog.example")
    refused = await sending.create_sequences(TUE, [item(row)], now=BEFORE)
    assert refused["refused"][0]["code"] == "PAUSED"
    assert await rules_svc.check_reply_backlog(None, datetime(2026, 11, 17, 12, 0, tzinfo=IST)) is False
    assert await flags(session) == []                                      # cleared once the backlog is empty
    friday = datetime(2026, 11, 13, 16, 0, tzinfo=IST)
    assert rules.reply_deadline(friday, IST) == datetime(2026, 11, 16, 16, 0, tzinfo=IST)
    saturday = datetime(2026, 11, 14, 11, 0, tzinfo=IST)
    assert rules.reply_deadline(saturday, IST) == datetime(2026, 11, 17, 0, 0, tzinfo=IST)


async def test_a_parsed_dsn_is_matched_by_message_id_and_applied(session, website):
    sending, rules_svc = services(session, website)
    box = await add_mailbox(session)
    record = await sent(session, box, "owner.eight@example.org", T0)
    raw = (FIXTURES / "08_postfix_user_unknown.eml").read_text().replace("<aaaaaaaa-0008@send-one.example>",
                                                                          record.message_id)
    result = await rules_svc.record_bounce(dsn.parse_bounce(raw), now=T0 + timedelta(hours=1))
    assert result["matched"] and result["kind"] == "HARD" and result["send_record_id"] == record.id
    events = (await session.execute(select(DeliveryEvent))).scalars().all()
    assert [(e.kind.value, e.smtp_status, e.origin) for e in events] == [("HARD_BOUNCE", "5.1.1", "dsn")]
    soft = (FIXTURES / "10_postfix_delayed.eml").read_text().replace("<aaaaaaaa-0010@send-one.example>",
                                                                    record.message_id)
    assert (await rules_svc.record_bounce(dsn.parse_bounce(soft), now=T0))["kind"] == "SOFT"
    assert (await rules_svc.record_bounce(dsn.parse_bounce("Subject: hello\n\nhi"), now=T0))["matched"] is False


async def test_the_display_mirror_copies_the_website_list(session, website):
    _, rules_svc = services(session, website)
    website.suppressed.update({email_hash("a@example.org"), email_hash("b@example.org")})
    now = datetime(2026, 11, 17, 3, 0, tzinfo=timezone.utc)
    assert await rules_svc.sync_mirror(None, now) == 2
    assert await rules_svc.sync_mirror(None, now) == 0      # the repeated boundary item is not stored twice
