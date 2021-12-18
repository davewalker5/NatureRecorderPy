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


@sightings_bp.route("/list")
def list_today():
    """
    Show the page that lists today's sightings and is the entry point for adding new ones

    :return: The HTML for the sightings listing page
    """
    from_date = datetime.datetime.today().date()
    sightings = list_sightings(from_date=from_date)
    return render_template("sightings/list.html",
                           sightings=sightings,
                           edit_enabled=True)


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
