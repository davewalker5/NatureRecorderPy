"""
Species conservation status rating business logic
"""

from sqlalchemy.exc import IntegrityError
from ..model import Session, StatusRating, SpeciesStatusRating


def create_species_status_rating(species_id, status_rating_id, region, start, end=None):
    """
    Create a species conservation status rating

    :param species_id: ID for the species
    :param status_rating_id: ID for the status rating value
    :param region: Region the rating applies to
    :param start: Start date for the rating
    :param end: End date for the rating or None
    :return: The SpeciesStatusRating instance for the record created
    """
    try:
        with Session.begin() as session:
            rating = SpeciesStatusRating(speciesId=species_id,
                                         statusRatingId=status_rating_id,
                                         region=region,
                                         start_date=start,
                                         end_date=end)
            session.add(rating)
    except IntegrityError as e:
        raise ValueError("Invalid species conservation status rating properties") from e

    return rating


def get_species_status_rating(species_status_rating_id):
    """
    Return a species conservation status rating given its ID

    :param species_status_rating_id: ID for the rating record
    :return: The SpeciesStatusRating instance for the specified record
    """
    with Session.begin() as session:
        rating = session.query(SpeciesStatusRating).get(species_status_rating_id)

    if rating is None:
        raise ValueError("Species conservation status rating not found")

    return rating


def list_species_status_ratings(scheme_id=None, species_id=None, region=None, current_only=False):
    """
    List species conservation status ratings matching the specified criteria

    :param scheme_id: ID for the status scheme or None for all schemes
    :param species_id: ID for the species or None for all species
    :param region: Region name or None for all regions
    :param current_only: If true, only current ratings are returned
    :return: A list of SpeciesStatusRating instances for records matching the
    """
    with Session.begin() as session:
        query = session.query(SpeciesStatusRating)\
            .join(SpeciesStatusRating.rating, aliased=True)

        if scheme_id:
            query = query.filter(SpeciesStatusRating.rating.has(StatusRating.statusSchemeId == scheme_id))

        if species_id:
            query = query.filter(SpeciesStatusRating.speciesId == species_id)

        if region:
            query = query.filter(SpeciesStatusRating.region == region)

        if current_only:
            query = query.filter(SpeciesStatusRating.end == None)

        ratings = query.all()

    return ratings
