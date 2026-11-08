"""Lead Radar: Create lead_radar_evaluations table and enums

Revision ID: 004_lead_radar_strategy
Revises: 003_phase3_enrichment
Create Date: 2026-11-06

Creates:
- lead_radar_evaluations
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = '004_lead_radar_strategy'
down_revision: Union[str, None] = '003_phase3_enrichment'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    # ── Enums ───────────────────────────────────────────────────
    owned_presence_enum = sa.Enum(
        'OWN_DOMAIN',
        'BUILDER_SUBDOMAIN',
        'PARENT_COMPANY_PAGE',
        'SOCIAL_ONLY',
        'MARKETPLACE_ONLY',
        'LINK_IN_BIO',
        'NONE_FOUND',
        'UNRESOLVED',
        name='ownedpresence'
    )
    owned_presence_enum.create(bind, checkfirst=True)

    availability_enum = sa.Enum(
        'WORKING',
        'PARKED',
        'COMING_SOON',
        'DNS_FAIL',
        'CERTIFICATE_FAIL',
        'REPEATED_SERVER_FAIL',
        'REDIRECTED',
        'UNKNOWN',
        name='availability'
    )
    availability_enum.create(bind, checkfirst=True)

    customer_task_covered_enum = sa.Enum(
        'INFORMATION',
        'PRODUCT_EVALUATION',
        'ENQUIRY',
        'BOOKING',
        'ORDERING',
        'LOCATION',
        'NONE_NEEDED',
        'UNKNOWN',
        name='customertaskcovered'
    )
    customer_task_covered_enum.create(bind, checkfirst=True)

    task_quality_enum = sa.Enum(
        'WORKS',
        'INCOMPLETE',
        'FAILS_REPRODUCIBLY',
        'NOT_TESTED',
        name='taskquality'
    )
    task_quality_enum.create(bind, checkfirst=True)

    buying_status_enum = sa.Enum(
        'EXPLICITLY_SEEKING',
        'EXPLICITLY_NOT_SEEKING',
        'SUPPLIER_ALREADY_CHOSEN',
        'UNKNOWN',
        name='buyingstatus'
    )
    buying_status_enum.create(bind, checkfirst=True)

    authority_enum = sa.Enum(
        'LOCAL_OWNER',
        'FRANCHISEE',
        'PARENT_COMPANY',
        'PROCUREMENT_TEAM',
        'UNRESOLVED',
        name='authority'
    )
    authority_enum.create(bind, checkfirst=True)

    segment_enum = sa.Enum(
        'A',
        'B',
        'C',
        'UNKNOWN',
        name='segment'
    )
    segment_enum.create(bind, checkfirst=True)

    # ── lead_radar_evaluations ───────────────────────────────────
    op.create_table(
        'lead_radar_evaluations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('owned_presence', owned_presence_enum, nullable=False, server_default='UNRESOLVED'),
        sa.Column('availability', availability_enum, nullable=False, server_default='UNKNOWN'),
        sa.Column('customer_task_covered', customer_task_covered_enum, nullable=False, server_default='UNKNOWN'),
        sa.Column('task_quality', task_quality_enum, nullable=False, server_default='NOT_TESTED'),
        sa.Column('buying_status', buying_status_enum, nullable=False, server_default='UNKNOWN'),
        sa.Column('authority', authority_enum, nullable=False, server_default='UNRESOLVED'),
        sa.Column('identity_verified', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('currently_active', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('absence_search_done', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('repeated_failure', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('segment', segment_enum, nullable=False, server_default='UNKNOWN'),
        sa.Column('warm_context', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('conditions_met', sa.JSON().with_variant(JSONB, 'postgresql'), nullable=True),
        sa.Column('condition_results', sa.JSON().with_variant(JSONB, 'postgresql'), nullable=True),
        sa.Column('matched_recipes', sa.JSON().with_variant(JSONB, 'postgresql'), nullable=True),
        sa.Column('primary_recipe_id', sa.String(length=20), nullable=True),
        sa.Column('pitch_opening_fact', sa.Text(), nullable=True),
        sa.Column('pitch_angle', sa.Text(), nullable=True),
        sa.Column('pitch_never_say', sa.Text(), nullable=True),
        sa.Column('pitch_recommended_solution', sa.Text(), nullable=True),
        sa.Column('revenue_category', sa.String(length=50), nullable=True),
        sa.Column('revenue_confidence', sa.String(length=20), nullable=True),
        sa.Column('min_annual_revenue', sa.Float(), nullable=True),
        sa.Column('max_annual_revenue', sa.Float(), nullable=True),
        sa.Column('revenue_currency', sa.String(length=10), nullable=False, server_default='USD'),
        sa.Column('revenue_formula', sa.Text(), nullable=True),
        sa.Column('absence_certificate_id', sa.String(length=100), nullable=True),
        sa.Column('absence_certificate_hash', sa.String(length=100), nullable=True),
        sa.Column('absence_certificate_data', sa.JSON().with_variant(JSONB, 'postgresql'), nullable=True),
        sa.Column('rank_opportunity_class', sa.String(length=50), nullable=True),
        sa.Column('rank_evidence_quality', sa.String(length=50), nullable=True),
        sa.Column('rank_task_severity', sa.String(length=50), nullable=True),
        sa.Column('rank_demand_level', sa.String(length=50), nullable=True),
        sa.Column('rank_authority_level', sa.String(length=50), nullable=True),
        sa.Column('why_this_business', sa.Text(), nullable=True),
        sa.Column('why_this_project', sa.Text(), nullable=True),
        sa.Column('why_now', sa.Text(), nullable=True),
        sa.Column('what_is_unknown', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('business_id'),
    )

    op.create_index('ix_lead_radar_segment', 'lead_radar_evaluations', ['segment'])
    op.create_index('ix_lead_radar_warm', 'lead_radar_evaluations', ['warm_context'])
    op.create_index('ix_lead_radar_recipe', 'lead_radar_evaluations', ['primary_recipe_id'])
    op.create_index('ix_lead_radar_created', 'lead_radar_evaluations', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_lead_radar_created', table_name='lead_radar_evaluations')
    op.drop_index('ix_lead_radar_recipe', table_name='lead_radar_evaluations')
    op.drop_index('ix_lead_radar_warm', table_name='lead_radar_evaluations')
    op.drop_index('ix_lead_radar_segment', table_name='lead_radar_evaluations')
    op.drop_table('lead_radar_evaluations')

    bind = op.get_bind()
    for name in ['segment', 'authority', 'buyingstatus', 'taskquality', 'customertaskcovered', 'availability', 'ownedpresence']:
        sa.Enum(name=name).drop(bind, checkfirst=True)

