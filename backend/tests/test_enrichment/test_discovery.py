"""
Tests for ContactDiscoveryEngine (Phase 3).
"""

import pytest

from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine
from backend.app.models.business import Business
from backend.app.models.opportunity import WebsiteAudit


class TestContactDiscoveryEngine:
    """Test suite for ContactDiscoveryEngine."""

    def setup_method(self):
        self.engine = ContactDiscoveryEngine()

    def test_extract_domain(self):
        """Extracts clean apex domain from various URL formats."""
        assert self.engine._extract_domain("https://www.apple.com/store") == "apple.com"
        assert self.engine._extract_domain("http://nordictech.se") == "nordictech.se"
        assert self.engine._extract_domain("sub.agency.co.uk") == "sub.agency.co.uk"
        assert self.engine._extract_domain("") is None

    def test_extract_from_html(self):
        """Extracts mailto links and regex emails from HTML."""
        html = """
        <html>
        <body>
            <h1>Get in Touch</h1>
            <p>Write directly to <a href="mailto:david@consulting.com">David Kim</a></p>
            <p>Or send general questions to info@consulting.com</p>
        </body>
        </html>
        """
        contacts = self.engine._extract_from_html(html, "https://consulting.com/contact")
        emails = [c.email for c in contacts]

        assert "david@consulting.com" in emails
        assert "info@consulting.com" in emails
        david_contact = next(c for c in contacts if c.email == "david@consulting.com")
        assert david_contact.full_name == "David Kim"

    @pytest.mark.asyncio
    async def test_merge_with_audit_emails(self):
        """Pulls contacts identified in prior technical audits."""
        biz = Business(
            name="Apex Dynamics",
            country_code="US",
            website_url="https://apexdynamics.com",
            email=None,
        )
        audit = WebsiteAudit(
            business_id=1,
            url_analyzed="https://apexdynamics.com",
            is_reachable=True,
            emails_found={"emails": ["contact@apexdynamics.com", "billing@apexdynamics.com"]},
        )

        contacts = await self.engine.discover_contacts(biz, audit=audit)
        emails = [c.email for c in contacts]

        assert "contact@apexdynamics.com" in emails
        assert "billing@apexdynamics.com" in emails

    @pytest.mark.asyncio
    async def test_synthetic_fallback_email(self):
        """Generates info@{domain} fallback when no explicit email found."""
        biz = Business(
            name="Boutique Hotel Alpha",
            country_code="CH",
            website_url="https://hotelalpha.ch",
            email=None,
        )
        contacts = await self.engine.discover_contacts(biz, audit=None)
        emails = [c.email for c in contacts]

        assert "info@hotelalpha.ch" in emails
        fallback = next(c for c in contacts if c.email == "info@hotelalpha.ch")
        assert fallback.source_method == "corporate_domain_default"
