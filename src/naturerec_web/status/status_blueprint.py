"""
The status blueprint supplies view functions and templates for conservation status scheme management
"""

from flask import Blueprint, render_template
from naturerec_model.logic import list_status_schemes


status_bp = Blueprint("status", __name__, template_folder='templates')


@status_bp.route("/list")
def list_all():
    """
    Show the page that lists all conservation status schemes and is the entry point for adding new ones

    :return: The HTML for the listing page
    """
    return render_template("status/list.html",
                           status_schemes=list_status_schemes(),
                           edit_enabled=True)
