"""
Phase E3 acceptance (docs/spec/email-engine-v2.md): batch create / cap refusal (the 11th on a 10-a-day day) /
ineligible refusal / write T1-T3 / HOLD codes / approve into E2 sequences / reject. Real app, throw-away SQLite,
stub model, nothing sent.
"""

import json
from datetime import datetime, timezone

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from backend.app.config import get_settings
from backend.app.engines.writer.validator import UNSUBSCRIBE_PLACEHOLDER
from backend.app.models.sending import EmailSequence, PauseFlag, PauseScope, SendRecord, SendState

from .conftest import next_tuesday

BATCHES = "/api/v1/outreach/batches"


def sync_session():
    url = get_settings().DATABASE_URL.replace("+aiosqlite", "")
    return Session(create_engine(url))


def written(api, ids):
    created = api.create(ids)
    assert created.status_code == 202, created.text
    body = created.json()
    # every lead held at selection (e.g. a blank company fact) leaves nothing to write: the batch is DONE at once
    assert body["status"] in ("WRITING", "DONE") and body["writing_active"] is True
    return api.detail(body["id"])      # the background task has finished when the TestClient call returns


def test_create_writes_three_texts_per_lead_with_evidence_and_a_proposed_schedule(api):
    batch = written(api, api.ids["eligible"][:3])
    assert batch["status"] == "REVIEW" and batch["counts"] == {"READY": 3}
    assert batch["send_date"] == next_tuesday().isoformat() and batch["template_version"] == "pilot-v1"
    lead = batch["leads"][0]
    name = lead["business_name"]
    assert lead["state"] == "READY" and lead["hold_reasons"] == []
    assert lead["subject"] == f"{name}: no website link in Instagram bio"
    t1, t2, t3 = lead["texts"]["t1"], lead["texts"]["t2"], lead["texts"]["t3"]
    assert t1.startswith(lead["evidence"]["observation"]["text"])
    sender = lead["sender_name"]
    assert f"I'm {sender} from SiteBlitz, a small web studio in Gujarat." in t1
    assert "Website setup starts at ₹7,999, with domain and hosting charged separately.\n\n" \
           f"Shall I make a sample page for {name} and send it here?" in t1
    for text in (t1, t2, t3):
        assert f"{sender} | SiteBlitz" in text and "WhatsApp: +91 92744 90242" in text
        assert text.endswith(f'Reply "stop" or unsubscribe here: {UNSUBSCRIBE_PLACEHOLDER}')
    assert "sample page" in t2 and "No further follow-ups are planned." in t3
    evidence = lead["evidence"]
    assert evidence["observation"]["type"] == "SOCIAL_ONLY"
    assert evidence["observation"]["evidence_url"].startswith("https://www.instagram.com/")
    assert evidence["provenance"]["source_url"] and evidence["provenance"]["captured_at"]
    assert evidence["provenance"]["excerpt"].startswith("bio shows ")
    assert evidence["verification"]["status"] == "VALID"
    assert lead["schedule_kind"] == "proposed"
    plan = lead["schedule"]
    assert plan["display_name"] == sender and [s["step"] for s in plan["steps"]] == [1, 2, 3]
    assert plan["steps"][0]["local_date"] == next_tuesday().isoformat()
    # the batch spreads over both mailboxes (least loaded first) and each text names its own mailbox's sender
    assert {lead["sender_name"] for lead in batch["leads"]} == {"Asha Test", "Ravi Test"}
    assert all(f"| SiteBlitz\n{lead['schedule']['mailbox']} | Test address, Gujarat" in lead["texts"]["t1"]
               for lead in batch["leads"])


def test_the_model_never_receives_an_email_address(api):
    written(api, api.ids["eligible"][:2])
    assert len(api.messages.calls) == 6       # three touches per lead, each passing first time
    for call in api.messages.calls:
        sent = json.dumps(call["messages"], ensure_ascii=False)
        assert "@" not in sent and "kesar0.example" not in sent


