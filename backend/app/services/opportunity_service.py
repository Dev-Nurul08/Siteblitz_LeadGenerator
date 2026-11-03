"""
Opportunity Service — orchestrates website resolution, deep auditing,
opportunity detection, and database persistence.
"""

from typing import Optional
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.engines.opportunity.auditor import WebsiteAuditor
from backend.app.engines.opportunity.detector import OpportunityDetector
from backend.app.engines.opportunity.resolver import WebsiteResolver
from backend.app.engines.opportunity.scorer import OpportunityScorer
from backend.app.models.business import Business, WebsiteStatus
from backend.app.models.opportunity import (
    Opportunity,
    OpportunityStatus,
    WebsiteAudit,
)

logger = structlog.get_logger(__name__)


class OpportunityService:
    """
    Coordinates Phase 2 opportunity detection workflow:
    1. Resolve & check website reachability and SSL
    2. Audit HTML technical quality and features
    3. Detect matching agency service needs
    4. Compute weighted opportunity scores
    5. Save audits and opportunities to the database
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.resolver = WebsiteResolver()
        self.auditor = WebsiteAuditor()
        self.detector = OpportunityDetector()
        self.scorer = OpportunityScorer()

    async def evaluate_business(self, business_id: int) -> dict:
        """
        Perform complete audit and opportunity detection for a business.
        """
        # Load business with categories
        stmt = (
            select(Business)
            .where(Business.id == business_id)
            .options(selectinload(Business.categories))
        )
        result = await self.session.execute(stmt)
        business = result.scalar_one_or_none()

        if not business:
            return {"error": f"Business with ID {business_id} not found"}

        categories = [c.category_name for c in business.categories]
        resolution = None
        audit = None
        audit_record = None

        # Step 1: Resolve website if provided
        if business.website_url:
            resolution = await self.resolver.resolve(business.website_url)

            # Update website status on business
            business.website_status = resolution.status
            if resolution.final_url and resolution.final_url != business.website_url:
                business.website_url = resolution.final_url

            # Step 2: Audit HTML if reachable
            if resolution.is_reachable and resolution.html_content:
                audit = self.auditor.audit_html(
                    url=resolution.final_url or business.website_url,
                    html_content=resolution.html_content,
                )

                # Persist WebsiteAudit
                audit_record = WebsiteAudit(
                    business_id=business.id,
                    url_analyzed=resolution.original_url,
                    final_url=resolution.final_url,
                    is_reachable=resolution.is_reachable,
                    http_status=resolution.http_status,
                    has_ssl=resolution.has_ssl,
                    load_time_seconds=resolution.load_time_seconds,
                    is_mobile_responsive=audit.is_mobile_responsive,
                    has_viewport_meta=audit.has_viewport_meta,
                    detected_cms=audit.detected_cms,
                    detected_frameworks={"frameworks": audit.detected_frameworks},
                    has_ecommerce=audit.has_ecommerce,
                    has_online_booking=audit.has_online_booking,
                    has_contact_form=audit.has_contact_form,
                    has_analytics=audit.has_analytics,
                    meta_title=audit.meta_title,
                    meta_description=audit.meta_description,
                    headings_summary=audit.headings_summary,
                    emails_found={"emails": audit.emails_found},
                    phones_found={"phones": audit.phones_found},
                    social_links_found=audit.social_links_found,
                    raw_audit_data=audit.raw_technologies,
                    audit_error=resolution.error_message,
                )
                self.session.add(audit_record)
                await self.session.flush()

                # Merge extracted emails or phone numbers into business if missing
                if audit.emails_found and not business.email:
                    business.email = audit.emails_found[0]
                if audit.phones_found and not business.phone:
                    business.phone = audit.phones_found[0]
                if audit.social_links_found and not business.social_urls:
                    business.social_urls = audit.social_links_found

        # Step 3: Detect Opportunities
        detected_needs = self.detector.detect_opportunities(
            business=business,
            audit=audit,
            resolution=resolution,
            business_categories=categories,
        )

        created_opportunities = []
        for need in detected_needs:
            scored = self.scorer.score_need(
                need=need,
                business=business,
                business_categories=categories,
            )

            # Check if this opportunity already exists for this business
            opp_stmt = select(Opportunity).where(
                Opportunity.business_id == business.id,
                Opportunity.service_category == need.service_category,
            )
            existing_opp = (await self.session.execute(opp_stmt)).scalar_one_or_none()

            if existing_opp:
                existing_opp.title = need.title
                existing_opp.summary = need.summary
                existing_opp.score = scored.score
                existing_opp.priority = scored.priority
                existing_opp.confidence = scored.confidence
                existing_opp.evidence = {
                    **need.evidence,
                    "score_breakdown": scored.score_breakdown,
                }
                existing_opp.pitch_angles = {"angles": need.pitch_angles}
                if audit_record:
                    existing_opp.audit_id = audit_record.id
                target_opp = existing_opp
            else:
                target_opp = Opportunity(
                    business_id=business.id,
                    audit_id=audit_record.id if audit_record else None,
                    service_category=need.service_category,
                    title=need.title,
                    summary=need.summary,
                    score=scored.score,
                    confidence=scored.confidence,
                    priority=scored.priority,
                    status=OpportunityStatus.IDENTIFIED,
                    evidence={
                        **need.evidence,
                        "score_breakdown": scored.score_breakdown,
                    },
                    pitch_angles={"angles": need.pitch_angles},
                )
                self.session.add(target_opp)

            created_opportunities.append(
                {
                    "service_category": need.service_category.value,
                    "title": need.title,
                    "score": scored.score,
                    "priority": scored.priority.value,
                }
            )

        await self.session.flush()

        logger.info(
            "business_evaluated",
            business_id=business.id,
            opportunities_found=len(created_opportunities),
        )

        return {
            "business_id": business.id,
            "business_name": business.name,
            "website_status": business.website_status.value,
            "audit_id": audit_record.id if audit_record else None,
            "opportunities": created_opportunities,
        }

    async def batch_evaluate_unaudited(self, limit: int = 50) -> dict:
        """
        Find businesses without opportunities or audits and evaluate them in batch.
        """
        stmt = (
            select(Business.id)
            .outerjoin(Opportunity, Business.id == Opportunity.business_id)
            .where(Opportunity.id.is_(None))
            .limit(limit)
        )
        rows = (await self.session.execute(stmt)).scalars().all()

        evaluated = []
        for biz_id in rows:
            res = await self.evaluate_business(biz_id)
            evaluated.append(res)

        return {
            "evaluated_count": len(evaluated),
            "results": evaluated,
        }
