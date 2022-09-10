"""
This module contains utilities for extracting values from POSTed form data
"""

import datetime
from flask import request
from src.naturerec_model.model import Sighting


def get_posted_int(key):
    """
    Retrieve a named integer value from the POSTed form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key] if key in request.form else None
    return int(value) if value else None


def get_posted_bool(key):
    """
    Retrieve a named boolean value from the POSTed form

    :param key: Value key
    :return: Value or None if not specified
    """
    int_value = get_posted_int(key)
    return True if int_value else False


def get_posted_float(key):
    """
    Retrieve a named float value from a POSTed form

    :param key: Value key
    :return: Value or None if not specified
    """
    value = request.form[key]
    return float(value) if value else None


def get_posted_date(key):
    """
    Retrieve a named date value from the POSTed form

    :param key: Value key
    :return: Value or None if not specified
    """
    date_string = request.form[key] if key in request.form else None
    return datetime.datetime.strptime(date_string, Sighting.DATE_DISPLAY_FORMAT).date() if date_string else None
