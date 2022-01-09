import datetime
from naturerec_model.model import Sighting
from naturerec_model.logic import get_location, create_location
from naturerec_model.logic import get_category, create_category
from naturerec_model.logic import get_species, create_species


def get_date_from_string(date_string):
    """
    Given a date string, return the corresponding date

    :param date_string: Representation of a date as DD/MM/YYYY
    :return: The date object corresponding the specified date
    """
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
