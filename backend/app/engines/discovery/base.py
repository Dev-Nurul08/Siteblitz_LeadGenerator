"""
Abstract base class for all source adapters.

Every data source (OSM, Wikidata, Companies House, CSV, etc.)
must implement this interface. The adapter contract ensures:
- Rate limiting is respected
- Source records are immutable after creation
- Attribution is preserved
- Errors are captured, not silently swallowed
"""

import abc
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class DiscoveredBusiness:
    """
    Normalized business record produced by a source adapter.

    This is the internal exchange format — adapters convert their
    source-specific data into this structure. Fields that cannot be
    determined from the source should remain None (never invented).
    """

    # Source identity
    source_external_id: str
    source_external_url: Optional[str] = None
    raw_data: dict = field(default_factory=dict)

    # Business identity
    name: str = ""
    description: Optional[str] = None

    # Location
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Category
    categories: list[str] = field(default_factory=list)
    source_categories: list[str] = field(default_factory=list)

    # Contact (business-level only)
    website_url: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    social_urls: dict = field(default_factory=dict)

    # Metadata
    opening_hours: Optional[str] = None
    employee_count: Optional[str] = None
    year_founded: Optional[int] = None


@dataclass
class AdapterResult:
    """Result of a single adapter fetch operation."""

    businesses: list[DiscoveredBusiness] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    has_more: bool = False
    next_cursor: Optional[str] = None
    total_available: Optional[int] = None


class BaseSourceAdapter(abc.ABC):
    """
    Abstract base class for all source adapters.

    Subclasses must implement:
    - discover(): Main discovery method, returns results
    - get_source_metadata(): Returns source configuration
    """

    def __init__(self, rate_limit_rpm: int = 30):
        self._rate_limit_rpm = rate_limit_rpm
        self._min_interval = 60.0 / rate_limit_rpm
        self._last_request_time: float = 0.0
        self._request_count: int = 0

    @abc.abstractmethod
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
        """
        Discover businesses from this source.

        Args:
            country_code: ISO country code (e.g., 'US', 'GB')
            region: State/province/region name
            city: City name
            category: Business category filter
            latitude: Center latitude for radius search
            longitude: Center longitude for radius search
            radius_km: Search radius in kilometers
            max_results: Maximum number of results to return
            cursor: Pagination cursor for resuming
            query_params: Source-specific additional parameters

        Returns:
            AdapterResult with discovered businesses and metadata
        """
        ...

    @abc.abstractmethod
    def get_source_metadata(self) -> dict:
        """
        Return metadata about this source adapter.

        Must include:
        - name: Human-readable source name
        - slug: URL-safe identifier
        - license_type: SourceLicense enum value
        - license_url: URL to license text
        - attribution_required: bool
        - allows_commercial_storage: bool
        - adapter_class: Full Python class path
        """
        ...

    async def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        now = time.monotonic()
        elapsed = now - self._last_request_time
        if elapsed < self._min_interval:
            wait_time = self._min_interval - elapsed
            logger.debug(
                "rate_limit_wait",
                adapter=self.__class__.__name__,
                wait_seconds=round(wait_time, 2),
            )
            await self._async_sleep(wait_time)
        self._last_request_time = time.monotonic()
        self._request_count += 1

    @staticmethod
    async def _async_sleep(seconds: float) -> None:
        """Async sleep helper."""
        import asyncio
        await asyncio.sleep(seconds)

    def _create_error(
        self,
        error_type: str,
        message: str,
        details: Optional[dict] = None,
        is_retryable: bool = False,
    ) -> dict:
        """Create a structured error record."""
        return {
            "error_type": error_type,
            "message": message,
            "details": details or {},
            "is_retryable": is_retryable,
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        }
