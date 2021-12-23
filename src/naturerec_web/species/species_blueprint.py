"""
The species blueprint supplies view functions and templates for species management
"""

from flask import Blueprint, render_template, request, redirect
from naturerec_model.logic import list_categories
from naturerec_model.logic import list_species, get_species, create_species, update_species
from naturerec_model.logic import list_species_status_ratings


species_bp = Blueprint("species", __name__, template_folder='templates')


def _render_species_editing_page(species_id, error):
    """
    Helper to render the species editing page

    :param species_id: ID for the species to edit or None for addition
    :param error: Error message to display on the page or None
    :return: The rendered species editing template
    """
    species = get_species(species_id) if species_id else None
    return render_template("species/edit.html",
                           categories=list_categories(),
                           category_id=species.categoryId if species else None,
                           species=species,
                           error=error)


def _render_species_list_page(category_id=None):
    """
    Helper to render the species list page

    :param category_id: ID of the category for which to list species
    :return: List of Species instances for matching species
    """
    species = list_species(category_id) if category_id else []
    return render_template("species/list.html",
                           categories=list_categories(),
                           category_id=category_id,
                           species=species,
                           edit_enabled=True)


def _get_posted_int(key):
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
    Show the page that lists species with category selection option

    :return: The HTML for the species listing page
    """
    if request.method == "POST":
        return _render_species_list_page(_get_posted_int("category"))
    else:
        return _render_species_list_page()


@species_bp.route("/list_status/<int:species_id>")
def list_status_ratings(species_id):
    """
    Show the page that lists species status ratings and is the entry point for adding new ones

    :param species_id: ID for the species for which to list ratings
    :return: The HTML for the species conservation status rating listing page
    """
    return render_template("species/list_status_ratings.html",
                           species_status_ratings=list_species_status_ratings(species_id=species_id),
                           edit_enabled=True)


@species_bp.route("/edit", defaults={"species_id": None}, methods=["GET", "POST"])
@species_bp.route("/add/<int:species_id>", methods=["GET", "POST"])
def edit(species_id):
    """
    Serve the page to add new species or edit an existing one and handle the appropriate action
    when the form is submitted

    :param species_id: ID for a species to edit or None to create a new species
    :return: The HTML for the species entry page or a response object redirecting to the category list page
    """
    if request.method == "POST":
        try:
            if species_id:
                _ = update_species(species_id, _get_posted_int("category"), request.form["name"])
            else:
                _ = create_species(_get_posted_int("category"), request.form["name"])
            return redirect("/species/list")
        except ValueError as e:
            return _render_species_editing_page(species_id, e)
    else:
        return _render_species_editing_page(species_id, None)
