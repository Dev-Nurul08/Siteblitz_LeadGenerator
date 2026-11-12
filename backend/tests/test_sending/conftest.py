"""
Shared fixtures for email engine v2 E2 (sending core). No test here touches the network or a real mailbox:
- the website's suppression API is an httpx.MockTransport (FakeWebsite);
- SMTP goes to an aiosmtpd server on 127.0.0.1 started per test (SmtpServer);
- E1's recheck_before_send is either a stub (FakeEligibility) or the real service with stubbed DNS / homepage checks.
Config is built directly (never from a real .env), like the writer tests.
"""

import asyncio
import socket
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

import httpx
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import backend.app.models  # noqa: F401  (registers every table on Base.metadata)
from backend.app.database import Base
from backend.app.engines.sending import scheduler as sched
from backend.app.engines.sending.suppression_client import SuppressionClient
from backend.app.engines.sending.tokens import email_hash
from backend.app.models.business import Business, BusinessLocation
from backend.app.models.eligibility import (
    CaptureMethod,
    EligibilityTier,
    EmailCapture,
    EmailEligibility,
    ObservationType,
    RecipientType,
    VerificationStatus,
)
from backend.app.models.sending import Mailbox, RampSetting, TlsMode
from backend.app.services.outreach_worker import OutreachWorker
from backend.app.services.sending_service import SendingConfig, SendingService

IST = sched.load_zone("Asia/Kolkata")
TUE = date(2026, 11, 17)
WED, THU = date(2026, 11, 18), date(2026, 11, 19)
NEXT_TUE = date(2026, 11, 24)
SECRET = "kat-secret-not-for-production-0123456789"
BASE = "https://siteblitz.example"
CONFIG = SendingConfig(api_key="test-api-key-not-for-production-0123456789", signing_secret=SECRET, base_url=BASE,
                       sender_name="Test Founder", reply_email="test.founder@send-one.example",
                       postal_address="Test address, Gujarat")


def ist(day: date, hh: int, mm: int = 0) -> datetime:
    return datetime(day.year, day.month, day.day, hh, mm, tzinfo=IST).astimezone(timezone.utc)


BEFORE = datetime(2026, 11, 12, 6, 0, tzinfo=timezone.utc)   # Thursday before TUE: when batches are approved


class Clock:
    def __init__(self, now: datetime):
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def at(self, moment: datetime) -> "Clock":
        self.now = sched.aware(moment)   # SQLite gives naive UTC back
        return self


@pytest.fixture
async def factory(tmp_path):
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'e2.db'}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


@pytest.fixture
async def session(factory):
    async with factory() as db:
        yield db


# ─── the website's suppression API ──────────────────────────────────────────


