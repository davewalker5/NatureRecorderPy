"""
The categories blueprint supplies view functions and templates for species category management
"""

from flask import Blueprint, render_template, request, redirect
from naturerec_model.logic import list_categories, get_category, create_category


categories_bp = Blueprint("categories", __name__, template_folder='templates')


@categories_bp.route("/list")
def list_all():
    """
    Show the page that lists all categories and is the entry point for adding new ones

    :return: The HTML for the category listing page
    """
    return render_template("categories/list.html",
                           categories=list_categories(),
                           edit_enabled=True)
