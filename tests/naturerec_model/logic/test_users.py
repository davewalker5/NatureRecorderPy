import unittest
from naturerec_model.model import create_database, Session, User
from naturerec_model.logic import create_user, authenticate, get_user


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=-1)

    def test_can_tidy_username(self):
        _ = create_user("Some One", "somepassword", self._user)
        with Session.begin() as session:
            user = session.query(User).all()[0]
        self.assertEqual("someone", user.username)

    def test_can_get_user_by_name(self):
        _ = create_user("someone", "somepassword", self._user)
        user = get_user("someone")
        self.assertEqual("someone", user.username)

    def test_can_get_user_by_id(self):
        _ = create_user("someone", "somepassword", self._user)
        with Session.begin() as session:
            user_id = session.query(User).all()[0].id
        user = get_user(user_id)
        self.assertEqual("someone", user.username)

    def test_cannot_get_missing_user_by_name(self):
        with self.assertRaises(ValueError):
            _ = get_user("Not There")

    def test_cannot_get_missing_user_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_user("-1")

    def test_can_authenticate(self):
        _ = create_user("someone", "somepassword", self._user)
        user = authenticate("someone", "somepassword")
        self.assertEqual("someone", user.username)

    def test_cannot_authenticate_missing_user(self):
        with self.assertRaises(ValueError):
            _ = authenticate("notthere", "somepassword")

    def test_cannot_authenticate_with_bad_password(self):
        _ = create_user("someone", "somepassword", self._user)
        with self.assertRaises(ValueError):
            _ = authenticate("someone", "wrong")
