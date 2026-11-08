"""
Pydantic schemas for Business, BusinessLocation, BusinessCategory models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from backend.app.models.business import BusinessStatus, BusinessType, WebsiteStatus
from backend.app.schemas.types import CountryCode, Email, HttpUrl, Opt, OptionalText, Phone, Slug, Text


# ─── Business Schemas ────────────────────────────────────────────


class BusinessBase(BaseModel):
    """Shared business fields."""

    name: str = Field(..., max_length=500)
    business_type: BusinessType = BusinessType.UNKNOWN
    description: Optional[str] = None
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    website_url: Optional[str] = None
    website_status: WebsiteStatus = WebsiteStatus.UNKNOWN
    social_urls: Optional[dict] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    employee_count_range: Optional[str] = None
    year_founded: Optional[int] = None


class BusinessCreate(BusinessBase):
    """Schema for creating a new business."""

    pass


class BusinessUpdate(BaseModel):
    """Schema for updating a business. All fields optional; limits = DB column sizes."""

    model_config = {"extra": "forbid"}

    name: Optional[Text(500, min_length=1)] = None
    business_type: Optional[BusinessType] = None
    description: OptionalText() = None
    country_code: Opt(CountryCode) = None
    website_url: Opt(HttpUrl) = None
    website_status: Optional[WebsiteStatus] = None
    phone: Opt(Phone) = None
    email: Opt(Email) = None
    status: Optional[BusinessStatus] = None


class LocationResponse(BaseModel):
    """Business location in API responses."""

    id: int
    address_line_1: Optional[str]
    city: Optional[str]
    state_province: Optional[str]
    postal_code: Optional[str]
    country_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_primary: bool

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    """Business category in API responses."""

    id: int
    category_name: str
    normalized_category: str
    industry_group: Optional[str]
    is_primary: bool

    model_config = {"from_attributes": True}


class BusinessResponse(BusinessBase):
    """Schema for business API responses."""

    id: int
    normalized_name: str
    status: BusinessStatus
    discovered_at: datetime
    last_verified_at: Optional[datetime]
    updated_at: datetime
    locations: list[LocationResponse] = []
    categories: list[CategoryResponse] = []

    model_config = {"from_attributes": True}


class BusinessListResponse(BaseModel):
    """Paginated list of businesses."""

    items: list[BusinessResponse]
    total: int
    page: int
    page_size: int
    pages: int


# ─── Discovery Configuration ────────────────────────────────────


class DiscoveryRequest(BaseModel):
    """Schema for triggering a business discovery run."""

    model_config = {"extra": "forbid"}

    source_slug: Slug
    country_code: Opt(CountryCode) = None
    # source_jobs.region / city / category_filter are String(200)
    region: OptionalText(200) = None
    city: OptionalText(200) = None
    category: OptionalText(200) = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius_km: Optional[float] = Field(None, ge=0.1, le=100)
    max_results: int = Field(500, ge=1, le=5000)
    query_params: dict = Field(default_factory=dict)

    @field_validator("source_slug")
    @classmethod
    def no_csv_via_run(cls, value: str) -> str:
        # CSV content must go through /discovery/import-csv, which enforces size and encoding.
        if value == "csv_import":
            raise ValueError("use POST /api/v1/discovery/import-csv to import a CSV file")
        return value

    @field_validator("query_params")
    @classmethod
    def only_known_query_params(cls, value: dict) -> dict:
        # Only documented options; free-form params let callers inject raw SPARQL or CSV text.
        allowed = {"min_confidence"}
        unknown = set(value) - allowed
        if unknown:
            raise ValueError(f"unknown query_params: {sorted(unknown)}; allowed: {sorted(allowed)}")
        if "min_confidence" in value:
            confidence = value["min_confidence"]
            if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                raise ValueError("min_confidence must be a number from 0 to 1")
        return value

    @model_validator(mode="after")
    def coordinates_together(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must be given together")
        return self


class DiscoveryStatusResponse(BaseModel):
    """Status of an ongoing discovery run."""

    job_id: int
    source_name: str
    status: str
    records_found: int
    records_new: int
    records_duplicate: int
    records_error: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

    model_config = {"from_attributes": True}
