from sqlalchemy import Column, Integer, Date, UniqueConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base
from .gender import Gender


class Sighting(Base):
    """
    Class representing a sighting of a species at a location
    """
    __tablename__ = "Sightings"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Related location id
    locationId = Column(Integer, ForeignKey("Locations.id"), nullable=False)
    #: Related species id
    speciesId = Column(Integer, ForeignKey("Species.id"), nullable=False)
    #: Date of the sighting
    date = Column(Date, nullable=False)
    #: Number of individuals seen
    number = Column(Integer, default=0, nullable=False)
    #: Whether or not young were seen
    withYoung = Column(Integer, default=0, nullable=False)
    #: Number of individuals seen
    gender = Column(Integer, default=Gender.UNKNOWN, nullable=False)

    #: Related location instance
    location = relationship("Location", lazy="joined")
    #: Related species instance
    species = relationship("Species", lazy="joined")

    __table_args__ = (UniqueConstraint('locationId', 'speciesId', 'date', name='SIGHTING_LOCATION_SPECIES_UX'),
                      CheckConstraint(gender.in_([Gender.UNKNOWN, Gender.MALE, Gender.FEMALE, Gender.BOTH])))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, " \
               f"locationId={self.locationId!r}, " \
               f"speciesId={self.speciesId!r}, " \
               f"date={self.date!r}, " \
               f"number={self.number!r}, " \
               f"withYoung={self.withYoung!r}, " \
               f"gender={self.gender!r})"
