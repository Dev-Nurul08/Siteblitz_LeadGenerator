"""E4 daily brief (real counts only), the API routes, the /start-day command file and the reconcile script."""

import asyncio
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import backend.app.database as database
import backend.app.models  # noqa: F401
from backend.app.config import get_settings
from backend.app.database import Base
from backend.app.engines.sending.tokens import email_hash
from backend.app.models.replies import (
    DraftKind,
    DraftState,
    InboundKind,
    InboundMessage,
    InboundState,
    OpportunitySnapshot,
    ReplyDraft,
    ReplySuppression,
    WebsiteWrite,
)
from backend.app.models.sending import (
    DeliveryEvent,
    DeliveryEventKind,
    PauseFlag,
    PauseScope,
    SendKind,
    SendRecord,
    SendState,
)
from backend.app.services.brief_service import build_brief

from .conftest import (
    CONFIG,
    TUE,
    Clock,
    FakeImapServer,
    FakeSite,
    ist,
    labels_answer,
    make_loop,
    ready_mailbox,
    sample_draft,
    sent_sequence,
    stub_client,
)

ROOT = Path(__file__).resolve().parents[3]
MON = TUE - timedelta(days=1)


def record(mailbox_id: int, key: str, kind: SendKind, accepted: datetime, step=None, day: date = MON) -> SendRecord:
    return SendRecord(kind=kind, step=step, idempotency_key=key, mailbox_id=mailbox_id, recipient_email=f"{key}@x.example",
                      recipient_hash=email_hash(f"{key}@x.example"), message_id=f"<{key}@send-one.example>",
                      scheduled_for=accepted, local_date=day, window_label="09:00-11:30", window_start=accepted,
                      window_end=accepted, state=SendState.ACCEPTED, submitted_at=accepted, accepted_at=accepted,
                      approved_at=accepted, approved_by="founder")


def inbound(mailbox_id, uid, sender, labels, received, kind=InboundKind.HUMAN, sequence_id=None,
            state=InboundState.PROCESSED) -> InboundMessage:
    return InboundMessage(mailbox_id=mailbox_id, folder="INBOX", uidvalidity=1, uid=uid, message_id=f"<{uid}@m>",
                          from_address=sender, from_hash=email_hash(sender), received_at=received,
                          raw_sha256=f"{uid:064d}", kind=kind, labels=labels, flags=[], state=state,
                          sequence_id=sequence_id)


