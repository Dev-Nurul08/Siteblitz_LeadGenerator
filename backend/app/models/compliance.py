"""
Phase 4 — Qualification and Legal Compliance Models.

Defines international compliance frameworks (CAN-SPAM, GDPR, PECR, CASL, Spam Act),
suppression and opt-out registries, evaluation audits, and final Qualified Leads.
"""

from datetime import datetime, timezone
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


class LegalFramework(str, enum.Enum):
    """International outbound marketing legal framework."""

    CAN_SPAM = "CAN_SPAM"  # United States (FTC CAN-SPAM Act)
    GDPR_UK = "GDPR_UK"  # United Kingdom (PECR + UK GDPR)
    GDPR_EU = "GDPR_EU"  # European Union (GDPR + ePrivacy)
    CASL = "CASL"  # Canada Anti-Spam Legislation
    AUSTRALIA_SPAM_ACT = "AUSTRALIA_SPAM_ACT"  # Australia Spam Act 2003
    GENERAL_B2B = "GENERAL_B2B"  # Rest of world default conservative standard


class OutreachMode(str, enum.Enum):
    """Execution authorization level for lead outreach."""

    AUTOMATED = "AUTOMATED"  # Approved for automated campaign queue
    MANUAL_REVIEW_ONLY = "MANUAL_REVIEW_ONLY"  # Requires human compliance approval
    PROHIBITED = "PROHIBITED"  # Strictly prohibited (opted out, banned jurisdiction, undeliverable)


class LegalBasis(str, enum.Enum):
    """Lawful basis for initiating B2B sales outreach."""

    LEGITIMATE_INTEREST = "LEGITIMATE_INTEREST"  # GDPR Art. 6(1)(f) B2B relevant interest
    CONSPICUOUSLY_PUBLISHED_B2B = "CONSPICUOUSLY_PUBLISHED_B2B"  # CASL / AU Spam Act published email
    OPT_OUT_REGIME = "OPT_OUT_REGIME"  # US CAN-SPAM affirmative opt-out with postal address
    EXPRESS_CONSENT = "EXPRESS_CONSENT"  # Direct inbound / trade show consent
    NONE = "NONE"  # No lawful basis identified


class LeadStatus(str, enum.Enum):
    """Status in the qualification lifecycle."""

    QUALIFIED = "QUALIFIED"  # Passed opportunity, deliverability, and compliance checks
    NEEDS_REVIEW = "NEEDS_REVIEW"  # Borderline score or strict jurisdiction requiring manual sign-off
    DISQUALIFIED = "DISQUALIFIED"  # Rejected due to risk, opt-out, or missing signals
    READY_FOR_OUTREACH = "READY_FOR_OUTREACH"  # Fully verified and AI-personalized; approved for Phase 5
    CONTACTED = "CONTACTED"  # Moved to active Phase 5 campaign
    CONVERTED = "CONVERTED"  # Converted to client meeting or deal


class OutreachChannel(str, enum.Enum):
    """Recommended communication medium."""

    EMAIL = "EMAIL"
    LINKEDIN = "LINKEDIN"
    PHONE = "PHONE"


# ─── Models ──────────────────────────────────────────────────────


class OptOut(Base):
    """
    Suppression list registry of opted-out email addresses and domains.
    Must be checked before ANY outreach evaluation or message sending.
    """

    __tablename__ = "opt_outs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    domain: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    reason: Mapped[str] = mapped_column(String(255), default="User requested unsubscribe", nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="UNSUBSCRIBE_LINK", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<OptOut email={self.email} source={self.source}>"


class ComplianceEvaluation(Base):
    """
    Formal compliance audit log per business/contact.
    Documents the jurisdiction rules, lawful basis, risk score, and required checklist.
    """

    __tablename__ = "compliance_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    contact_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("contacts.id", ondelete="SET NULL"), index=True, nullable=True
    )
    opportunity_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("opportunities.id", ondelete="SET NULL"), index=True, nullable=True
    )

    country_code: Mapped[str] = mapped_column(String(3), index=True, nullable=False)
    legal_framework: Mapped[LegalFramework] = mapped_column(
        Enum(LegalFramework), default=LegalFramework.GENERAL_B2B, nullable=False
    )
    is_outreach_permitted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    outreach_mode: Mapped[OutreachMode] = mapped_column(
        Enum(OutreachMode), default=OutreachMode.MANUAL_REVIEW_ONLY, nullable=False
    )
    legal_basis: Mapped[LegalBasis] = mapped_column(
        Enum(LegalBasis), default=LegalBasis.NONE, nullable=False
    )

    # Risk score between 0.0 (safest) and 1.0 (highest regulatory risk)
    risk_score: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)

    # Audited conditions: e.g. {"physical_address_required": true, "opt_out_link_mandatory": true}
    requirements_checklist: Mapped[dict] = mapped_column(JSON_TYPE, default=dict, nullable=False)
    evaluation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    business = relationship("Business", backref="compliance_evaluations")
    contact = relationship("Contact", backref="compliance_evaluations")
    opportunity = relationship("Opportunity", backref="compliance_evaluations")

    __table_args__ = (
        Index("ix_comp_eval_business_country", "business_id", "country_code"),
        Index("ix_comp_eval_permitted_mode", "is_outreach_permitted", "outreach_mode"),
    )

    def __repr__(self) -> str:
        return f"<ComplianceEvaluation id={self.id} country={self.country_code} mode={self.outreach_mode}>"


class QualifiedLead(Base):
    """
    A fully qualified, scored lead with an AI-generated, safety-validated pitch.
    Bridges between the research/evaluation phases and the Phase 5 Conversion Engine.
    """

    __tablename__ = "qualified_leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    contact_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("contacts.id", ondelete="CASCADE"), index=True, nullable=False
    )
    opportunity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("opportunities.id", ondelete="CASCADE"), index=True, nullable=False
    )
    compliance_evaluation_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("compliance_evaluations.id", ondelete="SET NULL"), index=True, nullable=True
    )

    # Composite Lead Score (0 - 100) combining Opportunity + Contact Deliverability + Regulatory Safety
    composite_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    lead_status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus), default=LeadStatus.QUALIFIED, nullable=False, index=True
    )
    outreach_channel: Mapped[OutreachChannel] = mapped_column(
        Enum(OutreachChannel), default=OutreachChannel.EMAIL, nullable=False
    )

    # AI Personalized Content tailored to digital-service signals
    personalized_subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    personalized_pitch: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pitch_template_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Output Safety & Compliance Verification
    validation_passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validation_flags: Mapped[list] = mapped_column(JSON_TYPE, default=list, nullable=False)

    last_contacted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    business = relationship("Business", backref="qualified_leads")
    contact = relationship("Contact", backref="qualified_leads")
    opportunity = relationship("Opportunity", backref="qualified_leads")
    compliance_evaluation = relationship("ComplianceEvaluation", backref="qualified_leads")

    __table_args__ = (
        Index("ix_qual_leads_score_status", "composite_score", "lead_status"),
    )

    def __repr__(self) -> str:
        return f"<QualifiedLead id={self.id} score={self.composite_score} status={self.lead_status}>"
