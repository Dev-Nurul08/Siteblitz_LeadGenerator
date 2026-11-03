"""
Tests for CountryRulesEngine (Phase 4).
"""

from backend.app.engines.qualification.country_rules import CountryRulesEngine
from backend.app.models.compliance import LegalBasis, LegalFramework, OutreachMode


class TestCountryRulesEngine:
    """Test suite for country-specific regulatory evaluations."""

    def setup_method(self):
        self.engine = CountryRulesEngine()

    def test_us_can_spam_evaluation(self):
        """US jurisdiction adheres to FTC CAN-SPAM Act."""
        profile = self.engine.evaluate_jurisdiction("US")
        assert profile.framework == LegalFramework.CAN_SPAM
        assert profile.is_outreach_permitted is True
        assert profile.default_mode == OutreachMode.AUTOMATED
        assert profile.legal_basis == LegalBasis.OPT_OUT_REGIME
        assert profile.risk_score <= 0.20
        assert profile.requirements_checklist["valid_physical_postal_address"] is True
        assert profile.requirements_checklist["clear_opt_out_link"] is True
        assert "UNSUBSCRIBE_LINK" in profile.mandatory_footer_elements

    def test_uk_gdpr_pecr_evaluation(self):
        """UK B2B corporate subscribers permit legitimate interest outreach."""
        profile = self.engine.evaluate_jurisdiction("GB", is_corporate_entity=True)
        assert profile.framework == LegalFramework.GDPR_UK
        assert profile.is_outreach_permitted is True
        assert profile.default_mode == OutreachMode.AUTOMATED
        assert profile.legal_basis == LegalBasis.LEGITIMATE_INTEREST

    def test_germany_strict_uwg_requires_manual_review(self):
        """Germany cold B2B email requires manual review due to strict UWG unfair competition laws."""
        profile = self.engine.evaluate_jurisdiction("DE")
        assert profile.framework == LegalFramework.GDPR_EU
        assert profile.is_outreach_permitted is True
        assert profile.default_mode == OutreachMode.MANUAL_REVIEW_ONLY
        assert profile.risk_score >= 0.50

    def test_canada_casl_evaluation(self):
        """Canada CASL requires conspicuous publication provenance check."""
        profile = self.engine.evaluate_jurisdiction("CA")
        assert profile.framework == LegalFramework.CASL
        assert profile.default_mode == OutreachMode.MANUAL_REVIEW_ONLY
        assert profile.legal_basis == LegalBasis.CONSPICUOUSLY_PUBLISHED_B2B
        assert profile.requirements_checklist["conspicuous_publication_provenance_logged"] is True

    def test_australia_spam_act_evaluation(self):
        """Australia Spam Act allows inferred consent for published B2B addresses."""
        profile = self.engine.evaluate_jurisdiction("AU")
        assert profile.framework == LegalFramework.AUSTRALIA_SPAM_ACT
        assert profile.is_outreach_permitted is True
        assert profile.default_mode == OutreachMode.AUTOMATED
        assert profile.legal_basis == LegalBasis.CONSPICUOUSLY_PUBLISHED_B2B

    def test_unknown_country_fallback(self):
        """Unknown or unlisted countries default to conservative manual review."""
        profile = self.engine.evaluate_jurisdiction("ZZ")
        assert profile.framework == LegalFramework.GENERAL_B2B
        assert profile.default_mode == OutreachMode.MANUAL_REVIEW_ONLY
        assert profile.is_outreach_permitted is True
