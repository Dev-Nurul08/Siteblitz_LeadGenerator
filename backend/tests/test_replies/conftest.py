"""
Shared fixtures for email engine v2 E4 (reply loop). No test touches the network, a real mailbox or a real model:
- IMAP is FakeImapServer (an imaplib-shaped fake: LIST, SELECT, STATUS, UID SEARCH, UID FETCH);
- the website (suppression list + snapshots) is an httpx.MockTransport (FakeSite);
- the model is a stub client for the classifier and another for the AI writer;
- SMTP goes to the E2 aiosmtpd server on 127.0.0.1 (smtp_server fixture).
Settings are built with Settings(_env_file=None, ...), so a real .env can never change a result (CLAUDE.md).
"""

import json
from datetime import date, datetime, timedelta, timezone
from email.message import EmailMessage
from email.utils import format_datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

import httpx
import pytest

from backend.app.config import Settings
from backend.app.engines.replies.classifier import ReplyClassifier
from backend.app.engines.replies.snapshot_client import SnapshotClient
from backend.app.engines.sending.suppression_client import SuppressionClient
from backend.app.engines.writer.writer import OutreachWriter
from backend.app.models.sending import Mailbox, TlsMode
from backend.app.services.reply_service import ReplyLoop, ReplyLoopDeps
from backend.tests.test_sending.conftest import (  # noqa: F401  (fixtures re-used by name)
    BASE,
    BEFORE,
    CONFIG,
    IST,
    TUE,
    Clock,
    FakeWebsite,
    admitted_sequence,
    factory,
    ist,
    session,
    smtp_server,
    website,
)

FACTS_MD = (Path(__file__).resolve().parents[3] / "docs" / "outreach" / "company-facts.md").read_text(encoding="utf-8")
EVAL_SET = json.loads((Path(__file__).parent / "fixtures" / "reply_eval_set.json").read_text(encoding="utf-8"))
OUR_SUBJECT = "Glow Hair Studio: no website link in Instagram bio"
OWNER = "info@glowhair.example"
MAILBOX = "test.founder@send-one.example"
WRITER_SETTINGS = Settings(_env_file=None, ANTHROPIC_API_KEY="test-key-not-real",
                           SITEBLITZ_SENDER_NAME="Test Founder", SITEBLITZ_REPLY_EMAIL=MAILBOX,
                           SITEBLITZ_POSTAL_ADDRESS="Test address, Gujarat")


# ─── IMAP ───────────────────────────────────────────────────────────────────


class FakeImapServer:
    """Folders of {uid: raw}. `fail` = connect | login | fetch | status makes that step fail."""

    def __init__(self, junk: Optional[str] = "Junk"):
        self.folders = {"INBOX": {"uidvalidity": 1001, "messages": {}}}
        if junk:
            self.folders[junk] = {"uidvalidity": 2002, "messages": {}}
        self.junk = junk
        self.fail: Optional[str] = None
        self.logins: list = []
        self.selects: list = []
        self.fetches: list = []
        self.connects = 0

    def add(self, raw: bytes, folder: str = "INBOX") -> int:
        messages = self.folders[folder]["messages"]
        uid = max(messages, default=0) + 1
        messages[uid] = raw
        return uid

    def renumber(self, folder: str = "INBOX", uidvalidity: int = 5005) -> None:
        """A new UIDVALIDITY: every message gets a new UID (as after a server-side rebuild)."""
        old = self.folders[folder]["messages"]
        self.folders[folder] = {"uidvalidity": uidvalidity,
                                "messages": {100 + i: raw for i, raw in enumerate(old.values(), start=1)}}

    def connector(self, host, port, tls, timeout=None):
        self.connects += 1
        if self.fail == "connect":
            raise ConnectionRefusedError("refused")
        assert host == "127.0.0.1" and tls == "none"
        return FakeImapConn(self)


def _unquote(name: str) -> str:
    return name[1:-1] if name.startswith('"') and name.endswith('"') else name


