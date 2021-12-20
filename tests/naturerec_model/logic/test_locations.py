import unittest
from src.naturerec_model.model import create_database, Session, Location
from src.naturerec_model.logic import create_location, get_location, list_locations, update_location


class TestLocations(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        create_location(name="Lashford Lane Fen",
                        address="Lashford Lane",
                        city="Wooton",
                        county="Oxfordshire",
                        postcode="OX13 6DY",
                        country="United Kingdom",
                        latitude=51.706694,
                        longitude=-1.324120)

    @staticmethod
    def create_additional_locations():
        create_location(name="Brock Hill", city="Lyndhurst", county="Hampshire", country="United Kingdom")
        create_location(name="Puttles Bridge", city="Brockenhurst", county="Hampshire", country="United Kingdom")
        create_location(name="Playa Flamenca", city="Alicante", county="Orihuela Costa", country="España")

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

    def test_can_update_location(self):
        with Session.begin() as session:
            location_id = session.query(Location).one().id

        update_location(location_id, "Lashford Lane Fen", "A County", "UK", "An Address", "A City", "AB1 1AB", 51.123,
                        -1.123)
        updated = get_location(location_id)

        self.assertEqual("Lashford Lane Fen", updated.name)
        self.assertEqual("An Address", updated.address)
        self.assertEqual("A City", updated.city)
        self.assertEqual("A County", updated.county)
        self.assertEqual("AB1 1AB", updated.postcode)
        self.assertEqual("UK", updated.country)
        self.assertEqual(51.123, updated.latitude)
        self.assertEqual(-1.123, updated.longitude)

    def test_can_update_location_name(self):
        with Session.begin() as session:
            location_id = session.query(Location).one().id

        update_location(location_id, "Some Location", "Oxfordshire", "United Kingdom")
        updated = get_location(location_id)

        self.assertEqual("Some Location", updated.name)
        self.assertEqual("Oxfordshire", updated.county)
        self.assertEqual("United Kingdom", updated.country)

    def test_cannot_update_location_to_create_duplicate(self):
        TestLocations.create_additional_locations()
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).filter(Location.name == "Lashford Lane Fen").one().id
            _ = update_location(location_id, "Brock Hill", "A County", "UK")

    def test_cannot_update_missing_location(self):
        with self.assertRaises(ValueError):
            _ = update_location(-1, "Some Location", "A County", "UK")

    def test_cannot_update_location_with_none_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, None, "A County", "UK")

    def test_cannot_update_location_with_blank_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "", "A County", "UK")

    def test_cannot_update_location_with_whitespace_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "    ", "A County", "UK")

    def test_cannot_update_location_with_none_county(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", None, "UK")

    def test_cannot_update_location_with_blank_county(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "", "UK")

    def test_cannot_update_location_with_whitespace_county(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "      ", "UK")

    def test_cannot_update_location_with_none_country(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "A County", None)

    def test_cannot_update_location_with_blank_country(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "A County", "")

    def test_cannot_update_location_with_whitespace_country(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "A County", "        ")

    def test_can_get_location_by_name(self):
        location = get_location("Lashford Lane Fen")
        self.assertEqual("Lashford Lane Fen", location.name)
        self.assertEqual("Lashford Lane", location.address)
        self.assertEqual("Wooton", location.city)
        self.assertEqual("Oxfordshire", location.county)
        self.assertEqual("OX13 6DY", location.postcode)
        self.assertEqual("United Kingdom", location.country)
        self.assertEqual(51.706694, location.latitude)
        self.assertEqual(-1.324120, location.longitude)

    def test_cannot_get_missing_location_by_name(self):
        with self.assertRaises(ValueError):
            _ = get_location("")

    def test_can_get_location_by_id(self):
        with Session.begin() as session:
            location_id = session.query(Location).one().id
        location = get_location(location_id)
        self.assertEqual("Lashford Lane Fen", location.name)
        self.assertEqual("Lashford Lane", location.address)
        self.assertEqual("Wooton", location.city)
        self.assertEqual("Oxfordshire", location.county)
        self.assertEqual("OX13 6DY", location.postcode)
        self.assertEqual("United Kingdom", location.country)
        self.assertEqual(51.706694, location.latitude)
        self.assertEqual(-1.324120, location.longitude)

    def test_cannot_get_missing_location_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_location(-1)

    def test_cannot_get_location_by_invalid_identifier(self):
        with self.assertRaises(TypeError):
            _ = get_location([])

    def test_can_list_all_locations(self):
        TestLocations.create_additional_locations()
        locations = list_locations()
        names = [location.name for location in locations]
        self.assertEqual(4, len(locations))
        self.assertTrue("Lashford Lane Fen" in names)
        self.assertTrue("Brock Hill" in names)
        self.assertTrue("Puttles Bridge" in names)
        self.assertTrue("Playa Flamenca" in names)

    def test_can_list_locations_by_city(self):
        TestLocations.create_additional_locations()
        locations = list_locations(city="Alicante")
        self.assertEqual(1, len(locations))
        self.assertEqual("Playa Flamenca", locations[0].name)

    def test_can_list_locations_by_missing_city(self):
        locations = list_locations(city="Manchester")
        self.assertEqual(0, len(locations))

    def test_can_list_locations_by_county(self):
        TestLocations.create_additional_locations()
        locations = list_locations(county="Hampshire")
        names = [location.name for location in locations]
        self.assertEqual(2, len(locations))
        self.assertTrue("Brock Hill" in names)
        self.assertTrue("Puttles Bridge" in names)

    def test_can_list_locations_by_missing_county(self):
        locations = list_locations(city="Greater Manchester")
        self.assertEqual(0, len(locations))

    def test_can_list_locations_by_country(self):
        TestLocations.create_additional_locations()
        locations = list_locations(country="United Kingdom")
        names = [location.name for location in locations]
        self.assertEqual(3, len(locations))
        self.assertTrue("Lashford Lane Fen" in names)
        self.assertTrue("Brock Hill" in names)
        self.assertTrue("Puttles Bridge" in names)

    def test_can_list_locations_by_missing_country(self):
        locations = list_locations(city="Belgium")
        self.assertEqual(0, len(locations))
