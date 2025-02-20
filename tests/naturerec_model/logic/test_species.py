import unittest
import datetime
from naturerec_model.model import create_database, Session, Species, Gender, User
from naturerec_model.logic import create_location
from naturerec_model.logic import create_category, get_category
from naturerec_model.logic import create_species, get_species, list_species, update_species, delete_species
from naturerec_model.logic import create_sighting


class TestSpecies(unittest.TestCase):
    def setUp(self) -> None:
        create_database()
        self._user = User(id=1)
        category = create_category("Birds", True, self._user)
        self._species = create_species(category.id, "Red Kite", "Milvus milvus", self._user)

    def test_can_create_species(self):
        category = get_category("Birds")
        with Session.begin() as session:
            species = session.query(Species).one()
        self.assertTrue(category.id, species.categoryId)
        self.assertEqual("Red Kite", species.name)
        self.assertEqual("Milvus milvus", species.scientific_name)

    def test_cannot_create_duplicate_species(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            category_id = session.query(Species).one().categoryId
            _ = create_species(category_id, "Red Kite", "Milvus milvus", self._user)

    def test_can_update_species(self):
        category_id = create_category("Insects", False, self._user).id
        with Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category_id, "Azure Damselfly", "Coenagrion puella", self._user)
        species = get_species(species_id)
        self.assertEqual("Insects", species.category.name)
        self.assertEqual("Azure Damselfly", species.name)
        self.assertEqual("Coenagrion puella", species.scientific_name)

    def test_cannot_update_species_to_create_duplicate(self):
        category = get_category("Birds")
        species = create_species(category.id, "Robin", "Erithacus rubecula", self._user)
        with self.assertRaises(ValueError):
            _ = update_species(species.id, category.id, "Red Kite", "Milvus milvus", self._user)

    def test_cannot_update_missing_species(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError):
            _ = update_species(-1, category.id, "Robin", "Erithacus rubecula", self._user)

    def test_cannot_update_species_with_missing_category(self):
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, -1, "Robin", "Erithacus rubecula", self._user)

    def test_cannot_update_species_with_none_name(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category.id, None, None, self._user)

    def test_cannot_update_species_with_blank_name(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category.id, "", None, self._user)

    def test_cannot_update_species_with_whitespace_name(self):
        category = get_category("Birds")
        with self.assertRaises(ValueError), Session.begin() as session:
            species_id = session.query(Species).one().id
            _ = update_species(species_id, category.id, "      ", None, self._user)

    def test_can_get_species_by_name(self):
        species = get_species("Red Kite")
        self.assertEqual("Red Kite", species.name)

    def test_cannot_get_missing_species_by_name(self):
        with self.assertRaises(ValueError):
            _ = get_species("")

    def test_can_get_species_by_id(self):
        with Session.begin() as session:
            species_id = session.query(Species).one().id
        species = get_species(species_id)
        self.assertEqual("Red Kite", species.name)

    def test_cannot_get_missing_species_by_id(self):
        with self.assertRaises(ValueError):
            _ = get_species(-1)

    def test_cannot_get_species_by_invalid_identifier(self):
        with self.assertRaises(TypeError):
            _ = get_species([])

    def test_can_list_species(self):
        category_id = get_category("Birds").id
        species = list_species(category_id)
        self.assertEqual(1, len(species))
        self.assertEqual("Red Kite", species[0].name)
        self.assertEqual("Milvus milvus", species[0].scientific_name)

    def test_can_delete_species(self):
        category_id = get_category("Birds").id
        species = list_species(category_id)
        self.assertEqual(1, len(species))
        delete_species(self._species.id)
        species = list_species(category_id)
        self.assertEqual(0, len(species))

    def test_cannot_delete_missing_species(self):
        with self.assertRaises(ValueError):
            delete_species(-1)

    def test_cannot_delete_species_with_sightings(self):
        location = create_location(name="Radley Lakes", county="Oxfordshire", country="United Kingdom", user=self._user)
        _ = create_sighting(location.id, self._species.id, datetime.date(2021, 12, 14), None, Gender.UNKNOWN, False,
                            "Notes", self._user)
        with self.assertRaises(ValueError):
            delete_species(self._species.id)
