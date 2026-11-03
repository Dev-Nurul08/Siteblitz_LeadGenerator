"""
Phase 2 — Opportunity and Website Audit models.

Tracks website technical audits, digital-need signals, agency opportunity
classification, and multi-factor prioritization scoring.
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


class ServiceCategory(str, enum.Enum):
    """Agency service division matching detected business needs."""

    NEW_WEBSITE = "NEW_WEBSITE"  # Business has no website or only social media
    WEBSITE_REDESIGN = "WEBSITE_REDESIGN"  # Obsolete design, not mobile friendly, SSL issues
    MOBILE_APP = "MOBILE_APP"  # High-touch business (dining, clinic, fitness) needing app
    ECOMMERCE_EXPANSION = "ECOMMERCE_EXPANSION"  # Retail/catalog needing digital store
    ONLINE_BOOKING = "ONLINE_BOOKING"  # Appointment-based business without digital scheduler
    SEO_PERFORMANCE = "SEO_PERFORMANCE"  # Critical performance, metadata, or heading flaws
    CUSTOM_WEB_APP = "CUSTOM_WEB_APP"  # Complex workflow/portal development need


class OpportunityPriority(str, enum.Enum):
    """Urgency / commercial prioritization level."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class OpportunityStatus(str, enum.Enum):
    """Lifecycle stage of an identified opportunity."""

    IDENTIFIED = "IDENTIFIED"
    EVALUATING = "EVALUATING"
    QUALIFIED = "QUALIFIED"
    DISQUALIFIED = "DISQUALIFIED"
    OUTREACH_PENDING = "OUTREACH_PENDING"
    IN_OUTREACH = "IN_OUTREACH"
    CONVERTED = "CONVERTED"


# ─── Website Audit Model ─────────────────────────────────────────


class WebsiteAudit(Base):
    """
    Detailed technical audit of a business's online presence.
    Stores objective signals (performance, CMS, responsiveness, SEO basics).
    """

    __tablename__ = "website_audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )

    # Resolution & Reachability
    url_analyzed: Mapped[str] = mapped_column(String(1000), nullable=False)
    final_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    is_reachable: Mapped[bool] = mapped_column(Boolean, default=False)
    http_status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    has_ssl: Mapped[bool] = mapped_column(Boolean, default=False)
    load_time_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Mobile Responsiveness
    is_mobile_responsive: Mapped[bool] = mapped_column(Boolean, default=False)
    has_viewport_meta: Mapped[bool] = mapped_column(Boolean, default=False)

    # Tech Stack & CMS Detection
    detected_cms: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    detected_frameworks: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    # e.g., {"libraries": ["jquery", "bootstrap"], "analytics": ["google_tag"]}

    # Capabilities & Features
    has_ecommerce: Mapped[bool] = mapped_column(Boolean, default=False)
    has_online_booking: Mapped[bool] = mapped_column(Boolean, default=False)
    has_contact_form: Mapped[bool] = mapped_column(Boolean, default=False)
    has_analytics: Mapped[bool] = mapped_column(Boolean, default=False)

    # SEO & Content Signals
    meta_title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    headings_summary: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    # e.g., {"h1_count": 1, "h2_count": 4}

    # Signals found on page
    emails_found: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    phones_found: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    social_links_found: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)

    # Raw audit payload & errors
    raw_audit_data: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    audit_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    audited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    business = relationship("Business", back_populates="audits")

    __table_args__ = (
        Index("ix_website_audits_business", "business_id"),
        Index("ix_website_audits_reachable", "is_reachable"),
    )

    def __repr__(self) -> str:
        return (
            f"<WebsiteAudit(id={self.id}, business_id={self.business_id}, "
            f"reachable={self.is_reachable}, cms='{self.detected_cms}')>"
        )


# ─── Opportunity Model ───────────────────────────────────────────


class Opportunity(Base):
    """
    Qualified digital-service opportunity matched to an agency capability.
    Synthesizes audit findings, business type, and market fit into a
    prioritized sales opportunity.
    """

    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    audit_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("website_audits.id", ondelete="SET NULL"), nullable=True
    )

    # Opportunity Classification
    service_category: Mapped[ServiceCategory] = mapped_column(
        Enum(ServiceCategory), nullable=False
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Opportunity Scoring (0 to 100)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)  # 0.0 to 1.0
    priority: Mapped[OpportunityPriority] = mapped_column(
        Enum(OpportunityPriority), default=OpportunityPriority.MEDIUM
    )
    status: Mapped[OpportunityStatus] = mapped_column(
        Enum(OpportunityStatus), default=OpportunityStatus.IDENTIFIED
    )

    # Evidence & Value Proposition
    evidence: Mapped[dict] = mapped_column(JSON_TYPE, nullable=False, default=dict)
    # e.g., {"reasons": ["No mobile viewport", "Slow load 5.2s"], "estimated_impact": "high"}
    pitch_angles: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    # Talking points tailored for agency sales reps

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    business = relationship("Business", back_populates="opportunities")
    audit = relationship("WebsiteAudit")

    __table_args__ = (
        Index("ix_opportunities_business", "business_id"),
        Index("ix_opportunities_service", "service_category"),
        Index("ix_opportunities_score", "score"),
        Index("ix_opportunities_priority", "priority"),
        Index("ix_opportunities_status", "status"),
    )

    def __repr__(self) -> str:
        return (
            f"<Opportunity(id={self.id}, business_id={self.business_id}, "
            f"service={self.service_category.value}, score={self.score})>"
        )
