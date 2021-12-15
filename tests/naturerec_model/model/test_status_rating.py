import unittest
from src.naturerec_model.model import create_database, Session, StatusScheme
from src.naturerec_model.logic import create_status_scheme, get_status_scheme
from src.naturerec_model.logic import create_status_rating

class TestStatusRating(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        scheme = create_status_scheme("BOCC4")
        _ = create_status_rating(scheme.id, "Red")

    def test_can_create_rating(self):
        with Session.begin() as session:
            scheme = session.query(StatusScheme).one()
        self.assertEqual(1, len(scheme.ratings))
        self.assertEqual("Red", scheme.ratings[0].name)

    def test_cannot_create_rating_against_missing_scheme(self):
        with self.assertRaises(ValueError):
            _ = create_status_rating(-1, "Red")

    def test_cannot_create_duplicate_rating(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = create_status_rating(scheme.id, "Red")

    def test_cannot_create_none_rating(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = create_status_rating(scheme.id, None)

    def test_cannot_create_blank_rating(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = create_status_rating(scheme.id, "")

    def test_cannot_create_whitespace_species(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = create_status_rating(scheme.id, "      ")
