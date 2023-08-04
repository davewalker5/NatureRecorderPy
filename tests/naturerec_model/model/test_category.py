import unittest
from naturerec_model.model import create_database, Session, Category, User
from naturerec_model.logic import create_category, get_category
from naturerec_model.logic import create_species


class TestCategory(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        category = create_category("Birds", self._user)
        _ = create_species(category.id, "Red Kite", self._user)

    def test_can_create_category(self):
        with Session.begin() as session:
            category = session.query(Category).one()
            self.assertEqual("Birds", category.name)

    def test_cannot_create_duplicate_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = create_species(category.id, "Red Kite", self._user)

    def test_cannot_create_none_category(self):
        with self.assertRaises(ValueError):
            _ = create_category(None, self._user)

    def test_cannot_create_blank_category(self):
        with self.assertRaises(ValueError):
            _ = create_category("", self._user)

    def test_cannot_create_whitespace_category(self):
        with self.assertRaises(ValueError):
            _ = create_category("       ", self._user)

    def test_related_species_returned_with_category(self):
        category = get_category("Birds")
        self.assertEqual(1, len(category.species))
        self.assertEqual("Red Kite", category.species[0].name)
