"""
Contact Discovery Engine module (Phase 3).

Collects the email addresses a business itself publishes:
- Polite website visit (robots.txt, homepage + /contact, /contact-us, /contactus, /about) — site_visit.py
- Emails only from mailto links, visible text and Cloudflare-encoded addresses (spec row 10), each with the
  page excerpt around it (email engine v2 spec row 3)
- Addresses already stored on the business (its source listing) and in an earlier website audit

Nothing here invents an address or a phone number. The old `discover_contacts()` made up `info@<domain>`,
`inquiry.<name>@gmail.com`, "Proprietor / Store Manager" and fake `+91 9825…` numbers; it was removed in
email engine v2 phase E1 together with the Hunter.io lookup (third-party addresses are not the business's
own publication). `backend/tests/test_eligibility/test_no_guessed_addresses.py` keeps it that way.
"""

from dataclasses import dataclass
import re
from typing import Optional
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup, Comment
import structlog

from backend.app.engines.enrichment.site_visit import visit_site
from backend.app.models.business import Business
from backend.app.models.opportunity import WebsiteAudit

logger = structlog.get_logger(__name__)

CONTACT_PAGE_PATHS = [
    "/contact", "/contact-us", "/contactus",
    "/about", "/about-us", "/our-team", "/team",
    "/leadership", "/staff", "/management", "/our-story",
]

EMAIL_SYNTAX = re.compile(r"[a-z0-9][a-z0-9._%+-]{0,63}@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,24}")
EMAIL_IN_TEXT = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,24}")
OBFUSCATED_IN_TEXT = re.compile(
    r"([a-zA-Z0-9._%+-]+)\s*[\[(](?:at|@)[\])]\s*([a-zA-Z0-9.-]+)\s*[\[(](?:dot|\.)[\])]\s*([a-zA-Z]{2,})",
    re.IGNORECASE,
)
# Not part of what a visitor reads, or not an address the business wrote for visitors (QA-040).
HIDDEN_TAGS = ["script", "style", "noscript", "template", "head", "svg", "iframe", "object", "textarea"]
PLACEHOLDER_DOMAINS = ("example.com", "example.org", "example.net", "example.in", "domain.com",
                       "yourdomain.com", "yoursite.com", "mysite.com", "website.com", "company.com",
                       "test.com", "sentry.io", "wixpress.com")
PLACEHOLDER_LOCAL_PARTS = {"you", "your", "yourname", "youremail", "your.name", "your.email", "name",
                           "username", "user", "someone", "example", "test", "johndoe", "john.doe",
                           "jane.doe"}
EXCERPT_MAX = 300   # email engine v2: the page excerpt stored with every address (<= 300 characters)
# The nearest element around a mailto / Cloudflare link whose text gives the address its context.
BLOCK_TAGS = ["p", "li", "td", "th", "dd", "address", "footer", "header", "section", "article", "div"]


@dataclass
class DiscoveredContact:
    """A raw candidate contact discovered from permitted sources."""

    email: str
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    source_method: str = "website_scrape"
    source_url: Optional[str] = None
    confidence: float = 0.80
    excerpt: Optional[str] = None   # visible page text around the address, <= EXCERPT_MAX characters


def _squash(text: str) -> str:
    return " ".join((text or "").split())


