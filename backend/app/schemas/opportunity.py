"""
Pydantic schemas for Opportunities and Website Audits (Phase 2).
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from backend.app.models.opportunity import (
    OpportunityPriority,
    OpportunityStatus,
    ServiceCategory,
)


class WebsiteAuditResponse(BaseModel):
    """Website audit details."""

    id: int
    business_id: int
    url_analyzed: str
    final_url: Optional[str] = None
    is_reachable: bool
    http_status: Optional[int] = None
    has_ssl: bool
    load_time_seconds: Optional[float] = None
    is_mobile_responsive: bool
    has_viewport_meta: bool
    detected_cms: Optional[str] = None
    detected_frameworks: Optional[dict] = None
    has_ecommerce: bool
    has_online_booking: bool
    has_contact_form: bool
    has_analytics: bool
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    headings_summary: Optional[dict] = None
    emails_found: Optional[dict] = None
    phones_found: Optional[dict] = None
    social_links_found: Optional[dict] = None
    audited_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OpportunityResponse(BaseModel):
    """Qualified sales opportunity."""

    id: int
    business_id: int
    audit_id: Optional[int] = None
    service_category: ServiceCategory
    title: str
    summary: str
    score: float
    confidence: float
    priority: OpportunityPriority
    status: OpportunityStatus
    evidence: dict
    pitch_angles: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    # Include business basic details if loaded
    business_name: Optional[str] = None
    business_country: Optional[str] = None
    business_website: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OpportunityUpdate(BaseModel):
    """Update opportunity status, priority, or score."""

    status: Optional[OpportunityStatus] = None
    priority: Optional[OpportunityPriority] = None
    score: Optional[float] = None


class OpportunityListResponse(BaseModel):
    """Paginated list of opportunities."""

    items: list[OpportunityResponse]
    total: int
    page: int
    page_size: int
    pages: int


class OpportunityStatsResponse(BaseModel):
    """Opportunity summary metrics for dashboard."""

    total_opportunities: int
    by_category: dict[str, int]
    by_priority: dict[str, int]
    by_status: dict[str, int]
    average_score: float
