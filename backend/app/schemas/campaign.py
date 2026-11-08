"""
Phase 5 — Conversion Engine Pydantic Schemas.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from backend.app.models.campaign import CampaignStatus, DealStage, MessageStatus, ReplyIntent
from backend.app.models.opportunity import ServiceCategory
from backend.app.schemas.types import CountryCode, Opt, OptionalText, Text


class CampaignCreate(BaseModel):
    """Payload to create a new campaign."""

    model_config = {"extra": "forbid"}

    name: Text(200, min_length=2)
    description: OptionalText() = None
    daily_send_limit: int = Field(50, ge=10, le=200)
    target_service_category: Optional[ServiceCategory] = None
    country_code: Opt(CountryCode) = None


class CampaignResponse(BaseModel):
    """Campaign response representation."""

    id: int
    name: str
    description: Optional[str] = None
    status: CampaignStatus
    target_service_category: Optional[str] = None
    country_code: Optional[str] = None
    daily_send_limit: int
    delay_seconds_between_sends: int
    total_leads_count: int
    sent_count: int
    opened_count: int
    replied_count: int
    converted_count: int
    bounced_count: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CampaignListResponse(BaseModel):
    """List of campaigns."""

    items: List[CampaignResponse]
    total: int


class OutreachMessageResponse(BaseModel):
    """Outreach message representation."""

    id: int
    campaign_id: int
    lead_id: int
    recipient_email: str
    sender_mailbox: str
    subject: str
    body_text: str
    status: MessageStatus
    scheduled_at: datetime
    sent_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DealStageUpdateRequest(BaseModel):
    """Update deal position in CRM pipeline."""

    model_config = {"extra": "forbid"}

    stage: DealStage
    estimated_value: Optional[float] = Field(None, ge=0)
    notes: OptionalText() = None


class InboundReplySimulateRequest(BaseModel):
    """Simulate recipient email reply."""

    model_config = {"extra": "forbid"}

    message_id: int = Field(..., ge=1)
    reply_text: Text(None, min_length=2)


class InboundReplyResponse(BaseModel):
    """Classification and pipeline progression response."""

    message_id: int
    intent: ReplyIntent
    confidence: float
    recommended_stage: Optional[str] = None
    action_summary: str
    suppressed: bool


class ConversionFunnelResponse(BaseModel):
    """5-phase end-to-end conversion funnel metrics."""

    funnel: Dict[str, int]
    revenue_won: float
    reply_rate: float
    qualification_rate: float
