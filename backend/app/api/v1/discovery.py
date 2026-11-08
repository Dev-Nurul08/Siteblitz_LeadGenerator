"""
API v1 — Discovery execution routes.
"""

from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db_session
from backend.app.models.source import SourceJob
from backend.app.schemas.business import DiscoveryRequest, DiscoveryStatusResponse
from backend.app.services.discovery_service import DiscoveryService

router = APIRouter(prefix="/discovery", tags=["Discovery"])

# Largest useful CSV: an import keeps at most 5,000 rows (DiscoveryRequest.max_results limit) and
# one business row is at most ~3 KB at the DB column sizes (name 500, address 500, website 1000 …).
MAX_CSV_BYTES = 15_000_000


@router.post("/run")
async def run_discovery(
    request: DiscoveryRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Trigger a business discovery run.

    This executes the discovery pipeline synchronously for now.
    For production, this should be queued as a background job.
    """
    service = DiscoveryService(session)
    result = await service.run_discovery(
        source_slug=request.source_slug,
        country_code=request.country_code,
        region=request.region,
        city=request.city,
        category=request.category,
        latitude=request.latitude,
        longitude=request.longitude,
        radius_km=request.radius_km,
        max_results=request.max_results,
        query_params=request.query_params,
    )

    if "error" in result and "job_id" not in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/import-csv")
async def import_csv(
    file: UploadFile = File(...),
    country_code: Optional[str] = Form(None, pattern="^[A-Za-z]{2}$"),
    delimiter: Literal[",", ";", "\t", "|"] = Form(","),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Import businesses from a CSV file.

    The CSV should have headers that match common field names
    (name, address, city, country, phone, email, website, category).
    """
    if not (file.filename or "").lower().endswith((".csv", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported",
        )

    # Read at most one byte past the limit so a huge upload is rejected without loading it all.
    content = await file.read(MAX_CSV_BYTES + 1)
    if len(content) > MAX_CSV_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"CSV file is larger than {MAX_CSV_BYTES // 1_000_000} MB",
        )
    try:
        csv_content = content.decode("utf-8-sig")  # Handle BOM
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="CSV must be UTF-8 encoded (in Excel: Save As → CSV UTF-8)",
        )
    if "\x00" in csv_content:
        raise HTTPException(status_code=400, detail="File is not a text CSV")

    service = DiscoveryService(session)
    result = await service.run_discovery(
        source_slug="csv_import",
        country_code=country_code.upper() if country_code else None,
        # Without this the service default (500) silently dropped every row after row 500.
        max_results=5000,
        query_params={
            "csv_content": csv_content,
            "delimiter": delimiter,
        },
    )

    return result


@router.get("/jobs/{job_id}", response_model=DiscoveryStatusResponse)
async def get_job_status(
    job_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """Get the status of a discovery job."""
    stmt = select(SourceJob).where(SourceJob.id == job_id)
    result = await session.execute(stmt)
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get source name
    from backend.app.models.source import Source
    source_stmt = select(Source.name).where(Source.id == job.source_id)
    source_result = await session.execute(source_stmt)
    source_name = source_result.scalar() or "Unknown"

    return DiscoveryStatusResponse(
        job_id=job.id,
        source_name=source_name,
        status=job.status.value,
        country_code=job.country_code,
        city=(job.city or '').strip() or None,
        category=job.category_filter,
        records_found=job.records_found,
        records_new=job.records_new,
        records_duplicate=job.records_duplicate,
        records_error=job.records_error,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message,
    )


@router.get("/jobs", response_model=list[DiscoveryStatusResponse])
async def list_jobs(
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
):
    """List recent discovery jobs."""
    from backend.app.models.source import Source

    stmt = (
        select(SourceJob, Source.name)
        .join(Source, SourceJob.source_id == Source.id)
        .order_by(SourceJob.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    rows = result.all()

    return [
        DiscoveryStatusResponse(
            job_id=job.id,
            source_name=source_name,
            status=job.status.value,
            country_code=job.country_code,
            city=(job.city or '').strip() or None,
            category=job.category_filter,
            records_found=job.records_found,
            records_new=job.records_new,
            records_duplicate=job.records_duplicate,
            records_error=job.records_error,
            started_at=job.started_at,
            completed_at=job.completed_at,
            error_message=job.error_message,
        )
        for job, source_name in rows
    ]
