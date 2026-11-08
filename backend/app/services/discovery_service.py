"""
Discovery service — orchestrates source adapters, normalization,
deduplication, and database persistence.

This is the main entry point for Phase 1 business discovery.
"""

import re
from datetime import datetime, timezone
from typing import Optional

import structlog
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.engines.discovery.base import AdapterResult, BaseSourceAdapter, DiscoveredBusiness
from backend.app.engines.discovery.normalizer import BusinessNormalizer, _haversine_distance
from backend.app.engines.discovery.geocode import resolved_place
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


# Words that say what kind of business it is, not which one — never enough to call two names the same.
_GENERIC_NAME_WORDS = {
    "the", "and", "for", "dr", "drs", "clinic", "clinics", "dental", "dentist", "dentists", "care",
    "centre", "center", "hospital", "multispeciality", "speciality", "specialty", "super", "advanced",
    "smile", "smiles", "tooth", "teeth", "salon", "beauty", "parlour", "parlor", "hair", "studio",
    "unisex", "spa", "cafe", "coffee", "restaurant", "restro", "lounge", "shop", "store", "point",
    "house", "india", "pvt", "ltd", "health", "family", "new", "best", "city", "plus",
}


def _share_distinctive_word(name1: str, name2: str) -> bool:
    """
    True when the distinctive words of one name are all in the other ("Cosmo Dentist" ⊂
    "Dr Gupta Cosmo Dental Clinic"). Branches differ by an extra word each ("Clove Dental Andheri"
    vs "Clove Dental Bandra") and are kept apart.
    """
    words = lambda n: {w for w in BusinessNormalizer.normalize_name(n).split()
                       if len(w) >= 4 and w not in _GENERIC_NAME_WORDS}
    a, b = words(name1), words(name2)
    return bool(a & b) and (a <= b or b <= a)


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
            # Surface the source's own reason on the job; it used to live only in
            # ingestion_errors, so a PARTIAL job with 0 results showed no explanation.
            if result.errors:
                job.error_message = "; ".join(
                    e.get("message", "unknown error") for e in result.errors[:3]
                )[:1000]

            if result.has_more:
                job.last_cursor = result.next_cursor
            # How many matching businesses the source has in the area (before max_results), so the
            # UI can say "500 of 3,780". Stored in the job's JSON params: no schema change needed.
            if result.total_available is not None:
                job.query_params = {**(job.query_params or {}), "available": result.total_available}

            await self.session.flush()

            return {
                "job_id": job.id,
                "source": source_slug,
                "status": job.status.value,
                **stats,
                "available": result.total_available,
                # What the city name resolved to (Nominatim), so a wrong place is visible.
                "resolved_place": resolved_place(city, country_code, region) if city else None,
                # The Discovery result card shows this under the counts.
                **({"error": job.error_message} if job.error_message else {}),
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
                # Each record runs in its own SAVEPOINT: one bad record is rolled back and logged
                # instead of poisoning the session and failing the whole job (seen 2026-11-08:
                # 4,286 Pune salons lost to one duplicate category row).
                async with self.session.begin_nested():
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
                        await self._create_business(discovered, source_record)
                        stats["new"] += 1

                    # Mark source record as processed
                    source_record.is_processed = True
                    await self.session.flush()

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

    async def _find_by_phone(self, discovered: DiscoveredBusiness,
                             country: Optional[str]) -> Optional[Business]:
        """
        Same phone number (last 10 digits) or same email in the same city / within 5 km = the same
        business,
        even when the sources spell the name differently ("Cafe Nirvana" vs "Nirvana Cafe").
        Needed once several sources are merged in one search.
        """
        digits = re.sub(r"\D", "", discovered.phone or "")
        email = (discovered.email or "").strip().lower()
        conditions = []
        if len(digits) >= 10:
            conditions.append(Business.phone.like(f"%{digits[-10:]}"))
        # Same email = same business too (city test 2026-11-08: one dentist listed twice under
        # two names with the same Gmail address and different phone formats).
        if "@" in email:
            conditions.append(func.lower(Business.email) == email)
        if not conditions:
            return None
        stmt = (select(Business).where(or_(*conditions))
                .options(selectinload(Business.locations)))
        if country:
            stmt = stmt.where(Business.country_code == country)
        for candidate in (await self.session.execute(stmt)).scalars().all():
            location = candidate.locations[0] if candidate.locations else None
            same_city = bool(location and location.city and discovered.city
                             and location.city.strip().lower() == discovered.city.strip().lower())
            distance = (_haversine_distance(location.latitude, location.longitude,
                                            discovered.latitude, discovered.longitude)
                        if location and location.latitude is not None and discovered.latitude is not None
                        else None)
            if not (same_city or (distance is not None and distance < 5.0)):
                continue
            # A shared phone / email alone can be a chain's head office: two branches of one clinic
            # are two sales opportunities. Merge only with a second sign — the same spot (≤ 0.5 km)
            # or one name's distinctive words contained in the other's (see _share_distinctive_word).
            if (distance is not None and distance <= 0.5) or _share_distinctive_word(
                    discovered.name, candidate.name):
                return candidate
        return None

    async def _find_existing_business(
        self, discovered: DiscoveredBusiness
    ) -> Optional[Business]:
        """Check if a business already exists using phone, then name + location matching."""
        normalized_name = self.normalizer.normalize_name(discovered.name)
        if not normalized_name:
            return None

        country = self.normalizer.normalize_country_code(discovered.country_code)
        by_phone = await self._find_by_phone(discovered, country)
        if by_phone:
            return by_phone

        # Query candidates by normalized name, with their locations: without the stored city /
        # coordinates every same-name business in the country looked like a duplicate, so two
        # different "Sharma Sweets" in Pune and Delhi were merged and the second was lost.
        stmt = (
            select(Business)
            .where(Business.normalized_name == normalized_name)
            .options(selectinload(Business.locations))
        )
        if country:
            stmt = stmt.where(Business.country_code == country)

        result = await self.session.execute(stmt)
        candidates = result.scalars().all()

        for candidate in candidates:
            location = candidate.locations[0] if candidate.locations else None
            is_dup, confidence = self.normalizer.is_potential_duplicate(
                discovered.name,
                candidate.name,
                city1=discovered.city,
                city2=location.city if location else None,
                country1=country,
                country2=candidate.country_code,
                lat1=discovered.latitude,
                lon1=discovered.longitude,
                lat2=location.latitude if location else None,
                lon2=location.longitude if location else None,
            )
            # 0.70 = the normalizer's "same city" / "within 5 km" levels. Lower levels (same name,
            # unknown place) are not enough evidence to merge two records.
            if is_dup and confidence >= 0.70:
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
        seen_categories: set[str] = set()
        for idx, cat in enumerate(discovered.categories):
            industry, normalized, source_cat = self.normalizer.normalize_category(cat)
            # amenity=clinic + healthcare=clinic both normalise to "clinic"; a second row would
            # break the (business, category) unique key and used to fail the whole job.
            if normalized.lower() in seen_categories:
                continue
            seen_categories.add(normalized.lower())
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
