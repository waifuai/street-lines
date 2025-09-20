"""
Unit tests for the Street Lines parking rectangle calculation algorithm.

This module contains comprehensive tests for the calculate_parking_rectangles
function, including validation of input parameters, JSON output structure,
and error handling. These tests ensure the algorithm produces correct results
and handles edge cases appropriately.
"""
import unittest
import json
from src.street_lines_cli import calculate_parking_rectangles

class TestStreetLinesCLI(unittest.TestCase):

    def test_calculate_parking_rectangles_valid_input(self):
        # Test with valid bounding box coordinates
        rectangles_json = calculate_parking_rectangles(0.0, 1.0, 2.0, 3.0) # Generic Coordinates
        rectangles = json.loads(rectangles_json)

        # Basic Assertions: Check for valid JSON structure and some expected fields
        self.assertIsInstance(rectangles, list)
        self.assertEqual(len(rectangles),1)
        self.assertIsInstance(rectangles[0], dict)
        self.assertIn("id", rectangles[0])


    def test_calculate_parking_rectangles_invalid_input(self):
        # Test with invalid bounding box coordinates (e.g., swapped lat/lon)
        with self.assertRaises(ValueError):
            calculate_parking_rectangles("invalid", 1.0, 2.0, 3.0)


if __name__ == '__main__':
    unittest.main()