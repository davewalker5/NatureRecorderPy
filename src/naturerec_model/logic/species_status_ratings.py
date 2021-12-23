"""
Species conservation status rating business logic
"""

import sqlalchemy as db
import datetime
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
    if start and start > datetime.datetime.now().date():
        raise ValueError("Cannot create a conservation status rating starting in the future")

    try:
        with Session.begin() as session:
            # Get the rating so we have the scheme ID
            status_rating = session.query(StatusRating).get(status_rating_id)
            if status_rating is None:
                raise ValueError("Status rating not found")

            # Find the overlapping ratings for this species and scheme
            today = datetime.datetime.today().date()
            today_string = today.strftime(SpeciesStatusRating.DISPLAY_DATE_FORMAT)
            overlapping = session.query(SpeciesStatusRating)\
                .filter(SpeciesStatusRating.speciesId == species_id,
                        SpeciesStatusRating.rating.has(StatusRating.statusSchemeId == status_rating.statusSchemeId),
                        SpeciesStatusRating.region == region,
                        db.or_(
                            SpeciesStatusRating.end == None,
                            SpeciesStatusRating.end >= today_string
                        ))\
                .all()

            # Mark overlapping ratings as ending today
            for rating in overlapping:
                rating.end_date = today

            # Add the new rating
            species_rating = SpeciesStatusRating(speciesId=species_id,
                                                 statusRatingId=status_rating_id,
                                                 region=region,
                                                 start_date=start,
                                                 end_date=end)
            session.add(species_rating)
    except IntegrityError as e:
        raise ValueError("Invalid species conservation status rating properties") from e

    return species_rating


def close_species_status_rating(species_status_rating_id):
    """
    Set the end date for a species conservation rating to today

    :param species_status_rating_id: ID for the rating to close
    """
    with Session.begin() as session:
        rating = session.query(SpeciesStatusRating).get(species_status_rating_id)
        if rating is None:
            raise ValueError("Species conservation status rating not found")

        rating.end_date = datetime.datetime.today().date()


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
