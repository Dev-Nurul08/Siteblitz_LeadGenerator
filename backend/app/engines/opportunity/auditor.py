"""
Website Auditor module (Phase 2).

Performs deep technical, accessibility, security, and capability inspection of business websites.
Fingerprints CMS, frameworks, mobile responsiveness, e-commerce, booking widgets,
SEO hygiene, structured data, analytics, privacy compliance, and contact signals.
"""

from dataclasses import dataclass, field
import json
import re
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import structlog

logger = structlog.get_logger(__name__)

# ─── Signatures ─────────────────────────────────────────────────────────────

CMS_SIGNATURES: dict[str, list[str]] = {
    "WordPress": [
        r"wp-content",
        r"wp-includes",
        r'<meta name="generator" content="WordPress',
        r"/wp-json/",
        r"elementor",
    ],
    "Shopify": [
        r"cdn\.shopify\.com",
        r"Shopify\.theme",
        r"myshopify\.com",
        r"Shopify\.routes",
    ],
    "Wix": [
        r"wix\.com",
        r"wix-warmup-data",
        r"_wix_browser_sess",
        r"static\.wixstatic\.com",
        r"wix-thunderbolt",
    ],
    "Squarespace": [
        r"static1\.squarespace\.com",
        r"squarespace\.com",
        r"SQUARESPACE_CONTEXT",
        r'<meta name="generator" content="Squarespace',
    ],
    "Webflow": [
        r"data-wf-page",
        r"data-wf-site",
        r"webflow\.com",
        r"assets\.website-files\.com",
    ],
    "Joomla": [
        r"/media/system/js/",
        r"/templates/[a-z0-9_-]+/",
        r'<meta name="generator" content="Joomla',
    ],
    "Drupal": [
        r"Drupal\.settings",
        r"/sites/default/files/",
        r'<meta name="generator" content="Drupal',
        r"drupal-settings-json",
    ],
    "Ghost": [
        r"ghost\.org",
        r'<meta name="generator" content="Ghost',
        r"ghost-portal",
    ],
    "HubSpot CMS": [
        r"hs-scripts\.com",
        r"hubspot\.com",
        r"hs-content-id",
    ],
    "PrestaShop": [
        r"prestashop",
        r"/modules/prestashop",
        r'<meta name="generator" content="PrestaShop',
    ],
    "Magento": [
        r"/skin/frontend/",
        r"/static/version[0-9]+/",
        r"Mage\.Cookies",
        r"mage/cookies",
    ],
    "BigCommerce": [
        r"cdn\.bigcommerce\.com",
        r"bigcommerce\.com",
    ],
    "Weebly": [
        r"weebly\.com",
        r"editmysite\.com",
    ],
    "Duda": [
        r"duda\.co",
        r"le-cdn\.website-editor\.net",
    ],
    "GoDaddy": [
        r"godaddy\.com",
        r"secureserver\.net",
    ],
}

FRAMEWORK_SIGNATURES: dict[str, list[str]] = {
    "Next.js": [r"/_next/static/", r"__NEXT_DATA__", r"id=\"__next\""],
    "Nuxt.js": [r"/_nuxt/", r"__NUXT__", r"id=\"__nuxt\""],
    "React": [r"data-reactroot", r"_reactListening", r"react\.production\.min\.js"],
    "Vue": [r"data-v-[a-z0-9]+", r"vue\.runtime", r"vue\.global"],
    "Angular": [r"ng-version", r"ng-app", r"<app-root"],
    "Svelte": [r"svelte-[a-z0-9]+", r"/_app/immutable/"],
    "jQuery": [r"jquery[\.-][0-9]", r"jquery\.min\.js", r"\$\.fn\.jquery"],
    "Bootstrap": [r"bootstrap(?:\.min)?\.(?:css|js)", r"class=\"[^\"]*col-(?:xs|sm|md|lg|xl)-"],
    "TailwindCSS": [r"tailwindcss", r"class=\"[^\"]*(?:flex|grid|p-[0-9]|text-[a-z]+)[^\"]*\""],
    "Alpine.js": [r"x-data", r"x-init", r"alpine(?:\.min)?\.js"],
    "HTMX": [r"hx-get", r"hx-post", r"htmx\.org"],
    "Astro": [r"astro-island", r"astro-root"],
}

