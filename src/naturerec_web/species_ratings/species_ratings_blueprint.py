"""
The species ratings blueprint supplies view functions and templates for species conservation status rating management
"""

import datetime
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from naturerec_model.logic import get_species
from naturerec_model.logic import list_status_schemes, get_status_scheme
from naturerec_model.logic import list_species_status_ratings, close_species_status_rating, \
    create_species_status_rating, delete_species_status_rating
from naturerec_web.request_utils import get_posted_int

species_ratings_bp = Blueprint("species_ratings", __name__, template_folder='templates')


def _render_rating_addition_page(species_id, error):
    """
    Helper to render the species conservation status rating page

    :param species_id: ID for the species for which to add a rating
    :param error: Error to display on the page or None
    :return: HTML for the rating page
    """
    return render_template("species_ratings/add.html",
                           schemes=list_status_schemes(),
                           species=get_species(species_id),
                           error=error)


@species_ratings_bp.route("/list_ratings/<int:species_id>", methods=["GET", "POST"])
@login_required
def list_status_ratings(species_id):
    """
    Show the page that lists species status ratings and handles "closing" of a rating by setting its end date to
    today

    :param species_id: ID for the species for which to list ratings
    :return: The HTML for the species conservation status rating listing page
    """
    error = None
    if request.method == "POST":
        error = None
        try:
            delete_record_id = get_posted_int("delete_record_id")
            if delete_record_id:
                delete_species_status_rating(delete_record_id)
            else:
                close_species_status_rating(get_posted_int("species_status_rating_id"))
        except ValueError as e:
            error = e

    return render_template("species_ratings/list.html",
                           species_status_ratings=list_species_status_ratings(species_id=species_id),
                           species=get_species(species_id),
                           error=error,
                           edit_enabled=True)


@species_ratings_bp.route("/list_scheme_ratings/<int:scheme_id>")
@login_required
def list_scheme_ratings(scheme_id):
    """
    Return the markup for the conservation status rating selector for the specified scheme

    :param scheme_id: ID for the conservation status scheme for which to list ratings
    :return: Rendered rating selection template
    """
    ratings = get_status_scheme(scheme_id).ratings if scheme_id else None
    return render_template("species_ratings/scheme_ratings.html",
                           ratings=ratings)


@species_ratings_bp.route("/add/<int:species_id>", methods=["GET", "POST"])
@login_required
def add(species_id):
    if request.method == "POST":
        try:
            _ = create_species_status_rating(species_id=species_id,
                                             status_rating_id=get_posted_int("rating"),
                                             region=request.form["region"],
                                             start=datetime.datetime.today().date())
            return redirect(f"/species_ratings/list_ratings/{species_id}")
        except ValueError as e:
            return _render_rating_addition_page(species_id, e)
    else:
        return _render_rating_addition_page(species_id, None)