def text_window(text: str, needle: str, limit: int = EXCERPT_MAX) -> Optional[str]:
    """The `limit`-character window of `text` centred on `needle` (case-insensitive), or None if absent."""
    text = _squash(text)
    if not needle:
        return None
    start = text.lower().find(needle.lower())
    if start < 0:
        return None
    pad = max(0, (limit - len(needle)) // 2)
    begin = max(0, start - pad)
    end = min(len(text), begin + limit)
    begin = max(0, end - limit)
    return text[begin:end].strip() or None


def element_context(element, email: str, limit: int = EXCERPT_MAX) -> str:
    """Text of the block around a link, with the link target written out when the text does not show it."""
    block = element.find_parent(BLOCK_TAGS) or element.parent or element
    text = _squash(block.get_text(" ", strip=True))
    inside = text_window(text, email, limit)
    if inside:
        return inside
    marker = f"<mailto:{email}>"
    anchor = _squash(element.get_text(" ", strip=True))
    room = max(0, limit - len(marker) - 1)
    around = (text_window(text, anchor, room) if anchor else None) or text[:room]
    return f"{around} {marker}".strip()[:limit]


class ContactDiscoveryEngine:
    """
    Reads the contact addresses a business publishes on its own pages (no guessing).
    """

    def __init__(self, timeout_seconds: float = 3.0):
        self.timeout_seconds = timeout_seconds

    async def published_contacts(
        self,
        business: Business,
        audit: Optional[WebsiteAudit] = None,
    ) -> list[DiscoveredContact]:
        """Addresses that exist somewhere for this business. Never a made-up one.

        1. the email on the business record (from its source listing: Tier 2 for email engine v2)
        2. emails a stored website audit read from its pages
        3. a polite visit of its own website (`_crawl_contact_pages`)
        No result is a valid result: an empty list.
        """
        found_map: dict[str, DiscoveredContact] = {}
        if business.email:
            email = business.email.lower().strip()
            found_map[email] = DiscoveredContact(
                email=email, phone=business.phone, source_method="business_profile",
                source_url=None, confidence=0.95)
        if audit and audit.emails_found:
            for raw in audit.emails_found.get("emails", []):
                email = raw.lower().strip()
                if email and email not in found_map:
                    found_map[email] = DiscoveredContact(
                        email=email, source_method="website_audit",
                        source_url=audit.final_url or audit.url_analyzed, confidence=0.90)
        if business.website_url and (audit is None or audit.is_reachable):
            for contact in await self._crawl_contact_pages(business.website_url):
                found_map.setdefault(contact.email, contact)
        return list(found_map.values())

    async def _crawl_contact_pages(self, base_url: str) -> list[DiscoveredContact]:
        """Visit the site politely and return the emails its own pages show.

        robots.txt, homepage + 4 contact paths, 2 MB / 5 redirects / SSRF guard (QA-040,
        outreach-engine spec rows 10-11). `site_visit.visit_site` also returns the site checks.
        """
        visit = await visit_site(base_url, self._extract_from_html, timeout=self.timeout_seconds)
        return visit.contacts

    def _extract_from_html(self, html: str, source_url: str) -> list[DiscoveredContact]:
        """Emails a visitor can see on the page: mailto links, visible text, Cloudflare-encoded ones.

        Spec row 10 allows only these three. Scripts (JSON-LD, analytics keys such as Sentry DSNs),
        HTML comments, form placeholders and example addresses are not the business's address (QA-040).
        """
        soup = BeautifulSoup(html, "html.parser")
        contacts: list[DiscoveredContact] = []
        seen: set[str] = set()

        def add(raw: Optional[str], method: str, confidence: float, name: Optional[str] = None,
                excerpt: Optional[str] = None) -> None:
            email = (raw or "").strip().strip(".").lower()
            if email in seen or not self._is_valid_email(email) or self._is_placeholder_email(email):
                return
            seen.add(email)
            contacts.append(DiscoveredContact(email=email, full_name=name, source_method=method,
                                              source_url=source_url, confidence=confidence,
                                              excerpt=excerpt))

        # 1. Cloudflare Email Protection: data-cfemail elements and /cdn-cgi/l/email-protection#<hex> links.
        # The decoded address is written into the element, so the excerpt shows what a visitor's browser shows.
        for element in soup.find_all(attrs={"data-cfemail": True}):
            decoded = self._decode_cloudflare_email(element["data-cfemail"])
            if decoded:
                element.string = decoded
                add(decoded, "cloudflare_decode", 0.90, excerpt=element_context(element, decoded))

        # 2. mailto links (a link may list several addresses separated by commas)
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if "/cdn-cgi/l/email-protection#" in href:
                decoded = self._decode_cloudflare_email(href.split("#", 1)[1])
                if decoded:
                    add(decoded, "cloudflare_decode", 0.90, excerpt=element_context(a, decoded))
            elif href.lower().startswith("mailto:"):
                anchor_text = a.get_text(strip=True)
                name = anchor_text if (anchor_text and "@" not in anchor_text and len(anchor_text) < 40) else None
                for part in unquote(href.split(":", 1)[1].split("?")[0]).split(","):
                    address = part.strip().strip(".").lower()
                    add(part, "mailto", 0.88, name, excerpt=element_context(a, address) if address else None)

        # 3. Visible text only: drop scripts, styles, head, form text and comments first
        for tag in soup(HIDDEN_TAGS):
            tag.decompose()
        for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
            comment.extract()
        text = soup.get_text(" ", strip=True)
        for match in EMAIL_IN_TEXT.findall(text)[:20]:
            add(match, "visible_text", 0.85, excerpt=text_window(text, match))
        # "name [at] domain [dot] com" written out on the page is still the address the business shows
        for found in OBFUSCATED_IN_TEXT.finditer(text):
            user, dom, tld = found.groups()
            add(f"{user}@{dom}.{tld}", "visible_text_obfuscated", 0.85,
                excerpt=text_window(text, found.group(0)))

        # The page text around the address beats the link's block when the visitor can read the address.
        for contact in contacts:
            visible = text_window(text, contact.email)
            if visible:
                contact.excerpt = visible
        return contacts

    @staticmethod
    def _decode_cloudflare_email(cf_hex: str) -> Optional[str]:
        """Decode Cloudflare XOR email protection cipher."""
        try:
            r = int(cf_hex[:2], 16)
            email = "".join(
                chr(int(cf_hex[i : i + 2], 16) ^ r) for i in range(2, len(cf_hex), 2)
            )
            return email.lower()
        except Exception:
            return None

    @staticmethod
    def _extract_domain(url: str) -> Optional[str]:
        if not url:
            return None
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc or None

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        if not email or "@" not in email or len(email) > 254:
            return False
        disallowed = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".js", ".css", ".woff", ".ttf")
        return not email.endswith(disallowed) and EMAIL_SYNTAX.fullmatch(email) is not None

    @staticmethod
    def _is_placeholder_email(email: str) -> bool:
        """Example / template addresses (`you@example.com`) and analytics keys (`…@o123.ingest.sentry.io`)."""
        local, _, domain = email.partition("@")
        return local in PLACEHOLDER_LOCAL_PARTS or any(
            domain == d or domain.endswith("." + d) for d in PLACEHOLDER_DOMAINS)
