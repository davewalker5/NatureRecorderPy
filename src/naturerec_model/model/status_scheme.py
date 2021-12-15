from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class StatusScheme(Base):
    """
    Class representing a conservation status scheme
    """
    __tablename__ = "StatusSchemes"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Scheme name
    name = Column(String, nullable=False, unique=True)

    #: Ratings associated with this conservation status scheme
    ratings = relationship("StatusRating",
                           back_populates="scheme",
                           cascade="all, delete, delete-orphan",
                           lazy="joined")

    __table_args__ = (UniqueConstraint('name', name='STATUS_SCHEME_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, name={self.name!r})"
