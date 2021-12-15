import unittest
import datetime
from src.naturerec_model.model import create_database, Session, SpeciesStatusRating
from src.naturerec_model.logic import create_category
from src.naturerec_model.logic import create_species
from src.naturerec_model.logic import create_status_scheme
from src.naturerec_model.logic import create_status_rating
from src.naturerec_model.logic import create_species_status_rating, get_species_status_rating, \
    list_species_status_ratings


class TestStatusRating(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._category = create_category("Birds")
        self._species = create_species(self._category.id, "Reed Bunting")
        self._scheme = create_status_scheme("BOCC4")
        self._rating = create_status_rating(self._scheme.id, "Amber")
        _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom",
                                         datetime.date(2015, 1, 1), datetime.date(2015, 12, 31))

    def test_can_create_rating(self):
        with Session.begin() as session:
            rating = session.query(SpeciesStatusRating).one()
        self.assertEqual("Reed Bunting", rating.species.name)
        self.assertEqual("BOCC4", rating.rating.scheme.name)
        self.assertEqual("Amber", rating.rating.name)
        self.assertEqual("United Kingdom", rating.region)
        self.assertEqual(datetime.date(2015, 1, 1), rating.start)
        self.assertEqual(datetime.date(2015, 12, 31), rating.end)

    def test_can_get_rating_by_id(self):
        with Session.begin() as session:
            rating_id = session.query(SpeciesStatusRating).one().id
        rating = get_species_status_rating(rating_id)
        self.assertEqual("Reed Bunting", rating.species.name)
        self.assertEqual("BOCC4", rating.rating.scheme.name)
        self.assertEqual("Amber", rating.rating.name)
        self.assertEqual("United Kingdom", rating.region)
        self.assertEqual(datetime.date(2015, 1, 1), rating.start)
        self.assertEqual(datetime.date(2015, 12, 31), rating.end)

    def test_cannot_get_missing_rating_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_species_status_rating(-1)

    def test_can_list_all_ratings(self):
        ratings = list_species_status_ratings()
        self.assertEqual(1, len(ratings))
        self.assertEqual("Reed Bunting", ratings[0].species.name)
        self.assertEqual("BOCC4", ratings[0].rating.scheme.name)
        self.assertEqual("Amber", ratings[0].rating.name)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start)
        self.assertEqual(datetime.date(2015, 12, 31), ratings[0].end)

    def test_can_list_filter_ratings_by_scheme(self):
        scheme = create_status_scheme("A Scheme")
        rating = create_status_rating(scheme.id, "A Rating")
        _ = create_species_status_rating(self._species.id, rating.id, "United Kingdom", datetime.date(2015, 1, 1))
        ratings = list_species_status_ratings(scheme_id=scheme.id)
        self.assertEqual(1, len(ratings))
        self.assertEqual("Reed Bunting", ratings[0].species.name)
        self.assertEqual("A Scheme", ratings[0].rating.scheme.name)
        self.assertEqual("A Rating", ratings[0].rating.name)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start)
        self.assertIsNone(ratings[0].end)

    def test_can_list_filter_ratings_by_species(self):
        species = create_species(self._category.id, "Bewick's Swan")
        _ = create_species_status_rating(species.id, self._rating.id, "United Kingdom", datetime.date(2015, 1, 1))
        ratings = list_species_status_ratings(species_id=species.id)
        self.assertEqual(1, len(ratings))
        self.assertEqual("Bewick's Swan", ratings[0].species.name)
        self.assertEqual("BOCC4", ratings[0].rating.scheme.name)
        self.assertEqual("Amber", ratings[0].rating.name)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start)
        self.assertIsNone(ratings[0].end)

    def test_can_list_filter_ratings_by_region(self):
        _ = create_species_status_rating(self._species.id, self._rating.id, "A Region", datetime.date(2015, 1, 1))
        ratings = list_species_status_ratings(region="A Region")
        self.assertEqual(1, len(ratings))
        self.assertEqual("Reed Bunting", ratings[0].species.name)
        self.assertEqual("BOCC4", ratings[0].rating.scheme.name)
        self.assertEqual("Amber", ratings[0].rating.name)
        self.assertEqual("A Region", ratings[0].region)
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start)
        self.assertIsNone(ratings[0].end)

    def test_can_list_current_ratings_only(self):
        _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom",
                                         datetime.date(2016, 1, 1))
        ratings = list_species_status_ratings(current_only=True)
        self.assertEqual(1, len(ratings))
        self.assertEqual("Reed Bunting", ratings[0].species.name)
        self.assertEqual("BOCC4", ratings[0].rating.scheme.name)
        self.assertEqual("Amber", ratings[0].rating.name)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual(datetime.date(2016, 1, 1), ratings[0].start)
        self.assertIsNone(ratings[0].end)
