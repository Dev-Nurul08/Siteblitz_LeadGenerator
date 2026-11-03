"""
Tests for WebsiteResolver (Phase 2).
"""

from unittest.mock import AsyncMock, patch
import httpx
import pytest

from backend.app.engines.opportunity.resolver import WebsiteResolver
from backend.app.models.business import WebsiteStatus


class TestWebsiteResolver:
    """Test suite for WebsiteResolver."""

    def setup_method(self):
        self.resolver = WebsiteResolver()

    def test_normalize_url(self):
        """Prepends https:// and strips whitespace."""
        assert self.resolver.normalize_url("example.com") == "https://example.com"
        assert self.resolver.normalize_url("  http://mytest.org ") == "http://mytest.org"
        assert self.resolver.normalize_url("https://alreadysecure.net") == "https://alreadysecure.net"
        assert self.resolver.normalize_url(None) is None
        assert self.resolver.normalize_url("") is None

    @pytest.mark.asyncio
    async def test_resolve_success_reachable_ssl(self):
        """Resolves accessible site with SSL."""
        mock_resp = httpx.Response(
            status_code=200,
            html="<html><head><title>Test</title></head><body>Hello</body></html>",
            request=httpx.Request("GET", "https://example.com"),
        )

        with patch.object(httpx.AsyncClient, "get", AsyncMock(return_value=mock_resp)):
            result = await self.resolver.resolve("example.com")

            assert result.is_reachable is True
            assert result.has_ssl is True
            assert result.http_status == 200
            assert result.status == WebsiteStatus.FOUND

    @pytest.mark.asyncio
    async def test_resolve_under_construction_detection(self):
        """Detects domain parking or under construction text."""
        mock_resp = httpx.Response(
            status_code=200,
            html="<html><body><h1>Coming Soon</h1><p>Our website in development</p></body></html>",
            request=httpx.Request("GET", "https://parked.com"),
        )

        with patch.object(httpx.AsyncClient, "get", AsyncMock(return_value=mock_resp)):
            result = await self.resolver.resolve("https://parked.com")

            assert result.is_reachable is True
            assert result.status == WebsiteStatus.UNDER_CONSTRUCTION

    @pytest.mark.asyncio
    async def test_resolve_broken_status(self):
        """Handles HTTP 500 error code."""
        mock_resp = httpx.Response(
            status_code=500,
            request=httpx.Request("GET", "https://broken.com"),
        )

        with patch.object(httpx.AsyncClient, "get", AsyncMock(return_value=mock_resp)):
            result = await self.resolver.resolve("https://broken.com")

            assert result.is_reachable is False
            assert result.status == WebsiteStatus.BROKEN
