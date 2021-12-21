"""
Category business logic
"""

from functools import singledispatch
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Category


def _check_for_existing_records(session, name):
    """
    Return the IDs for existing records with the specified name

    :param session: SQLAlchemy session on which to perform the query
    :param name: Name for the category to match
    :returns: A collection of category IDs for the matching records
    """
    categories = session.query(Category).filter(Category.name == name).all()
    return [category.id for category in categories]


def create_category(name):
    """
    Create a new species category

    :param name: Category name
    :returns: An instance of the Category class for the created record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the category is a duplicate
    """

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            if len(_check_for_existing_records(session, name.strip() if name else None)):
                raise ValueError("Duplicate category found")

            category = Category(name=name.strip() if name else None)
            session.add(category)
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate category name") from e

    return category


def update_category(category_id, name):
    """
    Update an existing species category

    :param category_id: ID for the category record to update
    :param name: Category name
    :returns: An instance of the Category class for the updated record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the category is a duplicate
    """

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            category_ids = _check_for_existing_records(session, name)

            # Remove the current category from the list, if it's there
            if category_id in category_ids:
                category_ids.remove(category_id)

            # If there's anything left, this is going to be a duplicate
            if len(category_ids):
                raise ValueError("Duplicate category found")

            category = session.query(Category).get(category_id)

            if category is None:
                raise ValueError("Category not found")

            category.name = name.strip() if name else None
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
