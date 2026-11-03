"""
Discovery service — orchestrates source adapters, normalization,
deduplication, and database persistence.

This is the main entry point for Phase 1 business discovery.
"""

from datetime import datetime, timezone
from typing import Optional

import structlog
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.engines.discovery.base import AdapterResult, BaseSourceAdapter, DiscoveredBusiness
from backend.app.engines.discovery.normalizer import BusinessNormalizer
from backend.app.engines.discovery.registry import SourceAdapterRegistry
from backend.app.models.business import (
    Business,
    BusinessCategory,
    BusinessLocation,
    BusinessSourceLink,
    BusinessStatus,
    IngestionError,
    IngestionErrorSeverity,
    WebsiteStatus,
)
from backend.app.models.source import (
    JobStatus,
    Source,
    SourceJob,
    SourceRecord,
)

logger = structlog.get_logger(__name__)


class DiscoveryService:
    """
    Orchestrates the business discovery pipeline:
    1. Resolve source adapter
    2. Execute discovery query
    3. Save raw source records
    4. Normalize business data
    5. Deduplicate against existing records
    6. Persist new businesses
    7. Track errors and job status
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.normalizer = BusinessNormalizer()

    async def run_discovery(
        self,
        source_slug: str,
        *,
        country_code: Optional[str] = None,
        region: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius_km: Optional[float] = None,
        max_results: int = 500,
        query_params: Optional[dict] = None,
    ) -> dict:
        """
        Execute a full discovery run for a given source.

        Returns a summary dict with job_id, counts, and errors.
        """
        # 1. Get or create source
        source = await self._get_or_create_source(source_slug)
        if not source:
            return {"error": f"Unknown source adapter: {source_slug}"}

        # 2. Create job record
        job = SourceJob(
            source_id=source.id,
            query_params=query_params or {},
            country_code=country_code,
            region=region,
            city=city,
            category_filter=category,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        self.session.add(job)
        await self.session.flush()

        try:
            # 3. Get adapter and discover
            adapter = self._get_adapter(source)
            result = await adapter.discover(
                country_code=country_code,
                region=region,
                city=city,
                category=category,
                latitude=latitude,
                longitude=longitude,
                radius_km=radius_km,
                max_results=max_results,
                query_params=query_params,
            )

            # 4. Process results
            stats = await self._process_results(source, job, result)

            # 5. Update job status
            job.status = (
                JobStatus.COMPLETED
                if not result.errors
                else JobStatus.PARTIAL
            )
            job.completed_at = datetime.now(timezone.utc)
            job.records_found = stats["found"]
            job.records_new = stats["new"]
            job.records_duplicate = stats["duplicate"]
            job.records_error = stats["errors"]

            if result.has_more:
                job.last_cursor = result.next_cursor

            await self.session.flush()

            return {
                "job_id": job.id,
                "source": source_slug,
                "status": job.status.value,
                **stats,
            }

        except Exception as e:
            logger.error("discovery_failed", source=source_slug, error=str(e))
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now(timezone.utc)
            await self.session.flush()

            return {
                "job_id": job.id,
                "source": source_slug,
                "status": "FAILED",
                "error": str(e),
            }

    async def _get_or_create_source(self, slug: str) -> Optional[Source]:
        """Get an existing source or create one from adapter metadata."""
        # Check database first
        stmt = select(Source).where(Source.slug == slug)
        result = await self.session.execute(stmt)
        source = result.scalar_one_or_none()

        if source:
            return source

        # Try to create from adapter metadata
        try:
            adapter_class = SourceAdapterRegistry.get_or_import(
                slug,
                # Try common paths
                f"backend.app.engines.discovery.{slug}.{slug.title().replace('_', '')}Adapter",
            )
        except ValueError:
            # Try known adapters
            known = {
                "openstreetmap": "backend.app.engines.discovery.osm.OSMAdapter",
                "csv_import": "backend.app.engines.discovery.csv_import.CSVImportAdapter",
            }
            if slug not in known:
                return None
            adapter_class = SourceAdapterRegistry.get_or_import(slug, known[slug])

        adapter = adapter_class()
        meta = adapter.get_source_metadata()

        source = Source(
            name=meta["name"],
            slug=meta["slug"],
            description=meta.get("description"),
            license_type=meta["license_type"],
            license_url=meta.get("license_url"),
            attribution_required=meta.get("attribution_required", False),
            attribution_text=meta.get("attribution_text"),
            allows_commercial_storage=meta.get("allows_commercial_storage", False),
            allows_contact_enrichment=meta.get("allows_contact_enrichment", False),
            allows_marketing_use=meta.get("allows_marketing_use", False),
            api_base_url=meta.get("api_base_url"),
            rate_limit_rpm=meta.get("rate_limit_rpm", 30),
            adapter_class=meta["adapter_class"],
        )
        self.session.add(source)
        await self.session.flush()

        return source

    def _get_adapter(self, source: Source) -> BaseSourceAdapter:
        """Instantiate the adapter for a given source."""
        adapter_class = SourceAdapterRegistry.get_or_import(
            source.slug, source.adapter_class
        )
        return adapter_class(rate_limit_rpm=source.rate_limit_rpm)

    async def _process_results(
        self, source: Source, job: SourceJob, result: AdapterResult
    ) -> dict:
        """Process adapter results: save records, normalize, deduplicate, persist."""
        stats = {"found": 0, "new": 0, "duplicate": 0, "errors": 0}

        # Save adapter errors
        for error in result.errors:
            await self._save_error(source.id, job.id, error)
            stats["errors"] += 1

        for discovered in result.businesses:
            stats["found"] += 1
            try:
                # Save raw source record
                source_record = await self._save_source_record(
                    source, job, discovered
                )
                if not source_record:
                    stats["duplicate"] += 1
                    continue

                # Check for existing business (deduplication)
                existing = await self._find_existing_business(discovered)
                if existing:
                    # Link to existing business
                    await self._link_business_to_source(
                        existing, source_record, method="dedup_match"
                    )
                    stats["duplicate"] += 1
                else:
                    # Create new business
                    business = await self._create_business(discovered, source_record)
                    stats["new"] += 1

                # Mark source record as processed
                source_record.is_processed = True

            except Exception as e:
                logger.error(
                    "record_processing_error",
                    external_id=discovered.source_external_id,
                    error=str(e),
                )
                stats["errors"] += 1
                await self._save_error(
                    source.id,
                    job.id,
                    {
                        "error_type": "processing",
                        "message": str(e),
                        "details": {"external_id": discovered.source_external_id},
                        "is_retryable": True,
                    },
                )

        return stats

    async def _save_source_record(
        self, source: Source, job: SourceJob, discovered: DiscoveredBusiness
    ) -> Optional[SourceRecord]:
        """Save a raw source record. Returns None if duplicate external_id."""
        # Check for existing record from same source
        stmt = select(SourceRecord).where(
            and_(
                SourceRecord.source_id == source.id,
                SourceRecord.external_id == discovered.source_external_id,
            )
        )
        result = await self.session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            return None  # Already have this record

        record = SourceRecord(
            source_id=source.id,
            job_id=job.id,
            external_id=discovered.source_external_id,
            external_url=discovered.source_external_url,
            raw_data=discovered.raw_data,
            name=discovered.name,
            country_code=self.normalizer.normalize_country_code(
                discovered.country_code
            ),
            category=(
                discovered.categories[0] if discovered.categories else None
            ),
            latitude=discovered.latitude,
            longitude=discovered.longitude,
        )
        self.session.add(record)
        await self.session.flush()
        return record

    async def _find_existing_business(
        self, discovered: DiscoveredBusiness
    ) -> Optional[Business]:
        """Check if a business already exists using name + location matching."""
        normalized_name = self.normalizer.normalize_name(discovered.name)
        if not normalized_name:
            return None

        country = self.normalizer.normalize_country_code(discovered.country_code)

        # Query candidates by normalized name
        stmt = select(Business).where(
            Business.normalized_name == normalized_name,
        )
        if country:
            stmt = stmt.where(Business.country_code == country)

        result = await self.session.execute(stmt)
        candidates = result.scalars().all()

        for candidate in candidates:
            is_dup, confidence = self.normalizer.is_potential_duplicate(
                discovered.name,
                candidate.name,
                city1=discovered.city,
                city2=None,  # Would need to join locations
                country1=country,
                country2=candidate.country_code,
                lat1=discovered.latitude,
                lon1=discovered.longitude,
            )
            if is_dup and confidence >= 0.50:
                return candidate

        return None

    async def _create_business(
        self, discovered: DiscoveredBusiness, source_record: SourceRecord
    ) -> Business:
        """Create a new canonical business from a discovered record."""
        normalized_name = self.normalizer.normalize_name(discovered.name)
        country = self.normalizer.normalize_country_code(discovered.country_code)

        # Normalize website
        website = self.normalizer.normalize_website(discovered.website_url)
        website_status = WebsiteStatus.UNKNOWN
        if website:
            website_status = WebsiteStatus.FOUND
        elif discovered.social_urls:
            website_status = WebsiteStatus.SOCIAL_ONLY

        business = Business(
            name=discovered.name,
            normalized_name=normalized_name,
            description=discovered.description,
            country_code=country,
            website_url=website,
            website_status=website_status,
            social_urls=discovered.social_urls or None,
            phone=self.normalizer.normalize_phone(discovered.phone),
            email=discovered.email,
            status=BusinessStatus.DISCOVERED,
        )
        self.session.add(business)
        await self.session.flush()

        # Add location
        if any([
            discovered.address_line_1,
            discovered.city,
            discovered.latitude,
        ]):
            location = BusinessLocation(
                business_id=business.id,
                address_line_1=discovered.address_line_1,
                city=discovered.city,
                state_province=discovered.state_province,
                postal_code=discovered.postal_code,
                country_code=country,
                latitude=discovered.latitude,
                longitude=discovered.longitude,
                is_primary=True,
            )
            self.session.add(location)

        # Add categories
        for idx, cat in enumerate(discovered.categories):
            industry, normalized, source_cat = self.normalizer.normalize_category(cat)
            source_original = (
                discovered.source_categories[idx]
                if idx < len(discovered.source_categories)
                else cat
            )
            category = BusinessCategory(
                business_id=business.id,
                category_name=normalized,
                normalized_category=normalized.lower(),
                source_category=source_original,
                industry_group=industry,
                is_primary=(idx == 0),
            )
            self.session.add(category)

        # Link to source record
        await self._link_business_to_source(
            business, source_record, method="initial_discovery"
        )

        await self.session.flush()
        return business

    async def _link_business_to_source(
        self,
        business: Business,
        source_record: SourceRecord,
        method: str = "unknown",
    ) -> None:
        """Create a link between a business and its source record."""
        link = BusinessSourceLink(
            business_id=business.id,
            source_record_id=source_record.id,
            is_primary_source=(method == "initial_discovery"),
            match_method=method,
        )
        self.session.add(link)

    async def _save_error(
        self,
        source_id: int,
        job_id: int,
        error: dict,
    ) -> None:
        """Save an ingestion error."""
        err = IngestionError(
            source_id=source_id,
            job_id=job_id,
            error_type=error.get("error_type", "unknown"),
            severity=IngestionErrorSeverity.ERROR,
            message=error.get("message", "Unknown error"),
            details=error.get("details"),
            is_retryable=error.get("is_retryable", False),
        )
        self.session.add(err)
