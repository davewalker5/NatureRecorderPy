import unittest
import os
from src.naturerec_model.model import create_database, get_data_path
from src.naturerec_model.logic import get_category, create_category
from src.naturerec_model.logic import create_species
from src.naturerec_model.logic import get_status_scheme, create_status_scheme, create_status_rating
from src.naturerec_model.logic import list_species_status_ratings
from src.naturerec_model.logic import list_job_status
from src.naturerec_model.data_exchange import StatusImportHelper


class TestStatusImportHelper(unittest.TestCase):
    def setUp(self) -> None:
        create_database()

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
        filename = os.path.join(get_data_path(), "valid_status_import.csv")
        TestStatusImportHelper._create_test_file(filename, [
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,BOCC5,Red,United Kingdom,01/12/2021,\n"
        ])

        # Import the statuses
        with open(filename, mode="rt", encoding="UTF-8") as f:
            exporter = StatusImportHelper(f)
            exporter.start()
            exporter.join()
        os.unlink(filename)

        # Check the scheme was imported correctly
        scheme = get_status_scheme("BOCC5")
        self.assertIsNotNone(scheme)
        self.assertEqual(1, len(scheme.ratings))
        self.assertEqual("Red", scheme.ratings[0].name)

        # Check the category and species were imported correctly
        category = get_category("Birds")
        self.assertIsNotNone(category)
        self.assertEqual(1, len(category.species))
        self.assertEqual("Arctic Skua", category.species[0].name)

        # Check the rating was imported correctly
        ratings = list_species_status_ratings(species_id=category.species[0].id)
        self.assertEqual(1, len(ratings))
        self.assertEqual(category.species[0].id, ratings[0].speciesId)
        self.assertEqual(scheme.ratings[0].id, ratings[0].statusRatingId)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual("2021-12-01 00:00:00", ratings[0].start)
        self.assertIsNone(ratings[0].end)

        # Confirm the job status record was created
        job_statuses = list_job_status()
        self.assertEqual(1, len(job_statuses))
        self.assertEqual(StatusImportHelper.JOB_NAME, job_statuses[0].name)
        self.assertIsNotNone(job_statuses[0].display_end_date)
        self.assertIsNone(job_statuses[0].error)

    def _perform_invalid_import(self, rows):
        """
        Helper to perform an import on an invalid file and confirm the expected error is raised

        :param rows: List of rows of data to write to the file
        """
        filename = os.path.join(get_data_path(), "invalid_status_import.csv")
        TestStatusImportHelper._create_test_file(filename, rows)

        with open(filename, mode="rt", encoding="UTF-8") as f:
            exporter = StatusImportHelper(f)
            exporter.start()
            with self.assertRaises(ValueError):
                exporter.join()

        os.unlink(filename)

        # Confirm the job status record was created
        job_statuses = list_job_status()
        self.assertEqual(1, len(job_statuses))
        self.assertEqual(StatusImportHelper.JOB_NAME, job_statuses[0].name)
        self.assertIsNotNone(job_statuses[0].display_end_date)
        self.assertIsNotNone(job_statuses[0].error)

    def test_can_import_status(self):
        self._perform_valid_import()

    def test_can_import_status_for_existing_category(self):
        _ = create_category("Birds")
        self._perform_valid_import()

    def test_can_import_status_for_existing_species(self):
        category = create_category("Birds")
        _ = create_species(category.id, "Arctic Skua")
        self._perform_valid_import()

    def test_can_import_status_for_existing_scheme(self):
        _ = create_status_scheme("BOCC5")
        self._perform_valid_import()

    def test_can_import_status_for_existing_rating(self):
        scheme = create_status_scheme("BOCC5")
        _ = create_status_rating(scheme.id, "Red")
        self._perform_valid_import()

    def test_cannot_import_file_with_blank_species(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            ",Birds,BOCC5,Red,United Kingdom,01/12/2021,\n"
        ])

    def test_cannot_import_file_with_blank_category(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,,BOCC5,Red,United Kingdom,01/12/2021,\n"
        ])

    def test_cannot_import_file_with_blank_scheme(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,,Red,United Kingdom,01/12/2021,\n"
        ])

    def test_cannot_import_file_with_blank_rating(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,BOCC5,,United Kingdom,01/12/2021,\n"
        ])

    def test_cannot_import_file_with_blank_region(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,BOCC5,Red,,01/12/2021,\n"
        ])

    def test_cannot_import_file_with_blank_start(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,BOCC5,Red,United Kingdom,,\n"
        ])

    def test_cannot_import_file_with_invalid_start(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,BOCC5,Red,United Kingdom,Not A Date,\n"
        ])

    def test_cannot_import_file_with_invalid_end(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,BOCC5,Red,United Kingdom,01/12/2021,Not A Date\n"
        ])

    def test_cannot_import_file_with_malformed_row(self):
        self._perform_invalid_import([
            "Species,Category,Scheme,Rating,Region,Start,End\n",
            "Arctic skua,Birds,BOCC5,\n"
        ])
