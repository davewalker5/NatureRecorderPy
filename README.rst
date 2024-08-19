.. image:: https://github.com/davewalker5/NatureRecorderPy/workflows/Python%20CI%20Build/badge.svg
    :target: https://github.com/davewalker5/NatureRecorderPy/actions
    :alt: Build Status

.. image:: https://codecov.io/gh/davewalker5/NatureRecorderPy/branch/main/graph/badge.svg?token=U86UFDVD5S
    :target: https://codecov.io/gh/davewalker5/NatureRecorderPy
    :alt: Coverage

.. image:: https://sonarcloud.io/api/project_badges/measure?project=davewalker5_NatureRecorderPy&metric=alert_status
    :target: https://sonarcloud.io/summary/new_code?id=davewalker5_NatureRecorderPy
    :alt: Quality Gate

.. image:: https://img.shields.io/github/issues/davewalker5/NatureRecorderPy
    :target: https://github.com/davewalker5/NatureRecorderPy/issues
    :alt: GitHub issues

.. image:: https://img.shields.io/github/v/release/davewalker5/NatureRecorderPy.svg?include_prereleases
    :target: https://github.com/davewalker5/NatureRecorderPy/releases
    :alt: Releases

.. image:: https://img.shields.io/badge/License-mit-blue.svg
    :target: https://github.com/davewalker5/NatureRecorderPy/blob/main/LICENSE
    :alt: License

.. image:: https://img.shields.io/badge/language-python-blue.svg
    :target: https://www.python.org
    :alt: Language

.. image:: https://img.shields.io/github/languages/code-size/davewalker5/NatureRecorderPy
    :target: https://github.com/davewalker5/NatureRecorderPy/
    :alt: GitHub code size in bytes


Nature Recorder
===============

Nature Recorder is an application for recording wildlife sightings, maintaining details of:

- Locations, with the following details:
    - Unique name
    - Address details
    - Latitude and longitude
- Categories, with the following details:
    - Category name e.g. birds, mammals
- Species, with the following details:
    - The category to which the species belongs
    - Species name
- Species sightings, consisting of:
    - The species, and by implication the category the species belongs to
    - Location
    - Date
    - Gender of the animals seen
    - Number of animals seen (optional)
    - Whether or not they were seen with young
- Conservation status information, consisting of:
    - Conservation schemes, acting as containers for a set of rating values
    - Conservation status ratings, values for the conservation status within a scheme
    - Species conservation status ratings, status ratings for a species with effective start and end dates

Structure
=========

+-------------------------------+----------------------------------------------------------------------+
| **Package**                   | **Contents**                                                         |
+-------------------------------+----------------------------------------------------------------------+
| naturerec_model               | Classes and business logic for the application                       |
+-------------------------------+----------------------------------------------------------------------+
| naturerec_web                 | A simple Flask-based web site built over the naturerec_model package |
+-------------------------------+----------------------------------------------------------------------+

Getting Started
===============

Please see the [Wiki](https://github.com/davewalker5/NatureRecorderPy/wiki) for configuration details and the user guide.

Authors
=======

- **Dave Walker** - _Initial work_ - [LinkedIn](https://www.linkedin.com/in/davewalker5/)

Feedback
========

To file issues or suggestions, please use the [Issues](https://github.com/davewalker5/NatureRecorderPy/issues) page for this project on GitHub.

License
=======

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
