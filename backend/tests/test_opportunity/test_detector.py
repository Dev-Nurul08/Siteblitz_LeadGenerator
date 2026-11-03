"""
Tests for OpportunityDetector (Phase 2).
"""

from backend.app.engines.opportunity.auditor import AuditResult
from backend.app.engines.opportunity.detector import OpportunityDetector
from backend.app.engines.opportunity.resolver import ResolutionResult
from backend.app.models.business import Business, WebsiteStatus
from backend.app.models.opportunity import ServiceCategory


class TestOpportunityDetector:
    """Test suite for OpportunityDetector."""

    def setup_method(self):
        self.detector = OpportunityDetector()

    def test_new_website_detected_for_unwebbed_business(self):
        """Businesses with no website trigger a NEW_WEBSITE opportunity."""
        biz = Business(
            name="Mario's Traditional Bakery",
            country_code="IT",
            website_url=None,
            website_status=WebsiteStatus.NOT_FOUND,
        )
        needs = self.detector.detect_opportunities(biz)
        categories = [n.service_category for n in needs]

        assert ServiceCategory.NEW_WEBSITE in categories
        new_web_need = next(n for n in needs if n.service_category == ServiceCategory.NEW_WEBSITE)
        assert "Mario's Traditional Bakery" in new_web_need.title
        assert new_web_need.need_severity >= 0.90

    def test_new_website_for_social_only_presence(self):
        """Businesses operating only through social media trigger NEW_WEBSITE."""
        biz = Business(
            name="Bella Salon Boutique",
            country_code="US",
            website_url=None,
            website_status=WebsiteStatus.SOCIAL_ONLY,
            social_urls={"instagram": "https://instagram.com/bellasalon"},
        )
        needs = self.detector.detect_opportunities(biz)
        new_web_need = next(n for n in needs if n.service_category == ServiceCategory.NEW_WEBSITE)

        assert "social media" in new_web_need.summary.lower()

    def test_website_redesign_detected_for_non_mobile_responsive(self):
        """Websites lacking mobile responsiveness trigger WEBSITE_REDESIGN."""
        biz = Business(
            name="Vintage Antiques Ltd",
            country_code="GB",
            website_url="https://vintageantiques.co.uk",
            website_status=WebsiteStatus.FOUND,
        )
        audit = AuditResult(
            url="https://vintageantiques.co.uk",
            is_mobile_responsive=False,
            has_viewport_meta=False,
        )
        res = ResolutionResult(
            original_url="https://vintageantiques.co.uk",
            final_url="https://vintageantiques.co.uk",
            is_reachable=True,
            has_ssl=True,
            load_time_seconds=1.2,
        )

        needs = self.detector.detect_opportunities(biz, audit=audit, resolution=res)
        categories = [n.service_category for n in needs]

        assert ServiceCategory.WEBSITE_REDESIGN in categories
        redesign_need = next(n for n in needs if n.service_category == ServiceCategory.WEBSITE_REDESIGN)
        assert any("mobile" in r.lower() for r in redesign_need.evidence["reasons"])

    def test_mobile_app_opportunity_for_restaurant(self):
        """Restaurants and high-frequency hospitality trigger MOBILE_APP opportunity."""
        biz = Business(
            name="Golden Dragon Bistro",
            country_code="US",
            website_url="https://goldendragon.com",
            website_status=WebsiteStatus.FOUND,
        )
        audit = AuditResult(
            url="https://goldendragon.com",
            is_mobile_responsive=True,
            has_viewport_meta=True,
        )
        res = ResolutionResult(
            original_url="https://goldendragon.com",
            final_url="https://goldendragon.com",
            is_reachable=True,
            has_ssl=True,
        )

        needs = self.detector.detect_opportunities(
            biz,
            audit=audit,
            resolution=res,
            business_categories=["Restaurant", "Food & Beverage"],
        )
        categories = [n.service_category for n in needs]
        assert ServiceCategory.MOBILE_APP in categories

    def test_online_booking_opportunity_for_clinic(self):
        """Clinics and salons without online booking trigger ONLINE_BOOKING."""
        biz = Business(
            name="Metro Dental Care",
            country_code="CA",
            website_url="https://metrodental.ca",
            website_status=WebsiteStatus.FOUND,
        )
        audit = AuditResult(
            url="https://metrodental.ca",
            is_mobile_responsive=True,
            has_viewport_meta=True,
            has_online_booking=False,
        )
        res = ResolutionResult(
            original_url="https://metrodental.ca",
            final_url="https://metrodental.ca",
            is_reachable=True,
            has_ssl=True,
        )

        needs = self.detector.detect_opportunities(
            biz,
            audit=audit,
            resolution=res,
            business_categories=["Dentist", "Health & Wellness"],
        )
        categories = [n.service_category for n in needs]
        assert ServiceCategory.ONLINE_BOOKING in categories

    def test_ecommerce_expansion_for_retail_shop(self):
        """Retail stores without e-commerce cart trigger ECOMMERCE_EXPANSION."""
        biz = Business(
            name="Artisan Leather Goods",
            country_code="DE",
            website_url="https://artisanleather.de",
            website_status=WebsiteStatus.FOUND,
        )
        audit = AuditResult(
            url="https://artisanleather.de",
            is_mobile_responsive=True,
            has_viewport_meta=True,
            has_ecommerce=False,
        )
        res = ResolutionResult(
            original_url="https://artisanleather.de",
            final_url="https://artisanleather.de",
            is_reachable=True,
            has_ssl=True,
        )

        needs = self.detector.detect_opportunities(
            biz,
            audit=audit,
            resolution=res,
            business_categories=["Retail", "General Shop"],
        )
        categories = [n.service_category for n in needs]
        assert ServiceCategory.ECOMMERCE_EXPANSION in categories
