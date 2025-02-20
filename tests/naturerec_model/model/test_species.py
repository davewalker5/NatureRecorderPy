import unittest
from naturerec_model.model import create_database, Session, Species, User
from naturerec_model.logic import create_category, get_category
from naturerec_model.logic import create_species


class TestSpecies(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        category = create_category("Birds", True, self._user)
        _ = create_species(category.id, "Red Kite", "Milvus milvus", self._user)

    def test_can_create_species(self):
        with Session.begin() as session:
            species = session.query(Species).one()
            self.assertEqual("Red Kite", species.name)
            self.assertEqual("Milvus milvus", species.scientific_name)
            self.assertEqual("Birds", species.category.name)

    def test_cannot_create_species_against_missing_category(self):
        with self.assertRaises(ValueError):
            _ = create_species(-1, "Red Kite", None, self._user)

    def test_cannot_create_duplicate_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "Red Kite", None, self._user)

    def test_cannot_create_none_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, None, None, self._user)

    def test_cannot_create_blank_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "", None, self._user)

    def test_cannot_create_whitespace_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "       ", None,self._user)