@dataclass
class FakeWebsite:
    suppressed: set = field(default_factory=set)
    mode: str = "ok"            # ok | down (503) | unauthorized (401) | timeout | refused | garbage
    added: list = field(default_factory=list)
    checks: int = 0

    def handler(self, request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == f"Bearer {CONFIG.api_key}"
        if self.mode == "timeout":
            raise httpx.ReadTimeout("timed out", request=request)
        if self.mode == "refused":
            raise httpx.ConnectError("refused", request=request)
        if self.mode == "down":
            return httpx.Response(503, json={"ok": False})
        if self.mode == "unauthorized":
            return httpx.Response(401, json={"ok": False})
        if self.mode == "garbage":
            return httpx.Response(200, text="<html>oops</html>")
        import json
        body = json.loads(request.content or b"{}")
        if request.url.path == "/api/outreach/suppressions/check":
            self.checks += 1
            return httpx.Response(200, json={"ok": True, "suppressed": [h for h in body["hashes"]
                                                                         if h in self.suppressed],
                                             "checked_at": "2026-11-17T03:30:00Z"},
                                  headers={"Cache-Control": "no-store"})
        if request.url.path == "/api/outreach/suppressions" and request.method == "POST":
            self.added.append(body)
            self.suppressed.add(body["hash"])
            return httpx.Response(200, json={"ok": True})
        if request.url.path == "/api/outreach/suppressions" and request.method == "GET":
            return httpx.Response(200, json={"ok": True, "items": [
                {"hash": h, "reason": "unsubscribe_one_click", "created_at": "2026-11-16T10:00:00Z"}
                for h in sorted(self.suppressed)], "next": None})
        return httpx.Response(404, json={"ok": False})

    def client(self) -> SuppressionClient:
        return SuppressionClient(BASE, CONFIG.api_key, transport=httpx.MockTransport(self.handler))


@pytest.fixture
def website():
    return FakeWebsite()


# ─── SMTP test server on 127.0.0.1 ──────────────────────────────────────────


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


class Collector:
    def __init__(self):
        self.envelopes = []
        self.data_started = 0     # complete messages received (counted before the handler answers)
        self.data_delay = 0.0
        self.rcpt_answer = None   # e.g. "550 5.1.1 <x>: Recipient address rejected: User unknown"
        self.data_answer = "250 2.0.0 Ok: queued"

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if self.rcpt_answer:
            return self.rcpt_answer
        envelope.rcpt_tos.append(address)
        return "250 OK"

    async def handle_DATA(self, server, session, envelope):
        self.data_started += 1
        if self.data_delay:
            await asyncio.sleep(self.data_delay)
        self.envelopes.append(envelope)
        return self.data_answer


@pytest.fixture
def smtp_server():
    from aiosmtpd.controller import Controller
    collector = Collector()
    controller = Controller(collector, hostname="127.0.0.1", port=free_port())
    controller.start()
    collector.port = controller.port
    yield collector
    controller.stop()


# ─── data builders ──────────────────────────────────────────────────────────


async def add_mailbox(db, port: int = 2525, slug: str = "TEST1", address: str = "test.founder@send-one.example",
                      display_name: str = "Test Founder", tls: TlsMode = TlsMode.NONE, host: str = "127.0.0.1"
                      ) -> Mailbox:
    box = Mailbox(slug=slug, address=address, display_name=display_name, domain=address.rsplit("@", 1)[1],
                  enabled=True, smtp_host=host, smtp_port=port, smtp_tls=tls, username=address)
    db.add(box)
    await db.flush()
    return box


async def set_ramp(db, stage: int = 1) -> None:
    db.add(RampSetting(stage=stage, daily_new_limit=sched.ramp_limit(stage), changed_by="test", note="test",
                       changed_at=BEFORE))
    await db.flush()


async def add_lead(db, name: str = "Glow Hair Studio", email: str = "info@glowhair.example", country="IN",
                   origin: str = "pool_e1:2026-11-12", eligible: bool = True) -> EmailEligibility:
    business = Business(name=name, normalized_name=name.lower(), country_code=country, website_url=None)
    db.add(business)
    await db.flush()
    db.add(BusinessLocation(business_id=business.id, city="Surat", country_code=country))
    capture = EmailCapture(business_id=business.id, email=email, method=CaptureMethod.FOUNDER_CONFIRMED,
                           source_url="https://www.instagram.com/example/", excerpt=f"bio shows {email}",
                           captured_at=BEFORE - timedelta(days=1), origin=origin, capture_key=f"k-{name}-{email}")
    db.add(capture)
    await db.flush()
    row = EmailEligibility(business_id=business.id, email=email, email_hash=email_hash(email),
                           tier=EligibilityTier.TIER1, capture_id=capture.id, method=CaptureMethod.FOUNDER_CONFIRMED,
                           recipient_type=RecipientType.BUSINESS, verification_status=VerificationStatus.VALID,
                           country=country, vertical="salon_beauty", observation_type=ObservationType.SOCIAL_ONLY,
                           observation_text="On 11 November 2026, the Instagram profile showed no website link.",
                           observation_checked_at=BEFORE - timedelta(days=1), suppressed=False,
                           hold_reasons=[] if eligible else ["NOT_VERIFIED"], eligible=eligible,
                           eligible_if_verified=True, evaluated_at=BEFORE)
    db.add(row)
    await db.flush()
    return row


STEP1_BODY = ("On 11 November 2026, the Instagram profile for Glow Hair Studio showed no website link.\n\n"
              "I'm Test Founder from SiteBlitz, a small web studio in Gujarat.\n\n"
              "Website setup starts at ₹7,999, with domain and hosting charged separately.\n\n"
              "Shall I make a sample page for Glow Hair Studio and send it here?\n\n"
              "Test Founder | SiteBlitz\n"
              'Reply "stop" or unsubscribe here: [unsubscribe URL]')


def item(row: EmailEligibility, subject: str = "Glow Hair Studio: no website link in Instagram bio") -> dict:
    return {"eligibility_id": row.id, "subject": subject, "body": STEP1_BODY, "content_version": "t1-v1",
            "approved_by": "founder"}


async def admitted_sequence(db, day: date = TUE, **lead_kwargs) -> dict:
    """One lead admitted for `day` (step 1 approved; steps 2 / 3 reserved, not yet written)."""
    row = await add_lead(db, **lead_kwargs)
    result = await SendingService(db, CONFIG).create_sequences(day, [item(row)], now=BEFORE)
    assert result["admitted"], result["refused"]
    await db.commit()
    return result["admitted"][0]


class FakeEligibility:
    """Stands in for E1's EligibilityService.recheck_before_send. `outcomes[business_id]` overrides the answer."""

    outcomes: dict = {}
    calls: list = []

    def __init__(self, session):
        self.session = session

    async def recheck_before_send(self, business_id, now=None):
        FakeEligibility.calls.append(business_id)
        override = FakeEligibility.outcomes.get(business_id)
        if override is not None:
            return override
        from sqlalchemy import select
        email = (await self.session.execute(select(EmailEligibility.email).where(
            EmailEligibility.business_id == business_id))).scalars().first()
        return {"business_id": business_id, "send_allowed": True, "reason": None, "send_to": email,
                "site_check": None, "rows": []}


@pytest.fixture(autouse=True)
def _reset_fake_eligibility():
    FakeEligibility.outcomes, FakeEligibility.calls = {}, []
    yield


def make_worker(factory, clock: Clock, website: FakeWebsite, config: SendingConfig = CONFIG,
                eligibility=FakeEligibility, **kwargs) -> OutreachWorker:
    kwargs.setdefault("inbox_guard", None)   # E4's inbox guard has its own tests (test_replies)
    return OutreachWorker(factory, config, website.client(), eligibility_factory=eligibility,
                          password_lookup=lambda slug: None, clock=clock, **kwargs)
