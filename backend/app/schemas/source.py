"""
Pydantic schemas for Source, SourceJob, and SourceRecord models.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from backend.app.models.source import JobStatus, SourceLicense, SourceStatus


# ─── Source Schemas ──────────────────────────────────────────────


class SourceBase(BaseModel):
    """Shared source fields."""

    name: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=100)
    description: Optional[str] = None
    license_type: SourceLicense
    license_url: Optional[str] = None
    license_notes: Optional[str] = None
    attribution_required: bool = False
    attribution_text: Optional[str] = None
    allows_commercial_storage: bool = False
    allows_contact_enrichment: bool = False
    allows_marketing_use: bool = False
    max_cache_duration_hours: Optional[int] = None
    api_base_url: Optional[str] = None
    rate_limit_rpm: int = 30
    adapter_class: str
    status: SourceStatus = SourceStatus.ACTIVE


class SourceCreate(SourceBase):
    """Schema for creating a new source."""

    pass


class SourceUpdate(BaseModel):
    """Schema for updating a source. All fields optional."""

    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    license_type: Optional[SourceLicense] = None
    license_url: Optional[str] = None
    license_notes: Optional[str] = None
    attribution_required: Optional[bool] = None
    allows_commercial_storage: Optional[bool] = None
    allows_contact_enrichment: Optional[bool] = None
    allows_marketing_use: Optional[bool] = None
    rate_limit_rpm: Optional[int] = None
    status: Optional[SourceStatus] = None


class SourceResponse(SourceBase):
    """Schema for source API responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Source Job Schemas ──────────────────────────────────────────


class SourceJobCreate(BaseModel):
    """Schema for creating a discovery job."""

    source_id: int
    query_params: dict = Field(default_factory=dict)
    country_code: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    category_filter: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = None
    bounding_box: Optional[dict] = None


class SourceJobResponse(BaseModel):
    """Schema for source job API responses."""

    id: int
    source_id: int
    query_params: dict
    country_code: Optional[str]
    region: Optional[str]
    city: Optional[str]
    category_filter: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    radius_km: Optional[float]
    status: JobStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    records_found: int
    records_new: int
    records_duplicate: int
    records_error: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Source Record Schemas ───────────────────────────────────────


class SourceRecordResponse(BaseModel):
    """Schema for source record API responses."""

    id: int
    source_id: int
    job_id: Optional[int]
    external_id: str
    external_url: Optional[str]
    name: Optional[str]
    country_code: Optional[str]
    category: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_processed: bool
    fetched_at: datetime

    model_config = {"from_attributes": True}
