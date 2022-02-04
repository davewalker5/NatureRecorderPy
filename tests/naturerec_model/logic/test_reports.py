import unittest
import datetime
from src.naturerec_model.model import create_database, Gender
from src.naturerec_model.logic import create_category, create_species, create_location, create_sighting
from src.naturerec_model.logic import location_individuals_report, location_days_report


class TestLocations(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._category = create_category("Birds")
        species = create_species(self._category.id, "Black-Headed Gull")
        self._location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom")
        create_sighting(self._location.id, species.id, datetime.date(2021, 12, 14), 30, Gender.UNKNOWN, False)

    def test_can_get_location_individuals_report(self):
        report, column_names = location_individuals_report(datetime.date(2021, 12, 1), self._location.id,
                                                           self._category.id)

        self.assertEqual(1, len(report))
        keys = [key for key in report[0].keys()]
        self.assertEqual("Species", keys[0])
        self.assertEqual("Count", keys[1])
        self.assertEqual("Black-Headed Gull", report[0]["Species"])
        self.assertEqual(30, report[0]["Count"])

        self.assertEqual(2, len(column_names))
        self.assertTrue("Species" in column_names)
        self.assertTrue("Count" in column_names)

    def test_can_get_location_sightings_report(self):
        report, column_names = location_days_report(datetime.date(2021, 12, 1), self._location.id, self._category.id)

        self.assertEqual(1, len(report))
        keys = [key for key in report[0].keys()]
        self.assertEqual("Species", keys[0])
        self.assertEqual("Count", keys[1])
        self.assertEqual("Black-Headed Gull", report[0]["Species"])
        self.assertEqual(1, report[0]["Count"])

        self.assertEqual(2, len(column_names))
        self.assertTrue("Species" in column_names)
        self.assertTrue("Count" in column_names)
