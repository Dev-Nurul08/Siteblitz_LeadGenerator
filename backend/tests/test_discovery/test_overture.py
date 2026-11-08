"""Tests for the Overture Maps Places adapter (no network: geocoder and DuckDB are stubbed)."""

import pytest

from backend.app.engines.discovery.overture import (
    OvertureAdapter,
    build_query,
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
    "total_available": 1,
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


def test_category_matching_is_whole_word_and_includes_names():
    import re
    from backend.app.engines.discovery.categories import category_regex, name_regex
    dent = re.compile(category_regex("dentist"))
    assert dent.search("dental_clinic") and dent.search("dentist")
    assert not dent.search("student_union")          # old %dent% substring bug
    assert not re.search(category_regex("accountant"), "taxi_service")
    names = re.compile(name_regex("salon"))
    assert names.search("glow unisex salon") and names.search("hair studio")
    assert names.search("classic mens parlour") and not names.search("krishna ice cream parlour")
    assert not names.search("stanza living | unisex pg")
    assert not names.search("comfy chair store")     # "hair" inside "chair"
    assert re.search(name_regex("dentist"), "smile dental care")
    assert category_regex("") is None and name_regex(None) is None


def test_query_uses_placeholders_only():
    sql = build_query("2026-10-21.0", True)
    assert sql.count("?") == 4 + 1 + 3 + 1  # bbox(4) + confidence + category/taxonomy/name + limit
    assert "Udaipur" not in sql and "cafe" not in sql
    assert "count(*) OVER ()" in sql
    with_country = build_query("2026-10-21.0", True, True)
    assert with_country.count("?") == 4 + 1 + 1 + 3 + 1  # + country
    assert "addresses[1].country" in with_country and "addresses[1].country" not in sql


@pytest.mark.asyncio
async def test_discover_requires_city_or_coordinates():
    result = await OvertureAdapter().discover(country_code="IN")
    assert not result.businesses
    assert result.errors[0]["error_type"] == "invalid_area"


@pytest.mark.asyncio
async def test_discover_rejects_district_sized_area(monkeypatch):
    async def huge_bbox(self, city, cc, state=None):
        return 70.0, 75.0, 20.0, 26.0

    monkeypatch.setattr(OvertureAdapter, "_city_bbox", huge_bbox)
    result = await OvertureAdapter().discover(country_code="IN", city="Rajasthan")
    assert result.errors[0]["error_type"] == "invalid_area"


@pytest.mark.asyncio
async def test_discover_maps_rows_and_passes_parameters(monkeypatch):
    seen = {}

    async def city_bbox(self, city, cc, state=None):
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
    from backend.app.engines.discovery.categories import category_regex, name_regex
    assert seen["params"] == [73.62, 73.80, 24.50, 24.66, 0.0, "IN",
                              category_regex("cafe"), category_regex("cafe"), name_regex("cafe"), 50]
    assert not result.errors
