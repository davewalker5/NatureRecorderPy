"""
The reports blueprint supplies view functions and templates for reporting on sightings
"""

from flask import Blueprint, render_template, request
from naturerec_model.logic import list_locations
from naturerec_model.logic import list_categories
from naturerec_model.logic import location_individuals_report, location_days_report
from naturerec_model.model import Sighting
from naturerec_web.request_utils import get_posted_date, get_posted_int

reports_bp = Blueprint("reports", __name__, template_folder='templates')


def _render_location_report_page(title, report_generator=None, from_date=None, to_date=None, location_id=None,
                                 category_id=None):
    """
    Helper to show a location-based reporting page

    :param title: Title of the  report
    :param report_generator: Report generator method
    :param from_date: From date for the reporting period
    :param to_date: To date for the reporting period
    :param location_id: ID for the location to report on
    :param category_id: ID for the category to report on
    :return: HTML for the rendered reporting page
    """
    from_date_string = from_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if from_date else ""
    to_date_string = to_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if to_date else ""

    if report_generator and from_date and location_id and category_id:
        report = report_generator(from_date=from_date, to_date=to_date, location_id=location_id,
                                  category_id=category_id)
    else:
        report = None

    return render_template("reports/location_report.html",
                           title=title,
                           locations=list_locations(),
                           categories=list_categories(),
                           category_id=category_id,
                           location_id=location_id,
                           from_date=from_date_string,
                           to_date=to_date_string,
                           report=report)


@reports_bp.route("/location/individuals", methods=["GET", "POST"])
def individuals_by_species_and_location():
    """
    Show the page that generates a report on the total number of individuals seen, filtering by location, category
    and date range

    :return: The HTML for the reporting page
    """
    title = "Individuals by Species & Location"
    if request.method == "POST":
        from_date = get_posted_date("from_date")
        to_date = get_posted_date("to_date")
        location_id = get_posted_int("location")
        category_id = get_posted_int("category")
        return _render_location_report_page(title, location_individuals_report, from_date, to_date, location_id,
                                            category_id)
    else:
        return _render_location_report_page(title)


@reports_bp.route("/location/sightings", methods=["GET", "POST"])
def sightings_by_species_and_location():
    """
    Report on the number of days on which a given species was seen, filtering by location, category and date range

    :return: The HTML for the reporting page
    """
    title = "Sightings by Species & Location"
    if request.method == "POST":
        from_date = get_posted_date("from_date")
        to_date = get_posted_date("to_date")
        location_id = get_posted_int("location")
        category_id = get_posted_int("category")
        return _render_location_report_page(title, location_days_report, from_date, to_date, location_id, category_id)
    else:
        return _render_location_report_page(title)
