"""
E2 worker against a real SMTP server on 127.0.0.1 (aiosmtpd): headers on the received raw message, the contract's
token, no HTML part, threading of steps 2 / 3, and the send outcomes (accepted, 5xx, 4xx).
"""

import email
from email import policy

from sqlalchemy import select

from backend.app.engines.sending import smtp as smtp_engine
from backend.app.engines.sending.tokens import email_hash, make_token, verify_token
from backend.app.models.sending import (
    DeliveryEvent,
    DeliveryEventKind,
    EmailSequence,
    PauseFlag,
    PauseScope,
    SendRecord,
    SendState,
    SequenceState,
)
from backend.app.services.sending_service import SendingService

from .conftest import (
    BASE,
    CONFIG,
    NEXT_TUE,
    SECRET,
    TUE,
    Clock,
    add_mailbox,
    admitted_sequence,
    ist,
    make_worker,
    set_ramp,
)

RECIPIENT = "info@glowhair.example"
MAILBOX = "test.founder@send-one.example"


async def setup(session, smtp_server, **kwargs):
    await add_mailbox(session, port=smtp_server.port)
    await set_ramp(session, 1)
    await session.commit()
    return await admitted_sequence(session, **kwargs)


async def records(session, sequence_id):
    session.expire_all()
    return (await session.execute(select(SendRecord).where(SendRecord.sequence_id == sequence_id)
                                  .order_by(SendRecord.step))).scalars().all()


def raw_header(raw: bytes, name: str) -> str:
    """The header exactly as it went over the wire (unfolded)."""
    head = raw.split(b"\r\n\r\n", 1)[0].decode("ascii")
    unfolded = head.replace("\r\n ", " ").replace("\r\n\t", " ")
    lines = [line for line in unfolded.split("\r\n") if line.lower().startswith(name.lower() + ":")]
    assert len(lines) == 1, (name, lines)
    return lines[0].split(":", 1)[1].strip()


async def test_headers_token_and_plain_text_on_the_received_raw_message(factory, session, website, smtp_server):
    admitted = await setup(session, smtp_server)
    summary = await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert summary["accepted"] == 1
    assert len(smtp_server.envelopes) == 1
    envelope = smtp_server.envelopes[0]
    assert envelope.mail_from == MAILBOX and envelope.rcpt_tos == [RECIPIENT]
    raw = envelope.original_content
    step1 = (await records(session, admitted["sequence_id"]))[0]

    token = make_token(email_hash(RECIPIENT), str(step1.id), SECRET)
    url = f"{BASE}/u/{token}"
    assert verify_token(token, SECRET) == {"h": email_hash(RECIPIENT), "m": str(step1.id), "v": 1}
    assert raw_header(raw, "From") == f'"Test Founder, SiteBlitz" <{MAILBOX}>'
    assert raw_header(raw, "To") == RECIPIENT
    assert raw_header(raw, "Subject") == "Glow Hair Studio: no website link in Instagram bio"
    assert raw_header(raw, "Message-ID") == step1.message_id
    assert step1.message_id.startswith("<") and step1.message_id.endswith("@send-one.example>")
    assert raw_header(raw, "Reply-To") == MAILBOX
    assert raw_header(raw, "List-Unsubscribe") == f"<{url}>, <mailto:{MAILBOX}?subject=unsubscribe>"
    assert raw_header(raw, "List-Unsubscribe-Post") == "List-Unsubscribe=One-Click"
    assert raw_header(raw, "Date")
    assert b"In-Reply-To" not in raw and b"References" not in raw

    message = email.message_from_bytes(raw, policy=policy.default)
    assert not message.is_multipart()
    assert message.get_content_type() == "text/plain"
    assert message.get_content_charset() == "utf-8"
    assert message["Content-Transfer-Encoding"] == "quoted-printable"
    assert b"<img" not in raw.lower() and b"text/html" not in raw.lower()
    body = message.get_content()
    assert "₹7,999" in body
    assert body.splitlines()[-1] ==f'Reply "stop" or unsubscribe here: {url}'
    assert "[unsubscribe URL]" not in body          # the writer's placeholder line was replaced

    assert step1.state == SendState.ACCEPTED and step1.smtp_code == 250 and step1.attempts == 1
    assert step1.accepted_at is not None
    sequence = await session.get(EmailSequence, admitted["sequence_id"])
    assert sequence.current_step == 1 and sequence.state == SequenceState.ACTIVE


