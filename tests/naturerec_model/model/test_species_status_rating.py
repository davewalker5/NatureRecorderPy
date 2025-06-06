import unittest
import datetime
from naturerec_model.model import create_database, Session, SpeciesStatusRating, User
from naturerec_model.logic import create_category
from naturerec_model.logic import create_species
from naturerec_model.logic import create_status_scheme
from naturerec_model.logic import create_status_rating
from naturerec_model.logic import create_species_status_rating


class TestSpeciesStatusRating(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        self._category = create_category("Birds", True, self._user)
        self._species = create_species(self._category.id, "Reed Bunting", None, self._user)
        self._scheme = create_status_scheme("BOCC4", self._user)
        self._rating = create_status_rating(self._scheme.id, "Amber", self._user)
        _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom",
                                         datetime.date(2015, 1, 1), self._user)

    def test_can_create_rating(self):
        with Session.begin() as session:
            rating = session.query(SpeciesStatusRating).one()
        self.assertEqual("Reed Bunting", rating.species.name)
        self.assertEqual("BOCC4", rating.rating.scheme.name)
        self.assertEqual("Amber", rating.rating.name)
        self.assertEqual("United Kingdom", rating.region)
        self.assertEqual(datetime.date(2015, 1, 1), rating.start_date)
        self.assertIsNone(rating.end_date)
        self.assertEqual("01/01/2015", rating.display_start_date)
        self.assertIsNone(rating.display_end_date)

    def test_cannot_create_rating_for_missing_species(self):
        with self.assertRaises(ValueError):
            _ = create_species_status_rating(-1, self._rating.id, "United Kingdom", datetime.date(2015, 1, 1), self._user)

    def test_cannot_create_rating_for_missing_rating(self):
        with self.assertRaises(ValueError):
            _ = create_species_status_rating(self._species.id, -1, "United Kingdom", datetime.date(2015, 1, 1), self._user)

    def test_cannot_create_rating_with_no_region(self):
        with self.assertRaises(ValueError):
            _ = create_species_status_rating(self._species.id, self._rating.id, None, datetime.date(2015, 1, 1), self._user)

    def test_cannot_create_rating_with_blank_region(self):
        with self.assertRaises(ValueError):
            _ = create_species_status_rating(self._species.id, self._rating.id, "", datetime.date(2015, 1, 1), self._user)

    def test_cannot_create_rating_with_whitespace_region(self):
        with self.assertRaises(ValueError):
            _ = create_species_status_rating(self._species.id, self._rating.id, "      ", datetime.date(2015, 1, 1), self._user)

    def test_cannot_create_rating_with_no_start_date(self):
        with self.assertRaises(ValueError):
            _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom", None, self._user)

    def test_cannot_create_rating_with_invalid_date_range(self):
        with self.assertRaises(ValueError):
            _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom",
                                             datetime.date(2015, 1, 2), self._user, datetime.date(2015, 1, 1))
