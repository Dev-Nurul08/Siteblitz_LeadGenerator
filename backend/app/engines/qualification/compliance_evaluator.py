"""
Compliance & Lead Qualification Evaluator (Phase 4).

Coordinates suppression list verification, cooling-off period enforcement,
jurisdiction regulatory assessment, and multi-factor lead qualification scoring.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Set

from backend.app.engines.qualification.country_rules import CountryComplianceProfile, CountryRulesEngine
from backend.app.models.business import Business
from backend.app.models.compliance import (
    LeadStatus,
    LegalBasis,
    LegalFramework,
    OutreachChannel,
    OutreachMode,
)
from backend.app.models.contact import Contact, EmailVerificationStatus, RoleLevel
from backend.app.models.opportunity import Opportunity, OpportunityPriority


@dataclass
class LeadEvaluationResult:
    """Complete evaluation report for an outreach candidate."""

    is_qualified: bool
    lead_status: LeadStatus
    outreach_mode: OutreachMode
    legal_framework: LegalFramework
    legal_basis: LegalBasis
    composite_score: float  # 0 to 100
    risk_score: float  # 0.0 to 1.0
    outreach_channel: OutreachChannel
    requirements_checklist: Dict[str, bool]
    rejection_reasons: List[str] = field(default_factory=list)
    evaluation_notes: str = ""


class ComplianceEvaluator:
    """
    Evaluates regulatory compliance and overall qualification readiness
    for a Business + Contact + Opportunity trio.
    """

    def __init__(self, country_rules: Optional[CountryRulesEngine] = None):
        self.rules_engine = country_rules or CountryRulesEngine()

    def evaluate_lead(
        self,
        business: Business,
        contact: Contact,
        opportunity: Opportunity,
        suppressed_emails: Optional[Set[str]] = None,
        suppressed_domains: Optional[Set[str]] = None,
        last_contacted_at: Optional[datetime] = None,
        cooldown_days: int = 30,
    ) -> LeadEvaluationResult:
        """
        Perform rigorous multi-point compliance and qualification evaluation.
        """
        rejection_reasons = []
        suppressed_emails = suppressed_emails or set()
        suppressed_domains = suppressed_domains or set()

        # 1. Suppression / Opt-Out Check
        recipient_email = (contact.email or "").strip().lower()
        recipient_domain = recipient_email.split("@")[-1] if "@" in recipient_email else ""

        if recipient_email in suppressed_emails:
            rejection_reasons.append(f"Email {recipient_email} is on global suppression/opt-out registry.")
        if recipient_domain and recipient_domain in suppressed_domains:
            rejection_reasons.append(f"Domain {recipient_domain} is globally suppressed from outreach.")

        # 2. Deliverability & Contact Integrity Check
        if contact.is_disposable or contact.email_status == EmailVerificationStatus.DISPOSABLE:
            rejection_reasons.append("Email address is a burner/disposable inbox.")

        if contact.email_status == EmailVerificationStatus.INVALID:
            rejection_reasons.append("Email failed MX DNS check or has invalid syntax.")

        # 3. Cooldown Period Check
        if last_contacted_at:
            # Handle tz-aware vs naive comparisons
            now = datetime.now(timezone.utc)
            if last_contacted_at.tzinfo is None:
                last_contacted_at = last_contacted_at.replace(tzinfo=timezone.utc)
            days_since = (now - last_contacted_at).days
            if days_since < cooldown_days:
                rejection_reasons.append(
                    f"In cooling period: Contacted {days_since} days ago (minimum {cooldown_days} days required)."
                )

        # 4. Country Jurisdiction Rules
        country_code = business.country_code or "US"
        is_corporate = True
        profile: CountryComplianceProfile = self.rules_engine.evaluate_jurisdiction(
            country_code=country_code,
            has_business_email=not contact.is_role_based,
            is_corporate_entity=is_corporate,
        )

        checklist = dict(profile.requirements_checklist)
        checklist["cooldown_period_respected"] = len([r for r in rejection_reasons if "cooling" in r.lower()]) == 0
        checklist["suppression_check_passed"] = len([r for r in rejection_reasons if "suppress" in r.lower()]) == 0

        # 5. Composite Lead Scoring
        # Opportunity score (0-100) -> 45% weight
        raw_opp_score = getattr(opportunity, "score", None)
        if raw_opp_score is None:
            raw_opp_score = getattr(opportunity, "composite_score", 50.0)
        opp_score = float(raw_opp_score if raw_opp_score is not None else 50.0)

        # Contact deliverability (0.0-1.0) -> 35% weight
        deliverability_score = float(contact.verification_score if contact.verification_score is not None else 0.5)

        # Compliance safety -> 20% weight (1.0 - risk_score)
        compliance_safety = max(0.0, 1.0 - profile.risk_score)

        raw_composite = (opp_score * 0.45) + ((deliverability_score * 100) * 0.35) + ((compliance_safety * 100) * 0.20)
        composite_score = round(min(100.0, max(0.0, raw_composite)), 1)

        # 6. Status & Outreach Mode Resolution
        if rejection_reasons:
            return LeadEvaluationResult(
                is_qualified=False,
                lead_status=LeadStatus.DISQUALIFIED,
                outreach_mode=OutreachMode.PROHIBITED,
                legal_framework=profile.framework,
                legal_basis=LegalBasis.NONE,
                composite_score=composite_score,
                risk_score=1.0,
                outreach_channel=OutreachChannel.EMAIL,
                requirements_checklist=checklist,
                rejection_reasons=rejection_reasons,
                evaluation_notes=f"Disqualified: {'; '.join(rejection_reasons)}",
            )

        # Determine if needs human review or automated outreach
        outreach_mode = profile.default_mode

        # If email is risky, role-based, or score is borderline -> force manual review
        is_borderline = composite_score < 60.0
        is_risky_email = contact.email_status in (EmailVerificationStatus.CATCH_ALL, EmailVerificationStatus.UNVERIFIED)
        is_generic_inbox = contact.role_level == RoleLevel.GENERAL_INBOX

        if is_borderline or is_risky_email or is_generic_inbox or profile.default_mode == OutreachMode.MANUAL_REVIEW_ONLY:
            lead_status = LeadStatus.NEEDS_REVIEW
            outreach_mode = OutreachMode.MANUAL_REVIEW_ONLY
        else:
            lead_status = LeadStatus.QUALIFIED
            outreach_mode = OutreachMode.AUTOMATED

        # Preferred channel selection
        channel = OutreachChannel.EMAIL
        if contact.linkedin_url and contact.role_level in (RoleLevel.EXECUTIVE, RoleLevel.MANAGEMENT):
            # For executives with LinkedIn, LinkedIn is a high-value secondary/primary channel
            channel = OutreachChannel.EMAIL  # Default primary remains verified email

        notes = (
            f"Evaluated under {profile.framework.value} ({profile.country_name}). "
            f"Lawful Basis: {profile.legal_basis.value}. Mode: {outreach_mode.value}. "
            f"Deliverability: {round(deliverability_score * 100)}%, Opportunity Score: {opp_score}."
        )

        return LeadEvaluationResult(
            is_qualified=True,
            lead_status=lead_status,
            outreach_mode=outreach_mode,
            legal_framework=profile.framework,
            legal_basis=profile.legal_basis,
            composite_score=composite_score,
            risk_score=profile.risk_score,
            outreach_channel=channel,
            requirements_checklist=checklist,
            rejection_reasons=[],
            evaluation_notes=notes,
        )
