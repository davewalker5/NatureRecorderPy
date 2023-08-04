import unittest
import datetime
from naturerec_model.model import create_database, User
from naturerec_model.logic import create_category
from naturerec_model.logic import create_species
from naturerec_model.logic import create_species_status_rating
from naturerec_model.logic import create_status_scheme, get_status_scheme
from naturerec_model.logic import create_status_rating, update_status_rating, delete_status_rating


class TestStatusRatings(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        scheme = create_status_scheme("BOCC4", self._user)
        self._rating = create_status_rating(scheme.id, "Red", self._user)

    def test_can_create_rating(self):
        scheme = get_status_scheme("BOCC4")
        self.assertEqual(1, len(scheme.ratings))
        self.assertTrue(scheme.id, scheme.ratings[0].statusSchemeId)
        self.assertEqual("Red", scheme.ratings[0].name)

    def test_can_update_rating(self):
        scheme = get_status_scheme("BOCC4")
        _ = update_status_rating(scheme.ratings[0].id, "Amber", self._user)
        updated = get_status_scheme("BOCC4")
        self.assertEqual(1, len(updated.ratings))
        self.assertTrue(scheme.id, updated.ratings[0].statusSchemeId)
        self.assertEqual("Amber", updated.ratings[0].name)

    def test_cannot_update_rating_to_create_duplicate(self):
        scheme = get_status_scheme("BOCC4")
        _ = create_status_rating(scheme.id, "Amber", self._user)
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, "Amber", self._user)

    def test_cannot_update_missing_rating(self):
        with self.assertRaises(ValueError):
            _ = update_status_rating(-1, "Amber", self._user)

    def test_cannot_update_rating_with_none_name(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, None, self._user)

    def test_cannot_update_rating_with_blank_name(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, "", self._user)

    def test_cannot_update_rating_with_whitespace_name(self):
        scheme = get_status_scheme("BOCC4")
        with self.assertRaises(ValueError):
            _ = update_status_rating(scheme.ratings[0].id, "      ", self._user)

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
        category = create_category("Birds", self._user)
        species = create_species(category.id, "Red Kite", self._user)
        _ = create_species_status_rating(species.id, self._rating.id, "United Kingdom", datetime.date(2015, 1, 1), self._user)
        with self.assertRaises(ValueError):
            delete_status_rating(self._rating.id)
