"""
E3 fix of E2: SMTP 4xx answers are tried at most 3 times in one window, then in the next permitted window; after 3
windows the record is FAILED (soft) and the sequence HELD with a reason (e2-notes open question 3). Real SMTP server
on 127.0.0.1 (aiosmtpd) answering 451 at RCPT; nothing leaves the machine.
"""

from sqlalchemy import select

from backend.app.models.sending import (
    DeliveryEvent,
    DeliveryEventKind,
    EmailSequence,
    PauseFlag,
    SendRecord,
    SendState,
    SequenceState,
)

from .conftest import TUE, WED, Clock, add_mailbox, admitted_sequence, ist, make_worker, set_ramp

GREYLIST = "451 4.7.1 Greylisted, please try again later"


async def setup(session, smtp_server):
    await add_mailbox(session, port=smtp_server.port)
    await set_ramp(session, 1)
    await session.commit()
    return await admitted_sequence(session)


async def steps(session, sequence_id):
    session.expire_all()
    return (await session.execute(select(SendRecord).where(SendRecord.sequence_id == sequence_id)
                                  .order_by(SendRecord.step))).scalars().all()


async def three_tries(factory, website, clock, day, hour):
    outcomes = []
    for minute in (1, 8, 15):
        clock.at(ist(day, hour, minute))
        summary = await make_worker(factory, clock, website).run_once()
        outcomes.append({k: v for k, v in summary.items() if k in ("not_sent", "failed", "accepted") and v})
    return outcomes


async def test_three_temporary_refusals_move_the_message_to_the_next_window(factory, session, website, smtp_server):
    admitted = await setup(session, smtp_server)
    smtp_server.rcpt_answer = GREYLIST
    clock = Clock(ist(TUE, 9, 1))
    outcomes = await three_tries(factory, website, clock, TUE, 9)
    assert outcomes == [{"not_sent": 1}] * 3
    step1 = (await steps(session, admitted["sequence_id"]))[0]
    assert step1.state == SendState.SCHEDULED and step1.attempts == 3
    assert step1.local_date == TUE and step1.window_label == "14:00-16:30"     # not later in the morning window
    assert step1.hold_reason == "SMTP_RETRY_NEXT_WINDOW:451"
    # a fourth try in the morning window does not happen
    clock.at(ist(TUE, 9, 22))
    assert (await make_worker(factory, clock, website).run_once()).get("not_sent", 0) == 0
    events = (await session.execute(select(DeliveryEvent))).scalars().all()
    assert [e.kind for e in events] == [DeliveryEventKind.SOFT_BOUNCE] * 3
    assert {e.detail["window_start"] for e in events} == {ist(TUE, 9, 0).isoformat()}
    # the greylisting ends: the afternoon window delivers it
    smtp_server.rcpt_answer = None
    clock.at(ist(TUE, 14, 1))
    assert (await make_worker(factory, clock, website).run_once())["accepted"] == 1
    assert len(smtp_server.envelopes) == 1


async def test_after_three_windows_the_record_fails_soft_and_the_sequence_is_held(factory, session, website,
                                                                                 smtp_server):
    admitted = await setup(session, smtp_server)
    smtp_server.rcpt_answer = GREYLIST
    clock = Clock(ist(TUE, 9, 1))
    first = await three_tries(factory, website, clock, TUE, 9)      # window 1: Tue morning
    second = await three_tries(factory, website, clock, TUE, 14)    # window 2: Tue afternoon
    step1 = (await steps(session, admitted["sequence_id"]))[0]
    assert step1.local_date == WED and step1.window_label == "09:00-11:30"
    third = await three_tries(factory, website, clock, WED, 9)      # window 3: Wed morning
    assert first == second == [{"not_sent": 1}] * 3
    assert third == [{"not_sent": 1}, {"not_sent": 1}, {"failed": 1}]

    step1, step2, step3 = await steps(session, admitted["sequence_id"])
    assert step1.state == SendState.FAILED and step1.hold_reason == "SOFT_BOUNCE_LIMIT" and step1.attempts == 9
    assert step1.submitted_at is None                       # nothing was ever accepted
    assert step2.state == step3.state == SendState.CANCELLED
    assert step2.cancel_reason.startswith("SEQUENCE_HELD: SOFT_BOUNCE_LIMIT")
    sequence = await session.get(EmailSequence, admitted["sequence_id"])
    await session.refresh(sequence)
    assert sequence.state == SequenceState.HELD
    assert "3 windows" in sequence.stop_reason and "451" in sequence.stop_reason
    assert smtp_server.envelopes == []
    # a soft limit is about one recipient: no pause flag is raised
    assert (await session.execute(select(PauseFlag))).scalars().all() == []
    # and nothing is tried again
    clock.at(ist(WED, 14, 1))
    summary = await make_worker(factory, clock, website).run_once()
    assert not summary.get("not_sent") and not summary.get("failed") and not summary.get("accepted")


async def test_a_held_sequence_blocks_a_new_sequence_for_the_same_business(factory, session, website, smtp_server):
    """The held prospect waits for a person; a later batch cannot silently start a second sequence."""
    from backend.app.services.sending_service import SendingService
    from .conftest import CONFIG, item
    admitted = await setup(session, smtp_server)
    await SendingService(session, CONFIG).hold_sequence(admitted["sequence_id"], "SOFT_BOUNCE_LIMIT: test")
    await session.commit()
    row_id = admitted["eligibility_id"]
    from backend.app.models.eligibility import EmailEligibility
    row = await session.get(EmailEligibility, row_id)
    result = await SendingService(session, CONFIG).create_sequences(WED, [item(row)], now=ist(TUE, 6))
    assert [r["code"] for r in result["refused"]] == ["ALREADY_IN_SEQUENCE"]
