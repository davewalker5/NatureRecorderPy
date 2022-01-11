import time
import datetime
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from naturerec_model.model import Sighting
from naturerec_model.model.utils import get_data_path
from naturerec_model.logic import get_location, create_location
from naturerec_model.logic import get_category, create_category
from naturerec_model.logic import get_species, create_species


def get_date_from_string(date_string):
    """
    Given a date string, return the corresponding date

    :param date_string: Representation of a date as DD/MM/YYYY
    :return: The date object corresponding the specified date
    """
    if date_string.casefold() == "TODAY".casefold():
        return datetime.datetime.today().date()
    else:
        return datetime.datetime.strptime(date_string, Sighting.DATE_IMPORT_FORMAT).date()


def create_test_location(name):
    """
    Create a named location, if it doesn't already exist

    :param name: Location name
    :return: Instance of the Location() class
    """
    try:
        location = get_location(name)
    except ValueError:
        location = create_location(name, "Oxfordshire", "United Kingdom")
    return location


def create_test_category(name):
    """
    Create a named category, if it doesn't already exist

    :param name: Category name
    :return: Instance of the Category() class
    """
    try:
        category = get_category(name)
    except ValueError:
        category = create_category(name)
    return category


def create_test_species(name, category_id):
    """
    Create a named species, if it doesn't already exist

    :param name: Species name
    :param category_id: Category the species belongs to
    :return: Instance of the Species() class
    """
    try:
        species = get_species(name)
    except ValueError:
        species = create_species(category_id, name)
    return species


def select_option(context, element, text, delay):
    """
    Select an option in a select list based on the visible text

    :param context: Behave context
    :param element: Name of the HTML select element
    :param text: Visible text for the option to select
    :param delay: Time, in seconds, to wait before making the selection or 0/None for no delay
    """
    # If requested, wait for the specified delay, to allow the select list to be rendered
    if delay:
        time.sleep(delay)

    # Click on the select element, first, to make its options visible and ready to interact with
    select_element = context.browser.find_element(By.NAME, element)
    select_element.click()

    # Create a select object from the element and select the requested value
    selector = Select(select_element)
    selector.select_by_visible_text(text)


def confirm_table_row_count(context, expected, delay):
    """
    Find a results table in the current page, count the number of rows in the table body
    and confirm they match the expected count

    :param context: Behave context, which contains a member for the Selenium browser driver
    :param expected: The expected row count
    :param delay: THe number of seconds to wait before attempting the check (or 0/None for no delay)
    """
    # If requested, wait for the specified delay, to allow the table to be rendered
    if delay:
        time.sleep(delay)

    # Find the table on the page
    table = context.browser.find_element(By.CLASS_NAME, "striped")
    table_body = table.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")

    # Confirm
    expected = int(expected)
    actual = len(table_rows)
    assert actual == expected


def confirm_span_exists(context, text, delay):
    """
    Confirm that a span containing the specified text exists on the page

    :param context: Behave context, which contains a member for the Selenium browser driver
    :param text: The expected text in the span
    :param delay: THe number of seconds to wait before attempting the check (or 0/None for no delay)
    """
    # If requested, wait for the specified delay, to allow the span to be rendered
    if delay:
        time.sleep(delay)

    # Find the span with the specified text
    xpath = f"//span[text()='{text}']"
    _ = context.browser.find_element(By.XPATH, xpath)


def get_export_filepath(filename):
    """
    Given a filename for sightings export, return the full path to the exported CSV file

    :param filename: Export file name
    :return: Full path to the export file with that name
    """
    return os.path.join(get_data_path(), "exports", filename)


def delete_export_file(filename):
    """
    Delete the export file with the specified name

    :param filename: Export file name
    """
    filepath = get_export_filepath(filename)
    if os.path.exists(filepath):
        os.unlink(filepath)