def test_the_11th_new_contact_on_a_10_a_day_day_is_refused_with_a_message(api):
    eleven = api.ids["eligible"][:11]
    refused = api.create(eleven)
    assert refused.status_code == 409
    detail = refused.json()["detail"]
    assert detail["code"] == "CAP_REACHED"
    assert detail["message"].startswith("Only 10 new first contacts are left for ")
    assert "you selected 11" in detail["message"] and "allows 10 a day" in detail["message"]
    assert [r["eligibility_id"] for r in detail["refused"]] == [eleven[10]]
    assert api.client.get(BATCHES).json()["items"] == []          # all or nothing: no batch was made
    assert api.messages.calls == []                                  # and nothing was written

    assert api.create(eleven[:10]).status_code == 202
    allowance = api.client.get(f"{BATCHES}/allowance", params={"date": next_tuesday().isoformat()}).json()
    assert allowance["left"] == 0 and allowance["reserved_by_batches"] == 10 and allowance["daily_limit"] == 10
    again = api.create([eleven[10]])
    assert again.status_code == 409 and again.json()["detail"]["code"] == "CAP_REACHED"
    assert again.json()["detail"]["message"].startswith("Only 0 new first contacts are left")


def test_ids_that_are_not_eligible_are_refused(api):
    response = api.create([api.ids["eligible"][0], api.ids["held"], 99999])
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["code"] == "NOT_ELIGIBLE"
    codes = {r["eligibility_id"]: (r["code"], r["message"]) for r in detail["refused"]}
    assert codes[api.ids["held"]] == ("NOT_ELIGIBLE", "not eligible: NOT_VERIFIED, NEEDS_FOUNDER_CHECK")
    assert codes[99999][0] == "NOT_FOUND" and api.ids["eligible"][0] not in codes
    assert api.client.get(BATCHES).json()["items"] == []


def test_a_lead_already_in_an_open_batch_or_a_sequence_is_refused(api):
    first = written(api, api.ids["eligible"][:1])
    again = api.create(api.ids["eligible"][:1])
    assert again.status_code == 409 and again.json()["detail"]["refused"][0]["code"] == "IN_BATCH"
    approve = api.client.post(f"{BATCHES}/{first['id']}/approve", json={"lead_ids": "all_ready", "approved_by": "Founder"})
    assert approve.status_code == 200, approve.text
    third = api.create(api.ids["eligible"][:1])
    assert third.json()["detail"]["refused"][0]["code"] == "IN_SEQUENCE"
    everything = api.client.get(f"{BATCHES}/candidates", params={"status": "all"}).json()
    busy = {c["id"]: c["busy"] for c in everything["items"]}
    assert busy[api.ids["eligible"][0]]["code"] == "IN_SEQUENCE" and busy[api.ids["eligible"][1]] is None
    assert everything["counts"]["selectable"] == 10 and everything["counts"]["busy"] == 1
    selectable = api.client.get(f"{BATCHES}/candidates", params={"status": "eligible"}).json()
    assert api.ids["eligible"][0] not in {c["id"] for c in selectable["items"]} and len(selectable["items"]) == 10


def test_approve_all_ready_creates_e2_sequences_with_three_approved_texts(api):
    batch = written(api, api.ids["eligible"][:2])
    response = api.client.post(f"{BATCHES}/{batch['id']}/approve", json={"lead_ids": "all_ready", "approved_by": "Founder"})
    assert response.status_code == 200, response.text
    result = response.json()
    assert len(result["approved"]) == 2 and result["refused"] == [] and result["batch"]["status"] == "DONE"
    lead = result["batch"]["leads"][0]
    assert lead["state"] == "APPROVED" and lead["approved_by"] == "Founder" and lead["approved_at"]
    assert lead["schedule_kind"] == "scheduled"
    assert [(s["step"], s["state"], s["approved_by"]) for s in lead["schedule"]["steps"]] == [
        (1, "SCHEDULED", "Founder"), (2, "SCHEDULED", "Founder"), (3, "SCHEDULED", "Founder")]
    assert lead["schedule"]["mailbox_id"] == batch["leads"][0]["schedule"]["mailbox_id"]   # the planned sender
    with sync_session() as db:
        sequence = db.get(EmailSequence, lead["sequence_id"])
        records = db.execute(select(SendRecord).where(SendRecord.sequence_id == sequence.id)
                             .order_by(SendRecord.step)).scalars().all()
        assert [r.body for r in records] == [lead["texts"]["t1"], lead["texts"]["t2"], lead["texts"]["t3"]]
        assert [r.subject for r in records] == [lead["subject"], f"Re: {lead['subject']}", f"Re: {lead['subject']}"]
        assert all(r.approved_by == "Founder" and r.approved_at is not None for r in records)
        assert [r.content_version for r in records] == ["pilot-v1:T1", "pilot-v1:T2", "pilot-v1:T3"]
        assert sequence.mailbox_id == batch["leads"][0]["schedule"]["mailbox_id"]
    allowance = api.client.get(f"{BATCHES}/allowance", params={"date": next_tuesday().isoformat()}).json()
    assert allowance["scheduled_new"] == 2 and allowance["reserved_by_batches"] == 0 and allowance["left"] == 8


