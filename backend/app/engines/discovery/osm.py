"""
OpenStreetMap (Overpass API) source adapter.

Discovers businesses from OSM using the Overpass API with
ODbL license compliance. Uses regional queries with
configurable geographic scope.

License: Open Data Commons Open Database License (ODbL)
Attribution: © OpenStreetMap contributors
Docs: https://wiki.openstreetmap.org/wiki/Overpass_API
"""

from typing import Optional

import httpx
import structlog

from backend.app.engines.discovery.base import (
    AdapterResult,
    BaseSourceAdapter,
    DiscoveredBusiness,
)

logger = structlog.get_logger(__name__)

# Overpass API endpoint
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

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
) -> str:
    """
    Build an Overpass QL query for business discovery.

    Supports either named area (city/country) or coordinate+radius search.
    """
    # Determine search area
    if latitude is not None and longitude is not None and radius_km:
        radius_m = int(radius_km * 1000)
        area_filter = f"(around:{radius_m},{latitude},{longitude})"
    elif city and country_code:
        area_filter = f'(area["name"="{city}"]["ISO3166-1"="{country_code}"]->.searchArea)'
    elif city:
        area_filter = f'(area["name"="{city}"]->.searchArea)'
    elif country_code:
        area_filter = f'(area["ISO3166-1"="{country_code}"]->.searchArea)'
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
{'' if latitude is not None else area_filter.replace('(', '').replace(')', '') + ';'}
(
{tag_queries}
);
out center {max_results};
"""
    return query.strip()


def _build_category_queries(
    category: str, area_filter: str, is_coord_search: bool
) -> str:
    """Build Overpass queries for a specific category."""
    clean = category.lower().strip().replace(" ", "_")
    queries = []

    for tag_key, tag_values in OSM_BUSINESS_TAGS.items():
        if clean in tag_values:
            if is_coord_search:
                queries.append(
                    f'  nwr["{tag_key}"="{clean}"]{area_filter};'
                )
            else:
                queries.append(
                    f'  nwr["{tag_key}"="{clean}"](area.searchArea);'
                )

    if not queries:
        # Fallback: search as name
        if is_coord_search:
            queries.append(
                f'  nwr["name"~"{category}",i]{area_filter};'
            )
        else:
            queries.append(
                f'  nwr["name"~"{category}",i](area.searchArea);'
            )

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
            # Build query
            query = _build_overpass_query(
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
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    OVERPASS_API_URL,
                    data={"data": query},
                    headers={"Accept": "application/json"},
                )
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
