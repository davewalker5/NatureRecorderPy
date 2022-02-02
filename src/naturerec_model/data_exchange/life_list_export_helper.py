"""
This module implements a helper that will export a life list to a CSV format file on a background thread
"""

import csv
import os
from .data_exchange_helper_base import DataExchangeHelperBase
from ..model import get_data_path
from ..logic.sightings import life_list


class LifeListExportHelper(DataExchangeHelperBase):
    JOB_NAME = "Life List export"
    COLUMN_NAMES = ["Category", "Species"]

    def __init__(self, filename, category_id):
        super().__init__(self.export)
        self._filename = filename
        self._category_id = category_id
        self.create_job_status()

    def __repr__(self):
        return f"{type(self).__name__}(" \
               f"filename={self._filename!r}, " \
               f"category_id={self._category_id!r})"

    def export(self):
        """
        Retrieve the life list matching the criteria passed to the init method and write it to file in CSV format
        """
        with open(self.get_file_export_path(), mode='wt', newline='', encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.COLUMN_NAMES)

            species = life_list(self._category_id)
            for species in species:
                writer.writerow([species.category.name, species.name])

    def get_file_export_path(self):
        """
        Construct and return the full path to the export file

        :return: Full path to the export file
        """
        export_folder = os.path.join(get_data_path(), "exports")
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        return os.path.join(export_folder, self._filename)
