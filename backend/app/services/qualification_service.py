"""
Phase 4 — Qualification & Compliance Service.

Orchestrates multi-source compliance checks, lead qualification scoring,
AI personalization generation, and suppression list lifecycle management.
"""

from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional, Set

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.engines.qualification.ai_personalizer import AIPersonalizer
from backend.app.engines.qualification.compliance_evaluator import ComplianceEvaluator
from backend.app.engines.qualification.country_rules import CountryRulesEngine
from backend.app.engines.qualification.output_validator import OutputValidator
from backend.app.models.business import Business
from backend.app.models.compliance import (
    ComplianceEvaluation,
    LeadStatus,
    OptOut,
    OutreachChannel,
    OutreachMode,
    QualifiedLead,
)
from backend.app.models.contact import Contact, EmailVerificationStatus, RoleLevel
from backend.app.models.opportunity import Opportunity, OpportunityPriority


class QualificationService:
    """
    Service managing lead qualification, AI pitch generation, and regulatory compliance.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.country_rules = CountryRulesEngine()
        self.evaluator = ComplianceEvaluator(self.country_rules)
        self.personalizer = AIPersonalizer()
        self.validator = OutputValidator()

    async def _get_suppressed_sets(self) -> tuple[Set[str], Set[str]]:
        """Fetch all suppressed email addresses and domains from registry."""
        stmt = select(OptOut.email, OptOut.domain)
        rows = (await self.session.execute(stmt)).all()
        emails = {r[0].lower().strip() for r in rows if r[0]}
        domains = {r[1].lower().strip() for r in rows if r[1]}
        return emails, domains

    async def qualify_lead(
        self,
        business_id: int,
        contact_id: Optional[int] = None,
        opportunity_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate and qualify a business for sales outreach.
        """
        # 1. Fetch Business
        b_stmt = select(Business).where(Business.id == business_id)
        business = (await self.session.execute(b_stmt)).scalar_one_or_none()
        if not business:
            return {"error": f"Business #{business_id} not found."}

        # 2. Resolve Contact (or pick best available)
        contact = None
        if contact_id:
            c_stmt = select(Contact).where(Contact.id == contact_id, Contact.business_id == business_id)
            contact = (await self.session.execute(c_stmt)).scalar_one_or_none()
        else:
            # Pick highest priority role with highest score
            c_stmt = (
                select(Contact)
                .where(Contact.business_id == business_id)
                .order_by(
                    Contact.verification_score.desc(),
                    Contact.role_level.asc(),
                )
            )
            contact = (await self.session.execute(c_stmt)).scalars().first()

        if not contact:
            return {"error": f"No contacts found for Business #{business_id}. Enrich contacts first."}

        # 3. Resolve Opportunity (or pick highest scoring)
        opportunity = None
        if opportunity_id:
            o_stmt = select(Opportunity).where(Opportunity.id == opportunity_id, Opportunity.business_id == business_id)
            opportunity = (await self.session.execute(o_stmt)).scalar_one_or_none()
        else:
            o_stmt = (
                select(Opportunity)
                .where(Opportunity.business_id == business_id)
                .order_by(Opportunity.score.desc())
            )
            opportunity = (await self.session.execute(o_stmt)).scalars().first()

        if not opportunity:
            return {"error": f"No digital opportunities identified for Business #{business_id}. Run audit first."}

        # 4. Suppression List & Cooldown Check
        suppressed_emails, suppressed_domains = await self._get_suppressed_sets()

        # Check existing qualified lead for cooldown
        existing_lead_stmt = select(QualifiedLead).where(
            QualifiedLead.business_id == business_id,
            QualifiedLead.contact_id == contact.id,
        )
        existing_lead = (await self.session.execute(existing_lead_stmt)).scalar_one_or_none()
        last_contacted_at = existing_lead.last_contacted_at if existing_lead else None

        # 5. Evaluate Compliance & Readiness
        eval_result = self.evaluator.evaluate_lead(
            business=business,
            contact=contact,
            opportunity=opportunity,
            suppressed_emails=suppressed_emails,
            suppressed_domains=suppressed_domains,
            last_contacted_at=last_contacted_at,
        )

        # 6. Record ComplianceEvaluation
        comp_eval = ComplianceEvaluation(
            business_id=business.id,
            contact_id=contact.id,
            opportunity_id=opportunity.id,
            country_code=business.country_code or "US",
            legal_framework=eval_result.legal_framework,
            is_outreach_permitted=eval_result.is_qualified,
            outreach_mode=eval_result.outreach_mode,
            legal_basis=eval_result.legal_basis,
            risk_score=eval_result.risk_score,
            requirements_checklist=eval_result.requirements_checklist,
            evaluation_notes=eval_result.evaluation_notes,
            evaluated_at=datetime.now(timezone.utc),
        )
        self.session.add(comp_eval)
        await self.session.flush()

        # 7. Generate Personalized Pitch if permitted
        personalized_subject = None
        personalized_pitch = None
        pitch_template = None
        validation_passed = False
        validation_flags = []

        if eval_result.is_qualified:
            pitch_res = self.personalizer.generate_pitch(
                business=business,
                contact=contact,
                opportunity=opportunity,
            )
            personalized_subject = pitch_res.subject_line
            personalized_pitch = pitch_res.body_text
            pitch_template = pitch_res.template_id

            # Validate generated pitch
            val_res = self.validator.validate(
                subject=personalized_subject,
                body=personalized_pitch,
            )
            validation_passed = val_res.is_valid
            validation_flags = val_res.errors + val_res.warnings

            if not validation_passed:
                # If safety validation failed, do not auto-approve
                eval_result.lead_status = LeadStatus.NEEDS_REVIEW

        # 8. Upsert QualifiedLead
        if not existing_lead:
            existing_lead = QualifiedLead(
                business_id=business.id,
                contact_id=contact.id,
                opportunity_id=opportunity.id,
                compliance_evaluation_id=comp_eval.id,
                composite_score=eval_result.composite_score,
                lead_status=eval_result.lead_status,
                outreach_channel=eval_result.outreach_channel,
                personalized_subject=personalized_subject,
                personalized_pitch=personalized_pitch,
                pitch_template_used=pitch_template,
                validation_passed=validation_passed,
                validation_flags=validation_flags,
            )
            self.session.add(existing_lead)
        else:
            existing_lead.compliance_evaluation_id = comp_eval.id
            existing_lead.composite_score = eval_result.composite_score
            existing_lead.lead_status = eval_result.lead_status
            existing_lead.outreach_channel = eval_result.outreach_channel
            existing_lead.personalized_subject = personalized_subject
            existing_lead.personalized_pitch = personalized_pitch
            existing_lead.pitch_template_used = pitch_template
            existing_lead.validation_passed = validation_passed
            existing_lead.validation_flags = validation_flags
            existing_lead.updated_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(existing_lead)

        return {
            "lead_id": existing_lead.id,
            "business_id": business.id,
            "business_name": business.name,
            "contact_email": contact.email,
            "contact_name": contact.full_name,
            "opportunity_service": opportunity.service_category.value,
            "composite_score": existing_lead.composite_score,
            "lead_status": existing_lead.lead_status.value,
            "outreach_mode": eval_result.outreach_mode.value,
            "legal_framework": eval_result.legal_framework.value,
            "legal_basis": eval_result.legal_basis.value,
            "validation_passed": validation_passed,
            "personalized_subject": personalized_subject,
            "personalized_pitch": personalized_pitch,
            "evaluation_notes": eval_result.evaluation_notes,
        }

    async def batch_qualify(self, limit: int = 25) -> Dict[str, Any]:
        """
        Batch evaluate businesses that have both contacts and opportunities.
        """
        # Find business IDs that have opportunities and contacts, but not yet qualified
        subquery_leads = select(QualifiedLead.business_id)

        stmt = (
            select(Business.id)
            .join(Opportunity, Opportunity.business_id == Business.id)
            .join(Contact, Contact.business_id == Business.id)
            .where(Business.id.not_in(subquery_leads))
            .group_by(Business.id)
            .limit(limit)
        )

        business_ids = (await self.session.execute(stmt)).scalars().all()

        results = []
        counts = {"QUALIFIED": 0, "NEEDS_REVIEW": 0, "DISQUALIFIED": 0, "ERROR": 0}

        for bid in business_ids:
            res = await self.qualify_lead(bid)
            if "error" in res:
                counts["ERROR"] += 1
            else:
                status = res.get("lead_status", "NEEDS_REVIEW")
                counts[status] = counts.get(status, 0) + 1
                results.append(res)

        return {
            "evaluated_count": len(business_ids),
            "counts": counts,
            "leads": results,
        }

    async def add_opt_out(
        self,
        email: str,
        reason: str = "User requested unsubscribe",
        source: str = "UNSUBSCRIBE_LINK",
        domain: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Register recipient in global suppression list and disqualify any pending outreach.
        """
        clean_email = email.strip().lower()
        clean_domain = domain.strip().lower() if domain else (clean_email.split("@")[-1] if "@" in clean_email else None)

        existing_stmt = select(OptOut).where(OptOut.email == clean_email)
        existing = (await self.session.execute(existing_stmt)).scalar_one_or_none()

        if not existing:
            opt = OptOut(
                email=clean_email,
                domain=clean_domain,
                reason=reason,
                source=source,
            )
            self.session.add(opt)

        # Disqualify any active leads for this email
        lead_stmt = (
            select(QualifiedLead)
            .join(Contact, QualifiedLead.contact_id == Contact.id)
            .where(func.lower(Contact.email) == clean_email)
        )
        affected_leads = (await self.session.execute(lead_stmt)).scalars().all()
        for lead in affected_leads:
            lead.lead_status = LeadStatus.DISQUALIFIED
            lead.validation_flags = (lead.validation_flags or []) + [f"Opted out on {datetime.now(timezone.utc).isoformat()}"]

        await self.session.commit()
        return {
            "email": clean_email,
            "status": "SUPPRESSED",
            "affected_leads_count": len(affected_leads),
        }

    async def update_lead_status(
        self,
        lead_id: int,
        status: LeadStatus,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Operator sign-off: Transition lead status (e.g. approve to READY_FOR_OUTREACH).
        """
        stmt = select(QualifiedLead).where(QualifiedLead.id == lead_id)
        lead = (await self.session.execute(stmt)).scalar_one_or_none()
        if not lead:
            return {"error": f"Lead #{lead_id} not found."}

        lead.lead_status = status
        if notes:
            lead.validation_flags = (lead.validation_flags or []) + [f"Operator Note: {notes}"]
        lead.updated_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(lead)
        return {"lead_id": lead.id, "status": lead.lead_status.value}
