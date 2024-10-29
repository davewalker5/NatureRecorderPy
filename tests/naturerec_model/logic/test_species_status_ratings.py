import unittest
import datetime
from naturerec_model.model import create_database, Session, SpeciesStatusRating, User
from naturerec_model.logic import create_category
from naturerec_model.logic import create_species
from naturerec_model.logic import create_status_scheme
from naturerec_model.logic import create_status_rating
from naturerec_model.logic import create_species_status_rating, get_species_status_rating, \
    list_species_status_ratings, close_species_status_rating, delete_species_status_rating


class TestStatusRating(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        self._category = create_category("Birds", self._user)
        self._species = create_species(self._category.id, "Reed Bunting", None, self._user)
        self._scheme = create_status_scheme("BOCC4", self._user)
        self._rating = create_status_rating(self._scheme.id, "Amber", self._user)
        self._species_status_rating = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom",
                                                                   datetime.date(2015, 1, 1), self._user,
                                                                   datetime.date(2015, 12, 31))

    def test_can_create_rating(self):
        with Session.begin() as session:
            rating = session.query(SpeciesStatusRating).one()
        self.assertEqual("Reed Bunting", rating.species.name)
        self.assertEqual("BOCC4", rating.rating.scheme.name)
        self.assertEqual("Amber", rating.rating.name)
        self.assertEqual("United Kingdom", rating.region)
        self.assertEqual(datetime.date(2015, 1, 1), rating.start_date)
        self.assertEqual(datetime.date(2015, 12, 31), rating.end_date)

    def test_cannot_create_future_rating(self):
        with self.assertRaises(ValueError):
            start = datetime.datetime.now() + datetime.timedelta(days=1)
            _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom", start.date(), self._user, None)

    def test_overlapping_ratings_are_closed(self):
        # Clear out the end date on the test rating
        with Session.begin() as session:
            rating = session.query(SpeciesStatusRating).one()
            rating.end_date = None

        rating = get_species_status_rating(rating.id)
        self.assertIsNone(rating.end_date)

        # Add an overlapping one
        _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom",
                                         datetime.date(2017, 1, 1), self._user, None)

        # List all ratings in date order and confirm the start and end dates are correct
        ratings = sorted(list_species_status_ratings(), key=lambda x: x.start)
        self.assertEqual(2, len(ratings))
        self.assertEqual(datetime.datetime.now().date(), ratings[0].end_date)
        self.assertEqual(datetime.date(2017, 1, 1), ratings[1].start_date)
        self.assertIsNone(ratings[1].end_date)

    def test_can_close_rating(self):
        with Session.begin() as session:
            rating_id = session.query(SpeciesStatusRating).one().id
        close_species_status_rating(rating_id, self._user)

    def test_cannot_close_missing_rating(self):
        with self.assertRaises(ValueError):
            close_species_status_rating(-1, self._user)

    def test_can_get_rating_by_id(self):
        with Session.begin() as session:
            rating_id = session.query(SpeciesStatusRating).one().id
        rating = get_species_status_rating(rating_id)
        self.assertEqual("Reed Bunting", rating.species.name)
        self.assertEqual("BOCC4", rating.rating.scheme.name)
        self.assertEqual("Amber", rating.rating.name)
        self.assertEqual("United Kingdom", rating.region)
        self.assertEqual(datetime.date(2015, 1, 1), rating.start_date)
        self.assertEqual(datetime.date(2015, 12, 31), rating.end_date)

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
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start_date)
        self.assertEqual(datetime.date(2015, 12, 31), ratings[0].end_date)

    def test_can_list_filter_ratings_by_scheme(self):
        scheme = create_status_scheme("A Scheme", self._user)
        rating = create_status_rating(scheme.id, "A Rating", self._user)
        _ = create_species_status_rating(self._species.id, rating.id, "United Kingdom", datetime.date(2015, 1, 1), self._user)
        ratings = list_species_status_ratings(scheme_id=scheme.id)
        self.assertEqual(1, len(ratings))
        self.assertEqual("Reed Bunting", ratings[0].species.name)
        self.assertEqual("A Scheme", ratings[0].rating.scheme.name)
        self.assertEqual("A Rating", ratings[0].rating.name)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start_date)
        self.assertIsNone(ratings[0].end_date)

    def test_can_list_filter_ratings_by_species(self):
        species = create_species(self._category.id, "Bewick's Swan", None, self._user)
        _ = create_species_status_rating(species.id, self._rating.id, "United Kingdom", datetime.date(2015, 1, 1), self._user)
        ratings = list_species_status_ratings(species_id=species.id)
        self.assertEqual(1, len(ratings))
        # Python title casing's a bit interesting!
        self.assertEqual("Bewick'S Swan", ratings[0].species.name)
        self.assertEqual("BOCC4", ratings[0].rating.scheme.name)
        self.assertEqual("Amber", ratings[0].rating.name)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start_date)
        self.assertIsNone(ratings[0].end_date)

    def test_can_list_filter_ratings_by_region(self):
        _ = create_species_status_rating(self._species.id, self._rating.id, "A Region", datetime.date(2015, 1, 1), self._user)
        ratings = list_species_status_ratings(region="A Region")
        self.assertEqual(1, len(ratings))
        self.assertEqual("Reed Bunting", ratings[0].species.name)
        self.assertEqual("BOCC4", ratings[0].rating.scheme.name)
        self.assertEqual("Amber", ratings[0].rating.name)
        self.assertEqual("A Region", ratings[0].region)
        self.assertEqual(datetime.date(2015, 1, 1), ratings[0].start_date)
        self.assertIsNone(ratings[0].end_date)

    def test_can_list_current_ratings_only(self):
        _ = create_species_status_rating(self._species.id, self._rating.id, "United Kingdom",
                                         datetime.date(2016, 1, 1), self._user)
        ratings = list_species_status_ratings(current_only=True)
        self.assertEqual(1, len(ratings))
        self.assertEqual("Reed Bunting", ratings[0].species.name)
        self.assertEqual("BOCC4", ratings[0].rating.scheme.name)
        self.assertEqual("Amber", ratings[0].rating.name)
        self.assertEqual("United Kingdom", ratings[0].region)
        self.assertEqual(datetime.date(2016, 1, 1), ratings[0].start_date)
        self.assertIsNone(ratings[0].end_date)

    def test_can_delete_species_status_rating(self):
        ratings = list_species_status_ratings()
        self.assertEqual(1, len(ratings))
        delete_species_status_rating(self._species_status_rating.id)
        ratings = list_species_status_ratings()
        self.assertEqual(0, len(ratings))

    def test_cannot_delete_missing_species_status_rating(self):
        with self.assertRaises(ValueError):
            delete_species_status_rating(-1)
