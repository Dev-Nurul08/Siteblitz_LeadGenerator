"""Tests for the Overture Maps Places adapter (no network: geocoder and DuckDB are stubbed)."""

import pytest

from backend.app.engines.discovery.overture import (
    OvertureAdapter,
    build_query,
    category_patterns,
    row_to_business,
    social_platform,
)

ROW = {
    "id": "08f3d0a2-0001",
    "name": "The Sookun Cafe",
    "confidence": 0.66,
    "operating_status": None,
    "basic_category": "cafe",
    "taxonomy_primary": "cafe",
    "websites": ["https://instagram.com/thesookun"],
    "socials": ["https://www.facebook.com/107499394415056"],
    "phones": ["+919166111587"],
    "emails": None,
    "addresses": [{"freeform": "Lake Rd", "locality": "Udaipur", "postcode": "313001",
                   "region": "RJ", "country": "IN"}],
    "brand_name": None,
    "brand_wikidata": None,
    "lon": 73.68,
    "lat": 24.58,
    "datasets": ["meta"],
}


def test_social_platform_matches_hosts_not_substrings():
    assert social_platform("https://www.instagram.com/x") == "instagram"
    assert social_platform("facebook.com/123") == "facebook"
    assert social_platform("https://x.com/brand") == "twitter"
    assert social_platform("https://www.fedex.com") is None  # contains "x.com" as text only
    assert social_platform("https://box.com") is None
    assert social_platform(None) is None


def test_row_with_only_social_links_has_no_own_website():
    biz = row_to_business(ROW, "Udaipur", "IN")
    assert biz.website_url is None
    assert biz.social_urls == {
        "instagram": "https://instagram.com/thesookun",
        "facebook": "https://www.facebook.com/107499394415056",
    }
    assert biz.phone == "+919166111587"
    assert biz.city == "Udaipur" and biz.country_code == "IN"
    assert biz.source_external_id == "overture:08f3d0a2-0001"
    assert biz.categories == ["cafe"]


def test_row_with_real_website_keeps_it():
    row = dict(ROW, websites=["https://instagram.com/a", "https://sookuncafe.in"])
    assert row_to_business(row, "Udaipur", "IN").website_url == "https://sookuncafe.in"


def test_category_patterns_and_query_use_placeholders_only():
    assert category_patterns("cafe") == ["%cafe%", "%coffee%"]
    assert category_patterns("") == []
    sql = build_query("2026-10-21.0", 2)
    assert sql.count("?") == 5 + 2 * 2 + 1  # bbox(4) + confidence + 2 patterns × 2 + limit
    assert "Udaipur" not in sql and "cafe" not in sql


@pytest.mark.asyncio
async def test_discover_requires_city_or_coordinates():
    result = await OvertureAdapter().discover(country_code="IN")
    assert not result.businesses
    assert result.errors[0]["error_type"] == "invalid_area"


@pytest.mark.asyncio
async def test_discover_rejects_district_sized_area(monkeypatch):
    async def huge_bbox(self, city, cc):
        return 70.0, 75.0, 20.0, 26.0

    monkeypatch.setattr(OvertureAdapter, "_city_bbox", huge_bbox)
    result = await OvertureAdapter().discover(country_code="IN", city="Rajasthan")
    assert result.errors[0]["error_type"] == "invalid_area"


@pytest.mark.asyncio
async def test_discover_maps_rows_and_passes_parameters(monkeypatch):
    seen = {}

    async def city_bbox(self, city, cc):
        return 73.62, 73.80, 24.50, 24.66

    def fake_query(self, sql, params):
        seen["params"] = params
        return [ROW]

    monkeypatch.setattr(OvertureAdapter, "_city_bbox", city_bbox)
    monkeypatch.setattr(OvertureAdapter, "_run_query", fake_query)
    result = await OvertureAdapter().discover(
        country_code="IN", city=" Udaipur ", category="cafe", max_results=50
    )
    assert [b.name for b in result.businesses] == ["The Sookun Cafe"]
    assert seen["params"] == [73.62, 73.80, 24.50, 24.66, 0.0,
                              "%cafe%", "%cafe%", "%coffee%", "%coffee%", 50]
    assert not result.errors
