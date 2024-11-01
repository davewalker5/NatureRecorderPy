from datetime import datetime
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .gender import Gender


class Sighting(Base):
    """
    Class representing a sighting of a species at a location
    """
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_DISPLAY_FORMAT = "%d/%m/%Y"
    DATE_IMPORT_FORMAT = "%d/%m/%Y"

    __tablename__ = "Sightings"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Related location id
    locationId = Column(Integer, ForeignKey("Locations.id"), nullable=False)
    #: Related species id
    speciesId = Column(Integer, ForeignKey("Species.id"), nullable=False)
    #: Date of the sighting. The database is shared between .NET and Python code and Entity Framework
    #: creates a TEXT column in SQLite where data's written in the form YYYY-MM-DD HH:MM:SS. So, while
    #: this field is the one that's persisted to the DB the intention is that it should be accessed via
    #: the sighting_date property
    date = Column(String, nullable=False)
    #: Number of distinct individuals seen
    number = Column(Integer, default=None, nullable=True)
    #: Whether or not young were seen
    withYoung = Column(Integer, default=0, nullable=False)
    #: Number of individuals seen
    gender = Column(Integer, default=Gender.UNKNOWN, nullable=False)
    #: Sighting notes
    notes = Column(String, default=None, nullable=True)
    #: Audit columns
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    date_updated = Column(DateTime, nullable=False)

    #: Related location instance
    location = relationship("Location", lazy="joined")
    #: Related species instance
    species = relationship("Species", lazy="joined")

    __table_args__ = (UniqueConstraint('locationId', 'speciesId', 'date', name='SIGHTING_LOCATION_SPECIES_DATE_UX'),
                      CheckConstraint(gender.in_([Gender.UNKNOWN, Gender.MALE, Gender.FEMALE, Gender.BOTH])),
                      CheckConstraint(withYoung.in_([0, 1])),
                      CheckConstraint("ifnull(number, 1) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, " \
               f"locationId={self.locationId!r}, " \
               f"speciesId={self.speciesId!r}, " \
               f"date={self.date!r}, " \
               f"number={self.number!r}, " \
               f"withYoung={self.withYoung!r}, " \
               f"gender={self.gender!r}, " \
               f"notes={self.notes!r})"

    @property
    def sighting_date(self):
        return datetime.strptime(self.date, self.DATE_FORMAT).date()

    @sighting_date.setter
    def sighting_date(self, value):
        self.date = value.strftime(self.DATE_FORMAT) if value else None

    @property
    def display_date(self):
        return self.sighting_date.strftime(Sighting.DATE_DISPLAY_FORMAT)

    @property
    def gender_name(self):
        return Gender.gender_name(self.gender)

    @property
    def with_young_name(self):
        return "Yes" if self.withYoung else "No"

    @property
    def csv_columns(self):
        return [
            self.species.name,
            self.species.scientific_name,
            self.species.category.name,
            self.number,
            self.gender_name,
            self.with_young_name,
            self.display_date,
            self.location.name,
            self.location.address,
            self.location.city,
            self.location.county,
            self.location.postcode,
            self.location.country,
            self.location.latitude,
            self.location.longitude,
            self.notes
        ]
