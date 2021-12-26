"""
The life list blueprint supplies view functions and templates for generating species sighting "life lists"
"""

from flask import Blueprint, render_template, request
from naturerec_model.logic import list_categories, get_category
from naturerec_model.logic import life_list


life_list_bp = Blueprint("life_list", __name__, template_folder='templates')


def _render_life_list_page(category_id=None):
    """
    Helper to render the life list page

    :param category_id: ID of the category for which to generate a life list
    :return: Rendered life list template
    """
    category = get_category(category_id) if category_id else None
    species = life_list(category_id) if category_id else []
    return render_template("life_list/list.html",
                           categories=list_categories(),
                           category=category,
                           category_id=category_id,
                           species=species,
                           edit_enabled=True)


def _get_posted_int(key):
    """
    Retrieve a named integer value from the POSTed form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key]
    return int(value) if value else None


@life_list_bp.route("/list", methods=["GET", "POST"])
def life_list_for_category():
    """
    Show the page that generates life lists for a given category, with category selection option

    :return: The HTML for the life list page
    """
    if request.method == "POST":
        return _render_life_list_page(_get_posted_int("category"))
    else:
        return _render_life_list_page()