def test_approve_selected_then_reject_with_a_reason(api):
    batch = written(api, api.ids["eligible"][:3])
    first, second, third = (lead["id"] for lead in batch["leads"])
    approved = api.client.post(f"{BATCHES}/{batch['id']}/approve", json={"lead_ids": [first], "approved_by": "Founder"})
    assert [a["lead_id"] for a in approved.json()["approved"]] == [first]
    rejected = api.client.post(f"{BATCHES}/{batch['id']}/reject",
                               json={"lead_ids": [second], "reason": "Salon looks closed on the map", "rejected_by": "Founder"})
    assert rejected.status_code == 200, rejected.text
    states = {lead["id"]: lead for lead in rejected.json()["batch"]["leads"]}
    assert states[first]["state"] == "APPROVED" and states[third]["state"] == "READY"
    assert states[second]["state"] == "REJECTED" and states[second]["reject_reason"] == "Salon looks closed on the map"
    assert states[second]["rejected_by"] == "Founder" and states[second]["rejected_at"]
    # an approved lead cannot be rejected here (stopping a sequence is E2 / E4's job)
    late = api.client.post(f"{BATCHES}/{batch['id']}/reject",
                           json={"lead_ids": [first], "reason": "changed my mind", "rejected_by": "Founder"})
    assert late.status_code == 409 and late.json()["detail"]["code"] == "NOT_REJECTABLE"
    # approving a rejected lead does nothing
    again = api.client.post(f"{BATCHES}/{batch['id']}/approve", json={"lead_ids": [second], "approved_by": "Founder"})
    assert again.json()["approved"] == [] and again.json()["skipped"][0]["state"] == "REJECTED"
    # a rejected lead frees its place in the allowance
    allowance = api.client.get(f"{BATCHES}/allowance", params={"date": next_tuesday().isoformat()}).json()
    assert allowance["scheduled_new"] == 1 and allowance["reserved_by_batches"] == 1 and allowance["left"] == 8


def test_a_text_that_fails_the_validator_twice_is_hold_and_never_approved(api_factory):
    api = api_factory(bad={"Kesar Salon 1"})
    batch = written(api, api.ids["eligible"][:2])
    held = next(lead for lead in batch["leads"] if lead["business_name"] == "Kesar Salon 1")
    assert held["state"] == "HOLD" and held["hold_reasons"] == ["VALIDATION_FAILED"]
    assert any("banned phrase" in d for d in held["hold_detail"]) and held["texts"]["t1"] is None
    result = api.client.post(f"{BATCHES}/{batch['id']}/approve", json={"lead_ids": "all_ready", "approved_by": "Founder"}).json()
    assert len(result["approved"]) == 1
    with sync_session() as db:
        assert db.execute(select(EmailSequence).where(EmailSequence.business_id == held["business_id"])).first() is None


def test_missing_company_fact_holds_every_lead_without_calling_the_model(api_factory):
    api = api_factory(env={"SITEBLITZ_POSTAL_ADDRESS": ""})
    batch = written(api, api.ids["eligible"][:2])
    assert {lead["state"] for lead in batch["leads"]} == {"HOLD"}
    assert batch["leads"][0]["hold_reasons"] == ["MISSING_COMPANY_FACT"]
    assert "SITEBLITZ_POSTAL_ADDRESS" in batch["leads"][0]["hold_detail"][0]
    assert api.messages.calls == []


