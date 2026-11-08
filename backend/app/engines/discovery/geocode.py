"""
City name → bounding box, shared by every source so they all search the same area.

One Nominatim request per (city, country), cached for the life of the process. Nominatim's usage
policy allows at most 1 request per second with an identifying User-Agent, so calls are
serialised behind a lock and spaced 1 s apart.

Why OSM uses this too (2026-11-08): resolving a city by its OSM boundary name matched the whole
district ("Udaipur" district, admin_level 5 — about 13,000 km²) plus same-named villages in other
states, and the Overpass query timed out after 120 s. A bounding box query of the city returns in
seconds and covers the same ground as the Overture search.
"""

import asyncio
import time
from typing import Optional

import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "SiteBlitzLeadGenerator/0.2 (internal business research tool)"

_cache: dict[tuple[str, str], tuple[float, float, float, float]] = {}
_lock = asyncio.Lock()
_last_call = 0.0


async def city_bbox(city: str, country_code: Optional[str]) -> tuple[float, float, float, float]:
    """(west, east, south, north). Raises LookupError when the city is unknown."""
    global _last_call
    key = (city.strip().lower(), (country_code or "").strip().lower())
    if key in _cache:
        return _cache[key]
    async with _lock:
        if key in _cache:
            return _cache[key]
        wait = 1.0 - (time.monotonic() - _last_call)
        if wait > 0:
            await asyncio.sleep(wait)
        params = {"city": city.strip(), "format": "jsonv2", "limit": 1}
        if country_code:
            params["countrycodes"] = country_code.strip().lower()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(NOMINATIM_URL, params=params, headers={"User-Agent": USER_AGENT})
        _last_call = time.monotonic()
        response.raise_for_status()
        hits = response.json()
        if not hits:
            raise LookupError(f"City '{city}' was not found in country '{country_code or 'any'}'.")
        south, north, west, east = (float(v) for v in hits[0]["boundingbox"])
        _cache[key] = (west, east, south, north)
        return _cache[key]
