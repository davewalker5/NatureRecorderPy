"""Add columns to audit user making changes

Revision ID: 560b0df5ff2a
Revises: 5a2e355711a1
Create Date: 2023-08-04 11:33:22.238393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '560b0df5ff2a'
down_revision = '5a2e355711a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Categories', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('Categories', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('JobStatuses', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('JobStatuses', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('Locations', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('Locations', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('Sightings', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('Sightings', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('Species', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('Species', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('SpeciesStatusRatings', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('SpeciesStatusRatings', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('StatusRatings', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('StatusRatings', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('StatusSchemes', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('StatusSchemes', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))

    op.add_column('Users', sa.Column('Created_By', sa.Integer, nullable=False, server_default="0"))
    op.add_column('Users', sa.Column('Updated_By', sa.Integer, nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column('Categories', 'Created_By')
    op.drop_column('Categories', 'Updated_By')

    op.drop_column('JobStatuses', 'Created_By')
    op.drop_column('JobStatuses', 'Updated_By')

    op.drop_column('Locations', 'Created_By')
    op.drop_column('Locations', 'Updated_By')

    op.drop_column('Sightings', 'Created_By')
    op.drop_column('Sightings', 'Updated_By')

    op.drop_column('Species', 'Created_By')
    op.drop_column('Species', 'Updated_By')

    op.drop_column('SpeciesStatusRatings', 'Created_By')
    op.drop_column('SpeciesStatusRatings', 'Updated_By')

    op.drop_column('StatusRatings', 'Created_By')
    op.drop_column('StatusRatings', 'Updated_By')

    op.drop_column('StatusSchemes', 'Created_By')
    op.drop_column('StatusSchemes', 'Updated_By')

    op.drop_column('Users', 'Created_By')
    op.drop_column('Users', 'Updated_By')
