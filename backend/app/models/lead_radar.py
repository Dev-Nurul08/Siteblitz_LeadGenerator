"""
Lead-Radar SQLAlchemy Database Model.

Stores the persistent 6-fact evaluation, condition states, matched sales recipes,
pitch copy, revenue ranges, absence certificates, and 6-tier deterministic ranking.
"""

from datetime import datetime
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
from backend.app.engines.lead_radar.types import (
    Authority,
    Availability,
    CustomerTaskCovered,
    OwnedPresence,
    Segment,
    TaskQuality,
    BuyingStatus,
)

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")


class LeadRadarEvaluation(Base):
    """
    Persistent Lead-Radar Strategy evaluation for a business entity.
    """
    __tablename__ = "lead_radar_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    # ─── SECTION 2: THE SIX SEPARATE FACTS ───────────────────────
    owned_presence: Mapped[OwnedPresence] = mapped_column(
        Enum(OwnedPresence), default=OwnedPresence.UNRESOLVED
    )
    availability: Mapped[Availability] = mapped_column(
        Enum(Availability), default=Availability.UNKNOWN
    )
    customer_task_covered: Mapped[CustomerTaskCovered] = mapped_column(
        Enum(CustomerTaskCovered), default=CustomerTaskCovered.UNKNOWN
    )
    task_quality: Mapped[TaskQuality] = mapped_column(
        Enum(TaskQuality), default=TaskQuality.NOT_TESTED
    )
    buying_status: Mapped[BuyingStatus] = mapped_column(
        Enum(BuyingStatus), default=BuyingStatus.UNKNOWN
    )
    authority: Mapped[Authority] = mapped_column(
        Enum(Authority), default=Authority.UNRESOLVED
    )

    identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    currently_active: Mapped[bool] = mapped_column(Boolean, default=False)
    absence_search_done: Mapped[bool] = mapped_column(Boolean, default=False)
    repeated_failure: Mapped[bool] = mapped_column(Boolean, default=False)

    # ─── SECTION 4: STRATEGIC SEGMENTATION & WARM CONTEXT ───────
    segment: Mapped[Segment] = mapped_column(
        Enum(Segment), default=Segment.UNKNOWN
    )
    warm_context: Mapped[bool] = mapped_column(Boolean, default=False)

    # ─── CONDITIONS EVALUATED (G1-G7, W1-W16, I1-I8, D1-D12, C1-C6, J1-J2)
    conditions_met: Mapped[Optional[list]] = mapped_column(JSON_TYPE, nullable=True)
    condition_results: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)

    # ─── RECIPES MATCHED (R1 - R17) ──────────────────────────────
    matched_recipes: Mapped[Optional[list]] = mapped_column(JSON_TYPE, nullable=True)
    primary_recipe_id: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # ─── SECTION 5: FACTUAL PITCH ────────────────────────────────
    pitch_opening_fact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pitch_angle: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pitch_never_say: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pitch_recommended_solution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ─── SECTION 7: REVENUE ESTIMATE ─────────────────────────────
    revenue_category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    revenue_confidence: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    min_annual_revenue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_annual_revenue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    revenue_currency: Mapped[str] = mapped_column(String(10), default="USD")
    revenue_formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ─── SECTION 10: ABSENCE CERTIFICATE ─────────────────────────
    absence_certificate_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    absence_certificate_hash: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    absence_certificate_data: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)

    # ─── SECTION 8: 6-TIER DETERMINISTIC RANKING ─────────────────
    rank_opportunity_class: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rank_evidence_quality: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rank_task_severity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rank_demand_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rank_authority_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    why_this_business: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_this_project: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_now: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    what_is_unknown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # Relationships
    business = relationship("Business", backref="lead_radar_evaluation")

    __table_args__ = (
        Index("ix_lead_radar_segment", "segment"),
        Index("ix_lead_radar_warm", "warm_context"),
        Index("ix_lead_radar_recipe", "primary_recipe_id"),
        Index("ix_lead_radar_created", "created_at"),
    )

