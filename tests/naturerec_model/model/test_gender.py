import unittest
from src.naturerec_model.model import Gender


class TestGender(unittest.TestCase):
    def test_can_get_unknown_gender_name(self):
        self.assertEqual("Unknown", Gender.gender_name(Gender.UNKNOWN))

    def test_can_get_male_gender_name(self):
        self.assertEqual("Male", Gender.gender_name(Gender.MALE))

    def test_can_get_female_gender_name(self):
        self.assertEqual("Female", Gender.gender_name(Gender.FEMALE))

    def test_can_get_both_gender_name(self):
        self.assertEqual("Both", Gender.gender_name(Gender.BOTH))

    def test_can_get_gender_map(self):
        gender_map = Gender.gender_map()
        self.assertEqual("Unknown", gender_map[Gender.UNKNOWN])
        self.assertEqual("Male", gender_map[Gender.MALE])
        self.assertEqual("Female", gender_map[Gender.FEMALE])
        self.assertEqual("Both", gender_map[Gender.BOTH])