class FakeImapConn:
    def __init__(self, server: FakeImapServer):
        self.server = server
        self.selected = None

    def login(self, user, password):
        if self.server.fail == "login":
            return "NO", [b"[AUTHENTICATIONFAILED] invalid credentials"]
        self.server.logins.append(user)
        return "OK", [b"LOGIN completed"]

    def list(self):
        lines = [b'(\\HasNoChildren) "/" "INBOX"', b'(\\HasNoChildren \\Sent) "/" "Sent"']
        if self.server.junk:
            lines.append(b'(\\HasNoChildren \\Junk) "/" "' + self.server.junk.encode() + b'"')
        return "OK", lines

    def select(self, mailbox, readonly=False):
        name = _unquote(mailbox)
        self.server.selects.append((name, readonly))
        self.selected = name
        return "OK", [str(len(self.server.folders[name]["messages"])).encode()]

    def status(self, mailbox, names):
        if self.server.fail == "status":
            return "NO", [b"STATUS failed"]
        folder = self.server.folders[_unquote(mailbox)]
        nxt = max(folder["messages"], default=0) + 1
        return "OK", [f'"{_unquote(mailbox)}" (UIDVALIDITY {folder["uidvalidity"]} UIDNEXT {nxt})'.encode()]

    def uid(self, command, *args):
        messages = self.server.folders[self.selected]["messages"]
        if command == "SEARCH":
            if args[0] == "UID":
                start = int(args[1].split(":")[0])
                found = [u for u in sorted(messages) if u >= start]
                if not found and messages:   # real servers answer n:* with the last UID even when it is < n
                    found = [max(messages)]
            else:
                found = sorted(messages)
            return "OK", [" ".join(str(u) for u in found).encode()]
        if command == "FETCH":
            if self.server.fail == "fetch":
                return "NO", [b"FETCH failed"]
            uid = int(args[0])
            raw = messages[uid]
            self.server.fetches.append((self.selected, uid, args[1]))
            limit = int(args[1].split("<0.")[1].rstrip(">)"))
            part = raw[:limit]
            head = f"1 (UID {uid} RFC822.SIZE {len(raw)} BODY[]<0> {{{len(part)}}}".encode()
            return "OK", [(head, part), b")"]
        return "BAD", [b"unknown command"]

    def logout(self):
        return "BYE", [b"bye"]


# ─── website: suppression list + snapshots ──────────────────────────────────


class FakeSite(FakeWebsite):
    """FakeWebsite (E2 suppression API) + POST /api/outreach/snapshots."""

    def __init__(self):
        super().__init__()
        self.snapshots: list = []
        self.snapshot_mode = "ok"   # ok | down | foreign_url

    def handler(self, request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/outreach/snapshots":
            assert request.headers["authorization"] == f"Bearer {CONFIG.api_key}"
            if self.snapshot_mode == "down":
                return httpx.Response(503, json={"ok": False})
            body = json.loads(request.content)
            self.snapshots.append(body)
            slug = f"glow-hair-studio-abcdefghij{len(self.snapshots)}"
            url = f"{BASE}/s/{slug}" if self.snapshot_mode == "ok" else f"https://evil.example/s/{slug}"
            return httpx.Response(200, json={"slug": slug, "url": url, "expires_at": "2026-12-17T00:00:00Z"})
        return super().handler(request)

    def client(self) -> SuppressionClient:
        return SuppressionClient(BASE, CONFIG.api_key, transport=httpx.MockTransport(self.handler))

    def snapshot_client(self) -> SnapshotClient:
        return SnapshotClient(BASE, CONFIG.api_key, transport=httpx.MockTransport(self.handler))


@pytest.fixture
def site():
    return FakeSite()


# ─── model stubs ────────────────────────────────────────────────────────────


class FakeMessages:
    def __init__(self, answer):
        self.answer = answer   # a dict, a callable(kwargs) -> dict, or an Exception
        self.calls: list = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        answer = self.answer(kwargs) if callable(self.answer) else self.answer
        if isinstance(answer, Exception):
            raise answer
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text=json.dumps(answer))])


def stub_client(answer):
    messages = FakeMessages(answer)
    return SimpleNamespace(beta=SimpleNamespace(messages=messages)), messages


def labels_answer(labels, **extra) -> dict:
    return {"labels": list(labels), "language": extra.get("language", "en"),
            "asks_for_commitment": extra.get("asks_for_commitment", False),
            "possible_opt_out": extra.get("possible_opt_out", False),
            "possible_complaint": extra.get("possible_complaint", False),
            "summary": extra.get("summary", "The owner replied.")}


def writer_answer(body: str, language: str = "en-IN", reply_class: str = "INTERESTED") -> dict:
    return {"decision": "WRITE", "hold_reason": None, "declared_country": "IN", "country_name": "India",
            "declared_language": language, "language_basis": "owner_message", "language_self_check": language,
            "observation_type": None, "observation_evidence_value": None, "channel": "email", "touch": None,
            "reply_class": reply_class, "subject": None, "body": body, "signoff": "Regards,",
            "opt_out_line": None, "suppress": False, "call_requested": False, "pause_until": None,
            "needs_founder": False}


DEFAULT_DRAFT = ("Hello Glow Hair Studio team,\n\nThank you for your reply. The Launch website is a single page "
                 "with your services, WhatsApp and call buttons, and basic technical setup. It costs ₹7,999, and "
                 "the domain and hosting are charged separately. Is this a new website for your salon, and what "
                 "should your clients be able to do on it?")


