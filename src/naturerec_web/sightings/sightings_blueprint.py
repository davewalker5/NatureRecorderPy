"""
The sightings blueprint supplies view functions and templates for sighting management
"""

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
    today = datetime.datetime.today()
    from_date = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    sightings = list_sightings(from_date=from_date)
    print(f"Sightings from {from_date}")
    print(sightings)
    return render_template("sightings/list.html",
                           sightings=sightings,
                           edit_enabled=True)
