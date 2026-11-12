"""E4 drafts: snapshot call shape, writer drafts, reply rules, approval through the E2 SMTP path (127.0.0.1), the
mailbox ceiling (reply reserve), reject / regenerate, and the 1-business-day reply backlog rule."""

from datetime import timedelta
from email import message_from_bytes, policy

import pytest
from sqlalchemy import select

from backend.app.engines.sending import scheduler as sched
from backend.app.engines.sending.tokens import email_hash
from backend.app.models.replies import DraftState, InboundMessage, OpportunitySnapshot, ReplyDraft
from backend.app.models.sending import (
    PauseFlag,
    PauseScope,
    SendKind,
    SendRecord,
    SendState,
)
from backend.app.services.reply_service import apply_reply_backlog
from backend.app.services.sending_service import Conflict

from .conftest import (
    BASE,
    CONFIG,
    MAILBOX,
    OWNER,
    TUE,
    Clock,
    FakeImapServer,
    eml,
    ist,
    labels_answer,
    make_loop,
    ready_mailbox,
    sent_sequence,
    set_classifier,
    set_writer,
    writer_answer,
)

WED = TUE + timedelta(days=1)


async def setup(factory, session, site, models, body, labels, smtp_port=2525, clock=None, **kwargs):
    await ready_mailbox(session, smtp_port=smtp_port)
    sent = await sent_sequence(session, **kwargs)
    set_classifier(models, labels_answer(labels))
    imap = FakeImapServer(junk=None)
    imap.add(eml(body, in_reply_to=sent.message_id, references=[sent.message_id],
                 message_id="<owner-reply-1@glowhair.example>"))
    loop = make_loop(factory, clock or Clock(ist(TUE, 12)), site, imap, models)
    await loop.reconcile()
    session.expire_all()
    return sent, loop, imap


async def drafts(session, state=None):
    session.expire_all()
    stmt = select(ReplyDraft).order_by(ReplyDraft.id)
    if state:
        stmt = stmt.where(ReplyDraft.state == state)
    return list((await session.execute(stmt)).scalars().all())


async def test_sample_request_creates_a_snapshot_and_a_waiting_draft_with_its_link(factory, session, site, models,
                                                                                    tmp_path):
    shot = tmp_path / "phone.png"
    shot.write_bytes(b"\x89PNG\r\n\x1a\n" + b"1" * 50)
    sent, loop, _ = await setup(factory, session, site, models, "Yes, please make the sample page.",
                                ["sample_requested"], evidence_path=str(shot))
    assert len(site.snapshots) == 1
    body = site.snapshots[0]
    assert body["business_name"] == "Glow Hair Studio" and body["city"] == "Surat"
    assert body["vertical"] == "salon_beauty" and body["concept_demo"] == "salon"
    assert body["observation"]["type"] == "SOCIAL_ONLY" and body["observation"]["checked_at"].startswith("2026-11-11")
    assert body["offer"]["price_inr"] == 7999 and body["reply_email"] == MAILBOX and body["expires_in_days"] == 30
    assert "evidence_image_base64" in body and "recording" not in body
    snapshot = (await session.execute(select(OpportunitySnapshot))).scalar_one()
    url = snapshot.url
    assert url == f"{BASE}/s/{snapshot.slug}" and snapshot.with_evidence_image
    [draft] = await drafts(session)
    assert draft.state == DraftState.WAITING and url in draft.body
    assert draft.recipient_email == OWNER and draft.subject.startswith("Re: ")
    assert draft.body.rstrip().endswith("Test address, Gujarat")       # the app's signature, not the model's
    task = models.writer_calls.calls[0]["messages"][0]["content"]
    assert url in task and OWNER not in task
    async with factory() as db:
        listed = await loop.list_drafts(db)
    assert listed[0]["business_name"] == "Glow Hair Studio" and listed[0]["snapshot_url"] == url


