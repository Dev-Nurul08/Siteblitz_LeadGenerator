"""
E2 outreach sending API on the real FastAPI app and a throw-away SQLite file. Settings come from monkeypatched
environment variables (test values only); nothing is sent.
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
from backend.app.engines.sending import scheduler as sched
from backend.app.models.sending import PauseFlag, PauseScope

from .conftest import CONFIG, add_lead

IST = sched.load_zone("Asia/Kolkata")
SECRET_VALUE = "very-secret-mailbox-password-for-tests"


def next_tuesday():
    today = datetime.now(timezone.utc).astimezone(IST).date()
    return today + timedelta(days=((1 - today.weekday()) % 7) or 7)


async def _seed(url: str) -> dict:
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        rows = [await add_lead(db, name=f"Salon {i}", email=f"info{i}@salon{i}.example") for i in range(11)]
        held = await add_lead(db, name="Held Salon", email="info@held.example", eligible=False)
        db.add(PauseFlag(scope=PauseScope.SOURCE_BATCH, scope_value="old:batch", reason_code="HARD_BOUNCE",
                         created_at=datetime.now(timezone.utc)))
        await db.commit()
        ids = {"eligible": [r.id for r in rows], "held": held.id}
    await engine.dispose()
    return ids


@pytest.fixture
def api(tmp_path, monkeypatch):
    url = f"sqlite+aiosqlite:///{tmp_path / 'api.db'}"
    ids = asyncio.run(_seed(url))
    monkeypatch.setenv("DATABASE_URL", url)
    for name, value in (("OUTREACH_API_KEY", CONFIG.api_key), ("OUTREACH_SIGNING_SECRET", CONFIG.signing_secret),
                        ("OUTREACH_PUBLIC_BASE_URL", CONFIG.base_url), ("SITEBLITZ_SENDER_NAME", "Test Founder"),
                        ("SITEBLITZ_REPLY_EMAIL", "test.founder@send-one.example"),
                        ("SITEBLITZ_POSTAL_ADDRESS", "Test address, Gujarat")):
        monkeypatch.setenv(name, value)
    monkeypatch.delenv("MAILBOX_TEST1_PASSWORD", raising=False)
    get_settings.cache_clear()
    monkeypatch.setattr(database, "_async_engine", None)
    monkeypatch.setattr(database, "_async_session_factory", None)
    from backend.app.main import app

    with TestClient(app) as client:
        yield client, ids
    get_settings.cache_clear()


MAILBOX = {"slug": "test1", "address": "Test.Founder@send-one.example", "display_name": "Test Founder",
           "smtp_host": "smtp.send-one.example", "smtp_port": 587, "smtp_tls": "starttls",
           "imap_host": "imap.send-one.example", "imap_port": 993, "imap_tls": "ssl",
           "username": "test.founder@send-one.example"}


def test_mailboxes_never_carry_a_password(api, monkeypatch):
    client, _ = api
    created = client.post("/api/v1/outreach/mailboxes", json=MAILBOX)
    assert created.status_code == 200, created.text
    body = created.json()
    assert body["slug"] == "TEST1" and body["address"] == "test.founder@send-one.example"
    assert body["from_header"] == '"Test Founder, SiteBlitz" <test.founder@send-one.example>'
    assert body["password_variable"] == "MAILBOX_TEST1_PASSWORD" and body["password_configured"] is False
    monkeypatch.setenv("MAILBOX_TEST1_PASSWORD", SECRET_VALUE)
    listed = client.get("/api/v1/outreach/mailboxes")
    assert listed.json()["items"][0]["password_configured"] is True
    assert SECRET_VALUE not in listed.text and "password\"" not in listed.text.replace("password_", "")
    disabled = client.post("/api/v1/outreach/mailboxes",
                           json={**MAILBOX, "enabled": False, "disabled_reason": "rested"})
    assert disabled.json()["enabled"] is False and disabled.json()["id"] == body["id"]


@pytest.mark.parametrize("change", [
    {"password": "x"},                                     # a password can never be posted
    {"smtp_host": "smtp.gmail.com"},                       # spec row 8: not Gmail / Workspace
    {"smtp_host": "smtp.office365.com"},
    {"smtp_host": "email-smtp.ap-south-1.amazonaws.com"},
    {"smtp_tls": "none"},                                  # plain SMTP only for a loopback test server
    {"display_name": "SiteBlitz"},
    {"display_name": "x@y.example"},
    {"address": "founder@gmail.com"},
    {"slug": "bad slug!"},
    {"smtp_port": 0},
])
def test_mailbox_validation(api, change):
    client, _ = api
    assert client.post("/api/v1/outreach/mailboxes", json={**MAILBOX, **change}).status_code == 422


def test_ramp_changes_only_by_an_explicit_call_one_stage_at_a_time(api):
    client, _ = api
    assert client.get("/api/v1/outreach/settings/ramp").json()["daily_new_limit"] == 0   # not started
    assert client.post("/api/v1/outreach/settings/ramp",
                       json={"stage": 2, "changed_by": "founder", "note": "skip"}).status_code == 409
    assert client.post("/api/v1/outreach/settings/ramp", json={"stage": 1, "changed_by": "founder"}).status_code == 422
    body = client.post("/api/v1/outreach/settings/ramp",
                       json={"stage": 1, "changed_by": "founder", "note": "launch gates passed"}).json()
    assert (body["stage"], body["daily_new_limit"]) == (1, 10)
    assert body["history"][0]["changed_by"] == "founder" and body["history"][0]["changed_at"]
    for stage, limit in ((2, 15), (3, 20), (4, 20)):
        body = client.post("/api/v1/outreach/settings/ramp",
                           json={"stage": stage, "changed_by": "founder", "note": "gate passed"}).json()
        assert body["daily_new_limit"] == limit


def batch(ids, send_date, approved_by="founder"):
    return {"send_date": send_date.isoformat(), "items": [
        {"eligibility_id": i, "subject": f"Salon {n}: no website link in Instagram bio",
         "body": "On 11 November 2026, the Instagram profile showed no website link.\n\nShall I make a sample page?",
         "content_version": "t1-v1", "approved_by": approved_by} for n, i in enumerate(ids)]}


def test_sequences_schedule_and_capacity(api):
    client, ids = api
    day = next_tuesday()
    assert client.post("/api/v1/outreach/mailboxes", json={**MAILBOX, "smtp_host": "127.0.0.1", "smtp_tls": "none",
                                                           "imap_host": None, "imap_port": None,
                                                           "imap_tls": None}).status_code == 200
    client.post("/api/v1/outreach/settings/ramp", json={"stage": 1, "changed_by": "founder", "note": "launch gates passed"})
    result = client.post("/api/v1/outreach/sequences", json=batch(ids["eligible"] + [ids["held"]], day))
    assert result.status_code == 200, result.text
    body = result.json()
    assert len(body["admitted"]) == 10, body["refused"][:2]
    refused = {r["eligibility_id"]: r for r in body["refused"]}
    eleventh = refused[ids["eligible"][10]]
    assert eleventh["code"] == "RAMP_LIMIT_REACHED"
    assert eleventh["message"] == (f"10 new first contacts are already scheduled for {day.isoformat()}; "
                                   "the current ramp allows 10 a day")
    assert refused[ids["held"]]["code"] == "NOT_ELIGIBLE"
    first = body["admitted"][0]["records"]
    assert [r["step"] for r in first] == [1, 2, 3] and first[0]["approved_by"] == "founder"
    assert first[1]["approved_by"] is None and first[1]["has_body"] is False

    again = client.post("/api/v1/outreach/sequences", json=batch(ids["eligible"][:1], day + timedelta(days=1)))
    assert again.json()["refused"][0]["code"] == "ALREADY_IN_SEQUENCE"

    schedule = client.get("/api/v1/outreach/schedule", params={"date": day.isoformat()}).json()
    assert len(schedule["items"]) == 10 and schedule["counts"] == {"SCHEDULED": 10}
    assert {i["window"] for i in schedule["items"]} == {"09:00-11:30", "14:00-16:30"}
    capacity = client.get("/api/v1/outreach/capacity", params={"date": day.isoformat()}).json()
    assert capacity["new_contacts"] == {"scheduled": 10, "daily_limit": 10, "free": 0}
    box = capacity["mailboxes"][0]
    assert (box["campaign_reserved"], box["campaign_free"], box["daily_ceiling"], box["reply_reserve"]) == (
        10, 15, 30, 5)
    assert client.get("/api/v1/outreach/capacity").status_code == 422
    assert client.get("/api/v1/outreach/schedule", params={"date": "17-11-2026"}).status_code == 422

    step2 = first[1]["id"]
    approved = client.post(f"/api/v1/outreach/send-records/{step2}/approve",
                           json={"body": "Following up on my note.", "approved_by": "founder"})
    assert approved.status_code == 200 and approved.json()["approved_by"] == "founder"
    assert client.post(f"/api/v1/outreach/send-records/{first[0]['id']}/approve",
                       json={"body": "x", "approved_by": "founder"}).status_code == 409
    resolve = client.post(f"/api/v1/outreach/send-records/{first[0]['id']}/resolve",
                          json={"outcome": "ACCEPTED", "resolved_by": "founder", "note": "checked"})
    assert resolve.status_code == 409                       # only an UNCERTAIN record can be resolved
    assert client.post(f"/api/v1/outreach/send-records/{first[0]['id']}/resolve",
                       json={"outcome": "MAYBE", "resolved_by": "founder", "note": "checked"}).status_code == 422


@pytest.mark.parametrize("body", [
    {"send_date": "2026-11-17", "items": []},
    {"send_date": "tuesday", "items": [{"eligibility_id": 1, "subject": "s", "body": "b", "approved_by": "f"}]},
    {"send_date": "2026-11-17", "items": [{"eligibility_id": 1, "subject": "s", "body": "b"}]},       # not approved
    {"send_date": "2026-11-17", "items": [{"eligibility_id": 1, "subject": "s", "body": "b", "approved_by": " "}]},
    {"send_date": "2026-11-17", "items": [{"eligibility_id": 0, "subject": "s", "body": "b", "approved_by": "f"}]},
])
def test_sequence_request_validation(api, body):
    client, _ = api
    assert client.post("/api/v1/outreach/sequences", json=body).status_code == 422


def test_pauses_are_listed_and_cleared_with_who_and_a_note(api):
    client, _ = api
    active = client.get("/api/v1/outreach/pauses", params={"active": "true"}).json()["items"]
    assert len(active) == 1 and active[0]["reason_code"] == "HARD_BOUNCE"
    pause_id = active[0]["id"]
    assert client.post("/api/v1/outreach/pauses", json={"pause_id": pause_id, "cleared_by": "founder"}
                       ).status_code == 422
    cleared = client.post("/api/v1/outreach/pauses",
                          json={"pause_id": pause_id, "cleared_by": "founder", "note": "batch re-checked"})
    assert cleared.status_code == 200
    assert cleared.json()["active"] is False and cleared.json()["cleared_by"] == "founder"
    assert client.post("/api/v1/outreach/pauses", json={"pause_id": pause_id, "cleared_by": "founder",
                                                        "note": "again"}).status_code == 409
    assert client.post("/api/v1/outreach/pauses", json={"pause_id": 999, "cleared_by": "founder",
                                                        "note": "missing"}).status_code == 404
    assert client.get("/api/v1/outreach/pauses", params={"active": "true"}).json()["items"] == []
