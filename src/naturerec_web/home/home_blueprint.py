"""
The home blueprint supplies view functions and templates for the site home page
"""
from flask import Blueprint, redirect

from naturerec_web.auth import has_roles

home_bp = Blueprint("home", __name__, template_folder='templates')


@home_bp.route("/")
def home():
    """
    Serve the home page for the site

    :return: Rendered home page template
    """
    if has_roles(["Administrator", "Reporter"]):
        return redirect("/sightings/edit")
    else:
        return redirect("/sightings/list")
