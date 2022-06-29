"""drop login_type column

Revision ID: cf00f84268e6
Revises: 64db3ddaf49e
Create Date: 2022-06-29 20:32:50.599846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cf00f84268e6"
down_revision = "64db3ddaf49e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("users", "login_type")


def downgrade() -> None:
    op.add_column("users", sa.Column("login_type", sa.String(10), nullable=False))
