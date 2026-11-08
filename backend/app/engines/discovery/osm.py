"""
OpenStreetMap (Overpass API) source adapter.

Discovers businesses from OSM using the Overpass API with
ODbL license compliance. Uses coordinate-based radius queries
with built-in city geocoding for reliable global coverage.

License: Open Data Commons Open Database License (ODbL)
Attribution: © OpenStreetMap contributors
Docs: https://wiki.openstreetmap.org/wiki/Overpass_API
"""

import re
from typing import Optional

import httpx
import structlog

from backend.app.engines.discovery.base import (
    AdapterResult,
    BaseSourceAdapter,
    DiscoveredBusiness,
)

logger = structlog.get_logger(__name__)

# Multiple Overpass endpoints for reliability
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# Nominatim for city → coordinate geocoding
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

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

# Well-known city center coordinates for fast lookup (no geocoding needed)
CITY_COORDINATES = {
    # India
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "pune": (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462),
    "surat": (21.1702, 72.8311),
    "kochi": (9.9312, 76.2673),
    "chandigarh": (30.7333, 76.7794),
    "indore": (22.7196, 75.8577),
    "nagpur": (21.1458, 79.0882),
    "bhopal": (23.2599, 77.4126),
    "patna": (25.6093, 85.1376),
    "goa": (15.2993, 74.1240),
    # USA
    "new york": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "chicago": (41.8781, -87.6298),
    "houston": (29.7604, -95.3698),
    "san francisco": (37.7749, -122.4194),
    "miami": (25.7617, -80.1918),
    "seattle": (47.6062, -122.3321),
    "boston": (42.3601, -71.0589),
    "dallas": (32.7767, -96.7970),
    "austin": (30.2672, -97.7431),
    # UK
    "london": (51.5074, -0.1278),
    "manchester": (53.4808, -2.2426),
    "birmingham": (52.4862, -1.8904),
    "leeds": (53.8008, -1.5491),
    "edinburgh": (55.9533, -3.1883),
    "glasgow": (55.8642, -4.2518),
    "bristol": (51.4545, -2.5879),
    # Europe
    "paris": (48.8566, 2.3522),
    "berlin": (52.5200, 13.4050),
    "amsterdam": (52.3676, 4.9041),
    "barcelona": (41.3874, 2.1686),
    "madrid": (40.4168, -3.7038),
    "rome": (41.9028, 12.4964),
    "milan": (45.4642, 9.1900),
    "lisbon": (38.7223, -9.1393),
    "vienna": (48.2082, 16.3738),
    "zurich": (47.3769, 8.5417),
    "stockholm": (59.3293, 18.0686),
    "dublin": (53.3498, -6.2603),
    "prague": (50.0755, 14.4378),
    "warsaw": (52.2297, 21.0122),
    "brussels": (50.8503, 4.3517),
    "copenhagen": (55.6761, 12.5683),
    # Asia-Pacific
    "tokyo": (35.6762, 139.6503),
    "singapore": (1.3521, 103.8198),
    "dubai": (25.2048, 55.2708),
    "abu dhabi": (24.4539, 54.3773),
    "hong kong": (22.3193, 114.1694),
    "shanghai": (31.2304, 121.4737),
    "beijing": (39.9042, 116.4074),
    "seoul": (37.5665, 126.9780),
    "bangkok": (13.7563, 100.5018),
    "kuala lumpur": (3.1390, 101.6869),
    "jakarta": (- 6.2088, 106.8456),
    "sydney": (-33.8688, 151.2093),
    "melbourne": (-37.8136, 144.9631),
    "auckland": (-36.8485, 174.7633),
    # Middle East / Africa
    "riyadh": (24.7136, 46.6753),
    "doha": (25.2854, 51.5310),
    "cairo": (30.0444, 31.2357),
    "cape town": (-33.9249, 18.4241),
    "nairobi": (-1.2921, 36.8219),
    "lagos": (6.5244, 3.3792),
    # South America
    "sao paulo": (-23.5505, -46.6333),
    "rio de janeiro": (-22.9068, -43.1729),
    "buenos aires": (-34.6037, -58.3816),
    "bogota": (4.7110, -74.0721),
    "lima": (-12.0464, -77.0428),
    "mexico city": (19.4326, -99.1332),
    # Canada
    "toronto": (43.6532, -79.3832),
    "vancouver": (49.2827, -123.1207),
    "montreal": (45.5017, -73.5673),
}


