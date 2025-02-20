import unittest
import os
from naturerec_model.data_exchange.sightings_import_helper import SightingsImportHelper
from naturerec_model.model import create_database, get_data_path, Gender, User
from naturerec_model.logic import create_category, get_category
from naturerec_model.logic import create_species
from naturerec_model.logic import create_location, get_location
from naturerec_model.logic import list_sightings
from naturerec_model.logic import list_job_status


class TestSightingsImportHelper(unittest.TestCase):
    IMPORT_FILE_HEADER_ROW = "Species,Scientific Name,Category,Number,Gender,WithYoung,Date,Location,Address,City,County,Postcode," \
                             "Country,Latitude,Longitude\n"

    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)

    @staticmethod
    def _create_test_file(filename, rows):
        """
        Helper to create a CSV file with test data

        :param filename: Full path to the CSV file
        :param rows: List of CSV-format row data
        """
        with open(filename, mode="wt", encoding="UTF-8") as f:
            f.writelines(rows)

    def _perform_valid_import(self):
        """
        Helper to run an import and confirm that it has completed successfully
        """

        # Create the test file
        filename = os.path.join(get_data_path(), "valid_sightings_import.csv")
        TestSightingsImportHelper._create_test_file(filename, [
            "Species,Scientific Name,Category,Number,Gender,WithYoung,Date,Location,Address,City,County,Postcode,Country,"
            "Latitude,Longitude,Notes\n",
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,-1.2880,\n"
        ])

        # Import the sightings
        with open(filename, mode="rt", encoding="UTF-8") as f:
            exporter = SightingsImportHelper(f, self._user)
            exporter.start()
            exporter.join()
        os.unlink(filename)

        # Check the species was imported correctly
        category = get_category("Birds")
        self.assertEqual(1, len(category.species))
        self.assertEqual("Robin", category.species[0].name)
        self.assertEqual("Erithacus rubecula", category.species[0].scientific_name)

        # Check the location was imported correctly
        location = get_location("Abingdon")
        self.assertEqual("An Address", location.address)
        self.assertEqual("Abingdon", location.city)
        self.assertEqual("Oxfordshire", location.county)
        self.assertEqual("OX14", location.postcode)
        self.assertEqual("United Kingdom", location.country)
        self.assertEqual(51.6708, location.latitude)
        self.assertEqual(-1.2880, location.longitude)

        # Check the sighting imported correctly
        sightings = list_sightings()
        self.assertEqual(1, len(sightings))
        self.assertEqual(category.species[0].id, sightings[0].speciesId)
        self.assertEqual(location.id, sightings[0].locationId)
        self.assertEqual(1, sightings[0].number)
        self.assertEqual(Gender.UNKNOWN, sightings[0].gender)
        self.assertEqual(0, sightings[0].withYoung)
        self.assertEqual("2021-02-01 00:00:00", sightings[0].date)

        # Confirm the job status record was created
        job_statuses = list_job_status()
        self.assertEqual(1, len(job_statuses))
        self.assertEqual(SightingsImportHelper.JOB_NAME, job_statuses[0].name)
        self.assertIsNotNone(job_statuses[0].display_end_date)
        self.assertIsNone(job_statuses[0].error)

    def _perform_invalid_import(self, rows):
        """
        Helper to perform an import on an invalid file and confirm the expected error is raised

        :param rows: List of rows of data to write to the file
        """
        filename = os.path.join(get_data_path(), "invalid_sightings_import.csv")
        TestSightingsImportHelper._create_test_file(filename, rows)

        with open(filename, mode="rt", encoding="UTF-8") as f:
            importer = SightingsImportHelper(f, self._user)
            importer.start()
            with self.assertRaises(ValueError):
                importer.join()

        os.unlink(filename)

        # Confirm the job status record was created
        job_statuses = list_job_status()
        self.assertEqual(1, len(job_statuses))
        self.assertEqual(SightingsImportHelper.JOB_NAME, job_statuses[0].name)
        self.assertIsNotNone(job_statuses[0].display_end_date)
        self.assertIsNotNone(job_statuses[0].error)

    def test_can_import_sightings(self):
        self._perform_valid_import()

    def test_can_import_sighting_for_existing_category(self):
        _ = create_category("Birds", True, self._user)
        self._perform_valid_import()

    def test_can_import_sighting_for_existing_species(self):
        category = create_category("Birds", True, self._user)
        _ = create_species(category.id, "Robin", "Erithacus rubecula", self._user)
        self._perform_valid_import()

    def test_can_import_sighting_for_existing_location(self):
        _ = create_location("Abingdon", "Oxfordshire", "United Kingdom", self._user, "An Address", "Abingdon", "OX14", 51.6708,
                            -1.2880)
        self._perform_valid_import()

    def test_cannot_import_duplicate_sighting(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,-1.2880\n",
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_blank_species(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            ",Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_blank_category(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_invalid_number(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,Not A Number,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,"
            "United Kingdom,51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_invalid_gender(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Not A Valid Gender,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,"
            "United Kingdom,51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_invalid_with_young(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,Not A Valid With Young Value,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,"
            "OX14,United Kingdom,51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_invalid_date(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,Not A Date,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_blank_location(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_blank_county(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,,OX14,United Kingdom,"
            "51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_blank_country(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,,"
            "51.6708,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_invalid_latitude(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "Not A Decimal,-1.2880\n"
        ])

    def test_cannot_import_sighting_with_invalid_longitude(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon,An Address,Abingdon,Oxfordshire,OX14,United Kingdom,"
            "51.6708,Not A Decimal\n"
        ])

    def test_cannot_import_file_with_malformed_row(self):
        self._perform_invalid_import([
            TestSightingsImportHelper.IMPORT_FILE_HEADER_ROW,
            "Robin,Erithacus rubecula,Birds,1,Unknown,No,01/02/2021,Abingdon\n"
        ])
