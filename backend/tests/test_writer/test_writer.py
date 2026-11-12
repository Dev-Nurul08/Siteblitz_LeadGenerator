"""Phase 13 acceptance: request privacy, hold-before-call, one rewrite, observations from checks (no network)."""

import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from backend.app.config import Settings
from backend.app.engines.intelligence.rules import Check
from backend.app.engines.writer.writer import (
    FALLBACK_BETA,
    MODEL,
    OutreachWriter,
    assemble_message,
    build_lead,
    build_observations,
    model_payload,
    vertical_for,
)
from backend.app.models.intelligence import CheckType as T, EvidenceConfidence as C, WebsiteVerdict as V
from backend.tests.test_writer.test_validator import SETTINGS, answer, lead, task

NOW = datetime(2026, 11, 10, 12, 0, tzinfo=timezone.utc)


class FakeMessages:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        reply = self.replies.pop(0)
        if isinstance(reply, SimpleNamespace):
            return reply
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text=json.dumps(reply))])


def fake_client(*replies):
    messages = FakeMessages(replies)
    return SimpleNamespace(beta=SimpleNamespace(messages=messages)), messages


def writer_with(*replies, settings=SETTINGS):
    client, messages = fake_client(*replies)
    return OutreachWriter(client=client, settings=settings), messages


def test_request_carries_no_email_or_phone():
    the_lead = lead(
        thread=[{"direction": "in", "channel": "email", "sent_at": "2026-11-10",
                 "text": "Call me on +91 98250 12345 or write to owner.glow@gmail.com"}],
    )
    the_lead["emails"] = ["owner.glow@gmail.com"]
    the_lead["phone"] = "+91 98250 12345"
    writer, messages = writer_with(answer())
    result = writer.write(the_lead, task())
    assert result.status == "READY", result.errors
    sent = json.dumps(messages.calls[0]["messages"], ensure_ascii=False)
    assert "@gmail.com" not in sent and "98250" not in sent and "12345" not in sent


def test_owner_reply_in_task_reaches_the_model_without_email_or_phone():
    # QA-2026-11-10 (QA-016): only LEAD was redacted; TASK.inbound_message went to the model as typed.
    writer, messages = writer_with(answer(), answer())
    writer.write(lead(), task(channel="email", touch=2,
                              inbound_message="Price batao. Mera number 98250 12345 hai, mail owner.glow@gmail.com"))
    assert messages.calls, "the model should have been called for a reply"
    sent = messages.calls[0]["messages"][0]["content"]  # the first user turn: LEAD + TASK as JSON
    assert "Price batao" in sent
    assert "@gmail.com" not in sent and "98250" not in sent and "12345" not in sent
    assert "t-1" not in sent  # the lead id stays in the app
    assert "(email removed)" in sent and "(phone removed)" in sent


def test_payload_is_allow_listed():
    payload = model_payload({**lead(), "emails": ["a@b.com"], "postcode": "396445", "lat": 20.9})
    assert set(payload) <= {"business_name", "vertical", "category", "city", "area", "region", "country",
                            "contact_name", "contact_name_source", "language_evidence", "observations", "optin",
                            "suppressed", "thread"}


