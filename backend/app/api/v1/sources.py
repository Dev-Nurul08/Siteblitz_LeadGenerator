"""
API v1 — Source management routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db_session
from backend.app.models.source import Source, SourceJob, JobStatus
from backend.app.schemas.source import (
    SourceCreate,
    SourceJobResponse,
    SourceResponse,
    SourceUpdate,
)

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.get("", response_model=list[SourceResponse])
async def list_sources(
    session: AsyncSession = Depends(get_db_session),
):
    """List all registered data sources."""
    stmt = select(Source).order_by(Source.name)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """Get a specific data source by ID."""
    stmt = select(Source).where(Source.id == source_id)
    result = await session.execute(stmt)
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("", response_model=SourceResponse, status_code=201)
async def create_source(
    data: SourceCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """Register a new data source."""
    # Check for duplicate slug
    stmt = select(Source).where(Source.slug == data.slug)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Source with this slug already exists")

    source = Source(**data.model_dump())
    session.add(source)
    await session.flush()
    await session.refresh(source)
    return source


@router.patch("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    data: SourceUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    """Update an existing data source."""
    stmt = select(Source).where(Source.id == source_id)
    result = await session.execute(stmt)
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(source, key, value)

    await session.flush()
    await session.refresh(source)
    return source


@router.get("/{source_id}/jobs", response_model=list[SourceJobResponse])
async def list_source_jobs(
    source_id: int,
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
):
    """List discovery jobs for a source."""
    stmt = (
        select(SourceJob)
        .where(SourceJob.source_id == source_id)
        .order_by(SourceJob.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
