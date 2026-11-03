"""
Tests for WebsiteAuditor (Phase 2).
"""

from backend.app.engines.opportunity.auditor import WebsiteAuditor


class TestWebsiteAuditor:
    """Test suite for WebsiteAuditor."""

    def setup_method(self):
        self.auditor = WebsiteAuditor()

    def test_mobile_responsive_detection(self):
        """Detects presence of viewport meta tag."""
        responsive_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Modern Responsive Business</title>
        </head>
        <body><h1>Welcome</h1></body>
        </html>
        """
        result = self.auditor.audit_html("https://example.com", responsive_html)
        assert result.is_mobile_responsive is True
        assert result.has_viewport_meta is True

    def test_non_responsive_detection(self):
        """Identifies obsolete websites lacking viewport meta tag."""
        obsolete_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Old Table Based Website</title>
        </head>
        <body><table><tr><td>Old content</td></tr></table></body>
        </html>
        """
        result = self.auditor.audit_html("https://example.com", obsolete_html)
        assert result.is_mobile_responsive is False
        assert result.has_viewport_meta is False

    def test_cms_detection_wordpress(self):
        """Detects WordPress CMS from assets and meta generator."""
        wp_html = """
        <html>
        <head>
            <meta name="generator" content="WordPress 6.4">
            <link rel="stylesheet" href="/wp-content/themes/custom/style.css">
        </head>
        <body><h1>Blog</h1></body>
        </html>
        """
        result = self.auditor.audit_html("https://example.com", wp_html)
        assert result.detected_cms == "WordPress"

    def test_cms_detection_shopify(self):
        """Detects Shopify e-commerce platform."""
        shopify_html = """
        <html>
        <head>
            <script src="https://cdn.shopify.com/s/files/1/0000/theme.js"></script>
        </head>
        <body><button class="add-to-cart">Buy Now</button></body>
        </html>
        """
        result = self.auditor.audit_html("https://shop.example.com", shopify_html)
        assert result.detected_cms == "Shopify"
        assert result.has_ecommerce is True

    def test_online_booking_detection(self):
        """Detects booking/scheduling widgets."""
        booking_html = """
        <html>
        <head><title>Dental Care</title></head>
        <body>
            <h1>Smile Clinic</h1>
            <a href="https://calendly.com/smileclinic/30min">Book an appointment online</a>
        </body>
        </html>
        """
        result = self.auditor.audit_html("https://smileclinic.com", booking_html)
        assert result.has_online_booking is True

    def test_contact_signals_extraction(self):
        """Extracts visible emails, telephone numbers, and social links."""
        contact_html = """
        <html>
        <head><title>Contact Us</title></head>
        <body>
            <p>Email us at: <a href="mailto:hello@acmeagency.com">hello@acmeagency.com</a></p>
            <p>Direct line: <a href="tel:+1234567890">+1 (234) 567-890</a></p>
            <footer>
                <a href="https://www.linkedin.com/company/acmeagency">LinkedIn</a>
                <a href="https://instagram.com/acmeagency">Instagram</a>
            </footer>
        </body>
        </html>
        """
        result = self.auditor.audit_html("https://acmeagency.com", contact_html)
        assert "hello@acmeagency.com" in result.emails_found
        assert "+1234567890" in result.phones_found
        assert "linkedin" in result.social_links_found
        assert "instagram" in result.social_links_found

    def test_seo_headings_audit(self):
        """Analyzes SEO heading hierarchy and title tag."""
        seo_html = """
        <html>
        <head>
            <title>Premier Law Firm in London | Expert Solicitors</title>
            <meta name="description" content="Award-winning legal advisors providing corporate and litigation counsel.">
        </head>
        <body>
            <h1>Leading Corporate Law Advisory</h1>
            <h2>Corporate Mergers</h2>
            <h2>Commercial Litigation</h2>
        </body>
        </html>
        """
        result = self.auditor.audit_html("https://lawfirm.example.com", seo_html)
        assert result.meta_title == "Premier Law Firm in London | Expert Solicitors"
        assert result.meta_description == "Award-winning legal advisors providing corporate and litigation counsel."
        assert result.headings_summary["h1_count"] == 1
        assert result.headings_summary["h2_count"] == 2
        assert "Leading Corporate Law" in result.headings_summary["h1_text"]
