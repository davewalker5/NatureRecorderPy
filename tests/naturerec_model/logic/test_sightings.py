import unittest
import datetime
from naturerec_model.model import create_database, Session, Sighting, Gender, User
from naturerec_model.logic import create_category, get_category
from naturerec_model.logic import create_species, get_species
from naturerec_model.logic import create_location, get_location
from naturerec_model.logic import create_sighting, get_sighting, list_sightings, update_sighting, \
    delete_sighting


class TestSightings(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        category = create_category("Birds", True, self._user)
        species = create_species(category.id, "Black-Headed Gull", None, self._user)
        location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom", user=self._user)
        self._sighting = create_sighting(location.id, species.id, datetime.date(2021, 12, 14), None, Gender.UNKNOWN,
                                         False, "Notes", self._user)

    def create_additional_sightings(self):
        category_id = get_category("Birds").id
        species = create_species(category_id, "Blackbird", None, self._user)
        location = create_location(name="Brock Hill", city="Lyndhurst", county="Hampshire", country="United Kingdom", user=self._user)
        create_sighting(location.id, species.id, datetime.date(2021, 12, 13), None, Gender.UNKNOWN, False, None, self._user)

    def test_can_create_sighting(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()
        self.assertEqual("Birds",  sighting.species.category.name)
        self.assertEqual("Black-Headed Gull",  sighting.species.name)
        self.assertEqual("Radley Lakes",  sighting.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), sighting.sighting_date)
        self.assertIsNone(sighting.number)
        self.assertEqual(Gender.UNKNOWN, sighting.gender)
        self.assertFalse(0, sighting.withYoung)
        self.assertEqual("Notes", sighting.notes)

    def test_can_update_sighting_date(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 15), None,
                        Gender.UNKNOWN, False, "Notes", self._user)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 15), updated.sighting_date)
        self.assertIsNone(updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)
        self.assertEqual("Notes", updated.notes)

    def test_can_update_sighting_location(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        location = create_location(name="Brock Hill", city="Lyndhurst", county="Hampshire", country="United Kingdom", user=self._user)
        update_sighting(sighting.id, location.id, sighting.species.id, datetime.date(2021, 12, 14), None,
                        Gender.UNKNOWN, False, "Notes", self._user)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Brock Hill",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertIsNone(updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)
        self.assertEqual("Notes", updated.notes)

    def test_can_update_sighting_species(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        category_id = get_category("Birds").id
        species = create_species(category_id, "Blackbird", None, self._user)
        update_sighting(sighting.id, sighting.location.id, species.id, datetime.date(2021, 12, 14), None,
                        Gender.UNKNOWN, False, "Notes", self._user)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Blackbird",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertIsNone(updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)
        self.assertEqual("Notes", updated.notes)

    def test_can_update_sighting_number(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14), 10,
                        Gender.UNKNOWN, False, "Notes", self._user)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertEqual(10, updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)
        self.assertEqual("Notes", updated.notes)

    def test_can_update_sighting_gender(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14), None,
                        Gender.MALE, False, "Notes", self._user)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertIsNone(updated.number)
        self.assertEqual(Gender.MALE, updated.gender)
        self.assertFalse(0, updated.withYoung)
        self.assertEqual("Notes", updated.notes)

    def test_can_update_sighting_with_young(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14), None,
                        Gender.UNKNOWN, True, "Notes", self._user)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertIsNone(updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertTrue(1, updated.withYoung)
        self.assertEqual("Notes", updated.notes)

    def test_can_update_sighting_notes(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14), None,
                        Gender.UNKNOWN, True, "Updated notes", self._user)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertIsNone(updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertTrue(1, updated.withYoung)
        self.assertEqual("Updated notes", updated.notes)

    def test_cannot_update_sighting_to_create_duplicate(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        new_sighting = create_sighting(sighting.location.id, sighting.species.id, datetime.date(2021, 12, 15), None,
                                       Gender.UNKNOWN, False, None, self._user)

        with self.assertRaises(ValueError):
            _ = update_sighting(new_sighting.id, new_sighting.locationId, new_sighting.speciesId,
                                datetime.date(2021, 12, 14), None, Gender.UNKNOWN, False, None, self._user)

    def test_cannot_update_missing_sighting(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(-1, sighting.locationId, sighting.speciesId, datetime.date(2021, 12, 15), None,
                                Gender.UNKNOWN, False, None, self._user)

    def test_cannot_update_sighting_for_missing_location(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, -1, sighting.species.id, datetime.date(2021, 12, 14), None, Gender.UNKNOWN,
                                False, None, self._user)

    def test_cannot_update_sighting_for_missing_species(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, -1, datetime.date(2021, 12, 14), None,
                                Gender.UNKNOWN, False, None, self._user)

    def test_cannot_update_sighting_with_invalid_number(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14),
                                -1, Gender.UNKNOWN, False, None, self._user)

    def test_cannot_update_sighting_with_invalid_gender(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14),
                                0, 10, False, None, self._user)

    def test_cannot_update_sighting_with_invalid_with_young(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14),
                                0, Gender.UNKNOWN, -1, None, self._user)

    def test_can_get_sighting_by_id(self):
        with Session.begin() as session:
            sighting_id = session.query(Sighting).one().id
        sighting = get_sighting(sighting_id)
        self.assertEqual("Birds",  sighting.species.category.name)
        self.assertEqual("Black-Headed Gull",  sighting.species.name)
        self.assertEqual("Radley Lakes",  sighting.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), sighting.sighting_date)
        self.assertIsNone(sighting.number)
        self.assertEqual(Gender.UNKNOWN, sighting.gender)
        self.assertFalse(0, sighting.withYoung)

    def test_cannot_get_missing_sighting_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_sighting(-1)

    def test_can_list_all_sightings(self):
        self.create_additional_sightings()
        sightings = list_sightings()
        self.assertEqual(2, len(sightings))

    def test_can_filter_sightings_by_from_date(self):
        self.create_additional_sightings()
        sightings = list_sightings(from_date=datetime.date(2021, 12, 14))
        self.assertEqual(1, len(sightings))
        self.assertEqual("Black-Headed Gull", sightings[0].species.name)
        self.assertEqual("Radley Lakes", sightings[0].location.name)

    def test_can_filter_sightings_by_to_date(self):
        self.create_additional_sightings()
        sightings = list_sightings(to_date=datetime.date(2021, 12, 13))
        self.assertEqual(1, len(sightings))
        self.assertEqual("Blackbird", sightings[0].species.name)
        self.assertEqual("Brock Hill", sightings[0].location.name)

    def test_can_filter_sightings_by_date_range(self):
        self.create_additional_sightings()
        sightings = list_sightings(from_date=datetime.date(2021, 12, 14),
                                   to_date=datetime.date(2021, 12, 15))
        self.assertEqual(1, len(sightings))
        self.assertEqual("Black-Headed Gull", sightings[0].species.name)
        self.assertEqual("Radley Lakes", sightings[0].location.name)

    def test_can_filter_sightings_by_location(self):
        self.create_additional_sightings()
        location_id = get_location("Brock Hill").id
        sightings = list_sightings(location_id=location_id)
        self.assertEqual(1, len(sightings))
        self.assertEqual("Blackbird", sightings[0].species.name)
        self.assertEqual("Brock Hill", sightings[0].location.name)

    def test_can_filter_sightings_by_species(self):
        self.create_additional_sightings()
        species_id = get_species("Black-Headed Gull").id
        sightings = list_sightings(species_id=species_id)
        self.assertEqual(1, len(sightings))
        self.assertEqual("Black-Headed Gull", sightings[0].species.name)
        self.assertEqual("Radley Lakes", sightings[0].location.name)

    def test_can_filter_sightings_by_multiple_criteria(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()
        sightings = list_sightings(from_date=datetime.date(2021, 12, 14),
                                   to_date=None,
                                   location_id=sighting.locationId,
                                   species_id=sighting.speciesId)
        self.assertEqual(1, len(sightings))

    def test_can_delete_sighting(self):
        sightings = list_sightings()
        self.assertEqual(1, len(sightings))
        delete_sighting(self._sighting.id)
        sightings = list_sightings()
        self.assertEqual(0, len(sightings))

    def test_cannot_delete_missing_sighting(self):
        with self.assertRaises(ValueError):
            delete_sighting(-1)
