from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class SpeciesStatusRating(Base):
    """
    Class representing the a conservation status scheme rating
    """
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DISPLAY_DATE_FORMAT = "%d/%m/%Y"
    IMPORT_DATE_FORMAT = "%d/%m/%Y"

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
    #: Start date for the rating. The database is shared between .NET and Python code and Entity Framework
    #: creates a TEXT column in SQLite where data's written in the form YYYY-MM-DD HH:MM:SS. So, while
    #: this field is the one that's persisted to the DB the intention is that it should be accessed via
    #: the corresponding property
    start = Column(String, nullable=False)
    #: End date for the rating - see comments about the start date
    end = Column(String, nullable=True)
    #: Audit columns
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    date_updated = Column(DateTime, nullable=False)

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

    @property
    def start_date(self):
        return datetime.strptime(self.start, self.DATE_FORMAT).date()

    @start_date.setter
    def start_date(self, value):
        self.start = value.strftime(self.DATE_FORMAT) if value else None

    @property
    def end_date(self):
        return datetime.strptime(self.end, self.DATE_FORMAT).date() if self.end is not None else None

    @end_date.setter
    def end_date(self, value):
        self.end = value.strftime(self.DATE_FORMAT) if value else None

    @property
    def display_start_date(self):
        return self.start_date.strftime(self.DISPLAY_DATE_FORMAT)

    @property
    def display_end_date(self):
        date = self.end_date
        return date.strftime(self.DISPLAY_DATE_FORMAT) if date else None
