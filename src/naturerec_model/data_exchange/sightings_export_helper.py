"""
This module implements a helper that will export sightings to a CSV format file on a background thread
"""

import csv
import os
from .sightings_data_exchange_helper_base import SightingsDataExchangeHelperBase
from ..model import get_data_path
from ..logic.sightings import list_sightings


class SightingsExportHelper(SightingsDataExchangeHelperBase):
    JOB_NAME = "Sightings export"

    def __init__(self, filename, from_date=None, to_date=None, location_id=None, species_id=None):
        super().__init__(self.export)
        self._filename = filename
        self._from_date = from_date
        self._to_date = to_date
        self._location_id = location_id
        self._species_id = species_id
        self.create_job_status()

    def __repr__(self):
        return f"{type(self).__name__}(" \
               f"filename={self._filename!r}, " \
               f"from_date={self._from_date!r}, " \
               f"to_date={self._to_date!r}, " \
               f"location_id={self._location_id!r}, " \
               f"species_id={self._species_id!r})"

    def export(self):
        """
        Retrieve a set of sightings matching the criteria passed to the init method and write
        them to file in CSV format
        """
        with open(self.get_file_export_path(), mode='wt', newline='', encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.COLUMN_NAMES)

            sightings = list_sightings(self._from_date, self._to_date, self._location_id, self._species_id)
            for sighting in sightings:
                writer.writerow(sighting.csv_columns)

    def get_file_export_path(self):
        """
        Construct and return the full path to the export file

        :return: Full path to the export file
        """
        export_folder = os.path.join(get_data_path(), "exports")
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        return os.path.join(export_folder, self._filename)
