"""
This module contains the business logic for the pre-defined reports
"""

import base64
import io
import datetime
import pandas as pd
from ..model import Engine, Sighting
import matplotlib

# Specify Agg as a non-interactive back-end
matplotlib.use('Agg')

import matplotlib.pyplot as plt


def get_report_barchart(report_df, y_column_name, x_label, y_label, title, subtitle, x_column_name=None):
    """
    Get the base-64 representation of an image containing a report barchart

    :param report_df: Report dataframe
    :param y_column_name: Name of the column containing the Y-axis values
    :param x_label: X-axis label
    :param y_label: Y-axis label
    :param title: Title
    :param subtitle: Subtitle
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

    # Set the chart titles
    plt.suptitle(title, fontsize=14)
    plt.title(subtitle, fontsize=8)
    # plt.title(title)

    # This prevents the X-labels from going over the edge of the plot
    plt.tight_layout()

    # Rather than saving to a file and loading that to get its base64 representation, save to a memory buffer and
    # then get the base-64 representation from that buffer
    # plt.savefig(image_path, format='png', dpi=300)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    barchart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # And clear the plot
    plt.clf()
    plt.cla()
    plt.close()

    return barchart_base64


def location_species_report(from_date, to_date, location_id, category_id):
    """
    Report on the species and sightings at a location in the specified date range

    :param from_date: Start date for reporting
    :param to_date: End-date for reporting
    :param location_id: Location id
    :param category_id: Category id
    :return: A Pandas Dataframe containing the results
    """

    # Format the dates in the format required in a SQL query
    from_date_string = from_date.strftime(Sighting.DATE_FORMAT)
    to_date_string = to_date.strftime(Sighting.DATE_FORMAT)

    # Construct the query
    sql_query = f"SELECT sp.Name AS 'Species', " \
                f"COUNT( sp.Id ) AS 'Sightings', " \
                f"SUM( IFNULL( s.Number, 1 ) ) AS 'Total Individuals', " \
                f"MIN( IFNULL( s.Number, 1 ) ) AS 'Minimum Seen', " \
                f"MAX( IFNULL( s.Number, 1 ) ) AS 'Maximum Seen', " \
                f"ROUND(AVG( IFNULL( s.Number, 1 ) ), 2) AS 'Average Seen' " \
                f"FROM SIGHTINGS s " \
                f"INNER JOIN LOCATIONS l ON l.Id = s.LocationId " \
                f"INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId " \
                f"INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId " \
                f"WHERE s.Date BETWEEN '{from_date_string}' AND '{to_date_string}' " \
                f"AND l.Id = {location_id} " \
                f"AND c.Id = {category_id} " \
                f"GROUP BY sp.Name"

    return pd.read_sql(sql_query, Engine).set_index("Species")


def species_by_date_report(from_date, to_date, location_id, species_id, by_week):
    """
    Return the species sightings report for a location, species and date range

    :param from_date: Start date for reporting
    :param to_date: End-date for reporting
    :param location_id: Location id
    :param species_id: Species id
    :param by_week: True to report by week number, False to report by month
    :return: A Pandas Dataframe containing the results
    """
    # Format the dates in the format required in a SQL query
    from_date_string = from_date.strftime(Sighting.DATE_FORMAT)
    to_date_string = to_date.strftime(Sighting.DATE_FORMAT)

    # Construct and execute the query
    format_specifier = "W" if by_week else "m"
    interval_column_name = "Week" if by_week else "Month_Number"
    sql_query = f"SELECT STRFTIME( '%{format_specifier}', Date ) AS {interval_column_name}, " \
                f"COUNT( sp.Id ) AS 'Sightings', " \
                f"MIN( IFNULL( s.Number, 1 ) ) AS 'Minimum Seen'," \
                f"MAX( IFNULL( s.Number, 1 ) ) AS 'Maximum Seen', " \
                f"ROUND(AVG( IFNULL( s.Number, 1 ) ), 2) AS 'Average Seen' " \
                f"FROM SIGHTINGS s " \
                f"INNER JOIN LOCATIONS l ON l.Id = s.LocationId " \
                f"INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId " \
                f"WHERE s.Date BETWEEN '{from_date_string}' AND '{to_date_string}' " \
                f"AND l.Id = {location_id} " \
                f"AND sp.Id = {species_id} " \
                f"GROUP BY STRFTIME( '%{format_specifier}', Date ), sp.Name"
    report_df = pd.read_sql(sql_query, Engine)

    # If we're reporting by month, add a month name column, remove the month number column and make the month
    # name the index. Otherwise, just make the week number the index
    if by_week:
        report_df.set_index(interval_column_name, inplace=True)
    else:
        report_df["Month"] = [datetime.datetime.strptime(month_number, "%m").strftime("%b")
                              for month_number
                              in report_df[interval_column_name]]
        report_df.set_index("Month", inplace=True)
        report_df.drop(columns=[interval_column_name], inplace=True)

    return report_df
