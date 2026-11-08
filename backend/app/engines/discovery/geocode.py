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

_cache: dict[tuple[str, str, str], tuple[float, float, float, float]] = {}
# What each lookup actually resolved to (shown on the job so a wrong match is visible).
_resolved: dict[tuple[str, str, str], dict] = {}
_lock = asyncio.Lock()
_last_call = 0.0


def _key(city: str, country_code: Optional[str], state: Optional[str]) -> tuple[str, str, str]:
    return (city.strip().lower(), (country_code or "").strip().lower(), (state or "").strip().lower())


def resolved_place(city: str, country_code: Optional[str], state: Optional[str] = None) -> Optional[dict]:
    """{"name", "type", "bbox_km"} of the last lookup for this city, if any."""
    return _resolved.get(_key(city, country_code, state))


async def city_bbox(city: str, country_code: Optional[str],
                    state: Optional[str] = None) -> tuple[float, float, float, float]:
    """(west, east, south, north). `state` disambiguates same-named cities. LookupError if unknown."""
    global _last_call
    key = _key(city, country_code, state)
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
        if state and state.strip():
            params["state"] = state.strip()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(NOMINATIM_URL, params=params, headers={"User-Agent": USER_AGENT})
        _last_call = time.monotonic()
        response.raise_for_status()
        hits = response.json()
        if not hits:
            raise LookupError(f"City '{city}' was not found in country '{country_code or 'any'}'.")
        south, north, west, east = (float(v) for v in hits[0]["boundingbox"])
        _cache[key] = (west, east, south, north)
        _resolved[key] = {
            "name": hits[0].get("display_name", "")[:200],
            "type": hits[0].get("type") or hits[0].get("addresstype"),
            "bbox_km": [round((east - west) * 111), round((north - south) * 111)],
        }
        return _cache[key]
