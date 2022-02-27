"""
The categories blueprint supplies view functions and templates for species category management
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from naturerec_model.logic import list_categories, get_category, create_category, update_category
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
def list_all():
    """
    Show the page that lists all categories and is the entry point for adding new ones

    :return: The HTML for the category listing page
    """
    if request.method == "POST":
        # If a record ID has been posted back for deletion, delete it before re-rendering the list
        # with the same filtering criteria
        delete_record_id = get_posted_int("delete_record_id")
        if delete_record_id:
            pass

    return render_template("categories/list.html",
                           categories=list_categories(),
                           edit_enabled=True)


@categories_bp.route("/edit", defaults={"category_id": None}, methods=["GET", "POST"])
@categories_bp.route("/add/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit(category_id):
    """
    Serve the page to add  new category or edit an existing one and handle the appropriate action
    when the form is submitted

    :param category_id: ID for a category to edit or None to create a new category
    :return: The HTML for the category entry page or a response object redirecting to the category list page
    """
    if request.method == "POST":
        try:
            if category_id:
                _ = update_category(category_id, request.form["name"])
            else:
                _ = create_category(request.form["name"])
            return redirect("/categories/list")
        except ValueError as e:
            return _render_category_editing_page(category_id, e)
    else:
        return _render_category_editing_page(category_id, None)
