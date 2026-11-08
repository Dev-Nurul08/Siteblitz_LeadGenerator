"""
Pydantic schemas for Contact Enrichment and Email Verification (Phase 3).
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

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
    verification_details: Optional[dict] = None
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
    is_free_email: bool = False
    has_valid_mx: bool
    verification_score: float
    domain: str
    mx_records: list[str] = []
    mail_provider: Optional[str] = None
    suggested_correction: Optional[str] = None


class VerifyPhoneRequest(BaseModel):
    """Request to validate and format a business phone number."""

    phone: str
    country_code: str = "US"


class VerifyPhoneResponse(BaseModel):
    """Result of phone verification and formatting."""

    raw_phone: str
    formatted_phone: Optional[str] = None
    is_valid: bool
    country_code: Optional[str] = None
    phone_type: str = "UNKNOWN"


class DomainContactSearchRequest(BaseModel):
    """Request to discover contacts on-demand for any domain/website."""

    domain_or_url: str


class DomainContactSearchResponse(BaseModel):
    """On-demand discovery of contacts for a domain."""

    query: str
    contacts_found: int
    contacts: list[dict] = []


class ContactStatsResponse(BaseModel):
    """Aggregated contact enrichment statistics."""

    total_contacts: int
    by_status: dict[str, int]
    by_role: dict[str, int]
    verified_rate: float
