"""
Fixtures for the E3 batch API: the real FastAPI app on a throw-away SQLite file, settings from monkeypatched
environment variables (test values only), the model replaced by backend/tests/pilot_fakes.py. Nothing is sent and
no model is called. Every business is fictional (.example domains).
"""

import asyncio
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import backend.app.database as database
import backend.app.models  # noqa: F401
from backend.app.config import get_settings
from backend.app.database import Base
from backend.app.engines.eligibility.rules import social_only_text
from backend.app.engines.sending import scheduler as sched
from backend.app.engines.sending.tokens import email_hash
from backend.app.models.business import Business, BusinessCategory, BusinessLocation
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
from backend.tests.pilot_fakes import pilot_fake_client

IST = sched.load_zone("Asia/Kolkata")
SECRET = "test-secret-not-for-production-0123456789"
ENV = {"OUTREACH_API_KEY": "test-api-key-not-for-production-0123456789", "OUTREACH_SIGNING_SECRET": SECRET,
       "OUTREACH_PUBLIC_BASE_URL": "https://siteblitz.example", "SITEBLITZ_SENDER_NAME": "Test Founder",
       "SITEBLITZ_REPLY_EMAIL": "test.founder@send-one.example", "SITEBLITZ_POSTAL_ADDRESS": "Test address, Gujarat",
       "ANTHROPIC_API_KEY": ""}


def next_tuesday():
    today = datetime.now(timezone.utc).astimezone(IST).date()
    return today + timedelta(days=((1 - today.weekday()) % 7) or 7)


async def add_lead(db, name: str, email: str, eligible: bool = True, holds=None) -> EmailEligibility:
    checked = datetime.now(timezone.utc) - timedelta(days=1)
    business = Business(name=name, normalized_name=name.lower(), country_code="IN", website_url=None,
                        social_urls={"instagram": f"https://www.instagram.com/{name.lower().replace(' ', '')}/"})
    db.add(business)
    await db.flush()
    db.add(BusinessLocation(business_id=business.id, city="Surat", country_code="IN", state_province="Gujarat"))
    db.add(BusinessCategory(business_id=business.id, category_name="beauty_salon", normalized_category="beauty_salon",
                            is_primary=True))
    capture = EmailCapture(business_id=business.id, email=email, method=CaptureMethod.FOUNDER_CONFIRMED,
                           source_url=business.social_urls["instagram"], excerpt=f"bio shows {email}",
                           captured_at=checked, origin="pool_e1:2026-11-12", capture_key=f"k-{name}-{email}")
    db.add(capture)
    await db.flush()
    row = EmailEligibility(business_id=business.id, email=email, email_hash=email_hash(email),
                           tier=EligibilityTier.TIER1, capture_id=capture.id, method=CaptureMethod.FOUNDER_CONFIRMED,
                           source_url=capture.source_url, captured_at=checked, excerpt=capture.excerpt,
                           recipient_type=RecipientType.BUSINESS,
                           verification_status=VerificationStatus.VALID if eligible else VerificationStatus.UNVERIFIED,
                           verification_provider="bouncer" if eligible else None,
                           verified_at=checked if eligible else None, country="IN", vertical="salon_beauty",
                           observation_type=ObservationType.SOCIAL_ONLY,
                           observation_text=social_only_text(checked, name), observation_checked_at=checked,
                           suppressed=False, hold_reasons=[] if eligible else (holds or ["NOT_VERIFIED"]),
                           eligible=eligible, eligible_if_verified=True, evaluated_at=checked)
    db.add(row)
    await db.flush()
    return row


async def seed(url: str, ramp_stage: int = 1, leads: int = 11) -> dict:
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        for slug, address, display in (("ASHA", "asha@send-one.example", "Asha Test"),
                                       ("RAVI", "ravi@send-two.example", "Ravi Test")):
            db.add(Mailbox(slug=slug, address=address, display_name=display, domain=address.split("@")[1],
                           enabled=True, smtp_host="smtp.send.example", smtp_port=587, smtp_tls=TlsMode.STARTTLS,
                           username=address))
        if ramp_stage:
            db.add(RampSetting(stage=ramp_stage, daily_new_limit=sched.ramp_limit(ramp_stage), changed_by="test",
                               note="test", changed_at=datetime.now(timezone.utc) - timedelta(days=1)))
        rows = [await add_lead(db, f"Kesar Salon {i}", f"info{i}@kesar{i}.example") for i in range(leads)]
        held = await add_lead(db, "Held Salon", "info@held.example", eligible=False,
                              holds=["NOT_VERIFIED", "NEEDS_FOUNDER_CHECK"])
        await db.commit()
        ids = {"eligible": [r.id for r in rows], "held": held.id}
    await engine.dispose()
    return ids


class Api:
    def __init__(self, client, ids, messages):
        self.client, self.ids, self.messages = client, ids, messages

    def create(self, ids, send_date=None, created_by="Founder"):
        return self.client.post("/api/v1/outreach/batches", json={
            "eligibility_ids": ids, "send_date": (send_date or next_tuesday()).isoformat(), "created_by": created_by})

    def detail(self, batch_id):
        response = self.client.get(f"/api/v1/outreach/batches/{batch_id}")
        assert response.status_code == 200, response.text
        return response.json()


def make_api(tmp_path, monkeypatch, ramp_stage=1, bad=(), env=None, stub=True, leads=11):
    url = f"sqlite+aiosqlite:///{tmp_path / 'batches.db'}"
    ids = asyncio.run(seed(url, ramp_stage, leads))
    monkeypatch.setenv("DATABASE_URL", url)
    for name, value in {**ENV, **(env or {})}.items():
        monkeypatch.setenv(name, value)
    get_settings.cache_clear()
    monkeypatch.setattr(database, "_async_engine", None)
    monkeypatch.setattr(database, "_async_session_factory", None)
    from backend.app.api.v1.outreach_batches import get_writer_client
    from backend.app.main import app
    client_stub, messages = pilot_fake_client(bad=bad)
    if stub:
        app.dependency_overrides[get_writer_client] = lambda: client_stub
    return app, ids, messages


@pytest.fixture
def api_factory(tmp_path, monkeypatch):
    opened = []

    def build(**kwargs):
        app, ids, messages = make_api(tmp_path, monkeypatch, **kwargs)
        client = TestClient(app)
        client.__enter__()
        opened.append((app, client))
        return Api(client, ids, messages)

    yield build
    for app, client in opened:
        client.__exit__(None, None, None)
        app.dependency_overrides.clear()
    get_settings.cache_clear()


@pytest.fixture
def api(api_factory):
    return api_factory()
