from sqlalchemy import Column, Integer, Float, String, UniqueConstraint, CheckConstraint
from .base import Base


class Location(Base):
    """
    Class representing the location where a sighting was made
    """
    __tablename__ = "Locations"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Location name
    name = Column(String, nullable=False, unique=True)
    #: Address
    address = Column(String, nullable=True)
    #: City
    city = Column(String, nullable=True)
    #: County
    county = Column(String, nullable=False)
    #: Postcode
    postcode = Column(String, nullable=True)
    #: Country
    country = Column(String, nullable=False)
    #: Latitude
    latitude = Column(Float, nullable=True)
    #: Longitude
    longitude = Column(Float, nullable=True)

    __table_args__ = (UniqueConstraint('name', name='LOCATION_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"),
                      CheckConstraint("LENGTH(TRIM(county)) > 0"),
                      CheckConstraint("LENGTH(TRIM(country)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"address={self.address!r}, " \
               f"address={self.city!r}, " \
               f"address={self.county!r}, " \
               f"address={self.postcode!r}, " \
               f"address={self.country!r}, " \
               f"address={self.latitude!r}, " \
               f"address={self.longitude!r})"
