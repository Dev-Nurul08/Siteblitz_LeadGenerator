"""
Website Auditor module.

Performs deep technical and capability inspection of business websites.
Fingerprints CMS, frameworks, mobile responsiveness, e-commerce, booking widgets,
SEO hygiene, and contact signals.
"""

from dataclasses import dataclass, field
import re
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import structlog

logger = structlog.get_logger(__name__)

# Common CMS signatures
CMS_SIGNATURES = {
    "WordPress": [
        r"wp-content",
        r"wp-includes",
        r'<meta name="generator" content="WordPress',
    ],
    "Shopify": [
        r"cdn\.shopify\.com",
        r"Shopify\.theme",
        r"myshopify\.com",
    ],
    "Wix": [
        r"wix\.com",
        r"wix-warmup-data",
        r"_wix_browser_sess",
    ],
    "Squarespace": [
        r"static1\.squarespace\.com",
        r"squarespace\.com",
    ],
    "Webflow": [
        r"data-wf-page",
        r"data-wf-site",
        r"webflow\.com",
    ],
    "Joomla": [
        r"/media/system/js/",
        r"/templates/[a-z0-9_-]+/",
    ],
    "Drupal": [
        r"Drupal\.settings",
        r"/sites/default/files/",
    ],
}

# Framework & library signatures
FRAMEWORK_SIGNATURES = {
    "React": [r"data-reactroot", r"_reactListening", r"react\.production\.min\.js"],
    "Vue": [r"data-v-[a-z0-9]+", r"vue\.runtime", r"vue\.global"],
    "Angular": [r"ng-version", r"ng-app"],
    "jQuery": [r"jquery[\.-][0-9]", r"jquery\.min\.js"],
    "Bootstrap": [r"bootstrap(?:\.min)?\.(?:css|js)", r"class=\"[^\"]*col-(?:xs|sm|md|lg)-"],
    "TailwindCSS": [r"tailwindcss", r"class=\"[^\"]*(?:flex|grid|p-[0-9]|text-[a-z]+)[^\"]*\""],
}

# Booking widget indicators
BOOKING_SIGNATURES = [
    r"calendly\.com",
    r"acuityscheduling\.com",
    r"booksy\.com",
    r"opentable\.com",
    r"resy\.com",
    r"setmore\.com",
    r"fresha\.com",
    r"appointlet\.com",
    r"tidycal\.com",
    r"book-online",
    r"appointment",
    r"book an appointment",
    r"schedule a call",
    r"reserve a table",
]

# E-commerce indicators
ECOMMERCE_SIGNATURES = [
    r"shopify",
    r"woocommerce",
    r"add-to-cart",
    r"cart-total",
    r"checkout-button",
    r"/cart",
    r"/checkout",
    r"shopping-cart",
    r"basket",
    r"view cart",
]


@dataclass
class AuditResult:
    """Detailed structural findings from analyzing a website's HTML."""

    url: str
    is_mobile_responsive: bool = False
    has_viewport_meta: bool = False
    detected_cms: Optional[str] = None
    detected_frameworks: list[str] = field(default_factory=list)
    has_ecommerce: bool = False
    has_online_booking: bool = False
    has_contact_form: bool = False
    has_analytics: bool = False

    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    headings_summary: dict = field(default_factory=dict)

    emails_found: list[str] = field(default_factory=list)
    phones_found: list[str] = field(default_factory=list)
    social_links_found: dict[str, str] = field(default_factory=dict)
    raw_technologies: dict = field(default_factory=dict)


