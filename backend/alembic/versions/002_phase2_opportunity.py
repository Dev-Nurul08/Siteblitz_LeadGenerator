"""Phase 2: Create opportunity engine tables

Revision ID: 002_phase2_opportunity
Revises: 001_phase1_discovery
Create Date: 2026-11-03

Creates:
- website_audits
- opportunities
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = '002_phase2_opportunity'
down_revision: Union[str, None] = '001_phase1_discovery'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Enums ───────────────────────────────────────────────────
    service_category_enum = sa.Enum(
        'NEW_WEBSITE',
        'WEBSITE_REDESIGN',
        'MOBILE_APP',
        'ECOMMERCE_EXPANSION',
        'ONLINE_BOOKING',
        'SEO_PERFORMANCE',
        'CUSTOM_WEB_APP',
        name='servicecategory'
    )
    service_category_enum.create(op.get_bind(), checkfirst=True)

    opportunity_priority_enum = sa.Enum(
        'LOW',
        'MEDIUM',
        'HIGH',
        'CRITICAL',
        name='opportunitypriority'
    )
    opportunity_priority_enum.create(op.get_bind(), checkfirst=True)

    opportunity_status_enum = sa.Enum(
        'IDENTIFIED',
        'EVALUATING',
        'QUALIFIED',
        'DISQUALIFIED',
        'OUTREACH_PENDING',
        'IN_OUTREACH',
        'CONVERTED',
        name='opportunitystatus'
    )
    opportunity_status_enum.create(op.get_bind(), checkfirst=True)

    # ── website_audits ──────────────────────────────────────────
    op.create_table(
        'website_audits',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('url_analyzed', sa.String(1000), nullable=False),
        sa.Column('final_url', sa.String(1000), nullable=True),
        sa.Column('is_reachable', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('http_status', sa.Integer(), nullable=True),
        sa.Column('has_ssl', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('load_time_seconds', sa.Float(), nullable=True),
        sa.Column('is_mobile_responsive', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('has_viewport_meta', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('detected_cms', sa.String(100), nullable=True),
        sa.Column('detected_frameworks', JSONB(), nullable=True),
        sa.Column('has_ecommerce', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('has_online_booking', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('has_contact_form', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('has_analytics', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('meta_title', sa.String(500), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('headings_summary', JSONB(), nullable=True),
        sa.Column('emails_found', JSONB(), nullable=True),
        sa.Column('phones_found', JSONB(), nullable=True),
        sa.Column('social_links_found', JSONB(), nullable=True),
        sa.Column('raw_audit_data', JSONB(), nullable=True),
        sa.Column('audit_error', sa.Text(), nullable=True),
        sa.Column('audited_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_website_audits_business', 'website_audits', ['business_id'])
    op.create_index('ix_website_audits_reachable', 'website_audits', ['is_reachable'])

    # ── opportunities ───────────────────────────────────────────
    op.create_table(
        'opportunities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('audit_id', sa.Integer(), nullable=True),
        sa.Column('service_category', service_category_enum, nullable=False),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('priority', opportunity_priority_enum, nullable=False, server_default='MEDIUM'),
        sa.Column('status', opportunity_status_enum, nullable=False, server_default='IDENTIFIED'),
        sa.Column('evidence', JSONB(), nullable=False, server_default='{}'),
        sa.Column('pitch_angles', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['audit_id'], ['website_audits.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_opportunities_business', 'opportunities', ['business_id'])
    op.create_index('ix_opportunities_service', 'opportunities', ['service_category'])
    op.create_index('ix_opportunities_score', 'opportunities', ['score'])
    op.create_index('ix_opportunities_priority', 'opportunities', ['priority'])
    op.create_index('ix_opportunities_status', 'opportunities', ['status'])


def downgrade() -> None:
    op.drop_table('opportunities')
    op.drop_table('website_audits')

    for enum_name in ['servicecategory', 'opportunitypriority', 'opportunitystatus']:
        op.execute(f'DROP TYPE IF EXISTS {enum_name}')