BOOKING_SIGNATURES: dict[str, list[str]] = {
    "Calendly": [r"calendly\.com"],
    "Acuity Scheduling": [r"acuityscheduling\.com"],
    "Booksy": [r"booksy\.com"],
    "OpenTable": [r"opentable\.com"],
    "Resy": [r"resy\.com"],
    "Setmore": [r"setmore\.com"],
    "Fresha": [r"fresha\.com"],
    "Appointlet": [r"appointlet\.com"],
    "TidyCal": [r"tidycal\.com"],
    "SimplyBook": [r"simplybook\.me"],
    "Bookeo": [r"bookeo\.com"],
    "Treatwell": [r"treatwell\.com"],
    "Vagaro": [r"vagaro\.com"],
    "Mindbody": [r"mindbodyonline\.com"],
    "Booker": [r"booker\.com"],
}

ECOMMERCE_SIGNATURES: dict[str, list[str]] = {
    "Shopify": [r"cdn\.shopify\.com", r"shopify"],
    "WooCommerce": [r"woocommerce", r"wc-api"],
    "BigCommerce": [r"bigcommerce"],
    "Magento": [r"mage/cookies", r"magento"],
    "PrestaShop": [r"prestashop"],
    "Ecwid": [r"ecwid\.com"],
    "Stripe Checkout": [r"js\.stripe\.com/v3", r"stripe-checkout"],
    "PayPal": [r"paypal\.com/sdk", r"paypalobjects\.com"],
    "Square Online": [r"squareup\.com", r"square-online"],
    "Snipcart": [r"snipcart\.com"],
}

ANALYTICS_SIGNATURES: dict[str, list[str]] = {
    "Google Tag Manager": [r"googletagmanager\.com/gtm\.js", r"gtm-[a-z0-9]+"],
    "Google Analytics 4": [r"googletagmanager\.com/gtag/js\?id=G-", r"gtag\(['\"]config['\"],\s*['\"]G-"],
    "Universal Analytics": [r"google-analytics\.com/analytics\.js", r"['\"]UA-[0-9]+-[0-9]+['\"]"],
    "Meta Pixel": [r"connect\.facebook\.net/en_US/fbevents\.js", r"fbq\(['\"]init['\"]"],
    "LinkedIn Insight": [r"snap\.licdn\.com/li\.lms-analytics/insight\.min\.js"],
    "TikTok Pixel": [r"analytics\.tiktok\.com/i18n/pixel"],
    "Hotjar": [r"static\.hotjar\.com/c/hotjar-"],
    "Microsoft Clarity": [r"clarity\.ms/tag/"],
    "Segment": [r"cdn\.segment\.com/analytics\.js"],
    "Plausible": [r"plausible\.io/js/script"],
    "Mixpanel": [r"cdn\.mxpnl\.com/libs/mixpanel"],
}

CHAT_WIDGET_SIGNATURES: dict[str, list[str]] = {
    "Intercom": [r"widget\.intercom\.io"],
    "Zendesk": [r"static\.zdassets\.com", r"zopim\.com"],
    "LiveChat": [r"cdn\.livechatinc\.com"],
    "Drift": [r"js\.driftt\.com"],
    "Crisp": [r"client\.crisp\.chat"],
    "Tidio": [r"code\.tidio\.co"],
    "Tawk.to": [r"embed\.tawk\.to"],
    "WhatsApp": [r"api\.whatsapp\.com/send", r"wa\.me/"],
    "HubSpot Chat": [r"js\.usemessages\.com"],
}

PRIVACY_CONSENT_SIGNATURES: dict[str, list[str]] = {
    "Cookiebot": [r"consent\.cookiebot\.com"],
    "OneTrust": [r"cdn\.cookielaw\.org", r"onetrust\.com"],
    "TrustArc": [r"trustarc\.com"],
    "CookieYes": [r"cdn-cookieyes\.com"],
    "Iubenda": [r"iubenda\.com"],
    "Osano": [r"osano\.com"],
    "Termly": [r"app\.termly\.io"],
}

