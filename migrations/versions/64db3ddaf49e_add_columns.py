"""add columns

Revision ID: 64db3ddaf49e
Revises: be0107f17bb3
Create Date: 2022-06-28 22:58:00.958836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "64db3ddaf49e"
down_revision = "be0107f17bb3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "created_at", sa.DateTime, server_default=sa.func.current_timestamp()
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.current_timestamp(),
            onupdate=sa.func.now(),
        ),
    )
    op.add_column("users", sa.Column("deleted_at", sa.DateTime, nullable=True))


def downgrade() -> None:
    pass
