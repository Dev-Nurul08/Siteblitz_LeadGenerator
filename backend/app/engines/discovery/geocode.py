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
import re
import time
import unicodedata
from typing import Optional

import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "SiteBlitzLeadGenerator/0.2 (internal business research tool)"

# Largest box (degrees per side) any source is asked to search. Overture and OSM queries over a
# larger box time out or return a whole province.
MAX_BBOX_DEGREES = 1.5

# Nominatim address types that are a settlement. A hit of another type (a business district, a
# landmark, a state) is not used when a settlement hit exists.
# Why (city test 2026-11-08): "Beijing" with state "Beijing" resolved to 北京金融街 (a 1 × 2 km
# commercial landuse) and the search returned 0 businesses.
SETTLEMENT_TYPES = {"city", "town", "village", "municipality"}

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


# Among hits that carry the requested name, a city beats a village of the same name.
# Why: "Nanded" (Maharashtra) resolved to a 1 km village in Chandrapur district, not Nanded city.
_SETTLEMENT_ORDER = {"city": 0, "municipality": 1, "town": 2, "village": 3}


def _kind(hit: dict) -> Optional[str]:
    return hit.get("addresstype") or hit.get("type")


def _is_settlement(hit: dict) -> bool:
    return _kind(hit) in SETTLEMENT_TYPES


def _is_area(hit: dict) -> bool:
    """A place or an administrative area (suburb, district, state ...), not a building or a landmark."""
    return hit.get("category") in ("place", "boundary")


def _norm(text: str) -> str:
    """Case-, accent- and punctuation-free form: "Bogotá" == "bogota", "Pimpri-Chinchwad" == "pimpri chinchwad"."""
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[\W_]+", " ", text).strip()


def _names(hit: dict) -> set[str]:
    """Every name Nominatim knows for the hit (local, English, old, alternative) plus its display name."""
    names = {_norm(hit.get("display_name", "").split(",")[0])}
    for value in (hit.get("namedetails") or {}).values():
        names.update(_norm(v) for v in str(value).split(";"))
    return names


def _same_name(hit: dict, city: str) -> bool:
    wanted = _norm(city)
    names = _names(hit)
    return wanted in names or (wanted.endswith(" city") and wanted[:-5] in names)


def _pick(hits: list[dict], city: str) -> Optional[dict]:
    """The largest settlement kind that carries the requested name; Nominatim's order breaks ties."""
    named = [h for h in hits if _is_settlement(h) and _same_name(h, city)]
    return min(named, key=lambda h: _SETTLEMENT_ORDER[_kind(h)]) if named else None


def _trim(west: float, east: float, south: float, north: float,
          lat: float, lon: float) -> tuple[float, float, float, float]:
    """The part of the box inside a MAX_BBOX_DEGREES square centred on the city's point."""
    half = MAX_BBOX_DEGREES / 2
    return max(west, lon - half), min(east, lon + half), max(south, lat - half), min(north, lat + half)


async def _search(params: dict) -> list[dict]:
    """One Nominatim request, at least 1 s after the previous one (caller holds _lock)."""
    global _last_call
    wait = 1.0 - (time.monotonic() - _last_call)
    if wait > 0:
        await asyncio.sleep(wait)
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(NOMINATIM_URL, params=params, headers={"User-Agent": USER_AGENT})
    _last_call = time.monotonic()
    response.raise_for_status()
    return response.json()


async def city_bbox(city: str, country_code: Optional[str],
                    state: Optional[str] = None) -> tuple[float, float, float, float]:
    """(west, east, south, north). `state` disambiguates same-named cities. LookupError if unknown.

    A city whose own boundary is larger than MAX_BBOX_DEGREES (Beijing, Shenzhen, Chongqing are
    whole municipalities) is trimmed to that square around the city's point, so the search returns
    the city centre instead of nothing. A state or district hit is never trimmed - the sources
    reject it, because a box around a state's centre would be a random area.
    """
    key = _key(city, country_code, state)
    if key in _cache:
        return _cache[key]
    async with _lock:
        if key in _cache:
            return _cache[key]
        params = {"city": city.strip(), "format": "jsonv2", "limit": 5, "namedetails": 1}
        if country_code:
            params["countrycodes"] = country_code.strip().lower()
        if state and state.strip():
            params["state"] = state.strip()
        hits = await _search(params)
        hit = _pick(hits, city)
        if hit is None and "state" in params:
            # With the state, Nominatim returned a landmark, a suburb or other cities of that state
            # ("Tokyo" + state "Tokyo" gave Hachioji); the city name alone is better.
            # If the name alone finds nothing, the state's other cities are not used.
            params.pop("state")
            hits = await _search(params)
            hit = _pick(hits, city)
        if hit is None and not hits:
            # The structured "city" search knows only places tagged as settlements. Some cities are
            # mapped only as their district ("Thrissur", Kerala: no city object, district 104 x 68 km),
            # which free text finds. Only an area or settlement is used from it, never a landmark.
            free = {k: v for k, v in params.items() if k != "city"}
            free["q"] = city.strip()
            hits = await _search(free)
            hit = _pick(hits, city)
        if hit is None:
            if not hits:
                raise LookupError(f"City '{city}' was not found in country '{country_code or 'any'}'.")
            # No settlement carries the name: the first settlement, else the first area (a suburb is
            # searched as is; a state or province is rejected by the sources' size limit, never
            # trimmed). A building or landmark alone is not a place to search: "Hubli-Dharwad"
            # matched only the municipal offices (a 0 km box).
            hit = next((h for h in hits if _is_settlement(h)), None) or next((h for h in hits if _is_area(h)), None)
            if hit is None:
                raise LookupError(
                    f"City '{city}' was not found in country '{country_code or 'any'}' "
                    f"(closest match: {hits[0].get('display_name', '')[:80]})."
                )
        south, north, west, east = (float(v) for v in hit["boundingbox"])
        full_km = [round((east - west) * 111), round((north - south) * 111)]
        trimmed = False
        if _is_settlement(hit) and ((east - west) > MAX_BBOX_DEGREES or (north - south) > MAX_BBOX_DEGREES):
            west, east, south, north = _trim(west, east, south, north, float(hit["lat"]), float(hit["lon"]))
            trimmed = True
        _cache[key] = (west, east, south, north)
        _resolved[key] = {
            "name": hit.get("display_name", "")[:200],
            "type": hit.get("addresstype") or hit.get("type"),
            "bbox_km": [round((east - west) * 111), round((north - south) * 111)],
            **({"trimmed_from_km": full_km} if trimmed else {}),
        }
        return _cache[key]
