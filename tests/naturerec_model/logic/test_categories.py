import unittest
from src.naturerec_model.model import create_database, Session, Category
from src.naturerec_model.logic import create_category, get_category, list_categories


class TestCategories(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        _ = create_category("Birds")

    def test_can_create_category(self):
        with Session.begin() as session:
            category = session.query(Category).one()
        self.assertEqual("Birds", category.name)

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
