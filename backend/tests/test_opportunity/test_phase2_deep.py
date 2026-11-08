"""
Deep and comprehensive tests for Phase 2 Opportunity Engine enhancements.
Validates:
- Extended CMS, framework, analytics, and widget fingerprinting
- Accessibility and security header auditing
- Schema.org / JSON-LD structured data detection
- Cookie and privacy compliance auditing
- All 7 ServiceCategory detections (including CUSTOM_WEB_APP)
- Commercial ROI valuation and prioritization matrix
"""

import pytest

from backend.app.engines.opportunity.auditor import WebsiteAuditor
from backend.app.engines.opportunity.detector import OpportunityDetector, DetectedNeed
from backend.app.engines.opportunity.resolver import ResolutionResult
from backend.app.engines.opportunity.scorer import OpportunityScorer
from backend.app.models.business import Business, WebsiteStatus
from backend.app.models.opportunity import OpportunityPriority, ServiceCategory


class TestDeepAuditorFeatures:
    """Test the enhanced auditing capabilities."""

    def setup_method(self):
        self.auditor = WebsiteAuditor()

    def test_extended_cms_and_framework_detection(self):
        """Detects Webflow CMS and modern frontend frameworks like Next.js and Tailwind."""
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Modern Tech Startup</title>
            <div data-wf-site="60a7e123" data-wf-page="60a7e124"></div>
            <link rel="stylesheet" href="/_next/static/css/styles.css">
            <div class="flex grid p-4 text-center"></div>
        </head>
        <body>
            <div id="__next">Hello Next</div>
        </body>
        </html>
        """
        result = self.auditor.audit_html("https://startup.io", html)
        assert result.detected_cms == "Webflow"
        assert "Next.js" in result.detected_frameworks
        assert "TailwindCSS" in result.detected_frameworks

    def test_structured_data_json_ld_detection(self):
        """Parses and extracts Schema.org types from JSON-LD scripts."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "name": "Elite Auto Care",
                "telephone": "+1-555-555-5555"
            }
            </script>
        </head>
        <body><h1>Auto Care</h1></body>
        </html>
        """
        result = self.auditor.audit_html("https://eliteautocare.com", html)
        assert result.has_structured_data is True
        assert "LocalBusiness" in result.schema_org_types
        assert "JSON-LD" in result.structured_data_format

    def test_accessibility_auditing(self):
        """Identifies missing alt attributes, missing lang tag, and unlabeled inputs."""
        html = """
        <html>
        <head><title>Test Page</title></head>
        <body>
            <img src="/logo.png">
            <img src="/banner.jpg">
            <form>
                <input type="text" name="customer_query">
            </form>
        </body>
        </html>
        """
        result = self.auditor.audit_html("https://example.com", html)
        assert result.total_images == 2
        assert result.images_without_alt == 2
        issues = [iss["type"] for iss in result.accessibility_issues]
        assert "missing_html_lang" in issues
        assert "missing_image_alt" in issues
        assert "unlabeled_form_inputs" in issues

    def test_security_headers_and_mixed_content_detection(self):
        """Audits security response headers and detects mixed-content assets."""
        headers = {
            "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
        }
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Secure Store</title></head>
        <body>
            <!-- Insecure image on secure domain -->
            <img src="http://insecure-cdn.com/product.jpg">
        </body>
        </html>
        """
        result = self.auditor.audit_html("https://securestore.com", html, headers=headers)
        assert result.has_ssl is True
        assert result.has_hsts is True
        assert result.security_headers["content_security_policy"] is True
        assert result.security_headers["x_frame_options"] is True
        assert result.has_mixed_content is True
        assert "http://insecure-cdn.com/product.jpg" in result.mixed_content_urls

    def test_analytics_and_cookie_consent_detection(self):
        """Detects Google Tag Manager, Meta Pixel, and Cookiebot privacy banner."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://www.googletagmanager.com/gtm.js?id=GTM-XXXX"></script>
            <script src="https://connect.facebook.net/en_US/fbevents.js"></script>
            <script id="Cookiebot" src="https://consent.cookiebot.com/uc.js"></script>
            <title>GDPR Ready Business</title>
        </head>
        <body>
            <a href="/privacy-policy">Privacy Policy</a>
            <a href="/terms-and-conditions">Terms of Service</a>
        </body>
        </html>
        """
        result = self.auditor.audit_html("https://gdprbiz.eu", html)
        assert result.has_analytics is True
        assert "Google Tag Manager" in result.analytics_tools
        assert "Meta Pixel" in result.analytics_tools
        assert result.cookie_consent_detected is True
        assert result.cookie_consent_provider == "Cookiebot"
        assert result.has_privacy_policy is True
        assert result.has_terms_of_service is True


