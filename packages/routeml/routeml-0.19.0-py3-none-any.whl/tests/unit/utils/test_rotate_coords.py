import unittest
import numpy as np
from math import isclose
from routeml.utils import rotate_coords

class RotateCoordsTest(unittest.TestCase):

    def test_rotation_by_zero_angle(self):
        coords = np.array([[0, 0], [1, 1], [2, 2]])
        angle = 0
        expected_result = coords

        result = rotate_coords(coords, angle)

        self.assertTrue(np.allclose(result, expected_result))

    def test_rotation_by_90_degrees(self):
        coords = np.array([[0, 0], [1, 1], [2, 2]])
        angle = 90
        expected_result = np.array([[0, 0], [-1, 1], [-2, 2]])

        result = rotate_coords(coords, angle)

        self.assertTrue(np.allclose(result, expected_result))

    def test_rotation_by_180_degrees(self):
        coords = np.array([[0, 0], [1, 1], [2, 2]])
        angle = 180
        expected_result = np.array([[0, 0], [-1, -1], [-2, -2]])

        result = rotate_coords(coords, angle)

        self.assertTrue(np.allclose(result, expected_result))

    def test_rotation_by_270_degrees(self):
        coords = np.array([[0, 0], [1, 1], [2, 2]])
        angle = 270
        expected_result = np.array([[0, 0], [1, -1], [2, -2]])

        result = rotate_coords(coords, angle)

        self.assertTrue(np.allclose(result, expected_result))

    def test_rotation_of_single_point(self):
        coords = np.array([[1, 1]])
        angle = 90
        expected_result = np.array([[1, 1]])

        result = rotate_coords(coords, angle)

        self.assertTrue(np.allclose(result, expected_result))

if __name__ == '__main__':
    unittest.main()
