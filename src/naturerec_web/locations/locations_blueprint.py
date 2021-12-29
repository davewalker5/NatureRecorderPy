"""
The locations blueprint supplies view functions and templates for location management
"""

import pgeocode
import pandas as pd
from flask import Blueprint, render_template, request, redirect
from naturerec_model.logic import list_locations, get_location, create_location, update_location


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
                                    _get_posted_float("latitude"),
                                    _get_posted_float("longitude"))
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
            return _render_location_editing_page(location_id, e)
    else:
        return _render_location_editing_page(location_id, None)


@locations_bp.route("/geocode/<postcode>")
def geocode(postcode):
    """
    Query a postcode and return the latitude and longitude

    :param postcode: Postcode to query
    :return: Dictionary containing the latitude and longitude for the postcode
    """
    result = {"latitude": "", "longitude": ""}

    try:
        # Currently only implemented for UK postcodes : Other countries to follow
        nomi = pgeocode.Nominatim("gb")
        geocode_sr = nomi.query_postal_code(postcode)
        if not pd.isnull(geocode_sr.latitude) and not pd.isnull(geocode_sr.longitude):
            result["latitude"] = round(geocode_sr.latitude, 6)
            result["longitude"] = round(geocode_sr.longitude, 6)
    except ValueError:
        # Already set up the default dictionary, above, so nothing to do here
        pass

    return result
