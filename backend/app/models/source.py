"""
Phase 1 — Source models.

Tracks data sources, their licenses, discovery jobs, and raw source records.
Every piece of business data must trace back to a documented source with
known reuse permissions.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")

from backend.app.database import Base


# ─── Enumerations ────────────────────────────────────────────────


class SourceLicense(str, enum.Enum):
    """Classification of data-source reuse permissions."""

    OPEN_LICENSE = "OPEN_LICENSE"  # e.g., ODbL (OpenStreetMap)
    LICENSED_COMMERCIAL = "LICENSED_COMMERCIAL"  # Paid/commercial license
    API_RESTRICTED = "API_RESTRICTED"  # Limited storage/reuse
    MANUAL_OR_OPT_IN = "MANUAL_OR_OPT_IN"  # Directly supplied / consent-based


class SourceStatus(str, enum.Enum):
    """Operational status of a data source."""

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DEPRECATED = "DEPRECATED"
    DISABLED = "DISABLED"


class JobStatus(str, enum.Enum):
    """Status of a discovery job execution."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    PARTIAL = "PARTIAL"  # Completed with some errors


# ─── Source ──────────────────────────────────────────────────────


class Source(Base):
    """
    A registered data source with documented license and usage terms.

    Examples: OpenStreetMap, Wikidata, Companies House, CSV Import.
    """

    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # License & reuse
    license_type: Mapped[SourceLicense] = mapped_column(
        Enum(SourceLicense), nullable=False
    )
    license_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    license_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attribution_required: Mapped[bool] = mapped_column(default=False)
    attribution_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Permitted uses
    allows_commercial_storage: Mapped[bool] = mapped_column(default=False)
    allows_contact_enrichment: Mapped[bool] = mapped_column(default=False)
    allows_marketing_use: Mapped[bool] = mapped_column(default=False)
    max_cache_duration_hours: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )

    # API configuration
    api_base_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    rate_limit_rpm: Mapped[int] = mapped_column(Integer, default=30)
    adapter_class: Mapped[str] = mapped_column(String(200), nullable=False)

    # Status
    status: Mapped[SourceStatus] = mapped_column(
        Enum(SourceStatus), default=SourceStatus.ACTIVE
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    jobs = relationship("SourceJob", back_populates="source", cascade="all, delete-orphan")
    records = relationship(
        "SourceRecord", back_populates="source", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Source(id={self.id}, name='{self.name}', license={self.license_type.value})>"


# ─── Source Job ──────────────────────────────────────────────────


class SourceJob(Base):
    """
    A single discovery-job execution against a source.

    Tracks the query parameters, geographic scope, execution status,
    and result counts for resumability and auditing.
    """

    __tablename__ = "source_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False
    )

    # Query configuration
    query_params: Mapped[dict] = mapped_column(JSON_TYPE, nullable=False, default=dict)
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    category_filter: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Geographic scope
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    radius_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bounding_box: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)

    # Execution
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus), default=JobStatus.PENDING
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Results
    records_found: Mapped[int] = mapped_column(Integer, default=0)
    records_new: Mapped[int] = mapped_column(Integer, default=0)
    records_duplicate: Mapped[int] = mapped_column(Integer, default=0)
    records_error: Mapped[int] = mapped_column(Integer, default=0)

    # Resumability
    last_cursor: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_resumable: Mapped[bool] = mapped_column(default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    source = relationship("Source", back_populates="jobs")
    records = relationship(
        "SourceRecord", back_populates="job", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_source_jobs_source_status", "source_id", "status"),
        Index("ix_source_jobs_country", "country_code"),
        {"schema": None},
    )

    def __repr__(self) -> str:
        return (
            f"<SourceJob(id={self.id}, source_id={self.source_id}, "
            f"status={self.status.value})>"
        )


# ─── Source Record ───────────────────────────────────────────────


class SourceRecord(Base):
    """
    Raw record as received from a data source, before normalization.

    Preserves the original source identifier and data for traceability.
    Never modified after creation — serves as the audit trail.
    """

    __tablename__ = "source_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False
    )
    job_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("source_jobs.id", ondelete="SET NULL"), nullable=True
    )

    # Source identification
    external_id: Mapped[str] = mapped_column(String(500), nullable=False)
    external_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Raw data (preserved exactly as received)
    raw_data: Mapped[dict] = mapped_column(JSON_TYPE, nullable=False)

    # Extracted fields (for indexing and quick lookup)
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Processing
    is_processed: Mapped[bool] = mapped_column(default=False)
    processing_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    source = relationship("Source", back_populates="records")
    job = relationship("SourceJob", back_populates="records")
    business_links = relationship(
        "BusinessSourceLink", back_populates="source_record", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_source_records_external", "source_id", "external_id", unique=True),
        Index("ix_source_records_country", "country_code"),
        Index("ix_source_records_processed", "is_processed"),
        {"schema": None},
    )

    def __repr__(self) -> str:
        return (
            f"<SourceRecord(id={self.id}, source_id={self.source_id}, "
            f"external_id='{self.external_id}')>"
        )
