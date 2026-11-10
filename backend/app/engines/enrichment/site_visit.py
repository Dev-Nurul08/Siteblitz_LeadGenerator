"""
Polite visit of one business website for the email finder (phase 14).

Spec: docs/spec/outreach-engine.md rows 9-12; fetch limits from docs/spec/website-intelligence.md row 6.

One visit = robots.txt, then the homepage, then /contact, /contact-us, /contactus and /about until a
page gives an email: at most 5 page GETs, one request at a time. Every GET has a 12 s total limit,
reads at most 2 MB, follows at most 5 redirects and passes the SSRF guard on every hop.
The homepage response also gives the site checks (down / protected / social / listing, HTTPS and
the viewport meta tag), classified the same way as `intelligence.checks.site_fetch_check`.
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import Callable, Optional
from urllib.parse import urljoin, urlparse

import httpx

from backend.app.engines.discovery.overture import social_platform
from backend.app.engines.intelligence.checks import PARKED_TOKENS, is_listing
from backend.app.engines.opportunity.auditor import WebsiteAuditor
from backend.app.engines.opportunity.resolver import UnsafeDestinationError, ensure_public_destination

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SiteBlitzEnricher/1.0"
ROBOTS_TOKEN = "siteblitzenricher"   # the product token a robots.txt group can name
CONTACT_PATHS = ("/contact", "/contact-us", "/contactus", "/about")   # discovery.CONTACT_PAGE_PATHS[:4]
TIMEOUT_SECONDS = 12.0
MAX_BYTES = 2 * 1024 * 1024
MAX_REDIRECTS = 5


async def _guard(request: httpx.Request) -> None:
    # Looked up at call time so tests can swap the guard for a local test server.
    await ensure_public_destination(request)


@dataclass
class Page:
    url: str
    status: Optional[int] = None
    final_url: Optional[str] = None
    content_type: str = ""
    body: str = ""
    truncated: bool = False
    error: Optional[str] = None      # timeout | connect | too_many_redirects | blocked | other
    detail: Optional[str] = None


async def fetch(client: httpx.AsyncClient, url: str, timeout: float = TIMEOUT_SECONDS) -> Page:
    """GET with a total time limit and a 2 MB read limit (the body is streamed, never loaded whole)."""
    page = Page(url=url)

    async def _get() -> None:
        async with client.stream("GET", url) as response:
            page.status = response.status_code
            page.final_url = str(response.url)
            page.content_type = response.headers.get("content-type", "").lower()
            chunks, size = [], 0
            async for chunk in response.aiter_bytes():
                chunks.append(chunk)
                size += len(chunk)
                if size >= MAX_BYTES:
                    page.truncated = True
                    break
            raw = b"".join(chunks)[:MAX_BYTES]
            try:
                page.body = raw.decode(response.encoding or "utf-8", errors="replace")
            except LookupError:   # a made-up charset in the Content-Type header
                page.body = raw.decode("utf-8", errors="replace")

    try:
        await asyncio.wait_for(_get(), timeout)
    except (asyncio.TimeoutError, httpx.TimeoutException):
        page.error = "timeout"
    except httpx.TooManyRedirects:
        page.error = "too_many_redirects"
    except UnsafeDestinationError as exc:
        page.error, page.detail = "blocked", str(exc)[:200]
    except httpx.ConnectError as exc:
        page.error, page.detail = "connect", str(exc)[:200]
    except Exception as exc:   # protocol errors, broken encodings, invalid URLs from the source data
        page.error, page.detail = "other", f"{type(exc).__name__}: {str(exc)[:180]}"
    return page


class RobotsRules:
    """
    robots.txt as RFC 9309 reads it. Written here because the standard library's
    urllib.robotparser has no `*` / `$` wildcards and uses the first matching rule instead of the
    longest one, so "Disallow: /*" would wrongly allow every page.
    """

    def __init__(self, rules: list[tuple[bool, str]]):
        self.rules = rules
        self._compiled = {pattern: self._regex(pattern) for _, pattern in rules}

    @classmethod
    def allow_all(cls) -> "RobotsRules":
        return cls([])

    @classmethod
    def disallow_all(cls) -> "RobotsRules":
        return cls([(False, "/")])

    @classmethod
    def parse(cls, text: str, token: str = ROBOTS_TOKEN) -> "RobotsRules":
        groups: list[tuple[set, list]] = []
        agents: Optional[set] = None
        rules: Optional[list] = None
        last_was_agent = False
        for raw_line in text.splitlines():
            line = raw_line.split("#", 1)[0].strip()
            if ":" not in line:
                continue
            key, value = (part.strip() for part in line.split(":", 1))
            key = key.lower()
            if key == "user-agent":
                if not last_was_agent:
                    agents, rules = set(), []
                    groups.append((agents, rules))
                agents.add(value.split("/")[0].strip().lower())
                last_was_agent = True
            elif key in ("allow", "disallow"):
                last_was_agent = False
                if rules is not None and value:   # an empty Disallow allows everything
                    rules.append((key == "allow", value))
        own = [rule for names, group in groups if token in names for rule in group]
        if own or any(token in names for names, _ in groups):
            return cls(own)
        return cls([rule for names, group in groups if "*" in names for rule in group])

    @staticmethod
    def _regex(pattern: str) -> re.Pattern:
        anchored = pattern.endswith("$")
        body = pattern[:-1] if anchored else pattern
        return re.compile("".join(".*" if ch == "*" else re.escape(ch) for ch in body)
                          + ("$" if anchored else ""))

    def can_fetch(self, url: str) -> bool:
        parsed = urlparse(url)
        path = (parsed.path or "/") + (f"?{parsed.query}" if parsed.query else "")
        if path == "/robots.txt":
            return True
        best: Optional[tuple[int, bool]] = None
        for allow, pattern in self.rules:
            if self._compiled[pattern].match(path):
                # Longest pattern wins; on a tie Allow wins (RFC 9309 section 2.2.2).
                if best is None or len(pattern) > best[0] or (len(pattern) == best[0] and allow):
                    best = (len(pattern), allow)
        return True if best is None else best[1]


@dataclass
class SiteVisit:
    listed_url: str
    outcome: str = "failed"      # ok | protected | failed | social | listing | blocked | robots_blocked
    note: Optional[str] = None
    http_status: Optional[int] = None
    final_url: Optional[str] = None
    has_https: Optional[bool] = None
    has_viewport: Optional[bool] = None
    robots: str = "not_fetched"  # found | none | unavailable | unreachable
    requests: int = 0
    pages: list[dict] = field(default_factory=list)
    contacts: list = field(default_factory=list)


def _origin(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


async def _load_robots(client: httpx.AsyncClient, origin: str, timeout: float,
                       visit: SiteVisit) -> tuple[Optional[RobotsRules], Page]:
    page = await fetch(client, f"{origin}/robots.txt", timeout)
    visit.requests += 1
    if page.error:
        visit.robots = "unreachable"
        return None, page
    if page.status == 200:
        visit.robots = "found"
        return RobotsRules.parse(page.body), page
    if page.status == 429 or page.status >= 500:
        # RFC 9309 section 2.3.1.4: an unreachable robots.txt means "assume complete disallow".
        visit.robots = "unavailable"
        return RobotsRules.disallow_all(), page
    visit.robots = "none"   # 4xx: there is no robots.txt, everything is allowed
    return RobotsRules.allow_all(), page


def _no_dns(page: Page) -> bool:
    detail = (page.detail or "").lower()
    return page.error == "connect" and ("getaddrinfo" in detail or "name or service" in detail
                                        or "nodename nor servname" in detail)


def new_client(timeout: float = TIMEOUT_SECONDS) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        timeout=httpx.Timeout(timeout),
        follow_redirects=True,
        max_redirects=MAX_REDIRECTS,
        headers={"User-Agent": USER_AGENT,
                 "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"},
        event_hooks={"request": [_guard]},
    )


async def visit_site(listed_url: str, extract: Callable[[str, str], list],
                     timeout: float = TIMEOUT_SECONDS) -> SiteVisit:
    """`extract(html, source_url)` returns the contacts a page shows (ContactDiscoveryEngine._extract_from_html)."""
    visit = SiteVisit(listed_url=listed_url)
    url = (listed_url or "").strip()
    if not url:
        visit.note = "No website address"
        return visit
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    if social_platform(url):
        visit.outcome = "social"
        return visit
    if is_listing(url):
        visit.outcome, visit.note = "listing", "Listed address is a directory / Google page, not an own site"
        return visit

    async with new_client(timeout) as client:
        robots, robots_page = await _load_robots(client, _origin(url), timeout, visit)
        if robots is None and robots_page.error == "connect" and url.startswith("https://"):
            # Same fallback as WebsiteResolver: no working HTTPS (refused or bad certificate) -> plain HTTP.
            url = "http://" + url[len("https://"):]
            robots, robots_page = await _load_robots(client, _origin(url), timeout, visit)
        if robots is None:
            visit.outcome = "blocked" if robots_page.error == "blocked" else "failed"
            visit.note = ("Domain has no DNS record" if _no_dns(robots_page)
                          else f"Site unreachable ({robots_page.error})")
            return visit
        if not robots.can_fetch(url):
            visit.outcome = "robots_blocked"
            visit.note = ("robots.txt unavailable (HTTP %s): treated as disallow" % robots_page.status
                          if visit.robots == "unavailable" else "robots.txt disallows the homepage")
            return visit

        home = await fetch(client, url, timeout)
        visit.requests += 1
        visit.http_status, visit.final_url = home.status, home.final_url
        visit.pages.append({"url": url, "status": home.status, "error": home.error, "emails": 0})
        if home.error:
            visit.outcome = "blocked" if home.error == "blocked" else "failed"
            visit.note = home.error
            return visit
        final = home.final_url or url
        if social_platform(final):
            visit.outcome, visit.note = "social", "Homepage redirects to a social profile"
            return visit
        if is_listing(final):
            visit.outcome, visit.note = "listing", "Homepage redirects to a directory / Google page"
            return visit
        visit.has_https = final.startswith("https://")
        if home.status in (401, 403, 429):
            visit.outcome = "protected"   # spec row 6: the site exists
            return visit
        if home.status >= 500 or home.status in (404, 410):
            visit.note = f"HTTP {home.status}"
            return visit
        if any(token in home.body[:4000].lower() for token in PARKED_TOKENS):
            visit.note = "Parked / coming-soon page"
            return visit
        visit.outcome = "ok"
        is_html = "html" in home.content_type
        if is_html:
            visit.has_viewport = WebsiteAuditor().audit_html(final, home.body).has_viewport_meta
            visit.contacts = extract(home.body, final)
            visit.pages[-1]["emails"] = len(visit.contacts)

        if _origin(final) != _origin(url):
            # The homepage moved to another host: its own robots.txt decides the contact pages.
            robots, _ = await _load_robots(client, _origin(final), timeout, visit)
            robots = robots or RobotsRules.disallow_all()
        for path in CONTACT_PATHS:
            if visit.contacts:
                break
            target = urljoin(final, path)
            if not robots.can_fetch(target):
                visit.pages.append({"url": target, "status": None, "error": "robots_disallowed", "emails": 0})
                continue
            page = await fetch(client, target, timeout)
            visit.requests += 1
            entry = {"url": target, "status": page.status, "error": page.error, "emails": 0}
            visit.pages.append(entry)
            landed = page.final_url or target
            if (page.error or page.status != 200 or "html" not in page.content_type
                    or social_platform(landed) or is_listing(landed)):
                continue
            found = extract(page.body, landed)
            entry["emails"] = len(found)
            visit.contacts.extend(found)
    return visit
