"""Added 'supports gender' category flag

Revision ID: 2cdd34308ad3
Revises: b8960906cfcb
Create Date: 2025-02-20 09:27:58.112087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cdd34308ad3'
down_revision = 'b8960906cfcb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Categories', sa.Column('Supports_Gender', sa.Integer, nullable=False, server_default="1"))


def downgrade() -> None:
    op.drop_column('Categories', 'Supports_Gender')
