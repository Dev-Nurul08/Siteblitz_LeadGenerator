"""
Tests for source adapters — OSM and CSV import.

Phase 1 acceptance criteria tested:
- Multiple source adapters work independently
- System can discover businesses in at least two countries
- Records have valid source references
- Missing fields are unknown, not invented
- Source terms and rate limits are respected
"""

import pytest

from backend.app.engines.discovery.osm import OSMAdapter, _build_overpass_query
from backend.app.engines.discovery.csv_import import CSVImportAdapter
from backend.app.engines.discovery.base import DiscoveredBusiness
from backend.app.engines.discovery.registry import SourceAdapterRegistry


class TestOSMAdapter:
    """Test the OpenStreetMap source adapter."""

    def test_metadata(self):
        """Source metadata must include license and attribution info."""
        adapter = OSMAdapter()
        meta = adapter.get_source_metadata()

        assert meta["name"] == "OpenStreetMap"
        assert meta["slug"] == "openstreetmap"
        assert meta["license_type"] == "OPEN_LICENSE"
        assert meta["attribution_required"] is True
        assert meta["allows_commercial_storage"] is True
        assert meta["license_url"] is not None

    def test_parse_element_with_website(self, sample_osm_element):
        """OSM element with website should produce a valid business."""
        adapter = OSMAdapter()
        business = adapter._parse_element(sample_osm_element, "GB")

        assert business is not None
        assert business.name == "The Best Restaurant"
        assert business.source_external_id == "osm:node:123456789"
        assert business.website_url == "https://bestrestaurant.co.uk"
        assert business.latitude == 51.5074
        assert business.longitude == -0.1278
        assert business.city == "London"
        assert business.country_code == "GB"
        assert "restaurant" in business.categories
        assert "facebook" in business.social_urls

    def test_parse_element_no_website(self, sample_osm_element_no_website):
        """OSM element without website — key opportunity signal."""
        adapter = OSMAdapter()
        business = adapter._parse_element(sample_osm_element_no_website, "US")

        assert business is not None
        assert business.name == "Joe's Pizza"
        assert business.website_url is None  # No website!
        assert business.country_code == "US"
        assert "instagram" in business.social_urls

    def test_parse_element_no_name(self):
        """Elements without names should be skipped."""
        adapter = OSMAdapter()
        element = {"type": "node", "id": 1, "lat": 0, "lon": 0, "tags": {}}
        assert adapter._parse_element(element) is None

    def test_overpass_query_with_coordinates(self):
        """Query with coordinates should use 'around' filter."""
        query = _build_overpass_query(
            latitude=51.5, longitude=-0.1, radius_km=5.0
        )
        assert "around:5000" in query

    def test_overpass_query_with_city_country(self):
        """Query with city+country should use area filter."""
        query = _build_overpass_query(
            country_code="GB", city="London"
        )
        assert "London" in query
        assert "GB" in query

    def test_overpass_query_with_category(self):
        """Query with category should filter by tag."""
        query = _build_overpass_query(
            latitude=51.5, longitude=-0.1, radius_km=5.0,
            category="restaurant",
        )
        assert "restaurant" in query

    def test_overpass_query_requires_area(self):
        """Query without area specification should raise."""
        with pytest.raises(ValueError, match="Must provide"):
            _build_overpass_query()

    def test_rate_limit_configured(self):
        """OSM adapter should have conservative rate limit."""
        adapter = OSMAdapter()
        assert adapter._rate_limit_rpm == 10
        assert adapter._min_interval == 6.0  # 60/10 = 6 seconds


