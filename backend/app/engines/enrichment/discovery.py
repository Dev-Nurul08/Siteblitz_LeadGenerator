"""
Contact Discovery Engine module.

Discovers B2B contacts from permitted sources:
- Company website pages (/contact, /about, /team)
- Stored website technical audit signals
- Domain email pattern generation
- Optional Hunter.io API integration (if configured)
"""

from dataclasses import dataclass, field
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import httpx
import structlog

from backend.app.config import get_settings
from backend.app.models.business import Business
from backend.app.models.opportunity import WebsiteAudit

logger = structlog.get_logger(__name__)

CONTACT_PAGE_PATHS = [
    "/contact", "/contact-us", "/contactus",
    "/about", "/about-us", "/our-team", "/team",
    "/leadership", "/staff",
]


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


class ContactDiscoveryEngine:
    """
    Coordinates multi-source B2B contact discovery.
    """

    def __init__(self, timeout_seconds: float = 8.0):
        self.timeout_seconds = timeout_seconds
        self.settings = get_settings()

    async def discover_contacts(
        self,
        business: Business,
        audit: Optional[WebsiteAudit] = None,
    ) -> list[DiscoveredContact]:
        """
        Extract contacts from all permitted channels for this business.
        """
        found_map: dict[str, DiscoveredContact] = {}

        # 1. Direct Business record email
        if business.email:
            em = business.email.lower().strip()
            found_map[em] = DiscoveredContact(
                email=em,
                phone=business.phone,
                source_method="business_profile",
                source_url=business.website_url,
            )

        # 2. Existing audit signals
        if audit and audit.emails_found:
            audit_emails = audit.emails_found.get("emails", [])
            for em in audit_emails:
                cleaned = em.lower().strip()
                if cleaned not in found_map:
                    found_map[cleaned] = DiscoveredContact(
                        email=cleaned,
                        source_method="website_audit",
                        source_url=audit.final_url or audit.url_analyzed,
                    )

        # 3. Targeted page crawl if website is reachable
        if business.website_url and (audit is None or audit.is_reachable):
            crawled = await self._crawl_contact_pages(business.website_url)
            for c in crawled:
                if c.email not in found_map:
                    found_map[c.email] = c

        # 4. Synthesize corporate inbox if domain exists but no email found
        if not found_map and business.website_url:
            domain = self._extract_domain(business.website_url)
            if domain:
                synthetic_email = f"info@{domain}"
                found_map[synthetic_email] = DiscoveredContact(
                    email=synthetic_email,
                    phone=business.phone,
                    source_method="corporate_domain_default",
                    source_url=business.website_url,
                )

        # 5. Hunter.io API integration (if API key is present)
        if self.settings.HUNTER_API_KEY and business.website_url:
            hunter_contacts = await self._query_hunter_api(business.website_url)
            for hc in hunter_contacts:
                if hc.email not in found_map:
                    found_map[hc.email] = hc

        return list(found_map.values())

    async def _crawl_contact_pages(self, base_url: str) -> list[DiscoveredContact]:
        """Fetch dedicated contact/about pages to locate team contacts."""
        results: list[DiscoveredContact] = []
        if not base_url.startswith(("http://", "https://")):
            base_url = f"https://{base_url}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SiteBlitzEnricher/1.0",
            "Accept": "text/html,application/xhtml+xml",
        }

        async with httpx.AsyncClient(timeout=self.timeout_seconds, follow_redirects=True) as client:
            for path in CONTACT_PAGE_PATHS[:3]:  # Probe top 3 contact paths
                target_url = urljoin(base_url, path)
                try:
                    resp = await client.get(target_url, headers=headers)
                    if resp.status_code == 200 and "text/html" in resp.headers.get("content-type", ""):
                        extracted = self._extract_from_html(resp.text, target_url)
                        results.extend(extracted)
                        if results:
                            break  # Found contacts, don't spam requests
                except Exception:
                    continue

        return results

    def _extract_from_html(self, html: str, source_url: str) -> list[DiscoveredContact]:
        """Extract contacts and mailto links from a page."""
        soup = BeautifulSoup(html, "html.parser")
        contacts = []

        # Find mailto links
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.lower().startswith("mailto:"):
                raw_email = href.split(":", 1)[1].split("?")[0].strip().lower()
                if self._is_valid_email(raw_email):
                    # Check if anchor text looks like a person's name
                    anchor_text = a.get_text(strip=True)
                    name = anchor_text if (anchor_text and "@" not in anchor_text and len(anchor_text) < 40) else None

                    contacts.append(
                        DiscoveredContact(
                            email=raw_email,
                            full_name=name,
                            source_method="website_scrape",
                            source_url=source_url,
                        )
                    )

        # Regex fallback for emails in text
        raw_emails = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", html
        )
        for em in raw_emails[:5]:
            em_clean = em.lower().strip()
            if self._is_valid_email(em_clean) and not any(c.email == em_clean for c in contacts):
                contacts.append(
                    DiscoveredContact(
                        email=em_clean,
                        source_method="website_scrape",
                        source_url=source_url,
                    )
                )

        return contacts

    async def _query_hunter_api(self, website_url: str) -> list[DiscoveredContact]:
        """Query Hunter.io domain search endpoint."""
        domain = self._extract_domain(website_url)
        if not domain:
            return []

        hunter_url = "https://api.hunter.io/v2/domain-search"
        params = {
            "domain": domain,
            "api_key": self.settings.HUNTER_API_KEY,
            "limit": 5,
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(hunter_url, params=params)
                if res.status_code == 200:
                    data = res.json().get("data", {})
                    emails = data.get("emails", [])
                    return [
                        DiscoveredContact(
                            email=item.get("value", "").lower(),
                            first_name=item.get("first_name"),
                            last_name=item.get("last_name"),
                            job_title=item.get("position"),
                            linkedin_url=item.get("linkedin"),
                            phone=item.get("phone_number"),
                            source_method="hunter_api",
                            source_url=f"https://hunter.io/search/{domain}",
                        )
                        for item in emails
                        if item.get("value")
                    ]
        except Exception as e:
            logger.warning("hunter_api_failed", error=str(e))

        return []

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
        if not email or "@" not in email:
            return False
        disallowed = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".js", ".css")
        return not email.endswith(disallowed)
