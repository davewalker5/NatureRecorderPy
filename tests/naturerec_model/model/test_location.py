import unittest
from naturerec_model.model import create_database, Session, Location, User
from naturerec_model.logic import create_location


class TestLocation(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        create_location(name="Lashford Lane Fen",
                        address="Lashford Lane",
                        city="Wooton",
                        county="Oxfordshire",
                        postcode="OX13 6DY",
                        country="United Kingdom",
                        latitude=51.706694,
                        longitude=-1.324120,
                        user=self._user)

    def test_can_create_location(self):
        with Session.begin() as session:
            location = session.query(Location).one()
        self.assertEqual("Lashford Lane Fen", location.name)
        self.assertEqual("Lashford Lane", location.address)
        self.assertEqual("Wooton", location.city)
        self.assertEqual("Oxfordshire", location.county)
        self.assertEqual("OX13 6DY", location.postcode)
        self.assertEqual("United Kingdom", location.country)
        self.assertEqual(51.706694, location.latitude)
        self.assertEqual(-1.324120, location.longitude)

    def test_can_create_location_with_minimal_properties(self):
        location_id = create_location(name="Brock Hill", county="Hampshire", country="United Kingdom", user=self._user).id

        with Session.begin() as session:
            location = session.query(Location).get(location_id)

        self.assertEqual("Brock Hill", location.name)
        self.assertEqual("Hampshire", location.county)
        self.assertEqual("United Kingdom", location.country)

    def test_cannot_create_location_with_duplicate_name(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="Lashford Lane Fen", county="Oxfordshire", country="United Kingdom", user=self._user)

    def test_cannot_create_location_with_none_name(self):
        with self.assertRaises(ValueError):
            _ = create_location(name=None, county="Oxfordshire", country="United Kingdom", user=self._user)

    def test_cannot_create_location_with_blank_name(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="", county="Oxfordshire", country="United Kingdom", user=self._user)

    def test_cannot_create_location_with_whitespace_name(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="       ", county="Oxfordshire", country="United Kingdom", user=self._user)

    def test_cannot_create_location_with_none_county(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="Brock Hill", county=None, country="United Kingdom", user=self._user)

    def test_cannot_create_location_with_blank_county(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="Brock Hill", county="", country="United Kingdom", user=self._user)

    def test_cannot_create_location_with_whitespace_county(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="Brock Hill", county="      ", country="United Kingdom", user=self._user)

    def test_cannot_create_location_with_none_country(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="Brock Hill", county="Hampshire", country=None, user=self._user)

    def test_cannot_create_location_with_blank_country(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="Brock Hill", county="Hampshire", country="", user=self._user)

    def test_cannot_create_location_with_whitespace_country(self):
        with self.assertRaises(ValueError):
            _ = create_location(name="Brock Hill", county="Hampshire", country="      ", user=self._user)