def test_request_shape_model_fallback_cache_schema():
    writer, messages = writer_with(answer())
    writer.write(lead(), task())
    call = messages.calls[0]
    assert call["model"] == MODEL == "claude-sonnet-5-5"
    assert call["fallbacks"] == "default" and call["betas"] == [FALLBACK_BETA]
    assert call["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert call["output_config"]["format"]["type"] == "json_schema"
    assert "COMPANY_FACTS" in call["system"][0]["text"] and "Test Road" not in call["system"][0]["text"]


def test_hold_is_decided_before_any_model_call():
    writer, messages = writer_with()
    assert writer.write(lead(country="DE"), task()).hold_reason == "COUNTRY_ON_HOLD"
    assert writer.write(lead(observations=[]), task()).hold_reason == "NO_OBSERVATION"
    assert writer.write(lead(suppressed=True), task()).hold_reason == "SUPPRESSED"
    assert writer.write(lead(), task(channel="whatsapp_reply", touch=None)).hold_reason == "NO_OPTIN"
    blank, blank_calls = writer_with(settings=Settings(_env_file=None, SITEBLITZ_SENDER_NAME=None,
                                                            SITEBLITZ_REPLY_EMAIL=None,
                                                            SITEBLITZ_POSTAL_ADDRESS=None))
    assert blank.write(lead(), task()).hold_reason == "MISSING_COMPANY_FACT"
    assert messages.calls == [] and blank_calls.calls == []


def test_one_rewrite_then_ready():
    bad = answer(body=answer()["body"].replace("I found", "I came across"))
    writer, messages = writer_with(bad, answer())
    result = writer.write(lead(), task())
    assert result.status == "READY" and result.attempts == 2
    retry = messages.calls[1]["messages"]
    assert [m["role"] for m in retry] == ["user", "assistant", "user"]
    assert "banned phrase" in retry[2]["content"]


def test_two_failures_hold_for_founder():
    bad = answer(body="Hello Glow Studio team, want a website?")
    writer, _ = writer_with(bad, bad)
    result = writer.write(lead(), task())
    assert result.status == "HOLD" and result.hold_reason == "VALIDATION_FAILED" and result.errors


def test_refusal_is_held_not_sent():
    writer, _ = writer_with(SimpleNamespace(stop_reason="refusal", content=[]))
    assert writer.write(lead(), task()).hold_reason == "MODEL_REFUSED"


def test_missing_api_key_holds_writer_unavailable_not_a_crash():
    # E3 brief: a missing key is HOLD WRITER_UNAVAILABLE, never a fallback text.
    writer = OutreachWriter(settings=SETTINGS)
    result = writer.write(lead(), task())
    assert result.status == "HOLD" and result.hold_reason == "WRITER_UNAVAILABLE"
    assert result.text is None and "ANTHROPIC_API_KEY" in result.errors[0]


def test_assembled_email_has_signature_and_opt_out():
    writer, _ = writer_with()
    text = assemble_message(answer(), writer.facts, "email")
    assert text.endswith("If this isn't useful, reply \"stop\" and I won't write again.")
    assert "Regards,\nAsha\nSiteBlitz | hello@siteblitz.example\nTest Road, Navsari, Gujarat" in text


def site_fetch(outcome, hours_ago, **detail):
    return Check(None, T.SITE_FETCH, outcome, target="https://www.glow.example/",
                 detail=detail, observed_at=NOW - timedelta(hours=hours_ago))


def test_observations_from_checks():
    down = build_observations(V.SITE_DOWN_CONFIRMED, C.HIGH, [site_fetch("failed", 10), site_fetch("failed", 1)],
                              [], now=NOW)
    assert [(o["type"], o["evidence_value"]) for o in down] == [("SITE_DOWN", "glow.example")]

    weak = build_observations(V.OWN_SITE_VERIFIED, C.HIGH,
                              [site_fetch("ok", 2, has_viewport=False, has_ssl=False)], [], now=NOW)
    assert [o["type"] for o in weak] == ["NO_VIEWPORT", "NO_HTTPS"]

    guess = Check(3, T.DOMAIN_GUESS, "none", "glow.com", observed_at=NOW - timedelta(days=2))
    zomato = Check(4, T.SOURCE_TAG, "found", "https://www.zomato.com/surat/glow", observed_at=NOW)
    social = build_observations(V.SOCIAL_ONLY_VERIFIED, C.MEDIUM, [guess, zomato], ["instagram"], now=NOW)
    assert [(o["type"], o["evidence_value"]) for o in social] == [("SOCIAL_ONLY", "Instagram"),
                                                                  ("AGGREGATOR_ONLY", "Zomato")]


def test_stale_or_low_confidence_checks_give_no_observation():
    old = Check(3, T.DOMAIN_GUESS, "none", "glow.com", observed_at=NOW - timedelta(days=31))
    assert build_observations(V.NO_SITE_VERIFIED, C.HIGH, [old], [], now=NOW) == []
    fresh = Check(3, T.DOMAIN_GUESS, "none", "glow.com", observed_at=NOW)
    assert build_observations(V.NO_SITE_VERIFIED, C.LOW, [fresh], [], now=NOW) == []


def test_build_lead_and_vertical():
    built = build_lead(lead_id="b-9", business_name="Bright Minds Classes", category="tutoring_service",
                       city="Navsari", country="in", observations=[])
    assert built["vertical"] == "coaching_tuition" and built["country"] == "IN"
    assert vertical_for("beauty_salon") == "salon_beauty"
    assert vertical_for("furniture_store") == "retail_showroom"
    assert vertical_for("plumber") == "other"
