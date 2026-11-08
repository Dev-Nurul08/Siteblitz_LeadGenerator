"""
API v1 — Qualification & Compliance Routes (Phase 4).

Exposes lead qualification endpoints, operator review workflows,
AI personalized pitch previews, and global suppression / opt-out management.
"""

from datetime import datetime, timezone
import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db_session
from backend.app.models.business import Business, BusinessLocation
from backend.app.models.compliance import (
    ComplianceEvaluation,
    LeadStatus,
    OptOut,
    QualifiedLead,
)
from backend.app.models.contact import Contact
from backend.app.models.opportunity import Opportunity
from backend.app.schemas.qualification import (
    LeadListResponse,
    LeadResponse,
    LeadStatsResponse,
    LeadStatusUpdateRequest,
    OptOutCreateRequest,
    OptOutListResponse,
    OptOutResponse,
)
from backend.app.services.qualification_service import QualificationService

router = APIRouter(prefix="/qualification", tags=["Qualification & Compliance"])


@router.get("/leads", response_model=LeadListResponse)
async def list_qualified_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    status: Optional[LeadStatus] = Query(None),
    min_score: Optional[float] = Query(None, ge=0.0, le=100.0),
    country: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db_session),
):
    """
    List qualified leads with comprehensive filtering and pagination.
    """
    stmt = (
        select(
            QualifiedLead,
            Business.name,
            Business.country_code,
            BusinessLocation.city,
            Contact.email,
            Contact.full_name,
            Contact.job_title,
            Opportunity.service_category,
            ComplianceEvaluation.legal_framework,
            ComplianceEvaluation.outreach_mode,
        )
        .join(Business, QualifiedLead.business_id == Business.id)
        .outerjoin(BusinessLocation, (BusinessLocation.business_id == Business.id) & (BusinessLocation.is_primary == True))
        .join(Contact, QualifiedLead.contact_id == Contact.id)
        .join(Opportunity, QualifiedLead.opportunity_id == Opportunity.id)
        .outerjoin(ComplianceEvaluation, QualifiedLead.compliance_evaluation_id == ComplianceEvaluation.id)
    )

    if status:
        stmt = stmt.where(QualifiedLead.lead_status == status)
    if min_score is not None:
        stmt = stmt.where(QualifiedLead.composite_score >= min_score)
    if country:
        stmt = stmt.where(Business.country_code == country.upper())
    if search:
        stmt = stmt.where(
            or_(
                Business.name.ilike(f"%{search}%"),
                Contact.email.ilike(f"%{search}%"),
                Contact.full_name.ilike(f"%{search}%"),
            )
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(QualifiedLead.composite_score.desc(), QualifiedLead.created_at.desc()).offset(offset).limit(page_size)

    rows = (await session.execute(stmt)).all()
    items = []
    for (
        lead,
        b_name,
        b_country,
        b_city,
        c_email,
        c_name,
        c_title,
        opp_service,
        comp_framework,
        comp_mode,
    ) in rows:
        resp = LeadResponse(
            id=lead.id,
            business_id=lead.business_id,
            business_name=b_name,
            business_country=b_country,
            business_city=b_city,
            contact_id=lead.contact_id,
            contact_name=c_name,
            contact_email=c_email,
            contact_job_title=c_title,
            opportunity_id=lead.opportunity_id,
            opportunity_service=opp_service.value if hasattr(opp_service, "value") else str(opp_service),
            composite_score=lead.composite_score,
            lead_status=lead.lead_status,
            outreach_channel=lead.outreach_channel,
            personalized_subject=lead.personalized_subject,
            personalized_pitch=lead.personalized_pitch,
            validation_passed=lead.validation_passed,
            validation_flags=lead.validation_flags or [],
            legal_framework=comp_framework,
            outreach_mode=comp_mode,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
        )
        items.append(resp)

    return LeadListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/leads/stats/overview", response_model=LeadStatsResponse)
async def get_lead_stats(
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get aggregated lead counts, average scores, and review queue counts.
    """
    total_stmt = select(func.count(QualifiedLead.id))
    total_leads = (await session.execute(total_stmt)).scalar() or 0

    status_stmt = select(QualifiedLead.lead_status, func.count(QualifiedLead.id)).group_by(QualifiedLead.lead_status)
    by_status = {row[0].value: row[1] for row in (await session.execute(status_stmt))}

    avg_stmt = select(func.avg(QualifiedLead.composite_score))
    avg_score = (await session.execute(avg_stmt)).scalar() or 0.0

    ready_count = by_status.get(LeadStatus.READY_FOR_OUTREACH.value, 0) + by_status.get(LeadStatus.QUALIFIED.value, 0)

    opt_stmt = select(func.count(OptOut.id))
    opt_count = (await session.execute(opt_stmt)).scalar() or 0

    return LeadStatsResponse(
        total_leads=total_leads,
        by_status=by_status,
        avg_composite_score=round(float(avg_score), 1),
        ready_for_outreach_count=ready_count,
        opt_out_count=opt_count,
    )


@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead_details(
    lead_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Fetch full details, audit record, and generated pitch for a qualified lead.
    """
    stmt = (
        select(
            QualifiedLead,
            Business.name,
            Business.country_code,
            BusinessLocation.city,
            Contact.email,
            Contact.full_name,
            Contact.job_title,
            Opportunity.service_category,
            ComplianceEvaluation.legal_framework,
            ComplianceEvaluation.outreach_mode,
        )
        .join(Business, QualifiedLead.business_id == Business.id)
        .outerjoin(BusinessLocation, (BusinessLocation.business_id == Business.id) & (BusinessLocation.is_primary == True))
        .join(Contact, QualifiedLead.contact_id == Contact.id)
        .join(Opportunity, QualifiedLead.opportunity_id == Opportunity.id)
        .outerjoin(ComplianceEvaluation, QualifiedLead.compliance_evaluation_id == ComplianceEvaluation.id)
        .where(QualifiedLead.id == lead_id)
    )

    row = (await session.execute(stmt)).first()
    if not row:
        raise HTTPException(status_code=404, detail=f"Qualified lead #{lead_id} not found.")

    (
        lead,
        b_name,
        b_country,
        b_city,
        c_email,
        c_name,
        c_title,
        opp_service,
        comp_framework,
        comp_mode,
    ) = row

    return LeadResponse(
        id=lead.id,
        business_id=lead.business_id,
        business_name=b_name,
        business_country=b_country,
        business_city=b_city,
        contact_id=lead.contact_id,
        contact_name=c_name,
        contact_email=c_email,
        contact_job_title=c_title,
        opportunity_id=lead.opportunity_id,
        opportunity_service=opp_service.value if hasattr(opp_service, "value") else str(opp_service),
        composite_score=lead.composite_score,
        lead_status=lead.lead_status,
        outreach_channel=lead.outreach_channel,
        personalized_subject=lead.personalized_subject,
        personalized_pitch=lead.personalized_pitch,
        validation_passed=lead.validation_passed,
        validation_flags=lead.validation_flags or [],
        legal_framework=comp_framework,
        outreach_mode=comp_mode,
        created_at=lead.created_at,
        updated_at=lead.updated_at,
    )


@router.patch("/leads/{lead_id}/status")
async def update_lead_status(
    lead_id: int,
    payload: LeadStatusUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Operator status transition: Approve to READY_FOR_OUTREACH, send to NEEDS_REVIEW, or DISQUALIFY.
    """
    service = QualificationService(session)
    result = await service.update_lead_status(lead_id, payload.status, payload.notes)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/qualify-business/{business_id}")
async def qualify_business(
    business_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Run regulatory compliance audit, compute lead score, and synthesize personalized pitch.
    """
    service = QualificationService(session)
    result = await service.qualify_lead(business_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/batch-qualify")
async def batch_qualify(
    limit: int = Query(25, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Batch qualify un-evaluated businesses.
    """
    service = QualificationService(session)
    return await service.batch_qualify(limit=limit)


# ─── Opt-Out & Suppression Registry Routes ──────────────────────


@router.get("/opt-outs", response_model=OptOutListResponse)
async def list_opt_outs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db_session),
):
    """
    List suppressed email addresses and domains.
    """
    stmt = select(OptOut)
    if search:
        stmt = stmt.where(
            or_(
                OptOut.email.ilike(f"%{search}%"),
                OptOut.domain.ilike(f"%{search}%"),
            )
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(OptOut.created_at.desc()).offset(offset).limit(page_size)

    rows = (await session.execute(stmt)).scalars().all()
    items = [
        OptOutResponse(
            id=o.id,
            email=o.email,
            domain=o.domain,
            reason=o.reason,
            source=o.source,
            created_at=o.created_at,
        )
        for o in rows
    ]

    return OptOutListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.post("/opt-outs", response_model=OptOutResponse)
async def create_opt_out(
    payload: OptOutCreateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Add email or domain to global suppression registry.
    """
    service = QualificationService(session)
    await service.add_opt_out(
        email=payload.email,
        reason=payload.reason,
        source=payload.source,
        domain=payload.domain,
    )

    stmt = select(OptOut).where(OptOut.email == payload.email.strip().lower())
    opt = (await session.execute(stmt)).scalar_one()

    return OptOutResponse(
        id=opt.id,
        email=opt.email,
        domain=opt.domain,
        reason=opt.reason,
        source=opt.source,
        created_at=opt.created_at,
    )


@router.post("/unsubscribe")
async def public_unsubscribe(
    email: str = Query(..., min_length=3),
    reason: Optional[str] = Query("Unsubscribed via link"),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Public 1-click unsubscribe endpoint for message recipients.
    """
    service = QualificationService(session)
    res = await service.add_opt_out(
        email=email,
        reason=reason or "Unsubscribed via link",
        source="UNSUBSCRIBE_LINK",
    )
    return {"message": "Successfully unsubscribed. You will receive no further messages.", "email": email}


@router.get("/unsubscribe")
async def public_unsubscribe_link(
    email: str = Query(..., min_length=3),
    reason: Optional[str] = Query("Unsubscribed via link"),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Same as POST /unsubscribe, for the link inside every message: a clicked link is a GET,
    and a GET-only click returning 405 would silently ignore the opt-out.
    """
    return await public_unsubscribe(email=email, reason=reason, session=session)