async def test_brief_counts_match_the_database(session):
    box = await ready_mailbox(session)
    box_id = box.id
    seq = await sent_sequence(session)     # step 1 accepted TUE 09:01 (today, not yesterday); steps 2 / 3 later
    yesterday = ist(MON, 10)
    session.add_all([
        record(box_id, "c1", SendKind.CAMPAIGN, yesterday, step=1),
        record(box_id, "c2", SendKind.CAMPAIGN, yesterday + timedelta(minutes=6), step=1),
        record(box_id, "c3", SendKind.CAMPAIGN, yesterday + timedelta(minutes=12), step=2),
        record(box_id, "r1", SendKind.REPLY, yesterday + timedelta(hours=3)),
        record(box_id, "old", SendKind.CAMPAIGN, yesterday - timedelta(days=1), step=1, day=MON - timedelta(days=1)),
    ])
    for kind, recipient in ((DeliveryEventKind.HARD_BOUNCE, "a"), (DeliveryEventKind.SOFT_BOUNCE, "b"),
                            (DeliveryEventKind.SOFT_BOUNCE, "c"), (DeliveryEventKind.SOFT_BOUNCE, "c"),
                            (DeliveryEventKind.POLICY_REJECTION, "d"), (DeliveryEventKind.COMPLAINT, "e")):
        session.add(DeliveryEvent(kind=kind, recipient_hash=email_hash(recipient), origin="dsn",
                                  occurred_at=yesterday + timedelta(hours=1)))
    session.add_all([
        inbound(box_id, 1, "a@shop.example", ["interested", "price"], yesterday, sequence_id=seq.sequence_id),
        inbound(box_id, 2, "a@shop.example", ["question"], yesterday + timedelta(hours=1),
                sequence_id=seq.sequence_id),
        inbound(box_id, 3, "b@shop.example", ["stop"], yesterday + timedelta(hours=2), sequence_id=seq.sequence_id),
        inbound(box_id, 4, "c@shop.example", ["needs_review"], yesterday + timedelta(hours=2),
                sequence_id=seq.sequence_id, state=InboundState.NEEDS_REVIEW),
        inbound(box_id, 5, "ooo@shop.example", ["out_of_office"], yesterday, kind=InboundKind.AUTO_REPLY),
        inbound(box_id, 6, "mailer-daemon@x.example", ["bounce"], yesterday, kind=InboundKind.DSN),
        inbound(box_id, 7, "stranger@else.example", [], yesterday, state=InboundState.FLAGGED),   # unmatched
        inbound(box_id, 8, "late@shop.example", ["interested"], ist(TUE, 10), sequence_id=seq.sequence_id),
    ])
    await session.flush()
    session.add_all([
        ReplySuppression(email_hash=email_hash("b@shop.example"), reason="reply_stop",
                         website_state=WebsiteWrite.PENDING, created_at=yesterday + timedelta(hours=2)),
        OpportunitySnapshot(business_id=seq.business_id, sequence_id=seq.sequence_id, slug="glow-abc", url="u",
                            expires_at=yesterday + timedelta(days=30), created_at=yesterday + timedelta(hours=1)),
        ReplyDraft(kind=DraftKind.REPLY, inbound_message_id=1, mailbox_id=box_id, recipient_email="a@shop.example",
                   labels=["price"], subject="Re: x", body="b", state=DraftState.WAITING, errors=[],
                   created_at=yesterday),
        ReplyDraft(kind=DraftKind.REPLY, inbound_message_id=2, mailbox_id=box_id, recipient_email="a@shop.example",
                   labels=["question"], subject="Re: x", body="b", state=DraftState.BLOCKED, errors=["date"],
                   created_at=yesterday),
        ReplyDraft(kind=DraftKind.STOP_CONFIRMATION, inbound_message_id=3, mailbox_id=box_id,
                   recipient_email="b@shop.example", labels=["stop"], subject="Re: x", body="b",
                   state=DraftState.OPTIONAL, errors=[], created_at=yesterday),
        PauseFlag(scope=PauseScope.NEW_CONTACTS, scope_value="", reason_code="REPLY_BACKLOG", created_at=yesterday),
    ])
    await session.commit()

    brief = await build_brief(session, CONFIG, TUE, ist(TUE, 8, 45))
    y = brief["yesterday"]
    assert y["accepted"] == {"total": 4, "campaign": 3, "new_contacts": 2, "replies": 1}
    assert (y["hard_bounces"], y["soft_bounces"], y["policy_rejections"], y["complaints_received"]) == (1, 2, 1, 1)
    assert y["complaint_rate_from_provider"] == "unknown"
    assert y["unique_human_replies"] == 3                      # a twice, b, c; the stranger is not a reply to us
    assert y["replies_by_label"] == {"interested": 1, "question": 1, "price": 1, "sample_requested": 0,
                                     "not_now": 0, "wrong_person": 0, "stop": 1, "complaint_legal": 0,
                                     "needs_review": 1}
    assert (y["out_of_office"], y["bounce_reports_read"]) == (1, 1)
    assert (y["stops_processed"], y["samples_created"]) == (1, 1)
    for field in ("quotes", "deposits", "payments", "paid_projects"):
        assert y[field] == {"value": None, "not_tracked": True}
    assert brief["since_last_brief"] is None
    assert (brief["drafts_waiting"], brief["drafts_blocked"]) == (1, 1)
    assert brief["messages_for_founder"] == 2                  # needs_review + the unmatched message
    assert brief["stops_pending_website_write"] == 1
    assert [p["reason_code"] for p in brief["active_pauses"]] == ["REPLY_BACKLOG"]
    today = brief["today"]
    assert today["campaign_day"] is True
    assert today["mailboxes"][0]["scheduled_today"] == 1 and today["mailboxes"][0]["by_step"] == {"step_1": 1}
    assert today["new_contact_allowance"]["blocked_by"] == ["REPLY_BACKLOG"]
    assert today["new_contact_allowance"]["left"] == 0 and today["new_contact_allowance"]["daily_limit"] == 10
    assert today["mailboxes"][0]["inbox_read_stale"] is True   # never reconciled
    # a second brief counts "since the last brief" from the first one's time
    again = await build_brief(session, CONFIG, TUE, ist(TUE, 11))
    assert again["since_last_brief"]["from"] == ist(TUE, 8, 45).isoformat()
    assert again["since_last_brief"]["unique_human_replies"] == 1          # only the 10:00 reply
    assert again["since_last_brief"]["accepted"]["total"] == 1             # step 1 at 09:01


