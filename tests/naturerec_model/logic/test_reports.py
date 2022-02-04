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
        report_df = location_individuals_report(datetime.date(2021, 12, 1), self._location.id, self._category.id)
        self.assertEqual(1, len(report_df.index))
        self.assertTrue("Black-Headed Gull" in report_df.index)
        self.assertEqual(30, report_df.loc["Black-Headed Gull", "Count"])

    def test_can_get_location_sightings_report(self):
        report_df = location_days_report(datetime.date(2021, 12, 1), self._location.id, self._category.id)
        self.assertEqual(1, len(report_df.index))
        self.assertTrue("Black-Headed Gull" in report_df.index)
        self.assertEqual(1, report_df.loc["Black-Headed Gull", "Count"])
