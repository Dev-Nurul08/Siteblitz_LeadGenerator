"""E4 IMAP reconciliation: read-only reads of INBOX + junk, UIDs, UIDVALIDITY, matching, the 24 h guard."""

from datetime import timedelta

from sqlalchemy import select

from backend.app.models.replies import ImapFolderState, InboundMessage, MailboxReconcile
from backend.app.models.sending import EmailSequence, PauseFlag, PauseScope, SendRecord, SendState, SequenceState
from backend.app.services.inbox_guard import check_inbox_freshness
from backend.tests.test_sending.conftest import make_worker

from .conftest import (
    CONFIG,
    OWNER,
    TUE,
    Clock,
    FakeImapServer,
    eml,
    ist,
    make_loop,
    ready_mailbox,
    sent_sequence,
)


async def stored(session) -> list[InboundMessage]:
    session.expire_all()
    return list((await session.execute(select(InboundMessage).order_by(InboundMessage.id))).scalars().all())


async def test_reads_inbox_and_junk_read_only_without_setting_seen(factory, session, site, models):
    await ready_mailbox(session)
    sent = await sent_sequence(session)
    imap = FakeImapServer()
    imap.add(eml("Yes please, send the sample.", in_reply_to=sent.message_id))
    imap.add(eml("What is the price?", frm="Other <other@shop.example>", message_id="<junk-1@shop.example>"),
             folder="Junk")
    summary = await make_loop(factory, Clock(ist(TUE, 12)), site, imap, models).reconcile()
    assert summary["ok"] and summary["mailboxes"][0]["new_messages"] == 2
    assert [f["folder"] for f in summary["mailboxes"][0]["folders"]] == ["INBOX", "Junk"]
    assert all(readonly for _, readonly in imap.selects)
    assert all("BODY.PEEK[]<0." in spec for _, _, spec in imap.fetches)   # PEEK: no \Seen flag
    rows = await stored(session)
    assert {r.folder for r in rows} == {"INBOX", "Junk"}
    reconcile = (await session.execute(select(MailboxReconcile))).scalar_one()
    assert reconcile.last_success_at is not None and reconcile.last_error is None
    states = {s.folder: s.last_uid for s in (await session.execute(select(ImapFolderState))).scalars()}
    assert states == {"INBOX": 1, "Junk": 1}


async def test_second_run_fetches_only_new_uids(factory, session, site, models):
    await ready_mailbox(session)
    sent = await sent_sequence(session)
    imap = FakeImapServer(junk=None)
    imap.add(eml("Price?", in_reply_to=sent.message_id, message_id="<a@x.example>"))
    loop = make_loop(factory, Clock(ist(TUE, 12)), site, imap, models)
    await loop.reconcile()
    await loop.reconcile()   # the server answers "UID 2:*" with UID 1 again: it must not be fetched or stored twice
    assert len(imap.fetches) == 1
    imap.add(eml("And the sample?", in_reply_to=sent.message_id, message_id="<b@x.example>"))
    await loop.reconcile()
    assert len(imap.fetches) == 2 and len(await stored(session)) == 2


async def test_uidvalidity_change_reads_again_without_duplicates(factory, session, site, models):
    await ready_mailbox(session)
    sent = await sent_sequence(session)
    imap = FakeImapServer(junk=None)
    imap.add(eml("Price?", in_reply_to=sent.message_id, message_id="<a@x.example>"))
    loop = make_loop(factory, Clock(ist(TUE, 12)), site, imap, models)
    await loop.reconcile()
    imap.renumber(uidvalidity=7777)
    imap.add(eml("Sample please", in_reply_to=sent.message_id, message_id="<c@x.example>"))
    summary = await loop.reconcile()
    assert summary["mailboxes"][0]["new_messages"] == 1
    rows = await stored(session)
    assert [r.message_id for r in rows] == ["<a@x.example>", "<c@x.example>"]
    state = (await session.execute(select(ImapFolderState))).scalar_one()
    assert state.uidvalidity == 7777 and state.uidvalidity_changed_at is not None and state.last_uid == 102


async def test_matching_by_in_reply_to_references_and_address(factory, session, site, models):
    await ready_mailbox(session)
    a = await sent_sequence(session, name="Glow Hair Studio", email="info@glowhair.example")
    b = await sent_sequence(session, name="Bright Tuition", email="hello@brighttuition.example")
    c = await sent_sequence(session, name="Silver Line Tailors", email="shop@silverline.example")
    imap = FakeImapServer(junk=None)
    imap.add(eml("Price?", in_reply_to=a.message_id, frm=f"<{a.email}>", message_id="<1@x.example>"))
    imap.add(eml("Price?", references=["<unknown@else.example>", b.message_id], frm="Other <other@b.example>",
                 message_id="<2@x.example>"))
    imap.add(eml("Price?", frm=f"Owner <{c.email}>", subject="website", message_id="<3@x.example>"))
    imap.add(eml("Price?", frm="Stranger <stranger@nowhere.example>", subject="hello", message_id="<4@x.example>"))
    await make_loop(factory, Clock(ist(TUE, 12)), site, imap, models).reconcile()
    rows = {r.message_id: r for r in await stored(session)}
    assert (rows["<1@x.example>"].sequence_id, rows["<1@x.example>"].match_method) == (a.sequence_id, "in_reply_to")
    assert (rows["<2@x.example>"].sequence_id, rows["<2@x.example>"].match_method) == (b.sequence_id, "references")
    assert (rows["<3@x.example>"].sequence_id, rows["<3@x.example>"].match_method) == (c.sequence_id, "address")
    assert rows["<4@x.example>"].sequence_id is None and "UNMATCHED" in rows["<4@x.example>"].flags


