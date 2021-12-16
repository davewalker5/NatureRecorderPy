"""
The sightings blueprint supplies view functions and templates for sighting management
"""

import os
import datetime
from flask import Blueprint, render_template
from naturerec_model.logic import list_sightings


sightings_bp = Blueprint("sightings", __name__, template_folder='templates')


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
