"""
Email engine v2 E1 - importing an email-finder folder (old board row 14b): businesses, website checks, contacts
with provenance; idempotent; chain hosts held. The folder is written here with made-up test data.
"""

import csv
import json

from sqlalchemy import func, select

from backend.app.models.business import Business
from backend.app.models.contact import Contact
from backend.app.models.eligibility import CaptureMethod, EmailCapture, HoldReason
from backend.app.models.intelligence import CheckType, WebsiteCheck
from backend.app.services.email_finder_import import EmailFinderImporter

from .conftest import NOW, service

SITE_FIELDS = ["id", "name", "town", "vertical", "basic_category", "website", "skip_reason", "outcome", "note",
               "http_status", "final_url", "has_https", "has_viewport", "robots", "requests", "emails_found"]
EMAIL_FIELDS = ["id", "name", "town", "vertical", "email", "source_url", "source_method", "free_mail",
                "domain_matches_site"]


def write_folder(folder, leads, emails, visits, extras=None):
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / "sites.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=SITE_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(leads)
    with open(folder / "emails.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=EMAIL_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(emails)
    with open(folder / "visits.jsonl", "w", encoding="utf-8") as f:
        for visit in visits:
            f.write(json.dumps(visit) + "\n")
    if extras:
        with open(folder / "leads.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(extras[0]))
            writer.writeheader()
            writer.writerows(extras)


def lead(lead_id, name, website, outcome="ok", **kw):
    return {"id": lead_id, "name": name, "town": "Surat", "vertical": "salon_beauty",
            "basic_category": "beauty_salon", "website": website, "outcome": outcome, **kw}


def visit(url, outcome="ok", contacts=(), has_viewport=False, visited_at="2026-11-12T10:30:00+0530"):
    return {"listed_url": url, "outcome": outcome, "note": None, "http_status": 200 if outcome == "ok" else None,
            "final_url": url, "has_https": True, "has_viewport": has_viewport, "robots": "none", "requests": 2,
            "pages": [], "contacts": list(contacts), "visited_at": visited_at}


def contact(email, url, excerpt=None, method="mailto"):
    return {"email": email, "source_method": method, "source_url": url, "excerpt": excerpt}


def email_row(lead_id, email, url, method="mailto"):
    return {"id": lead_id, "email": email, "source_url": url, "source_method": method}


async def counts(session):
    async def n(model, *where):
        return (await session.execute(select(func.count(model.id)).where(*where))).scalar()
    return {"businesses": await n(Business), "contacts": await n(Contact), "captures": await n(EmailCapture),
            "checks": await n(WebsiteCheck, WebsiteCheck.check_type == CheckType.SITE_FETCH)}


async def test_import_is_idempotent_and_keeps_provenance(session, tmp_path):
    folder = tmp_path / "email_finder" / "2026-11-12"
    page = "https://glowhair.in/contact"
    write_folder(
        folder,
        [lead("ov-1", "Glow Hair Studio", "https://glowhair.in"),
         lead("ov-2", "Tutor Point", "https://tutorpoint.in", outcome="failed"),
         lead("ov-3", "Skipped College", "https://college.in", outcome="skipped"),
         lead("ov-4", "No Address", "", outcome="no_address")],
        [email_row("ov-1", "info@glowhair.in", page)],
        [visit("https://glowhair.in", contacts=[contact("info@glowhair.in", page, "Bookings: info@glowhair.in")]),
         visit("https://tutorpoint.in", outcome="failed")],
        extras=[{"id": "ov-1", "emails": "listed@glowhair.in", "phones": "+919800000001", "brand": "",
                 "instagram": "https://instagram.com/glowhair", "state": "Gujarat", "lat": "21.17", "lon": "72.83"}])

    first = await EmailFinderImporter(session).import_folder(folder)
    assert first["origin"] == "email_finder:2026-11-12"
    assert (first["businesses_created"], first["leads_imported"], first["leads_not_imported"]) == (2, 2, 2)
    assert (first["captures_added"], first["captures_with_excerpt"], first["listing_captures_added"]) == (1, 1, 1)
    after_first = await counts(session)
    assert after_first == {"businesses": 2, "contacts": 2, "captures": 2, "checks": 2}

    second = await EmailFinderImporter(session).import_folder(folder)
    assert await counts(session) == after_first                 # re-running adds nothing
    assert second["businesses_matched_by_source_id"] == 2
    assert "captures_added" not in second and "website_checks_added" not in second

    capture = (await session.execute(select(EmailCapture).where(
        EmailCapture.method == CaptureMethod.MAILTO))).scalar_one()
    assert (capture.source_url, capture.excerpt) == (page, "Bookings: info@glowhair.in")
    assert capture.captured_at.isoformat().startswith("2026-11-12T")
    check = (await session.execute(select(WebsiteCheck).where(WebsiteCheck.target == "https://glowhair.in")
                                   )).scalar_one()
    assert check.outcome == "ok" and check.detail["has_viewport"] is False
    business = (await session.execute(select(Business).where(Business.name == "Glow Hair Studio"))).scalar_one()
    assert business.country_code == "IN" and business.social_urls == {"instagram": "https://instagram.com/glowhair"}


async def test_phase14_style_rows_without_excerpt_are_held_as_incomplete(session, tmp_path):
    folder = tmp_path / "email_finder" / "2026-11-10"
    page = "https://glowhair.in/"
    write_folder(folder, [lead("ov-1", "Glow Hair Studio", "https://glowhair.in")],
                 [email_row("ov-1", "info@glowhair.in", page)],
                 [visit("https://glowhair.in", contacts=[contact("info@glowhair.in", page)])])
    stats = await EmailFinderImporter(session).import_folder(folder)
    assert stats["captures_without_excerpt"] == 1
    await service(session).evaluate(now=NOW)
    row = (await service(session).list_eligibility(None, 10))["items"][0]
    assert HoldReason.PROVENANCE_INCOMPLETE.value in row["hold_reasons"]
    assert row["tier"] == "HOLD"


async def test_host_shared_by_three_businesses_is_a_chain(session, tmp_path):
    folder = tmp_path / "pool" / "2026-11-12"
    leads, emails, visits = [], [], []
    for n in (1, 2, 3):
        url = f"https://stores.bigchain.in/surat-{n}"
        leads.append(lead(f"ov-{n}", f"Big Chain Store {n}", url))
        emails.append(email_row(f"ov-{n}", f"store{n}@bigchain.in", url))
        visits.append(visit(url, contacts=[contact(f"store{n}@bigchain.in", url, f"Mail store{n}@bigchain.in")]))
    write_folder(folder, leads, emails, visits)
    await EmailFinderImporter(session).import_folder(folder)
    summary = await service(session).evaluate(now=NOW)
    assert summary["by_hold_reason"][HoldReason.CHAIN_OR_DIRECTORY.value] == 3