def test_missing_api_key_holds_writer_unavailable_and_fakes_no_text(api_factory):
    api = api_factory(stub=False)          # the real client path; ANTHROPIC_API_KEY is "" in the test env
    batch = written(api, api.ids["eligible"][:2])
    assert [lead["hold_reasons"] for lead in batch["leads"]] == [["WRITER_UNAVAILABLE"]] * 2
    assert all(lead["texts"] == {"t1": None, "t2": None, "t3": None} for lead in batch["leads"])


def test_ramp_stage_0_and_a_pause_give_no_allowance(api_factory):
    api = api_factory(ramp_stage=0)
    allowance = api.client.get(f"{BATCHES}/allowance", params={"date": next_tuesday().isoformat()}).json()
    assert allowance["left"] == 0 and allowance["limited_by"] == "ramp_stage_0"
    refused = api.create(api.ids["eligible"][:1])
    assert refused.status_code == 409 and "stage 0" in refused.json()["detail"]["message"]


def test_a_new_contacts_pause_blocks_the_batch_with_its_reason(api):
    with sync_session() as db:
        db.add(PauseFlag(scope=PauseScope.NEW_CONTACTS, scope_value="", reason_code="REPLY_BACKLOG",
                         created_at=datetime.now(timezone.utc)))
        db.commit()
    allowance = api.client.get(f"{BATCHES}/allowance", params={"date": next_tuesday().isoformat()}).json()
    assert allowance["left"] == 0 and allowance["limited_by"] == "paused"
    assert allowance["pauses"][0]["reason_code"] == "REPLY_BACKLOG" and allowance["pauses"][0]["blocks_new_contacts"]
    refused = api.create(api.ids["eligible"][:1])
    assert "REPLY_BACKLOG" in refused.json()["detail"]["message"]


def test_a_pause_raised_after_writing_refuses_approval_and_keeps_the_lead_ready(api):
    batch = written(api, api.ids["eligible"][:1])
    with sync_session() as db:
        db.add(PauseFlag(scope=PauseScope.GLOBAL, scope_value="", reason_code="COMPLAINT",
                         created_at=datetime.now(timezone.utc)))
        db.commit()
    result = api.client.post(f"{BATCHES}/{batch['id']}/approve", json={"lead_ids": "all_ready", "approved_by": "Founder"}).json()
    assert result["approved"] == [] and result["refused"][0]["code"] == "PAUSED"
    lead = result["batch"]["leads"][0]
    assert lead["state"] == "READY" and lead["approval_refusal"]["code"] == "PAUSED"
    with sync_session() as db:
        assert db.execute(select(SendRecord)).first() is None


def test_unknown_batch_and_bad_input(api):
    assert api.client.get(f"{BATCHES}/999").status_code == 404
    assert api.client.post(BATCHES, json={"eligibility_ids": [], "created_by": "Founder"}).status_code == 422
    assert api.client.post(BATCHES, json={"eligibility_ids": [1], "created_by": ""}).status_code == 422
    batch = written(api, api.ids["eligible"][:1])
    bad = api.client.post(f"{BATCHES}/{batch['id']}/approve", json={"lead_ids": "everything", "approved_by": "F"})
    assert bad.status_code == 422
    short = api.client.post(f"{BATCHES}/{batch['id']}/reject", json={"lead_ids": [batch["leads"][0]["id"]],
                                                                     "reason": "x", "rejected_by": "F"})
    assert short.status_code == 422
    nothing = api.client.post(f"{BATCHES}/{batch['id']}/write")
    assert nothing.status_code == 409 and nothing.json()["detail"]["code"] == "NOTHING_TO_WRITE"


def test_default_sending_day_is_a_campaign_day(api):
    allowance = api.client.get(f"{BATCHES}/allowance").json()
    assert allowance["campaign_day"] is True and allowance["left"] >= 0
    assert [m["display_name"] for m in allowance["mailboxes"]] == ["Asha Test", "Ravi Test"]
