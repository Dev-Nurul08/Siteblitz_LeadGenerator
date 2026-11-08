"""
Website Intelligence service — runs checks, stores them, and keeps one LeadAssessment per business.

assess()      network checks (source tags, socials, link-in-bio, site fetch, domain guesses) → recompute
recompute()   verdict + score from stored checks only (after a manual search / activity / label)
"""

from datetime import datetime, timezone
from typing import Optional

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.engines.intelligence import checks as net
from backend.app.engines.intelligence.rules import (
    Assessment,
    Check,
    Facts,
    assess,
    missing_for_hot,
    skip_reason,
)
from backend.app.engines.opportunity.resolver import WebsiteResolver
from backend.app.models.business import Business, BusinessSourceLink, WebsiteStatus
from backend.app.models.compliance import OptOut
from backend.app.models.intelligence import (
    CheckType,
    ContactLog,
    FounderLabel,
    LeadAssessment,
    SocialIdentity,
    WebsiteCheck,
    WebsiteVerdict,
)
from backend.app.models.opportunity import Opportunity, OpportunityStatus, ServiceCategory
from backend.app.models.source import SourceRecord

logger = structlog.get_logger(__name__)

# Keep the old Business.website_status in step so lists and exports show the verified state.
VERDICT_TO_WEBSITE_STATUS = {
    WebsiteVerdict.OWN_SITE_VERIFIED: WebsiteStatus.FOUND,
    WebsiteVerdict.SOCIAL_ONLY_VERIFIED: WebsiteStatus.SOCIAL_ONLY,
    WebsiteVerdict.NO_SITE_VERIFIED: WebsiteStatus.NOT_FOUND,
    WebsiteVerdict.SITE_DOWN_CONFIRMED: WebsiteStatus.BROKEN,
}


