"""
Species business logic
"""

from functools import singledispatch
import sqlalchemy as db
from datetime import datetime as dt
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Species, Sighting, SpeciesStatusRating


def _check_for_existing_records(session, category_id, name):
    """
    Return the IDs for existing records matching the specified criteria

    :param session: SQLAlchemy session on which to perform the query
    :param category_id: ID of the species category to match
    :param name: Name for the species to match
    :returns: A collection of species IDs for the matching records
    """
    species = session.query(Species)\
        .filter(Species.categoryId == category_id,
                Species.name == name)\
        .all()
    return [s.id for s in species]


def create_species(category_id, name, scientific_name, user):
    """
    Create a new species for a specified category

    :param category_id: Category ID
    :param name: Species name
    :param name: Species scientific name
    :param user: Current user
    :returns: An instance of the Species class for the created record
    :raises ValueError: If the species is a duplicate or has an invalid name
    """

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied_name = " ".join(name.split()).title() if name else None
            tidied_scientific_name = " ".join(scientific_name.split()).title() if scientific_name else None
            if len(_check_for_existing_records(session, category_id, tidied_name)):
                raise ValueError("Duplicate category found")

            species = Species(categoryId=category_id,
                              name=tidied_name,
                              scientific_name=tidied_scientific_name,
                              created_by=user.id,
                              updated_by=user.id,
                              date_created=dt.utcnow(),
                              date_updated=dt.utcnow())
            session.add(species)
    except IntegrityError as e:
        raise ValueError("Missing category or invalid or duplicate species name") \
            from e

    return species


def update_species(species_id, category_id, name, scientific_name, user):
    """
    Update an existing species

    :param species_id: ID of the species record to updated
    :param category_id: Category ID
    :param name: Species name
    :param name: Species scientific name
    :param user: Current user
    :returns: An instance of the Species class for the updated record
    :raises ValueError: If the species is a duplicate or has an invalid name
    """
    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied_name = " ".join(name.split()).title() if name else None
            tidied_scientific_name = " ".join(scientific_name.split()).title() if scientific_name else None
            species_ids = _check_for_existing_records(session, category_id, tidied_name)

            # Remove the current category from the list, if it's there
            if species_id in species_ids:
                species_ids.remove(species_id)

            # If there's anything left, this is going to be a duplicate
            if len(species_ids):
                raise ValueError("Duplicate species found")

            species = session.query(Species).get(species_id)
            if species is None:
                raise ValueError("Species not found")

            species.categoryId = category_id
            species.name = tidied_name
            species.scientific_name = tidied_scientific_name
            species.updated_by = user.id
            species.date_updated = dt.utcnow()
    except IntegrityError as e:
        raise ValueError("Missing category or invalid or duplicate species name") \
            from e

    return species


@singledispatch
def get_species(_):
    """
    Return the Species instance for the species with the specified identifier

    :param _: Species name or ID
    :return: Instance of the species
    :raises ValueError: If the species doesn't exist
    """
    raise TypeError("Invalid parameter type")


@get_species.register(str)
def _(name):
    try:
        with Session.begin() as session:
            species = session.query(Species).filter(Species.name == name).one()
    except NoResultFound as e:
        raise ValueError("Category not found") from e

    return species


@get_species.register(int)
def _(species_id):
    with Session.begin() as session:
        species = session.query(Species).get(species_id)

    if species is None:
        raise ValueError("Category not found")

    return species


def list_species(category_id):
    """
    List all the species for the specified category

    :return: A list of Species instances
    """
    with Session.begin() as session:
        species = session.query(Species)\
            .filter(Species.categoryId == category_id)\
            .order_by(db.asc(Species.name))\
            .all()
    return species


def delete_species(species_id):
    """
    Delete a species

    :param species_id: ID of the species to delete
    :raises ValueError: If the species doesn't exist
    :raises ValueError: If the species has sightings
    """
    with Session.begin() as session:
        # Get the species instance
        species = session.query(Species).get(species_id)
        if not species:
            raise ValueError("Species not found")

        # Check there are no sightings against it
        sightings = session.query(Sighting)\
            .filter(Sighting.speciesId == species_id)\
            .limit(1)\
            .all()

        if len(sightings) > 0:
            raise ValueError("Cannot delete a species that has sightings recorded against it")

        # Delete any conservation status rating records
        statuses = session.query(SpeciesStatusRating)\
            .filter(SpeciesStatusRating.speciesId == species_id)\
            .all()
        for status in statuses:
            session.delete(status)

        # Delete the species
        session.delete(species)
