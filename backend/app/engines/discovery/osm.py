"""
OpenStreetMap (Overpass API) source adapter.

Discovers businesses from OSM using the Overpass API with
ODbL license compliance. Uses regional queries with
configurable geographic scope.

License: Open Data Commons Open Database License (ODbL)
Attribution: © OpenStreetMap contributors
Docs: https://wiki.openstreetmap.org/wiki/Overpass_API
"""

import re
from typing import Optional

import httpx
import structlog

from backend.app.engines.discovery.categories import CATEGORY_TOKENS, name_words
from backend.app.engines.discovery.geocode import city_bbox

from backend.app.engines.discovery.base import (
    AdapterResult,
    BaseSourceAdapter,
    DiscoveredBusiness,
)

logger = structlog.get_logger(__name__)

# Overpass API endpoint
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

# overpass-api.de answers HTTP 406 to generic client User-Agents (verified 2026-11-08 with
# httpx's default "python-httpx/x.y"), so every request must identify the tool.
OVERPASS_USER_AGENT = "SiteBlitzLeadGenerator/0.2 (internal business research tool)"


def _ql_escape(value: str) -> str:
    """Escape user text for use inside a double-quoted Overpass QL string."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _ql_regex_escape(value: str) -> str:
    """Escape user text for use as a literal inside an Overpass QL (POSIX ERE) regex string."""
    return _ql_escape(re.sub(r"([.^$*+?()\[\]{}|\\])", r"\\\1", value))

# OSM amenity/shop tags that map to business categories
OSM_BUSINESS_TAGS = {
    # Amenity tags
    "amenity": [
        "restaurant", "cafe", "bar", "pub", "fast_food", "bakery",
        "ice_cream", "nightclub", "cinema", "theatre",
        "dentist", "doctors", "clinic", "hospital", "pharmacy", "veterinary",
        "bank", "atm", "bureau_de_change",
        "car_rental", "car_wash", "fuel",
        "school", "university", "college", "driving_school",
        "gym", "spa",
        "studio", "events_venue",
        "place_of_worship",
    ],
    # Shop tags
    "shop": [
        "supermarket", "convenience", "clothes", "shoes", "jewelry",
        "electronics", "mobile_phone", "computer",
        "furniture", "hardware", "garden_centre",
        "beauty", "hairdresser", "optician",
        "bakery", "butcher", "greengrocer", "deli",
        "florist", "gift", "books", "stationery",
        "toys", "pet", "sports",
        "car", "car_parts", "car_repair", "tyres",
        "laundry", "dry_cleaning",
        "travel_agency", "copyshop",
    ],
    # Tourism tags
    "tourism": [
        "hotel", "motel", "hostel", "guest_house",
        "apartment", "camp_site", "resort",
    ],
    # Office tags
    "office": [
        "lawyer", "accountant", "insurance", "estate_agent",
        "architect", "company", "it", "consulting", "marketing",
        "financial", "association",
    ],
    # Craft tags
    "craft": [
        "plumber", "electrician", "painter", "carpenter",
        "photographer", "brewery", "winery", "roofer",
        "hvac", "locksmith",
    ],
}


def _build_overpass_query(
    *,
    country_code: Optional[str] = None,
    city: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = None,
    category: Optional[str] = None,
    max_results: int = 500,
    bbox: Optional[tuple[float, float, float, float]] = None,
) -> str:
    """
    Build an Overpass QL query for business discovery.
    `bbox` = (west, east, south, north) of a geocoded city — preferred over a named area.

    Supports either named area (city/country) or coordinate+radius search.
    """
    # Determine search area.
    # City areas in OSM never carry the ISO3166-1 tag (only countries do), so a city is
    # found as an administrative boundary *inside* the country and converted to an area.
    area_setup = ""
    if bbox is not None:
        west, east, south, north = (float(v) for v in bbox)
        area_filter = f"({south},{west},{north},{east})"
        latitude = south  # marks a geometry filter (not a named area) for the query builders below
    elif latitude is not None and longitude is not None and radius_km:
        radius_m = int(radius_km * 1000)
        area_filter = f"(around:{radius_m},{float(latitude)},{float(longitude)})"
    elif city and country_code:
        cc = _ql_escape(country_code.strip().upper())
        city_re = _ql_regex_escape(city.strip())
        area_filter = "(area.searchArea)"
        area_setup = (
            f'area["ISO3166-1"="{cc}"]["admin_level"="2"]->.country;\n'
            f'rel(area.country)["boundary"="administrative"]'
            f'[~"^name(:en)?$"~"^{city_re}$",i];\n'
            f"map_to_area->.searchArea;"
        )
    elif city:
        area_filter = "(area.searchArea)"
        area_setup = (
            f'area["name"="{_ql_escape(city.strip())}"]["boundary"="administrative"]->.searchArea;'
        )
    elif country_code:
        area_filter = "(area.searchArea)"
        area_setup = (
            f'area["ISO3166-1"="{_ql_escape(country_code.strip().upper())}"]'
            f'["admin_level"="2"]->.searchArea;'
        )
    else:
        raise ValueError("Must provide either coordinates+radius or city/country")

    # Determine tag filters
    if category:
        # Search for specific category
        tag_queries = _build_category_queries(category, area_filter, latitude is not None)
    else:
        # Search for all business types
        tag_queries = _build_all_business_queries(area_filter, latitude is not None)

    # Build full query
    timeout = 90 if not category else 60
    query = f"""
