"""
Phase 1 — Business models.

Canonical business entities, locations, categories, source links,
and ingestion error tracking. Handles multi-location businesses
and multi-source deduplication.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")

from backend.app.database import Base


# ─── Enumerations ────────────────────────────────────────────────


class BusinessStatus(str, enum.Enum):
    """Lifecycle status of a business record."""

    DISCOVERED = "DISCOVERED"  # Just found, not yet researched
    ACTIVE = "ACTIVE"  # Confirmed operating
    INACTIVE = "INACTIVE"  # Appears closed or dormant
    DUPLICATE = "DUPLICATE"  # Merged into another record
    INVALID = "INVALID"  # Bad data / not a real business
    ARCHIVED = "ARCHIVED"  # Manually archived


class WebsiteStatus(str, enum.Enum):
    """Status of a business's known website presence."""

    UNKNOWN = "UNKNOWN"  # Not yet checked
    NOT_FOUND = "NOT_FOUND"  # No website identified
    SOCIAL_ONLY = "SOCIAL_ONLY"  # Only social media presence
    FOUND = "FOUND"  # Official website identified
    BROKEN = "BROKEN"  # Website exists but not functioning
    UNDER_CONSTRUCTION = "UNDER_CONSTRUCTION"


class BusinessType(str, enum.Enum):
    """Classification of the business entity type."""

    COMPANY = "COMPANY"
    SOLE_TRADER = "SOLE_TRADER"
    PARTNERSHIP = "PARTNERSHIP"
    FRANCHISE = "FRANCHISE"
    NON_PROFIT = "NON_PROFIT"
    GOVERNMENT = "GOVERNMENT"
    INDIVIDUAL_PROFESSIONAL = "INDIVIDUAL_PROFESSIONAL"  # For portfolio campaigns
    UNKNOWN = "UNKNOWN"


# ─── Business ────────────────────────────────────────────────────


class Business(Base):
    """
    Canonical business entity — the single source of truth for a business.

    A business may have multiple locations, categories, and source records.
    Deduplication merges source records into a single canonical business.
    """

    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Identity
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(500), nullable=False)
    business_type: Mapped[BusinessType] = mapped_column(
        Enum(BusinessType), default=BusinessType.UNKNOWN
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Primary country
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    country_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Online presence
    website_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    website_status: Mapped[WebsiteStatus] = mapped_column(
        Enum(WebsiteStatus), default=WebsiteStatus.UNKNOWN
    )
    social_urls: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    # e.g., {"facebook": "...", "instagram": "...", "linkedin": "..."}

    # Contact (business-level, not personal)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(320), nullable=True)

    # Status
    status: Mapped[BusinessStatus] = mapped_column(
        Enum(BusinessStatus), default=BusinessStatus.DISCOVERED
    )
    merged_into_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Metadata
    employee_count_range: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    year_founded: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)

    # Timestamps
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    locations = relationship(
        "BusinessLocation", back_populates="business", cascade="all, delete-orphan"
    )
    categories = relationship(
        "BusinessCategory", back_populates="business", cascade="all, delete-orphan"
    )
    source_links = relationship(
        "BusinessSourceLink", back_populates="business", cascade="all, delete-orphan"
    )
    audits = relationship(
        "WebsiteAudit", back_populates="business", cascade="all, delete-orphan"
    )
    opportunities = relationship(
        "Opportunity", back_populates="business", cascade="all, delete-orphan"
    )
    contacts = relationship(
        "Contact", back_populates="business", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_businesses_country", "country_code"),
        Index("ix_businesses_status", "status"),
        Index("ix_businesses_website_status", "website_status"),
        Index("ix_businesses_normalized_name", "normalized_name"),
        Index(
            "ix_businesses_dedup",
            "normalized_name",
            "country_code",
        ),
    )

    @property
    def city(self) -> Optional[str]:
        if self.locations:
            return self.locations[0].city
        return None

    @property
    def website(self) -> Optional[str]:
        return self.website_url

    @property
    def category(self) -> Optional[str]:
        if self.categories:
            return self.categories[0].category_name
        return None

    def __repr__(self) -> str:
        return f"<Business(id={self.id}, name='{self.name}', country='{self.country_code}')>"


# ─── Business Location ──────────────────────────────────────────


