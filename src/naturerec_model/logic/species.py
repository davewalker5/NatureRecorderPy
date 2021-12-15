"""
Species business logic
"""

from functools import singledispatch
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Species


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
            species = Species(categoryId=category_id, name=name.strip() if name else None)
            session.add(species)
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
