"""
Email engine v2, phase E1 - import an email-finder output folder into the app database (replaces board row 14b).

A folder written by `scripts/email_finder.py` (phase 14) or `scripts/pool_e1.py` holds:
  sites.csv     one row per lead: id (Overture id), name, town, vertical, basic_category, website, outcome, ...
  emails.csv    one row per lead + address: email, source_url, source_method
  visits.jsonl  the raw visits: listed_url, outcome, final_url, has_https, has_viewport, visited_at, contacts
                (contacts carry the page excerpt from E1 on; phase-14 visits have none)
  leads.csv     optional (pool runs): state, address, postcode, lat, lon, phones, emails (Overture listing),
                brand and social links of each lead
Each lead becomes (or is matched to) a business: first by its Overture source id, then by the app's normal
duplicate rules (DiscoveryService). Its visit becomes a SITE_FETCH website check with the visit time; each address a
Contact row plus an EmailCapture with source URL, method, capture time and excerpt; an Overture listing address an
EmailCapture of method `listing` (Tier 2). Re-running the same folder adds nothing: checks carry an `import_key`,
captures a unique `capture_key`, contacts are unique per (business, address).
Skipped leads (website-intelligence rule 9) and leads without a website address are not imported.
"""

import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.engines.discovery.base import DiscoveredBusiness
from backend.app.engines.discovery.overture import OvertureAdapter, social_platform
from backend.app.models.business import Business, BusinessSourceLink
from backend.app.models.contact import Contact, EmailVerificationStatus, RoleLevel
from backend.app.models.eligibility import EXCERPT_MAX_CHARS, CaptureMethod, EmailCapture
from backend.app.models.intelligence import CheckType, WebsiteCheck
from backend.app.models.source import JobStatus, Source, SourceJob, SourceRecord
from backend.app.services.discovery_service import DiscoveryService
from backend.app.services.eligibility_service import capture_key

logger = structlog.get_logger(__name__)

METHODS = {"mailto": CaptureMethod.MAILTO, "visible_text": CaptureMethod.VISIBLE_TEXT,
           "visible_text_obfuscated": CaptureMethod.VISIBLE_TEXT,
           "cloudflare_decode": CaptureMethod.CLOUDFLARE_DECODE}
NOT_IMPORTED = {"skipped", "no_address"}
SOCIAL_COLUMNS = ("facebook", "instagram", "linkedin", "tiktok", "youtube", "twitter", "whatsapp", "linktree")
LIST_SPLIT = re.compile(r"[;|,\s]+")


def normal_url(url: str) -> str:
    url = (url or "").strip()
    return url if url.startswith(("http://", "https://")) else f"https://{url}"


def parse_time(text: Optional[str]) -> Optional[datetime]:
    """visits.jsonl writes time.strftime('%Y-%m-%dT%H:%M:%S%z'), e.g. 2026-11-10T19:35:12+0530."""
    if not text:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    try:
        moment = datetime.fromisoformat(text)
        return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_visits(path: Path) -> dict[str, dict]:
    visits = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                visits[record["listed_url"]] = record
    return visits


def split_list(text: Optional[str]) -> list[str]:
    return [part for part in LIST_SPLIT.split(text or "") if part]


def _float(text: Optional[str]) -> Optional[float]:
    try:
        return float(text) if text not in (None, "") else None
    except ValueError:
        return None


