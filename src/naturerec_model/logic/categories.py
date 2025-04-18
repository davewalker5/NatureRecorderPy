"""
Category business logic
"""

from functools import singledispatch
import sqlalchemy as db
from datetime import datetime as dt
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Category, Species
from .naming import tidy_string, Casing

def _check_for_existing_records(session, name):
    """
    Return the IDs for existing records with the specified name

    :param session: SQLAlchemy session on which to perform the query
    :param name: Name for the category to match
    :returns: A collection of category IDs for the matching records
    """
    categories = session.query(Category).filter(Category.name == name).all()
    return [category.id for category in categories]


def create_category(name, supports_gender, user):
    """
    Create a new species category

    :param name: Category name
    :param supports_gender: True if the category supports entry of gender against sightings
    :param user: Current user
    :returns: An instance of the Category class for the created record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the category is a duplicate
    """

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied = tidy_string(name, Casing.TITLE_CASE)
            if len(_check_for_existing_records(session, tidied)):
                raise ValueError("Duplicate category found")

            category = Category(name=tidied,
                                supports_gender=supports_gender,
                                created_by=user.id,
                                updated_by=user.id,
                                date_created=dt.utcnow(),
                                date_updated=dt.utcnow())
            session.add(category)
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate category name") from e

    return category


def update_category(category_id, name, supports_gender, user):
    """
    Update an existing species category

    :param category_id: ID for the category record to update
    :param name: Category name
    :param supports_gender: True if the category supports entry of gender against sightings
    :param user: Current user
    :returns: An instance of the Category class for the updated record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the category is a duplicate
    """

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied = tidy_string(name, Casing.TITLE_CASE)
            category_ids = _check_for_existing_records(session, tidied)

            # Remove the current category from the list, if it's there
            if category_id in category_ids:
                category_ids.remove(category_id)

            # If there's anything left, this is going to be a duplicate
            if len(category_ids):
                raise ValueError("Duplicate category found")

            category = session.query(Category).get(category_id)

            if category is None:
                raise ValueError("Category not found")

            category.name = tidied
            category.supports_gender = supports_gender
            category.updated_by = user.id
            category.date_updated = dt.utcnow()
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate category name") from e

    return category


@singledispatch
def get_category(_):
    """
    Return the Category instance for the category with the specified identifier

    :param _: Category name or ID
    :return: Instance of the category
    :raises ValueError: If the category doesn't exist
    """
    raise TypeError("Invalid parameter type")


@get_category.register(str)
def _(name):
    try:
        with Session.begin() as session:
            category = session.query(Category).filter(Category.name == name).one()
    except NoResultFound as e:
        raise ValueError("Category not found") from e

    return category


@get_category.register(int)
def _(category_id):
    with Session.begin() as session:
        category = session.query(Category).get(category_id)

    if category is None:
        raise ValueError("Category not found")

    return category


def list_categories():
    """
    List all the categories in the database

    :return: A list of Category instances
    """
    with Session.begin() as session:
        categories = session.query(Category).order_by(db.asc(Category.name)).all()
    return categories


def delete_category(category_id):
    """
    Delete a category

    :param category_id: ID of the category to delete
    :raises ValueError: If the category doesn't exist
    :raises ValueError: If the category has sightings
    """
    with Session.begin() as session:
        # Get the category instance
        category = session.query(Category).get(category_id)
        if not category:
            raise ValueError("Species not found")

        # Check there are no species assigned to it
        species = session.query(Species)\
            .filter(Species.categoryId == category_id)\
            .limit(1)\
            .all()

        if len(species) > 0:
            raise ValueError("Cannot delete a category that has species assigned to it")

        # Delete the category
        session.delete(category)
