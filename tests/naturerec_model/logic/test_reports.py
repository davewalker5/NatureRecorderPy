import unittest
import datetime
from naturerec_model.model import create_database, Gender, User
from naturerec_model.logic import create_category, create_species, create_location, create_sighting
from naturerec_model.logic import location_species_report, get_report_barchart, species_by_date_report


class TestLocations(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        self._category = create_category("Birds", self._user)
        self._species = create_species(self._category.id, "Black-Headed Gull", self._user)
        self._location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom", user=self._user)
        create_sighting(self._location.id, self._species.id, datetime.date(2021, 12, 14), 30, Gender.UNKNOWN, False,
                        None, self._user)

    def test_can_get_location_species_report(self):
        report_df = location_species_report(datetime.date(2021, 12, 1), datetime.datetime.today(), self._location.id,
                                            self._category.id)
        self.assertEqual(1, len(report_df.index))
        self.assertTrue("Black-Headed Gull" in report_df.index)
        self.assertEqual(1, report_df.loc["Black-Headed Gull", "Sightings"])
        self.assertEqual(30, report_df.loc["Black-Headed Gull", "Total Individuals"])
        self.assertEqual(30, report_df.loc["Black-Headed Gull", "Minimum Seen"])
        self.assertEqual(30, report_df.loc["Black-Headed Gull", "Maximum Seen"])
        self.assertEqual(30, report_df.loc["Black-Headed Gull", "Average Seen"])

    def test_can_get_species_by_date_report(self):
        report_df = species_by_date_report(datetime.date(2021, 12, 1), datetime.datetime.today(), self._location.id,
                                           self._species.id, False)
        self.assertEqual(1, len(report_df.index))
        self.assertEqual(1, report_df.loc["Dec", "Sightings"])
        self.assertEqual(30, report_df.loc["Dec", "Minimum Seen"])
        self.assertEqual(30, report_df.loc["Dec", "Maximum Seen"])
        self.assertEqual(30, report_df.loc["Dec", "Average Seen"])

    def test_can_get_report_barchart_base64(self):
        report_df = location_species_report(datetime.date(2021, 12, 1), datetime.datetime.today(), self._location.id,
                                            self._category.id)
        base64 = get_report_barchart(report_df, "Total Individuals", "Species", "Total", "Title", "Subtitle", None)
        self.assertTrue(len(base64) > 0)
