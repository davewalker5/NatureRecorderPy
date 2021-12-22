import threading
import csv
import os
from src.naturerec_model.model import get_data_path
from naturerec_model.logic.sightings import list_sightings


class CsvExportHelper(threading.Thread):
    COLUMN_NAMES = [
        'Species',
        'Category',
        'Number',
        'Gender',
        'WithYoung',
        'Date',
        'Location',
        'Address',
        'City',
        'County',
        'Postcode',
        'Country',
        'Latitude',
        'Longitude'
    ]

    def __init__(self, filename, from_date=None, to_date=None, location_id=None, species_id=None):
        threading.Thread.__init__(self)
        self._filename = filename
        self._from_date = from_date
        self._to_date = to_date
        self._location_id = location_id
        self._species_id = species_id

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

    def run(self, *args, **kwargs):
        """
        Export sightings to a CSV file on a background thread

        :param args: Variable positional arguments
        :param kwargs: Variable keyword arguments
        """
        self.export()

    def get_file_export_path(self):
        """
        Construct and return the full path to the export file

        :return: Full path to the export file
        """
        export_folder = os.path.join(get_data_path(), "exports")
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        return os.path.join(export_folder, self._filename)
