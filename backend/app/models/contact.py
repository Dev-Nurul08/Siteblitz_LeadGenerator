"""
Phase 3 — Contact and Email Verification models.

Tracks business contacts, decision-makers, verified email addresses,
MX status, role classifications, and data provenance.
"""

from datetime import datetime
import enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")


# ─── Enumerations ────────────────────────────────────────────────


class RoleLevel(str, enum.Enum):
    """Hierarchy and seniority classification of a business contact."""

    EXECUTIVE = "EXECUTIVE"  # Founder, Owner, CEO, Managing Director
    MANAGEMENT = "MANAGEMENT"  # General Manager, Operations Manager, Store Manager
    TECHNICAL = "TECHNICAL"  # CTO, Lead Developer, IT Director
    MARKETING = "MARKETING"  # CMO, Marketing Director
    STAFF = "STAFF"  # General staff member
    GENERAL_INBOX = "GENERAL_INBOX"  # info@, hello@, contact@, sales@


class EmailVerificationStatus(str, enum.Enum):
    """Deliverability verification classification."""

    VERIFIED = "VERIFIED"  # Valid syntax, active MX, confirmed mailbox
    UNVERIFIED = "UNVERIFIED"  # Syntax valid, not yet checked via network
    ROLE_BASED = "ROLE_BASED"  # info@, support@, admin@
    CATCH_ALL = "CATCH_ALL"  # Domain accepts all addresses
    DISPOSABLE = "DISPOSABLE"  # Temporary/burner email service
    INVALID = "INVALID"  # Malformed syntax or non-existent domain


# ─── Contact Model ───────────────────────────────────────────────


class Contact(Base):
    """
    Business contact associated with an identified company.
    Strictly follows permitted sources (company website, business registries, public API).
    """

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )

    # Personal / Identity details
    full_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    role_level: Mapped[RoleLevel] = mapped_column(
        Enum(RoleLevel), default=RoleLevel.GENERAL_INBOX
    )

    # Electronic communications
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    email_status: Mapped[EmailVerificationStatus] = mapped_column(
        Enum(EmailVerificationStatus), default=EmailVerificationStatus.UNVERIFIED
    )
    verification_score: Mapped[float] = mapped_column(Float, default=0.5)  # 0.0 to 1.0
    has_valid_mx: Mapped[bool] = mapped_column(Boolean, default=False)
    is_role_based: Mapped[bool] = mapped_column(Boolean, default=False)
    is_disposable: Mapped[bool] = mapped_column(Boolean, default=False)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Provenance / Consent tracking (GDPR/CAN-SPAM audit trail)
    source_method: Mapped[str] = mapped_column(
        String(100), nullable=False, default="website_scrape"
    )  # "website_scrape", "hunter_api", "business_registry", "manual"
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    verification_details: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    business = relationship("Business", back_populates="contacts")

    __table_args__ = (
        Index("ix_contacts_business", "business_id"),
        Index("ix_contacts_email", "email"),
        Index("ix_contacts_status", "email_status"),
        Index("ix_contacts_role", "role_level"),
    )

    def __repr__(self) -> str:
        return (
            f"<Contact(id={self.id}, business_id={self.business_id}, "
            f"email='{self.email}', role='{self.role_level.value}')>"
        )