async def test_a_foreign_snapshot_url_is_refused_and_no_draft_is_made(factory, session, site, models):
    site.snapshot_mode = "foreign_url"
    await setup(factory, session, site, models, "Interested, send it.", ["interested"])
    msg = (await session.execute(select(InboundMessage))).scalar_one()
    assert msg.state.value == "FLAGGED" and any(f.startswith("SNAPSHOT_FAILED") for f in msg.flags)
    assert await drafts(session) == [] and models.writer_calls.calls == []


async def test_a_price_question_gets_a_draft_without_a_snapshot(factory, session, site, models):
    await setup(factory, session, site, models, "How much for one page?", ["price"])
    assert site.snapshots == []
    [draft] = await drafts(session)
    assert draft.state == DraftState.WAITING and "₹7,999" in draft.body


async def test_a_draft_with_a_discount_or_a_date_is_blocked(factory, session, site, models):
    set_writer(models, writer_answer("Hello Glow Hair Studio team,\n\nThank you for your reply. For you I can do the "
                                     "Launch website at a 10% discount if you confirm by Friday. Would that work?"))
    await setup(factory, session, site, models, "How much for one page?", ["price"])
    [draft] = await drafts(session)
    assert draft.state == DraftState.BLOCKED
    assert any(e.startswith("discount") for e in draft.errors) and any(e.startswith("date") for e in draft.errors)
    msg = (await session.execute(select(InboundMessage))).scalar_one()
    assert "DRAFT_BLOCKED" in msg.flags
    async with factory() as db:
        assert await (make_loop(factory, Clock(ist(TUE, 12)), site, FakeImapServer(), models)).list_drafts(db) == []


async def test_approval_sends_through_the_e2_path_threaded_and_counted(factory, session, site, models, smtp_server):
    sent, loop, _ = await setup(factory, session, site, models, "How much for one page?", ["price"],
                                smtp_port=smtp_server.port)
    [draft] = await drafts(session)
    result = await loop.approve(draft.id, "founder")
    assert result["state"] == "SENT" and result["smtp"]["outcome"] == "ACCEPTED"
    assert len(smtp_server.envelopes) == 1
    envelope = smtp_server.envelopes[0]
    assert envelope.mail_from == MAILBOX and envelope.rcpt_tos == [OWNER]
    received = message_from_bytes(envelope.content, policy=policy.default)
    assert received["In-Reply-To"] == "<owner-reply-1@glowhair.example>"
    assert received["References"].split() == [sent.message_id, "<owner-reply-1@glowhair.example>"]
    assert received["Subject"] == f"Re: {sent.subject}"
    assert received["From"].addresses[0].addr_spec == MAILBOX and "List-Unsubscribe" in received
    assert "₹7,999" in received.get_content()
    record = (await session.execute(select(SendRecord).where(SendRecord.kind == SendKind.REPLY))).scalar_one()
    assert record.state == SendState.ACCEPTED and record.approved_by == "founder"
    assert record.mailbox_id == draft.mailbox_id and record.message_id == result["message_id"]
    assert record.local_date == TUE and record.recipient_hash == email_hash(OWNER)
    msg = (await session.execute(select(InboundMessage))).scalar_one()
    assert msg.handled_at is not None and msg.handled_by == "founder"
    with pytest.raises(Conflict):
        await loop.approve(draft.id, "founder")              # never twice
    assert len(smtp_server.envelopes) == 1


