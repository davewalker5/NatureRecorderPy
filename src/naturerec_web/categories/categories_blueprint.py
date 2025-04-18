"""
The categories blueprint supplies view functions and templates for species category management
"""

from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_required, current_user
from naturerec_model.logic import list_categories, get_category, create_category, update_category, delete_category
from naturerec_web.auth import requires_roles
from naturerec_web.auth.requires_roles import has_roles
from naturerec_web.request_utils import get_posted_int

categories_bp = Blueprint("categories", __name__, template_folder='templates')


def _render_category_editing_page(category_id, error):
    """
    Helper to render the category editing page

    :param category_id: ID for the category to edit or None for addition
    :param error: Error message to display on the page or None
    :return: The rendered category editing template
    """
    category = get_category(category_id) if category_id else None
    return render_template("categories/edit.html",
                           category=category,
                           error=error)


@categories_bp.route("/list", methods=["GET", "POST"])
@login_required
@requires_roles(["Administrator", "Reporter", "Reader"])
def list_all():
    """
    Show the page that lists all categories and is the entry point for adding new ones

    :return: The HTML for the category listing page
    """
    error = None
    is_admin = has_roles(["Administrator"])
    if request.method == "POST":
        try:
            if is_admin:
                delete_record_id = get_posted_int("delete_record_id")
                if delete_record_id:
                    delete_category(delete_record_id)
            else:
                abort(401)
        except ValueError as e:
            error = e

    return render_template("categories/list.html",
                           categories=list_categories(),
                           edit_enabled=is_admin,
                           error=error)


@categories_bp.route("/edit", defaults={"category_id": None}, methods=["GET", "POST"])
@categories_bp.route("/add/<int:category_id>", methods=["GET", "POST"])
@login_required
@requires_roles(["Administrator"])
def edit(category_id):
    """
    Serve the page to add  new category or edit an existing one and handle the appropriate action
    when the form is submitted

    :param category_id: ID for a category to edit or None to create a new category
    :return: The HTML for the category entry page or a response object redirecting to the category list page
    """
    if request.method == "POST":
        # The "supports gender" flag is a check box and is only POSTed if it's checked. If it's unchecked, it
        # won't appear in the form data
        supports_gender = True if "supports_gender" in request.form else False

        try:
            if category_id:
                _ = update_category(category_id, request.form["name"], supports_gender, current_user)
            else:
                _ = create_category(request.form["name"], supports_gender, current_user)
            return redirect("/categories/list")
        except ValueError as e:
            return _render_category_editing_page(category_id, e)
    else:
        return _render_category_editing_page(category_id, None)
