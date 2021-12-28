import unittest
import datetime
from src.naturerec_model.model import create_database
from src.naturerec_model.logic import create_job_status, list_job_status, complete_job_status


class TestJobStatus(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        _ = create_job_status("A Test Job", "Some Job Parameters", datetime.datetime(2021, 12, 1, 10, 45, 0))

    def test_can_create_job_status(self):
        job_statuses = list_job_status()
        self.assertEqual(1, len(job_statuses))
        self.assertEqual("A Test Job", job_statuses[0].name)
        self.assertEqual("Some Job Parameters", job_statuses[0].parameters)
        self.assertEqual("01/12/2021 10:45:00", job_statuses[0].display_start_date)
        self.assertIsNone(job_statuses[0].display_end_date)
        self.assertIsNone(job_statuses[0].error)
        self.assertIsNone(job_statuses[0].runtime)

    def test_can_complete_job_status(self):
        job_status_id = list_job_status()[0].id
        job_status = complete_job_status(job_status_id, datetime.datetime(2021, 12, 1, 10, 51, 35), None)
        self.assertEqual("01/12/2021 10:51:35", job_status.display_end_date)
        self.assertEqual("00:06:35", job_status.runtime)
        self.assertIsNone(job_status.error)

    def test_can_complete_job_status_with_error(self):
        job_status_id = list_job_status()[0].id
        job_status = complete_job_status(job_status_id, datetime.datetime(2021, 12, 1, 10, 51, 35), "Some Error")
        self.assertEqual("01/12/2021 10:51:35", job_status.display_end_date)
        self.assertEqual("00:06:35", job_status.runtime)
        self.assertEqual("Some Error", job_status.error)

    def test_can_list_job_status_with_name(self):
        _ = create_job_status("Another Job", "Some Other Job Parameters", datetime.datetime(2021, 12, 2, 11, 45, 0))
        job_statuses = list_job_status(name="Another Job")
        self.assertEqual(1, len(job_statuses))
        self.assertEqual("Another Job", job_statuses[0].name)

    def test_can_list_job_status_with_from_date(self):
        _ = create_job_status("Another Job", "Some Other Job Parameters", datetime.datetime(2021, 12, 2, 11, 45, 0))
        job_statuses = list_job_status(from_date=datetime.datetime(2021, 12, 2, 0, 0, 0))
        self.assertEqual(1, len(job_statuses))
        self.assertEqual("Another Job", job_statuses[0].name)

    def test_can_list_job_status_with_to_date(self):
        _ = create_job_status("Another Job", "Some Other Job Parameters", datetime.datetime(2021, 12, 2, 11, 45, 0))
        job_statuses = list_job_status(to_date=datetime.datetime(2021, 12, 2, 0, 0, 0))
        self.assertEqual(1, len(job_statuses))
        self.assertEqual("A Test Job", job_statuses[0].name)
