"""
This module contains the business logic for the pre-defined reports
"""

import datetime
import pandas as pd
import matplotlib.pyplot as plt
from ..model import Engine, Sighting


def location_individuals_report(from_date, location_id, category_id, to_date=None):
    """
    Report on the total number of individuals seen, filtering by location, category and date range

    :param from_date: Start date for reporting
    :param location_id: Location id
    :param category_id: Category id
    :param to_date: End-date for reporting or None for today
    :return: A Pandas Dataframe containing the results
    """
    # If the "to" date isn't set, make it today
    if not to_date:
        to_date = datetime.datetime.today()

    # Format the dates in the format required in a SQL query
    from_date_string = from_date.strftime(Sighting.DATE_FORMAT)
    to_date_string = to_date.strftime(Sighting.DATE_FORMAT)

    # Construct the query
    sql_query = f"SELECT sp.Name AS 'Species', SUM( IFNULL( s.Number, 1 ) ) AS 'Count' " \
                f"FROM SIGHTINGS s " \
                f"INNER JOIN LOCATIONS l ON l.Id = s.LocationId " \
                f"INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId " \
                f"INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId " \
                f"WHERE Date BETWEEN '{from_date_string}' AND '{to_date_string}' " \
                f"AND l.Id = {location_id} " \
                f"AND c.Id = {category_id} " \
                f"GROUP BY sp.Name"

    return pd.read_sql(sql_query, Engine).set_index("Species")


def location_days_report(from_date, location_id, category_id, to_date=None):
    """
    Report on the number of days on which a given species was seen, filtering by location, category and date range

    :param from_date: Start date for reporting
    :param location_id: Location id
    :param category_id: Category id
    :param to_date: End-date for reporting or None for today
    :return: A Pandas Dataframe containing the results
    """
    # If the "to" date isn't set, make it today
    if not to_date:
        to_date = datetime.datetime.today()

    # Format the dates in the format required in a SQL query
    from_date_string = from_date.strftime(Sighting.DATE_FORMAT)
    to_date_string = to_date.strftime(Sighting.DATE_FORMAT)

    # Construct the query
    sql_query = f"SELECT sp.Name AS 'Species', COUNT( s.Id ) AS 'Count' " \
                f"FROM SIGHTINGS s " \
                f"INNER JOIN LOCATIONS l ON l.Id = s.LocationId " \
                f"INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId " \
                f"INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId " \
                f"WHERE Date BETWEEN '{from_date_string}' AND '{to_date_string}' " \
                f"AND l.Id = {location_id} " \
                f"AND c.Id = {category_id} " \
                f"GROUP BY sp.Name"

    return pd.read_sql(sql_query, Engine).set_index("Species")


def save_report_barchart(report_df, y_column_name, x_label, y_label, title, image_path, x_column_name=None):
    """
    Export a PNG image containing the data for a report

    :param report_df: Report dataframe
    :param y_column_name: Name of the column containing the Y-axis values
    :param x_label: X-axis label
    :param y_label: Y-axis label
    :param title: TItle
    :param image_path: Output image path
    :param x_column_name: Name of the column containing the X-axis labels or None to use the index
    """

    # Set up the X and  Y axes
    x = report_df[x_column_name] if x_column_name else report_df.index
    y = report_df[y_column_name]
    x_pos = [i for i, _ in enumerate(x)]

    # Configure the style and plot type
    plt.style.use('ggplot')
    plt.bar(x_pos, y, color='green')

    # Set up the axes and title
    plt.xlabel(x_label)
    plt.xticks(x_pos, x)
    plt.xticks(rotation=90)
    plt.ylabel(y_label)
    plt.title(title)

    # This prevents the X-labels from going over the edge of the plot
    plt.tight_layout()

    # Save to the specified file in PNG format
    plt.savefig(image_path, format='png', dpi=300)
