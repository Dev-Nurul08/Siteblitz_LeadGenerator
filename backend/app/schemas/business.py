"""
Pydantic schemas for Business, BusinessLocation, BusinessCategory models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.app.models.business import BusinessStatus, BusinessType, WebsiteStatus


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
    """Schema for updating a business. All fields optional."""

    name: Optional[str] = Field(None, max_length=500)
    business_type: Optional[BusinessType] = None
    description: Optional[str] = None
    country_code: Optional[str] = None
    website_url: Optional[str] = None
    website_status: Optional[WebsiteStatus] = None
    phone: Optional[str] = None
    email: Optional[str] = None
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

    source_slug: str
    country_code: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = Field(None, ge=0.1, le=100)
    max_results: int = Field(500, ge=1, le=5000)
    query_params: dict = Field(default_factory=dict)


class DiscoveryStatusResponse(BaseModel):
    """Status of an ongoing discovery run."""

    job_id: int
    source_name: str
    status: str
    city: Optional[str] = None
    country_code: Optional[str] = None
    category: Optional[str] = None
    records_found: int
    records_new: int
    records_duplicate: int
    records_error: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

    model_config = {"from_attributes": True}
