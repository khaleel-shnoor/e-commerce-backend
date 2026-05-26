"""Add 'pending' value to productstatus enum for product approval workflow.

Revision ID: 20260526_004
Revises: 20260518_003
Create Date: 2026-05-26
"""

from typing import Sequence, Union

from alembic import op

revision: str = "20260526_004"
down_revision: Union[str, None] = "20260518_003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # asyncpg serializes Python str-enums by .name (uppercase), so the PostgreSQL
    # enum values mirror the Python enum member names, not their lowercase .value.
    # Existing members are DRAFT, ACTIVE, INACTIVE, ARCHIVED (uppercase).
    op.execute("ALTER TYPE productstatus ADD VALUE IF NOT EXISTS 'PENDING'")


def downgrade() -> None:
    # PostgreSQL does not support removing enum values; downgrade is a no-op.
    # To fully revert, recreate the type without 'pending' and migrate the column.
    pass
