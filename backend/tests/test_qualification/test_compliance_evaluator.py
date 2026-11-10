"""
Tests for ComplianceEvaluator (Phase 4).
"""

from datetime import datetime, timedelta, timezone

from backend.app.engines.qualification.compliance_evaluator import ComplianceEvaluator
from backend.app.models.business import Business, BusinessLocation
from backend.app.models.compliance import LeadStatus, OutreachMode
from backend.app.models.contact import Contact, EmailVerificationStatus, RoleLevel
from backend.app.models.opportunity import Opportunity, OpportunityPriority, ServiceCategory


class TestComplianceEvaluator:
    """Test suite for lead compliance and readiness evaluation."""

    def setup_method(self):
        self.evaluator = ComplianceEvaluator()
        self.business = Business(
            id=1,
            name="Apex Dental Care",
            country_code="US",
            website_url="https://apexdental.com",
        )
        self.business.locations = [BusinessLocation(city="Chicago")]
        self.contact = Contact(
            id=1,
            business_id=1,
            full_name="Dr. Sarah Jenkins",
            email="sjenkins@apexdental.com",
            role_level=RoleLevel.EXECUTIVE,
            email_status=EmailVerificationStatus.VERIFIED,
            verification_score=0.95,
            is_disposable=False,
            is_role_based=False,
        )
        self.opportunity = Opportunity(
            id=1,
            business_id=1,
            service_category=ServiceCategory.ONLINE_BOOKING,
            priority=OpportunityPriority.HIGH,
            title="Online Booking System Needed",
            summary="Clinic has no direct online scheduler",
            score=85.0,
        )

    def test_clean_verified_lead_evaluates_as_qualified(self):
        """Verified contact with strong opportunity in US qualifies for automated outreach."""
        res = self.evaluator.evaluate_lead(
            business=self.business,
            contact=self.contact,
            opportunity=self.opportunity,
        )
        assert res.is_qualified is True
        assert res.lead_status == LeadStatus.QUALIFIED
        assert res.outreach_mode == OutreachMode.AUTOMATED
        assert res.composite_score >= 80.0
        assert len(res.rejection_reasons) == 0

    def test_suppressed_email_disqualifies_lead(self):
        """Email present in suppression list is immediately disqualified."""
        suppressed = {"sjenkins@apexdental.com"}
        res = self.evaluator.evaluate_lead(
            business=self.business,
            contact=self.contact,
            opportunity=self.opportunity,
            suppressed_emails=suppressed,
        )
        assert res.is_qualified is False
        assert res.lead_status == LeadStatus.DISQUALIFIED
        assert res.outreach_mode == OutreachMode.PROHIBITED
        assert any("suppression" in r.lower() for r in res.rejection_reasons)

    def test_suppressed_domain_disqualifies_lead(self):
        """Company domain present in suppression list blocks outreach to any employee."""
        suppressed_domains = {"apexdental.com"}
        res = self.evaluator.evaluate_lead(
            business=self.business,
            contact=self.contact,
            opportunity=self.opportunity,
            suppressed_domains=suppressed_domains,
        )
        assert res.is_qualified is False
        assert res.lead_status == LeadStatus.DISQUALIFIED
        assert any("domain" in r.lower() for r in res.rejection_reasons)

    def test_disposable_email_disqualifies_lead(self):
        """Disposable / burner email addresses are disqualified."""
        self.contact.is_disposable = True
        self.contact.email_status = EmailVerificationStatus.DISPOSABLE
        res = self.evaluator.evaluate_lead(
            business=self.business,
            contact=self.contact,
            opportunity=self.opportunity,
        )
        assert res.is_qualified is False
        assert res.lead_status == LeadStatus.DISQUALIFIED
        assert any("burner" in r.lower() or "disposable" in r.lower() for r in res.rejection_reasons)

    def test_recent_contact_violates_cooldown(self):
        """Contact contacted 10 days ago violates 30-day cooldown period."""
        recent_date = datetime.now(timezone.utc) - timedelta(days=10)
        res = self.evaluator.evaluate_lead(
            business=self.business,
            contact=self.contact,
            opportunity=self.opportunity,
            last_contacted_at=recent_date,
            cooldown_days=30,
        )
        assert res.is_qualified is False
        assert res.lead_status == LeadStatus.DISQUALIFIED
        assert any("cooling" in r.lower() for r in res.rejection_reasons)

    def test_strict_country_routes_to_manual_review(self):
        """Lead in Germany (DE) routes to NEEDS_REVIEW / MANUAL_REVIEW_ONLY."""
        self.business.country_code = "DE"
        res = self.evaluator.evaluate_lead(
            business=self.business,
            contact=self.contact,
            opportunity=self.opportunity,
        )
        assert res.is_qualified is True
        assert res.lead_status == LeadStatus.NEEDS_REVIEW
        assert res.outreach_mode == OutreachMode.MANUAL_REVIEW_ONLY

    def test_missing_country_is_held_not_treated_as_us(self):
        """QA-2026-11-10 (QA-015): an empty country became "US" and qualified for automated sending."""
        for missing in (None, ""):
            self.business.country_code = missing
            res = self.evaluator.evaluate_lead(
                business=self.business,
                contact=self.contact,
                opportunity=self.opportunity,
            )
            assert res.lead_status == LeadStatus.NEEDS_REVIEW, missing
            assert res.outreach_mode == OutreachMode.MANUAL_REVIEW_ONLY, missing

    def test_borderline_score_routes_to_needs_review(self):
        """Low opportunity score brings composite score below 60, triggering manual review."""
        self.opportunity.score = 25.0
        self.contact.verification_score = 0.40
        res = self.evaluator.evaluate_lead(
            business=self.business,
            contact=self.contact,
            opportunity=self.opportunity,
        )
        assert res.is_qualified is True
        assert res.lead_status == LeadStatus.NEEDS_REVIEW
        assert res.composite_score < 60.0
