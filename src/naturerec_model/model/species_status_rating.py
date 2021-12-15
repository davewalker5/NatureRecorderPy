from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class SpeciesStatusRating(Base):
    """
    Class representing the a conservation status scheme rating
    """
    __tablename__ = "SpeciesStatusRatings"
    __table_args__ = (CheckConstraint("LENGTH(TRIM(region)) > 0"),
                      CheckConstraint("(end IS NULL) or (end >= start)"))

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Related Species Id
    speciesId = Column(Integer, ForeignKey("Species.id"), nullable=False)
    #: Related Rating Id
    statusRatingId = Column(Integer, ForeignKey("StatusRatings.id"), nullable=False)
    #: Region where the rating applies
    region = Column(String, nullable=False)
    #: Start date for the rating
    start = Column(Date, nullable=False)
    #: End date for the rating
    end = Column(Date, nullable=True)

    #: Related species
    species = relationship("Species", lazy="joined")
    #: Related status rating
    rating = relationship("StatusRating", lazy="joined")

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, " \
               f"speciesId={self.speciesId!r}, " \
               f"statusRatingId={self.statusRatingId!r}, " \
               f"region={self.region!r}, " \
               f"start={self.start!r}," \
               f"end={self.end!r})"
