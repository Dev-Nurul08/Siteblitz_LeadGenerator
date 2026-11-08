"""
API v1 — Opportunity management and technical website audit routes (Phase 2).
"""

import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.database import get_db_session
from backend.app.models.business import Business
from backend.app.models.opportunity import (
    Opportunity,
    OpportunityPriority,
    OpportunityStatus,
    ServiceCategory,
    WebsiteAudit,
)
from backend.app.schemas.opportunity import (
    AuditUrlRequest,
    AuditUrlResponse,
    OpportunityListResponse,
    OpportunityResponse,
    OpportunityStatsResponse,
    OpportunityUpdate,
    WebsiteAuditResponse,
)
from backend.app.services.opportunity_service import OpportunityService

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.get("", response_model=OpportunityListResponse)
async def list_opportunities(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    service_category: Optional[ServiceCategory] = Query(None),
    priority: Optional[OpportunityPriority] = Query(None),
    status: Optional[OpportunityStatus] = Query(None),
    min_score: Optional[float] = Query(None, ge=0, le=100),
    country: Optional[str] = Query(None, pattern="^[A-Za-z]{2}$", description="ISO 3166-1 alpha-2 country code"),
    session: AsyncSession = Depends(get_db_session),
):
    """
    List opportunities with filtering and pagination.
    """
    stmt = (
        select(Opportunity, Business.name, Business.country_code, Business.website_url)
        .join(Business, Opportunity.business_id == Business.id)
    )

    if service_category:
        stmt = stmt.where(Opportunity.service_category == service_category)
    if priority:
        stmt = stmt.where(Opportunity.priority == priority)
    if status:
        stmt = stmt.where(Opportunity.status == status)
    if min_score is not None:
        stmt = stmt.where(Opportunity.score >= min_score)
    if country:
        stmt = stmt.where(Business.country_code == country.upper())

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(Opportunity.score.desc()).offset(offset).limit(page_size)

    rows = (await session.execute(stmt)).all()
    items = []
    for opp, b_name, b_country, b_website in rows:
        resp = OpportunityResponse(
            id=opp.id,
            business_id=opp.business_id,
            audit_id=opp.audit_id,
            service_category=opp.service_category,
            title=opp.title,
            summary=opp.summary,
            score=opp.score,
            confidence=opp.confidence,
            priority=opp.priority,
            status=opp.status,
            evidence=opp.evidence,
            pitch_angles=opp.pitch_angles,
            created_at=opp.created_at,
            updated_at=opp.updated_at,
            business_name=b_name,
            business_country=b_country,
            business_website=b_website,
        )
        items.append(resp)

    return OpportunityListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/stats/overview", response_model=OpportunityStatsResponse)
