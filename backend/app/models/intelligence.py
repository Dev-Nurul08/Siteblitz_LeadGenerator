"""
Phase 2 — Website Intelligence models (spec: docs/spec/website-intelligence.md).

Separate tables (not new columns on `businesses`) so an existing database gets them from
`create_all` without a migration. The verdict is always recomputed from the stored checks;
checks are never edited, so "why did this change?" can be answered later.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, Integer, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")


class WebsiteVerdict(str, enum.Enum):
    OWN_SITE_VERIFIED = "OWN_SITE_VERIFIED"
    SOCIAL_ONLY_VERIFIED = "SOCIAL_ONLY_VERIFIED"
    NO_SITE_VERIFIED = "NO_SITE_VERIFIED"
    SITE_DOWN_CONFIRMED = "SITE_DOWN_CONFIRMED"
    UNKNOWN = "UNKNOWN"
    SKIP = "SKIP"


class EvidenceConfidence(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class LeadTier(str, enum.Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"
    REVIEW = "REVIEW"
    SKIP = "SKIP"


class OutreachReadiness(str, enum.Enum):
    READY = "READY"
    RESEARCH = "RESEARCH"
    BLOCKED = "BLOCKED"


class CheckType(str, enum.Enum):
    SOURCE_TAG = "SOURCE_TAG"
    SOCIAL_LINK = "SOCIAL_LINK"
    LINK_IN_BIO = "LINK_IN_BIO"
    DOMAIN_GUESS = "DOMAIN_GUESS"
    SITE_FETCH = "SITE_FETCH"
    SEARCH = "SEARCH"
    MANUAL_SEARCH = "MANUAL_SEARCH"
    MANUAL_ACTIVITY = "MANUAL_ACTIVITY"
    SKIP_RULE = "SKIP_RULE"
    # Email engine v2 (E1): a 390 px phone render of the homepage (scripts/render_check.cjs).
    # outcome zoomed_out | fits | error; detail = inner_width, final_url, screenshot path.
    PHONE_RENDER = "PHONE_RENDER"


class FounderLabel(str, enum.Enum):
    CORRECT = "CORRECT"
    WRONG = "WRONG"
    UNSURE = "UNSURE"


class WebsiteCheck(Base):
    """One observation made while deciding whether a business has a website (append-only)."""

    __tablename__ = "website_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    check_type: Mapped[CheckType] = mapped_column(Enum(CheckType), nullable=False)
    target: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    # e.g. found / none / matched / no_match / ok / protected / failed / blocked / social / active
    outcome: Mapped[str] = mapped_column(String(50), nullable=False)
    detail: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_website_checks_business", "business_id", "check_type"),)


class SocialIdentity(Base):
    """A social profile linked to a business and how sure we are it is theirs."""

    __tablename__ = "social_identities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    platform: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    evidence_source: Mapped[str] = mapped_column(String(100), nullable=False)
    # discovered | confirmed | rejected
    match_status: Mapped[str] = mapped_column(String(20), nullable=False, default="discovered")
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_social_identities_business", "business_id"),)


class LeadAssessment(Base):
    """Current verdict, score and tier of one business (1:1), plus the founder's label."""

    __tablename__ = "lead_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    website_verdict: Mapped[WebsiteVerdict] = mapped_column(Enum(WebsiteVerdict), nullable=False)
    evidence_confidence: Mapped[EvidenceConfidence] = mapped_column(
        Enum(EvidenceConfidence), nullable=False
    )
    need_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # None = unscored
    tier: Mapped[LeadTier] = mapped_column(Enum(LeadTier), nullable=False)
    outreach_readiness: Mapped[OutreachReadiness] = mapped_column(
        Enum(OutreachReadiness), nullable=False
    )
    # {"website_gap": 60, "business_problem": 0, "activity": 10, "service_fit": 10}
    score_breakdown: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    # [{"points": 60, "part": "website_gap", "text": "...", "check_ids": [3, 4]}]
    reasons: Mapped[Optional[list]] = mapped_column(JSON_TYPE, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    label: Mapped[Optional[FounderLabel]] = mapped_column(Enum(FounderLabel), nullable=True)
    # ownership | activity | identity | exclusion | need (only when label = WRONG)
    label_wrong_part: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    label_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    labeled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    business = relationship("Business")

    __table_args__ = (
        Index("ix_lead_assessments_tier", "tier"),
        Index("ix_lead_assessments_verdict", "website_verdict"),
    )


class ContactLog(Base):
    """A contact attempt the founder made himself (sending from the app is off)."""

    __tablename__ = "contact_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    channel: Mapped[str] = mapped_column(String(20), nullable=False)   # phone|email|social|form|visit
    outcome: Mapped[str] = mapped_column(String(30), nullable=False)   # interested|not_now|no_reply|do_not_contact|other
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_contact_logs_business", "business_id"),)
