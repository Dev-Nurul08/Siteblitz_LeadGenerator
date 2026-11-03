"""
Tests for OpportunityScorer (Phase 2).
"""

from backend.app.engines.opportunity.detector import DetectedNeed
from backend.app.engines.opportunity.scorer import OpportunityScorer
from backend.app.models.business import Business
from backend.app.models.opportunity import OpportunityPriority, ServiceCategory


class TestOpportunityScorer:
    """Test suite for OpportunityScorer."""

    def setup_method(self):
        self.scorer = OpportunityScorer()

    def test_high_urgency_unwebbed_business_scores_high_or_critical(self):
        """Urgent missing website with contact info scores as HIGH/CRITICAL."""
        biz = Business(
            name="Harborview Dental Clinic",
            country_code="US",
            phone="+12065551234",
            email="office@harborviewdental.com",
        )
        need = DetectedNeed(
            service_category=ServiceCategory.NEW_WEBSITE,
            title="New Custom Website",
            summary="Business has no website.",
            evidence={"missing_website": True},
            pitch_angles=["Build credibility"],
            need_severity=0.95,
        )

        scored = self.scorer.score_need(
            need=need,
            business=biz,
            business_categories=["Dentist", "Clinic"],
        )

        assert scored.score >= 80.0
        assert scored.priority == OpportunityPriority.CRITICAL
        assert scored.score_breakdown["need_severity"] == 38.0
        assert scored.score_breakdown["market_viability"] == 20.0
        assert scored.score_breakdown["contactability"] == 15.0

    def test_lower_severity_scores_as_medium(self):
        """Mild deficiency with minimal contact details scores as MEDIUM/LOW."""
        biz = Business(
            name="Corner Convenience",
            country_code="GB",
            phone=None,
            email=None,
        )
        need = DetectedNeed(
            service_category=ServiceCategory.SEO_PERFORMANCE,
            title="SEO Optimization",
            summary="Missing meta description.",
            evidence={},
            pitch_angles=[],
            need_severity=0.50,
        )

        scored = self.scorer.score_need(
            need=need,
            business=biz,
            business_categories=["Convenience Store"],
        )

        assert scored.score < 65.0
        assert scored.priority in [OpportunityPriority.MEDIUM, OpportunityPriority.LOW]

    def test_score_never_exceeds_100(self):
        """Scores are strictly bounded between 0 and 100."""
        biz = Business(
            name="Enterprise Global Law Partners",
            country_code="US",
            phone="+18005550199",
            email="partners@globallaw.com",
        )
        need = DetectedNeed(
            service_category=ServiceCategory.NEW_WEBSITE,
            title="New Custom Website",
            summary="Need website.",
            evidence={},
            pitch_angles=[],
            need_severity=1.0,
        )

        scored = self.scorer.score_need(
            need=need,
            business=biz,
            business_categories=["Lawyer", "Legal"],
        )

        assert 0.0 <= scored.score <= 100.0