async def test_a_reply_stops_the_sequence_and_cancels_follow_ups(factory, session, site, models):
    await ready_mailbox(session)
    sent = await sent_sequence(session)
    imap = FakeImapServer(junk=None)
    imap.add(eml("Interesting. What is the price?", in_reply_to=sent.message_id))
    await make_loop(factory, Clock(ist(TUE, 12)), site, imap, models).reconcile()
    session.expire_all()
    sequence = await session.get(EmailSequence, sent.sequence_id)
    assert sequence.state == SequenceState.STOPPED_REPLY
    steps = (await session.execute(select(SendRecord).where(SendRecord.sequence_id == sent.sequence_id)
                                   .order_by(SendRecord.step))).scalars().all()
    assert [s.state for s in steps] == [SendState.ACCEPTED, SendState.CANCELLED, SendState.CANCELLED]


async def test_failed_read_pauses_the_mailbox_and_a_good_read_clears_it(factory, session, site, models):
    box_id = (await ready_mailbox(session)).id
    imap = FakeImapServer()
    imap.fail = "login"
    clock = Clock(ist(TUE, 8, 30))
    loop = make_loop(factory, clock, site, imap, models)
    summary = await loop.reconcile()
    assert not summary["ok"] and "LOGIN failed" in summary["mailboxes"][0]["error"]
    assert summary["stale_mailboxes"] == [box_id]

    async def active():
        session.expire_all()
        return (await session.execute(select(PauseFlag).where(
            PauseFlag.cleared_at.is_(None), PauseFlag.reason_code == "INBOX_NOT_RECONCILED"))).scalars().all()

    flags = await active()
    assert [(f.scope, f.scope_value) for f in flags] == [(PauseScope.MAILBOX, str(box_id))]
    imap.fail = None
    assert (await loop.reconcile())["ok"]
    assert await active() == []
    # 24 h later without a complete read: paused again (also from the worker's cycle)
    clock.at(ist(TUE, 8, 31) + timedelta(hours=24))
    imap.fail = "status"
    await loop.reconcile()
    assert len(await active()) == 1
    async with factory() as db:
        assert await check_inbox_freshness(db, CONFIG, clock.now) == [box_id]


async def test_worker_holds_mail_of_a_mailbox_whose_inbox_was_not_read(factory, session, site, models,
                                                                       smtp_server):
    box_id = (await ready_mailbox(session, smtp_port=smtp_server.port)).id
    sent_seq = await sent_sequence(session)
    record = (await session.execute(select(SendRecord).where(SendRecord.sequence_id == sent_seq.sequence_id,
                                                             SendRecord.step == 1))).scalar_one()
    record.state, record.submitted_at, record.accepted_at = SendState.SCHEDULED, None, None   # not sent yet
    record_id = record.id
    await session.commit()
    clock = Clock(ist(TUE, 9, 1))
    worker = make_worker(factory, clock, site, inbox_guard=check_inbox_freshness)
    summary = await worker.run_once()
    assert summary["stale_inboxes"] == [box_id] and smtp_server.envelopes == []
    session.expire_all()
    assert (await session.get(SendRecord, record_id)).hold_reason == "PAUSED:INBOX_NOT_RECONCILED"
    await make_loop(factory, clock, site, FakeImapServer(), models).reconcile()
    clock.at(ist(TUE, 9, 2))
    await worker.run_once()
    assert len(smtp_server.envelopes) == 1


async def test_own_copies_and_list_mail_are_ignored(factory, session, site, models):
    await ready_mailbox(session)
    imap = FakeImapServer(junk=None)
    imap.add(eml("copy", frm="Test Founder <test.founder@send-one.example>", message_id="<own@x.example>"))
    imap.add(eml("newsletter", frm="news@shop.example", headers={"List-Id": "<news.shop.example>"},
                 message_id="<list@x.example>"))
    await make_loop(factory, Clock(ist(TUE, 12)), site, imap, models).reconcile()
    assert {(r.kind.value, r.state.value) for r in await stored(session)} == {("OWN", "IGNORED"),
                                                                             ("AUTOMATED", "IGNORED")}
    assert models.classifier_calls.calls == []


async def test_reconcile_without_imap_settings_fails_that_mailbox(factory, session, site, models):
    box = await ready_mailbox(session)
    box.imap_host = None
    await session.commit()
    summary = await make_loop(factory, Clock(ist(TUE, 12)), site, FakeImapServer(), models).reconcile()
    assert not summary["ok"] and "IMAP host" in summary["mailboxes"][0]["error"]
    assert OWNER   # (the address constant is used by other tests in this module's helpers)
