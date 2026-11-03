"""
Tests for Wikidata source adapter.
"""

import pytest
from unittest.mock import AsyncMock, patch
import httpx

from backend.app.engines.discovery.wikidata import (
    WikidataAdapter,
    build_sparql_query,
)


class TestWikidataAdapter:
    """Test suite for WikidataAdapter."""

    def test_metadata(self):
        """Adapter metadata matches CC0 open-license specifications."""
        adapter = WikidataAdapter()
        meta = adapter.get_source_metadata()

        assert meta["name"] == "Wikidata"
        assert meta["slug"] == "wikidata"
        assert meta["license_type"] == "OPEN_LICENSE"
        assert meta["allows_commercial_storage"] is True
        assert meta["allows_contact_enrichment"] is True
        assert meta["allows_marketing_use"] is True
        assert meta["attribution_required"] is False
        assert meta["rate_limit_rpm"] == 30

    def test_sparql_query_builder(self):
        """Builds proper SPARQL with country, city, and category filters."""
        # Query with country and city
        query = build_sparql_query(
            country_code="GB",
            city="London",
            category="software",
            max_results=50,
        )
        assert "wd:Q145" in query  # UK country QID
        assert "London" in query
        assert "LIMIT 50" in query
        assert "wdt:P856" in query  # website property

    def test_sparql_query_unknown_country(self):
        """Unknown country code creates ISO 3166-1 alpha-2 property filter."""
        query = build_sparql_query(
            country_code="NZ",
            max_results=25,
        )
        assert 'wdt:P297 "NZ"' in query
        assert "LIMIT 25" in query

    def test_parse_binding_valid(self):
        """Valid SPARQL binding parses into a DiscoveredBusiness."""
        adapter = WikidataAdapter()
        binding = {
            "item": {"type": "uri", "value": "http://www.wikidata.org/entity/Q2283"},
            "itemLabel": {"type": "literal", "value": "Microsoft"},
            "description": {"type": "literal", "value": "American multinational technology corporation"},
            "website": {"type": "uri", "value": "https://www.microsoft.com"},
            "coord": {"type": "literal", "value": "Point(-122.13 47.64)"},
            "hqLabel": {"type": "literal", "value": "Redmond"},
            "countryCode": {"type": "literal", "value": "US"},
        }

        biz = adapter._parse_binding(binding)
        assert biz is not None
        assert biz.source_external_id == "wikidata:Q2283"
        assert biz.source_external_url == "http://www.wikidata.org/entity/Q2283"
        assert biz.name == "Microsoft"
        assert biz.website_url == "https://www.microsoft.com"
        assert biz.city == "Redmond"
        assert biz.country_code == "US"
        assert biz.longitude == -122.13
        assert biz.latitude == 47.64

    def test_parse_binding_skips_unlabelled(self):
        """Skips raw Q-identifier if no human-readable label was returned."""
        adapter = WikidataAdapter()
        binding = {
            "item": {"type": "uri", "value": "http://www.wikidata.org/entity/Q99999999"},
            "itemLabel": {"type": "literal", "value": "Q99999999"},
        }
        biz = adapter._parse_binding(binding)
        assert biz is None

    @pytest.mark.asyncio
    async def test_discover_mocked_success(self):
        """Executes discovery with mocked HTTP response."""
        adapter = WikidataAdapter()
        mock_data = {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q1001"},
                        "itemLabel": {"value": "Acme Technologies"},
                        "website": {"value": "https://acme.example"},
                        "countryCode": {"value": "GB"},
                    }
                ]
            }
        }

        mock_resp = httpx.Response(
            status_code=200,
            json=mock_data,
            request=httpx.Request("GET", "https://query.wikidata.org/sparql"),
        )

        with patch.object(httpx.AsyncClient, "get", AsyncMock(return_value=mock_resp)):
            result = await adapter.discover(country_code="GB", max_results=10)

            assert len(result.businesses) == 1
            assert result.businesses[0].name == "Acme Technologies"
            assert result.businesses[0].country_code == "GB"
            assert result.businesses[0].source_external_id == "wikidata:Q1001"
            assert len(result.errors) == 0

    @pytest.mark.asyncio
    async def test_discover_rate_limit(self):
        """Handles HTTP 429 rate limit correctly."""
        adapter = WikidataAdapter()
        mock_resp = httpx.Response(
            status_code=429,
            request=httpx.Request("GET", "https://query.wikidata.org/sparql"),
        )

        with patch.object(httpx.AsyncClient, "get", AsyncMock(return_value=mock_resp)):
            result = await adapter.discover(country_code="US")
            assert len(result.businesses) == 0
            assert len(result.errors) == 1
            assert result.errors[0]["error_type"] == "rate_limit"
            assert result.errors[0]["is_retryable"] is True
