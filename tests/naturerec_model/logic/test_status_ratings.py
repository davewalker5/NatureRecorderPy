import unittest
from src.naturerec_model.model import create_database, Session, StatusRating
from src.naturerec_model.logic import create_status_scheme, get_status_scheme
from src.naturerec_model.logic import create_status_rating


class TestStatusRatings(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        scheme = create_status_scheme("BOCC4")
        _ = create_status_rating(scheme.id, "Red")

    def test_can_create_rating(self):
        scheme = get_status_scheme("BOCC4")
        with Session.begin() as session:
            rating = session.query(StatusRating).one()
        self.assertTrue(scheme.id, rating.statusSchemeId)
        self.assertEqual("Red", rating.name)
