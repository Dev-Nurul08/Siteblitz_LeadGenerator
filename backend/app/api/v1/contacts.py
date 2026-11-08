"""
API v1 — Contact management, email verification, and domain intelligence routes (Phase 3).
"""

import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db_session
from backend.app.engines.enrichment.verifier import EmailVerifier
from backend.app.models.business import Business
from backend.app.models.contact import Contact, EmailVerificationStatus, RoleLevel
from backend.app.schemas.contact import (
    ContactCreate,
    ContactListResponse,
    ContactResponse,
    ContactStatsResponse,
    DomainContactSearchRequest,
    DomainContactSearchResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
    VerifyPhoneRequest,
    VerifyPhoneResponse,
)
from backend.app.services.enrichment_service import EnrichmentService

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("", response_model=ContactListResponse)
async def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    business_id: Optional[int] = Query(None),
    role_level: Optional[RoleLevel] = Query(None),
    email_status: Optional[EmailVerificationStatus] = Query(None),
    min_score: Optional[float] = Query(None, ge=0.0, le=1.0),
    search: Optional[str] = Query(None, max_length=500, description="Search by email or name"),
    session: AsyncSession = Depends(get_db_session),
):
    """
    List business contacts with filtering and pagination.
    """
    stmt = (
        select(Contact, Business.name, Business.country_code, Business.phone)
        .join(Business, Contact.business_id == Business.id)
    )

    if business_id:
        stmt = stmt.where(Contact.business_id == business_id)
    if role_level:
        stmt = stmt.where(Contact.role_level == role_level)
    if email_status:
        stmt = stmt.where(Contact.email_status == email_status)
    if min_score is not None:
        stmt = stmt.where(Contact.verification_score >= min_score)
    if search:
        stmt = stmt.where(
            or_(
                Contact.email.ilike(f"%{search}%"),
                Contact.full_name.ilike(f"%{search}%"),
                Business.name.ilike(f"%{search}%"),
            )
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.order_by(Contact.verification_score.desc(), Contact.created_at.desc()).offset(offset).limit(page_size)

    rows = (await session.execute(stmt)).all()
    items = []
    for c, b_name, b_country, b_phone in rows:
        resp = ContactResponse(
            id=c.id,
            business_id=c.business_id,
            full_name=c.full_name,
            first_name=c.first_name,
            last_name=c.last_name,
            job_title=c.job_title,
            role_level=c.role_level,
            email=c.email,
            email_status=c.email_status,
            verification_score=c.verification_score,
            has_valid_mx=c.has_valid_mx,
            is_role_based=c.is_role_based,
            is_disposable=c.is_disposable,
            phone=c.phone or b_phone,
            linkedin_url=c.linkedin_url,
            source_method=c.source_method,
            source_url=c.source_url,
            verification_details=c.verification_details,
            verified_at=c.verified_at,
            created_at=c.created_at,
            business_name=b_name,
            business_country=b_country,
        )
        items.append(resp)

    return ContactListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/stats/overview", response_model=ContactStatsResponse)
async def get_contact_stats(
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get aggregated contact counts, deliverability rate, and role breakdown.
    """
    total_stmt = select(func.count(Contact.id))
    total = (await session.execute(total_stmt)).scalar() or 0

    # By status
    status_stmt = select(Contact.email_status, func.count(Contact.id)).group_by(Contact.email_status)
    by_status = {row[0].value: row[1] for row in (await session.execute(status_stmt))}

    # By role
    role_stmt = select(Contact.role_level, func.count(Contact.id)).group_by(Contact.role_level)
    by_role = {row[0].value: row[1] for row in (await session.execute(role_stmt))}

    verified_count = by_status.get("VERIFIED", 0) + by_status.get("ROLE_BASED", 0)
    verified_rate = round((verified_count / total * 100) if total > 0 else 0.0, 1)

    return ContactStatsResponse(
        total_contacts=total,
        by_status=by_status,
        by_role=by_role,
        verified_rate=verified_rate,
    )


@router.post("/enrich-business/{business_id}")
async def enrich_business_contacts(
    business_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Trigger contact discovery and email verification for a business.
    """
    service = EnrichmentService(session)
    result = await service.enrich_business(business_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/batch-enrich")
async def batch_enrich(
    limit: int = Query(25, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Discover contacts for businesses that have none registered.
    """
    service = EnrichmentService(session)
    return await service.batch_enrich_businesses(limit=limit)


@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_standalone_email(
    request: VerifyEmailRequest,
):
    """
    Standalone email address verification tool with MX and mail provider inspection.
    """
    verifier = EmailVerifier()
    res = verifier.verify(request.email)
    return VerifyEmailResponse(
        email=res.email,
        status=res.status,
        is_valid_syntax=res.is_valid_syntax,
        is_disposable=res.is_disposable,
        is_role_based=res.is_role_based,
        is_free_email=res.is_free_email,
        has_valid_mx=res.has_valid_mx,
        verification_score=res.verification_score,
        domain=res.domain,
        mx_records=res.mx_records,
        mail_provider=res.mail_provider,
        suggested_correction=res.suggested_correction,
    )


@router.post("/verify-phone", response_model=VerifyPhoneResponse)
async def verify_standalone_phone(
    request: VerifyPhoneRequest,
):
    """
    Validate, normalize, and format a business telephone number.
    """
    res = EmailVerifier.verify_phone(request.phone, default_country=request.country_code)
    return VerifyPhoneResponse(
        raw_phone=res.raw_phone,
        formatted_phone=res.formatted_phone,
        is_valid=res.is_valid,
        country_code=res.country_code,
        phone_type=res.phone_type,
    )


@router.post("/find-domain-contacts", response_model=DomainContactSearchResponse)
async def find_domain_contacts(
    request: DomainContactSearchRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    On-demand domain contact discovery and verification without requiring a pre-existing business record.
    """
    service = EnrichmentService(session)
    res = await service.discover_domain_contacts(request.domain_or_url)
    return DomainContactSearchResponse(
        query=res["query"],
        contacts_found=res["contacts_found"],
        contacts=res["contacts"],
    )


@router.post("", response_model=ContactResponse)
async def create_manual_contact(
    data: ContactCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Manually add a contact for a business. Automatically runs verification and role classification.
    """
    biz_stmt = select(Business).where(Business.id == data.business_id)
    biz = (await session.execute(biz_stmt)).scalar_one_or_none()
    if not biz:
        raise HTTPException(status_code=404, detail="Business not found")

    verifier = EmailVerifier()
    ver_res = verifier.verify(data.email)

    from backend.app.engines.enrichment.classifier import ContactClassifier
    classifier = ContactClassifier()
    cls_res = classifier.classify_contact(data.full_name, data.job_title, data.email)

    contact = Contact(
        business_id=data.business_id,
        email=data.email.lower().strip(),
        full_name=cls_res.full_name,
        first_name=cls_res.first_name,
        last_name=cls_res.last_name,
        job_title=cls_res.job_title,
        role_level=cls_res.role_level,
        email_status=ver_res.status,
        verification_score=ver_res.verification_score,
        has_valid_mx=ver_res.has_valid_mx,
        is_role_based=ver_res.is_role_based,
        is_disposable=ver_res.is_disposable,
        phone=data.phone,
        linkedin_url=data.linkedin_url,
        source_method="manual",
        verification_details=ver_res.details,
    )
    session.add(contact)
    await session.flush()
    await session.refresh(contact)

    return ContactResponse(
        id=contact.id,
        business_id=contact.business_id,
        full_name=contact.full_name,
        first_name=contact.first_name,
        last_name=contact.last_name,
        job_title=contact.job_title,
        role_level=contact.role_level,
        email=contact.email,
        email_status=contact.email_status,
        verification_score=contact.verification_score,
        has_valid_mx=contact.has_valid_mx,
        is_role_based=contact.is_role_based,
        is_disposable=contact.is_disposable,
        phone=contact.phone,
        linkedin_url=contact.linkedin_url,
        source_method=contact.source_method,
        source_url=contact.source_url,
        verification_details=contact.verification_details,
        verified_at=contact.verified_at,
        created_at=contact.created_at,
        business_name=biz.name,
        business_country=biz.country_code,
    )


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Delete a contact by ID.
    """
    stmt = select(Contact).where(Contact.id == contact_id)
    contact = (await session.execute(stmt)).scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    await session.delete(contact)
    await session.flush()
    return {"status": "deleted", "contact_id": contact_id}
