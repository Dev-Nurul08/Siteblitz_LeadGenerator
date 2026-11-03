"""
Tests for ContactClassifier (Phase 3).
"""

from backend.app.engines.enrichment.classifier import ContactClassifier
from backend.app.models.contact import RoleLevel


class TestContactClassifier:
    """Test suite for ContactClassifier."""

    def setup_method(self):
        self.classifier = ContactClassifier()

    def test_name_parsing_with_honorifics(self):
        """Strips Dr./Mr./Ms. and separates first and last names."""
        res1 = self.classifier.classify_contact(full_name="Dr. Marcus Vance", job_title="CEO")
        assert res1.first_name == "Marcus"
        assert res1.last_name == "Vance"
        assert res1.full_name == "Marcus Vance"
        assert res1.role_level == RoleLevel.EXECUTIVE

        res2 = self.classifier.classify_contact(full_name="Ms. Claire Dupont", job_title="Operations Director")
        assert res2.first_name == "Claire"
        assert res2.last_name == "Dupont"
        assert res2.role_level == RoleLevel.MANAGEMENT

    def test_executive_role_classification(self):
        """Classifies Founders, CEOs, and Owners as EXECUTIVE."""
        titles = [
            "Founder & CEO",
            "Co-Founder",
            "Managing Director",
            "President",
            "Owner & Principal",
        ]
        for t in titles:
            res = self.classifier.classify_contact(job_title=t)
            assert res.role_level == RoleLevel.EXECUTIVE, f"Failed on title: {t}"

    def test_technical_role_classification(self):
        """Classifies CTOs and Engineers as TECHNICAL."""
        titles = [
            "Chief Technology Officer",
            "CTO",
            "Lead Developer",
            "IT Systems Architect",
            "Webmaster",
        ]
        for t in titles:
            res = self.classifier.classify_contact(job_title=t)
            assert res.role_level == RoleLevel.TECHNICAL, f"Failed on title: {t}"

    def test_marketing_role_classification(self):
        """Classifies CMOs and Marketing Managers as MARKETING."""
        titles = [
            "Chief Marketing Officer",
            "CMO",
            "Head of Marketing",
            "Digital Marketing Manager",
            "Growth Lead",
        ]
        for t in titles:
            res = self.classifier.classify_contact(job_title=t)
            assert res.role_level == RoleLevel.MARKETING, f"Failed on title: {t}"

    def test_general_inbox_classification(self):
        """Classifies role addresses like info@ and contact@ as GENERAL_INBOX."""
        res_info = self.classifier.classify_contact(email="info@bakery.com")
        assert res_info.role_level == RoleLevel.GENERAL_INBOX

        res_contact = self.classifier.classify_contact(email="contact@agency.co.uk")
        assert res_contact.role_level == RoleLevel.GENERAL_INBOX
