"""SSRF guard: server-side fetches must never reach private / internal addresses."""

import httpx
import pytest

from backend.app.engines.opportunity.resolver import (
    UnsafeDestinationError,
    WebsiteResolver,
    ensure_public_destination,
)
from backend.app.models.business import WebsiteStatus


@pytest.mark.asyncio
@pytest.mark.parametrize("url", [
    "http://127.0.0.1:8000/api/v1/sources",
    "http://localhost/",
    "http://169.254.169.254/latest/meta-data/",  # cloud metadata
    "http://10.0.0.5/",
    "http://192.168.1.1/",
    "http://[::1]/",
])
async def test_hook_blocks_internal_addresses(url):
    with pytest.raises(UnsafeDestinationError):
        await ensure_public_destination(httpx.Request("GET", url))


@pytest.mark.asyncio
async def test_hook_allows_public_ip_literal():
    await ensure_public_destination(httpx.Request("GET", "http://1.1.1.1/"))


@pytest.mark.asyncio
async def test_resolver_reports_blocked_url_without_fetching():
    result = await WebsiteResolver().resolve("http://127.0.0.1:8000/health")
    assert result.status == WebsiteStatus.BROKEN
    assert result.is_reachable is False
    assert result.error_message.startswith("Blocked:")
    assert result.html_content is None
