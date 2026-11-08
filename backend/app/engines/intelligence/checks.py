"""
Website Intelligence checks — the observations behind a verdict (spec rows 2–8).

Each function returns `rules.Check` objects; the service stores them append-only.
Network calls reuse the SSRF-guarded resolver. Instagram / Facebook / LinkedIn / TikTok pages are
never fetched (login walls, platform terms) — they are recorded as "not checked", and the search
check covers finding a website they might link to.
"""

import asyncio
import re
import socket
from typing import Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from backend.app.engines.discovery.normalizer import BusinessNormalizer
from backend.app.engines.discovery.overture import social_platform
from backend.app.engines.intelligence.rules import Check
from backend.app.engines.opportunity.auditor import WebsiteAuditor
from backend.app.engines.opportunity.resolver import (
    WebsiteResolver,
    ensure_public_destination,
)
from backend.app.models.intelligence import CheckType

# Spec row 5 — domain guesses per country; the generic `.com` is always tried.
CCTLDS = {"IN": [".in", ".co.in"], "GB": [".co.uk", ".uk"], "AU": [".com.au"], "NZ": [".co.nz"]}
LINK_IN_BIO_PLATFORMS = {"linktree"}
LINK_IN_BIO_HOSTS = ("linktr.ee", "bio.link", "beacons.ai")
# Links that point at a listing of the business, not a website it owns (Google short links /
# Maps / retired business.site pages, and directories). Recorded, never counted as "own website".
LISTING_HOSTS = ("g.co", "goo.gl", "google.com", "business.site", "justdial.com", "practo.com",
                 "zomato.com", "swiggy.com", "sulekha.com", "indiamart.com", "tripadvisor.com")


def is_listing(url: Optional[str]) -> bool:
    host = (urlparse(url if url and "://" in url else f"https://{url or ''}").hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in LISTING_HOSTS)


PARKED_TOKENS = ("domain parked", "buy this domain", "this domain is for sale", "coming soon",
                 "under construction", "website in development", "parked free")


def website_links(raw_records: list[dict], website_url: Optional[str]) -> list[str]:
    """Every non-social web address the sources list for the business."""
    links: list[str] = []
    candidates = [website_url] if website_url else []
    for raw in raw_records:
        tags = raw.get("tags") or {}
        candidates += [tags.get("website"), tags.get("contact:website"), tags.get("url")]
        candidates += list(raw.get("websites") or [])
        candidates.append(raw.get("website"))
    for url in candidates:
        if url and isinstance(url, str) and not social_platform(url):
            normal = url.strip()
            if not normal.startswith(("http://", "https://")):
                normal = "https://" + normal
            if normal not in links:
                links.append(normal)
    return links


def source_checks(raw_records: list[dict], website_url: Optional[str],
                  social_urls: dict, skip: Optional[str]) -> list[Check]:
    checks = [Check(None, CheckType.SKIP_RULE, "skip" if skip else "pass",
                    detail={"reason": skip} if skip else {})]
    links = website_links(raw_records, website_url)
    if links:
        checks += [Check(None, CheckType.SOURCE_TAG, "listing" if is_listing(link) else "found",
                         target=link) for link in links]
    else:
        checks.append(Check(None, CheckType.SOURCE_TAG, "none",
                            detail={"note": "No website field in any source record"}))
    for platform, url in (social_urls or {}).items():
        checks.append(Check(None, CheckType.SOCIAL_LINK, "found", target=url,
                            detail={"platform": platform}))
    return checks


