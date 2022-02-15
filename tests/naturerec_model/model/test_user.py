import unittest
from src.naturerec_model.model import create_database, Session, User
from src.naturerec_model.logic import create_user


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        create_database()

    def test_can_create_user(self):
        _ = create_user("someone", "somepassword")
        with Session.begin() as session:
            user = session.query(User).all()[0]
        self.assertEqual("someone", user.username)

    def test_cannot_create_duplicate_user(self):
        _ = create_user("someone", "somepassword")
        with self.assertRaises(ValueError):
            _ = create_user("someone", "somepassword")

    def test_cannot_create_user_with_blank_name(self):
        with self.assertRaises(ValueError):
            _ = create_user("", "somepassword")

    def test_cannot_create_user_with_none_name(self):
        with self.assertRaises(ValueError):
            _ = create_user(None, "somepassword")

    def test_cannot_create_user_with_blank_password(self):
        with self.assertRaises(ValueError):
            _ = create_user("someone", "")

    def test_cannot_create_user_with_none_password(self):
        with self.assertRaises(ValueError):
            _ = create_user("someone", None)
