"""
The species blueprint supplies view functions and templates for species management
"""

from flask import Blueprint, render_template, request
from naturerec_model.logic import list_categories, get_category
from naturerec_model.logic import list_species


species_bp = Blueprint("species", __name__, template_folder='templates')


def _render_species_list_page(category_id=None):
    """
    Helper to render the species list page

    :param category_id: ID of the category for which to list species
    :return: List of Species instances for matching species
    """
    species = list_species(category_id) if category_id else []
    return render_template("species/list.html",
                           category_id=category_id,
                           categories=list_categories(),
                           species=species,
                           edit_enabled=True)

def _get_filter_int(key):
    """
    Retrieve a named integer value from the POSTed filtering form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key]
    return int(value) if value else None


@species_bp.route("/list", methods=["GET", "POST"])
def list_filtered_species():
    """
    Show the page that lists today's sightings and is the entry point for adding new ones

    :return: The HTML for the sightings listing page
    """
    if request.method == "POST":
        return _render_species_list_page(_get_filter_int("category"))
    else:
        return _render_species_list_page()
