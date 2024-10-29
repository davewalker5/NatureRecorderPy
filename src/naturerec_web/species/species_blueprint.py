"""
The species blueprint supplies view functions and templates for species management
"""

from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_required, current_user
from naturerec_model.logic import list_categories
from naturerec_model.logic import list_species, get_species, create_species, update_species, delete_species
from naturerec_web.auth import requires_roles, has_roles
from naturerec_web.request_utils import get_posted_int

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


def _render_species_list_page(category_id=None, error=None):
    """
    Helper to render the species list page

    :param category_id: ID of the category for which to list species
    :param error: Error message to show on the page
    :return: Rendered species list template
    """
    is_admin = has_roles(["Administrator"])
    species = list_species(category_id) if category_id else []
    return render_template("species/list.html",
                           categories=list_categories(),
                           category_id=category_id,
                           species=species,
                           edit_enabled=is_admin,
                           error=error)


@species_bp.route("/list", methods=["GET", "POST"])
@login_required
@requires_roles(["Administrator", "Reporter", "Reader"])
def list_filtered_species():
    """
    Show the page that lists species with category selection option

    :return: The HTML for the species listing page
    """
    if request.method == "POST":
        error = None
        try:
            delete_record_id = get_posted_int("delete_record_id")
            if delete_record_id:
                if has_roles(["Administrator"]):
                    delete_species(delete_record_id)
                else:
                    abort(401)
        except ValueError as e:
            error = e

        return _render_species_list_page(get_posted_int("category"), error)
    else:
        return _render_species_list_page()


@species_bp.route("/add", defaults={"species_id": None}, methods=["GET", "POST"])
@species_bp.route("/edit/<int:species_id>", methods=["GET", "POST"])
@login_required
@requires_roles(["Administrator"])
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
                _ = update_species(species_id, get_posted_int("category"), request.form["name"], request.form["scientific_name"], current_user)
            else:
                _ = create_species(get_posted_int("category"), request.form["name"], current_user)
            return redirect("/species/list")
        except ValueError as e:
            return _render_species_editing_page(species_id, e)
    else:
        return _render_species_editing_page(species_id, None)
