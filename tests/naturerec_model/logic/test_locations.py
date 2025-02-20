import unittest
import datetime
from naturerec_model.model import create_database, Session, Location, Gender, User
from naturerec_model.logic import create_location, get_location, list_locations, update_location, delete_location
from naturerec_model.logic import create_category
from naturerec_model.logic import create_species
from naturerec_model.logic import create_sighting


class TestLocations(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        self._location = create_location(name="Lashford Lane Fen",
                                         address="Lashford Lane",
                                         city="Wooton",
                                         county="Oxfordshire",
                                         postcode="OX13 6DY",
                                         country="United Kingdom",
                                         latitude=51.706694,
                                         longitude=-1.324120,
                                         user=self._user)

    def create_additional_locations(self):
        create_location(name="Brock Hill", city="Lyndhurst", county="Hampshire", country="United Kingdom", user=self._user)
        create_location(name="Puttles Bridge", city="Brockenhurst", county="Hampshire", country="United Kingdom", user=self._user)
        create_location(name="Playa Flamenca", city="Alicante", county="Orihuela Costa", country="España", user=self._user)

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

        update_location(location_id, "Lashford Lane Fen", "A County", "United Kingdom", self._user,  "An Address",
                        "A City", "AB1 1AB", 51.123, -1.123)
        updated = get_location(location_id)

        self.assertEqual("Lashford Lane Fen", updated.name)
        self.assertEqual("An Address", updated.address)
        self.assertEqual("A City", updated.city)
        self.assertEqual("A County", updated.county)
        self.assertEqual("AB1 1AB", updated.postcode)
        self.assertEqual("United Kingdom", updated.country)
        self.assertEqual(51.123, updated.latitude)
        self.assertEqual(-1.123, updated.longitude)

    def test_can_update_location_name(self):
        with Session.begin() as session:
            location_id = session.query(Location).one().id

        update_location(location_id, "Some Location", "Oxfordshire", "United Kingdom", self._user)
        updated = get_location(location_id)

        self.assertEqual("Some Location", updated.name)
        self.assertEqual("Oxfordshire", updated.county)
        self.assertEqual("United Kingdom", updated.country)

    def test_cannot_update_location_to_create_duplicate(self):
        self.create_additional_locations()
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).filter(Location.name == "Lashford Lane Fen").one().id
            _ = update_location(location_id, "Brock Hill", "A County", "UK", self._user)

    def test_cannot_update_missing_location(self):
        with self.assertRaises(ValueError):
            _ = update_location(-1, "Some Location", "A County", "UK", self._user)

    def test_cannot_update_location_with_none_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, None, "A County", "UK", self._user)

    def test_cannot_update_location_with_blank_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "", "A County", "UK", self._user)

    def test_cannot_update_location_with_whitespace_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "    ", "A County", "UK", self._user)

    def test_cannot_update_location_with_none_county(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", None, "UK", self._user)

    def test_cannot_update_location_with_blank_county(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "", "UK", self._user)

    def test_cannot_update_location_with_whitespace_county(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "      ", "UK", self._user)

    def test_cannot_update_location_with_none_country(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "A County", None, self._user)

    def test_cannot_update_location_with_blank_country(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "A County", "", self._user)

    def test_cannot_update_location_with_whitespace_country(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            location_id = session.query(Location).one().id
            _ = update_location(location_id, "Some Location", "A County", "        ", self._user)

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
        self.create_additional_locations()
        locations = list_locations()
        names = [location.name for location in locations]
        self.assertEqual(4, len(locations))
        self.assertTrue("Lashford Lane Fen" in names)
        self.assertTrue("Brock Hill" in names)
        self.assertTrue("Puttles Bridge" in names)
        self.assertTrue("Playa Flamenca" in names)

    def test_can_list_locations_by_city(self):
        self.create_additional_locations()
        locations = list_locations(city="Alicante")
        self.assertEqual(1, len(locations))
        self.assertEqual("Playa Flamenca", locations[0].name)

    def test_can_list_locations_by_missing_city(self):
        locations = list_locations(city="Manchester")
        self.assertEqual(0, len(locations))

    def test_can_list_locations_by_county(self):
        self.create_additional_locations()
        locations = list_locations(county="Hampshire")
        names = [location.name for location in locations]
        self.assertEqual(2, len(locations))
        self.assertTrue("Brock Hill" in names)
        self.assertTrue("Puttles Bridge" in names)

    def test_can_list_locations_by_missing_county(self):
        locations = list_locations(city="Greater Manchester")
        self.assertEqual(0, len(locations))

    def test_can_list_locations_by_country(self):
        self.create_additional_locations()
        locations = list_locations(country="United Kingdom")
        names = [location.name for location in locations]
        self.assertEqual(3, len(locations))
        self.assertTrue("Lashford Lane Fen" in names)
        self.assertTrue("Brock Hill" in names)
        self.assertTrue("Puttles Bridge" in names)

    def test_can_list_locations_by_missing_country(self):
        locations = list_locations(city="Belgium")
        self.assertEqual(0, len(locations))

    def test_can_delete_location(self):
        locations = list_locations()
        self.assertEqual(1, len(locations))
        delete_location(self._location.id)
        locations = list_locations()
        self.assertEqual(0, len(locations))

    def test_cannot_delete_missing_location(self):
        with self.assertRaises(ValueError):
            delete_location(-1)

    def test_cannot_delete_location_with_sightings(self):
        category = create_category("Birds", True, self._user)
        species = create_species(category.id, "Wren", None, self._user)
        _ = create_sighting(self._location.id, species.id, datetime.date(2021, 12, 14), None, Gender.UNKNOWN, False,
                            "Notes", self._user)
        with self.assertRaises(ValueError):
            delete_location(-1)
