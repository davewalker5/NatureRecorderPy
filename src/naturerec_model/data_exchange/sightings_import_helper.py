"""
This module implements a helper that will import sightings from a CSV format file on a background thread
"""

import csv
import datetime
from io import StringIO
from .sightings_data_exchange_helper_base import SightingsDataExchangeHelperBase
from ..model import Gender, Sighting
from ..logic import create_location, get_location
from ..logic import create_sighting


class SightingsImportHelper(SightingsDataExchangeHelperBase):
    JOB_NAME = "Sightings import"

    def __init__(self, f):
        """
        Initialiser

        :param f: IO stream (result of open() or a FileStorage object)
        """
        super().__init__(self.import_sightings)
        self._file = f
        self.create_job_status()

    def __repr__(self):
        return f"{type(self).__name__}(f={self._file!r})"

    def import_sightings(self):
        """
        Import the sightings, row by row
        """
        self._read_csv_rows()
        for row in self._rows:
            species_id = self.create_species(row[1], row[0])
            location_id = self._create_location(row)
            date = datetime.datetime.strptime(row[5], Sighting.DATE_IMPORT_FORMAT).date()
            number = int(row[2]) if row[2].strip() else None
            gender = [key for key, value in Gender.gender_map().items() if value == row[3].strip().title()][0]
            with_young = 1 if row[4].strip().title() == "Yes" else 0
            notes = row[14] if row[14] else None
            _ = create_sighting(location_id, species_id, date, number, gender, with_young, notes)

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

        # Build an in-memory collection of CSV rows. As the import files should be relatively small, this won't
        # be too much of an overhead and saves reading the file twice
        for row in reader:
            self._validate_row(row, len(self._rows) + 1)
            self._rows.append(row)

    @classmethod
    def _validate_row(cls, row, row_number):
        """
        Validate all the fields in a CSV import row

        :param row: CSV row (collection of fields)
        :param row_number: Row number for error reporting
        """
        if len(row) != 15:
            raise ValueError(f"Malformed data at row {row_number}")

        cls._check_not_empty(row, 0, row_number)            # Species
        cls._check_not_empty(row, 1, row_number)            # Category
        cls._check_valid_int(row, 2, row_number, True)      # Number

        # Gender
        cls._check_valid_value(row, 3, row_number, Gender.gender_map().values())

        # With Young
        cls._check_valid_value(row, 4, row_number, ["Yes", "No"])

        cls._check_valid_date(row, 5, row_number)           # Date
        cls._check_not_empty(row, 6, row_number)            # Location
        cls._check_not_empty(row, 9, row_number)            # County
        cls._check_not_empty(row, 11, row_number)           # Country
        cls._check_valid_float(row, 12, row_number, True)   # Latitude
        cls._check_valid_float(row, 13, row_number, True)   # Longitude

    @classmethod
    def _check_not_empty(cls, row, index, row_number):
        """
        Check a field in a CSV row isn't empty

        :param row: CSV row (collection of fields)
        :param index: Field index
        :param row_number: Row number for error reporting
        :raises ValueError: If the field is empty
        """
        if not row[index].strip():
            raise ValueError(f"Missing value for {cls.get_field_name(index)} on row {row_number}")

    @classmethod
    def _check_valid_value(cls, row, index, row_number, valid_values):
        """
        Check a field in a CSV row is a valid floating point number

        :param row: CSV row (collection of fields)
        :param index: Field index
        :param row_number: Row number for error reporting
        :param valid_values: Collection of valid values to compare with
        :raises ValueError: If the field isn't in the valid values collection
        """
        if not row[index].strip().title() in valid_values:
            raise ValueError(f"Invalid value for {cls.get_field_name(index)} on row {row_number}")

    @classmethod
    def _check_valid_int(cls, row, index, row_number, can_be_empty):
        """
        Check a field in a CSV row is a valid integer

        :param row: CSV row (collection of fields)
        :param index: Field index
        :param row_number: Row number for error reporting
        :param can_be_empty: True if the value can be empty
        :raises ValueError: If the field isn't a valid int
        """
        value = row[index].strip()
        if value:
            try:
                _ = int(value)
            except ValueError:
                raise ValueError(f"Invalid value for {cls.get_field_name(index)} on row {row_number}")
        elif not can_be_empty:
            raise ValueError(f"{cls.get_field_name(index)} cannot be empty on row {row_number}")

    @classmethod
    def _check_valid_float(cls, row, index, row_number, can_be_empty):
        """
        Check a field in a CSV row is a valid floating point number

        :param row: CSV row (collection of fields)
        :param index: Field index
        :param row_number: Row number for error reporting
        :param can_be_empty: True if the value can be empty
        :raises ValueError: If the field isn't a valid float
        """
        value = row[index].strip()
        if value:
            try:
                _ = float(value)
            except ValueError:
                raise ValueError(f"Invalid value for {cls.get_field_name(index)} on row {row_number}")
        elif not can_be_empty:
            raise ValueError(f"{cls.get_field_name(index)} cannot be empty on row {row_number}")

    @classmethod
    def _check_valid_date(cls, row, index, row_number):
        """
        Check a field in a CSV row is a valid date

        :param row: CSV row (collection of fields)
        :param index: Field index
        :param row_number: Row number for error reporting
        :raises ValueError: If the field isn't a valid date
        """
        try:
            _ = datetime.datetime.strptime(row[index], Sighting.DATE_IMPORT_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid value for {cls.get_field_name(index)} on row {row_number}")

    @staticmethod
    def _create_location(row):
        tidied_name = " ".join(row[6].split()).title()
        try:
            location = get_location(tidied_name)
        except ValueError:
            latitude = float(row[12]) if row[12].strip() else None
            longitude = float(row[13]) if row[12].strip() else None
            location = create_location(tidied_name, row[9], row[11], row[7], row[8], row[10], latitude, longitude)
        return location.id
