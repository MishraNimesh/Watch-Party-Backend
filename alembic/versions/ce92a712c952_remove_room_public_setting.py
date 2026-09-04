"""remove room public setting

Revision ID: ce92a712c952
Revises: b4e64c3569be
Create Date: 2026-09-05 01:04:05.653182
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ce92a712c952"
down_revision = "b4e64c3569be"
branch_labels = None
depends_on = None
def upgrade() -> None:
    op.drop_column("rooms", "is_public")


def downgrade() -> None:
    op.add_column(
        "rooms",
        sa.Column(
            "is_public",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )