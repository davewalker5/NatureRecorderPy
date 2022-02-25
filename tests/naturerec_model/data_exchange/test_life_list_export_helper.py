import unittest
import datetime
import csv
from src.naturerec_model.model import create_database, Gender
from src.naturerec_model.logic import create_category
from src.naturerec_model.logic import create_species
from src.naturerec_model.logic import create_location
from src.naturerec_model.logic import create_sighting
from src.naturerec_model.logic import list_job_status
from src.naturerec_model.data_exchange import LifeListExportHelper


class TestSightingsExportHelper(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._category = create_category("Birds")
        self._gull = create_species(self._category.id, "Black-Headed Gull")
        self._location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom")
        _ = create_sighting(self._location.id, self._gull.id, datetime.date(2021, 12, 14), None, Gender.UNKNOWN, False,
                            None)

    def test_can_export_life_list(self):
        # Export the sightings
        exporter = LifeListExportHelper(filename="life_list_export.csv", category_id=self._category.id)
        exporter.start()
        exporter.join()

        # Read the file
        rows = []
        with open(exporter.get_file_export_path(), mode="rt", encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        self.assertEqual(2, len(rows))
        self.assertEqual(LifeListExportHelper.COLUMN_NAMES, rows[0])
        self.assertEqual(2, len(rows[1]))
        self.assertEqual("Birds", rows[1][0])
        self.assertEqual("Black-Headed Gull", rows[1][1])

        # Confirm the job status record was created
        job_statuses = list_job_status()
        self.assertEqual(1, len(job_statuses))
        self.assertEqual(LifeListExportHelper.JOB_NAME, job_statuses[0].name)
        self.assertIsNotNone(job_statuses[0].display_end_date)
        self.assertIsNone(job_statuses[0].error)
