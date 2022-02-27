"""
The locations blueprint supplies view functions and templates for location management
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from naturerec_model.logic import list_locations, get_location, create_location, update_location, geocode_postcode
from naturerec_web.request_utils import get_posted_float, get_posted_int

locations_bp = Blueprint("locations", __name__, template_folder='templates')


def _render_location_editing_page(location_id, error):
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


@locations_bp.route("/list", methods=["GET", "POST"])
@login_required
def list_all():
    """
    Show the page that lists all locations and is the entry point for adding new ones

    :return: The HTML for the location listing page
    """
    if request.method == "POST":
        # If a record ID has been posted back for deletion, delete it before re-rendering the list
        # with the same filtering criteria
        delete_record_id = get_posted_int("delete_record_id")
        if delete_record_id:
            pass

    return render_template("locations/list.html",
                           locations=list_locations(),
                           edit_enabled=True)


@locations_bp.route("/edit", defaults={"location_id": None}, methods=["GET", "POST"])
@locations_bp.route("/add/<int:location_id>", methods=["GET", "POST"])
@login_required
def edit(location_id):
    """
    Serve the page to add  new location or edit an existing one and handle the appropriate action
    when the form is submitted

    :param location_id: ID for a location to edit or None to create a new location
    :return: The HTML for the location entry page or a response object redirecting to the location list page
    """
    if request.method == "POST":
        try:
            if location_id:
                _ = update_location(location_id,
                                    request.form["name"],
                                    request.form["county"],
                                    request.form["country"],
                                    request.form["address"],
                                    request.form["city"],
                                    request.form["postcode"],
                                    get_posted_float("latitude"),
                                    get_posted_float("longitude"))
            else:
                _ = create_location(request.form["name"],
                                    request.form["county"],
                                    request.form["country"],
                                    request.form["address"],
                                    request.form["city"],
                                    request.form["postcode"],
                                    get_posted_float("latitude"),
                                    get_posted_float("longitude"))
            return redirect("/locations/list")
        except ValueError as e:
            return _render_location_editing_page(location_id, e)
    else:
        return _render_location_editing_page(location_id, None)


@locations_bp.route("/geocode/<postcode>", defaults={"country": "United Kingdom"})
@locations_bp.route("/geocode/<postcode>/<country>")
@login_required
def geocode(postcode, country):
    """
    Query a postcode and return the latitude and longitude

    :param postcode: Postcode to query
    :param country: Country where the postcode is located
    :return: Dictionary containing the latitude and longitude for the postcode
    """
    try:
        return geocode_postcode(postcode, country)
    except ValueError:
        return {"latitude": "", "longitude": ""}
