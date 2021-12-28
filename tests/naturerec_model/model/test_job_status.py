import unittest
import datetime
from src.naturerec_model.model import Session, create_database, JobStatus
from src.naturerec_model.logic import create_job_status


class TestJobStatus(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        _ = create_job_status("A Test Job", "Some Job Parameters", datetime.datetime(2021, 12, 1, 10, 45, 0))

    def test_can_create_job_status(self):
        with Session.begin() as session:
            job_status = session.query(JobStatus).one()
            self.assertEqual("A Test Job", job_status.name)
            self.assertEqual("Some Job Parameters", job_status.parameters)
            self.assertEqual("01/12/2021 10:45:00", job_status.display_start_date)
            self.assertIsNone(job_status.display_end_date)
            self.assertIsNone(job_status.error)

    def test_can_calculate_runtime(self):
        with Session.begin() as session:
            job_status = session.query(JobStatus).one()
            job_status.end_date = datetime.datetime(2021, 12, 1, 10, 51, 35)
            self.assertEqual("00:06:35", job_status.runtime)

    def test_cannot_create_job_status_with_no_name(self):
        with self.assertRaises(ValueError):
            _ = create_job_status(None, None, datetime.datetime(2021, 12, 1, 10, 45, 0))

    def test_cannot_create_job_status_with_blank_name(self):
        with self.assertRaises(ValueError):
            _ = create_job_status("", None, datetime.datetime(2021, 12, 1, 10, 45, 0))

    def test_cannot_create_job_status_with_whitespace_name(self):
        with self.assertRaises(ValueError):
            _ = create_job_status("      ", None, datetime.datetime(2021, 12, 1, 10, 45, 0))

    def test_cannot_create_job_status_with_no_start(self):
        with self.assertRaises(ValueError):
            _ = create_job_status("A Test Job", None, None)