async def test_the_mailbox_ceiling_counts_replies_and_refuses_the_31st(factory, session, site, models, smtp_server):
    sent, loop, _ = await setup(factory, session, site, models, "How much for one page?", ["price"],
                                smtp_port=smtp_server.port)
    [draft] = await drafts(session)
    # 29 messages already on this mailbox's day (incl. the 3 of the sequence): the reply is the 30th and fits.
    async with factory() as db:
        existing = len((await db.execute(select(SendRecord).where(SendRecord.local_date == TUE))).scalars().all())
        for index in range(sched.MAILBOX_DAILY_CEILING - 1 - existing):
            db.add(SendRecord(kind=SendKind.REPLY, idempotency_key=f"filler:{index}", mailbox_id=draft.mailbox_id,
                              recipient_email=f"x{index}@y.example", recipient_hash=email_hash(f"x{index}@y.example"),
                              message_id=f"<filler-{index}@send-one.example>", scheduled_for=ist(TUE, 9),
                              local_date=TUE, window_label="reply", window_start=ist(TUE, 9),
                              window_end=ist(TUE, 9), state=SendState.ACCEPTED, approved_at=ist(TUE, 9),
                              approved_by="founder", submitted_at=ist(TUE, 9)))
        await db.commit()
    assert (await loop.approve(draft.id, "founder"))["state"] == "SENT"
    # a second reply on the same day would be the 31st
    second = ReplyDraft(kind=draft.kind, inbound_message_id=draft.inbound_message_id, sequence_id=draft.sequence_id,
                        business_id=draft.business_id, mailbox_id=draft.mailbox_id, recipient_email=OWNER,
                        labels=["price"], subject=draft.subject, body=draft.body, state=DraftState.WAITING,
                        errors=[], created_at=ist(TUE, 12, 30))
    session.add(second)
    await session.commit()
    with pytest.raises(Conflict, match="REPLY_CAPACITY_FULL"):
        await loop.approve(second.id, "founder")
    assert len(smtp_server.envelopes) == 1


async def test_approval_refused_while_paused_or_suppressed_or_website_down(factory, session, site, models,
                                                                          smtp_server):
    sent, loop, _ = await setup(factory, session, site, models, "How much for one page?", ["price"],
                                smtp_port=smtp_server.port)
    [draft] = await drafts(session)
    draft_id = draft.id
    flag = PauseFlag(scope=PauseScope.DOMAIN, scope_value="send-one.example", reason_code="POLICY_REJECTION",
                     created_at=ist(TUE, 11))
    session.add(flag)
    await session.commit()
    with pytest.raises(Conflict, match="POLICY_REJECTION"):
        await loop.approve(draft_id, "founder")
    flag.cleared_at = ist(TUE, 11, 30)
    await session.commit()
    site.mode = "down"
    with pytest.raises(Exception, match="suppression check unavailable"):
        await loop.approve(draft_id, "founder")
    session.expire_all()
    assert (await session.get(ReplyDraft, draft_id)).state == DraftState.WAITING
    assert (await session.execute(select(PauseFlag.reason_code).where(PauseFlag.cleared_at.is_(None)))
            ).scalar_one() == "SUPPRESSION_UNAVAILABLE"
    assert smtp_server.envelopes == []


async def test_a_suppressed_recipient_is_never_answered(factory, session, site, models, smtp_server):
    sent, loop, _ = await setup(factory, session, site, models, "How much for one page?", ["price"],
                                smtp_port=smtp_server.port)
    [draft] = await drafts(session)
    draft_id = draft.id
    site.suppressed.add(email_hash(OWNER))     # unsubscribed by link after the draft was written
    with pytest.raises(Conflict, match="suppressed"):
        await loop.approve(draft_id, "founder")
    session.expire_all()
    assert (await session.get(ReplyDraft, draft_id)).state == DraftState.REJECTED
    assert smtp_server.envelopes == []


async def test_reject_and_regenerate(factory, session, site, models):
    sent, loop, _ = await setup(factory, session, site, models, "How much for one page?", ["price"])
    [draft] = await drafts(session)
    new = await loop.regenerate(draft.id, "founder", "shorter please")
    assert new["state"] == "WAITING" and new["regenerations"] == 1
    states = [d.state for d in await drafts(session)]
    assert states == [DraftState.SUPERSEDED, DraftState.WAITING]
    async with factory() as db:
        out = await loop.reject(db, new["id"], "founder", "I called them instead", close_thread=True)
        await db.commit()
    assert out["state"] == "REJECTED"
    session.expire_all()
    assert (await session.execute(select(InboundMessage.handled_by))).scalar_one() == "founder"