[out:json][timeout:{timeout}];
{area_setup}
(
{tag_queries}
);
out center {int(max_results)};
"""
    return query.strip()


# OSM keys whose values name a kind of business (healthcare=dentist, leisure=fitness_centre …).
CATEGORY_KEYS = ["amenity", "shop", "office", "craft", "healthcare", "leisure", "tourism"]


def _build_category_queries(
    category: str, area_filter: str, is_coord_search: bool
) -> str:
    """
    Overpass queries for one category: every OSM key whose value is one of the category's
    word-parts, plus a name match (e.g. "Smile Dental Care" tagged only as a generic clinic).
    Both are needed for volume — see categories.py.
    """
    where = area_filter if is_coord_search else "(area.searchArea)"
    clean = category.lower().strip().replace(" ", "_")
    tokens = sorted({clean, *CATEGORY_TOKENS.get(clean, [])})
    values = "|".join(_ql_regex_escape(t) for t in tokens)
    queries = [f'  nwr["{key}"~"^({values})$"]{where};' for key in CATEGORY_KEYS]
    words = "|".join(_ql_regex_escape(w) for w in name_words(category))
    if words:
        # Name matches only on elements that are some kind of business (not "Dental College Road").
        keys = "|".join(CATEGORY_KEYS)
        queries.append(f'  nwr["name"~"({words})",i][~"^({keys})$"~"."]{where};')
    return "\n".join(queries)


def _build_all_business_queries(area_filter: str, is_coord_search: bool) -> str:
    """Build Overpass queries for all business types."""
    queries = []
    # Only query main business tags to keep response size manageable
    main_tags = ["amenity", "shop", "tourism", "office"]

    for tag_key in main_tags:
        if is_coord_search:
            queries.append(f'  nwr["{tag_key}"]["name"]{area_filter};')
        else:
            queries.append(f'  nwr["{tag_key}"]["name"](area.searchArea);')

    return "\n".join(queries)


class OSMAdapter(BaseSourceAdapter):
    """
    OpenStreetMap source adapter using the Overpass API.

    License: ODbL — data is freely reusable with attribution.
    Rate limit: Conservative to respect public Overpass endpoint.
    """

    def __init__(self, rate_limit_rpm: int = 10):
        super().__init__(rate_limit_rpm=rate_limit_rpm)

    def get_source_metadata(self) -> dict:
        return {
            "name": "OpenStreetMap",
            "slug": "openstreetmap",
            "description": (
                "Business data from OpenStreetMap via Overpass API. "
                "Data is under the Open Data Commons Open Database License (ODbL)."
            ),
            "license_type": "OPEN_LICENSE",
            "license_url": "https://www.openstreetmap.org/copyright",
            "attribution_required": True,
            "attribution_text": "© OpenStreetMap contributors",
            "allows_commercial_storage": True,
            "allows_contact_enrichment": True,
            "allows_marketing_use": False,  # ODbL allows storage, not direct marketing
            "api_base_url": OVERPASS_API_URL,
            "adapter_class": "backend.app.engines.discovery.osm.OSMAdapter",
        }

    async def discover(
        self,
        *,
        country_code: Optional[str] = None,
        region: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius_km: Optional[float] = None,
        max_results: int = 500,
        cursor: Optional[str] = None,
        query_params: Optional[dict] = None,
    ) -> AdapterResult:
        """Discover businesses from OpenStreetMap via Overpass API."""
        result = AdapterResult()

        try:
            # A city is searched by its geocoded bounding box (same area as Overture, and fast);
            # the named-area query is only the fallback when the geocoder is unreachable.
            bbox = None
            if city and city.strip() and not (latitude is not None and longitude is not None and radius_km):
                try:
                    bbox = await city_bbox(city, country_code)
                except LookupError:
                    raise
                except Exception as exc:
                    logger.warning("osm_geocode_failed_fallback_to_area", city=city, error=str(exc))

            # Build query
            query = _build_overpass_query(
                bbox=bbox,
                country_code=country_code,
                city=city,
                latitude=latitude,
                longitude=longitude,
                radius_km=radius_km,
                category=category,
                max_results=max_results,
            )

            logger.info(
                "osm_discovery_start",
                country=country_code,
                city=city,
                category=category,
                radius_km=radius_km,
            )

            # Rate limit
            await self._rate_limit()

            # Execute query
            # The public Overpass server answers 429/502/503/504 when busy; those are retried
            # (3 tries) after waiting one rate-limit interval per try (OSM_OVERPASS_RPM → 6 s).
            async with httpx.AsyncClient(timeout=120.0) as client:
                for attempt in range(3):
                    response = await client.post(
                        OVERPASS_API_URL,
                        data={"data": query},
                        headers={
                            "Accept": "application/json",
                            "User-Agent": OVERPASS_USER_AGENT,
                        },
                    )
                    if response.status_code not in (429, 502, 503, 504) or attempt == 2:
                        break
                    logger.info("overpass_busy_retry", status=response.status_code, attempt=attempt + 1)
                    await self._async_sleep(self._min_interval * (attempt + 1))
                response.raise_for_status()
                data = response.json()

            # Parse elements
            elements = data.get("elements", [])
            logger.info("osm_elements_received", count=len(elements))

            for element in elements:
                try:
                    business = self._parse_element(element, country_code)
                    if business and business.name:
                        result.businesses.append(business)
                except Exception as e:
                    result.errors.append(
                        self._create_error(
                            "parse_error",
                            f"Failed to parse OSM element: {e}",
                            details={"element_id": element.get("id")},
                            is_retryable=False,
                        )
                    )

            result.total_available = len(elements)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                result.errors.append(
                    self._create_error(
                        "rate_limit",
                        "Overpass API rate limit exceeded",
                        is_retryable=True,
                    )
                )
            else:
                result.errors.append(
                    self._create_error(
                        "http_error",
                        f"Overpass API error: {e.response.status_code}",
                        details={"status": e.response.status_code},
                        is_retryable=e.response.status_code >= 500,
                    )
                )
        except LookupError as e:
            result.errors.append(self._create_error("city_not_found", str(e)))
        except httpx.TimeoutException:
            result.errors.append(
                self._create_error(
                    "timeout",
                    "Overpass API request timed out",
                    is_retryable=True,
                )
            )
        except Exception as e:
            result.errors.append(
                self._create_error(
                    "unknown",
                    f"Unexpected error: {str(e)}",
                    is_retryable=False,
                )
            )

        logger.info(
            "osm_discovery_complete",
            businesses_found=len(result.businesses),
            errors=len(result.errors),
        )

        return result

    def _parse_element(
        self, element: dict, default_country: Optional[str] = None
    ) -> Optional[DiscoveredBusiness]:
        """Parse a single OSM element into a DiscoveredBusiness."""
        tags = element.get("tags", {})
        name = tags.get("name")

        if not name:
            return None

        # Get coordinates
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        # Determine categories from tags
        categories = []
        source_categories = []
        for tag_key in ["amenity", "shop", "tourism", "office", "craft", "healthcare", "leisure"]:
            if tag_key in tags:
                value = tags[tag_key]
                source_categories.append(f"{tag_key}:{value}")
                categories.append(value)

        # Extract address
        address = tags.get("addr:street", "")
        house_number = tags.get("addr:housenumber", "")
        if house_number and address:
            address = f"{house_number} {address}"

        # Extract social URLs
        social_urls = {}
        for key in ["facebook", "instagram", "twitter", "linkedin"]:
            if key in tags:
                social_urls[key] = tags[key]
            elif f"contact:{key}" in tags:
                social_urls[key] = tags[f"contact:{key}"]

        # Determine website (filter out social profiles)
        website = tags.get("website") or tags.get("contact:website")

        # Get country code
        country = tags.get("addr:country") or default_country

        return DiscoveredBusiness(
            source_external_id=f"osm:{element.get('type', 'node')}:{element.get('id')}",
            source_external_url=(
                f"https://www.openstreetmap.org/{element.get('type', 'node')}/{element.get('id')}"
            ),
            raw_data=element,
            name=name,
            description=tags.get("description"),
            address_line_1=address or None,
            city=tags.get("addr:city"),
            state_province=tags.get("addr:state"),
            postal_code=tags.get("addr:postcode"),
            country_code=country,
            latitude=lat,
            longitude=lon,
            categories=categories,
            source_categories=source_categories,
            website_url=website,
            phone=tags.get("phone") or tags.get("contact:phone"),
            email=tags.get("email") or tags.get("contact:email"),
            social_urls=social_urls,
            opening_hours=tags.get("opening_hours"),
        )
