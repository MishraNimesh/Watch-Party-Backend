"""add room visibility and capacity

Revision ID: b4e64c3569be
Revises: 
Create Date: 2026-09-05 00:50:46.063139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4e64c3569be'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'rooms',
        sa.Column(
            'is_public',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.add_column(
        'rooms',
        sa.Column(
            'max_members',
            sa.Integer(),
            nullable=False,
            server_default='10'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('rooms', 'max_members')
    op.drop_column('rooms', 'is_public')