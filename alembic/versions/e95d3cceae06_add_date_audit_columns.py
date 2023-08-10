"""Added created/updated dates to the audit columns

Revision ID: e95d3cceae06
Revises: 560b0df5ff2a
Create Date: 2023-08-05 08:37:11.894275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e95d3cceae06'
down_revision = '560b0df5ff2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Categories', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('Categories', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('JobStatuses', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('JobStatuses', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('Locations', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('Locations', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('Sightings', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('Sightings', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('Species', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('Species', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('SpeciesStatusRatings', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('SpeciesStatusRatings', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('StatusRatings', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('StatusRatings', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('StatusSchemes', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('StatusSchemes', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))

    op.add_column('Users', sa.Column('Date_Created', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))
    op.add_column('Users', sa.Column('Date_Updated', sa.DateTime, nullable=False, server_default="1994-01-01 00:00:00"))


def downgrade() -> None:
    op.drop_column('Categories', 'Date_Created')
    op.drop_column('Categories', 'Date_Updated')

    op.drop_column('JobStatuses', 'Date_Created')
    op.drop_column('JobStatuses', 'Date_Updated')

    op.drop_column('Locations', 'Date_Created')
    op.drop_column('Locations', 'Date_Updated')

    op.drop_column('Sightings', 'Date_Created')
    op.drop_column('Sightings', 'Date_Updated')

    op.drop_column('Species', 'Date_Created')
    op.drop_column('Species', 'Date_Updated')

    op.drop_column('SpeciesStatusRatings', 'Date_Created')
    op.drop_column('SpeciesStatusRatings', 'Date_Updated')

    op.drop_column('StatusRatings', 'Date_Created')
    op.drop_column('StatusRatings', 'Date_Updated')

    op.drop_column('StatusSchemes', 'Date_Created')
    op.drop_column('StatusSchemes', 'Date_Updated')

    op.drop_column('Users', 'Date_Created')
    op.drop_column('Users', 'Date_Updated')
