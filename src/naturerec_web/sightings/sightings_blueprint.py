"""
The sightings blueprint supplies view functions and templates for sighting management
"""

import datetime
from flask import Blueprint, render_template, request, session, redirect
from naturerec_model.logic import list_sightings, get_sighting, create_sighting, update_sighting
from naturerec_model.logic import list_locations
from naturerec_model.logic import list_categories
from naturerec_model.logic import list_species
from naturerec_model.model import Gender, Sighting
from naturerec_model.data_exchange import SightingsImportHelper

sightings_bp = Blueprint("sightings", __name__, template_folder='templates')


def _render_sighting_editing_page(sighting_id, message, error):
    """
    Helper to render the sighting editing page

    :param sighting_id: ID for the sighting to edit
    :param message: Message to display on the page or None
    :param error: Error to display on the page or None
    :return: The rendered sighting editing template
    """
    locations = list_locations()
    categories = list_categories()
    sighting = get_sighting(sighting_id) if sighting_id else None

    # If we have a sighting, it's used to set the default date and location. Otherwise, we look for those
    # properties in session
    if sighting:
        location_id = sighting.locationId
        category_id = sighting.species.categoryId
        sighting_date = sighting.sighting_date.strftime(Sighting.DATE_DISPLAY_FORMAT)
    else:
        location_id = int(session["location_id"]) if "location_id" in session else 0
        category_id = int(session["category_id"]) if "category_id" in session else 0
        sighting_date = session["sighting_date"] \
            if "sighting_date" in session \
            else datetime.datetime.now().strftime(Sighting.DATE_DISPLAY_FORMAT)

    return render_template("sightings/edit.html",
                           locations=locations,
                           categories=categories,
                           sighting=sighting,
                           location_id=location_id,
                           category_id=category_id,
                           sighting_date=sighting_date,
                           genders=Gender.gender_map(),
                           with_young={1: "Yes", 0: "No"},
                           message=message,
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
    message = session.pop("message") if "message" in session else None
    return render_template("sightings/list.html",
                           from_date=from_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if from_date else "",
                           to_date=to_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if to_date else "",
                           location_id=location_id,
                           category_id=category_id,
                           species_id=species_id,
                           locations=list_locations(),
                           categories=list_categories(),
                           action_button_label="Filter Sightings",
                           sightings=sightings,
                           message=message,
                           edit_enabled=True)


def _render_sightings_import_page(error):
    """
    Helper to render the sightings import page

    :param error: Error message to display on the page or None
    :return: The rendered import template
    """
    return render_template("sightings/import.html",
                           error=error)


def _get_filter_int(key):
    """
    Retrieve a named integer value from the POSTed filtering form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key] if key in request.form else None
    return int(value) if value else None


def _get_filter_date(key):
    """
    Retrieve a named date value from the POSTed filtering form

    :param key: Value key
    :return: Value or None if not specified
    """
    date_string = request.form[key] if key in request.form else None
    return datetime.datetime.strptime(date_string, Sighting.DATE_DISPLAY_FORMAT).date() if date_string else None


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
            # Get the selected date and put it into session
            date_string = request.form["date"]
            session["sighting_date"] = date_string
            sighting_date = datetime.datetime.strptime(date_string, Sighting.DATE_DISPLAY_FORMAT).date()

            # Get the selected location and put it into session
            location_id = request.form["location"]
            session["location_id"] = location_id

            # Get the selected category and put it into session
            category_id = request.form["category"]
            session["category_id"] = category_id

            if sighting_id:
                _ = update_sighting(sighting_id,
                                    location_id,
                                    request.form["species"],
                                    sighting_date,
                                    request.form["number"],
                                    request.form["gender"],
                                    request.form["with_young"])
                sighting = get_sighting(sighting_id)
            else:
                created_id = create_sighting(location_id,
                                             request.form["species"],
                                             sighting_date,
                                             request.form["number"],
                                             request.form["gender"],
                                             request.form["with_young"]).id
                sighting = get_sighting(created_id)

            # Construct the confirmation message
            action = "Updated" if sighting_id else "Added"
            message = f"{action} sighting of {sighting.species.name} " \
                      f"at {sighting.location.name} " \
                      f"on {sighting.display_date}"

            return _render_sighting_editing_page(sighting_id, message, None)
        except ValueError as e:
            return _render_sighting_editing_page(sighting_id, None, e)
    else:
        return _render_sighting_editing_page(sighting_id, None, None)


@sightings_bp.route("/import", methods=["GET", "POST"])
def import_sightings():
    """
    Serve the page to import sightings and handle the import when the form is submitted

    :return: The HTML for the import page or a response object redirecting to the scheme list page
    """
    if request.method == "POST":
        try:
            importer = SightingsImportHelper(request.files["csv_file_name"])
            importer.start()
            session["message"] = "Sightings are being imported in the background"
            return redirect("/sightings/list")
        except ValueError as e:
            return _render_sightings_import_page(e)
    else:
        return _render_sightings_import_page(None)
