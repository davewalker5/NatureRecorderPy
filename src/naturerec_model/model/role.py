from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint, DateTime
from .base import Base


class Role(Base):
    """
    Class representing an application role
    """
    __tablename__ = "Roles"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Role Name
    name = Column(String, unique=True, nullable=False)
    #: Audit columns
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    date_updated = Column(DateTime, nullable=False)

    __table_args__ = (UniqueConstraint('name', name='ROLE_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, username={self.name!r})"
