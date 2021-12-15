"""
Conservation status scheme rating business logic
"""

from sqlalchemy.exc import IntegrityError
from ..model import Session, StatusRating


def create_status_rating(status_scheme_id, name):
    """
    Create a new species conservation status scheme rating

    :param status_scheme_id: ID for the conservation status scheme
    :param name: Rating name
    :returns: An instance of the StatusScheme class for the created record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the status scheme is a duplicate
    """

    try:
        with Session.begin() as session:
            scheme = StatusRating(statusSchemeId=status_scheme_id, name=name.strip() if name else None)
            session.add(scheme)
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate conservation status scheme rating") from e

    return scheme