# ─── API on the real app ────────────────────────────────────────────────────


async def _seed(url: str) -> None:
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


@pytest.fixture
def api(tmp_path, monkeypatch):
    url = f"sqlite+aiosqlite:///{tmp_path / 'api.db'}"
    asyncio.run(_seed(url))
    monkeypatch.setenv("DATABASE_URL", url)
    for name, value in (("OUTREACH_API_KEY", CONFIG.api_key), ("OUTREACH_SIGNING_SECRET", CONFIG.signing_secret),
                        ("OUTREACH_PUBLIC_BASE_URL", CONFIG.base_url), ("SITEBLITZ_SENDER_NAME", "Test Founder"),
                        ("SITEBLITZ_REPLY_EMAIL", "test.founder@send-one.example"),
                        ("SITEBLITZ_POSTAL_ADDRESS", "Test address, Gujarat")):
        monkeypatch.setenv(name, value)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    get_settings.cache_clear()
    monkeypatch.setattr(database, "_async_engine", None)
    monkeypatch.setattr(database, "_async_session_factory", None)
    from backend.app.api.v1 import outreach_replies
    from backend.app.main import app

    # The routes get a loop whose website and model are the test fakes (no network, no real model).
    classifier_client, _ = stub_client(labels_answer(["interested"]))
    writer_client, _ = stub_client(sample_draft)
    models = SimpleNamespace(classifier_client=classifier_client, writer_client=writer_client)
    loop = make_loop(database.get_async_session_factory(), Clock(ist(TUE, 8, 45)), FakeSite(), FakeImapServer(),
                     models)
    app.dependency_overrides[outreach_replies.reply_loop] = lambda: loop
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        get_settings.cache_clear()


def test_api_routes_answer(api):
    brief = api.get("/api/v1/outreach/brief", params={"date": "2026-11-17"})
    assert brief.status_code == 200
    body = brief.json()
    assert body["date"] == "2026-11-17" and body["yesterday"]["quotes"] == {"value": None, "not_tracked": True}
    assert body["complaint_rate_from_provider"] == "unknown"
    assert api.get("/api/v1/outreach/drafts").json() == {"items": []}
    assert api.get("/api/v1/outreach/drafts", params={"state": "bogus"}).status_code == 422
    assert api.get("/api/v1/outreach/inbound", params={"needs_founder": "true"}).json() == {"items": []}
    assert api.post("/api/v1/outreach/drafts/99/approve", json={"approved_by": "founder"}).status_code == 404
    assert api.post("/api/v1/outreach/drafts/99/approve", json={"approved_by": ""}).status_code == 422
    assert api.post("/api/v1/outreach/drafts/99/reject", json={"rejected_by": "f", "note": "no"}).status_code == 422
    assert api.post("/api/v1/outreach/inbound/99/close", json={"closed_by": "f", "note": "done"}).status_code == 404
    reconcile = api.post("/api/v1/outreach/reconcile")
    assert reconcile.status_code == 200 and reconcile.json()["ok"] is False and reconcile.json()["mailboxes"] == []


