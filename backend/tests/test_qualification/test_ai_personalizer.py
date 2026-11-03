"""
Tests for AIPersonalizer (Phase 4).
"""

from backend.app.engines.qualification.ai_personalizer import AIPersonalizer
from backend.app.models.business import Business, BusinessCategory, BusinessLocation
from backend.app.models.contact import Contact, RoleLevel
from backend.app.models.opportunity import Opportunity, OpportunityPriority, ServiceCategory


class TestAIPersonalizer:
    """Test suite for AI personalized pitch generation."""

    def setup_method(self):
        self.personalizer = AIPersonalizer()
        self.business = Business(
            id=1,
            name="Bella Trattoria",
            country_code="US",
            website_url="https://bellatrattoria.com",
        )
        self.business.locations = [BusinessLocation(city="Boston")]
        self.business.categories = [BusinessCategory(category_name="Restaurant", source_category="restaurant")]
        self.contact = Contact(
            id=1,
            business_id=1,
            first_name="Marco",
            full_name="Marco Rossi",
            email="marco@bellatrattoria.com",
            role_level=RoleLevel.EXECUTIVE,
        )

    def test_new_website_pitch_generation(self):
        """Generates dedicated website creation pitch when business has no website."""
        opp = Opportunity(
            id=1,
            business_id=1,
            service_category=ServiceCategory.NEW_WEBSITE,
            priority=OpportunityPriority.CRITICAL,
        )
        res = self.personalizer.generate_pitch(self.business, self.contact, opp)
        assert "Marco" in res.body_text
        assert "Bella Trattoria" in res.subject_line
        assert "doesn't have a dedicated website" in res.body_text
        assert "{{UNSUBSCRIBE_LINK}}" in res.body_text
        assert "100 Innovation Way" in res.body_text

    def test_mobile_redesign_pitch_generation(self):
        """Generates mobile responsiveness pitch when website is broken on smartphones."""
        opp = Opportunity(
            id=2,
            business_id=1,
            service_category=ServiceCategory.WEBSITE_REDESIGN,
            priority=OpportunityPriority.HIGH,
        )
        res = self.personalizer.generate_pitch(self.business, self.contact, opp)
        assert "mobile screens" in res.body_text
        assert "smartphone" in res.body_text
        assert "{{UNSUBSCRIBE_LINK}}" in res.body_text

    def test_online_booking_pitch_generation(self):
        """Generates appointment scheduling engine pitch for service clinics and salons."""
        opp = Opportunity(
            id=3,
            business_id=1,
            service_category=ServiceCategory.ONLINE_BOOKING,
            priority=OpportunityPriority.HIGH,
        )
        res = self.personalizer.generate_pitch(self.business, self.contact, opp)
        assert "booking" in res.subject_line.lower()
        assert "book appointments" in res.body_text.lower()
        assert "{{UNSUBSCRIBE_LINK}}" in res.body_text

    def test_mobile_app_pitch_generation(self):
        """Generates mobile app & loyalty pitch for repeat customer businesses."""
        opp = Opportunity(
            id=4,
            business_id=1,
            service_category=ServiceCategory.MOBILE_APP,
            priority=OpportunityPriority.HIGH,
        )
        res = self.personalizer.generate_pitch(self.business, self.contact, opp)
        assert "mobile app" in res.body_text.lower()
        assert "reordering" in res.body_text.lower()
        assert "{{UNSUBSCRIBE_LINK}}" in res.body_text
