import unittest
import datetime
from src.naturerec_model.model import create_database, Session, Sighting, Gender
from src.naturerec_model.logic import create_category, get_category
from src.naturerec_model.logic import create_species, get_species
from src.naturerec_model.logic import create_location, get_location
from src.naturerec_model.logic import create_sighting, get_sighting, list_sightings, update_sighting


class TestSightings(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        category = create_category("Birds")
        species = create_species(category.id, "Black-Headed Gull")
        location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom")
        create_sighting(location.id, species.id, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN, False)

    @staticmethod
    def create_additional_sightings():
        category_id = get_category("Birds").id
        species = create_species(category_id, "Blackbird")
        location = create_location(name="Brock Hill", city="Lyndhurst", county="Hampshire", country="United Kingdom")
        create_sighting(location.id, species.id, datetime.date(2021, 12, 13), 0, Gender.UNKNOWN, False)

    def test_can_create_sighting(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()
        self.assertEqual("Birds",  sighting.species.category.name)
        self.assertEqual("Black-Headed Gull",  sighting.species.name)
        self.assertEqual("Radley Lakes",  sighting.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), sighting.sighting_date)
        self.assertEqual(0, sighting.number)
        self.assertEqual(Gender.UNKNOWN, sighting.gender)
        self.assertFalse(0, sighting.withYoung)

    def test_can_update_sighting_date(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 15), 0,
                        Gender.UNKNOWN, False)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 15), updated.sighting_date)
        self.assertEqual(0, updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)

    def test_can_update_sighting_location(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        location = create_location(name="Brock Hill", city="Lyndhurst", county="Hampshire", country="United Kingdom")
        update_sighting(sighting.id, location.id, sighting.species.id, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN,
                        False)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Brock Hill",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertEqual(0, updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)

    def test_can_update_sighting_species(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        category_id = get_category("Birds").id
        species = create_species(category_id, "Blackbird")
        update_sighting(sighting.id, sighting.location.id, species.id, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN,
                        False)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Blackbird",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertEqual(0, updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)

    def test_can_update_sighting_number(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14), 10,
                        Gender.UNKNOWN, False)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertEqual(10, updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertFalse(0, updated.withYoung)

    def test_can_update_sighting_gender(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14), 0,
                        Gender.MALE, False)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertEqual(0, updated.number)
        self.assertEqual(Gender.MALE, updated.gender)
        self.assertFalse(0, updated.withYoung)

    def test_can_update_sighting_with_young(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14), 0,
                        Gender.UNKNOWN, True)
        updated = get_sighting(sighting.id)

        self.assertEqual("Birds",  updated.species.category.name)
        self.assertEqual("Black-Headed Gull",  updated.species.name)
        self.assertEqual("Radley Lakes",  updated.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), updated.sighting_date)
        self.assertEqual(0, updated.number)
        self.assertEqual(Gender.UNKNOWN, updated.gender)
        self.assertTrue(1, updated.withYoung)

    def test_cannot_update_sighting_to_create_duplicate(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        new_sighting = create_sighting(sighting.location.id, sighting.species.id, datetime.date(2021, 12, 15), 0,
                                       Gender.UNKNOWN, False)

        with self.assertRaises(ValueError):
            _ = update_sighting(new_sighting.id, new_sighting.locationId, new_sighting.speciesId,
                                datetime.date(2021, 12, 14), 0, Gender.UNKNOWN, False)

    def test_cannot_update_missing_sighting(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(-1, sighting.locationId, sighting.speciesId, datetime.date(2021, 12, 15), 0,
                                Gender.UNKNOWN, False)

    def test_cannot_update_sighting_for_missing_location(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, -1, sighting.species.id, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN,
                                False)

    def test_cannot_update_sighting_for_missing_species(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, -1, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN,
                                False)

    def test_cannot_update_sighting_with_invalid_number(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14),
                                -1, Gender.UNKNOWN, False)

    def test_cannot_update_sighting_with_invalid_gender(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14),
                                0, 10, False)

    def test_cannot_update_sighting_with_invalid_with_young(self):
        with Session.begin() as session:
            sighting = session.query(Sighting).one()

        with self.assertRaises(ValueError):
            _ = update_sighting(sighting.id, sighting.location.id, sighting.species.id, datetime.date(2021, 12, 14),
                                0, Gender.UNKNOWN, -1)

    def test_can_get_sighting_by_id(self):
        with Session.begin() as session:
            sighting_id = session.query(Sighting).one().id
        sighting = get_sighting(sighting_id)
        self.assertEqual("Birds",  sighting.species.category.name)
        self.assertEqual("Black-Headed Gull",  sighting.species.name)
        self.assertEqual("Radley Lakes",  sighting.location.name)
        self.assertEqual(datetime.date(2021, 12, 14), sighting.sighting_date)
        self.assertEqual(0, sighting.number)
        self.assertEqual(Gender.UNKNOWN, sighting.gender)
        self.assertFalse(0, sighting.withYoung)

    def test_cannot_get_missing_sighting_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_sighting(-1)

    def test_can_list_all_sightings(self):
        TestSightings.create_additional_sightings()
        sightings = list_sightings()
        self.assertEqual(2, len(sightings))

    def test_can_filter_sightings_by_from_date(self):
        TestSightings.create_additional_sightings()
        sightings = list_sightings(from_date=datetime.date(2021, 12, 14))
        self.assertEqual(1, len(sightings))
        self.assertEqual("Black-Headed Gull", sightings[0].species.name)
        self.assertEqual("Radley Lakes", sightings[0].location.name)

    def test_can_filter_sightings_by_to_date(self):
        TestSightings.create_additional_sightings()
        sightings = list_sightings(to_date=datetime.date(2021, 12, 13))
        self.assertEqual(1, len(sightings))
        self.assertEqual("Blackbird", sightings[0].species.name)
        self.assertEqual("Brock Hill", sightings[0].location.name)

    def test_can_filter_sightings_by_date_range(self):
        TestSightings.create_additional_sightings()
        sightings = list_sightings(from_date=datetime.date(2021, 12, 14),
                                   to_date=datetime.date(2021, 12, 15))
        self.assertEqual(1, len(sightings))
        self.assertEqual("Black-Headed Gull", sightings[0].species.name)
        self.assertEqual("Radley Lakes", sightings[0].location.name)

    def test_can_filter_sightings_by_location(self):
        TestSightings.create_additional_sightings()
        location_id = get_location("Brock Hill").id
        sightings = list_sightings(location_id=location_id)
        self.assertEqual(1, len(sightings))
        self.assertEqual("Blackbird", sightings[0].species.name)
        self.assertEqual("Brock Hill", sightings[0].location.name)

    def test_can_filter_sightings_by_species(self):
        TestSightings.create_additional_sightings()
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
