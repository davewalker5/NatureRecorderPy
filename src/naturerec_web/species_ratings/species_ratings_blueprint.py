"""
The species ratings blueprint supplies view functions and templates for species conservation status rating management
"""

from flask import Blueprint, render_template, request
from naturerec_model.logic import list_species_status_ratings, close_species_status_rating


species_ratings_bp = Blueprint("species_ratings", __name__, template_folder='templates')


def _get_posted_int(key):
    """
    Retrieve a named integer value from the POSTed filtering form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key]
    return int(value) if value else None


@species_ratings_bp.route("/list_status/<int:species_id>", methods=["GET", "POST"])
def list_status_ratings(species_id):
    """
    Show the page that lists species status ratings and handles "closing" of a rating by setting its end date to
    today

    :param species_id: ID for the species for which to list ratings
    :return: The HTML for the species conservation status rating listing page
    """
    error = None
    if request.method == "POST":
        try:
            close_species_status_rating(_get_posted_int("species_status_rating_id"))
        except ValueError as e:
            error = e

    ratings = list_species_status_ratings(species_id=species_id)
    return render_template("species_ratings/list.html",
                           species_status_ratings=ratings,
                           error=error,
                           edit_enabled=True)
