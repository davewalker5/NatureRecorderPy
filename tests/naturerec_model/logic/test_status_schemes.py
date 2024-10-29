import unittest
import datetime
from naturerec_model.model import create_database, Session, StatusScheme, User
from naturerec_model.logic import create_category
from naturerec_model.logic import create_species
from naturerec_model.logic import create_species_status_rating
from naturerec_model.logic import create_status_rating
from naturerec_model.logic import create_status_scheme, get_status_scheme, list_status_schemes, \
    update_status_scheme, delete_status_scheme


class TestStatusSchemes(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        self._scheme = create_status_scheme("BOCC4", self._user)

    def test_can_create_scheme(self):
        with Session.begin() as session:
            scheme = session.query(StatusScheme).one()
        self.assertEqual("BOCC4", scheme.name)

    def test_can_update_scheme(self):
        with Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
        _ = update_status_scheme(scheme_id, "Some Scheme", self._user)
        scheme = get_status_scheme(scheme_id)
        self.assertEqual("Some Scheme", scheme.name)

    def test_cannot_update_scheme_to_create_duplicate(self):
        scheme = create_status_scheme("Some Scheme", self._user)
        with self.assertRaises(ValueError):
            _ = update_status_scheme(scheme.id, "BOCC4", self._user)

    def test_cannot_update_missing_scheme(self):
        with self.assertRaises(ValueError):
            _ = update_status_scheme(-1, "Some Scheme", self._user)

    def test_cannot_update_scheme_with_none_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
            _ = update_status_scheme(scheme_id, None, self._user)

    def test_cannot_update_scheme_with_blank_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
            _ = update_status_scheme(scheme_id, "", self._user)

    def test_cannot_update_scheme_with_whitespace_name(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            scheme_id = session.query(StatusScheme).one().id
            _ = update_status_scheme(scheme_id, "      ", self._user)

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

    def test_can_list_schemes(self):
        schemes = list_status_schemes()
        self.assertEqual(1, len(schemes))
        self.assertEqual("BOCC4", schemes[0].name)

    def test_can_delete_scheme(self):
        schemes = list_status_schemes()
        self.assertEqual(1, len(schemes))
        delete_status_scheme(self._scheme.id)
        schemes = list_status_schemes()
        self.assertEqual(0, len(schemes))

    def test_cannot_delete_missing_scheme(self):
        with self.assertRaises(ValueError):
            delete_status_scheme(-1)

    def test_can_delete_scheme_with_unused_ratings(self):
        _ = create_status_rating(self._scheme.id, "Amber", self._user)
        schemes = list_status_schemes()
        self.assertEqual(1, len(schemes))
        delete_status_scheme(self._scheme.id)
        schemes = list_status_schemes()
        self.assertEqual(0, len(schemes))

    def test_cannot_delete_scheme_with_species_ratings(self):
        category = create_category("Birds", self._user)
        species = create_species(category.id, "Reed Bunting", None, self._user)
        rating = create_status_rating(self._scheme.id, "Amber", self._user)
        _ = create_species_status_rating(species.id, rating.id, "United Kingdom", datetime.date(2015, 1, 1), self._user)
        with self.assertRaises(ValueError):
            delete_status_scheme(self._scheme.id)
