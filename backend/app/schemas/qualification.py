"""
Phase 4 — Qualification & Compliance Pydantic Schemas.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from backend.app.models.compliance import (
    LeadStatus,
    LegalBasis,
    LegalFramework,
    OutreachChannel,
    OutreachMode,
)


class LeadResponse(BaseModel):
    """Qualified lead response payload."""

    id: int
    business_id: int
    business_name: str
    business_country: Optional[str] = None
    business_city: Optional[str] = None
    contact_id: int
    contact_name: Optional[str] = None
    contact_email: str
    contact_job_title: Optional[str] = None
    opportunity_id: int
    opportunity_service: str
    composite_score: float
    lead_status: LeadStatus
    outreach_channel: OutreachChannel
    personalized_subject: Optional[str] = None
    personalized_pitch: Optional[str] = None
    validation_passed: bool
    validation_flags: List[str] = []
    legal_framework: Optional[LegalFramework] = None
    outreach_mode: Optional[OutreachMode] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Paginated list of qualified leads."""

    items: List[LeadResponse]
    total: int
    page: int
    page_size: int
    pages: int


class LeadStatusUpdateRequest(BaseModel):
    """Operator status transition request."""

    status: LeadStatus
    notes: Optional[str] = None


class LeadStatsResponse(BaseModel):
    """Aggregated qualification metrics."""

    total_leads: int
    by_status: Dict[str, int]
    avg_composite_score: float
    ready_for_outreach_count: int
    opt_out_count: int


class OptOutCreateRequest(BaseModel):
    """Add recipient to suppression registry."""

    email: str = Field(..., min_length=3, max_length=255)
    domain: Optional[str] = None
    reason: str = "User requested unsubscribe"
    source: str = "MANUAL"


class OptOutResponse(BaseModel):
    """Suppression registry item."""

    id: int
    email: str
    domain: Optional[str] = None
    reason: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True


class OptOutListResponse(BaseModel):
    """Paginated suppression list."""

    items: List[OptOutResponse]
    total: int
    page: int
    page_size: int
    pages: int
