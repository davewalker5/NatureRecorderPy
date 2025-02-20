"""Add RBAC support

Revision ID: 5ce1dfff9cd4
Revises: e95d3cceae06
Create Date: 2023-08-09 18:41:32.771350

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from datetime import datetime
from naturerec_model.model import Role, User
from pprint import pprint as pp

# revision identifiers, used by Alembic.
revision = '5ce1dfff9cd4'
down_revision = 'e95d3cceae06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('Roles',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False, server_default="0"),
    sa.Column('updated_by', sa.Integer(), nullable=False, server_default="0"),
    sa.Column('date_created', sa.DateTime(), nullable=False, server_default="1994-01-01 00:00:00"),
    sa.Column('date_updated', sa.DateTime(), nullable=False, server_default="1994-01-01 00:00:00"),
    sa.CheckConstraint('LENGTH(TRIM(name)) > 0'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='ROLE_NAME_UX')
    )

    op.create_table('UserRoles',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False, server_default="0"),
    sa.Column('date_created', sa.DateTime(), nullable=False, server_default="1994-01-01 00:00:00"),
    sa.ForeignKeyConstraint(['role_id'], ['Roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Get an ORM session
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Get a list of user IDs for the current users and sort them
    users = session.query(User)
    user_ids = [user.id for user in users]
    user_ids.sort()

    # Identify the "default" user ID, accounting for the fact that there may not be any users yet
    user_id = user_ids[0] if len(user_ids) > 0 else 0

    # Create the roles, using the first user as the creator
    for name in ["Administrator", "Reporter", "Reader"]:
        session.add(Role(name=name,
                         created_by=user_id,
                         updated_by=user_id,
                         date_created=datetime.now(),
                         date_updated=datetime.now()))

    # Apply the admin role to existing users (avoids loss of functionality due to access rights)
    admin_role = session.query(Role).filter(Role.name=="Administrator").first()
    for user_id in user_ids:
        bind.execute(f"INSERT INTO UserRoles ( user_id, role_id, created_by, date_created ) "
                     f"VALUES ( {user_id}, {admin_role.id}, {user_id}, '{str(datetime.now())}')")
    session.commit()


def downgrade() -> None:
    op.drop_table('UserRoles')
    op.drop_table('Roles')
