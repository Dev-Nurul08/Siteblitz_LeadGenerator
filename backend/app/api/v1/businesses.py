"""
API v1 — Business management routes.
"""

import math
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.database import get_db_session
from backend.app.models.business import (
    Business,
    BusinessCategory,
    BusinessLocation,
    BusinessSourceLink,
    BusinessStatus,
    WebsiteStatus,
)
from backend.app.models.source import SourceRecord
from backend.app.services import export_service
from backend.app.schemas.business import (
    BusinessListResponse,
    BusinessResponse,
    BusinessUpdate,
)

router = APIRouter(prefix="/businesses", tags=["Businesses"])


def _filtered_businesses(
    *,
    country: Optional[str],
    status: Optional[BusinessStatus],
    website_status: Optional[WebsiteStatus],
    category: Optional[str],
    search: Optional[str],
    job_id: Optional[int],
):
    """Business query with the list filters applied (shared by the list and the export)."""
    stmt = select(Business).options(
        selectinload(Business.locations),
        selectinload(Business.categories),
    )
    if country:
        stmt = stmt.where(Business.country_code == country.upper())
    if status:
        stmt = stmt.where(Business.status == status)
    if website_status:
        stmt = stmt.where(Business.website_status == website_status)
    if search:
        stmt = stmt.where(
            or_(
                Business.name.ilike(f"%{search}%"),
                Business.normalized_name.ilike(f"%{search}%"),
            )
        )
    if category:
        stmt = stmt.where(
            Business.id.in_(
                select(BusinessCategory.business_id).where(
                    BusinessCategory.normalized_category.ilike(f"%{category}%")
                )
            )
        )
    if job_id:
        # Businesses a discovery job found = those linked to that job's raw source records
        # (new ones and existing ones it matched as duplicates).
        stmt = stmt.where(
            Business.id.in_(
                select(BusinessSourceLink.business_id)
                .join(SourceRecord, SourceRecord.id == BusinessSourceLink.source_record_id)
                .where(SourceRecord.job_id == job_id)
            )
        )
    # Don't show duplicates or invalid by default
    if not status:
        stmt = stmt.where(
            Business.status.notin_([
                BusinessStatus.DUPLICATE,
                BusinessStatus.INVALID,
            ])
        )
    return stmt


COUNTRY_QUERY = Query(None, pattern="^[A-Za-z]{2}$", description="ISO 3166-1 alpha-2 country code")