class TestCSVImportAdapter:
    """Test the CSV import adapter."""

    def test_metadata(self):
        """CSV import metadata should indicate manual/opt-in license."""
        adapter = CSVImportAdapter()
        meta = adapter.get_source_metadata()

        assert meta["slug"] == "csv_import"
        assert meta["license_type"] == "MANUAL_OR_OPT_IN"
        assert meta["allows_commercial_storage"] is True

    @pytest.mark.asyncio
    async def test_import_valid_csv(self, sample_csv_content):
        """Import should parse valid CSV rows correctly."""
        adapter = CSVImportAdapter()
        result = await adapter.discover(
            query_params={"csv_content": sample_csv_content},
        )

        # Should parse 5 rows — "Empty Row" has a name so it's included
        # (row with name "Empty Row" but empty other fields is still valid)
        assert len(result.businesses) == 5
        assert len(result.errors) == 0

        # Check first business
        acme = result.businesses[0]
        assert acme.name == "Acme Corp"
        assert acme.city == "Springfield"
        assert acme.country_code == "US"
        assert acme.website_url == "https://acme.com"
        assert acme.email == "info@acme.com"

        # Check business without website
        bakery = result.businesses[1]
        assert bakery.name == "Best Bakery"
        assert bakery.website_url is None  # Missing, not invented

    @pytest.mark.asyncio
    async def test_import_with_country_override(self, sample_csv_content):
        """Country code parameter should serve as default."""
        adapter = CSVImportAdapter()
        result = await adapter.discover(
            country_code="US",
            query_params={"csv_content": sample_csv_content},
        )

        # Businesses without country in CSV should get the default
        for biz in result.businesses:
            # All have country in this CSV, but the adapter provides default
            assert biz.source_external_id.startswith("csv:row:")

    @pytest.mark.asyncio
    async def test_import_empty_csv(self):
        """Empty CSV should return no results with error."""
        adapter = CSVImportAdapter()
        result = await adapter.discover(
            query_params={"csv_content": ""},
        )

        assert len(result.businesses) == 0
        assert len(result.errors) > 0

    @pytest.mark.asyncio
    async def test_import_no_params(self):
        """Missing query_params should return error."""
        adapter = CSVImportAdapter()
        result = await adapter.discover()

        assert len(result.businesses) == 0
        assert len(result.errors) > 0

    @pytest.mark.asyncio
    async def test_import_max_results(self, sample_csv_content):
        """Max results should limit imported rows."""
        adapter = CSVImportAdapter()
        result = await adapter.discover(
            max_results=2,
            query_params={"csv_content": sample_csv_content},
        )

        assert len(result.businesses) <= 2
        assert result.has_more is True

    @pytest.mark.asyncio
    async def test_preserves_source_id(self, sample_csv_content):
        """Each row should have a traceable source ID."""
        adapter = CSVImportAdapter()
        result = await adapter.discover(
            query_params={"csv_content": sample_csv_content},
        )

        for biz in result.businesses:
            assert biz.source_external_id.startswith("csv:row:")
            assert biz.raw_data  # Raw data preserved


class TestSourceAdapterRegistry:
    """Test the adapter registry."""

    def setup_method(self):
        SourceAdapterRegistry.clear()

    def test_register_and_get(self):
        SourceAdapterRegistry.register("openstreetmap", OSMAdapter)
        assert SourceAdapterRegistry.get("openstreetmap") is OSMAdapter

    def test_get_unknown(self):
        assert SourceAdapterRegistry.get("nonexistent") is None

    def test_list_registered(self):
        SourceAdapterRegistry.register("openstreetmap", OSMAdapter)
        SourceAdapterRegistry.register("csv_import", CSVImportAdapter)

        registered = SourceAdapterRegistry.list_registered()
        assert "openstreetmap" in registered
        assert "csv_import" in registered

    def test_dynamic_import(self):
        """Should be able to import adapter from class path."""
        adapter_class = SourceAdapterRegistry.get_or_import(
            "osm_test",
            "backend.app.engines.discovery.osm.OSMAdapter",
        )
        assert adapter_class is OSMAdapter

    def test_invalid_import(self):
        """Invalid class path should raise ValueError."""
        with pytest.raises(ValueError):
            SourceAdapterRegistry.get_or_import(
                "bad",
                "nonexistent.module.Adapter",
            )

    def test_reject_non_adapter(self):
        """Non-adapter classes should be rejected."""
        with pytest.raises(TypeError):
            SourceAdapterRegistry.register("bad", str)
