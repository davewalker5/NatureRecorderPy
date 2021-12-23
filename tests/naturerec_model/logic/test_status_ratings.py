import unittest
from src.naturerec_model.model import create_database, Session, StatusRating
from src.naturerec_model.logic import create_status_scheme, get_status_scheme
from src.naturerec_model.logic import create_status_rating, update_status_rating


class TestStatusRatings(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        scheme = create_status_scheme("BOCC4")
        _ = create_status_rating(scheme.id, "Red")

    def test_can_create_rating(self):
        scheme = get_status_scheme("BOCC4")
        self.assertEqual(1, len(scheme.ratings))
        self.assertTrue(scheme.id, scheme.ratings[0].statusSchemeId)
        self.assertEqual("Red", scheme.ratings[0].name)

    def test_can_update_rating(self):
        scheme = get_status_scheme("BOCC4")
        _ = update_status_rating(scheme.ratings[0].id, "Amber")
        updated = get_status_scheme("BOCC4")
        self.assertEqual(1, len(updated.ratings))
        self.assertTrue(scheme.id, updated.ratings[0].statusSchemeId)
        self.assertEqual("Amber", updated.ratings[0].name)

    def test_cannot_update_rating_to_create_duplicate(self):
        scheme = get_status_scheme("BOCC4")
        _ = create_status_rating(scheme.id, "Amber")
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, "Amber")

    def test_cannot_update_missing_rating(self):
        with self.assertRaises(ValueError):
            _ = update_status_rating(-1, "Amber")

    def test_cannot_update_rating_with_none_name(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, None)

    def test_cannot_update_rating_with_blank_name(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, "")

    def test_cannot_update_rating_with_whitespace_name(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, "      ")
