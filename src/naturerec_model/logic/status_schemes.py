"""
Conservation status scheme business logic
"""

from functools import singledispatch
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, StatusScheme


def create_status_scheme(name):
    """
    Create a new species conservation status scheme

    :param name: Scheme name
    :returns: An instance of the StatusScheme class for the created record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the status scheme is a duplicate
    """

    try:
        with Session.begin() as session:
            scheme = StatusScheme(name=name.strip() if name else None)
            session.add(scheme)
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate conservation status scheme name") from e

    return scheme


@singledispatch
def get_status_scheme(_):
    """
    Return the StatusScheme instance for the scheme with the specified identifier

    :param _: Scheme name or ID
    :return: Instance of the scheme
    :raises ValueError: If the scheme doesn't exist
    """
    raise TypeError("Invalid parameter type")


@get_status_scheme.register(str)
def _(name):
    try:
        with Session.begin() as session:
            scheme = session.query(StatusScheme).filter(StatusScheme.name == name).one()
    except NoResultFound as e:
        raise ValueError("Conservation status scheme not found") from e

    return scheme


@get_status_scheme.register(int)
def _(status_scheme_id):
    with Session.begin() as session:
        scheme = session.query(StatusScheme).get(status_scheme_id)

    if scheme is None:
        raise ValueError("Conservation status scheme not found")

    return scheme


def list_status_schemes():
    """
    List all the conservation status schemes in the database

    :return: A list of StatusScheme instances
    """
    with Session.begin() as session:
        schemes = session.query(StatusScheme).order_by(db.asc(StatusScheme.name)).all()
    return schemes