SOCIAL_PROOF_SIGNATURES: dict[str, list[str]] = {
    "Trustpilot": [r"trustpilot\.com", r"widget\.trustpilot\.com"],
    "Google Reviews": [r"google\.com/maps/place", r"elfsight\.com/google-reviews", r"tagembed"],
    "Yelp Badge": [r"yelp\.com/biz"],
    "Feefo": [r"api\.feefo\.com"],
    "Reviews.io": [r"widget\.reviews\.io"],
}


# ─── Dataclass ──────────────────────────────────────────────────────────────

@dataclass
class AuditResult:
    """Comprehensive structural and technical findings from analyzing a business website."""

    url: str
    is_mobile_responsive: bool = False
    has_viewport_meta: bool = False
    viewport_content: Optional[str] = None

    # Tech Stack
    detected_cms: Optional[str] = None
    cms_version_hint: Optional[str] = None
    detected_frameworks: list[str] = field(default_factory=list)
    detected_libraries: list[str] = field(default_factory=list)

    # Capabilities
    has_ecommerce: bool = False
    ecommerce_platform: Optional[str] = None
    has_online_booking: bool = False
    booking_platform: Optional[str] = None
    has_contact_form: bool = False
    form_count: int = 0
    has_analytics: bool = False
    analytics_tools: list[str] = field(default_factory=list)

    # SEO & Headings
    meta_title: Optional[str] = None
    meta_title_length: int = 0
    meta_description: Optional[str] = None
    meta_description_length: int = 0
    canonical_url: Optional[str] = None
    headings_summary: dict = field(default_factory=dict)
    has_robots_meta: bool = False
    robots_directives: Optional[str] = None
    og_tags: dict[str, str] = field(default_factory=dict)
    twitter_cards: dict[str, str] = field(default_factory=dict)

    # Contact Info
    emails_found: list[str] = field(default_factory=list)
    phones_found: list[str] = field(default_factory=list)
    social_links_found: dict[str, str] = field(default_factory=dict)

    # Security & Headers
    has_ssl: bool = False
    has_hsts: bool = False
    has_mixed_content: bool = False
    mixed_content_urls: list[str] = field(default_factory=list)
    security_headers: dict[str, bool] = field(default_factory=dict)

    # Accessibility
    accessibility_issues: list[dict] = field(default_factory=list)
    total_images: int = 0
    images_without_alt: int = 0

    # Structured Data
    has_structured_data: bool = False
    schema_org_types: list[str] = field(default_factory=list)
    structured_data_format: list[str] = field(default_factory=list)

    # Compliance & Extras
    cookie_consent_detected: bool = False
    cookie_consent_provider: Optional[str] = None
    has_privacy_policy: bool = False
    has_terms_of_service: bool = False
    chat_widget: bool = False
    chat_provider: Optional[str] = None
    social_proof_widgets: list[str] = field(default_factory=list)

    # Performance Indicators
    dom_element_count: int = 0
    script_count: int = 0
    stylesheet_count: int = 0
    inline_style_count: int = 0

    raw_technologies: dict = field(default_factory=dict)


# ─── WebsiteAuditor ─────────────────────────────────────────────────────────

