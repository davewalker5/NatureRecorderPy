"""
Species business logic
"""

from functools import singledispatch
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Species


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


def create_species(category_id, name):
    """
    Create a new species for a specified category

    :param category_id: Category ID
    :param name: Species name
    :returns: An instance of the Species class for the created record
    :raises ValueError: If the species is a duplicate or has an invalid name
    """

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            if len(_check_for_existing_records(session, category_id, name.strip() if name else None)):
                raise ValueError("Duplicate category found")

            species = Species(categoryId=category_id, name=name.strip() if name else None)
            session.add(species)
    except IntegrityError as e:
        raise ValueError("Missing category or invalid or duplicate species name") \
            from e

    return species


def update_species(species_id, category_id, name):
    """
    Update an existing species

    :param species_id: ID of the species record to updated
    :param category_id: Category ID
    :param name: Species name
    :returns: An instance of the Species class for the updated record
    :raises ValueError: If the species is a duplicate or has an invalid name
    """
    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            species_ids = _check_for_existing_records(session, category_id, name)

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
            species.name = name.strip() if name else None
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
