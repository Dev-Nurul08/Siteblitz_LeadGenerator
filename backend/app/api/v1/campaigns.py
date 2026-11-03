"""
API v1 — Campaign, Outreach & Conversion Engine Routes (Phase 5).

Exposes campaign orchestration, throttled batch dispatches,
CRM sales pipeline board, reply simulation, and end-to-end conversion analytics.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db_session
from backend.app.models.campaign import Campaign, OutreachMessage
from backend.app.schemas.campaign import (
    CampaignCreate,
    CampaignListResponse,
    CampaignResponse,
    ConversionFunnelResponse,
    DealStageUpdateRequest,
    InboundReplyResponse,
    InboundReplySimulateRequest,
    OutreachMessageResponse,
)
from backend.app.services.campaign_service import CampaignService

router = APIRouter(prefix="/campaigns", tags=["Conversion Engine & Outreach"])


@router.post("", response_model=CampaignResponse)
async def create_campaign(
    payload: CampaignCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Create a new outbound sales campaign with deliverability safeguards.
    """
    service = CampaignService(session)
    campaign = await service.create_campaign(
        name=payload.name,
        description=payload.description,
        daily_send_limit=payload.daily_send_limit,
        target_service_category=payload.target_service_category,
        country_code=payload.country_code,
    )
    return campaign


@router.get("", response_model=CampaignListResponse)
async def list_campaigns(
    session: AsyncSession = Depends(get_db_session),
):
    """
    List all campaigns with aggregated performance metrics.
    """
    stmt = select(Campaign).order_by(Campaign.created_at.desc())
    rows = (await session.execute(stmt)).scalars().all()
    return CampaignListResponse(
        items=[CampaignResponse.from_orm(c) for c in rows],
        total=len(rows),
    )


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get detailed metrics for a specific campaign.
    """
    stmt = select(Campaign).where(Campaign.id == campaign_id)
    c = (await session.execute(stmt)).scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=404, detail=f"Campaign #{campaign_id} not found.")
    return c


@router.post("/{campaign_id}/enroll")
async def enroll_leads(
    campaign_id: int,
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Enroll qualified leads into the campaign and generate scheduled dispatch slots.
    """
    service = CampaignService(session)
    result = await service.enroll_qualified_leads(campaign_id=campaign_id, limit=limit)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{campaign_id}/dispatch")
async def dispatch_next_batch(
    campaign_id: int,
    batch_size: int = Query(10, ge=1, le=50),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Dispatch next due batch of scheduled messages with multi-mailbox rotation.
    """
    service = CampaignService(session)
    result = await service.dispatch_next_batch(campaign_id=campaign_id, batch_size=batch_size)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/pipeline/crm")
async def get_crm_pipeline(
    session: AsyncSession = Depends(get_db_session),
):
    """
    Fetch all active deals grouped by pipeline stage for the Kanban sales board.
    """
    service = CampaignService(session)
    return await service.get_crm_pipeline()


@router.patch("/pipeline/crm/{deal_id}")
async def update_deal_stage(
    deal_id: int,
    payload: DealStageUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Move a deal across sales pipeline stages (e.g. Contacted -> Meeting Scheduled -> Won).
    """
    service = CampaignService(session)
    result = await service.update_deal_stage(
        deal_id=deal_id,
        stage=payload.stage,
        estimated_value=payload.estimated_value,
        notes=payload.notes,
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/replies/simulate", response_model=InboundReplyResponse)
async def simulate_inbound_reply(
    payload: InboundReplySimulateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Simulate an inbound email reply to test sentiment analysis, suppression, and CRM progression.
    """
    service = CampaignService(session)
    result = await service.handle_inbound_reply(
        message_id=payload.message_id,
        reply_text=payload.reply_text,
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return InboundReplyResponse(
        message_id=result["message_id"],
        intent=result["intent"],
        confidence=result["confidence"],
        recommended_stage=result["recommended_stage"],
        action_summary=result["action_summary"],
        suppressed=result["suppressed"],
    )


@router.get("/analytics/funnel", response_model=ConversionFunnelResponse)
async def get_conversion_funnel(
    session: AsyncSession = Depends(get_db_session),
):
    """
    End-to-end 5-phase conversion funnel analytics.
    """
    service = CampaignService(session)
    return await service.get_conversion_funnel()