async def test_reply_backlog_blocks_new_contacts_after_one_business_day(factory, session, site, models,
                                                                        smtp_server):
    # the reply arrives Tuesday 10:00 India time; it is overdue from Wednesday 10:00
    sent, loop, _ = await setup(factory, session, site, models, "Interested, how much?", ["interested", "price"],
                                smtp_port=smtp_server.port)

    async def backlog(at):
        async with factory() as db:
            breached = await apply_reply_backlog(db, CONFIG, site.client(), at)
            await db.commit()
        session.expire_all()
        flags = (await session.execute(select(PauseFlag).where(
            PauseFlag.cleared_at.is_(None), PauseFlag.reason_code == "REPLY_BACKLOG"))).scalars().all()
        return breached, [(f.scope, f.reason_code) for f in flags]

    assert await backlog(ist(WED, 9, 59)) == (False, [])
    assert await backlog(ist(WED, 10, 1)) == (True, [(PauseScope.NEW_CONTACTS, "REPLY_BACKLOG")])
    [draft] = await drafts(session, DraftState.WAITING)
    loop.deps.clock = lambda: ist(WED, 10, 5)
    await loop.approve(draft.id, "founder")
    assert await backlog(ist(WED, 10, 6)) == (False, [])


async def test_backlog_counts_messages_without_a_label_and_the_founder_can_close_them(factory, session, site,
                                                                                      models):
    await ready_mailbox(session)
    sent = await sent_sequence(session)
    imap = FakeImapServer(junk=None)
    imap.add(eml("Interested, send the sample.", in_reply_to=sent.message_id))
    loop = make_loop(factory, Clock(ist(TUE, 12)), site, imap, models, api_key=False)
    await loop.reconcile()
    async with factory() as db:
        assert await apply_reply_backlog(db, CONFIG, site.client(), ist(WED, 10, 1)) is True
        await db.commit()
    async with factory() as db:
        [item] = await loop.list_inbound(db, needs_founder=True)
        assert item["labels"] == ["needs_review"]
        await loop.close_inbound(db, item["id"], "founder", "answered on the phone")
        await db.commit()
    async with factory() as db:
        assert await apply_reply_backlog(db, CONFIG, site.client(), ist(WED, 10, 2)) is False


async def test_a_failed_or_blocked_regeneration_keeps_the_waiting_draft(factory, session, site, models):
    sent, loop, _ = await setup(factory, session, site, models, "How much for one page?", ["price"])
    [draft] = await drafts(session)
    draft_id = draft.id
    set_writer(models, writer_answer("Hello Glow Hair Studio team,\n\nThank you. I can send it tomorrow at a 10% "
                                     "discount. Would that work for you?"))
    blocked = await loop.regenerate(draft_id, "founder", None)
    assert blocked["state"] == "BLOCKED"
    session.expire_all()
    assert (await session.get(ReplyDraft, draft_id)).state == DraftState.WAITING
    set_writer(models, RuntimeError("model down"))
    with pytest.raises(Conflict, match="no new draft"):
        await loop.regenerate(draft_id, "founder", None)
    session.expire_all()
    assert (await session.get(ReplyDraft, draft_id)).state == DraftState.WAITING


async def test_a_later_stop_means_no_answer_is_owed(factory, session, site, models):
    sent, loop, imap = await setup(factory, session, site, models, "Interested, how much?", ["interested", "price"])
    imap.add(eml("Actually, please stop. Not interested.", in_reply_to=sent.message_id,
                 message_id="<owner-reply-2@glowhair.example>"))
    await loop.reconcile()
    session.expire_all()
    first = (await session.execute(select(InboundMessage).where(
        InboundMessage.message_id == "<owner-reply-1@glowhair.example>"))).scalar_one()
    assert first.handled_by == "system" and "stop" in first.handled_note
    async with factory() as db:
        assert await apply_reply_backlog(db, CONFIG, site.client(), ist(WED, 12)) is False
    session.expire_all()
    states = [(d.kind.value, d.state) for d in await drafts(session)]
    assert states == [("REPLY", DraftState.REJECTED), ("STOP_CONFIRMATION", DraftState.OPTIONAL)]
