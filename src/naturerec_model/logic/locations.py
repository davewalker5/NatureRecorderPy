"""
Locations business logic
"""

import sqlalchemy as db
import pandas as pd
import pgeocode
import pycountry
from functools import singledispatch
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Location, Sighting


def _check_for_existing_records(session, name):
    """
    Return the IDs for existing records with the specified name

    :param session: SQLAlchemy session on which to perform the query
    :param name: Name for the location to match
    :returns: A collection of location IDs for the matching records
    """
    locations = session.query(Location).filter(Location.name == name).all()
    return [location.id for location in locations]


def create_location(name, county, country, user, address=None, city=None, postcode=None, latitude=None, longitude=None):
    """
    Create a new location

    :param name: Location name
    :param county: County
    :param country: Country
    :param user: Current user
    :param address: Address or None
    :param city: City or None
    :param postcode: Postcode or None
    :param latitude: Latitude or None
    :param longitude: Longitude or None
    :return: An instance of the Location class for the created record
    """
    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied = " ".join(name.split()).title() if name else None
            if len(_check_for_existing_records(session, tidied)):
                raise ValueError("Duplicate location found")

            location = Location(name=tidied,
                                address=" ".join(address.split()) if address else None,
                                city=" ".join(city.split()) if city else None,
                                county=" ".join(county.split()) if county else None,
                                postcode=" ".join(postcode.split()).upper() if postcode else None,
                                country=" ".join(country.split()) if country else None,
                                latitude=latitude,
                                longitude=longitude,
                                created_by=user.id,
                                updated_by=user.id)
            session.add(location)
    except IntegrityError as e:
        raise ValueError("Invalid location properties or duplicate name") from e

    return location


def update_location(location_id, name, county, country, user, address=None, city=None, postcode=None, latitude=None,
                    longitude=None):
    """
    Update an existing new location

    :param location_id: ID for the location  to update
    :param name: Location name
    :param county: County
    :param country: Country
    :param user: Current user
    :param address: Address or None
    :param city: City or None
    :param postcode: Postcode or None
    :param latitude: Latitude or None
    :param longitude: Longitude or None
    :return: An instance of the Location class for the created record
    """
    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied = " ".join(name.split()).title() if name else None
            location_ids = _check_for_existing_records(session, tidied)

            # Remove the current location from the list, if it's there
            if location_id in location_ids:
                location_ids.remove(location_id)

            # If there's anything left, this is going to be a duplicate
            if len(location_ids):
                raise ValueError("Duplicate location found")

            location = session.query(Location).get(location_id)
            if location is None:
                raise ValueError("Location not found")

            location.name = tidied
            location.address = " ".join(address.split()) if address else None
            location.city = " ".join(city.split()) if city else None
            location.county = " ".join(county.split()) if county else None
            location.postcode = " ".join(postcode.split()).upper() if postcode else None
            location.country = " ".join(country.split()) if country else None
            location.latitude = latitude
            location.longitude = longitude
            location.updated_by = user.id
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


def geocode_postcode(postcode, country):
    """
    Given a postcode and country, return the latitude and longitude for the postcode

    :param postcode: Postcode
    :param country: Country where the postcode is located
    :return: A dictionary containing the latitude and longitude or blank if not found
    """
    # Set a default result and check we've got a postcode, at least. If not, don't bother
    # doing any further work as we're not going to get a latitude and longitude
    postcode = postcode.strip() if postcode else None
    if not postcode:
        raise ValueError("Invalid postcode for geocoding")

    # Tidy up the country name then attempt to get its 2-character country code, defaulting to
    # GB if there's an error
    try:
        tidied_country_name = " ".join(country.split()).title()
        country_code = pycountry.countries.get(name=tidied_country_name).alpha_2
    except (LookupError, AttributeError):
        raise ValueError("Invalid country for geocoding")

    # Get the geocoder instance
    try:
        nomi = pgeocode.Nominatim(country_code)
    except (AttributeError, ValueError):
        raise ValueError("Unrecognised country code for geocoding")

    # Look up the latitude and longitude for the postcode
    geocode_sr = nomi.query_postal_code(postcode)
    if pd.isnull(geocode_sr.latitude) or pd.isnull(geocode_sr.longitude):
        raise ValueError("Invalid postcode for geocoding")

    # Return a dictionary of latitude and longitude
    return {"latitude": round(geocode_sr.latitude, 6),
            "longitude": round(geocode_sr.longitude, 6)}


def delete_location(location_id):
    """
    Delete a location

    :param location_id: ID of the species to delete
    :raises ValueError: If the location doesn't exist
    :raises ValueError: If the location has sightings
    """
    with Session.begin() as session:
        # Get the species instance
        location = session.query(Location).get(location_id)
        if not location:
            raise ValueError("Location not found")

        # Check there are no sightings against it
        sightings = session.query(Sighting)\
            .filter(Sighting.locationId == location_id)\
            .limit(1)\
            .all()

        if len(sightings) > 0:
            raise ValueError("Cannot delete a location that has sightings recorded against it")

        # Delete the location
        session.delete(location)
