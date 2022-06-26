"""create users table

Revision ID: be0107f17bb3
Revises: 
Create Date: 2022-06-26 16:57:27.983228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "be0107f17bb3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("login_type", sa.String(10), nullable=False),
        sa.Column("password", sa.String(60), nullable=False),
        sa.Column("nickname", sa.String(50), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("phone_number", sa.String(15), nullable=False),
    )

    op.create_unique_constraint("uq_user_email", "users", ["email"])


def downgrade() -> None:
    op.drop_table("users")