def _identity_signals(html: str, name: str, city: Optional[str], phone: Optional[str]) -> list[str]:
    """Which identity signals a page shows (spec row 5 needs ≥ 2)."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()
    head = " ".join(filter(None, [soup.title.get_text(" ", strip=True) if soup.title else "",
                                  *(h.get_text(" ", strip=True) for h in soup.find_all("h1")[:3])])).lower()
    signals = []
    tokens = [t for t in BusinessNormalizer.normalize_name(name).split() if len(t) > 2]
    if tokens and all(t in head or t in text[:5000] for t in tokens):
        signals.append("name")
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) >= 8 and digits[-8:] in re.sub(r"\D", "", text):
        signals.append("phone")
    if city and city.strip().lower() in text:
        signals.append("city")
    return signals


def domain_candidates(name: str, country: Optional[str]) -> list[str]:
    base = re.sub(r"[^a-z0-9]", "", BusinessNormalizer.normalize_name(name))
    if len(base) < 3:
        return []
    cc = (country or "").lower()
    tlds = [".com"] + CCTLDS.get(cc.upper(), [f".{cc}", f".co.{cc}"] if cc else [])
    return [f"{base}{tld}" for tld in dict.fromkeys(tlds)]


async def _resolves(host: str) -> Optional[bool]:
    try:
        await asyncio.get_running_loop().getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        return True
    except socket.gaierror:
        return False
    except Exception:
        return None


async def domain_guess_checks(name: str, country: Optional[str], city: Optional[str],
                              phone: Optional[str], resolver: WebsiteResolver) -> list[Check]:
    checks = []
    for domain in domain_candidates(name, country):
        exists = await _resolves(domain)
        if exists is None:
            checks.append(Check(None, CheckType.DOMAIN_GUESS, "error", target=domain))
            continue
        if not exists:
            checks.append(Check(None, CheckType.DOMAIN_GUESS, "none", target=domain,
                                detail={"note": "Domain does not exist (no DNS)"}))
            continue
        result = await resolver.resolve(f"https://{domain}")
        signals = _identity_signals(result.html_content or "", name, city, phone) \
            if result.html_content else []
        outcome = "matched" if len(signals) >= 2 else "no_match"
        checks.append(Check(None, CheckType.DOMAIN_GUESS, outcome, target=domain,
                            detail={"signals": signals, "http_status": result.http_status,
                                    "note": "Exists but is not this business" if outcome == "no_match"
                                    else "Page names this business"}))
    if not checks:
        checks.append(Check(None, CheckType.DOMAIN_GUESS, "none", target=None,
                            detail={"note": "Name too short to guess a domain"}))
    return checks


async def site_fetch_check(url: str, resolver: WebsiteResolver) -> Check:
    """Spec row 6."""
    result = await resolver.resolve(url)
    detail = {"http_status": result.http_status, "final_url": result.final_url,
              "has_ssl": result.has_ssl, "load_time_seconds": result.load_time_seconds,
              "error": result.error_message}
    if result.error_message and result.error_message.startswith("Blocked:"):
        return Check(None, CheckType.SITE_FETCH, "blocked", target=url, detail=detail)
    if result.final_url and social_platform(result.final_url):
        return Check(None, CheckType.SITE_FETCH, "social", target=url, detail=detail)
    if result.final_url and is_listing(result.final_url):
        return Check(None, CheckType.SITE_FETCH, "listing", target=url, detail=detail)
    status = result.http_status
    if status in (401, 403, 429):
        return Check(None, CheckType.SITE_FETCH, "protected", target=url, detail=detail)
    if status is None or status >= 500 or status in (404, 410):
        return Check(None, CheckType.SITE_FETCH, "failed", target=url, detail=detail)
    html = (result.html_content or "")
    if any(token in html[:4000].lower() for token in PARKED_TOKENS):
        return Check(None, CheckType.SITE_FETCH, "failed", target=url,
                     detail={**detail, "note": "Parked / coming-soon page"})
    audit = WebsiteAuditor().audit_html(result.final_url or url, html)
    detail["has_viewport"] = audit.has_viewport_meta
    return Check(None, CheckType.SITE_FETCH, "ok", target=url, detail=detail)


async def link_in_bio_checks(social_urls: dict) -> tuple[list[Check], list[str]]:
    """Resolve Linktree-style pages to the external links they list (no login-walled sites)."""
    checks, found = [], []
    for platform, url in (social_urls or {}).items():
        host = (urlparse(url if "://" in url else f"https://{url}").hostname or "").lower()
        if platform not in LINK_IN_BIO_PLATFORMS and not host.endswith(LINK_IN_BIO_HOSTS):
            checks.append(Check(None, CheckType.LINK_IN_BIO, "not_checked", target=url,
                                detail={"note": f"{platform} pages are not fetched (login wall / terms)"}))
            continue
        try:
            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True,
                                         event_hooks={"request": [ensure_public_destination]}) as client:
                response = await client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a["href"] for a in soup.find_all("a", href=True)
                     if a["href"].startswith("http") and not social_platform(a["href"])
                     and not (urlparse(a["href"]).hostname or "").endswith(LINK_IN_BIO_HOSTS)]
            links = list(dict.fromkeys(links))[:5]
            found += links
            checks.append(Check(None, CheckType.LINK_IN_BIO, "links" if links else "none",
                                target=url, detail={"links": links}))
        except Exception as exc:
            checks.append(Check(None, CheckType.LINK_IN_BIO, "error", target=url,
                                detail={"error": str(exc)[:300]}))
    return checks, found
