"""
The status blueprint supplies view functions and templates for conservation status scheme management
"""

from flask import Blueprint, render_template, request, redirect
from naturerec_model.logic import list_status_schemes, get_status_scheme, create_status_scheme, update_status_scheme
from naturerec_model.logic import create_status_rating, update_status_rating


status_bp = Blueprint("status", __name__, template_folder='templates')


def _render_status_scheme_editing_page(status_scheme_id, error):
    """
    Helper to render the consevation status scheme editing page

    :param status_scheme_id: ID for the conservation status scheme to edit or None for addition
    :param error: Error message to display on the page or None
    :return: The rendered editing template
    """
    status_scheme = get_status_scheme(status_scheme_id) if status_scheme_id else None
    return render_template("status/edit_scheme.html",
                           status_scheme=status_scheme,
                           edit_enabled=True,
                           error=error)


def _render_status_rating_editing_page(status_scheme_id, status_rating_id, error):
    """
    Helper to render the consevation status rating editing page

    :param status_scheme_id: ID for the parent conservation status scheme
    :param status_rating_id: ID for the conservation status rating to edit or None for addition
    :param error: Error message to display on the page or None
    :return: The rendered editing template
    """
    status_scheme = get_status_scheme(status_scheme_id) if status_scheme_id else None
    matching_ratings = [rating for rating in status_scheme.ratings if rating.id == status_rating_id]
    status_rating = matching_ratings[0] if matching_ratings else None
    return render_template("status/edit_rating.html",
                           status_scheme_id=status_scheme.id if status_scheme else None,
                           status_rating=status_rating,
                           edit_enabled=True,
                           error=error)


@status_bp.route("/list")
def list_all():
    """
    Show the page that lists all conservation status schemes and is the entry point for adding new ones

    :return: The HTML for the listing page
    """
    return render_template("status/list.html",
                           status_schemes=list_status_schemes(),
                           edit_enabled=True)


@status_bp.route("/edit", defaults={"status_scheme_id": None}, methods=["GET", "POST"])
@status_bp.route("/edit/<int:status_scheme_id>", methods=["GET", "POST"])
def edit_scheme(status_scheme_id):
    """
    Serve the page to add new conservation status rating or edit an existing one and handle the appropriate action
    when the form is submitted

    :param status_scheme_id: ID for a conservation status scheme to edit or None to create a new one
    :return: The HTML for the data entry page or a response object redirecting to the scheme list page
    """
    if request.method == "POST":
        try:
            if status_scheme_id:
                _ = update_status_scheme(status_scheme_id, request.form["name"])
            else:
                _ = create_status_scheme(request.form["name"])
            return redirect("/status/list")
        except ValueError as e:
            return _render_status_scheme_editing_page(status_scheme_id, e)
    else:
        return _render_status_scheme_editing_page(status_scheme_id, None)


@status_bp.route("/add_rating/<int:status_scheme_id>", defaults={"status_rating_id": None}, methods=["GET", "POST"])
@status_bp.route("/edit_rating/<int:status_scheme_id>/<int:status_rating_id>", methods=["GET", "POST"])
def edit_rating(status_scheme_id, status_rating_id):
    """
    Serve the page to add new species or edit an existing one and handle the appropriate action
    when the form is submitted

    :param status_scheme_id: ID for the parent conservation status scheme
    :param status_rating_id: ID for a conservation status rating to edit or None to create a new one
    :return: The HTML for the data entry page or a response object redirecting to the scheme list page
    """
    if request.method == "POST":
        try:
            if status_rating_id:
                _ = update_status_rating(status_rating_id, request.form["name"])
            else:
                _ = create_status_rating(status_scheme_id, request.form["name"])
            return redirect(f"/status/edit/{status_scheme_id}")
        except ValueError as e:
            return _render_status_rating_editing_page(status_scheme_id, status_rating_id, e)
    else:
        return _render_status_rating_editing_page(status_scheme_id, status_rating_id, None)
