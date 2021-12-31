import unittest
from src.naturerec_model.logic import geocode_postcode


class TestLocations(unittest.TestCase):
    def test_can_geocode_uk_postcode(self):
        coordinates = geocode_postcode("OX14 3HG", "United Kingdom")
        self.assertEqual(51.6276, coordinates["latitude"])
        self.assertEqual(-1.255983, coordinates["longitude"])

    def test_can_geocode_postcode_with_leading_trailing_whitespace(self):
        coordinates = geocode_postcode("    OX14 3HG    ", "United Kingdom")
        self.assertEqual(51.6276, coordinates["latitude"])
        self.assertEqual(-1.255983, coordinates["longitude"])

    def test_can_geocode_non_uk_postcode(self):
        coordinates = geocode_postcode("03189", "Spain")
        self.assertEqual(37.9391, coordinates["latitude"])
        self.assertEqual(-0.735096, coordinates["longitude"])

    def test_can_geocode_for_country_with_whitespace(self):
        coordinates = geocode_postcode("OX14 3HG", "   united     Kingdom   ")
        self.assertEqual(51.6276, coordinates["latitude"])
        self.assertEqual(-1.255983, coordinates["longitude"])

    def test_cannot_geocode_none_postcode(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode(None, "United Kingdom")

    def test_cannot_geocode_blank_postcode(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode("", "United Kingdom")

    def test_cannot_geocode_whitespace_postcode(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode("     ", "United Kingdom")

    def test_cannot_geocode_invalid_postcode(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode("This isn't a real postcode", "United Kingdom")

    def test_cannot_geocode_for_none_country(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode("OX14 3HG", None)

    def test_cannot_geocode_for_blank_country(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode("OX14 3HG", "")

    def test_cannot_geocode_for_whitespace_country(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode("OX14 3HG", "         ")

    def test_cannot_geocode_for_invalid_country(self):
        with self.assertRaises(ValueError):
            _ = geocode_postcode("OX14 3HG", "This is not a valid country name")
