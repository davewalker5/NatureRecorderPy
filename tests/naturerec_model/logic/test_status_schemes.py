import unittest
from src.naturerec_model.model import create_database, Session, StatusScheme
from src.naturerec_model.logic import create_status_scheme, get_status_scheme, list_status_schemes, \
    update_status_scheme


class TestStatusSchemes(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        _ = create_status_scheme("BOCC4")

    def test_can_create_scheme(self):
        with Session.begin() as session:
            scheme = session.query(StatusScheme).one()
        self.assertEqual("BOCC4", scheme.name)

    def test_can_update_scheme(self):
        with Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
        _ = update_status_scheme(scheme_id, "Some Scheme")
        scheme = get_status_scheme(scheme_id)
        self.assertEqual("Some Scheme", scheme.name)

    def test_cannot_update_scheme_to_create_duplicate(self):
        scheme = create_status_scheme("Some Scheme")
        with self.assertRaises(ValueError):
            _ = update_status_scheme(scheme.id, "BOCC4")

    def test_cannot_update_missing_scheme(self):
        with self.assertRaises(ValueError):
            _ = update_status_scheme(-1, "Some Scheme")

    def test_cannot_update_scheme_with_none_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
            _ = update_status_scheme(scheme_id, None)

    def test_cannot_update_scheme_with_blank_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
            _ = update_status_scheme(scheme_id, "")

    def test_cannot_update_scheme_with_whitespace_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
            _ = update_status_scheme(scheme_id, "      ")

    def test_can_get_scheme_by_name(self):
        scheme = get_status_scheme("BOCC4")
        self.assertEqual("BOCC4", scheme.name)

    def test_cannot_get_missing_scheme_by_name(self):
        with self.assertRaises(ValueError):
            _ = get_status_scheme("")

    def test_can_get_scheme_by_id(self):
        with Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
        scheme = get_status_scheme(scheme_id)
        self.assertEqual("BOCC4", scheme.name)

    def test_cannot_get_missing_scheme_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_status_scheme(-1)

    def test_cannot_get_scheme_by_invalid_identifier(self):
        with self.assertRaises(TypeError):
            _ = get_status_scheme([])

    def test_can_list_categories(self):
        schemes = list_status_schemes()
        self.assertEqual(1, len(schemes))
        self.assertEqual("BOCC4", schemes[0].name)
