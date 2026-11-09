"""Phase 3: Create contact and enrichment engine tables

Revision ID: 003_phase3_enrichment
Revises: 002_phase2_opportunity
Create Date: 2026-11-03

Creates:
- contacts
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = '003_phase3_enrichment'
down_revision: Union[str, None] = '002_phase2_opportunity'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Enums ───────────────────────────────────────────────────
    role_level_enum = sa.Enum(
        'EXECUTIVE',
        'MANAGEMENT',
        'TECHNICAL',
        'MARKETING',
        'STAFF',
        'GENERAL_INBOX',
        name='rolelevel'
    )
    role_level_enum.create(op.get_bind(), checkfirst=True)

    email_verification_status_enum = sa.Enum(
        'VERIFIED',
        'UNVERIFIED',
        'ROLE_BASED',
        'CATCH_ALL',
        'DISPOSABLE',
        'INVALID',
        name='emailverificationstatus'
    )
    email_verification_status_enum.create(op.get_bind(), checkfirst=True)

    # ── contacts ────────────────────────────────────────────────
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(200), nullable=True),
        sa.Column('first_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=True),
        sa.Column('job_title', sa.String(200), nullable=True),
        sa.Column('role_level', role_level_enum, nullable=False, server_default='GENERAL_INBOX'),
        sa.Column('email', sa.String(320), nullable=False),
        sa.Column('email_status', email_verification_status_enum, nullable=False, server_default='UNVERIFIED'),
        sa.Column('verification_score', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('has_valid_mx', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_role_based', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_disposable', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('linkedin_url', sa.String(500), nullable=True),
        sa.Column('source_method', sa.String(100), nullable=False, server_default='website_scrape'),
        sa.Column('source_url', sa.String(1000), nullable=True),
        sa.Column('verification_details', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_contacts_business', 'contacts', ['business_id'])
    op.create_index('ix_contacts_email', 'contacts', ['email'])
    op.create_index('ix_contacts_status', 'contacts', ['email_status'])
    op.create_index('ix_contacts_role', 'contacts', ['role_level'])


def downgrade() -> None:
    op.drop_table('contacts')

    for enum_name in ['rolelevel', 'emailverificationstatus']:
        op.execute(f'DROP TYPE IF EXISTS {enum_name}')

