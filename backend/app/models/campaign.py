"""
Phase 5 — Conversion Engine Models.

Tracks outbound campaigns, throttled dispatch queues, sender mailbox rotation,
CRM sales pipeline stages, and conversion analytics.
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


class CampaignStatus(str, enum.Enum):
    """Campaign execution lifecycle state."""

    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class MessageStatus(str, enum.Enum):
    """Outreach message dispatch and delivery state."""

    QUEUED = "QUEUED"
    SENDING = "SENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    OPENED = "OPENED"
    REPLIED = "REPLIED"
    BOUNCED = "BOUNCED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class DealStage(str, enum.Enum):
    """CRM sales pipeline stages for converted prospects."""

    PROSPECT = "PROSPECT"
    CONTACTED = "CONTACTED"
    MEETING_SCHEDULED = "MEETING_SCHEDULED"
    PROPOSAL_SENT = "PROPOSAL_SENT"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"


class ReplyIntent(str, enum.Enum):
    """Inbound email classification category."""

    INTERESTED = "INTERESTED"
    NOT_INTERESTED = "NOT_INTERESTED"
    UNSUBSCRIBE_REQUEST = "UNSUBSCRIBE_REQUEST"
    OUT_OF_OFFICE = "OUT_OF_OFFICE"
    GENERAL_INQUIRY = "GENERAL_INQUIRY"
    UNKNOWN = "UNKNOWN"


class EventType(str, enum.Enum):
    """Conversion funnel analytics event."""

    CAMPAIGN_STARTED = "CAMPAIGN_STARTED"
    MESSAGE_SENT = "MESSAGE_SENT"
    MESSAGE_OPENED = "MESSAGE_OPENED"
    REPLY_RECEIVED = "REPLY_RECEIVED"
    DEAL_CREATED = "DEAL_CREATED"
    DEAL_STAGE_CHANGED = "DEAL_STAGE_CHANGED"
    UNSUBSCRIBE = "UNSUBSCRIBE"


# ─── Models ──────────────────────────────────────────────────────


class Campaign(Base):
    """
    Outbound campaign managing throttled outreach batches.
    """

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[CampaignStatus] = mapped_column(
        Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False, index=True
    )

    # Audience targeting criteria
    target_service_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Deliverability Throttling Safeguards (prevents mailbox burn)
    daily_send_limit: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    delay_seconds_between_sends: Mapped[int] = mapped_column(Integer, default=180, nullable=False)
    send_window_start_hour: Mapped[int] = mapped_column(Integer, default=9, nullable=False)  # 9 AM
    send_window_end_hour: Mapped[int] = mapped_column(Integer, default=17, nullable=False)  # 5 PM

    # Aggregated performance stats
    total_leads_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    opened_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    replied_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    converted_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bounced_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    messages = relationship("OutreachMessage", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Campaign id={self.id} name='{self.name}' status={self.status.value}>"


class OutreachMessage(Base):
    """
    Individual email dispatch scheduled and sent to a qualified lead.
    """

    __tablename__ = "outreach_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    campaign_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), index=True, nullable=False
    )
    lead_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("qualified_leads.id", ondelete="CASCADE"), index=True, nullable=False
    )
    contact_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("contacts.id", ondelete="CASCADE"), index=True, nullable=False
    )
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False
    )

    # Routing and Identity
    sender_mailbox: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(300), nullable=False)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[MessageStatus] = mapped_column(
        Enum(MessageStatus), default=MessageStatus.QUEUED, nullable=False, index=True
    )

    # Dispatch tracking
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    replied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    campaign = relationship("Campaign", back_populates="messages")
    lead = relationship("QualifiedLead")
    contact = relationship("Contact")
    business = relationship("Business")

    __table_args__ = (
        Index("ix_outreach_campaign_status", "campaign_id", "status"),
        Index("ix_outreach_scheduled", "scheduled_at", "status"),
    )

    def __repr__(self) -> str:
        return f"<OutreachMessage id={self.id} recipient='{self.recipient_email}' status={self.status.value}>"


class CRMDeal(Base):
    """
    Sales pipeline opportunity created when a lead is contacted or replies.
    """

    __tablename__ = "crm_deals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lead_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("qualified_leads.id", ondelete="CASCADE"), index=True, nullable=False
    )
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    stage: Mapped[DealStage] = mapped_column(
        Enum(DealStage), default=DealStage.PROSPECT, nullable=False, index=True
    )
    estimated_value: Mapped[float] = mapped_column(Float, default=5000.0, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
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
    lead = relationship("QualifiedLead")
    business = relationship("Business")

    def __repr__(self) -> str:
        return f"<CRMDeal id={self.id} title='{self.title}' stage={self.stage.value} value=${self.estimated_value}>"


class AnalyticsEvent(Base):
    """
    Audit log of conversion and engagement events.
    """

    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType), nullable=False, index=True)
    campaign_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    lead_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    metadata_payload: Mapped[dict] = mapped_column(JSON_TYPE, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<AnalyticsEvent type={self.event_type.value} created_at={self.created_at}>"
