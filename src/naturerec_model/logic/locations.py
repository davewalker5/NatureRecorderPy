"""
Locations business logic
"""

from functools import singledispatch
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Location


def create_location(name, county, country, address=None, city=None, postcode=None, latitude=None, longitude=None):
    """
    Create a new location

    :param name: Location name
    :param county: County
    :param country: Country
    :param address: Address or None
    :param city: City or None
    :param postcode: Postcode or None
    :param latitude: Latitude or None
    :param longitude: Longitude or None
    :return: An instance of the Location class for the created record
    """
    try:
        with Session.begin() as session:
            location = Location(name=name.strip() if name else None,
                                address=address.strip() if address else None,
                                city=city.strip() if city else None,
                                county=county.strip() if county else None,
                                postcode=postcode.strip() if postcode else None,
                                country=country.strip() if country else None,
                                latitude=latitude,
                                longitude=longitude)
            session.add(location)
    except IntegrityError as e:
        raise ValueError("Invalid location properties or duplicate name") from e

    return location


@singledispatch
def get_location(_):
    """
    Return the Location instance for the location with the specified identifier

    :param _: Location name or ID
    :return: Instance of the location
    :raises ValueError: If the location doesn't exist
    """
    raise TypeError("Invalid parameter type")


@get_location.register(str)
def _(name):
    try:
        with Session.begin() as session:
            location = session.query(Location).filter(Location.name == name).one()
    except NoResultFound as e:
        raise ValueError("Location not found") from e

    return location


@get_location.register(int)
def _(category_id):
    with Session.begin() as session:
        location = session.query(Location).get(category_id)

    if location is None:
        raise ValueError("Location not found")

    return location


def list_locations(city=None, county=None, country=None):
    """

    :param city: City to filter by or None
    :param county: County to filter by or None
    :param country: Country to filter by or None
    :return: List of matching locations
    """
    with Session.begin() as session:
        query = session.query(Location)

        if city and city.strip():
            query = query.filter(Location.city == city)

        if county and county.strip():
            query = query.filter(Location.county == county)

        if country and country.strip():
            query = query.filter(Location.country == country)

        locations = query.order_by(db.asc(Location.name)).all()

    return locations