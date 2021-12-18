"""
Sightings business logic
"""

import sqlalchemy as db
from sqlalchemy.exc import IntegrityError
from ..model import Session, Sighting


def _check_for_existing_records(session, location_id, species_id, date):
    """
    Return the number of existing records with the specified location, species and date

    :param session: SQLAlchemy session on which to perform the query
    :param location_id: ID for the location to match
    :param species_id: ID for the species to match
    :param date: Sighting date to match
    :returns: A collection of sighting IDs for the matching records
    """
    formatted_date_string = date.strftime(Sighting.DATE_FORMAT)
    sightings = session.query(Sighting) \
        .filter(Sighting.locationId == location_id,
                Sighting.speciesId == species_id,
                Sighting.date == formatted_date_string) \
        .all()

    return [sighting.id for sighting in sightings]


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
            if len(_check_for_existing_records(session, location_id, species_id, date)):
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


def update_sighting(sighting_id, location_id, species_id, date, number, gender, with_young):
    """
    Update an existing sighting

    :param sighting_id: ID for the sighting to update
    :param location_id: ID for the location where the sighting was made
    :param species_id: ID for the species sighted
    :param date: Date of the sighting
    :param number: Number of individuals seen
    :param gender: Gender of the individuals seen
    :param with_young: Whether or not young were seen
    :return: An instance of the Sighting class for the updated record
    """
    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before updating a record. First, get
            # all records matching the essential criteria
            sighting_ids = _check_for_existing_records(session, location_id, species_id, date)

            # Remove the current sighting from the list, if it's there
            if sighting_id in sighting_ids:
                sighting_ids.remove(sighting_id)

            # If there's anything left, this is going to be a duplicate
            if len(sighting_ids):
                raise ValueError("Duplicate sighting found")

            sighting = session.query(Sighting).get(sighting_id)
            if sighting is None:
                raise ValueError("Sighting not found")

            sighting.sighting_date = date
            sighting.locationId = location_id
            sighting.speciesId = species_id
            sighting.number = number
            sighting.gender = gender
            sighting.withYoung = with_young
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
