"""
The reports blueprint supplies view functions and templates for reporting on sightings
"""

from flask import Blueprint, render_template, request
from naturerec_model.logic import list_locations, get_location
from naturerec_model.logic import list_categories, get_category
from naturerec_model.logic import location_individuals_report
from naturerec_web.request_utils import get_posted_date, get_posted_int

reports_bp = Blueprint("reports", __name__, template_folder='templates')


def _render_location_report_page(report_generator=None, from_date=None, to_date=None, location_id=None,
                                 category_id=None):
    """

    :param report_generator:
    :param from_date:
    :param to_date:
    :param location_id:
    :param category_id:
    :return:
    """
    location = get_location(location_id) if location_id else None
    category = get_category(category_id) if category_id else None

    if report_generator and from_date and location_id and category_id:
        report = report_generator(from_date=from_date, to_date=to_date, location_id=location_id,
                                  category_id=category_id)
    else:
        report = None

    return render_template("life_list/list.html",
                           locations=list_locations(),
                           categories=list_categories(),
                           category_id=category_id,
                           location_id=location_id,
                           category=category,
                           location=location,
                           report=report)


@reports_bp.route("/location/individuals", methods=["GET", "POST"])
def life_list_for_category():
    """
    Show the page that generates a report on the total number of individuals seen, filtering by location, category
    and date range

    :return: The HTML for the reporting page
    """
    if request.method == "POST":
        from_date = get_posted_date("from_date")
        to_date = get_posted_date("to_date")
        location_id = get_posted_int("location")
        category_id = get_posted_int("category")
        return _render_location_report_page(location_individuals_report, from_date, to_date, location_id, category_id)
    else:
        return _render_location_report_page()