class BusinessLocation(Base):
    """
    A physical location or service area of a business.

    Supports multi-location businesses (e.g., franchise chains).
    """

    __tablename__ = "business_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )

    # Address
    address_line_1: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    address_line_2: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    state_province: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Coordinates
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Location metadata
    is_primary: Mapped[bool] = mapped_column(default=True)
    is_headquarters: Mapped[bool] = mapped_column(default=False)
    location_name: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )  # e.g., "Downtown Branch"

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    business = relationship("Business", back_populates="locations")

    __table_args__ = (
        Index("ix_business_locations_business", "business_id"),
        Index("ix_business_locations_city", "city"),
        Index("ix_business_locations_country", "country_code"),
        Index("ix_business_locations_coords", "latitude", "longitude"),
    )

    def __repr__(self) -> str:
        return (
            f"<BusinessLocation(id={self.id}, business_id={self.business_id}, "
            f"city='{self.city}')>"
        )


# ─── Business Category ──────────────────────────────────────────


class BusinessCategory(Base):
    """
    Normalized industry classification for a business.

    A business can belong to multiple categories.
    """

    __tablename__ = "business_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )

    # Category
    category_name: Mapped[str] = mapped_column(String(200), nullable=False)
    normalized_category: Mapped[str] = mapped_column(String(200), nullable=False)
    source_category: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )  # Original category from source

    # Industry hierarchy
    industry_group: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )  # e.g., "Food & Beverage"
    sub_industry: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )  # e.g., "Restaurant"

    is_primary: Mapped[bool] = mapped_column(default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    business = relationship("Business", back_populates="categories")

    __table_args__ = (
        Index("ix_business_categories_business", "business_id"),
        Index("ix_business_categories_normalized", "normalized_category"),
        Index("ix_business_categories_industry", "industry_group"),
        UniqueConstraint(
            "business_id", "normalized_category", name="uq_business_category"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<BusinessCategory(id={self.id}, business_id={self.business_id}, "
            f"category='{self.normalized_category}')>"
        )


# ─── Business Source Link ────────────────────────────────────────


class BusinessSourceLink(Base):
    """
    Mapping between a canonical business and its source records.

    Preserves data provenance — every field value can be traced
    back to its original source.
    """

    __tablename__ = "business_source_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    source_record_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("source_records.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Link metadata
    is_primary_source: Mapped[bool] = mapped_column(default=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)  # 0.0–1.0
    match_method: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )  # e.g., "name_location", "external_id", "manual"

    # Timestamps
    linked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    business = relationship("Business", back_populates="source_links")
    source_record = relationship("SourceRecord", back_populates="business_links")

    __table_args__ = (
        UniqueConstraint(
            "business_id", "source_record_id", name="uq_business_source_link"
        ),
        Index("ix_bsl_business", "business_id"),
        Index("ix_bsl_source_record", "source_record_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<BusinessSourceLink(business_id={self.business_id}, "
            f"source_record_id={self.source_record_id})>"
        )


# ─── Ingestion Error ────────────────────────────────────────────


class IngestionErrorSeverity(str, enum.Enum):
    """Severity level of an ingestion error."""

    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class IngestionError(Base):
    """
    Tracks invalid records, retryable failures, and rejection reasons
    during the discovery and ingestion process.
    """

    __tablename__ = "ingestion_errors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("sources.id"), nullable=True
    )
    job_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("source_jobs.id"), nullable=True
    )
    source_record_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("source_records.id"), nullable=True
    )

    # Error details
    error_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # e.g., "validation", "network", "rate_limit"
    severity: Mapped[IngestionErrorSeverity] = mapped_column(
        Enum(IngestionErrorSeverity), default=IngestionErrorSeverity.ERROR
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)

    # Retryability
    is_retryable: Mapped[bool] = mapped_column(default=False)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    resolved: Mapped[bool] = mapped_column(default=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Timestamps
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        Index("ix_ingestion_errors_source", "source_id"),
        Index("ix_ingestion_errors_job", "job_id"),
        Index("ix_ingestion_errors_type", "error_type"),
        Index("ix_ingestion_errors_resolved", "resolved"),
    )

    def __repr__(self) -> str:
        return (
            f"<IngestionError(id={self.id}, type='{self.error_type}', "
            f"severity={self.severity.value})>"
        )