class WebsiteAuditor:
    """
    Analyzes website HTML and HTTP headers to produce an in-depth audit report.
    """

    def audit_html(
        self,
        url: str,
        html_content: str,
        headers: Optional[dict] = None,
        original_url: Optional[str] = None,
        final_url: Optional[str] = None,
    ) -> AuditResult:
        """
        Inspect raw HTML and response headers of a business website and extract all signals.
        """
        if not html_content:
            return AuditResult(url=url)

        headers = headers or {}
        soup = BeautifulSoup(html_content, "html.parser")
        text_lower = html_content.lower()

        # 1. Mobile Responsiveness / Viewport
        viewport_tag = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
        has_viewport = False
        is_responsive = False
        viewport_content = None
        if viewport_tag and viewport_tag.get("content"):
            viewport_content = str(viewport_tag["content"]).strip()
            content_lower = viewport_content.lower()
            if "width=device-width" in content_lower or "initial-scale=1" in content_lower:
                has_viewport = True
                is_responsive = True

        # 2. Meta Tags (SEO Basics)
        title_tag = soup.find("title")
        meta_title = title_tag.get_text(strip=True) if title_tag else None
        meta_title_len = len(meta_title) if meta_title else 0

        desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        meta_desc = desc_tag.get("content", "").strip() if desc_tag else None
        meta_desc_len = len(meta_desc) if meta_desc else 0

        canonical_tag = soup.find("link", attrs={"rel": re.compile(r"^canonical$", re.I)})
        canonical_url = canonical_tag.get("href", "").strip() if canonical_tag else None

        robots_tag = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
        has_robots_meta = bool(robots_tag)
        robots_directives = robots_tag.get("content", "").strip() if robots_tag else None

        # Open Graph & Twitter Cards
        og_tags: dict[str, str] = {}
        for tag in soup.find_all("meta", property=re.compile(r"^og:", re.I)):
            prop = tag.get("property", "").lower()
            val = tag.get("content", "").strip()
            if prop and val:
                og_tags[prop] = val

        twitter_cards: dict[str, str] = {}
        for tag in soup.find_all("meta", attrs={"name": re.compile(r"^twitter:", re.I)}):
            name = tag.get("name", "").lower()
            val = tag.get("content", "").strip()
            if name and val:
                twitter_cards[name] = val

        # 3. Heading Structure
        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")
        h3_tags = soup.find_all("h3")
        headings_summary = {
            "h1_count": len(h1_tags),
            "h2_count": len(h2_tags),
            "h3_count": len(h3_tags),
            "h1_text": h1_tags[0].get_text(strip=True)[:150] if h1_tags else None,
        }

        # 4. CMS Detection
        detected_cms = None
        cms_version_hint = None
        for cms_name, patterns in CMS_SIGNATURES.items():
            for pat in patterns:
                if re.search(pat, html_content, re.IGNORECASE):
                    detected_cms = cms_name
                    break
            if detected_cms:
                break

        # Check generator meta for version hint
        generator_tag = soup.find("meta", attrs={"name": re.compile(r"^generator$", re.I)})
        if generator_tag and generator_tag.get("content"):
            gen_content = generator_tag["content"].strip()
            cms_version_hint = gen_content
            if not detected_cms:
                for candidate in CMS_SIGNATURES.keys():
                    if candidate.lower() in gen_content.lower():
                        detected_cms = candidate
                        break

        # 5. Frameworks & Libraries Detection
        detected_frameworks = []
        for framework, patterns in FRAMEWORK_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                detected_frameworks.append(framework)

        # 6. E-Commerce Detection
        has_ecommerce = False
        ecommerce_platform = None
        for platform, patterns in ECOMMERCE_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                has_ecommerce = True
                ecommerce_platform = platform
                break

        if not has_ecommerce:
            if soup.find(attrs={"class": re.compile(r"(cart|checkout|woocommerce|shopping-bag)", re.I)}):
                has_ecommerce = True
                ecommerce_platform = "Generic Cart"

        # 7. Online Booking Detection
        has_online_booking = False
        booking_platform = None
        for platform, patterns in BOOKING_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                has_online_booking = True
                booking_platform = platform
                break

        if not has_online_booking:
            # Generic booking phrasing
            generic_booking = [
                r"book an appointment",
                r"schedule a consultation",
                r"reserve a table",
                r"book-online",
                r"appointment-calendar",
            ]
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in generic_booking):
                has_online_booking = True
                booking_platform = "Custom Booking"

        # 8. Contact Form Detection
        forms = soup.find_all("form")
        form_count = len(forms)
        has_contact_form = False
        for form in forms:
            inputs = form.find_all(["input", "textarea"])
            types = [inp.get("type", "").lower() for inp in inputs]
            names = [str(inp.get("name", "")).lower() for inp in inputs]
            if "email" in types or any("email" in n for n in names) or form.find("textarea"):
                has_contact_form = True
                break

        # 9. Analytics Detection
        analytics_tools = []
        for tool_name, patterns in ANALYTICS_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                analytics_tools.append(tool_name)
        has_analytics = len(analytics_tools) > 0

        # 10. Live Chat & Support
        chat_widget = False
        chat_provider = None
        for provider, patterns in CHAT_WIDGET_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                chat_widget = True
                chat_provider = provider
                break

        # 11. Privacy & Cookie Consent
        cookie_consent_detected = False
        cookie_consent_provider = None
        for provider, patterns in PRIVACY_CONSENT_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                cookie_consent_detected = True
                cookie_consent_provider = provider
                break

        has_privacy_policy = bool(
            soup.find("a", href=re.compile(r"privacy", re.I))
            or re.search(r"privacy policy", text_lower)
        )
        has_terms_of_service = bool(
            soup.find("a", href=re.compile(r"(terms|conditions|tos)", re.I))
            or re.search(r"terms (?:and|of) (?:service|conditions)", text_lower)
        )

        # 12. Social Proof
        social_proof_widgets = []
        for provider, patterns in SOCIAL_PROOF_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                social_proof_widgets.append(provider)

        # 13. Accessibility Checks
        images = soup.find_all("img")
        total_images = len(images)
        images_without_alt = sum(1 for img in images if not img.get("alt"))
        accessibility_issues = []

        if not soup.find("html", attrs={"lang": True}):
            accessibility_issues.append({"type": "missing_html_lang", "severity": "medium", "message": "HTML tag missing lang attribute"})

        if images_without_alt > 0:
            accessibility_issues.append({
                "type": "missing_image_alt",
                "severity": "high" if images_without_alt > 3 else "medium",
                "message": f"{images_without_alt} of {total_images} images lack alternative text",
            })

        # Check forms for missing labels
        unlabeled_inputs = 0
        for form in forms:
            for inp in form.find_all("input"):
                if inp.get("type", "").lower() in ["hidden", "submit", "button"]:
                    continue
                inp_id = inp.get("id")
                has_label = bool(inp_id and soup.find("label", attrs={"for": inp_id})) or bool(inp.find_parent("label")) or bool(inp.get("aria-label")) or bool(inp.get("placeholder"))
                if not has_label:
                    unlabeled_inputs += 1

        if unlabeled_inputs > 0:
            accessibility_issues.append({
                "type": "unlabeled_form_inputs",
                "severity": "high",
                "message": f"{unlabeled_inputs} form inputs lack explicit accessibility labels",
            })

        # 14. Structured Data / Schema.org
        schema_types = set()
        structured_formats = []

        # JSON-LD
        for s in soup.find_all("script", type="application/ld+json"):
            structured_formats.append("JSON-LD")
            try:
                data = json.loads(s.string or "{}")
                if isinstance(data, dict):
                    t = data.get("@type")
                    if isinstance(t, str):
                        schema_types.add(t)
                    elif isinstance(t, list):
                        schema_types.update(t)
                    # Check for @graph
                    graph = data.get("@graph", [])
                    if isinstance(graph, list):
                        for item in graph:
                            if isinstance(item, dict) and item.get("@type"):
                                schema_types.add(item["@type"])
            except Exception:
                pass

        # Microdata
        for item in soup.find_all(attrs={"itemtype": True}):
            structured_formats.append("Microdata")
            itype = str(item.get("itemtype", "")).split("/")[-1]
            if itype:
                schema_types.add(itype)

        has_structured_data = len(schema_types) > 0

        # 15. Security & SSL Headers
        norm_headers = {k.lower(): v for k, v in headers.items()}
        has_ssl = url.startswith("https://")
        has_hsts = "strict-transport-security" in norm_headers

        security_headers = {
            "strict_transport_security": has_hsts,
            "content_security_policy": "content-security-policy" in norm_headers,
            "x_frame_options": "x-frame-options" in norm_headers,
            "x_content_type_options": "x-content-type-options" in norm_headers,
            "referrer_policy": "referrer-policy" in norm_headers,
        }

        # Check for mixed content (http:// assets on https:// page)
        mixed_content_urls = []
        if has_ssl:
            for tag, attr in [("img", "src"), ("script", "src"), ("link", "href"), ("iframe", "src")]:
                for el in soup.find_all(tag):
                    src = el.get(attr, "")
                    if src.startswith("http://"):
                        mixed_content_urls.append(src)
        has_mixed_content = len(mixed_content_urls) > 0

        # 16. Performance Indicators (DOM Bloat)
        all_elements = soup.find_all()
        dom_element_count = len(all_elements)
        script_count = len(soup.find_all("script"))
        stylesheet_count = len(soup.find_all("link", rel=re.compile(r"stylesheet", re.I)))
        inline_style_count = len(soup.find_all(style=True))

        # 17. Contact Extraction
        emails = set()
        # mailto links
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.lower().startswith("mailto:"):
                raw_email = href.split(":", 1)[1].split("?")[0].strip()
                if self._is_valid_email(raw_email):
                    emails.add(raw_email.lower())

        # Email regex scan
        found_raw_emails = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", html_content
        )
        for e in found_raw_emails:
            if self._is_valid_email(e):
                emails.add(e.lower())

        # Phone numbers
        phones = set()
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.lower().startswith("tel:"):
                raw_phone = href.split(":", 1)[1].split("?")[0].strip()
                if raw_phone and len(raw_phone) >= 7:
                    phones.add(raw_phone)

        # 18. Social Links
        socials = {}
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            h_lower = href.lower()
            for network in ["facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com", "youtube.com", "tiktok.com", "pinterest.com"]:
                net_key = "twitter" if ("x.com" in h_lower or "twitter.com" in h_lower) else network.split(".")[0]
                if network in h_lower and net_key not in socials:
                    socials[net_key] = href

        return AuditResult(
            url=url,
            is_mobile_responsive=is_responsive,
            has_viewport_meta=has_viewport,
            viewport_content=viewport_content,
            detected_cms=detected_cms,
            cms_version_hint=cms_version_hint,
            detected_frameworks=detected_frameworks,
            has_ecommerce=has_ecommerce,
            ecommerce_platform=ecommerce_platform,
            has_online_booking=has_online_booking,
            booking_platform=booking_platform,
            has_contact_form=has_contact_form,
            form_count=form_count,
            has_analytics=has_analytics,
            analytics_tools=analytics_tools,
            meta_title=meta_title,
            meta_title_length=meta_title_len,
            meta_description=meta_desc,
            meta_description_length=meta_desc_len,
            canonical_url=canonical_url,
            headings_summary=headings_summary,
            has_robots_meta=has_robots_meta,
            robots_directives=robots_directives,
            og_tags=og_tags,
            twitter_cards=twitter_cards,
            emails_found=sorted(list(emails))[:5],
            phones_found=sorted(list(phones))[:5],
            social_links_found=socials,
            has_ssl=has_ssl,
            has_hsts=has_hsts,
            has_mixed_content=has_mixed_content,
            mixed_content_urls=mixed_content_urls[:5],
            security_headers=security_headers,
            accessibility_issues=accessibility_issues,
            total_images=total_images,
            images_without_alt=images_without_alt,
            has_structured_data=has_structured_data,
            schema_org_types=sorted(list(schema_types)),
            structured_data_format=list(set(structured_formats)),
            cookie_consent_detected=cookie_consent_detected,
            cookie_consent_provider=cookie_consent_provider,
            has_privacy_policy=has_privacy_policy,
            has_terms_of_service=has_terms_of_service,
            chat_widget=chat_widget,
            chat_provider=chat_provider,
            social_proof_widgets=social_proof_widgets,
            dom_element_count=dom_element_count,
            script_count=script_count,
            stylesheet_count=stylesheet_count,
            inline_style_count=inline_style_count,
            raw_technologies={
                "cms": detected_cms,
                "cms_version_hint": cms_version_hint,
                "frameworks": detected_frameworks,
                "analytics": analytics_tools,
                "ecommerce": ecommerce_platform,
                "booking": booking_platform,
                "chat": chat_provider,
                "security_headers": security_headers,
                "schema_org_types": sorted(list(schema_types)),
            },
        )

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Filter out placeholder or asset file emails."""
        if not email or "@" not in email:
            return False
        disallowed_exts = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".js", ".css", ".woff", ".ttf")
        if email.lower().endswith(disallowed_exts):
            return False
        disallowed_domains = ("example.com", "domain.com", "email.com", "sentry.io", "wixpress.com")
        if any(email.lower().endswith(d) for d in disallowed_domains):
            return False
        return True
