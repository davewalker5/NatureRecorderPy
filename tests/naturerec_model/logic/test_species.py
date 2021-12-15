import unittest
from src.naturerec_model.model import create_database, Session, Species
from src.naturerec_model.logic import create_category, get_category
from src.naturerec_model.logic import create_species, get_species, list_species


class TestSpecies(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        category = create_category("Birds")
        _ = create_species(category.id, "Red Kite")

    def test_can_create_species(self):
        category = get_category("Birds")
        with Session.begin() as session:
            species = session.query(Species).one()
        self.assertTrue(category.id, species.categoryId)
        self.assertEqual("Red Kite", species.name)

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
