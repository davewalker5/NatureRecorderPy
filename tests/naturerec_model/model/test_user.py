import unittest
from src.naturerec_model.model import create_database, Session, User
from src.naturerec_model.logic import create_user, authenticate


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        create_database()

    def test_can_create_user(self):
        _ = create_user("someone", "somepassword")
        with Session.begin() as session:
            user = session.query(User).all()[0]
        self.assertEqual("someone", user.username)

    def test_can_tidy_username(self):
        _ = create_user("Some One", "somepassword")
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

    def test_can_authenticate(self):
        _ = create_user("someone", "somepassword")
        authenticate("someone", "somepassword")
        # Authentication throws an exception on failure so there's no return here

    def test_cannot_authenticate_missing_user(self):
        with self.assertRaises(ValueError):
            _ = authenticate("notthere", "somepassword")

    def test_cannot_authenticate_with_bad_password(self):
        _ = create_user("someone", "somepassword")
        with self.assertRaises(ValueError):
            _ = authenticate("someone", "wrong")
