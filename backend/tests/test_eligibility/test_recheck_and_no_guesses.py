"""
Email engine v2 E1:
- spec E1 criterion "a test proves a SITE_DOWN lead is rechecked before send" (recheck_before_send);
- regression: no code path can produce a guessed address (info@<domain>, inquiry.<name>@gmail.com, ...).
The homepage check and DNS are stubbed.
"""

import re
from datetime import timedelta
from pathlib import Path

from sqlalchemy import select

from backend.app.engines.eligibility.verification import MxAnswer
from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine
from backend.app.engines.enrichment.site_visit import SiteVisit
from backend.app.models.business import Business
from backend.app.models.eligibility import VerificationStatus
from backend.app.models.intelligence import CheckType, WebsiteCheck
from backend.app.services.enrichment_service import EnrichmentService

from .conftest import NOW, add_business, add_capture, add_check, service

REPO = Path(__file__).resolve().parents[3]


class Paid:
    provider = "bouncer"

    async def verify(self, email):
        from backend.app.engines.eligibility.verification import VerifierResult
        return VerifierResult("bouncer", VerificationStatus.VALID, {"status": "deliverable"})


def site_check_returning(outcome, calls):
    async def check(url):
        calls.append(url)
        return SiteVisit(listed_url=url, outcome=outcome, note=None if outcome == "ok" else "connect")
    return check


async def site_down_lead(session):
    """Homepage failed twice 8 h apart; its address was read on its own site before it went down."""
    business = await add_business(session, name="Shree Retail Showroom", website="https://shreeretail.in")
    await add_capture(session, business, "info@shreeretail.in", source_url="https://shreeretail.in/contact",
                      captured_at=NOW - timedelta(days=2))
    await add_check(session, business, "failed", NOW - timedelta(hours=9))
    await add_check(session, business, "failed", NOW - timedelta(hours=1))
    return business


async def test_site_down_lead_is_rechecked_right_before_send(session):
    business = await site_down_lead(session)
    calls = []
    svc = service(session, paid=Paid(), site_check=site_check_returning("failed", calls))
    await svc.evaluate(verify=True, now=NOW)
    assert (await svc.business_rows(business.id))[0]["eligible"] is True

    send_time = NOW + timedelta(minutes=30)
    result = await svc.recheck_before_send(business.id, now=send_time)
    assert calls == ["https://shreeretail.in"]                       # a fresh homepage check ran
    assert result["site_down_lead"] is True and result["site_check"]["outcome"] == "failed"
    assert result["send_allowed"] is True and result["send_to"] == "info@shreeretail.in"
    stored = (await session.execute(select(WebsiteCheck).where(
        WebsiteCheck.business_id == business.id, WebsiteCheck.check_type == CheckType.SITE_FETCH)
        .order_by(WebsiteCheck.id.desc()))).scalars().first()
    assert stored.detail["recheck_before_send"] is True and stored.outcome == "failed"


async def test_recovered_site_blocks_the_send(session):
    business = await site_down_lead(session)
    svc = service(session, paid=Paid(), site_check=site_check_returning("ok", []))
    await svc.evaluate(verify=True, now=NOW)
    result = await svc.recheck_before_send(business.id, now=NOW + timedelta(minutes=30))
    assert result["send_allowed"] is False and result["reason"] == "SITE_RECOVERED"
    assert "SITE_RECOVERED" in result["rows"][0]["hold_reasons"]


async def test_mailbox_on_the_down_domain_must_still_accept_mail(session):
    business = await site_down_lead(session)

    async def no_mx(domain):
        return MxAnswer(null_mx=True)

    svc = service(session, paid=Paid(), site_check=site_check_returning("failed", []))
    await svc.evaluate(verify=True, now=NOW)
    gone = service(session, paid=Paid(), lookup=no_mx, site_check=site_check_returning("failed", []))
    result = await gone.recheck_before_send(business.id, now=NOW + timedelta(minutes=30))
    assert result["send_allowed"] is False
    assert {"MAILBOX_DOMAIN_DOWN", "VERIFIER_INVALID"} <= set(result["rows"][0]["hold_reasons"])


# ─── no guessed addresses anywhere ───────────────────────────────────────────

GUESS_PATTERNS = [
    re.compile(r"""f["'](info|contact|hello|inquiry|enquiry|sales|admin|office)[.@]?\{"""),   # f"info@{domain}"
    re.compile(r"""["']@gmail\.com["']\s*$"""),
    re.compile(r"corporate_domain_default|local_business_registry"),
    re.compile(r"""f["']\+91 9825"""),                                                          # fake phones
    re.compile(r"""f["']\+1 \(555\)"""),
]


def test_no_source_file_builds_a_guessed_address():
    offenders = []
    for path in list((REPO / "backend" / "app").rglob("*.py")) + list((REPO / "scripts").rglob("*.py")) + \
            list(REPO.glob("*.py")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(p.search(line) for p in GUESS_PATTERNS):
                offenders.append(f"{path.relative_to(REPO)}:{number}: {line.strip()}")
    assert offenders == []
    assert not (REPO / "export_surat_leads.py").exists()


async def test_enrichment_of_a_site_without_addresses_creates_no_contact(session, monkeypatch):
    async def no_crawl(self, base_url):
        return []

    monkeypatch.setattr(ContactDiscoveryEngine, "_crawl_contact_pages", no_crawl)
    business = await add_business(session, name="Quiet Coaching Classes", website="https://quietcoaching.in")
    business.phone = None
    result = await EnrichmentService(session).enrich_business(business.id)
    assert result["contacts_count"] == 0 and result["contacts"] == []
    refreshed = (await session.execute(select(Business).where(Business.id == business.id))).scalar_one()
    assert refreshed.email is None and refreshed.phone is None
    assert not hasattr(ContactDiscoveryEngine, "discover_contacts")
    assert not hasattr(ContactDiscoveryEngine, "_query_hunter_api")
