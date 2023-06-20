"""
The reports blueprint supplies view functions and templates for reporting on sightings
"""

import datetime
import os
from flask import Blueprint, render_template, request
from flask_login import login_required
from naturerec_model.logic import list_locations, get_location
from naturerec_model.logic import list_categories, get_category
from naturerec_model.logic import get_species
from naturerec_model.logic import location_species_report, get_report_barchart, species_by_date_report
from naturerec_model.model import Sighting
from naturerec_web.request_utils import get_posted_date, get_posted_int

reports_bp = Blueprint("reports", __name__, template_folder='templates')


def _render_location_report_page(from_date=None, to_date=None, location_id=None, category_id=None):
    """
    Helper to show a location-based reporting page

    :param from_date: From date for the reporting period
    :param to_date: To date for the reporting period
    :param location_id: ID for the location to report on
    :param category_id: ID for the category to report on
    :return: HTML for the rendered reporting page
    """
    # This is done just to make the Behave tests work when the reports page opens a new tab
    form_target = "target='_blank'" if "NATUREREC_SAME_PAGE_REPORT" not in os.environ else ""

    # If the to date isn't set, make to today
    if not to_date:
        to_date = datetime.datetime.today()

    from_date_string = from_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if from_date else ""
    to_date_string = to_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if to_date else ""

    if from_date and location_id and category_id:
        # Generate the report
        report_df = location_species_report(from_date, to_date, location_id, category_id)

        # Get the location and category details and use them to construct a sub-title
        location = get_location(location_id)
        category = get_category(category_id)
        subtitle = f"Location: {location.name}\n" \
                   f"Category: {category.name}   " \
                   f"From: {from_date_string}   " \
                   f"To: {to_date_string}"

        # Create the bar charts from the report
        chart_config = [
            {
                "title": "Number of Sightings by Location and Species",
                "y-column": "Sightings",
                "y-label": "Number of Sightings"
            },
            {
                "title": "Total Individuals by Location and Species",
                "y-column": "Total Individuals",
                "y-label": "Total Individuals Seen"
            },
            {
                "title": "Average Individuals per Sighting",
                "y-column": "Average Seen",
                "y-label": "Average Individuals Seen"
            }
        ]

        charts = []
        for config in chart_config:
            barchart_base64 = get_report_barchart(report_df, config["y-column"], "Species", config["y-label"],
                                                  config["title"], subtitle, None)
            charts.append(barchart_base64)

    else:
        report_df = None
        charts = None

    return render_template("reports/location_report.html",
                           title="Location Report",
                           locations=list_locations(),
                           categories=list_categories(),
                           category_id=category_id,
                           location_id=location_id,
                           from_date=from_date_string,
                           to_date=to_date_string,
                           report=report_df,
                           charts=charts,
                           form_target=form_target)


def _render_species_report_page(from_date=None, to_date=None, location_id=None, category_id=None, species_id=None,
                                interval=None):
    """
    Helper to show a location-based reporting page

    :param from_date: From date for the reporting period
    :param to_date: To date for the reporting period
    :param location_id: ID for the location to report on
    :param category_id: ID for the category used to select the species
    :param species_id: ID for the species to report on
    :param interval: Reporting interval
    :return: HTML for the rendered reporting page
    """
    # This is done just to make the Behave tests work when the reports page opens a new tab
    form_target = "target='_blank'" if "NATUREREC_SAME_PAGE_REPORT" not in os.environ else ""

    # If the to date isn't set, make to today
    if not to_date:
        to_date = datetime.datetime.today()

    from_date_string = from_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if from_date else ""
    to_date_string = to_date.strftime(Sighting.DATE_DISPLAY_FORMAT) if to_date else ""

    if from_date and location_id and category_id and species_id:
        # Generate the report
        by_week = interval.casefold() == "week" if interval else False
        report_df = species_by_date_report(from_date, to_date, location_id, species_id, by_week)

        # Get the location and species details and use them to construct a sub-title
        location = get_location(location_id)
        species = get_species(species_id)
        subtitle = f"Location: {location.name}\n" \
                   f"Species: {species.name}   " \
                   f"From: {from_date_string}   " \
                   f"To: {to_date_string}"

        # Create the bar charts from the report
        chart_config = [
            {
                "title": "Number of Sightings by Location and Date",
                "y-column": "Sightings",
                "y-label": "Number of Sightings"
            },
            {
                "title": "Average Individuals per Sighting",
                "y-column": "Average Seen",
                "y-label": "Average Individuals Seen"
            }
        ]

        charts = []
        for config in chart_config:
            barchart_base64 = get_report_barchart(report_df, config["y-column"], "Month", config["y-label"],
                                                  config["title"], subtitle, None)
            charts.append(barchart_base64)

    else:
        report_df = None
        charts = None

    return render_template("reports/species_by_date_report.html",
                           title="Species by Date Report",
                           locations=list_locations(),
                           categories=list_categories(),
                           category_id=category_id,
                           species_id=species_id,
                           location_id=location_id,
                           from_date=from_date_string,
                           to_date=to_date_string,
                           interval=interval,
                           report=report_df,
                           charts=charts,
                           form_target=form_target)


@reports_bp.route("/location", methods=["GET", "POST"])
@login_required
def location_report():
    """
    Show the page that generates a location, species and sighting report for a given date range

    :return: The HTML for the reporting page
    """
    if request.method == "POST":
        from_date = get_posted_date("from_date")
        to_date = get_posted_date("to_date")
        location_id = get_posted_int("location")
        category_id = get_posted_int("category")
        return _render_location_report_page(from_date, to_date, location_id, category_id)
    else:
        return _render_location_report_page()


@reports_bp.route("/species", methods=["GET", "POST"])
@login_required
def species_report():
    """
    Show the page that generates a species sighting report for a given date range and location

    :return: The HTML for the reporting page
    """
    if request.method == "POST":
        from_date = get_posted_date("from_date")
        to_date = get_posted_date("to_date")
        location_id = get_posted_int("location")
        category_id = get_posted_int("category")
        species_id = get_posted_int("species")
        interval = request.form["interval"]
        return _render_species_report_page(from_date, to_date, location_id, category_id, species_id, interval)
    else:
        return _render_species_report_page()
