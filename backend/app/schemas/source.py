"""
Pydantic schemas for Source, SourceJob, and SourceRecord models.
"""

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from backend.app.models.source import JobStatus, SourceLicense, SourceStatus
from backend.app.schemas.types import HttpUrl, Opt, OptionalText, Slug, Text

# The registry imports adapter_class by name. Accepting any dotted path from a request would let
# a caller make the server import arbitrary modules, so only the built-in adapters are allowed.
KNOWN_ADAPTER_CLASSES = Literal[
    "backend.app.engines.discovery.osm.OSMAdapter",
    "backend.app.engines.discovery.overture.OvertureAdapter",
    "backend.app.engines.discovery.combined.CombinedAdapter",
    "backend.app.engines.discovery.csv_import.CSVImportAdapter",
    "backend.app.engines.discovery.wikidata.WikidataAdapter",
]


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
    """Schema for registering a new source (validated; limits = DB column sizes)."""

    model_config = {"extra": "forbid"}

    name: Text(200, min_length=2)
    slug: Slug
    description: OptionalText() = None
    license_url: Opt(HttpUrl) = None
    license_notes: OptionalText() = None
    attribution_text: OptionalText(500) = None
    max_cache_duration_hours: Optional[int] = Field(None, ge=0)
    api_base_url: Opt(HttpUrl) = None
    # 1000 = the CSV adapter's own ceiling, the highest rate any built-in adapter uses
    rate_limit_rpm: int = Field(30, ge=1, le=1000)
    adapter_class: KNOWN_ADAPTER_CLASSES


class SourceUpdate(BaseModel):
    """Schema for updating a source. All fields optional."""

    model_config = {"extra": "forbid"}

    name: Optional[Text(200, min_length=2)] = None
    description: OptionalText() = None
    license_type: Optional[SourceLicense] = None
    license_url: Opt(HttpUrl) = None
    license_notes: OptionalText() = None
    attribution_required: Optional[bool] = None
    allows_commercial_storage: Optional[bool] = None
    allows_contact_enrichment: Optional[bool] = None
    allows_marketing_use: Optional[bool] = None
    rate_limit_rpm: Optional[int] = Field(None, ge=1, le=1000)
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