@router.get("", response_model=BusinessListResponse)
async def list_businesses(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    country: Optional[str] = COUNTRY_QUERY,
    status: Optional[BusinessStatus] = Query(None),
    website_status: Optional[WebsiteStatus] = Query(None),
    category: Optional[str] = Query(None, max_length=200, description="Filter by category"),
    search: Optional[str] = Query(None, max_length=500, description="Search by name"),
    job_id: Optional[int] = Query(None, ge=1, description="Only businesses found by this discovery job"),
    session: AsyncSession = Depends(get_db_session),
):
    """
    List businesses with filtering and pagination.

    Supports filtering by country, status, website status,
    category, name search and discovery job.
    """
    stmt = _filtered_businesses(
        country=country, status=status, website_status=website_status,
        category=category, search=search, job_id=job_id,
    )

    # Count total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await session.execute(count_stmt)
    total = total_result.scalar() or 0

    # Paginate
    offset = (page - 1) * page_size
    stmt = stmt.order_by(Business.discovered_at.desc()).offset(offset).limit(page_size)

    result = await session.execute(stmt)
    businesses = result.scalars().unique().all()

    return BusinessListResponse(
        items=businesses,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/points")
async def business_points(
    country: Optional[str] = COUNTRY_QUERY,
    status: Optional[BusinessStatus] = Query(None),
    website_status: Optional[WebsiteStatus] = Query(None),
    category: Optional[str] = Query(None, max_length=200),
    search: Optional[str] = Query(None, max_length=500),
    job_id: Optional[int] = Query(None, ge=1),
    # 5000 = the largest discovery job (DiscoveryRequest.max_results)
    limit: int = Query(5000, ge=1, le=5000),
    session: AsyncSession = Depends(get_db_session),
):
    """Lightweight map points (id, name, lat, lon, website status, category) for the same filters."""
    stmt = _filtered_businesses(
        country=country, status=status, website_status=website_status,
        category=category, search=search, job_id=job_id,
    ).order_by(Business.discovered_at.desc()).limit(limit)
    businesses = (await session.execute(stmt)).scalars().unique().all()
    points = []
    for b in businesses:
        location = b.locations[0] if b.locations else None
        if location and location.latitude is not None and location.longitude is not None:
            points.append({
                "id": b.id,
                "name": b.name,
                "lat": location.latitude,
                "lon": location.longitude,
                "website_status": b.website_status.value,
                "category": b.categories[0].category_name if b.categories else None,
            })
    return {"total": len(businesses), "points": points}


# Declared before "/{business_id}": FastAPI matches routes in order, and "export" would
# otherwise be parsed as a business id and rejected with 422.
@router.get("/export")
async def export_businesses(
    format: Literal["csv", "pdf"] = Query("csv"),
    country: Optional[str] = COUNTRY_QUERY,
    status: Optional[BusinessStatus] = Query(None),
    website_status: Optional[WebsiteStatus] = Query(None),
    category: Optional[str] = Query(None, max_length=200),
    search: Optional[str] = Query(None, max_length=500),
    job_id: Optional[int] = Query(None, ge=1),
    session: AsyncSession = Depends(get_db_session),
):
    """Download every business matching the filters as CSV (all columns) or PDF (summary table)."""
    stmt = _filtered_businesses(
        country=country, status=status, website_status=website_status,
        category=category, search=search, job_id=job_id,
    ).order_by(Business.discovered_at.desc())
    businesses = (await session.execute(stmt)).scalars().unique().all()
    rows = [export_service.business_row(b) for b in businesses]

    applied = {
        "country": country, "status": status.value if status else None,
        "website": website_status.value if website_status else None,
        "category": category, "search": search, "job": job_id,
    }
    filters_text = ", ".join(f"{k}={v}" for k, v in applied.items() if v)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    filename = f"siteblitz-businesses{'-job' + str(job_id) if job_id else ''}-{stamp}.{format}"

    if format == "csv":
        body, media_type = export_service.to_csv(rows), "text/csv; charset=utf-8"
    else:
        body, media_type = export_service.to_pdf(rows, filters_text), "application/pdf"
    return Response(
        content=body,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(
    business_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """Get a specific business by ID with all details."""
    stmt = (
        select(Business)
        .where(Business.id == business_id)
        .options(
            selectinload(Business.locations),
            selectinload(Business.categories),
        )
    )
    result = await session.execute(stmt)
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.patch("/{business_id}", response_model=BusinessResponse)
async def update_business(
    business_id: int,
    data: BusinessUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    """Update a business record."""
    stmt = (
        select(Business)
        .where(Business.id == business_id)
        .options(
            selectinload(Business.locations),
            selectinload(Business.categories),
        )
    )
    result = await session.execute(stmt)
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(business, key, value)

    await session.flush()
    await session.refresh(business)
    return business


@router.get("/stats/overview")
async def get_stats(
    session: AsyncSession = Depends(get_db_session),
):
    """Get overview statistics for the business database."""
    # Total businesses
    total_stmt = select(func.count(Business.id)).where(
        Business.status.notin_([BusinessStatus.DUPLICATE, BusinessStatus.INVALID])
    )
    total = (await session.execute(total_stmt)).scalar() or 0

    # By status
    status_stmt = (
        select(Business.status, func.count(Business.id))
        .group_by(Business.status)
    )
    status_result = await session.execute(status_stmt)
    by_status = {str(row[0].value): row[1] for row in status_result}

    # By website status
    ws_stmt = (
        select(Business.website_status, func.count(Business.id))
        .where(Business.status.notin_([BusinessStatus.DUPLICATE, BusinessStatus.INVALID]))
        .group_by(Business.website_status)
    )
    ws_result = await session.execute(ws_stmt)
    by_website = {str(row[0].value): row[1] for row in ws_result}

    # By country
    country_stmt = (
        select(Business.country_code, func.count(Business.id))
        .where(
            Business.status.notin_([BusinessStatus.DUPLICATE, BusinessStatus.INVALID]),
            Business.country_code.isnot(None),
        )
        .group_by(Business.country_code)
        .order_by(func.count(Business.id).desc())
        .limit(20)
    )
    country_result = await session.execute(country_stmt)
    by_country = {row[0]: row[1] for row in country_result}

    # Top categories
    cat_stmt = (
        select(BusinessCategory.industry_group, func.count(BusinessCategory.id))
        .where(BusinessCategory.industry_group.isnot(None))
        .group_by(BusinessCategory.industry_group)
        .order_by(func.count(BusinessCategory.id).desc())
        .limit(10)
    )
    cat_result = await session.execute(cat_stmt)
    top_categories = {row[0]: row[1] for row in cat_result}

    return {
        "total_businesses": total,
        "by_status": by_status,
        "by_website_status": by_website,
        "by_country": by_country,
        "top_categories": top_categories,
    }