class TestDeepOpportunityDetection:
    """Test deep service opportunity identification across all 7 service lines."""

    def setup_method(self):
        self.detector = OpportunityDetector()

    def test_custom_web_app_detected_for_enterprise_and_logistics(self):
        """Large organizations and logistics companies trigger CUSTOM_WEB_APP."""
        biz = Business(
            name="Apex Global Freight & Logistics",
            country_code="US",
            website_url="https://apexfreight.com",
            website_status=WebsiteStatus.FOUND,
        )
        res = ResolutionResult(
            original_url="https://apexfreight.com",
            final_url="https://apexfreight.com",
            is_reachable=True,
            has_ssl=True,
        )
        audit = WebsiteAuditor().audit_html("https://apexfreight.com", "<html><head><meta name='viewport' content='width=device-width'></head><body><h1>Logistics</h1></body></html>")

        needs = self.detector.detect_opportunities(
            biz, audit=audit, resolution=res, business_categories=["Logistics", "Freight", "Warehousing"]
        )
        categories = [n.service_category for n in needs]
        assert ServiceCategory.CUSTOM_WEB_APP in categories
        custom_need = next(n for n in needs if n.service_category == ServiceCategory.CUSTOM_WEB_APP)
        assert custom_need.estimated_value_usd >= 20000.0
        assert any("portal" in p.lower() for p in custom_need.pitch_angles)

    def test_seo_performance_opportunity_triggered_by_missing_metadata(self):
        """Pages missing meta title, description, and structured data trigger SEO_PERFORMANCE."""
        biz = Business(
            name="Downtown Bakery",
            country_code="CA",
            website_url="https://downtownbakery.ca",
            website_status=WebsiteStatus.FOUND,
        )
        res = ResolutionResult(
            original_url="https://downtownbakery.ca",
            final_url="https://downtownbakery.ca",
            is_reachable=True,
            has_ssl=True,
        )
        # HTML with no title, no meta description, and 2 H1 tags
        html = "<html><body><h1>First Heading</h1><h1>Second Heading</h1><p>Welcome</p></body></html>"
        audit = WebsiteAuditor().audit_html("https://downtownbakery.ca", html)

        needs = self.detector.detect_opportunities(
            biz, audit=audit, resolution=res, business_categories=["Bakery"]
        )
        categories = [n.service_category for n in needs]
        assert ServiceCategory.SEO_PERFORMANCE in categories
        seo_need = next(n for n in needs if n.service_category == ServiceCategory.SEO_PERFORMANCE)
        assert len(seo_need.evidence["deficiencies"]) >= 3


class TestDeepOpportunityScoring:
    """Test commercial valuation, confidence calculations, and recommendations."""

    def setup_method(self):
        self.scorer = OpportunityScorer()

    def test_commercial_valuation_and_recommended_actions(self):
        """Validates valuation multipliers, ROI summaries, and recommended actions."""
        biz = Business(
            name="Prestige Beverly Hills Dental",
            country_code="US",
            phone="+13105550100",
            email="dr@beverlyhillsdental.com",
        )
        need = DetectedNeed(
            service_category=ServiceCategory.WEBSITE_REDESIGN,
            title="Redesign for Beverly Hills Dental",
            summary="Website is not mobile responsive.",
            evidence={"mobile_responsive": False},
            pitch_angles=["Improve conversion"],
            need_severity=0.90,
        )

        scored = self.scorer.score_need(need, biz, ["Dentist", "Medical"])

        # Dental in US has premium tier + US multiplier
        assert scored.estimated_value_low >= 5000.0
        assert scored.estimated_value_high >= 20000.0
        assert scored.priority == OpportunityPriority.CRITICAL
        assert "immediate" in scored.recommended_action.lower()
        assert "Estimated project value" in scored.roi_summary
        assert scored.confidence >= 0.85
