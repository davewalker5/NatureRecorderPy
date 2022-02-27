import unittest
import datetime
from src.naturerec_model.model import create_database
from src.naturerec_model.logic import create_category
from src.naturerec_model.logic import create_species
from src.naturerec_model.logic import create_species_status_rating
from src.naturerec_model.logic import create_status_scheme, get_status_scheme
from src.naturerec_model.logic import create_status_rating, update_status_rating, delete_status_rating


class TestStatusRatings(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        scheme = create_status_scheme("BOCC4")
        self._rating = create_status_rating(scheme.id, "Red")

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

    def test_can_delete_rating(self):
        scheme = get_status_scheme("BOCC4")
        self.assertEqual(1, len(scheme.ratings))
        delete_status_rating(self._rating.id)
        scheme = get_status_scheme("BOCC4")
        self.assertEqual(0, len(scheme.ratings))

    def test_cannot_delete_missing_rating(self):
        with self.assertRaises(ValueError):
            delete_status_rating(-1)

    def test_cannot_delete_rating_with_species_ratings(self):
        category = create_category("Birds")
        species = create_species(category.id, "Red Kite")
        _ = create_species_status_rating(species.id, self._rating.id, "United Kingdom", datetime.date(2015, 1, 1))
        with self.assertRaises(ValueError):
            delete_status_rating(self._rating.id)
