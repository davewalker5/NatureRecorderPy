"""add species scientific name

Revision ID: b8960906cfcb
Revises: 5ce1dfff9cd4
Create Date: 2024-10-29 03:04:18.463075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8960906cfcb'
down_revision = '5ce1dfff9cd4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Species', sa.Column('Scientific_Name', sa.Text, nullable=True))


def downgrade() -> None:
    op.drop_column('Species', 'Scientific_Name')