async def get_opportunity_stats(
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get aggregated opportunity counts and score distribution.
    """
    total_stmt = select(func.count(Opportunity.id))
    total = (await session.execute(total_stmt)).scalar() or 0

    # By category
    cat_stmt = (
        select(Opportunity.service_category, func.count(Opportunity.id))
        .group_by(Opportunity.service_category)
    )
    by_category = {row[0].value: row[1] for row in (await session.execute(cat_stmt))}

    # By priority
    pri_stmt = (
        select(Opportunity.priority, func.count(Opportunity.id))
        .group_by(Opportunity.priority)
    )
    by_priority = {row[0].value: row[1] for row in (await session.execute(pri_stmt))}

    # By status
    sta_stmt = (
        select(Opportunity.status, func.count(Opportunity.id))
        .group_by(Opportunity.status)
    )
    by_status = {row[0].value: row[1] for row in (await session.execute(sta_stmt))}

    # Average score
    avg_stmt = select(func.avg(Opportunity.score))
    avg_score = (await session.execute(avg_stmt)).scalar() or 0.0

    return OpportunityStatsResponse(
        total_opportunities=total,
        by_category=by_category,
        by_priority=by_priority,
        by_status=by_status,
        average_score=round(float(avg_score), 1),
    )


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get single opportunity by ID.
    """
    stmt = (
        select(Opportunity, Business.name, Business.country_code, Business.website_url)
        .join(Business, Opportunity.business_id == Business.id)
        .where(Opportunity.id == opportunity_id)
    )
    row = (await session.execute(stmt)).first()
    if not row:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    opp, b_name, b_country, b_website = row
    return OpportunityResponse(
        id=opp.id,
        business_id=opp.business_id,
        audit_id=opp.audit_id,
        service_category=opp.service_category,
        title=opp.title,
        summary=opp.summary,
        score=opp.score,
        confidence=opp.confidence,
        priority=opp.priority,
        status=opp.status,
        evidence=opp.evidence,
        pitch_angles=opp.pitch_angles,
        created_at=opp.created_at,
        updated_at=opp.updated_at,
        business_name=b_name,
        business_country=b_country,
        business_website=b_website,
    )


@router.patch("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: int,
    data: OpportunityUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Update opportunity status or priority.
    """
    stmt = select(Opportunity).where(Opportunity.id == opportunity_id)
    opp = (await session.execute(stmt)).scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    if data.status is not None:
        opp.status = data.status
    if data.priority is not None:
        opp.priority = data.priority
    if data.score is not None:
        opp.score = data.score

    await session.flush()
    await session.refresh(opp)

    # Get business details for response
    biz = (await session.execute(select(Business).where(Business.id == opp.business_id))).scalar_one()

    return OpportunityResponse(
        id=opp.id,
        business_id=opp.business_id,
        audit_id=opp.audit_id,
        service_category=opp.service_category,
        title=opp.title,
        summary=opp.summary,
        score=opp.score,
        confidence=opp.confidence,
        priority=opp.priority,
        status=opp.status,
        evidence=opp.evidence,
        pitch_angles=opp.pitch_angles,
        created_at=opp.created_at,
        updated_at=opp.updated_at,
        business_name=biz.name,
        business_country=biz.country_code,
        business_website=biz.website_url,
    )


@router.post("/evaluate-business/{business_id}")
async def evaluate_business(
    business_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Trigger real-time website audit and opportunity identification for a business.
    """
    service = OpportunityService(session)
    result = await service.evaluate_business(business_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/batch-evaluate")
async def batch_evaluate(
    limit: int = Query(25, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Audit and identify opportunities for businesses that haven't been evaluated yet.
    """
    service = OpportunityService(session)
    result = await service.batch_evaluate_unaudited(limit=limit)
    return result


@router.get("/audits/{business_id}", response_model=list[WebsiteAuditResponse])
async def get_business_audits(
    business_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get audit history for a business.
    """
    stmt = (
        select(WebsiteAudit)
        .where(WebsiteAudit.business_id == business_id)
        .order_by(WebsiteAudit.audited_at.desc())
    )
    audits = (await session.execute(stmt)).scalars().all()
    return audits


@router.post("/audit-url", response_model=AuditUrlResponse)
async def audit_url_on_demand(
    request: AuditUrlRequest,
):
    """
    On-demand real-time website audit and opportunity identification for any URL.
    Does not require a pre-existing business record in the database.
    """
    from backend.app.engines.opportunity.resolver import WebsiteResolver
    from backend.app.engines.opportunity.auditor import WebsiteAuditor
    from backend.app.engines.opportunity.detector import OpportunityDetector
    from backend.app.engines.opportunity.scorer import OpportunityScorer

    resolver = WebsiteResolver()
    auditor = WebsiteAuditor()
    detector = OpportunityDetector()
    scorer = OpportunityScorer()

    resolution = await resolver.resolve(request.url)
    audit = None
    if resolution.is_reachable and resolution.html_content:
        audit = auditor.audit_html(
            url=resolution.final_url or request.url,
            html_content=resolution.html_content,
            headers=resolution.headers,
            original_url=resolution.original_url,
            final_url=resolution.final_url,
        )

    # Synthetic business container for evaluation
    name = request.business_name or (request.url.split("//")[-1].split("/")[0])
    temp_biz = Business(
        name=name,
        normalized_name=name.lower(),
        country_code=request.country_code or "US",
        website_url=resolution.final_url or request.url,
        website_status=resolution.status,
    )

    detected_needs = detector.detect_opportunities(
        business=temp_biz,
        audit=audit,
        resolution=resolution,
        business_categories=request.categories,
    )

    scored_opps = []
    for need in detected_needs:
        scored = scorer.score_need(need, temp_biz, request.categories)
        scored_opps.append({
            "service_category": need.service_category.value,
            "title": need.title,
            "summary": need.summary,
            "score": scored.score,
            "priority": scored.priority.value,
            "confidence": scored.confidence,
            "estimated_value_low": scored.estimated_value_low,
            "estimated_value_high": scored.estimated_value_high,
            "recommended_action": scored.recommended_action,
            "roi_summary": scored.roi_summary,
            "pitch_angles": need.pitch_angles,
            "evidence": need.evidence,
        })

    return AuditUrlResponse(
        url=request.url,
        final_url=resolution.final_url,
        is_reachable=resolution.is_reachable,
        status=resolution.status.value,
        load_time_seconds=resolution.load_time_seconds,
        has_ssl=resolution.has_ssl,
        is_mobile_responsive=audit.is_mobile_responsive if audit else False,
        detected_cms=audit.detected_cms if audit else None,
        detected_frameworks=audit.detected_frameworks if audit else [],
        has_ecommerce=audit.has_ecommerce if audit else False,
        has_online_booking=audit.has_online_booking if audit else False,
        has_analytics=audit.has_analytics if audit else False,
        emails_found=audit.emails_found if audit else [],
        phones_found=audit.phones_found if audit else [],
        social_links_found=audit.social_links_found if audit else {},
        audit_summary=audit.raw_technologies if audit else {},
        opportunities=scored_opps,
    )

