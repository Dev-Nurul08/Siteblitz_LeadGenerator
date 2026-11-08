"""
Pydantic schemas for Contact Enrichment and Email Verification (Phase 3).
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

from backend.app.models.contact import EmailVerificationStatus, RoleLevel
from backend.app.schemas.types import Text


class ContactResponse(BaseModel):
    """Business contact response schema."""

    id: int
    business_id: int
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    role_level: RoleLevel
    email: str
    email_status: EmailVerificationStatus
    verification_score: float
    has_valid_mx: bool
    is_role_based: bool
    is_disposable: bool
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    source_method: str
    source_url: Optional[str] = None
    verified_at: Optional[datetime] = None
    created_at: datetime

    # Business context
    business_name: Optional[str] = None
    business_country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ContactCreate(BaseModel):
    """Schema for adding a manual contact."""

    business_id: int
    email: str
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None


class ContactListResponse(BaseModel):
    """Paginated list of business contacts."""

    items: list[ContactResponse]
    total: int
    page: int
    page_size: int
    pages: int


class VerifyEmailRequest(BaseModel):
    """Request to verify an arbitrary email address (format is judged by the verifier itself)."""

    model_config = {"extra": "forbid"}

    email: Text(320, min_length=3)


class VerifyEmailResponse(BaseModel):
    """Result of standalone email verification."""

    email: str
    status: EmailVerificationStatus
    is_valid_syntax: bool
    is_disposable: bool
    is_role_based: bool
    has_valid_mx: bool
    verification_score: float
    domain: str
    mx_records: list[str]


class ContactStatsResponse(BaseModel):
    """Aggregated contact enrichment statistics."""

    total_contacts: int
    by_status: dict[str, int]
    by_role: dict[str, int]
    verified_rate: float
