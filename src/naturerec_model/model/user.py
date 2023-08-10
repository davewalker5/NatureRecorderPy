from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .user_role import UserRole


class User(UserMixin, Base):
    """
    Class representing an application user
    """
    __tablename__ = "Users"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Username
    username = Column(String, unique=True, nullable=False)
    #: Salt used in password hashing
    salt = Column(String, nullable=False)
    #: Hashed password
    password = Column(String, nullable=False)
    #: Audit columns
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    date_updated = Column(DateTime, nullable=False)

    # Roles for the current user
    roles = relationship("Role", secondary=UserRole, lazy=False)

    __table_args__ = (UniqueConstraint('username', name='USER_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(username)) > 0"),
                      CheckConstraint("LENGTH(TRIM(password)) > 0"),
                      CheckConstraint("LENGTH(TRIM(salt)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, username={self.username!r}, salt={self.salt!r}," \
               f"password={self.password!r})"
