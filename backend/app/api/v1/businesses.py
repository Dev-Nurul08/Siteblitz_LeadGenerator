"""
API v1 — Business management routes.
"""

import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.database import get_db_session
from backend.app.models.business import (
    Business,
    BusinessCategory,
    BusinessLocation,
    BusinessStatus,
    WebsiteStatus,
)
from backend.app.schemas.business import (
    BusinessListResponse,
    BusinessResponse,
    BusinessUpdate,
)

router = APIRouter(prefix="/businesses", tags=["Businesses"])


@router.get("", response_model=BusinessListResponse)
async def list_businesses(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    country: Optional[str] = Query(None, description="Filter by country code"),
    status: Optional[BusinessStatus] = Query(None),
    website_status: Optional[WebsiteStatus] = Query(None),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by name"),
    session: AsyncSession = Depends(get_db_session),
):
    """
    List businesses with filtering and pagination.

    Supports filtering by country, status, website status,
    category, and name search.
    """
    # Base query
    stmt = select(Business).options(
        selectinload(Business.locations),
        selectinload(Business.categories),
    )

    # Apply filters
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
        stmt = stmt.join(Business.categories).where(
            BusinessCategory.normalized_category.ilike(f"%{category}%")
        )

    # Don't show duplicates or invalid by default
    if not status:
        stmt = stmt.where(
            Business.status.notin_([
                BusinessStatus.DUPLICATE,
                BusinessStatus.INVALID,
            ])
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
