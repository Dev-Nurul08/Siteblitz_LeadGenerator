"""
"All sources" adapter — Overture Places + OpenStreetMap in one search (one job).

Why: the founder wants as many targeted businesses per run as exist. The sources overlap only
partly (Udaipur cafés 2026-11-08: OSM added 22 cafés Overture did not have). Both run at the same
time; the discovery service then merges duplicates (same source id, same phone, or same name in
the same place). A failure of one source never loses the other's results — it is reported as an
error on the job (status PARTIAL) with the reason.
"""

import asyncio
from typing import Optional

from backend.app.engines.discovery.base import AdapterResult, BaseSourceAdapter
from backend.app.engines.discovery.osm import OSMAdapter
from backend.app.engines.discovery.overture import OvertureAdapter


class CombinedAdapter(BaseSourceAdapter):
    def __init__(self, rate_limit_rpm: int = 30):
        super().__init__(rate_limit_rpm=rate_limit_rpm)

    def get_source_metadata(self) -> dict:
        return {
            "name": "All sources (Overture + OpenStreetMap)",
            "slug": "all_sources",
            "description": "Runs Overture Places and OpenStreetMap together and merges duplicates.",
            "license_type": "OPEN_LICENSE",
            "license_url": "https://docs.overturemaps.org/attribution/",
            "license_notes": "Overture: CDLA-Permissive-2.0 / Apache-2.0. OpenStreetMap: ODbL (attribution, share-alike for the database).",
            "attribution_required": True,
            "attribution_text": "© Overture Maps Foundation and its providers · © OpenStreetMap contributors",
            "allows_commercial_storage": True,
            "allows_contact_enrichment": True,
            "allows_marketing_use": False,  # the OSM part keeps the original adapter's conservative flag
            "adapter_class": "backend.app.engines.discovery.combined.CombinedAdapter",
        }

    async def discover(self, *, country_code: Optional[str] = None, region: Optional[str] = None,
                       city: Optional[str] = None, category: Optional[str] = None,
                       latitude: Optional[float] = None, longitude: Optional[float] = None,
                       radius_km: Optional[float] = None, max_results: int = 500,
                       cursor: Optional[str] = None, query_params: Optional[dict] = None) -> AdapterResult:
        kwargs = dict(country_code=country_code, region=region, city=city, category=category,
                      latitude=latitude, longitude=longitude, radius_km=radius_km,
                      max_results=max_results, query_params=query_params)
        overture, osm = await asyncio.gather(
            OvertureAdapter().discover(**kwargs),
            OSMAdapter().discover(**{k: v for k, v in kwargs.items() if k != "query_params"}),
            return_exceptions=True,
        )
        result = AdapterResult()
        for name, part in (("Overture", overture), ("OpenStreetMap", osm)):
            if isinstance(part, Exception):
                result.errors.append(self._create_error("source_failed", f"{name}: {part}", is_retryable=True))
                continue
            result.businesses += part.businesses
            result.errors += [{**e, "message": f"{name}: {e.get('message')}"} for e in part.errors]
        # Overture reports every match in the area (before max_results); OSM has no total. The two
        # overlap, so their sum would overstate. max() = "everything was fetched" when Overture was
        # under the limit, and Overture's full count when it was capped (then: raise Max results).
        overture_total = overture.total_available if not isinstance(overture, Exception) else 0
        result.total_available = max(overture_total or 0, len(result.businesses))
        return result
