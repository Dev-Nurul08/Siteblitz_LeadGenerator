"""
Email engine v2 E1 - outreach API: eligibility list / evaluate and the founder's Instagram-bio confirmations.
Real FastAPI app on a throw-away SQLite file; the verifier ladder is stubbed (no DNS, no Bouncer).
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
from backend.app.services import eligibility_service

from .conftest import add_business, ladder, no_viewport_lead

PROFILE = "https://www.instagram.com/glowhair.surat/"


async def _seed(url: str) -> dict:
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        social = await add_business(db, name="Glow Hair Studio", website=None,
                                    social_urls={"instagram": PROFILE})
        abroad = await add_business(db, name="Austin Salon", website=None, country="US",
                                    social_urls={"instagram": "https://instagram.com/austinsalon"})
        site = await no_viewport_lead(db, name="Tutor Point", website="https://tutorpoint.in",
                                      email="info@tutorpoint.in")
        ids = {"social": social.id, "abroad": abroad.id, "site": site.id}
        await db.commit()
    await engine.dispose()
    return ids


@pytest.fixture
def api(tmp_path, monkeypatch):
    url = f"sqlite+aiosqlite:///{tmp_path / 'api.db'}"
    ids = asyncio.run(_seed(url))
    monkeypatch.setenv("DATABASE_URL", url)
    get_settings.cache_clear()
    monkeypatch.setattr(database, "_async_engine", None)
    monkeypatch.setattr(database, "_async_session_factory", None)
    monkeypatch.setattr(eligibility_service.VerificationLadder, "from_settings", classmethod(lambda cls, s: ladder()))
    from backend.app.main import app

    with TestClient(app) as client:
        yield client, ids
    get_settings.cache_clear()


def confirmation(business_id, **kw):
    body = {"business_id": business_id, "profile_url": PROFILE,
            "checked_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "website_link_present": False, "email_seen": "GlowHair.Surat@Gmail.com"}
    body.update(kw)
    return body


@pytest.mark.parametrize("params", [{"status": "all"}, {"limit": 0}, {"limit": 501}, {"limit": "ten"}])
def test_eligibility_list_validates_query(api, params):
    client, _ = api
    assert client.get("/api/v1/outreach/eligibility", params=params).status_code == 422


@pytest.mark.parametrize("body", [{"business_ids": [0]}, {"business_ids": "1"}, {"verify": "maybe"},
                                  {"business_id": 1}, {"business_ids": list(range(1, 1003))}])
def test_evaluate_validates_body(api, body):
    client, _ = api
    assert client.post("/api/v1/outreach/eligibility/evaluate", json=body).status_code == 422


def test_evaluate_and_list_with_counts(api):
    client, ids = api
    result = client.post("/api/v1/outreach/eligibility/evaluate", json={"verify": True})
    assert result.status_code == 200, result.text
    summary = result.json()
    assert (summary["rows"], summary["eligible"], summary["eligible_if_verified"]) == (1, 0, 1)
    assert summary["by_hold_reason"] == {"NOT_VERIFIED": 1} and summary["paid_verifier_configured"] is False

    listed = client.get("/api/v1/outreach/eligibility", params={"status": "hold", "limit": 5}).json()
    assert listed["total"] == 1 and listed["counts"]["by_hold_reason"] == {"NOT_VERIFIED": 1}
    row = listed["items"][0]
    assert row["business_id"] == ids["site"] and row["provenance"]["source_url"].startswith("https://tutorpoint.in")
    assert row["observation"]["type"] == "NO_VIEWPORT" and row["verification_status"] == "UNVERIFIED"
    assert client.get("/api/v1/outreach/eligibility", params={"status": "eligible"}).json()["total"] == 0


@pytest.mark.parametrize("change", [
    {"profile_url": "https://facebook.com/glowhair"},       # spec row 4 is about the Instagram bio
    {"profile_url": "javascript:alert(1)"},
    {"email_seen": "not-an-email"},
    {"website_link_present": "no"},                         # a real true / false only
    {"website_link_present": None},
    {"business_id": 0},
    {"checked_at": "yesterday"},
    {"note": "extra field"},
])
def test_confirmation_validation(api, change):
    client, ids = api
    body = {**confirmation(ids["social"]), **change}
    response = client.post("/api/v1/outreach/confirmations", json=body)
    assert response.status_code == 422, response.text


def test_confirmation_in_the_future_or_unknown_business(api):
    client, ids = api
    future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    assert client.post("/api/v1/outreach/confirmations",
                       json=confirmation(ids["social"], checked_at=future)).status_code == 422
    assert client.post("/api/v1/outreach/confirmations", json=confirmation(99999)).status_code == 404


def test_pending_then_confirmed_gives_tier1_social_only(api):
    client, ids = api
    pending = client.get("/api/v1/outreach/confirmations/pending").json()
    assert [(i["business_id"], i["profile_url"]) for i in pending["items"]] == [(ids["social"], PROFILE)]

    response = client.post("/api/v1/outreach/confirmations", json=confirmation(ids["social"]))
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["confirmation"]["email_seen"] == "glowhair.surat@gmail.com"
    row = body["eligibility"][0]
    assert row["tier"] == "TIER1" and row["provenance"]["method"] == "founder_confirmed"
    assert row["provenance"]["source_url"] == PROFILE
    assert row["observation"]["type"] == "SOCIAL_ONLY"
    assert row["observation"]["text"].endswith(
        "the Instagram profile for Glow Hair Studio showed no website link when we checked its bio.")
    assert row["hold_reasons"] == ["NOT_VERIFIED"] and row["eligible_if_verified"] is True

    assert client.get("/api/v1/outreach/confirmations/pending").json()["total"] == 0


def test_confirmation_with_a_website_link_gives_no_observation(api):
    client, ids = api
    body = client.post("/api/v1/outreach/confirmations",
                       json=confirmation(ids["social"], website_link_present=True)).json()
    assert "NO_PILOT_OBSERVATION" in body["eligibility"][0]["hold_reasons"]


def test_confirmed_business_outside_india_stays_held(api):
    client, ids = api
    body = client.post("/api/v1/outreach/confirmations",
                       json=confirmation(ids["abroad"], profile_url="https://instagram.com/austinsalon")).json()
    assert "COUNTRY_NOT_IN_PILOT" in body["eligibility"][0]["hold_reasons"]
