"""
Overture Maps Places source adapter.

Why this source exists: OpenStreetMap is volunteer-mapped and thin for small Indian businesses
(audit 2026-11-08: Udaipur has 29 named cafes in OSM vs 242 in Overture; only 3.8 % of OSM
businesses there carry a phone vs 83 % in Overture). Overture Places merges Meta (Facebook pages),
Microsoft, Foursquare and other providers, and each place carries websites, socials, phones and
emails — exactly the signals needed to tell "has a website" from "social media only".

License: CDLA-Permissive-2.0 / Apache-2.0 depending on the upstream provider (no OSM data, no
share-alike). Attribution: "© Overture Maps Foundation" + provider notices.
Docs: https://docs.overturemaps.org/guides/places

How it works: a city name is turned into a bounding box with one Nominatim lookup, then DuckDB
reads only the matching rows of Overture's public GeoParquet release on S3 (≈ 20 s per city).
"""

import asyncio
from typing import Any, Optional
from urllib.parse import urlparse

import httpx
import structlog

from backend.app.config import get_settings
from backend.app.engines.discovery.base import (
    AdapterResult,
    BaseSourceAdapter,
    DiscoveredBusiness,
)

logger = structlog.get_logger(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "SiteBlitzLeadGenerator/0.2 (internal business research tool)"

# A city bounding box larger than this (in degrees, ≈ 110 km per degree) means the name matched a
# state or a whole district; scanning it would download gigabytes, so the job asks for a city.
MAX_BBOX_DEGREES = 1.5

# Category words used in the UI → fragments of Overture `basic_category` / `taxonomy` values.
CATEGORY_SYNONYMS: dict[str, list[str]] = {
    "cafe": ["cafe", "coffee"],
    "salon": ["salon", "beauty", "hair"],
    "hairdresser": ["hair", "salon"],
    "gym": ["gym", "fitness"],
    "dentist": ["dent"],
    "clinic": ["clinic", "medical", "doctor"],
    "lawyer": ["lawyer", "legal", "attorney"],
    "accountant": ["accountant", "accounting", "tax"],
    "estate_agent": ["real_estate"],
    "car_repair": ["auto_repair", "car_repair", "automotive"],
    "plumber": ["plumb"],
    "electrician": ["electric"],
    "hotel": ["hotel", "resort", "guest_house", "hostel"],
    "school": ["school", "education", "tutor", "coaching"],
}

SOCIAL_HOSTS = {
    "facebook.com": "facebook",
    "fb.com": "facebook",
    "instagram.com": "instagram",
    "linkedin.com": "linkedin",
    "tiktok.com": "tiktok",
    "youtube.com": "youtube",
    "x.com": "twitter",
    "twitter.com": "twitter",
    "wa.me": "whatsapp",
    "whatsapp.com": "whatsapp",
    "linktr.ee": "linktree",
}


def social_platform(url: Optional[str]) -> Optional[str]:
    """Return the platform name if the URL's host is a social network, else None.

    Matched on the parsed host (exact or subdomain), never by substring: "fedex.com" must not
    be mistaken for "x.com".
    """
    if not url:
        return None
    candidate = url if "://" in url else f"https://{url}"
    host = (urlparse(candidate).hostname or "").lower()
    for domain, platform in SOCIAL_HOSTS.items():
        if host == domain or host.endswith("." + domain):
            return platform
    return None


def category_patterns(category: Optional[str]) -> list[str]:
    """ILIKE patterns for a UI category word (empty list = all categories)."""
    if not category or not category.strip():
        return []
    key = category.strip().lower().replace(" ", "_")
    fragments = CATEGORY_SYNONYMS.get(key, [key])
    return [f"%{fragment}%" for fragment in fragments]


def build_query(release: str, n_patterns: int) -> str:
    """
    SQL for one bounding box. Every user-controlled value is a `?` parameter; only the
    release folder (from settings) and the number of placeholders are formatted in.
    """
    source = f"s3://overturemaps-us-west-2/release/{release}/theme=places/type=place/*"
    category_clause = ""
    if n_patterns:
        ors = " OR ".join(["(basic_category ILIKE ? OR taxonomy.primary ILIKE ?)"] * n_patterns)
        category_clause = f"AND ({ors})"
    return f"""
        SELECT id, names.primary AS name, confidence, operating_status, basic_category,
               taxonomy.primary AS taxonomy_primary, websites, socials, phones, emails,
               addresses, brand.names.primary AS brand_name, brand.wikidata AS brand_wikidata,
               (bbox.xmin + bbox.xmax) / 2 AS lon, (bbox.ymin + bbox.ymax) / 2 AS lat,
               list_transform(sources, lambda s: s.dataset) AS datasets
        FROM read_parquet('{source}', hive_partitioning = 1)
        WHERE bbox.xmin BETWEEN ? AND ? AND bbox.ymin BETWEEN ? AND ?
          AND names.primary IS NOT NULL
          AND coalesce(operating_status, '') <> 'permanently_closed'
          AND confidence >= ?
          {category_clause}
        ORDER BY confidence DESC
        LIMIT ?
    """


def row_to_business(row: dict[str, Any], fallback_city: Optional[str],
                    fallback_country: Optional[str]) -> DiscoveredBusiness:
    """Map one Overture row (as a dict) to the internal exchange format."""
    websites = [w for w in (row.get("websites") or []) if w]
    socials = [s for s in (row.get("socials") or []) if s]

    social_urls: dict[str, str] = {}
    own_website = None
    for url in websites + socials:
        platform = social_platform(url)
        if platform:
            social_urls.setdefault(platform, url)
        elif own_website is None and url in websites:
            own_website = url

    address = (row.get("addresses") or [None])[0] or {}
    category = row.get("basic_category") or row.get("taxonomy_primary")

    raw = {
        "overture_id": row.get("id"),
        "confidence": row.get("confidence"),
        "operating_status": row.get("operating_status"),
        "basic_category": row.get("basic_category"),
        "taxonomy_primary": row.get("taxonomy_primary"),
        "websites": websites,
        "socials": socials,
        "phones": list(row.get("phones") or []),
        "emails": list(row.get("emails") or []),
        "brand_name": row.get("brand_name"),
        "brand_wikidata": row.get("brand_wikidata"),
        "datasets": list(row.get("datasets") or []),
    }

    return DiscoveredBusiness(
        source_external_id=f"overture:{row.get('id')}",
        source_external_url=None,
        raw_data=raw,
        name=(row.get("name") or "").strip(),
        address_line_1=address.get("freeform"),
        city=address.get("locality") or fallback_city,
        state_province=address.get("region"),
        postal_code=address.get("postcode"),
        country_code=address.get("country") or fallback_country,
        latitude=row.get("lat"),
        longitude=row.get("lon"),
        categories=[category] if category else [],
        source_categories=[f"overture:{category}"] if category else [],
        website_url=own_website,
        phone=(row.get("phones") or [None])[0],
        email=(row.get("emails") or [None])[0],
        social_urls=social_urls,
    )


class OvertureAdapter(BaseSourceAdapter):
    """Overture Maps Places — bulk, open-licensed business places with contact + social links."""

    def __init__(self, rate_limit_rpm: int = 30):
        super().__init__(rate_limit_rpm=rate_limit_rpm)

    def get_source_metadata(self) -> dict:
        return {
            "name": "Overture Maps Places",
            "slug": "overture",
            "description": (
                "Open business places from Overture Maps (Meta, Microsoft, Foursquare and other "
                "providers) with websites, social profiles, phones and emails."
            ),
            "license_type": "OPEN_LICENSE",
            "license_url": "https://docs.overturemaps.org/attribution/",
            "license_notes": (
                "CDLA-Permissive-2.0 or Apache-2.0 per provider. Contacting businesses is still "
                "subject to each country's marketing rules."
            ),
            "attribution_required": True,
            "attribution_text": "© Overture Maps Foundation and its data providers",
            "allows_commercial_storage": True,
            "allows_contact_enrichment": True,
            "allows_marketing_use": True,
            "api_base_url": "s3://overturemaps-us-west-2/release/",
            "adapter_class": "backend.app.engines.discovery.overture.OvertureAdapter",
        }

    async def _city_bbox(self, city: str, country_code: Optional[str]) -> tuple[float, float, float, float]:
        """(west, east, south, north) of a city via one Nominatim lookup (1 request per job)."""
        params = {"city": city, "format": "jsonv2", "limit": 1}
        if country_code:
            params["countrycodes"] = country_code.lower()
        await self._rate_limit()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                NOMINATIM_URL, params=params, headers={"User-Agent": USER_AGENT}
            )
            response.raise_for_status()
            hits = response.json()
        if not hits:
            raise LookupError(f"City '{city}' was not found in country '{country_code or 'any'}'.")
        south, north, west, east = (float(v) for v in hits[0]["boundingbox"])
        return west, east, south, north

    def _run_query(self, sql: str, params: list) -> list[dict[str, Any]]:
        """Blocking DuckDB read of the public Parquet files (called in a worker thread)."""
        # Imported here so the API can start even where DuckDB is not installed yet.
        import duckdb

        con = duckdb.connect()
        try:
            con.execute("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
            cursor = con.execute(sql, params)
            columns = [d[0] for d in cursor.description]
            return [dict(zip(columns, values)) for values in cursor.fetchall()]
        finally:
            con.close()

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
        result = AdapterResult()
        settings = get_settings()
        min_confidence = float((query_params or {}).get("min_confidence", 0.0))

        try:
            if latitude is not None and longitude is not None and radius_km:
                # 1 degree latitude ≈ 111 km; longitude degrees shrink with latitude — a square
                # box slightly larger than the circle is fine for discovery.
                d = radius_km / 111.0
                west, east, south, north = longitude - d, longitude + d, latitude - d, latitude + d
            elif city and city.strip():
                west, east, south, north = await self._city_bbox(city.strip(), country_code)
            else:
                raise ValueError(
                    "Overture needs a city or coordinates + radius (a whole country is too large)."
                )

            if (east - west) > MAX_BBOX_DEGREES or (north - south) > MAX_BBOX_DEGREES:
                raise ValueError(
                    f"'{city}' matched an area of {east - west:.1f}° × {north - south:.1f}° "
                    "(a district or state). Enter a city name or use coordinates + radius."
                )

            patterns = category_patterns(category)
            sql = build_query(settings.OVERTURE_RELEASE, len(patterns))
            params: list = [west, east, south, north, min_confidence]
            for pattern in patterns:
                params += [pattern, pattern]
            params.append(int(max_results))

            logger.info("overture_discovery_start", city=city, category=category,
                        bbox=[west, east, south, north])
            rows = await asyncio.to_thread(self._run_query, sql, params)

            for row in rows:
                try:
                    business = row_to_business(row, city.strip() if city else None, country_code)
                    if business.name:
                        result.businesses.append(business)
                except Exception as exc:  # one bad row must not lose the whole job
                    result.errors.append(self._create_error(
                        "parse_error", f"Failed to parse Overture row: {exc}",
                        details={"id": row.get("id")},
                    ))
            result.total_available = len(rows)

        except LookupError as exc:
            result.errors.append(self._create_error("city_not_found", str(exc)))
        except ValueError as exc:
            result.errors.append(self._create_error("invalid_area", str(exc)))
        except httpx.HTTPError as exc:
            result.errors.append(self._create_error(
                "geocoder_error", f"City lookup failed: {exc}", is_retryable=True))
        except ImportError:
            result.errors.append(self._create_error(
                "missing_dependency", "DuckDB is not installed: pip install duckdb"))
        except Exception as exc:
            result.errors.append(self._create_error(
                "overture_error",
                f"Overture read failed: {exc}. If the release folder no longer exists, update "
                f"OVERTURE_RELEASE (current: {settings.OVERTURE_RELEASE}).",
                is_retryable=True,
            ))

        logger.info("overture_discovery_complete",
                    businesses_found=len(result.businesses), errors=len(result.errors))
        return result
