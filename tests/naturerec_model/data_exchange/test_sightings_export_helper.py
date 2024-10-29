import unittest
import datetime
import csv
from naturerec_model.model import create_database, Gender, User
from naturerec_model.logic import create_category
from naturerec_model.logic import create_species
from naturerec_model.logic import create_location
from naturerec_model.logic import create_sighting
from naturerec_model.logic import list_job_status
from naturerec_model.data_exchange import SightingsExportHelper


class TestSightingsExportHelper(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        self._category = create_category("Birds", self._user)
        self._gull = create_species(self._category.id, "Black-Headed Gull", "Chroicocephalus ridibundus", self._user)
        self._cormorant = create_species(self._category.id, "Cormorant", "Phalacrocorax carbo", self._user)
        self._location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom", user=self._user)
        _ = create_sighting(self._location.id, self._gull.id, datetime.date(2021, 12, 14), None, Gender.UNKNOWN, False,
                            None, self._user)

    def test_can_export_sightings(self):
        # Export the sightings
        exporter = SightingsExportHelper(filename="export.csv", user=self._user)
        exporter.start()
        exporter.join()

        # Read the file
        rows = []
        with open(exporter.get_file_export_path(), mode="rt", encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        self.assertEqual(2, len(rows))
        self.assertEqual(SightingsExportHelper.COLUMN_NAMES, rows[0])
        self.assertEqual(16, len(rows[1]))
        self.assertEqual("Black-Headed Gull", rows[1][0])
        self.assertEqual("Chroicocephalus Ridibundus", rows[1][1])
        self.assertEqual("Birds", rows[1][2])
        self.assertEqual("", rows[1][3])
        self.assertEqual("Unknown", rows[1][4])
        self.assertEqual("No", rows[1][5])
        self.assertEqual("14/12/2021", rows[1][6])
        self.assertEqual("Radley Lakes",  rows[1][7])
        self.assertEqual("", rows[1][8])
        self.assertEqual("", rows[1][9])
        self.assertEqual("Oxfordshire",  rows[1][10])
        self.assertEqual("", rows[1][11])
        self.assertEqual("United Kingdom",  rows[1][12])
        self.assertEqual("", rows[1][13])
        self.assertEqual("", rows[1][14])

        # Confirm the job status record was created
        job_statuses = list_job_status()
        self.assertEqual(1, len(job_statuses))
        self.assertEqual(SightingsExportHelper.JOB_NAME, job_statuses[0].name)
        self.assertIsNotNone(job_statuses[0].display_end_date)
        self.assertIsNone(job_statuses[0].error)
