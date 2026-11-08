"""
API v1 — Website Intelligence (phase 2): verdicts, need score, tiers, evidence, founder labels.
"""

import math
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.database import get_db_session
from backend.app.models.business import Business, BusinessSourceLink, BusinessStatus
from backend.app.models.intelligence import ContactLog, FounderLabel, LeadAssessment, LeadTier, WebsiteVerdict
from backend.app.models.source import SourceJob, SourceRecord
from backend.app.schemas.types import HttpUrl, Opt, OptionalText
from backend.app.services.intelligence_service import IntelligenceService

router = APIRouter(prefix="/intelligence", tags=["Website Intelligence"])


class ManualSearchRequest(BaseModel):
    model_config = {"extra": "forbid"}
    found_url: Opt(HttpUrl) = None  # empty = "I searched name + city and found no website"
    note: OptionalText() = None


class ActivityRequest(BaseModel):
    model_config = {"extra": "forbid"}
    active: bool
    method: Literal["call", "visit", "post"]
    note: OptionalText() = None


class ContactLogRequest(BaseModel):
    model_config = {"extra": "forbid"}
    channel: Literal["phone", "email", "social", "form", "visit"]
    outcome: Literal["interested", "not_now", "no_reply", "do_not_contact", "other"]
    note: OptionalText() = None


class LabelRequest(BaseModel):
    model_config = {"extra": "forbid"}
    label: FounderLabel
    wrong_part: Optional[Literal["ownership", "activity", "identity", "exclusion", "need"]] = None
    note: OptionalText() = None


def _job_filter(job_id: int):
    return Business.id.in_(
        select(BusinessSourceLink.business_id)
        .join(SourceRecord, SourceRecord.id == BusinessSourceLink.source_record_id)
        .where(SourceRecord.job_id == job_id))


@router.post("/assess/{business_id}")
async def assess_business(business_id: int, include_franchises: bool = False,
                          session: AsyncSession = Depends(get_db_session)):
    """Run every website check for one business and return its verdict, score and evidence."""
    result = await IntelligenceService(session).assess_business(business_id, include_franchises)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/assess-batch")
