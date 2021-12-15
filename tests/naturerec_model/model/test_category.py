import unittest
from src.naturerec_model.model import create_database, Session, Category
from src.naturerec_model.logic import create_category, get_category
from src.naturerec_model.logic import create_species

class TestCategory(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        category = create_category("Birds")
        _ = create_species(category.id, "Red Kite")

    def test_can_create_category(self):
        with Session.begin() as session:
            category = session.query(Category).one()
            self.assertEqual("Birds", category.name)

    def test_cannot_create_duplicate_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "Red Kite")

    def test_cannot_create_none_category(self):
        with self.assertRaises(ValueError):
            _ = create_category(None)

    def test_cannot_create_blank_category(self):
        with self.assertRaises(ValueError):
            _ = create_category("")

    def test_cannot_create_whitespace_category(self):
        with self.assertRaises(ValueError):
            _ = create_category("       ")

    def test_related_species_returned_with_category(self):
        category = get_category("Birds")
        self.assertEqual(1, len(category.species))
        self.assertEqual("Red Kite", category.species[0].name)
