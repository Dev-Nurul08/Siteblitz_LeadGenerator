"""
Website Resolver module.

Validates URLs, tests HTTP reachability, follows redirects, checks SSL,
and determines canonical website status (FOUND, BROKEN, UNDER_CONSTRUCTION, NOT_FOUND).
"""

from dataclasses import dataclass
import time
from typing import Optional
from urllib.parse import urlparse

import httpx
import structlog

from backend.app.models.business import WebsiteStatus

logger = structlog.get_logger(__name__)


@dataclass
class ResolutionResult:
    """Outcome of resolving a business website URL."""

    original_url: str
    final_url: Optional[str] = None
    is_reachable: bool = False
    http_status: Optional[int] = None
    has_ssl: bool = False
    load_time_seconds: Optional[float] = None
    status: WebsiteStatus = WebsiteStatus.UNKNOWN
    error_message: Optional[str] = None
    html_content: Optional[str] = None
    headers: Optional[dict] = None


class WebsiteResolver:
    """
    Probes business website endpoints to verify existence, reachability,
    SSL configuration, and redirect chains.
    """

    def __init__(
        self,
        timeout_seconds: float = 12.0,
        user_agent: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SiteBlitzAuditor/1.0"
        ),
    ):
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    @staticmethod
    def normalize_url(url: Optional[str]) -> Optional[str]:
        """Ensure scheme is present and clean URL."""
        if not url:
            return None
        cleaned = url.strip()
        if not cleaned:
            return None
        if not cleaned.startswith(("http://", "https://")):
            cleaned = f"https://{cleaned}"
        return cleaned

    async def resolve(self, url: str) -> ResolutionResult:
        """
        Probe a website URL and determine its reachability, SSL, and status.
        """
        normalized = self.normalize_url(url)
        if not normalized:
            return ResolutionResult(
                original_url=url or "",
                is_reachable=False,
                status=WebsiteStatus.NOT_FOUND,
                error_message="Invalid or empty URL",
            )

        start_time = time.monotonic()
        client_headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout_seconds,
                follow_redirects=True,
                verify=True,  # Test SSL certificate
            ) as client:
                response = await client.get(normalized, headers=client_headers)
                elapsed = time.monotonic() - start_time

                final_url = str(response.url)
                has_ssl = final_url.startswith("https://")
                status_code = response.status_code

                # Classify status
                if 200 <= status_code < 400:
                    html_snippet = response.text[:2000].lower()
                    if any(
                        token in html_snippet
                        for token in [
                            "under construction",
                            "coming soon",
                            "website in development",
                            "domain parked",
                            "buy this domain",
                        ]
                    ):
                        website_status = WebsiteStatus.UNDER_CONSTRUCTION
                    else:
                        website_status = WebsiteStatus.FOUND
                elif status_code in [404, 410]:
                    website_status = WebsiteStatus.NOT_FOUND
                else:
                    website_status = WebsiteStatus.BROKEN

                return ResolutionResult(
                    original_url=normalized,
                    final_url=final_url,
                    is_reachable=(status_code < 500),
                    http_status=status_code,
                    has_ssl=has_ssl,
                    load_time_seconds=round(elapsed, 3),
                    status=website_status,
                    html_content=response.text,
                    headers=dict(response.headers),
                )

        except httpx.ConnectError:
            # Try HTTP if HTTPS failed (might not have SSL)
            if normalized.startswith("https://"):
                http_fallback = normalized.replace("https://", "http://", 1)
                try:
                    async with httpx.AsyncClient(
                        timeout=self.timeout_seconds,
                        follow_redirects=True,
                    ) as client:
                        response = await client.get(http_fallback, headers=client_headers)
                        elapsed = time.monotonic() - start_time
                        return ResolutionResult(
                            original_url=normalized,
                            final_url=str(response.url),
                            is_reachable=True,
                            http_status=response.status_code,
                            has_ssl=False,  # Proves lack of SSL!
                            load_time_seconds=round(elapsed, 3),
                            status=WebsiteStatus.FOUND if response.status_code < 400 else WebsiteStatus.BROKEN,
                            html_content=response.text,
                            headers=dict(response.headers),
                        )
                except Exception:
                    pass

            return ResolutionResult(
                original_url=normalized,
                is_reachable=False,
                status=WebsiteStatus.BROKEN,
                error_message="Could not establish connection to host",
            )

        except httpx.TimeoutException:
            return ResolutionResult(
                original_url=normalized,
                is_reachable=False,
                status=WebsiteStatus.BROKEN,
                error_message=f"Connection timed out after {self.timeout_seconds}s",
            )

        except Exception as e:
            logger.warning("website_resolve_failed", url=normalized, error=str(e))
            return ResolutionResult(
                original_url=normalized,
                is_reachable=False,
                status=WebsiteStatus.BROKEN,
                error_message=str(e),
            )
