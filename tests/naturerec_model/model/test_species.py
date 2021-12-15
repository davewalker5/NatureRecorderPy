import unittest
from src.naturerec_model.model import create_database, Session, Species
from src.naturerec_model.logic import create_category, get_category
from src.naturerec_model.logic import create_species

class TestSpecies(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        category = create_category("Birds")
        _ = create_species(category.id, "Red Kite")

    def test_can_create_species(self):
        with Session.begin() as session:
            species = session.query(Species).one()
            self.assertEqual("Red Kite", species.name)
            self.assertEqual("Birds", species.category.name)

    def test_cannot_create_species_against_missing_category(self):
        with self.assertRaises(ValueError):
            _ = create_species(-1, "Red Kite")

    def test_cannot_create_duplicate_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "Red Kite")

    def test_cannot_create_none_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, None)

    def test_cannot_create_blank_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "")

    def test_cannot_create_whitespace_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "       ")
