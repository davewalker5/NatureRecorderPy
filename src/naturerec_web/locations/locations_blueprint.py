"""
The locations blueprint supplies view functions and templates for location management
"""

from flask import Blueprint, render_template, request, redirect
from naturerec_model.logic import list_locations, get_location, create_location


locations_bp = Blueprint("locations", __name__, template_folder='templates')


def _render_airport_editing_page(location_id, error):
    """
    Helper to render the location editing page

    :param location_id: ID for the location to edit or None for addition
    :param error: Error message to display on the page or None
    :return: The rendered location editing template
    """
    location = get_location(location_id) if location_id else None
    return render_template("locations/edit.html",
                           location=location,
                           error=error)


def _get_posted_float(key):
    """
    Retrieve a named float value from a POSTed form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key]
    return float(value) if value else None


@locations_bp.route("/list")
def list_all():
    """
    Show the page that lists all locations and is the entry point for adding new ones

    :return: The HTML for the location listing page
    """
    return render_template("locations/list.html",
                           locations=list_locations(),
                           edit_enabled=True)


@locations_bp.route("/edit", defaults={"location_id": None}, methods=["GET", "POST"])
@locations_bp.route("/add/<int:location_id>", methods=["GET", "POST"])
def edit(location_id):
    """
    Serve the page to add  new location or edit an existing one and handle the appropriate action
    when the form is submitted

    :param location_id: ID for a location to edit or None to create a new airport
    :return: The HTML for the location entry page or a response object redirecting to the location list page
    """
    if request.method == "POST":
        try:
            if location_id:
                pass
            else:
                _ = create_location(request.form["name"],
                                    request.form["county"],
                                    request.form["country"],
                                    request.form["address"],
                                    request.form["city"],
                                    request.form["postcode"],
                                    _get_posted_float("latitude"),
                                    _get_posted_float("longitude"))
            return redirect("/locations/list")
        except ValueError as e:
            return _render_airport_editing_page(location_id, e)
    else:
        return _render_airport_editing_page(location_id, None)
