from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey
from .base import Base


UserRole = Table(
    "UserRoles",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("Users.id")),
    Column("role_id", Integer, ForeignKey("Roles.id")),
    Column('created_by', Integer, nullable=False),
    Column('date_created', DateTime, nullable=False))
