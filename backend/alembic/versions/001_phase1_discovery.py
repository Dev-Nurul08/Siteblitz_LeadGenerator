"""Phase 1: Create discovery engine tables

Revision ID: 001_phase1_discovery
Revises: 
Create Date: 2026-11-01

Creates:
- sources
- source_jobs
- source_records
- businesses
- business_locations
- business_categories
- business_source_links
- ingestion_errors
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = '001_phase1_discovery'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── sources ─────────────────────────────────────────────────
    op.create_table('sources',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('license_type', sa.Enum('OPEN_LICENSE','LICENSED_COMMERCIAL','API_RESTRICTED','MANUAL_OR_OPT_IN', name='sourcelicense'), nullable=False),
        sa.Column('license_url', sa.String(500), nullable=True),
        sa.Column('license_notes', sa.Text(), nullable=True),
        sa.Column('attribution_required', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('attribution_text', sa.String(500), nullable=True),
        sa.Column('allows_commercial_storage', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('allows_contact_enrichment', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('allows_marketing_use', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('max_cache_duration_hours', sa.Integer(), nullable=True),
        sa.Column('api_base_url', sa.String(500), nullable=True),
        sa.Column('rate_limit_rpm', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('adapter_class', sa.String(200), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE','PAUSED','DEPRECATED','DISABLED', name='sourcestatus'), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug'),
    )

    # ── source_jobs ─────────────────────────────────────────────
    op.create_table('source_jobs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('query_params', JSONB(), nullable=False, server_default='{}'),
        sa.Column('country_code', sa.String(10), nullable=True),
        sa.Column('region', sa.String(200), nullable=True),
        sa.Column('city', sa.String(200), nullable=True),
        sa.Column('category_filter', sa.String(200), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('radius_km', sa.Float(), nullable=True),
        sa.Column('bounding_box', JSONB(), nullable=True),
        sa.Column('status', sa.Enum('PENDING','RUNNING','COMPLETED','FAILED','CANCELLED','PARTIAL', name='jobstatus'), nullable=False, server_default='PENDING'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('records_found', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('records_new', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('records_duplicate', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('records_error', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_cursor', sa.String(500), nullable=True),
        sa.Column('is_resumable', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_source_jobs_source_status', 'source_jobs', ['source_id', 'status'])
    op.create_index('ix_source_jobs_country', 'source_jobs', ['country_code'])

    # ── source_records ──────────────────────────────────────────
    op.create_table('source_records',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=True),
        sa.Column('external_id', sa.String(500), nullable=False),
        sa.Column('external_url', sa.String(1000), nullable=True),
        sa.Column('raw_data', JSONB(), nullable=False),
        sa.Column('name', sa.String(500), nullable=True),
        sa.Column('country_code', sa.String(10), nullable=True),
        sa.Column('category', sa.String(200), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('processing_error', sa.Text(), nullable=True),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['job_id'], ['source_jobs.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_source_records_external', 'source_records', ['source_id', 'external_id'], unique=True)
    op.create_index('ix_source_records_country', 'source_records', ['country_code'])
    op.create_index('ix_source_records_processed', 'source_records', ['is_processed'])

    # ── businesses ──────────────────────────────────────────────
    op.create_table('businesses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('normalized_name', sa.String(500), nullable=False),
        sa.Column('business_type', sa.Enum('COMPANY','SOLE_TRADER','PARTNERSHIP','FRANCHISE','NON_PROFIT','GOVERNMENT','INDIVIDUAL_PROFESSIONAL','UNKNOWN', name='businesstype'), nullable=False, server_default='UNKNOWN'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('country_code', sa.String(10), nullable=True),
        sa.Column('country_name', sa.String(100), nullable=True),
        sa.Column('website_url', sa.String(1000), nullable=True),
        sa.Column('website_status', sa.Enum('UNKNOWN','NOT_FOUND','SOCIAL_ONLY','FOUND','BROKEN','UNDER_CONSTRUCTION', name='websitestatus'), nullable=False, server_default='UNKNOWN'),
        sa.Column('social_urls', JSONB(), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('email', sa.String(320), nullable=True),
        sa.Column('status', sa.Enum('DISCOVERED','ACTIVE','INACTIVE','DUPLICATE','INVALID','ARCHIVED', name='businessstatus'), nullable=False, server_default='DISCOVERED'),
        sa.Column('merged_into_id', sa.Integer(), nullable=True),
        sa.Column('employee_count_range', sa.String(50), nullable=True),
        sa.Column('year_founded', sa.Integer(), nullable=True),
        sa.Column('extra_data', JSONB(), nullable=True),
        sa.Column('discovered_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('last_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_businesses_country', 'businesses', ['country_code'])
    op.create_index('ix_businesses_status', 'businesses', ['status'])
    op.create_index('ix_businesses_website_status', 'businesses', ['website_status'])
    op.create_index('ix_businesses_normalized_name', 'businesses', ['normalized_name'])
    op.create_index('ix_businesses_dedup', 'businesses', ['normalized_name', 'country_code'])

    # ── business_locations ──────────────────────────────────────
    op.create_table('business_locations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('address_line_1', sa.String(500), nullable=True),
        sa.Column('address_line_2', sa.String(500), nullable=True),
        sa.Column('city', sa.String(200), nullable=True),
        sa.Column('state_province', sa.String(200), nullable=True),
        sa.Column('postal_code', sa.String(50), nullable=True),
        sa.Column('country_code', sa.String(10), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_headquarters', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('location_name', sa.String(200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_business_locations_business', 'business_locations', ['business_id'])
    op.create_index('ix_business_locations_city', 'business_locations', ['city'])
    op.create_index('ix_business_locations_country', 'business_locations', ['country_code'])
    op.create_index('ix_business_locations_coords', 'business_locations', ['latitude', 'longitude'])

    # ── business_categories ─────────────────────────────────────
    op.create_table('business_categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('category_name', sa.String(200), nullable=False),
        sa.Column('normalized_category', sa.String(200), nullable=False),
        sa.Column('source_category', sa.String(500), nullable=True),
        sa.Column('industry_group', sa.String(200), nullable=True),
        sa.Column('sub_industry', sa.String(200), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('business_id', 'normalized_category', name='uq_business_category'),
    )
    op.create_index('ix_business_categories_business', 'business_categories', ['business_id'])
    op.create_index('ix_business_categories_normalized', 'business_categories', ['normalized_category'])
    op.create_index('ix_business_categories_industry', 'business_categories', ['industry_group'])

    # ── business_source_links ───────────────────────────────────
    op.create_table('business_source_links',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('source_record_id', sa.Integer(), nullable=False),
        sa.Column('is_primary_source', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('match_method', sa.String(100), nullable=True),
        sa.Column('linked_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_record_id'], ['source_records.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('business_id', 'source_record_id', name='uq_business_source_link'),
    )
    op.create_index('ix_bsl_business', 'business_source_links', ['business_id'])
    op.create_index('ix_bsl_source_record', 'business_source_links', ['source_record_id'])

    # ── ingestion_errors ────────────────────────────────────────
    op.create_table('ingestion_errors',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('job_id', sa.Integer(), nullable=True),
        sa.Column('source_record_id', sa.Integer(), nullable=True),
        sa.Column('error_type', sa.String(100), nullable=False),
        sa.Column('severity', sa.Enum('WARNING','ERROR','CRITICAL', name='ingestionerrorseverity'), nullable=False, server_default='ERROR'),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('details', JSONB(), nullable=True),
        sa.Column('is_retryable', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_retries', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('resolved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id']),
        sa.ForeignKeyConstraint(['job_id'], ['source_jobs.id']),
        sa.ForeignKeyConstraint(['source_record_id'], ['source_records.id']),
    )
    op.create_index('ix_ingestion_errors_source', 'ingestion_errors', ['source_id'])
    op.create_index('ix_ingestion_errors_job', 'ingestion_errors', ['job_id'])
    op.create_index('ix_ingestion_errors_type', 'ingestion_errors', ['error_type'])
    op.create_index('ix_ingestion_errors_resolved', 'ingestion_errors', ['resolved'])


def downgrade() -> None:
    op.drop_table('ingestion_errors')
    op.drop_table('business_source_links')
    op.drop_table('business_categories')
    op.drop_table('business_locations')
    op.drop_table('businesses')
    op.drop_table('source_records')
    op.drop_table('source_jobs')
    op.drop_table('sources')

    # Drop enums
    for enum_name in ['sourcelicense', 'sourcestatus', 'jobstatus', 'businesstype', 'websitestatus', 'businessstatus', 'ingestionerrorseverity']:
        op.execute(f'DROP TYPE IF EXISTS {enum_name}')
