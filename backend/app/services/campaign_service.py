"""
Phase 5 — Conversion & Campaign Service.

Orchestrates campaign scheduling, throttled multi-mailbox delivery,
inbound reply intent handling, CRM pipeline updates, and funnel analytics.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.engines.conversion.replies import ReplyIntentClassifier
from backend.app.engines.conversion.scheduler import CampaignScheduler
from backend.app.engines.conversion.sender import MultiMailboxSender
from backend.app.models.business import Business
from backend.app.models.campaign import (
    AnalyticsEvent,
    Campaign,
    CampaignStatus,
    CRMDeal,
    DealStage,
    EventType,
    MessageStatus,
    OutreachMessage,
    ReplyIntent,
)
from backend.app.models.compliance import LeadStatus, OptOut, QualifiedLead
from backend.app.models.contact import Contact
from backend.app.models.opportunity import Opportunity
from backend.app.services.qualification_service import QualificationService


class CampaignService:
    """
    Manages outbound marketing campaigns, throttled dispatch queues,
    and CRM sales pipeline lifecycle.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.scheduler = CampaignScheduler()
        self.sender = MultiMailboxSender()
        self.reply_classifier = ReplyIntentClassifier()

    async def create_campaign(
        self,
        name: str,
        description: Optional[str] = None,
        daily_send_limit: int = 50,
        target_service_category: Optional[str] = None,
        country_code: Optional[str] = None,
    ) -> Campaign:
        """
        Create a new sales campaign.
        """
        campaign = Campaign(
            name=name,
            description=description,
            daily_send_limit=daily_send_limit,
            target_service_category=target_service_category,
            country_code=country_code,
            status=CampaignStatus.DRAFT,
        )
        self.session.add(campaign)
        await self.session.commit()
        await self.session.refresh(campaign)
        return campaign

    async def enroll_qualified_leads(
        self,
        campaign_id: int,
        lead_ids: Optional[List[int]] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Enroll qualified leads into campaign outreach schedule.
        """
        c_stmt = select(Campaign).where(Campaign.id == campaign_id)
        campaign = (await self.session.execute(c_stmt)).scalar_one_or_none()
        if not campaign:
            return {"error": f"Campaign #{campaign_id} not found."}

        # Leads already scheduled in this campaign must not be enrolled (and emailed) twice.
        already_enrolled = select(OutreachMessage.lead_id).where(
            OutreachMessage.campaign_id == campaign_id
        )

        # Select leads with valid pitches.
        # The scheduler reads lead.contact and lead.business; async SQLAlchemy cannot lazy-load
        # them (MissingGreenlet), so they are loaded with the query.
        stmt = (
            select(QualifiedLead)
            .join(Contact, QualifiedLead.contact_id == Contact.id)
            .join(Business, QualifiedLead.business_id == Business.id)
            .options(selectinload(QualifiedLead.contact), selectinload(QualifiedLead.business))
            .where(
                QualifiedLead.lead_status.in_([LeadStatus.READY_FOR_OUTREACH, LeadStatus.QUALIFIED]),
                QualifiedLead.personalized_pitch.isnot(None),
                QualifiedLead.id.not_in(already_enrolled),
            )
        )

        if lead_ids:
            stmt = stmt.where(QualifiedLead.id.in_(lead_ids))
        if campaign.country_code:
            stmt = stmt.where(Business.country_code == campaign.country_code.upper())

        stmt = stmt.limit(limit)
        leads = (await self.session.execute(stmt)).scalars().all()

        if not leads:
            return {"enrolled_count": 0, "message": "No eligible qualified leads found for enrollment."}

        messages = self.scheduler.schedule_lead_messages(
            campaign=campaign,
            leads=leads,
            start_time=datetime.now(timezone.utc),
        )

        for m in messages:
            self.session.add(m)

        campaign.total_leads_count += len(messages)
        campaign.status = CampaignStatus.RUNNING
        campaign.started_at = datetime.now(timezone.utc)

        await self.session.commit()
        return {
            "campaign_id": campaign.id,
            "enrolled_count": len(messages),
            "status": campaign.status.value,
        }

    async def dispatch_next_batch(
        self,
        campaign_id: int,
        batch_size: int = 10,
    ) -> Dict[str, Any]:
        """
        Dispatch the next batch of scheduled messages.
        """
        c_stmt = select(Campaign).where(Campaign.id == campaign_id)
        campaign = (await self.session.execute(c_stmt)).scalar_one_or_none()
        if not campaign:
            return {"error": f"Campaign #{campaign_id} not found."}

        # Find queued messages ready for sending
        now = datetime.now(timezone.utc)
        stmt = (
            select(OutreachMessage)
            .where(
                OutreachMessage.campaign_id == campaign_id,
                OutreachMessage.status == MessageStatus.QUEUED,
                OutreachMessage.scheduled_at <= now,
            )
            .limit(batch_size)
        )
        messages = (await self.session.execute(stmt)).scalars().all()

        dispatched, not_sent = [], []
        for msg in messages:
            # No sending provider exists, so no provider event: nothing is marked SENT, counted, logged as
            # MESSAGE_SENT or moved to CONTACTED (email engine v2 E1; real sending is E2).
            report = self.sender.dispatch(msg, simulate=True)
            if not report.success:
                not_sent.append({"message_id": msg.id, "reason": report.error})
                continue
            campaign.sent_count += 1

            # Log analytics event
            event = AnalyticsEvent(
                event_type=EventType.MESSAGE_SENT,
                campaign_id=campaign.id,
                message_id=msg.id,
                lead_id=msg.lead_id,
                metadata_payload={"recipient": msg.recipient_email, "sender": report.sender_used},
            )
            self.session.add(event)

            # Create or update CRM deal
            deal_stmt = select(CRMDeal).where(CRMDeal.lead_id == msg.lead_id)
            deal = (await self.session.execute(deal_stmt)).scalar_one_or_none()
            if not deal:
                deal = CRMDeal(
                    lead_id=msg.lead_id,
                    business_id=msg.business_id,
                    title=f"Outreach Deal: {msg.subject[:60]}",
                    stage=DealStage.CONTACTED,
                    estimated_value=5000.0,
                    notes=f"First outreach sent via {report.sender_used}",
                )
                self.session.add(deal)
            else:
                deal.stage = DealStage.CONTACTED
                deal.last_activity_at = now

            dispatched.append({
                "message_id": msg.id,
                "recipient": msg.recipient_email,
                "sender": report.sender_used,
                "sent_at": report.sent_at.isoformat(),
            })

        await self.session.commit()
        return {
            "campaign_id": campaign.id,
            "dispatched_count": len(dispatched),
            "total_sent": campaign.sent_count,
            "messages": dispatched,
            "not_sent_count": len(not_sent),
            "not_sent": not_sent,
        }

    async def handle_inbound_reply(
        self,
        message_id: int,
        reply_text: str,
    ) -> Dict[str, Any]:
        """
        Process inbound recipient reply, classify sentiment, and advance CRM stage.
        """
        msg_stmt = select(OutreachMessage).where(OutreachMessage.id == message_id)
        msg = (await self.session.execute(msg_stmt)).scalar_one_or_none()
        if not msg:
            return {"error": f"OutreachMessage #{message_id} not found."}

        classification = self.reply_classifier.classify_reply(reply_text)
        now = datetime.now(timezone.utc)

        msg.status = MessageStatus.REPLIED
        msg.replied_at = now

        # Update Campaign stats
        c_stmt = select(Campaign).where(Campaign.id == msg.campaign_id)
        campaign = (await self.session.execute(c_stmt)).scalar_one_or_none()
        if campaign:
            campaign.replied_count += 1
            if classification.intent == ReplyIntent.INTERESTED:
                campaign.converted_count += 1

        # Suppression trigger
        if classification.should_suppress:
            qual_service = QualificationService(self.session)
            await qual_service.add_opt_out(
                email=msg.recipient_email,
                reason="Recipient requested removal via reply",
                source="INBOUND_REPLY",
            )

        # CRM Deal progression
        deal_stmt = select(CRMDeal).where(CRMDeal.lead_id == msg.lead_id)
        deal = (await self.session.execute(deal_stmt)).scalar_one_or_none()

        if deal and classification.recommended_stage:
            deal.stage = classification.recommended_stage
            deal.notes = f"Inbound Reply ({classification.intent.value}): {reply_text[:100]}"
            deal.last_activity_at = now

        # Analytics event
        event = AnalyticsEvent(
            event_type=EventType.REPLY_RECEIVED,
            campaign_id=msg.campaign_id,
            message_id=msg.id,
            lead_id=msg.lead_id,
            metadata_payload={
                "intent": classification.intent.value,
                "confidence": classification.confidence,
                "action": classification.action_summary,
            },
        )
        self.session.add(event)

        await self.session.commit()

        return {
            "message_id": msg.id,
            "intent": classification.intent.value,
            "confidence": classification.confidence,
            "recommended_stage": classification.recommended_stage.value if classification.recommended_stage else None,
            "action_summary": classification.action_summary,
            "suppressed": classification.should_suppress,
        }

    async def get_crm_pipeline(self) -> Dict[str, Any]:
        """
        Fetch all deals grouped by stage for the interactive sales Kanban board.
        """
        stmt = (
            select(CRMDeal, Business.name, Business.country_code, QualifiedLead.composite_score)
            .join(Business, CRMDeal.business_id == Business.id)
            .join(QualifiedLead, CRMDeal.lead_id == QualifiedLead.id)
            .order_by(CRMDeal.last_activity_at.desc())
        )
        rows = (await self.session.execute(stmt)).all()

        stages = {s.value: [] for s in DealStage}
        total_pipeline_value = 0.0
        won_value = 0.0

        for deal, b_name, b_country, score in rows:
            stages[deal.stage.value].append({
                "id": deal.id,
                "lead_id": deal.lead_id,
                "business_id": deal.business_id,
                "business_name": b_name,
                "country_code": b_country,
                "lead_score": score,
                "title": deal.title,
                "stage": deal.stage.value,
                "estimated_value": deal.estimated_value,
                "notes": deal.notes,
                "last_activity_at": deal.last_activity_at.isoformat(),
            })
            total_pipeline_value += deal.estimated_value
            if deal.stage == DealStage.WON:
                won_value += deal.estimated_value

        return {
            "stages": stages,
            "total_deals": len(rows),
            "total_pipeline_value": round(total_pipeline_value, 2),
            "won_value": round(won_value, 2),
        }

    async def update_deal_stage(
        self,
        deal_id: int,
        stage: DealStage,
        estimated_value: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Move deal along sales pipeline stages.
        """
        stmt = select(CRMDeal).where(CRMDeal.id == deal_id)
        deal = (await self.session.execute(stmt)).scalar_one_or_none()
        if not deal:
            return {"error": f"Deal #{deal_id} not found."}

        deal.stage = stage
        if estimated_value is not None:
            deal.estimated_value = estimated_value
        if notes:
            deal.notes = notes
        deal.last_activity_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(deal)
        return {"deal_id": deal.id, "stage": deal.stage.value, "value": deal.estimated_value}

    async def get_conversion_funnel(self) -> Dict[str, Any]:
        """
        Calculate end-to-end conversion rates across all 5 architectural phases.
        """
        # Phase 1: Discovered Businesses
        b_count = (await self.session.execute(select(func.count(Business.id)))).scalar() or 0

        # Phase 2: Audited Opportunities
        opp_count = (await self.session.execute(select(func.count(Opportunity.id)))).scalar() or 0

        # Phase 3: Enriched Contacts
        contact_count = (await self.session.execute(select(func.count(Contact.id)))).scalar() or 0

        # Phase 4: Qualified Leads
        lead_count = (await self.session.execute(select(func.count(QualifiedLead.id)))).scalar() or 0

        # Phase 5: Outreach & Deals
        sent_count = (await self.session.execute(select(func.count(OutreachMessage.id)).where(OutreachMessage.status == MessageStatus.SENT))).scalar() or 0
        replied_count = (await self.session.execute(select(func.count(OutreachMessage.id)).where(OutreachMessage.status == MessageStatus.REPLIED))).scalar() or 0

        deals_won_stmt = select(func.count(CRMDeal.id), func.sum(CRMDeal.estimated_value)).where(CRMDeal.stage == DealStage.WON)
        won_row = (await self.session.execute(deals_won_stmt)).first()
        won_count = won_row[0] or 0
        won_revenue = float(won_row[1] or 0.0)

        return {
            "funnel": {
                "phase1_discovered_businesses": b_count,
                "phase2_identified_opportunities": opp_count,
                "phase3_enriched_contacts": contact_count,
                "phase4_qualified_leads": lead_count,
                "phase5_sent_messages": sent_count,
                "phase5_replied_prospects": replied_count,
                "phase5_deals_won": won_count,
            },
            "revenue_won": won_revenue,
            "reply_rate": round((replied_count / sent_count * 100) if sent_count > 0 else 0.0, 1),
            "qualification_rate": round((lead_count / b_count * 100) if b_count > 0 else 0.0, 1),
        }
