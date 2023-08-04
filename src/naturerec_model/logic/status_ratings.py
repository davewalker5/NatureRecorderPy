"""
Conservation status scheme rating business logic
"""

from sqlalchemy.exc import IntegrityError
from ..model import Session, StatusRating, SpeciesStatusRating


def _check_for_existing_records(session, status_scheme_id, name):
    """
    Return the IDs for existing records with the specified name belonging to the specified scheme

    :param session: SQLAlchemy session on which to perform the query
    :param status_scheme_id: ID for the conservation status scheme to match
    :param name: Name for the conservation status rating to match
    :returns: A collection of conservation status rating IDs for the matching records
    """
    ratings = session.query(StatusRating)\
        .filter(StatusRating.statusSchemeId == status_scheme_id,
                StatusRating.name == name)\
        .all()
    return [rating.id for rating in ratings]


def create_status_rating(status_scheme_id, name, user):
    """
    Create a new species conservation status scheme rating

    :param status_scheme_id: ID for the conservation status scheme
    :param name: Rating name
    :param user: Current user
    :returns: An instance of the StatusRating class for the created record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the status rating is a duplicate
    """

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied = " ".join(name.split()).title() if name else None
            if len(_check_for_existing_records(session, status_scheme_id, tidied)):
                raise ValueError("Duplicate conservation status rating found")

            scheme = StatusRating(statusSchemeId=status_scheme_id, name=tidied, created_by=user.id, updated_by=user.id)
            session.add(scheme)
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate conservation status scheme rating") from e

    return scheme


def update_status_rating(status_rating_id, name, user):
    """
    Update an existing species conservation status scheme rating

    :param status_rating_id: ID for the conservation status rating
    :param name: Rating name
    :param user: Current user
    :returns: An instance of the StatusRating class for the created record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the status rating is a duplicate
    """

    try:
        with Session.begin() as session:
            rating = session.query(StatusRating).get(status_rating_id)
            if rating is None:
                raise ValueError("Conservation status scheme not found")

            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied = " ".join(name.split()).title() if name else None
            rating_ids = _check_for_existing_records(session, rating.statusSchemeId, tidied)

            # Remove the current scheme from the list, if it's there
            if status_rating_id in rating_ids:
                rating_ids.remove(status_rating_id)

            # If there's anything left, this is going to be a duplicate
            if len(rating_ids):
                raise ValueError("Duplicate conservation status scheme found")

            rating.name = tidied
            rating.updated_by = user.id
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate conservation status scheme rating") from e

    return rating


def delete_status_rating(status_rating_id):
    """
    Delete a conservation status rating

    :param status_rating_id: ID of the status rating to delete
    :raises ValueError: If the rating doesn't exist
    :raises ValueError: If there are species ratings for the status rating
    """
    with Session.begin() as session:
        # Get the status rating instance
        status_rating = session.query(StatusRating).get(status_rating_id)
        if not status_rating:
            raise ValueError("Conservation status rating not found")

        # Check there are no species ratings against it
        species_status_ratings = session.query(SpeciesStatusRating)\
            .filter(SpeciesStatusRating.statusRatingId == status_rating_id)\
            .limit(1)\
            .all()

        if len(species_status_ratings) > 0:
            raise ValueError("Cannot delete a conservation status rating that has species ratings recorded against it")

        # Delete the rating
        session.delete(status_rating)
