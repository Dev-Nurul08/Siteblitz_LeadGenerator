"""All-sources adapter: both sources merged; one failing source never loses the other's results."""

import pytest

from backend.app.engines.discovery.base import AdapterResult, DiscoveredBusiness
from backend.app.engines.discovery.combined import CombinedAdapter
from backend.app.engines.discovery.osm import OSMAdapter
from backend.app.engines.discovery.overture import OvertureAdapter


def biz(ext, name):
    return DiscoveredBusiness(source_external_id=ext, name=name)


@pytest.mark.asyncio
async def test_merges_both_sources_and_counts_available(monkeypatch):
    async def ov(self, **kw):
        return AdapterResult(businesses=[biz("overture:1", "A"), biz("overture:2", "B")], total_available=950)

    async def osm(self, **kw):
        return AdapterResult(businesses=[biz("osm:node:9", "C")])

    monkeypatch.setattr(OvertureAdapter, "discover", ov)
    monkeypatch.setattr(OSMAdapter, "discover", osm)
    result = await CombinedAdapter().discover(city="Pune", country_code="IN", category="salon", max_results=2)
    assert [b.source_external_id for b in result.businesses] == ["overture:1", "overture:2", "osm:node:9"]
    assert result.total_available == 950  # Overture was capped: there are more to fetch


@pytest.mark.asyncio
async def test_one_source_failing_keeps_the_other(monkeypatch):
    async def ov(self, **kw):
        return AdapterResult(businesses=[biz("overture:1", "A")], total_available=1)

    async def osm(self, **kw):
        raise RuntimeError("Overpass 504")

    monkeypatch.setattr(OvertureAdapter, "discover", ov)
    monkeypatch.setattr(OSMAdapter, "discover", osm)
    result = await CombinedAdapter().discover(city="Udaipur", country_code="IN", category="cafe")
    assert len(result.businesses) == 1
    assert "OpenStreetMap" in result.errors[0]["message"] and "504" in result.errors[0]["message"]