class EmailFinderImporter:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.discovery = DiscoveryService(session)

    async def _overture_source(self) -> Source:
        source = (await self.session.execute(select(Source).where(Source.slug == "overture"))).scalar_one_or_none()
        if source:
            return source
        meta = OvertureAdapter().get_source_metadata()
        source = Source(**{k: meta[k] for k in (
            "name", "slug", "description", "license_type", "license_url", "license_notes", "attribution_required",
            "attribution_text", "allows_commercial_storage", "allows_contact_enrichment", "allows_marketing_use",
            "api_base_url", "adapter_class")})
        self.session.add(source)
        await self.session.flush()
        return source

    async def _job(self, source: Source, origin: str, count: int) -> SourceJob:
        """One source job per imported folder, so the app's "found by job" lists show these businesses."""
        for job in (await self.session.execute(select(SourceJob).where(SourceJob.source_id == source.id))).scalars():
            if (job.query_params or {}).get("import_origin") == origin:
                return job
        job = SourceJob(source_id=source.id, query_params={"import_origin": origin}, country_code="IN",
                        status=JobStatus.COMPLETED, records_found=count,
                        started_at=datetime.now(timezone.utc), completed_at=datetime.now(timezone.utc))
        self.session.add(job)
        await self.session.flush()
        return job

    def _discovered(self, lead: dict, extra: dict, website: str) -> DiscoveredBusiness:
        socials = {}
        for column in SOCIAL_COLUMNS:
            url = (extra.get(column) or "").strip()
            platform = social_platform(url) if url else None
            if platform:
                socials.setdefault(platform, url)
        listing_emails = [e.lower() for e in split_list(extra.get("emails")) if "@" in e]
        phones = split_list(extra.get("phones"))
        raw = {"overture_id": lead["id"], "basic_category": lead.get("basic_category") or None,
               "websites": [website] if website else [], "socials": list(socials.values()), "phones": phones,
               "emails": listing_emails, "brand_name": (extra.get("brand") or None),
               "vertical": lead.get("vertical") or None, "import_origin": None}
        return DiscoveredBusiness(
            source_external_id=f"overture:{lead['id']}", source_external_url=None, raw_data=raw,
            name=(lead.get("name") or "").strip() or "(no name)", address_line_1=extra.get("address") or None,
            city=lead.get("town") or extra.get("city") or None, state_province=extra.get("state") or None,
            postal_code=extra.get("postcode") or None, country_code="IN", latitude=_float(extra.get("lat")),
            longitude=_float(extra.get("lon")),
            categories=[lead["basic_category"]] if lead.get("basic_category") else [],
            source_categories=[f"overture:{lead['basic_category']}"] if lead.get("basic_category") else [],
            website_url=website or None, phone=phones[0] if phones else None,
            email=listing_emails[0] if listing_emails else None, social_urls=socials)

    async def _business_for(self, source: Source, job: SourceJob, lead: dict, extra: dict, website: str,
                            origin: str, stats: dict) -> Optional[Business]:
        external_id = f"overture:{lead['id']}"
        record = (await self.session.execute(select(SourceRecord).where(
            SourceRecord.source_id == source.id, SourceRecord.external_id == external_id))).scalar_one_or_none()
        if record is not None:
            found = (await self.session.execute(
                select(Business).join(BusinessSourceLink, BusinessSourceLink.business_id == Business.id)
                .where(BusinessSourceLink.source_record_id == record.id).limit(1))).scalar_one_or_none()
            if found:
                stats["businesses_matched_by_source_id"] += 1
                return found
        discovered = self._discovered(lead, extra, website)
        discovered.raw_data["import_origin"] = origin
        async with self.session.begin_nested():
            if record is None:
                record = await self.discovery._save_source_record(source, job, discovered)
            existing = await self.discovery._find_existing_business(discovered)
            if existing:
                await self.discovery._link_business_to_source(existing, record, method="dedup_match")
                stats["businesses_matched_by_dedup"] += 1
                business = existing
            else:
                business = await self.discovery._create_business(discovered, record)
                stats["businesses_created"] += 1
            record.is_processed = True
            await self.session.flush()
        return business

    async def import_folder(self, folder: Path, origin: Optional[str] = None) -> dict:
        folder = Path(folder)
        origin = origin or f"{folder.parent.name}:{folder.name}"
        sites = read_csv(folder / "sites.csv")
        emails_by_lead: dict[str, list[dict]] = defaultdict(list)
        for row in read_csv(folder / "emails.csv"):
            emails_by_lead[row["id"]].append(row)
        extras = {row["id"]: row for row in read_csv(folder / "leads.csv")}
        visits = read_visits(folder / "visits.jsonl")
        stats: dict[str, int] = defaultdict(int)
        source = await self._overture_source()
        job = await self._job(source, origin, len(sites))

        for lead in sites:
            if lead.get("outcome") in NOT_IMPORTED or not (lead.get("website") or "").strip():
                stats["leads_not_imported"] += 1
                continue
            url = normal_url(lead["website"])
            visit = visits.get(url)
            if visit is None:
                stats["leads_without_visit"] += 1
                continue
            extra = extras.get(lead["id"], {})
            business = await self._business_for(source, job, lead, extra, url, origin, stats)
            stats["leads_imported"] += 1
            await self._import_check(business, visit, url, origin, stats)
            await self._import_emails(business, emails_by_lead.get(lead["id"], []), visit, origin, stats)
            await self._import_listing_emails(business, extra, stats)
        await self.session.flush()
        logger.info("email_finder_import", folder=str(folder), **stats)
        return {"origin": origin, **dict(sorted(stats.items()))}

    async def _import_check(self, business: Business, visit: dict, url: str, origin: str, stats: dict) -> None:
        key = f"{origin}|{url}"
        rows = (await self.session.execute(select(WebsiteCheck.detail).where(
            WebsiteCheck.business_id == business.id, WebsiteCheck.check_type == CheckType.SITE_FETCH))).scalars()
        if any((detail or {}).get("import_key") == key for detail in rows):
            return
        self.session.add(WebsiteCheck(
            business_id=business.id, check_type=CheckType.SITE_FETCH, target=url[:1000],
            outcome=visit.get("outcome") or "failed",
            detail={"http_status": visit.get("http_status"), "final_url": visit.get("final_url"),
                    "has_ssl": visit.get("has_https"), "has_viewport": visit.get("has_viewport"),
                    "note": visit.get("note"), "robots": visit.get("robots"), "requests": visit.get("requests"),
                    "import_key": key, "source": origin},
            observed_at=parse_time(visit.get("visited_at")) or datetime.now(timezone.utc)))
        stats["website_checks_added"] += 1

    async def _import_emails(self, business: Business, rows: list[dict], visit: dict, origin: str,
                             stats: dict) -> None:
        captured_at = parse_time(visit.get("visited_at"))
        by_key = {((c.get("email") or "").lower(), c.get("source_url") or ""): c for c in visit.get("contacts") or []}
        for row in rows:
            email = (row.get("email") or "").strip().lower()
            source_url = row.get("source_url") or None
            if not email:
                continue
            contact = by_key.get((email, source_url or ""), {})
            raw_method = row.get("source_method") or contact.get("source_method") or ""
            method = METHODS.get(raw_method)
            if method is None:
                stats["emails_unknown_method"] += 1
                continue
            excerpt = (contact.get("excerpt") or "")[:EXCERPT_MAX_CHARS] or None
            key = capture_key(business.id, email, origin, source_url)
            if (await self.session.execute(select(EmailCapture.id).where(EmailCapture.capture_key == key))
                    ).scalar_one_or_none() is None:
                self.session.add(EmailCapture(
                    business_id=business.id, email=email, method=method, raw_method=raw_method,
                    source_url=source_url, excerpt=excerpt, captured_at=captured_at, origin=origin,
                    capture_key=key))
                stats["captures_added"] += 1
                stats["captures_with_excerpt" if excerpt else "captures_without_excerpt"] += 1
            await self._contact(business, email, raw_method or "website_scrape", source_url, stats)

    async def _import_listing_emails(self, business: Business, extra: dict, stats: dict) -> None:
        for email in [e.lower() for e in split_list(extra.get("emails")) if "@" in e]:
            key = capture_key(business.id, email, "overture", None)
            if (await self.session.execute(select(EmailCapture.id).where(EmailCapture.capture_key == key))
                    ).scalar_one_or_none() is None:
                self.session.add(EmailCapture(
                    business_id=business.id, email=email, method=CaptureMethod.LISTING, raw_method="overture",
                    source_url=None, excerpt=None, captured_at=None, origin="overture", capture_key=key))
                stats["listing_captures_added"] += 1
            await self._contact(business, email, "business_profile", None, stats)

    async def _contact(self, business: Business, email: str, method: str, source_url: Optional[str],
                       stats: dict) -> None:
        exists = (await self.session.execute(select(Contact.id).where(
            Contact.business_id == business.id, Contact.email == email))).scalar_one_or_none()
        if exists is None:
            self.session.add(Contact(business_id=business.id, email=email, role_level=RoleLevel.GENERAL_INBOX,
                                     email_status=EmailVerificationStatus.UNVERIFIED, source_method=method[:100],
                                     source_url=source_url))
            await self.session.flush()
            stats["contacts_added"] += 1
