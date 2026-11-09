"""
Wikidata SPARQL source adapter.

Discovers commercial entities, enterprises, and businesses from Wikidata
using SPARQL queries against the Wikidata query service.

License: Creative Commons CC0 1.0 Universal (Public Domain Dedication)
Attribution: None required (CC0), but provenance is tracked
Endpoint: https://query.wikidata.org/sparql
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

WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"

# Common Wikidata QIDs for business types
WIKIDATA_BUSINESS_CLASSES = {
    "business": "wd:Q4830453",          # business enterprise
    "company": "wd:Q783794",            # company
    "restaurant": "wd:Q11707",          # restaurant
    "hotel": "wd:Q27686",               # hotel
    "software": "wd:Q7397",             # software company
    "agency": "wd:Q83995",              # marketing/advertising agency
    "startup": "wd:Q628867",            # startup company
    "retailer": "wd:Q126793",           # retail company
    "consulting": "wd:Q2092147",        # consulting firm
}

# Country code to Wikidata country entity QID mapping for common target markets
COUNTRY_QIDS = {
    "US": "wd:Q30",
    "GB": "wd:Q145",
    "UK": "wd:Q145",
    "DE": "wd:Q183",
    "FR": "wd:Q142",
    "CA": "wd:Q16",
    "AU": "wd:Q408",
    "JP": "wd:Q17",
    "SG": "wd:Q334",
    "NL": "wd:Q55",
    "SE": "wd:Q34",
    "CH": "wd:Q39",
    "ES": "wd:Q29",
    "IT": "wd:Q38",
    "AE": "wd:Q878",
    "IN": "wd:Q668",
}


def build_sparql_query(
    *,
    country_code: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    max_results: int = 100,
) -> str:
    """
    Construct a SPARQL query to retrieve businesses from Wikidata.
    """
    class_qid = WIKIDATA_BUSINESS_CLASSES.get(
        (category or "").lower(), "wd:Q4830453"
    )

    country_filter = ""
    if country_code:
        cc_upper = country_code.upper()
        if cc_upper in COUNTRY_QIDS:
            country_filter = f"?item wdt:P17 {COUNTRY_QIDS[cc_upper]} ."
        else:
            country_filter = f"""
            ?item wdt:P17 ?country .
            ?country wdt:P297 "{cc_upper}" .
            """

    city_filter = ""
    if city:
        city_filter = f"""
        ?item wdt:P159 ?hq .
        ?hq rdfs:label ?cityName .
        FILTER(LANG(?cityName) = "en" && REGEX(?cityName, "^{city}$", "i"))
        """

    query = f"""
    SELECT DISTINCT ?item ?itemLabel ?description ?website ?coord ?hqLabel ?countryCode ?employees ?inception WHERE {{
        ?item wdt:P31/wdt:P279* {class_qid} .
        {country_filter}
        {city_filter}
        OPTIONAL {{ ?item wdt:P856 ?website . }}
        OPTIONAL {{ ?item wdt:P625 ?coord . }}
        OPTIONAL {{ ?item wdt:P159 ?hq . }}
        OPTIONAL {{
            ?item wdt:P17 ?country .
            ?country wdt:P297 ?countryCode .
        }}
        OPTIONAL {{ ?item wdt:P1128 ?employees . }}
        OPTIONAL {{ ?item wdt:P571 ?inception . }}
        OPTIONAL {{
            ?item schema:description ?description .
            FILTER(LANG(?description) = "en")
        }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {min(max_results, 500)}
    """
    return query


class WikidataAdapter(BaseSourceAdapter):
    """
    Source adapter for querying structured business entities from Wikidata.
    """

    def __init__(
        self,
        rate_limit_rpm: int = 30,
        timeout_seconds: float = 45.0,
        user_agent: str = "SiteBlitzLeadIntelligence/1.0 (info@siteblitz.com)",
    ):
        super().__init__(rate_limit_rpm=rate_limit_rpm)
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def get_source_metadata(self) -> dict:
        """Metadata for registering Wikidata as a source."""
        return {
            "name": "Wikidata",
            "slug": "wikidata",
            "description": (
                "Free and open knowledge base acting as central storage for structured "
                "data across Wikipedia and Wikimedia projects."
            ),
            "license_type": "OPEN_LICENSE",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "license_notes": "CC0 1.0 Universal Public Domain Dedication. Unrestricted reuse.",
            "attribution_required": False,
            "attribution_text": "Wikidata contributors (CC0)",
            "allows_commercial_storage": True,
            "allows_contact_enrichment": True,
            "allows_marketing_use": True,
            "max_cache_duration_hours": None,
            "api_base_url": WIKIDATA_SPARQL_URL,
            "rate_limit_rpm": self._rate_limit_rpm,
            "adapter_class": "backend.app.engines.discovery.wikidata.WikidataAdapter",
            "status": "ACTIVE",
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
        max_results: int = 100,
        query_params: Optional[dict] = None,
    ) -> AdapterResult:
        """
        Query Wikidata for businesses matching the given criteria.
        """
        result = AdapterResult()
        await self._rate_limit()

        sparql = (query_params or {}).get("sparql")
        if not sparql:
            sparql = build_sparql_query(
                country_code=country_code,
                city=city,
                category=category,
                max_results=max_results,
            )

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/sparql-results+json",
        }

        logger.info(
            "wikidata_query_start",
            country=country_code,
            city=city,
            category=category,
            limit=max_results,
        )

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.get(
                    WIKIDATA_SPARQL_URL,
                    params={"query": sparql, "format": "json"},
                    headers=headers,
                )

                if response.status_code == 429:
                    result.errors.append(
                        self._create_error(
                            "rate_limit",
                            "Wikidata SPARQL rate limit exceeded",
                            is_retryable=True,
                        )
                    )
                    return result

                if response.status_code != 200:
                    result.errors.append(
                        self._create_error(
                            "api_error",
                            f"Wikidata returned HTTP {response.status_code}: {response.text[:200]}",
                            is_retryable=(response.status_code >= 500),
                        )
                    )
                    return result

                data = response.json()
                bindings = data.get("results", {}).get("bindings", [])

                for item in bindings:
                    parsed = self._parse_binding(item, default_country=country_code)
                    if parsed:
                        result.businesses.append(parsed)

        except httpx.TimeoutException:
            result.errors.append(
                self._create_error(
                    "timeout",
                    f"Wikidata query timed out after {self.timeout_seconds}s",
                    is_retryable=True,
                )
            )
        except Exception as e:
            logger.error("wikidata_query_exception", error=str(e))
            result.errors.append(
                self._create_error(
                    "unknown",
                    f"Wikidata query error: {str(e)}",
                    is_retryable=False,
                )
            )

        logger.info(
            "wikidata_query_complete",
            found=len(result.businesses),
            errors=len(result.errors),
        )
        return result

    def _parse_binding(
        self, binding: dict, default_country: Optional[str] = None
    ) -> Optional[DiscoveredBusiness]:
        """Convert a single SPARQL result binding into a DiscoveredBusiness."""
        item_uri = binding.get("item", {}).get("value", "")
        item_qid = item_uri.split("/")[-1] if "/" in item_uri else ""

        name = binding.get("itemLabel", {}).get("value")
        if not name or name.startswith("Q") and name[1:].isdigit():
            # Skip unlabelled entity IDs
            return None

        website = binding.get("website", {}).get("value")
        coord_val = binding.get("coord", {}).get("value")  # "Point(lon lat)"
        lat = None
        lon = None
        if coord_val and coord_val.startswith("Point("):
            coords_clean = coord_val.replace("Point(", "").replace(")", "").strip()
            parts = coords_clean.split()
            if len(parts) == 2:
                try:
                    lon = float(parts[0])
                    lat = float(parts[1])
                except ValueError:
                    pass

        country_code = binding.get("countryCode", {}).get("value") or default_country
        hq_city = binding.get("hqLabel", {}).get("value")
        description = binding.get("description", {}).get("value")

        return DiscoveredBusiness(
            source_external_id=f"wikidata:{item_qid}",
            source_external_url=item_uri,
            raw_data=binding,
            name=name,
            description=description,
            city=hq_city,
            country_code=country_code,
            latitude=lat,
            longitude=lon,
            website_url=website,
            categories=["company"],
            source_categories=["wikidata:Q4830453"],
        )
