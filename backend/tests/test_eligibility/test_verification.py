"""
Email engine v2 E1 - verifier ladder: syntax + MX, Bouncer mapping, no key = UNVERIFIED, 30-day cache.
DNS and the Bouncer API are stubbed (httpx.MockTransport); nothing leaves this machine.
"""

from datetime import timedelta

import httpx
import pytest
from sqlalchemy import select

from backend.app.config import Settings
from backend.app.engines.eligibility.verification import (
    BOUNCER_ENDPOINT,
    BouncerVerifier,
    MxAnswer,
    SyntaxMxVerifier,
    VerificationLadder,
    map_bouncer,
)
from backend.app.models.eligibility import EmailVerification, HoldReason, VerificationStatus

from .conftest import NOW, no_viewport_lead, service


def lookup_returning(answer: MxAnswer):
    async def lookup(domain):
        return answer
    return lookup


# ─── 1. syntax + MX ──────────────────────────────────────────────────────────


async def test_mx_found_is_a_pass_but_not_valid():
    result = await SyntaxMxVerifier(lookup_returning(MxAnswer(mx_hosts=["mx.glowhair.in"]))).verify("info@glowhair.in")
    assert result.status == VerificationStatus.UNVERIFIED and result.detail["mx_ok"] is True


@pytest.mark.parametrize("answer,note", [
    (MxAnswer(null_mx=True), "null MX"),
    (MxAnswer(), "no MX and no A"),
    (MxAnswer(domain_exists=False), "NXDOMAIN"),
])
async def test_null_mx_missing_mx_or_missing_domain_is_invalid(answer, note):
    result = await SyntaxMxVerifier(lookup_returning(answer)).verify("info@glowhair.in")
    assert result.status == VerificationStatus.INVALID and note in result.detail["note"]


async def test_a_record_without_mx_is_an_implicit_mx():
    result = await SyntaxMxVerifier(lookup_returning(MxAnswer(has_address=True))).verify("info@glowhair.in")
    assert result.status == VerificationStatus.UNVERIFIED and result.detail["mx_ok"] is True


async def test_bad_syntax_is_invalid_and_dns_timeout_is_no_answer():
    called = []

    async def lookup(domain):
        called.append(domain)
        return MxAnswer(error="Timeout")

    verifier = SyntaxMxVerifier(lookup)
    assert (await verifier.verify("not an email")).status == VerificationStatus.INVALID
    assert called == []
    assert (await verifier.verify("info@glowhair.in")).status is None


# ─── 2. Bouncer ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize("status,accept_all,expected", [
    ("deliverable", "no", VerificationStatus.VALID),
    ("deliverable", "yes", VerificationStatus.CATCH_ALL),
    ("risky", "yes", VerificationStatus.CATCH_ALL),
    ("risky", "no", VerificationStatus.RISKY),
    ("risky", "unknown", VerificationStatus.RISKY),
    ("undeliverable", "no", VerificationStatus.INVALID),
    ("unknown", "unknown", VerificationStatus.UNKNOWN),
    ("something-new", "no", VerificationStatus.UNKNOWN),
])
def test_bouncer_mapping(status, accept_all, expected):
    assert map_bouncer({"status": status, "domain": {"acceptAll": accept_all}}) == expected


def bouncer(handler) -> BouncerVerifier:
    return BouncerVerifier("test-key", transport=httpx.MockTransport(handler))


async def test_bouncer_request_shape_and_result():
    seen = {}

    def handler(request: httpx.Request):
        seen["url"], seen["key"] = str(request.url), request.headers.get("x-api-key")
        return httpx.Response(200, json={"email": "info@glowhair.in", "status": "deliverable",
                                         "reason": "accepted_email", "domain": {"acceptAll": "no", "free": "no"},
                                         "account": {"role": "yes"}, "score": 100})

    result = await bouncer(handler).verify("info@glowhair.in")
    assert seen["url"].startswith(BOUNCER_ENDPOINT + "?") and "email=info%40glowhair.in" in seen["url"]
    assert seen["key"] == "test-key"
    assert result.status == VerificationStatus.VALID
    assert result.detail["reason"] == "accepted_email" and result.detail["role"] == "yes"