async def test_steps_two_and_three_thread_under_step_one(factory, session, website, smtp_server):
    admitted = await setup(session, smtp_server)
    clock = Clock(ist(TUE, 9, 1))
    worker = make_worker(factory, clock, website)
    await worker.run_once()
    step1, step2, step3 = await records(session, admitted["sequence_id"])
    assert step2.local_date == NEXT_TUE and step2.subject == "Re: " + step1.subject

    clock.at(ist(NEXT_TUE, 9, 1))
    assert (await worker.run_once())["held"] == 1                 # step 2 has no approved text yet
    assert (await records(session, admitted["sequence_id"]))[1].hold_reason == "NOT_APPROVED"
    assert len(smtp_server.envelopes) == 1

    service = SendingService(session, CONFIG)
    await service.approve_follow_up(step2.id, "Following up on my note: shall I make the sample page?\n\nTest Founder",
                                    "founder", "t2-v1", now=clock())
    await session.commit()
    assert (await worker.run_once())["accepted"] == 1
    raw2 = smtp_server.envelopes[1].original_content
    assert raw_header(raw2, "In-Reply-To") == step1.message_id
    assert raw_header(raw2, "References") == step1.message_id
    assert raw_header(raw2, "Subject") == "Re: Glow Hair Studio: no website link in Instagram bio"

    step3 = (await records(session, admitted["sequence_id"]))[2]
    await service.approve_follow_up(step3.id, "I'll close this note here. Thank you.\n\nTest Founder", "founder",
                                    "t3-v1", now=clock())
    await session.commit()
    clock.at(step3.scheduled_for)
    assert (await worker.run_once())["accepted"] == 1
    raw3 = smtp_server.envelopes[2].original_content
    assert raw_header(raw3, "In-Reply-To") == step2.message_id
    assert raw_header(raw3, "References") == f"{step1.message_id} {step2.message_id}"
    sequence = await session.get(EmailSequence, admitted["sequence_id"])
    await session.refresh(sequence)
    assert sequence.state == SequenceState.COMPLETED and sequence.current_step == 3


async def test_nothing_is_sent_before_the_window_opens(factory, session, website, smtp_server):
    await setup(session, smtp_server)
    summary = await make_worker(factory, Clock(ist(TUE, 8, 59)), website).run_once()
    assert smtp_server.envelopes == [] and website.checks == 0
    assert summary["accepted"] == 0


async def test_a_missed_window_moves_to_the_next_window_with_capacity(factory, session, website, smtp_server):
    admitted = await setup(session, smtp_server)
    clock = Clock(ist(TUE, 11, 45))            # the worker was not running in the morning window
    summary = await make_worker(factory, clock, website).run_once()
    assert summary["moved"] == 1 and smtp_server.envelopes == []
    step1 = (await records(session, admitted["sequence_id"]))[0]
    assert step1.local_date == TUE and step1.window_label == "14:00-16:30"
    clock.at(ist(TUE, 14, 1))
    assert (await make_worker(factory, clock, website).run_once())["accepted"] == 1