async def assess_batch(
    job_id: Optional[int] = Query(None, ge=1),
    limit: int = Query(25, ge=1, le=100),
    only_unassessed: bool = True,
    include_franchises: bool = False,
    recheck: Optional[Literal["UNKNOWN"]] = None,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Assess up to `limit` businesses (optionally only those found by one job).
    recheck=UNKNOWN re-runs the checks of "Needs review" businesses — e.g. a listed website that
    failed once becomes "Website down" when it fails again ≥ 6 h later.
    """
    stmt = select(Business.id).where(
        Business.status.notin_([BusinessStatus.DUPLICATE, BusinessStatus.INVALID]))
    if job_id:
        stmt = stmt.where(_job_filter(job_id))
    if recheck:
        stmt = stmt.where(Business.id.in_(select(LeadAssessment.business_id).where(
            LeadAssessment.website_verdict == WebsiteVerdict(recheck))))
    elif only_unassessed:
        stmt = stmt.where(Business.id.notin_(select(LeadAssessment.business_id)))
    ids = (await session.execute(stmt.order_by(Business.id).limit(limit))).scalars().all()
    tiers: dict[str, int] = {}
    for detail in await IntelligenceService(session).assess_many(list(ids), include_franchises):
        tier = (detail.get("assessment") or {}).get("tier", "ERROR")
        tiers[tier] = tiers.get(tier, 0) + 1
    remaining_stmt = select(func.count(Business.id)).where(
        Business.status.notin_([BusinessStatus.DUPLICATE, BusinessStatus.INVALID]),
        Business.id.notin_(select(LeadAssessment.business_id)))
    if job_id:
        remaining_stmt = remaining_stmt.where(_job_filter(job_id))
    remaining = (await session.execute(remaining_stmt)).scalar() or 0
    return {"assessed": len(ids), "by_tier": tiers, "remaining_unassessed": remaining}


@router.get("/leads")
async def list_leads(
    tier: Optional[LeadTier] = None,
    verdict: Optional[Literal[
        "OWN_SITE_VERIFIED", "SOCIAL_ONLY_VERIFIED", "NO_SITE_VERIFIED",
        "SITE_DOWN_CONFIRMED", "UNKNOWN", "SKIP", "UNCHECKED"]] = None,
    job_id: Optional[int] = Query(None, ge=1),
    labeled: Optional[bool] = None,
    search: Optional[str] = Query(None, max_length=500),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
):
    """Businesses with their assessment (UNCHECKED = not assessed yet), best need score first."""
    base = (select(Business, LeadAssessment)
            .outerjoin(LeadAssessment, LeadAssessment.business_id == Business.id)
            .where(Business.status.notin_([BusinessStatus.DUPLICATE, BusinessStatus.INVALID])))
    if job_id:
        base = base.where(_job_filter(job_id))
    if search:
        base = base.where(or_(Business.name.ilike(f"%{search}%"),
                              Business.normalized_name.ilike(f"%{search}%")))
    filtered = base
    if tier:
        filtered = filtered.where(LeadAssessment.tier == tier)
    if verdict == "UNCHECKED":
        filtered = filtered.where(LeadAssessment.id.is_(None))
    elif verdict:
        filtered = filtered.where(LeadAssessment.website_verdict == WebsiteVerdict(verdict))
    if labeled is True:
        filtered = filtered.where(LeadAssessment.label.isnot(None))
    elif labeled is False:
        filtered = filtered.where(LeadAssessment.label.is_(None))

    total = (await session.execute(select(func.count()).select_from(filtered.subquery()))).scalar() or 0
    rows = (await session.execute(
        filtered.options(selectinload(Business.locations), selectinload(Business.categories))
        .order_by(LeadAssessment.need_score.desc().nulls_last(), Business.name)
        .offset((page - 1) * page_size).limit(page_size))).all()

    # Tab counts for the same base filters (job / search), independent of tier / verdict.
    sub = base.subquery()
    tier_counts = {str(t.value if hasattr(t, "value") else t): n for t, n in (await session.execute(
        select(sub.c.tier, func.count()).group_by(sub.c.tier))).all() if t is not None}
    verdict_counts = {str(v.value if hasattr(v, "value") else v): n for v, n in (await session.execute(
        select(sub.c.website_verdict, func.count()).group_by(sub.c.website_verdict))).all()
        if v is not None}
    unchecked = (await session.execute(select(func.count()).select_from(sub).where(
        sub.c.website_verdict.is_(None)))).scalar() or 0
    verdict_counts["UNCHECKED"] = unchecked

    items = []
    for business, a in rows:
        location = business.locations[0] if business.locations else None
        items.append({
            "id": business.id, "name": business.name,
            "category": business.categories[0].category_name if business.categories else None,
            "city": location.city if location else None,
            "country_code": business.country_code,
            "phone": business.phone, "email": business.email,
            "website_url": business.website_url,
            "social_platforms": sorted((business.social_urls or {}).keys()),
            "lat": location.latitude if location else None,
            "lon": location.longitude if location else None,
            "website_verdict": a.website_verdict.value if a else "UNCHECKED",
            "evidence_confidence": a.evidence_confidence.value if a else None,
            "need_score": a.need_score if a else None,
            "tier": a.tier.value if a else None,
            "outreach_readiness": a.outreach_readiness.value if a else None,
            "label": a.label.value if a and a.label else None,
            "assessed_at": a.assessed_at.isoformat() if a and a.assessed_at else None,
        })
    return {"items": items, "total": total, "page": page, "page_size": page_size,
            "pages": math.ceil(total / page_size) if total else 0,
            "tier_counts": tier_counts, "verdict_counts": verdict_counts}


@router.get("/stats")
async def stats(session: AsyncSession = Depends(get_db_session)):
    """Counts for the stepper and the pilot strip."""
    active = Business.status.notin_([BusinessStatus.DUPLICATE, BusinessStatus.INVALID])
    businesses = (await session.execute(select(func.count(Business.id)).where(active))).scalar() or 0
    by_tier = {t.value: n for t, n in (await session.execute(
        select(LeadAssessment.tier, func.count()).group_by(LeadAssessment.tier))).all()}
    labels = {l.value: n for l, n in (await session.execute(
        select(LeadAssessment.label, func.count()).where(LeadAssessment.label.isnot(None))
        .group_by(LeadAssessment.label))).all()}
    assessed = sum(by_tier.values())
    needs_review = by_tier.get("REVIEW", 0)
    contacted = (await session.execute(select(func.count(func.distinct(ContactLog.business_id))))).scalar() or 0
    jobs = (await session.execute(select(func.count(SourceJob.id)))).scalar() or 0
    return {"businesses": businesses, "assessed": assessed, "unassessed": max(businesses - assessed, 0),
            "by_tier": by_tier, "needs_review": needs_review, "labels": labels,
            "labeled": sum(labels.values()), "contacted": contacted, "jobs": jobs}


@router.get("/business/{business_id}")
async def business_detail(business_id: int, session: AsyncSession = Depends(get_db_session)):
    result = await IntelligenceService(session).detail(business_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/business/{business_id}/manual-search")
async def manual_search(business_id: int, payload: ManualSearchRequest,
                        session: AsyncSession = Depends(get_db_session)):
    """Record the founder's own web search for "name + city" (found a site, or found none)."""
    result = await IntelligenceService(session).record_manual_search(
        business_id, payload.found_url, payload.note)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/business/{business_id}/activity")
async def activity(business_id: int, payload: ActivityRequest,
                   session: AsyncSession = Depends(get_db_session)):
    """Record that the business is open (or closed) — e.g. after a phone call."""
    result = await IntelligenceService(session).record_activity(
        business_id, payload.active, payload.method, payload.note)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/business/{business_id}/label")
async def label(business_id: int, payload: LabelRequest,
                session: AsyncSession = Depends(get_db_session)):
    """Founder's Correct / Wrong / Unsure label on the verdict (pilot benchmark, spec row 19)."""
    if payload.label == FounderLabel.WRONG and not payload.wrong_part:
        raise HTTPException(status_code=422, detail="Say what was wrong (wrong_part).")
    result = await IntelligenceService(session).set_label(
        business_id, payload.label, payload.wrong_part, payload.note)
    if "error" in result:
        raise HTTPException(status_code=409, detail=result["error"])
    return result


@router.post("/business/{business_id}/contact-log")
async def contact_log(business_id: int, payload: ContactLogRequest,
                      session: AsyncSession = Depends(get_db_session)):
    """Log a call / email / message the founder made himself; "do_not_contact" blocks the lead."""
    result = await IntelligenceService(session).log_contact(
        business_id, payload.channel, payload.outcome, payload.note)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