# ─── /start-day command file ────────────────────────────────────────────────

COMMAND = ROOT / ".claude" / "commands" / "start-day.md"


def test_start_day_command_names_only_real_endpoints():
    from backend.app.main import app

    text = COMMAND.read_text(encoding="utf-8")
    spec = {path: {m.upper() for m in methods} for path, methods in app.openapi()["paths"].items()}
    spec["/health"] = {"GET"}
    patterns = {re.compile("^" + re.sub(r"\{[^}]+\}", "[^/]+", path) + "$"): methods for path, methods in spec.items()}
    found = []
    for line in text.splitlines():
        for match in re.finditer(r"http://127\.0\.0\.1:8000(/[^\s\"`?]*)", line):
            method = "POST" if "-X POST" in line[:match.start()] else "GET"
            path = match.group(1).replace("<id>", "1")
            allowed = [methods for pattern, methods in patterns.items() if pattern.match(path)]
            assert allowed and method in allowed[0], f"{method} {path} is not an API route"
            found.append((method, re.sub(r"/1(/|$)", r"/{id}\1", path)))
    assert set(found) >= {("GET", "/health"), ("POST", "/api/v1/outreach/reconcile"), ("GET", "/api/v1/outreach/brief"),
                          ("GET", "/api/v1/outreach/drafts"), ("POST", "/api/v1/outreach/drafts/{id}/approve"),
                          ("POST", "/api/v1/outreach/drafts/{id}/reject"),
                          ("POST", "/api/v1/outreach/drafts/{id}/regenerate"),
                          ("GET", "/api/v1/outreach/inbound"), ("POST", "/api/v1/outreach/inbound/{id}/close")}
    for needed in ("abhi track nahi hota", "run_all.py", "hold <n>", "send replies", "/debate", "Monday",
                   "Do not start it yourself"):
        assert needed in text


# ─── scripts ────────────────────────────────────────────────────────────────


def test_reconcile_script_exit_codes():
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import outreach_reconcile
    finally:
        sys.path.remove(str(ROOT / "scripts"))
    ok = {"ok": True, "mailboxes": [{"mailbox_id": 1, "ok": True, "new_messages": 2, "error": None}],
          "processed": {"PROCESSED": 2}, "stale_mailboxes": []}
    assert outreach_reconcile.report(ok)[0] == 0
    failed = {**ok, "ok": False, "mailboxes": [{"mailbox_id": 1, "ok": False, "new_messages": 0,
                                                "error": "LOGIN failed: NO"}], "stale_mailboxes": [1]}
    code, lines = outreach_reconcile.report(failed)
    assert code == 1 and any("FAILED: LOGIN failed" in line for line in lines) and any("paused" in l for l in lines)
    assert outreach_reconcile.report({"ok": False, "mailboxes": []})[0] == 2
    assert not any("@" in line for line in outreach_reconcile.report(ok)[1])   # no addresses printed


def test_task_registration_script_is_present_and_not_run():
    text = (ROOT / "scripts" / "register_outreach_tasks.ps1").read_text(encoding="utf-8")
    assert "08:30" in text and "Tuesday, Wednesday, Thursday" in text and "outreach_reconcile.py" in text
    assert "-StartWhenAvailable" in text


def test_brief_dates_are_india_days():
    from backend.app.services.brief_service import day_bounds
    start, end = day_bounds(date(2026, 11, 16))
    assert start == datetime(2026, 11, 15, 18, 30, tzinfo=timezone.utc) and end - start == timedelta(days=1)
