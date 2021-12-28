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

import csv
import datetime
from io import StringIO
from .data_exchange_helper_base import DataExchangeHelperBase
from ..model import SpeciesStatusRating
from ..logic import get_status_scheme, create_status_scheme, create_status_rating
from ..logic import create_species_status_rating


class StatusImportHelper(DataExchangeHelperBase):
    def __init__(self, f):
        """
        Initialiser

        :param f: IO stream (result of open() or a FileStorage object)
        """
        super().__init__(self.import_ratings)
        self._file = f
        self._rows = []

    def import_ratings(self):
        """
        Import the conservation status rating file, row by row
        """
        self._read_csv_rows()
        for row in self._rows:
            species_id = self.create_species(row[1], row[0])
            rating_id = self._create_rating(row[2], row[3])
            start = datetime.datetime.strptime(row[5], SpeciesStatusRating.IMPORT_DATE_FORMAT).date()
            end = datetime.datetime.strptime(row[6], SpeciesStatusRating.IMPORT_DATE_FORMAT).date() \
                if row[6].strip() else None
            _ = create_species_status_rating(species_id, rating_id, row[4].strip(), start, end)

    def _read_csv_rows(self):
        """
        Read the import file and return a set of valid rows

        :return: List of CSV row objects
        :raises ValueError: If there are unexpected blanks or a malformed row
        """
        self._rows = []

        # The data source could've been opened in binary or text mode, so read it all then decode it if necessary.
        # Layout files are small so reading all their content into memory shouldn't be problematic
        data = self._file.read()
        csv_text = data if isinstance(data, str) else data.decode("UTF-8")

        # Initialise a CSV reader over the string memory buffer and read and discard the header row
        csv_io = StringIO(csv_text)
        reader = csv.reader(csv_io)
        _ = next(reader, None)

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
    def _create_rating(scheme_name, rating_name):
        """
        Ensure the rating with the specified name exists in the specified scheme

        :param scheme_name: Name of the conservation status scheme to which the rating belongs
        :param rating_name: Name of the rating
        """
        tidied_scheme_name = " ".join(scheme_name.split())
        tidied_rating_name = " ".join(rating_name.split()).title()

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
