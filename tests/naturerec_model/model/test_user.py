import unittest
from naturerec_model.model import create_database, Session, User
from naturerec_model.logic import create_user


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)

    def test_can_create_user(self):
        _ = create_user("someone", "somepassword", self._user)
        with Session.begin() as session:
            user = session.query(User).all()[0]
        self.assertEqual("someone", user.username)

    def test_cannot_create_duplicate_user(self):
        _ = create_user("someone", "somepassword", self._user)
        with self.assertRaises(ValueError):
            _ = create_user("someone", "somepassword", self._user)

    def test_cannot_create_user_with_blank_name(self):
        with self.assertRaises(ValueError):
            _ = create_user("", "somepassword", self._user)

    def test_cannot_create_user_with_none_name(self):
        with self.assertRaises(ValueError):
            _ = create_user(None, "somepassword", self._user)

    def test_cannot_create_user_with_blank_password(self):
        with self.assertRaises(ValueError):
            _ = create_user("someone", "", self._user)

    def test_cannot_create_user_with_none_password(self):
        with self.assertRaises(ValueError):
            _ = create_user("someone", None, self._user)
