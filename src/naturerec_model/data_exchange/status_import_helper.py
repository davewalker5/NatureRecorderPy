"""
This module implements a helper that will import conservation status schemes, ratings and species ratings on a
background thread. The source for the import is a CSV file with the following columns:

+----------+-----------------------------------------------------------------------------+
| Column   | Contents                                                                    |
+----------+-----------------------------------------------------------------------------+
| Species  | Name of the species                                                         |
+----------+-----------------------------------------------------------------------------+
| Category | Category to which the species belongs                                       |
+----------+-----------------------------------------------------------------------------+
| Scheme   | Name of the conservation status scheme                                      |
+----------+-----------------------------------------------------------------------------+
| Rating   | Name of the rating on that scheme e.g. Red, Amber, Green                    |
+----------+-----------------------------------------------------------------------------+
| Region   | Region of the world to which the rating applies e.g. United Kingdom         |
+----------+-----------------------------------------------------------------------------+
| Start    | The start date for the rating in DD/MM/YYYY format                          |
+----------+-----------------------------------------------------------------------------+
| End      | The end date for the rating in DD/MM/YYYY format or a blank for no end date |
+----------+-----------------------------------------------------------------------------+

The header row must be present but is ignored. Categories, species, schemes and ratings are created as required.
"""

import threading
import csv
import datetime
from naturerec_model.model import SpeciesStatusRating
from naturerec_model.logic import create_category, get_category
from naturerec_model.logic import create_species
from naturerec_model.logic import get_status_scheme, create_status_scheme, create_status_rating
from naturerec_model.logic import create_species_status_rating


class StatusImportHelper(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self._filename = filename
        self._rows = []
        self._exception = None

    def import_ratings(self):
        """
        Import the conservation status rating file, row by row
        """
        self._read_csv_rows()
        for row in self._rows:
            species_id = self._create_species(row[1], row[0])
            rating_id = self._create_rating(row[2], row[3])
            start = datetime.datetime.strptime(row[5], SpeciesStatusRating.IMPORT_DATE_FORMAT).date()
            end = datetime.datetime.strptime(row[6], SpeciesStatusRating.IMPORT_DATE_FORMAT).date() \
                if row[6].strip() else None
            _ = create_species_status_rating(species_id, rating_id, row[4].strip(), start, end)

    def run(self, *args, **kwargs):
        """
        Import conservation status schemes and ratings from a CSV file on a background thread

        :param args: Variable positional arguments
        :param kwargs: Variable keyword arguments
        """
        try:
            self.import_ratings()
        except BaseException as e:
            # If we get an error during import, capture it. join(), below, then raises it in the calling
            # thread
            self._exception = e

    def join(self):
        """
        If we have an exception, raise it in the calling thread when joined
        """
        threading.Thread.join(self)
        if self._exception:
            raise self._exception

    def _read_csv_rows(self):
        """
        Read the import file and return a set of valid rows

        :return: List of CSV row objects
        :raises ValueError: If there are unexpected blanks or a malformed row
        """
        self._rows = []
        with open(self._filename, mode="rt", encoding="UTF-8") as f:
            # Skip the headers
            reader = csv.reader(f)
            next(reader)

            # Build an in-memory collection of  CSV rows. As the conservation status files are small, this won't
            # be too much of an overhead and saves reading the file twice
            for row in reader:
                # Must have the right number of columns
                if len(row) != 7:
                    raise ValueError(f"Malformed data at row {len(self._rows) + 1}")

                # All bar the final column in the row (the end date) must have a value
                for i in range(0, 6):
                    if not row[i].strip():
                        raise ValueError(f"Missing data at row {len(self._rows) + 1}")

                # Start date must be in the right format
                try:
                    _ = datetime.datetime.strptime(row[5], SpeciesStatusRating.IMPORT_DATE_FORMAT).date()
                except ValueError as e:
                    raise ValueError(f"Invalid start date format at row {len(self._rows) + 1}") from e

                # Ditto the end date, if specified
                if row[6].strip():
                    try:
                        _ = datetime.datetime.strptime(row[6], SpeciesStatusRating.IMPORT_DATE_FORMAT).date()
                    except ValueError as e:
                        raise ValueError(f"Invalid end date format at row {len(self._rows) + 1}") from e

                self._rows.append(row)

    @staticmethod
    def _create_species(category_name, species_name):
        """
        Ensure the species with the specified name exists in the specified category

        :param category_name: Name of the category to which the species belongs
        :param species_name: Name of the species
        """
        tidied_category_name = category_name.strip()
        tidied_species_name = species_name.strip()

        # See if the category exists and, if not, create it and the species
        try:
            category = get_category(tidied_category_name)
        except ValueError:
            category = create_category(tidied_category_name)
            return create_species(category.id, tidied_species_name).id

        # See if the species exists against the existing category. If so, just return its ID
        species_ids = [species.id for species in category.species if species.name == tidied_species_name]
        if len(species_ids):
            return species_ids[0]

        # Doesn't exist so create it and return its ID
        return create_species(category.id, tidied_species_name).id

    @staticmethod
    def _create_rating(scheme_name, rating_name):
        """
        Ensure the rating with the specified name exists in the specified scheme

        :param scheme_name: Name of the conservation status scheme to which the rating belongs
        :param rating_name: Name of the rating
        """
        tidied_scheme_name = scheme_name.strip()
        tidied_rating_name = rating_name.strip()

        # See if the category exists and, if not, create it and the species
        try:
            scheme = get_status_scheme(tidied_scheme_name)
        except ValueError:
            scheme = create_status_scheme(tidied_scheme_name)
            return create_status_rating(scheme.id, tidied_rating_name).id

        # See if the rating exists against the existing scheme. If so, just return its ID
        rating_ids = [rating.id for rating in scheme.ratings if rating.name == tidied_rating_name]
        if len(rating_ids):
            return rating_ids[0]

        # Doesn't exist so create it and return its ID
        return create_status_rating(scheme.id, tidied_rating_name).id
