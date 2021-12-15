"""
Category business logic
"""

from functools import singledispatch
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, Category


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
            category = Category(name=name.strip() if name else None)
            session.add(category)
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
    raise TypeError("Invalid parameter type for get_airline")


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