async def test_hard_bounce_at_rcpt_fails_suppresses_and_pauses_the_batch(factory, session, website, smtp_server):
    admitted = await setup(session, smtp_server)
    smtp_server.rcpt_answer = "550 5.1.1 <info@glowhair.example>: Recipient address rejected: User unknown"
    summary = await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert summary["failed"] == 1 and smtp_server.envelopes == []
    step1, step2, step3 = await records(session, admitted["sequence_id"])
    assert step1.state == SendState.FAILED and step1.smtp_code == 550 and step1.smtp_status == "5.1.1"
    assert step2.state == step3.state == SendState.CANCELLED
    sequence = await session.get(EmailSequence, admitted["sequence_id"])
    await session.refresh(sequence)
    assert sequence.state == SequenceState.STOPPED_BOUNCE
    assert website.added == [{"hash": email_hash(RECIPIENT), "reason": "hard_bounce",
                              "source": f"smtp:send_record:{step1.id}"}]
    flags = (await session.execute(select(PauseFlag))).scalars().all()
    assert [(f.scope, f.scope_value, f.reason_code) for f in flags] == [
        (PauseScope.SOURCE_BATCH, "pool_e1:2026-11-12", "HARD_BOUNCE")]
    events = (await session.execute(select(DeliveryEvent))).scalars().all()
    assert [e.kind for e in events] == [DeliveryEventKind.HARD_BOUNCE]


async def test_policy_rejection_after_data_pauses_the_sending_domain(factory, session, website, smtp_server):
    await setup(session, smtp_server)
    smtp_server.data_answer = "550 5.7.26 This message does not pass authentication checks"
    summary = await make_worker(factory, Clock(ist(TUE, 9, 1)), website).run_once()
    assert summary["failed"] == 1
    flags = (await session.execute(select(PauseFlag))).scalars().all()
    assert [(f.scope, f.scope_value, f.reason_code) for f in flags] == [
        (PauseScope.DOMAIN, "send-one.example", "POLICY_REJECTION")]
    assert website.added == []      # a policy block says nothing about the address: not suppressed


async def test_temporary_refusal_is_not_sent_and_tried_again_later(factory, session, website, smtp_server):
    admitted = await setup(session, smtp_server)
    smtp_server.rcpt_answer = "451 4.7.1 Greylisted, please try again later"
    clock = Clock(ist(TUE, 9, 1))
    summary = await make_worker(factory, clock, website).run_once()
    assert summary["not_sent"] == 1
    step1 = (await records(session, admitted["sequence_id"]))[0]
    assert step1.state == SendState.SCHEDULED and step1.submitted_at is None and step1.attempts == 1
    assert step1.hold_reason == "SMTP_NOT_SENT:rcpt:451"
    smtp_server.rcpt_answer = None
    clock.at(ist(TUE, 9, 8))
    assert (await make_worker(factory, clock, website).run_once())["accepted"] == 1
    assert len(smtp_server.envelopes) == 1


def test_smtp_adapter_logs_in_and_dot_stuffs(smtp_server):
    from aiosmtpd.controller import Controller
    from aiosmtpd.smtp import AuthResult

    from .conftest import Collector, free_port

    def authenticator(server, session, envelope, mechanism, auth_data):
        return AuthResult(success=auth_data.login == b"user" and auth_data.password == b"secret-pw")

    collector = Collector()
    controller = Controller(collector, hostname="127.0.0.1", port=free_port(), authenticator=authenticator,
                            auth_require_tls=False)
    controller.start()
    try:
        data = b"Subject: t\r\n\r\n.leading dot line\r\nlast\r\n"
        good = smtp_engine.submit(smtp_engine.SmtpConfig("127.0.0.1", controller.port, "none", "user", "secret-pw",
                                                         5), "a@send-one.example", "b@example.org", data)
        assert good.outcome == smtp_engine.ACCEPTED and good.code == 250
        assert b"\r\n.leading dot line\r\n" in collector.envelopes[0].original_content
        bad = smtp_engine.submit(smtp_engine.SmtpConfig("127.0.0.1", controller.port, "none", "user", "wrong", 5),
                                 "a@send-one.example", "b@example.org", data)
        assert bad.outcome == smtp_engine.NOT_SENT and bad.mailbox_problem and bad.phase == "auth"
    finally:
        controller.stop()
    refused = smtp_engine.submit(smtp_engine.SmtpConfig("smtp.example.org", 25, "none", "u", None, 5),
                                 "a@send-one.example", "b@example.org", b"x")
    assert refused.outcome == smtp_engine.NOT_SENT and "loopback" in refused.response
