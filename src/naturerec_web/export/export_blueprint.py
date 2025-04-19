"""
The export blueprint supplies view functions and templates for exporting sightings
"""

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from naturerec_model.logic import list_locations
from naturerec_model.logic import list_categories
from naturerec_model.data_exchange import SightingsExportHelper
from naturerec_model.model import Sighting
from naturerec_web.request_utils import get_posted_date, get_posted_int
from naturerec_web.auth import requires_roles

export_bp = Blueprint("export", __name__, template_folder='templates')


def _render_export_filters_page(from_date=None,
                                to_date=None,
                                location_id=None,
                                category_id=None,
                                species_id=None,
                                message=None):
    """
    Helper to render the export filters page

    :param from_date: Include sightings on or after this date
    :param to_date: Include sightings up to this date
    :param location_id: Include sightings at this location
    :param category_id: Species category for the selected species
    :param species_id: Include sightings for this species
    :param message: Message to display on the page
    :return: The HTML for the rendered sightings export page
    """
    return render_template("export/filters.html",
                           message=message,
                           filename_required=True,
                           from_date=from_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if from_date else "",
                           to_date=to_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if to_date else "",
                           location_id=location_id,
                           category_id=category_id,
                           species_id=species_id,
                           locations=list_locations(),
                           categories=list_categories(),
                           action_button_label="Export Sightings",
                           edit_enabled=True)


@export_bp.route("/filters", methods=["GET", "POST"])
@login_required
@requires_roles(["Administrator"])
def export():
    """
    Show the page that presents filters for exporting sightings

    :return: The HTML for the sightings export page
    """
    if request.method == "POST":
        # Get the export parameters
        filename = request.form["filename"]
        from_date = get_posted_date("from_date")
        to_date = get_posted_date("to_date")
        location_id = get_posted_int("location")
        category_id = get_posted_int("category")
        species_id = get_posted_int("species")

        # Kick off the export
        exporter = SightingsExportHelper(filename, current_user, from_date, to_date, location_id, species_id)
        exporter.start()

        # Go to the export filter page
        message = "Matching sightings are exporting in the background"
        return _render_export_filters_page(from_date, to_date, location_id, category_id, species_id, message)
    else:
        return _render_export_filters_page()
