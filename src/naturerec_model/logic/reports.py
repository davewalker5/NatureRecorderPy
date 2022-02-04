"""
This module contains the business logic for the pre-defined reports
"""

import datetime
import sqlalchemy as db
from ..model import Engine, Sighting


def results_to_list(results, column_names):
    """
    Given a SQL alchemy result set and a list of named columns, reformat the results into a list of dictionaries,
    one per row, in which the keys are the column names

    :param results: SQLAlchemy results
    :param column_names: List of column names
    :return: Reformatted results
    """
    return [{column_name: row[index] for index, column_name in enumerate(column_names)} for row in results]


def location_individuals_report(from_date, location_id, category_id, to_date=None):
    """
    Report on the total number of individuals seen, filtering by location, category and date range

    :param from_date: Start date for reporting
    :param location_id: Location id
    :param category_id: Category id
    :param to_date: End-date for reporting or None for today
    :return: A tuple of the report results and the column names
    """
    # If the "to" date isn't set, make it today
    if not to_date:
        to_date = datetime.datetime.today()

    # Format the dates in the format required in a SQL query
    from_date_string = from_date.strftime(Sighting.DATE_FORMAT)
    to_date_string = to_date.strftime(Sighting.DATE_FORMAT)

    # Construct the query
    sql_query = f"SELECT sp.Name, SUM( IFNULL( s.Number, 1 ) ) AS 'Count' " \
                f"FROM SIGHTINGS s " \
                f"INNER JOIN LOCATIONS l ON l.Id = s.LocationId " \
                f"INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId " \
                f"INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId " \
                f"WHERE Date BETWEEN '{from_date_string}' AND '{to_date_string}' " \
                f"AND l.Id = {location_id} " \
                f"AND c.Id = {category_id} " \
                f"GROUP BY sp.Name"

    # Run the query and convert the SQL Alchemy results to a more usable format
    results = Engine.execute(db.text(sql_query))
    column_names = ["Species", "Count"]
    return results_to_list(results, column_names), column_names


def location_days_report(from_date, location_id, category_id, to_date=None):
    """
    Report on the number of days on which a given species was seen, filtering by location, category and date range

    :param from_date: Start date for reporting
    :param location_id: Location id
    :param category_id: Category id
    :param to_date: End-date for reporting or None for today
    :return: A tuple of the report results and the column names
    """
    # If the "to" date isn't set, make it today
    if not to_date:
        to_date = datetime.datetime.today()

    # Format the dates in the format required in a SQL query
    from_date_string = from_date.strftime(Sighting.DATE_FORMAT)
    to_date_string = to_date.strftime(Sighting.DATE_FORMAT)

    # Construct the query
    sql_query = f"SELECT sp.Name, COUNT( s.Id ) AS 'Count' " \
                f"FROM SIGHTINGS s " \
                f"INNER JOIN LOCATIONS l ON l.Id = s.LocationId " \
                f"INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId " \
                f"INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId " \
                f"WHERE Date BETWEEN '{from_date_string}' AND '{to_date_string}' " \
                f"AND l.Id = {location_id} " \
                f"AND c.Id = {category_id} " \
                f"GROUP BY sp.Name"

    # Run the query and convert the SQL Alchemy results to a more usable format
    results = Engine.execute(db.text(sql_query))
    column_names = ["Species", "Count"]
    return results_to_list(results, column_names), column_names