class IntelligenceService:
    def __init__(self, session: AsyncSession, resolver: Optional[WebsiteResolver] = None):
        self.session = session
        self.resolver = resolver or WebsiteResolver()

    # ─── loading ─────────────────────────────────────────────────────────

    async def _business(self, business_id: int) -> Optional[Business]:
        stmt = (select(Business).where(Business.id == business_id)
                .options(selectinload(Business.locations), selectinload(Business.categories)))
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def _raw_records(self, business_id: int) -> list[dict]:
        stmt = (select(SourceRecord.raw_data)
                .join(BusinessSourceLink, BusinessSourceLink.source_record_id == SourceRecord.id)
                .where(BusinessSourceLink.business_id == business_id))
        return [r for r in (await self.session.execute(stmt)).scalars().all() if isinstance(r, dict)]

    async def _stored_checks(self, business_id: int) -> list[Check]:
        rows = (await self.session.execute(
            select(WebsiteCheck).where(WebsiteCheck.business_id == business_id)
            .order_by(WebsiteCheck.observed_at, WebsiteCheck.id))).scalars().all()
        return [Check(r.id, r.check_type, r.outcome, r.target, r.detail or {}, r.observed_at)
                for r in rows]

    async def _suppressed(self, business: Business) -> bool:
        dnc = await self.session.execute(select(func.count(ContactLog.id)).where(
            ContactLog.business_id == business.id, ContactLog.outcome == "do_not_contact"))
        if (dnc.scalar() or 0) > 0:
            return True
        email = (business.email or "").lower()
        if not email:
            return False
        domain = email.split("@")[-1]
        hit = await self.session.execute(
            select(func.count(OptOut.id)).where((OptOut.email == email) | (OptOut.domain == domain)))
        return (hit.scalar() or 0) > 0

    def _facts(self, business: Business, raw: list[dict], include_franchises: bool,
               suppressed: bool) -> Facts:
        categories = [c.category_name for c in business.categories] + [
            str(r.get("basic_category") or "") for r in raw]
        return Facts(name=business.name, categories=[c for c in categories if c],
                     phone=business.phone, email=business.email,
                     social_platforms=list((business.social_urls or {}).keys()),
                     raw_records=raw, include_franchises=include_franchises, suppressed=suppressed)

    async def _store(self, business_id: int, new_checks: list[Check]) -> None:
        now = datetime.now(timezone.utc)
        for c in new_checks:
            self.session.add(WebsiteCheck(business_id=business_id, check_type=c.type,
                                          target=(c.target or None) and c.target[:1000],
                                          outcome=c.outcome, detail=c.detail, observed_at=now))
        await self.session.flush()

    # ─── public API ──────────────────────────────────────────────────────

    async def assess_business(self, business_id: int, include_franchises: bool = False) -> dict:
        business = await self._business(business_id)
        if not business:
            return {"error": f"Business {business_id} not found"}
        raw = await self._raw_records(business_id)
        suppressed = await self._suppressed(business)
        facts = self._facts(business, raw, include_franchises, suppressed)
        skip = skip_reason(facts)
        city = business.locations[0].city if business.locations else None

        new = net.source_checks(raw, business.website_url, business.social_urls or {}, skip)
        await self._sync_socials(business)
        if not skip:
            bio_checks, bio_links = await net.link_in_bio_checks(business.social_urls or {})
            new += bio_checks
            links = net.website_links(raw, business.website_url) + bio_links
            site_ok = False
            for url in list(dict.fromkeys(links))[:3]:
                fetch = await net.site_fetch_check(url, self.resolver)
                new.append(fetch)
                site_ok = site_ok or fetch.outcome in ("ok", "protected")
            if not site_ok:
                new += await net.domain_guess_checks(business.name, business.country_code, city,
                                                     business.phone, self.resolver)
        await self._store(business_id, new)
        return await self.recompute(business_id, include_franchises=include_franchises)

    async def _sync_socials(self, business: Business) -> None:
        existing = {(s.platform, s.url) for s in (await self.session.execute(
            select(SocialIdentity).where(SocialIdentity.business_id == business.id))).scalars()}
        for platform, url in (business.social_urls or {}).items():
            if (platform, url) not in existing:
                self.session.add(SocialIdentity(business_id=business.id, platform=platform, url=url,
                                                evidence_source="source_listing",
                                                match_status="discovered"))

    async def recompute(self, business_id: int, include_franchises: bool = False) -> dict:
        business = await self._business(business_id)
        if not business:
            return {"error": f"Business {business_id} not found"}
        raw = await self._raw_records(business_id)
        facts = self._facts(business, raw, include_franchises, await self._suppressed(business))
        stored = await self._stored_checks(business_id)
        result = assess(stored, facts)

        row = (await self.session.execute(select(LeadAssessment).where(
            LeadAssessment.business_id == business_id))).scalar_one_or_none()
        if row is None:
            row = LeadAssessment(business_id=business_id)
            self.session.add(row)
        row.website_verdict = result.verdict
        row.evidence_confidence = result.confidence
        row.need_score = result.need_score
        row.tier = result.tier
        row.outreach_readiness = result.readiness
        row.score_breakdown = result.breakdown
        row.reasons = result.reasons
        row.summary = result.summary
        row.assessed_at = datetime.now(timezone.utc)

        if result.verdict in VERDICT_TO_WEBSITE_STATUS:
            business.website_status = VERDICT_TO_WEBSITE_STATUS[result.verdict]
        if result.verdict == WebsiteVerdict.OWN_SITE_VERIFIED:
            # Spec row 17: a "new website" opportunity is wrong once a site is verified.
            for opp in (await self.session.execute(select(Opportunity).where(
                    Opportunity.business_id == business_id,
                    Opportunity.service_category == ServiceCategory.NEW_WEBSITE))).scalars():
                opp.status = OpportunityStatus.DISQUALIFIED
        await self.session.flush()
        return await self.detail(business_id)

    async def detail(self, business_id: int) -> dict:
        business = await self._business(business_id)
        if not business:
            return {"error": f"Business {business_id} not found"}
        row = (await self.session.execute(select(LeadAssessment).where(
            LeadAssessment.business_id == business_id))).scalar_one_or_none()
        stored = await self._stored_checks(business_id)
        socials = (await self.session.execute(select(SocialIdentity).where(
            SocialIdentity.business_id == business_id))).scalars().all()
        location = business.locations[0] if business.locations else None
        assessment = None
        if row:
            assessment = {
                "website_verdict": row.website_verdict.value,
                "evidence_confidence": row.evidence_confidence.value,
                "need_score": row.need_score,
                "tier": row.tier.value,
                "outreach_readiness": row.outreach_readiness.value,
                "score_breakdown": row.score_breakdown,
                "reasons": row.reasons or [],
                "summary": row.summary,
                "assessed_at": row.assessed_at.isoformat() if row.assessed_at else None,
                "next_actions": missing_for_hot(Assessment(
                    row.website_verdict, row.evidence_confidence, row.need_score, row.tier,
                    row.outreach_readiness, row.score_breakdown, row.reasons or [], row.summary or "")),
                "label": row.label.value if row.label else None,
                "label_wrong_part": row.label_wrong_part,
                "label_note": row.label_note,
                "labeled_at": row.labeled_at.isoformat() if row.labeled_at else None,
            }
        logs = (await self.session.execute(select(ContactLog).where(
            ContactLog.business_id == business_id).order_by(ContactLog.logged_at.desc(),
                                                            ContactLog.id.desc()))).scalars().all()
        return {
            "contact_log": [{"id": log.id, "channel": log.channel, "outcome": log.outcome,
                             "note": log.note, "logged_at": log.logged_at.isoformat()} for log in logs],
            "business": {
                "id": business.id, "name": business.name, "phone": business.phone,
                "email": business.email, "website_url": business.website_url,
                "country_code": business.country_code,
                "city": location.city if location else None,
                "address": location.address_line_1 if location else None,
                "lat": location.latitude if location else None,
                "lon": location.longitude if location else None,
                "category": business.categories[0].category_name if business.categories else None,
                "social_urls": business.social_urls or {},
            },
            "assessment": assessment,
            "checks": [{"id": c.id, "type": c.type.value, "outcome": c.outcome, "target": c.target,
                        "detail": c.detail, "observed_at": c.observed_at.isoformat()}
                       for c in stored],
            "socials": [{"platform": s.platform, "url": s.url, "match_status": s.match_status,
                         "evidence_source": s.evidence_source} for s in socials],
        }

    async def record_manual_search(self, business_id: int, found_url: Optional[str],
                                   note: Optional[str]) -> dict:
        outcome = "found" if found_url else "none"
        await self._store(business_id, [Check(None, CheckType.MANUAL_SEARCH, outcome,
                                              target=found_url, detail={"note": note} if note else {})])
        return await self.recompute(business_id)

    async def record_activity(self, business_id: int, active: bool, method: str,
                              note: Optional[str]) -> dict:
        await self._store(business_id, [Check(None, CheckType.MANUAL_ACTIVITY,
                                              "active" if active else "inactive",
                                              detail={"method": method, **({"note": note} if note else {})})])
        return await self.recompute(business_id)

    async def set_label(self, business_id: int, label: FounderLabel, wrong_part: Optional[str],
                        note: Optional[str]) -> dict:
        row = (await self.session.execute(select(LeadAssessment).where(
            LeadAssessment.business_id == business_id))).scalar_one_or_none()
        if row is None:
            return {"error": "Assess this business before labelling it."}
        row.label = label
        row.label_wrong_part = wrong_part if label == FounderLabel.WRONG else None
        row.label_note = note
        row.labeled_at = datetime.now(timezone.utc)
        await self.session.flush()
        return await self.detail(business_id)

    async def log_contact(self, business_id: int, channel: str, outcome: str,
                          note: Optional[str]) -> dict:
        if not await self._business(business_id):
            return {"error": f"Business {business_id} not found"}
        self.session.add(ContactLog(business_id=business_id, channel=channel, outcome=outcome,
                                    note=note, logged_at=datetime.now(timezone.utc)))
        await self.session.flush()
        has_assessment = (await self.session.execute(select(LeadAssessment.id).where(
            LeadAssessment.business_id == business_id))).scalar_one_or_none()
        # A do-not-contact entry must immediately block outreach readiness.
        return await (self.recompute(business_id) if has_assessment else self.detail(business_id))
