import unittest
import datetime
from src.naturerec_model.model import create_database, Session, Species, Gender
from src.naturerec_model.logic import create_location
from src.naturerec_model.logic import create_category, get_category
from src.naturerec_model.logic import create_species, get_species, list_species, update_species, delete_species
from src.naturerec_model.logic import create_sighting


class TestSpecies(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        category = create_category("Birds")
        self._species = create_species(category.id, "Red Kite")

    def test_can_create_species(self):
        category = get_category("Birds")
        with Session.begin() as session:
            species = session.query(Species).one()
        self.assertTrue(category.id, species.categoryId)
        self.assertEqual("Red Kite", species.name)

    def test_cannot_create_duplicate_species(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            category_id = session.query(Species).one().categoryId
            _ = create_species(category_id, "Red Kite")

    def test_can_update_species(self):
        category_id = create_category("Insects").id
        with Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category_id, "Azure Damselfly")
        species = get_species(species_id)
        self.assertEqual("Insects", species.category.name)
        self.assertEqual("Azure Damselfly", species.name)

    def test_cannot_update_species_to_create_duplicate(self):
        category = get_category("Birds")
        species = create_species(category.id, "Robin")
        with self.assertRaises(ValueError):
            _ = update_species(species.id, category.id, "Red Kite")

    def test_cannot_update_missing_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = update_species(-1, category.id, "Robin")

    def test_cannot_update_species_with_missing_category(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, -1, "Robin")

    def test_cannot_update_species_with_none_name(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category.id, None)

    def test_cannot_update_species_with_blank_name(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category.id, "")

    def test_cannot_update_species_with_whitespace_name(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category.id, "      ")

    def test_can_get_species_by_name(self):
        species = get_species("Red Kite")
        self.assertEqual("Red Kite", species.name)

    def test_cannot_get_missing_species_by_name(self):
        with self.assertRaises(ValueError):
            _ = get_species("")

    def test_can_get_species_by_id(self):
        with Session.begin() as session:
            species_id = session.query(Species).one().id
        species = get_species(species_id)
        self.assertEqual("Red Kite", species.name)

    def test_cannot_get_missing_species_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_species(-1)

    def test_cannot_get_species_by_invalid_identifier(self):
        with self.assertRaises(TypeError):
            _ = get_species([])

    def test_can_list_species(self):
        category_id = get_category("Birds").id
        species = list_species(category_id)
        self.assertEqual(1, len(species))
        self.assertEqual("Red Kite", species[0].name)

    def test_can_delete_species(self):
        category_id = get_category("Birds").id
        species = list_species(category_id)
        self.assertEqual(1, len(species))
        delete_species(self._species.id)
        species = list_species(category_id)
        self.assertEqual(0, len(species))

    def test_cannot_delete_missing_species(self):
        with self.assertRaises(ValueError):
            delete_species(-1)

    def test_cannot_delete_species_with_sightings(self):
        location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom")
        _ = create_sighting(location.id, self._species.id, datetime.date(2021, 12, 14), None, Gender.UNKNOWN, False,
                            "Notes")
        with self.assertRaises(ValueError):
            delete_species(self._species.id)
