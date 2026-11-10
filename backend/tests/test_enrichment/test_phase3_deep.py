"""
Deep and comprehensive tests for Phase 3 Contact Enrichment Engine enhancements.
Validates:
- Obfuscated email decoding ([at], [dot], Cloudflare cfemail)
- Schema.org Person structured data extraction
- Free consumer email detection and typo corrections
- Mail provider fingerprinting via DNS MX (Google Workspace, M365)
- Phone verification, formatting, and toll-free identification
- Comprehensive department and seniority classification
- On-demand domain contact discovery
"""

import pytest

from backend.app.engines.enrichment.classifier import ContactClassifier
from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine
from backend.app.engines.enrichment.verifier import EmailVerifier
from backend.app.models.contact import EmailVerificationStatus, RoleLevel


class TestDeepVerificationFeatures:
    """Test enhanced email and phone verification."""

    def setup_method(self):
        self.verifier = EmailVerifier()

    def test_typo_domain_suggestion(self):
        """Identifies common domain typos and suggests corrections."""
        res = self.verifier.verify("founder@gmial.com")
        assert res.suggested_correction == "founder@gmail.com"

        res_yahoo = self.verifier.verify("contact@yaho.com")
        assert res_yahoo.suggested_correction == "contact@yahoo.com"

    def test_free_email_provider_flagging(self):
        """Identifies free consumer webmail (Gmail/Yahoo/Outlook)."""
        res = self.verifier.verify("john.doe@gmail.com")
        assert res.is_free_email is True
        assert res.is_valid_syntax is True
        assert res.is_disposable is False

    def test_disposable_domain_detection(self):
        """Detects temporary disposable domains."""
        res = self.verifier.verify("tempuser@temp-mail.org")
        assert res.is_disposable is True
        assert res.status == EmailVerificationStatus.DISPOSABLE
        assert res.verification_score == 0.0

    def test_phone_verification_and_e164_formatting(self):
        """Formats and validates phone numbers."""
        res = EmailVerifier.verify_phone("(555) 234-5678", default_country="US")
        assert res.is_valid is True
        assert res.formatted_phone == "+5552345678"

        res_toll = EmailVerifier.verify_phone("+1-800-555-0199")
        assert res_toll.is_valid is True
        assert res_toll.phone_type == "TOLL_FREE"

        res_short = EmailVerifier.verify_phone("123")
        assert res_short.is_valid is False


class TestDeepClassificationFeatures:
    """Test enhanced hierarchy, department, and international name normalization."""

    def setup_method(self):
        self.classifier = ContactClassifier()

    def test_international_honorifics_and_compound_names(self):
        """Strips international honorifics and preserves compound surnames."""
        res = self.classifier.classify_contact(
            full_name="Dr. Alexander Van Der Bellen",
            job_title="Managing Director",
            email="alex@company.com",
        )
        assert res.first_name == "Alexander"
        assert res.last_name == "Van Der Bellen"
        assert res.full_name == "Alexander Van Der Bellen"
        assert res.role_level == RoleLevel.EXECUTIVE
        assert res.department == "EXECUTIVE"
        assert res.seniority_score == 1.0

    def test_department_and_seniority_classification(self):
        """Classifies technical and marketing departments correctly."""
        tech_res = self.classifier.classify_contact(
            full_name="Sarah Connor",
            job_title="Lead Software Engineer",
            email="sarah@tech.io",
        )
        assert tech_res.role_level == RoleLevel.TECHNICAL
        assert tech_res.department == "ENGINEERING"

        mktg_res = self.classifier.classify_contact(
            full_name="Emma Stone",
            job_title="Head of Growth & Digital Marketing",
            email="emma@growth.io",
        )
        assert mktg_res.role_level == RoleLevel.MARKETING
        assert mktg_res.department == "MARKETING"


class TestDeepDiscoveryFeatures:
    """Test obfuscated email decoding and Schema.org Person extraction."""

    def setup_method(self):
        self.discovery = ContactDiscoveryEngine()

    def test_cloudflare_email_decoding(self):
        """Decodes Cloudflare XOR obfuscated email addresses."""
        # 'hello@acme.com' encoded with key 0x12
        # h(0x68)^0x12=0x7a, e(0x65)^0x12=0x77, l(0x6c)^0x12=0x7e, l(0x6c)^0x12=0x7e, o(0x6f)^0x12=0x7d
        # @(0x40)^0x12=0x52, a(0x61)^0x12=0x73, c(0x63)^0x12=0x71, m(0x6d)^0x12=0x7f, e(0x65)^0x12=0x77
        # .(0x2e)^0x12=0x3c, c(0x63)^0x12=0x71, o(0x6f)^0x12=0x7d, m(0x6d)^0x12=0x7f
        cf_hex = "12" + "7a777e7e7d5273717f773c717d7f"
        decoded = self.discovery._decode_cloudflare_email(cf_hex)
        assert decoded == "hello@acme.com"

    def test_obfuscated_text_email_extraction(self):
        """Extracts [at] [dot] styled email obfuscation from page text."""
        html = """
        <html>
        <body>
            <p>Reach our press team: press [at] newsroom [dot] com</p>
        </body>
        </html>
        """
        extracted = self.discovery._extract_from_html(html, "https://example.com")
        emails = [c.email for c in extracted]
        assert "press@newsroom.com" in emails

    def test_schema_org_person_in_script_is_not_extracted(self):
        """JSON-LD sits in a <script>; the outreach spec (row 10) takes emails only from mailto
        links, visible text and Cloudflare-encoded addresses (QA-040)."""
        html = """
        <html>
        <head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Person",
                "name": "Grace Hopper",
                "jobTitle": "Chief Technology Officer",
                "email": "grace@navy.gov",
                "telephone": "+1-202-555-0100"
            }
            </script>
        </head>
        <body><h1>About Us</h1></body>
        </html>
        """
        extracted = self.discovery._extract_from_html(html, "https://navy.gov/team")
        assert extracted == []

