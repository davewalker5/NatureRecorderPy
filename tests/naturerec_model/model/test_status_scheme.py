import unittest
from src.naturerec_model.model import create_database, Session, StatusScheme
from src.naturerec_model.logic import create_status_scheme
from src.naturerec_model.logic import create_status_rating


class TestStatusScheme(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        scheme = create_status_scheme("BOCC4")
        _ = create_status_rating(scheme.id, "Red")
        _ = create_status_rating(scheme.id, "Amber")

    def test_can_create_scheme(self):
        with Session.begin() as session:
            scheme = session.query(StatusScheme).one()
            self.assertEqual("BOCC4", scheme.name)

    def test_cannot_create_duplicate_scheme(self):
        with self.assertRaises(ValueError):
            _ = create_status_scheme("BOCC4")

    def test_cannot_create_none_scheme(self):
        with self.assertRaises(ValueError):
            _ = create_status_scheme(None)

    def test_cannot_create_blank_scheme(self):
        with self.assertRaises(ValueError):
            _ = create_status_scheme("")

    def test_cannot_create_whitespace_scheme(self):
        with self.assertRaises(ValueError):
            _ = create_status_scheme("       ")

    def test_related_ratings_returned_with_scheme(self):
        with Session.begin() as session:
            scheme = session.query(StatusScheme).one()
        rating_names = [rating.name for rating in scheme.ratings]
        self.assertEqual(2, len(scheme.ratings))
        self.assertTrue("Red" in rating_names)
        self.assertTrue("Amber" in rating_names)
