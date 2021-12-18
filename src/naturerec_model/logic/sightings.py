"""
Sightings business logic
"""

import sqlalchemy as db
from sqlalchemy.exc import IntegrityError
from ..model import Session, Sighting


def create_sighting(location_id, species_id, date, number, gender, with_young):
    """
    Create a new sighting

    :param location_id: ID for the location where the sighting was made
    :param species_id: ID for the species sighted
    :param date: Date of the sighting
    :param number: Number of individuals seen
    :param gender: Gender of the individuals seen
    :param with_young: Whether or not young were seen
    :return: An instance of the Sighting class for the created record
    """
    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            formatted_date_string = date.strftime(Sighting.DATE_FORMAT)
            existing = session.query(Sighting)\
                .filter(Sighting.locationId == location_id,
                        Sighting.speciesId == species_id,
                        Sighting.date == formatted_date_string)\
                .all()
            if len(existing):
                raise ValueError("Duplicate sighting found")

            sighting = Sighting(locationId=location_id,
                                speciesId=species_id,
                                sighting_date=date,
                                number=number,
                                gender=gender,
                                withYoung=with_young)
            session.add(sighting)
    except IntegrityError as e:
        raise ValueError("Invalid sighting properties") from e

    return sighting


def get_sighting(sighting_id):
    """
    Return the sighting with the specified ID

    :param sighting_id: ID for the sighting to return
    :returns: Instance of Sighting for the record with the specified ID
    """
    with Session.begin() as session:
        sighting = session.query(Sighting).get(sighting_id)

        if sighting is None:
            raise ValueError("Sighting not found")

    return sighting


def list_sightings(from_date=None, to_date=None, location_id=None, species_id=None):
    """
    Return a list of sightings matching the specified criteria

    :param from_date: Minimum sighting date or None for all sightings
    :param to_date: Maximum sighting date or None for all sightings
    :param location_id: Location at which sightings were made or None for all sightings
    :param species_id: Sighted species or None for all sightings
    :return: A list of sightings matching the specified criteria
    """
    with Session.begin() as session:
        query = session.query(Sighting)

        if from_date:
            from_date_string = from_date.strftime(Sighting.DATE_FORMAT)
            query = query.filter(Sighting.date >= from_date_string)

        if to_date:
            to_date_string = to_date.strftime(Sighting.DATE_FORMAT)
            query = query.filter(Sighting.date <= to_date_string)

        if location_id:
            query = query.filter(Sighting.locationId == location_id)

        if species_id:
            query = query.filter(Sighting.speciesId == species_id)

        sightings = query.order_by(db.asc(Sighting.date)).all()

    return sightings