async def _geocode_city(city: str, country_code: str = None) -> tuple[float, float]:
    """
    Geocode a city name to (latitude, longitude) coordinates.
    Uses built-in lookup first, then Nominatim as fallback.
    """
    # 1. Fast built-in lookup
    key = city.lower().strip()
    if key in CITY_COORDINATES:
        return CITY_COORDINATES[key]

    # 2. Nominatim geocoding fallback
    params = {"q": city, "format": "json", "limit": 1}
    if country_code:
        params["countrycodes"] = country_code.lower()

    headers = {
        "User-Agent": "SiteBlitz-LeadIntelligence/1.0 (contact@siteblitz.io)"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(NOMINATIM_URL, params=params, headers=headers)
            if resp.status_code == 200:
                results = resp.json()
                if results:
                    lat = float(results[0]["lat"])
                    lon = float(results[0]["lon"])
                    logger.info("geocoded_city", city=city, lat=lat, lon=lon)
                    return (lat, lon)
    except Exception as e:
        logger.warning("geocode_failed", city=city, error=str(e))

    raise ValueError(
        f"Could not geocode city '{city}'. "
        f"Please provide latitude/longitude coordinates directly."
    )


def _build_overpass_query(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = 5.0,
    category: Optional[str] = None,
    max_results: int = 500,
    city: Optional[str] = None,
    country_code: Optional[str] = None,
) -> str:
    """
    Build an Overpass QL query using coordinate + radius or city/country area search.
    """
    area_setup = ""
    if latitude is not None and longitude is not None:
        radius_m = int((radius_km or 5.0) * 1000)
        area_filter = f"(around:{radius_m},{float(latitude)},{float(longitude)})"
    elif city and country_code:
        cc = _ql_escape(country_code.strip().upper())
        city_re = _ql_regex_escape(city.strip())
        area_filter = "(area.searchArea)"
        area_setup = (
            f'area["ISO3166-1"="{cc}"]["admin_level"="2"]->.country;\n'
            f'rel(area.country)["boundary"="administrative"]'
            f'[~"^name(:en)?$"~"^{city_re}$",i];\n'
            f"map_to_area->.searchArea;\n"
        )
    elif city:
        area_filter = "(area.searchArea)"
        area_setup = (
            f'area["name"="{_ql_escape(city.strip())}"]["boundary"="administrative"]->.searchArea;\n'
        )
    elif country_code:
        area_filter = "(area.searchArea)"
        area_setup = (
            f'area["ISO3166-1"="{_ql_escape(country_code.strip().upper())}"]'
            f'["admin_level"="2"]->.searchArea;\n'
        )
    else:
        raise TypeError("Must provide either coordinates+radius or city/country")

    if category:
        tag_queries = _build_category_queries(category, area_filter)
    else:
        tag_queries = _build_all_business_queries(area_filter)

    timeout = min(60, max(25, max_results // 10))

    query = f"""[out:json][timeout:{timeout}];
{area_setup}(
{tag_queries}
);
out center {int(max_results)};"""
    return query.strip()


def _build_category_queries(category: str, area_filter: str) -> str:
    """Build Overpass queries for a specific category."""
    clean = category.lower().strip().replace(" ", "_")
    queries = []

    for tag_key, tag_values in OSM_BUSINESS_TAGS.items():
        if clean in tag_values:
            queries.append(f'  nwr["{tag_key}"="{clean}"]{area_filter};')

    if not queries:
        name_re = _ql_regex_escape(category)
        queries.append(f'  nwr["name"~"{name_re}",i]{area_filter};')

    return "\n".join(queries)


def _build_all_business_queries(area_filter: str) -> str:
    """Build Overpass queries for all business types."""
    main_tags = ["amenity", "shop", "tourism", "office"]
    queries = [f'  nwr["{tag}"]["name"]{area_filter};' for tag in main_tags]
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
            "api_base_url": OVERPASS_ENDPOINTS[0],
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
            # --- Resolve coordinates ---
            lat = latitude
            lon = longitude
            radius = radius_km or 5.0  # Default 5km radius

            if lat is None or lon is None:
                if city:
                    lat, lon = await _geocode_city(city, country_code)
                    if not radius_km:
                        radius = 5.0  # 5km city center radius
                else:
                    result.errors.append(
                        self._create_error(
                            "missing_location",
                            "Please provide a city name or latitude/longitude coordinates.",
                            is_retryable=False,
                        )
                    )
                    return result

            # --- Build query ---
            query = _build_overpass_query(
                latitude=lat,
                longitude=lon,
                radius_km=radius,
                category=category,
                max_results=max_results,
            )

            logger.info(
                "osm_discovery_start",
                country=country_code,
                city=city,
                category=category,
                lat=lat,
                lon=lon,
                radius_km=radius,
                max_results=max_results,
            )

            # Rate limit
            await self._rate_limit()

            # --- Execute query across endpoints with fallback ---
            data = None
            last_err = None
            headers = {
                "User-Agent": OVERPASS_USER_AGENT,
                "Accept": "application/json",
            }

            async with httpx.AsyncClient(timeout=55.0) as client:
                for ep in OVERPASS_ENDPOINTS:
                    try:
                        logger.info("osm_trying_endpoint", endpoint=ep)
                        response = await client.post(
                            ep,
                            data={"data": query},
                            headers=headers,
                        )
                        if response.status_code == 200:
                            data = response.json()
                            logger.info("osm_endpoint_success", endpoint=ep)
                            break
                        else:
                            last_err = f"HTTP {response.status_code} from {ep}"
                            logger.warning("osm_endpoint_failed", endpoint=ep, status=response.status_code)
                    except Exception as exc:
                        last_err = str(exc)
                        logger.warning("osm_endpoint_error", endpoint=ep, error=last_err)
                        continue

            if data is None:
                result.errors.append(
                    self._create_error(
                        "all_endpoints_failed",
                        f"All Overpass API endpoints failed: {last_err}",
                        is_retryable=True,
                    )
                )
                return result

            # --- Parse elements ---
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

        except ValueError as e:
            result.errors.append(
                self._create_error(
                    "geocode_error",
                    str(e),
                    is_retryable=False,
                )
            )
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
        for tag_key in ["amenity", "shop", "tourism", "office", "craft"]:
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

        # Determine phone: check comprehensive tags
        phone = (
            tags.get("phone")
            or tags.get("contact:phone")
            or tags.get("contact:mobile")
            or tags.get("mobile")
            or tags.get("whatsapp")
            or tags.get("contact:whatsapp")
            or tags.get("telephone")
            or tags.get("contact:telephone")
            or tags.get("tel")
        )

        # Determine email: check comprehensive tags
        email = (
            tags.get("email")
            or tags.get("contact:email")
            or tags.get("contact:mail")
            or tags.get("mail")
        )

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
            phone=phone,
            email=email,
            social_urls=social_urls,
            opening_hours=tags.get("opening_hours"),
        )