class WebsiteAuditor:
    """
    Analyzes website HTML and returns technical capability signals.
    """

    def audit_html(self, url: str, html_content: str) -> AuditResult:
        """
        Inspect raw HTML of a business website and extract all signals.
        """
        if not html_content:
            return AuditResult(url=url)

        soup = BeautifulSoup(html_content, "html.parser")
        text_lower = html_content.lower()

        # 1. Mobile Responsiveness / Viewport
        viewport_tag = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
        has_viewport = False
        is_responsive = False
        if viewport_tag and viewport_tag.get("content"):
            content = viewport_tag["content"].lower()
            if "width=device-width" in content or "initial-scale=1" in content:
                has_viewport = True
                is_responsive = True

        # 2. Meta Tags (SEO Basics)
        title_tag = soup.find("title")
        meta_title = title_tag.get_text(strip=True) if title_tag else None

        desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        meta_desc = desc_tag.get("content", "").strip() if desc_tag else None

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
        for cms_name, patterns in CMS_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                detected_cms = cms_name
                break

        # 5. Frameworks & Libraries
        detected_frameworks = []
        for framework, patterns in FRAMEWORK_SIGNATURES.items():
            if any(re.search(pat, html_content, re.IGNORECASE) for pat in patterns):
                detected_frameworks.append(framework)

        # 6. Capabilities
        # E-commerce
        has_ecommerce = (
            detected_cms == "Shopify"
            or any(re.search(pat, text_lower) for pat in ECOMMERCE_SIGNATURES)
            or bool(soup.find(attrs={"class": re.compile(r"(cart|checkout|woocommerce)", re.I)}))
        )

        # Online Booking
        has_online_booking = any(
            re.search(pat, text_lower) for pat in BOOKING_SIGNATURES
        )

        # Contact Form
        forms = soup.find_all("form")
        has_contact_form = False
        for form in forms:
            inputs = form.find_all(["input", "textarea"])
            types = [inp.get("type", "").lower() for inp in inputs]
            names = [str(inp.get("name", "")).lower() for inp in inputs]
            if (
                "email" in types
                or any("email" in n for n in names)
                or form.find("textarea")
            ):
                has_contact_form = True
                break

        # Analytics
        has_analytics = any(
            token in text_lower
            for token in ["googletagmanager", "google-analytics", "gtag(", "fbq(", "segment.io"]
        )

        # 7. Contact Extraction (from visible HTML)
        emails = set()
        # mailto links
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.lower().startswith("mailto:"):
                raw_email = href.split(":", 1)[1].split("?")[0].strip()
                if self._is_valid_email(raw_email):
                    emails.add(raw_email.lower())

        # Email regex scan in text
        found_raw_emails = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", html_content
        )
        for e in found_raw_emails:
            if self._is_valid_email(e):
                emails.add(e.lower())

        phones = set()
        # tel links
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.lower().startswith("tel:"):
                raw_phone = href.split(":", 1)[1].split("?")[0].strip()
                if raw_phone:
                    phones.add(raw_phone)

        # 8. Social Links
        socials = {}
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            for network in ["facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com", "youtube.com", "tiktok.com"]:
                if network in href.lower() and not socials.get(network.split(".")[0]):
                    socials[network.split(".")[0]] = href

        return AuditResult(
            url=url,
            is_mobile_responsive=is_responsive,
            has_viewport_meta=has_viewport,
            detected_cms=detected_cms,
            detected_frameworks=detected_frameworks,
            has_ecommerce=has_ecommerce,
            has_online_booking=has_online_booking,
            has_contact_form=has_contact_form,
            has_analytics=has_analytics,
            meta_title=meta_title,
            meta_description=meta_desc,
            headings_summary=headings_summary,
            emails_found=sorted(list(emails))[:5],
            phones_found=sorted(list(phones))[:5],
            social_links_found=socials,
            raw_technologies={
                "cms": detected_cms,
                "frameworks": detected_frameworks,
                "analytics": has_analytics,
            },
        )

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Filter out placeholder or image file emails."""
        if not email or "@" not in email:
            return False
        disallowed_exts = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".js", ".css")
        if email.lower().endswith(disallowed_exts):
            return False
        disallowed_domains = ("example.com", "domain.com", "email.com", "sentry.io")
        if any(email.lower().endswith(d) for d in disallowed_domains):
            return False
        return True