def sample_draft(kwargs) -> dict:
    """Writer stub: puts the sample page link from the task into the body (as the real writer is told to)."""
    task = json.loads(kwargs["messages"][0]["content"])["TASK"]
    link = (task.get("attachments_allowed") or [None])[0]
    body = DEFAULT_DRAFT if not link else (
        "Hello Glow Hair Studio team,\n\nThank you for your reply. Here is the sample page I prepared for your "
        f"salon: {link}\n\nIt shows how your services and a WhatsApp button could look on a phone. The Launch "
        "website costs ₹7,999, and the domain and hosting are charged separately. Would you like to change "
        "anything on it?")
    return writer_answer(body)


@pytest.fixture
def models():
    """Default stubs: the classifier says `interested`, the writer writes DEFAULT_DRAFT / the sample draft."""
    classifier_client, classifier_calls = stub_client(labels_answer(["interested"]))
    writer_client, writer_calls = stub_client(sample_draft)
    return SimpleNamespace(classifier_client=classifier_client, classifier_calls=classifier_calls,
                           writer_client=writer_client, writer_calls=writer_calls)


def set_classifier(models, answer) -> None:
    models.classifier_calls.answer = answer


def set_writer(models, answer) -> None:
    models.writer_calls.answer = answer


# ─── data + loop builders ───────────────────────────────────────────────────


async def add_imap_mailbox(db, smtp_port: int = 2525) -> Mailbox:
    box = Mailbox(slug="TEST1", address=MAILBOX, display_name="Test Founder", domain="send-one.example",
                  enabled=True, smtp_host="127.0.0.1", smtp_port=smtp_port, smtp_tls=TlsMode.NONE,
                  imap_host="127.0.0.1", imap_port=1143, imap_tls=TlsMode.NONE, username=MAILBOX)
    db.add(box)
    await db.flush()
    return box


def make_loop(factory, clock, site: FakeSite, imap: FakeImapServer, models, api_key: bool = True,
              suppression=True) -> ReplyLoop:
    settings = WRITER_SETTINGS if api_key else Settings(
        _env_file=None, ANTHROPIC_API_KEY=None, SITEBLITZ_SENDER_NAME="Test Founder",
        SITEBLITZ_REPLY_EMAIL=MAILBOX, SITEBLITZ_POSTAL_ADDRESS="Test address, Gujarat")
    writer = OutreachWriter(client=models.writer_client, settings=settings)
    deps = ReplyLoopDeps(
        config=CONFIG, suppression=site.client() if suppression else None, snapshots=site.snapshot_client(),
        classifier=ReplyClassifier(lambda: models.classifier_client, api_key_set=api_key),
        writer_factory=lambda: writer, facts_md=FACTS_MD, imap_connector=imap.connector,
        password_lookup=lambda slug: None, clock=clock)
    return ReplyLoop(factory, deps)


def eml(body: str = "", *, subject: str = f"Re: {OUR_SUBJECT}", frm: str = f"Glow Owner <{OWNER}>",
        to: str = MAILBOX, in_reply_to: Optional[str] = None, references: Optional[list] = None,
        headers: Optional[dict] = None, message_id: Optional[str] = None,
        sent: datetime = datetime(2026, 11, 17, 10, 0, tzinfo=IST)) -> bytes:
    msg = EmailMessage()
    msg["From"] = frm
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = format_datetime(sent)
    msg["Message-ID"] = message_id or f"<reply-{abs(hash((body, subject, frm))) % 10**12}@mail.example>"
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = " ".join(references)
    for key, value in (headers or {}).items():
        msg[key] = value
    msg.set_content(body or "")
    return msg.as_bytes()


def case_raw(case: dict, message_id: str = "<step1@send-one.example>", in_reply_to: Optional[str] = None,
             frm: str = f"Glow Owner <{OWNER}>") -> bytes:
    if case.get("raw"):
        return case["raw"].replace("{MESSAGE_ID}", message_id).replace("\n", "\r\n").encode("utf-8")
    return eml(case.get("body", ""), subject=case.get("subject", EVAL_SET["default_subject"]),
               headers=case.get("headers"), in_reply_to=in_reply_to,
               references=[in_reply_to] if in_reply_to else None, frm=frm,
               message_id=f"<{case['id']}@mail.example>")


RECEIVED = date(2026, 11, 17)
NOW_AFTER_REPLY = ist(TUE, 12, 0)


def at(day: date, hh: int, mm: int = 0) -> datetime:
    return ist(day, hh, mm)


def utc(moment: datetime) -> datetime:
    return moment.astimezone(timezone.utc)


__all__ = ["timedelta"]