@pytest.mark.parametrize("code", [401, 402, 429, 500])
async def test_bouncer_http_errors_are_no_answer(code):
    result = await bouncer(lambda request: httpx.Response(code, json={"message": "0 credits left"})).verify("a@b.in")
    assert result.status is None and result.detail["error"] == f"HTTP {code}"


async def test_bouncer_network_error_is_no_answer():
    def handler(request):
        raise httpx.ConnectError("offline")
    assert (await bouncer(handler).verify("a@b.in")).status is None


def test_ladder_without_key_has_no_paid_verifier():
    assert VerificationLadder.from_settings(Settings(_env_file=None)).paid is None
    assert isinstance(VerificationLadder.from_settings(Settings(_env_file=None, BOUNCER_API_KEY="k")).paid,
                      BouncerVerifier)


# ─── 3. ladder + cache through the service ───────────────────────────────────


class CountingVerifier:
    provider = "bouncer"

    def __init__(self, status=VerificationStatus.VALID):
        self.calls, self.status = [], status

    async def verify(self, email):
        from backend.app.engines.eligibility.verification import VerifierResult
        self.calls.append(email)
        return VerifierResult("bouncer", self.status, {"status": "deliverable"})


async def test_without_a_key_the_address_stays_unverified(session):
    await no_viewport_lead(session)
    summary = await service(session).evaluate(verify=True, now=NOW)
    assert summary["eligible"] == 0 and summary["eligible_if_verified"] == 1
    assert summary["by_hold_reason"] == {HoldReason.NOT_VERIFIED.value: 1}
    assert summary["paid_verifier_configured"] is False
    rows = (await session.execute(select(EmailVerification))).scalars().all()
    assert [(r.provider, r.status) for r in rows] == [("syntax_mx", VerificationStatus.UNVERIFIED)]


async def test_with_a_verifier_the_lead_becomes_eligible_and_the_result_is_cached(session):
    await no_viewport_lead(session)
    paid = CountingVerifier()
    summary = await service(session, paid=paid).evaluate(verify=True, now=NOW)
    assert summary["eligible"] == 1 and paid.calls == ["info@glowhair.in"]

    # a second run inside 30 days uses the cache
    await service(session, paid=paid).evaluate(verify=True, now=NOW + timedelta(days=10))
    assert paid.calls == ["info@glowhair.in"]
    # after 30 days the address is verified again (the observation itself is stale by then, so the ladder is
    # called directly here; evaluate() would not spend a verifier call on a held lead)
    await service(session, paid=paid).verify_emails(["info@glowhair.in"], now=NOW + timedelta(days=31))
    assert len(paid.calls) == 2
    stale = await service(session, paid=paid).evaluate(verify=True, now=NOW + timedelta(days=31))
    assert stale["by_hold_reason"] == {HoldReason.OBSERVATION_STALE.value: 1}


async def test_paid_verifier_is_not_called_for_held_or_mx_invalid_addresses(session):
    await no_viewport_lead(session, render=None)            # PHONE_CHECK_PENDING: not a candidate
    paid = CountingVerifier()
    await service(session, paid=paid).evaluate(verify=True, now=NOW)
    assert paid.calls == []

    lead = await no_viewport_lead(session, email="info@deadmail.in", name="Second Salon",
                                  website="https://secondsalon.in")
    await service(session, paid=paid, lookup=lookup_returning(MxAnswer())).evaluate([lead.id], verify=True, now=NOW)
    assert paid.calls == []   # the free MX check already said INVALID


async def test_business_marked_invalid_later_loses_its_eligible_row(session):
    from backend.app.models.business import BusinessStatus
    lead = await no_viewport_lead(session)
    await service(session, paid=CountingVerifier()).evaluate(verify=True, now=NOW)
    assert (await service(session).business_rows(lead.id))[0]["eligible"] is True
    lead.status = BusinessStatus.INVALID
    await session.flush()
    await service(session).evaluate(now=NOW)
    row = (await service(session).business_rows(lead.id))[0]
    assert row["eligible"] is False and row["hold_reasons"] == ["NOT_A_PROSPECT"]
