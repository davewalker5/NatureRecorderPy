import unittest
import datetime
from src.naturerec_model.model import create_database, Session, Sighting, Gender
from src.naturerec_model.logic import create_category
from src.naturerec_model.logic import create_species
from src.naturerec_model.logic import create_location
from src.naturerec_model.logic import create_sighting


class TestSighting(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._category = create_category("Birds")
        self._gull = create_species(self._category.id, "Black-Headed Gull")
        self._cormorant = create_species(self._category.id, "Cormorant")
        self._location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom")
        _ = create_sighting(self._location.id, self._gull.id, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN, False)

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

    def test_can_create_sighting_for_males(self):
        sighting_id = create_sighting(self._location.id, self._cormorant.id, datetime.date(2021, 12, 14), 0,
                                      Gender.MALE, False).id
        with Session.begin() as session:
            sighting = session.query(Sighting).get(sighting_id)
            self.assertEqual(Gender.MALE, sighting.gender)

    def test_can_create_sighting_for_females(self):
        sighting_id = create_sighting(self._location.id, self._cormorant.id, datetime.date(2021, 12, 14), 0,
                                      Gender.FEMALE, False).id
        with Session.begin() as session:
            sighting = session.query(Sighting).get(sighting_id)
            self.assertEqual(Gender.FEMALE, sighting.gender)

    def test_can_create_sighting_for_both_genders(self):
        sighting_id = create_sighting(self._location.id, self._cormorant.id, datetime.date(2021, 12, 14), 0,
                                      Gender.BOTH, False).id
        with Session.begin() as session:
            sighting = session.query(Sighting).get(sighting_id)
            self.assertEqual(Gender.BOTH, sighting.gender)

    def test_cannot_create_sighting_for_invalid_gender(self):
        with self.assertRaises(ValueError):
            _ = create_sighting(self._location.id, self._cormorant.id, datetime.date(2021, 12, 14), 0,
                                -1, False)

    def test_cannot_create_same_sighting_twice(self):
        with self.assertRaises(ValueError):
            _ = create_sighting(self._location.id, self._gull.id, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN, False)

    def test_cannot_create_sighting_for_missing_location(self):
        with self.assertRaises(ValueError):
            _ = create_sighting(-1, self._cormorant.id, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN, False)

    def test_cannot_create_sighting_for_missing_species(self):
        with self.assertRaises(ValueError):
            _ = create_sighting(self._location.id, -1, datetime.date(2021, 12, 14), 0, Gender.UNKNOWN, False)
