from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class StatusRating(Base):
    """
    Class representing the a conservation status scheme rating
    """
    __tablename__ = "StatusRatings"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Parent scheme Id
    statusSchemeId = Column(Integer, ForeignKey("StatusSchemes.id"), nullable=False)
    #: Rating name
    name = Column(String, nullable=False)
    #: Audit columns
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)

    #: Parent scheme instance
    scheme = relationship("StatusScheme", back_populates="ratings", lazy="joined")

    __table_args__ = (UniqueConstraint('statusSchemeId', 'name', name='RATING_SCHEME_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, statusSchemeId={self.statusSchemeId!r}, name={self.name!r})"
