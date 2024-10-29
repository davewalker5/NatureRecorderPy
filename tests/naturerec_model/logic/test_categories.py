import unittest
from naturerec_model.model import create_database, Session, Category, User
from naturerec_model.logic import create_category, get_category, list_categories, update_category, delete_category
from naturerec_model.logic import create_species



class TestCategories(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        self._category = create_category("Birds", self._user)

    def test_can_create_category(self):
        with Session.begin() as session:
            category = session.query(Category).one()
        self.assertEqual("Birds", category.name)

    def test_cannot_create_duplicate_category(self):
        with self.assertRaises(ValueError):
            _ = create_category("Birds", self._user)

    def test_can_update_category(self):
        with Session.begin() as session:
            category_id = session.query(Category).one().id
            _ = update_category(category_id, "Insects", self._user)
            updated = session.query(Category).get(category_id)
            self.assertEqual("Insects", updated.name)

    def test_cannot_update_category_to_create_duplicate(self):
        with Session.begin() as session:
            category_id = session.query(Category).one().id

        _ = create_category("Insects", self._user)

        with self.assertRaises(ValueError):
            _ = update_category(category_id, "Insects", self._user)

    def test_cannot_update_missing_category(self):
        with self.assertRaises(ValueError):
            _ = update_category(-1, "Insects", self._user)

    def test_cannot_update_category_with_none_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            category_id = session.query(Category).one().id
            _ = update_category(category_id, None, self._user)

    def test_cannot_update_category_with_blank_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            category_id = session.query(Category).one().id
            _ = update_category(category_id, "", self._user)

    def test_cannot_update_category_with_whitespace_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            category_id = session.query(Category).one().id
            _ = update_category(category_id, "      ", self._user)

    def test_can_get_category_by_name(self):
        category = get_category("Birds")
        self.assertEqual("Birds", category.name)

    def test_cannot_get_missing_category_by_name(self):
        with self.assertRaises(ValueError):
            _ = get_category("Insects")

    def test_can_get_category_by_id(self):
        with Session.begin() as session:
            category_id = session.query(Category).one().id
        category = get_category(category_id)
        self.assertEqual("Birds", category.name)

    def test_cannot_get_missing_category_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_category(-1)

    def test_cannot_get_category_by_invalid_identifier(self):
        with self.assertRaises(TypeError):
            _ = get_category([])

    def test_can_list_categories(self):
        categories = list_categories()
        self.assertEqual(1, len(categories))
        self.assertEqual("Birds", categories[0].name)

    def test_can_delete_category(self):
        categories = list_categories()
        self.assertEqual(1, len(categories))
        delete_category(self._category.id)
        categories = list_categories()
        self.assertEqual(0, len(categories))

    def test_cannot_delete_missing_category(self):
        with self.assertRaises(ValueError):
            delete_category(-1)

    def test_cannot_delete_category_with_species(self):
        _ = create_species(self._category.id, "Blackbird", None, self._user)
        with self.assertRaises(ValueError):
            delete_category(self._category.id)
