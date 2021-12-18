"""
The sightings blueprint supplies view functions and templates for sighting management
"""

import datetime
from flask import Blueprint, render_template, request, redirect
from naturerec_model.logic import list_sightings, get_sighting, create_sighting, update_sighting
from naturerec_model.logic import list_locations
from naturerec_model.logic import list_categories
from naturerec_model.logic import list_species
from naturerec_model.model import Gender

sightings_bp = Blueprint("sightings", __name__, template_folder='templates')


def _render_sighting_editing_page(sighting_id, error):
    """
    Helper to render the sighting editing page

    :param sighting_id: ID for the sighting to edit
    :param error: Error message to display on the page or None
    :return: The rendered sighting editing template
    """
    locations = list_locations()
    categories = list_categories()
    sighting = get_sighting(sighting_id) if sighting_id else None
    return render_template("sightings/edit.html",
                           locations=locations,
                           categories=categories,
                           sighting=sighting,
                           genders=Gender.gender_map(),
                           with_young={1: "Yes", 0: "No"},
                           error=error)


def _render_sightings_list_page(from_date=None, to_date=None, location_id=None, category_id=None, species_id=None):
    """
    Helper to render the sightings list page

    :param from_date: Include sightings on or after this date
    :param to_date: Include sightings up to this date
    :param location_id: Include sightings at this location
    :param category_id: Species category for the selected species
    :param species_id: Include sightings for this species
    :return: The HTML for the rendered sightings list page
    """
    # If there aren't any filtering criteria, set the from date to today to prevent the whole database being
    # returned. Note that category isn't a direct filtering criteria - it's used in selection of the species
    if from_date is None and to_date is None and location_id is None and species_id is None:
        from_date = datetime.datetime.today().date()

    # Find matching sightings
    sightings = list_sightings(from_date=from_date,
                               to_date=to_date,
                               location_id=location_id,
                               species_id=species_id)

    # Serve the page
    return render_template("sightings/list.html",
                           from_date=from_date.strftime("%d/%m/%Y") if from_date else "",
                           to_date=to_date.strftime("%d/%m/%Y") if to_date else "",
                           location_id=location_id,
                           category_id=category_id,
                           species_id=species_id,
                           locations=list_locations(),
                           categories=list_categories(),
                           sightings=sightings,
                           edit_enabled=True)


def _get_filter_value(key):
    """
    Retrieve a named value from the POSTed filtering form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key]
    return value if value else None


def _get_filter_int(key):
    """
    Retrieve a named integer value from the POSTed filtering form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = _get_filter_value(key)
    return int(value) if value else None


def _get_filter_date(key):
    """
    Retrieve a named date value from the POSTed filtering form

    :param key: Value key
    :return: Value or None if not specified
    """
    date_string = _get_filter_value(key)
    return datetime.datetime.strptime(date_string, "%d/%m/%Y").date() if date_string else None


@sightings_bp.route("/list", methods=["GET", "POST"])
def list_filtered_sightings():
    """
    Show the page that lists today's sightings and is the entry point for adding new ones

    :return: The HTML for the sightings listing page
    """
    if request.method == "POST":
        return _render_sightings_list_page(_get_filter_date("from_date"),
                                           _get_filter_date("to_date"),
                                           _get_filter_int("location"),
                                           _get_filter_int("category"),
                                           _get_filter_int("species"))
    else:
        return _render_sightings_list_page()


@sightings_bp.route("/list_species/<int:category_id>/<int:selected_species_id>")
def list_species_for_category(category_id, selected_species_id):
    """
    Return the markup for the species selector for the specified category

    :param category_id: ID for the category for which to list species
    :param selected_species_id: ID for the species to select by default
    :return: Rendered species selection template
    """
    species = list_species(category_id)
    return render_template("sightings/species.html",
                           species=species,
                           species_id=selected_species_id)


@sightings_bp.route("/edit", defaults={"sighting_id": None}, methods=["GET", "POST"])
@sightings_bp.route("/edit/<int:sighting_id>", methods=["GET", "POST"])
def edit(sighting_id):
    """
    Serve the page to add new sighting or edit an existing one and handle the appropriate action
    when the form is submitted

    :param sighting_id: ID for a sighting to edit or None to create a new sighting
    :return: The HTML for the sighting entry page or a response object redirecting to the sighting list page
    """
    if request.method == "POST":
        try:
            sighting_date = datetime.datetime.strptime(request.form["date"], "%d/%m/%Y").date()
            if sighting_id:
                _ = update_sighting(sighting_id,
                                    request.form["location"],
                                    request.form["species"],
                                    sighting_date,
                                    request.form["number"],
                                    request.form["gender"],
                                    request.form["with_young"])
            else:
                _ = create_sighting(request.form["location"],
                                    request.form["species"],
                                    sighting_date,
                                    request.form["number"],
                                    request.form["gender"],
                                    request.form["with_young"])
            return redirect("/sightings/list")
        except ValueError as e:
            return _render_sighting_editing_page(sighting_id, e)
    else:
        return _render_sighting_editing_page(sighting_id, None)
