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


Running the Application
=======================

Pre-requisites
--------------

To run the application, a virtual environment should be created, the requirements should be installed using pip and the
environment should be activated.


Creating an Empty Database
--------------------------

With the pre-requisites in place, an empty database with the correct schema in place can be created by running the
following commands from the root of the project:

::

    export NATURE_RECORDER_DB="`pwd`/data/naturerecorder.db"
    export PYTHONPATH=`pwd`/src
    python -m naturerec_model

The first command will need to be modified based on the current operating system.


Adding a User to the Database
-----------------------------

Once the database has been created, enter the following commands from the root of the project to prompt for a
username and password and add that user to the database:

::

    export NATURE_RECORDER_DB="`pwd`/data/naturerecorder.db"
    export PYTHONPATH=`pwd`/src
    python add_user.py

The first two commands will need to be modified based on the current operating system.


Running the Web Application
---------------------------

To run the web-based application in the Flask development web server, enter the following from the
"src/naturerec_web" folder:

::

    export NATURE_RECORDER_DB="`pwd`/../../data/naturerecorder.db"
    export PYTHONPATH=`pwd`/..
    export FLASK_APP=naturerecorder.py
    export FLASK_ENV=development
    flask run

The first four commands will need to be modified based on the current operating system. Once the development server
is running, browse to the following URL in a  web browser:

::

    http://127.0.0.1:5000/


Unit Tests and Coverage
=======================

Currently, the unit tests use a SQLite database as the back-end rather than mocking the database.

To run the unit tests, a virtual environment should be created, the requirements should be installed using pip and the
environment should be activated.

The tests can then be run from the command line, at the root of the project folder, as follows:

::

    export PYTHONPATH=`pwd`/src/
    python -m unittest

The first command adds the source folder, containing the two packages under test, to the PYTHONPATH environment
variable so the packages will be found when the tests attempt to import them. The command will need to be modified
based on the current operating system.

Similarly, a coverage report can be generated by running the following commands from the root of the project folder:

::

    export PYTHONPATH=`pwd`/src/
    coverage run --branch --source src -m unittest discover
    coverage html -d cov_html

This will create a folder "cov_html" containing the coverage report in HTML format.


Generating Documentation
========================

To generate the documentation, a virtual environment should be created, the requirements should be installed
using pip and the environment should be activated.

HTML documentation can then be created by running the following commands from the "docs" sub-folder:

::

    export PYTHONPATH=`pwd`/../src/
    make html

The resulting documentation is written to the docs/build/html folder and can be viewed by opening "index.html" in a
web browser.


Dependencies
============

The nature recorder application has dependencies listed in requirements.txt.


Distribution
============

A distribution can be created that includes both the "naturerec_model" and "naturerec_web" packages by running the
following from a command prompt at the root of the project:

::

    python setup.py bdist_wheel

Note that the project's virtual environment should **not** be activated when creating distributions.


License
=======

This software is licensed under the MIT License:

https://opensource.org/licenses/MIT

Copyright 2021 David Walker

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
