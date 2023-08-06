import unittest

from routeml.utils import montreal_to_canonical, canonical_to_montreal

class TestConversionFunctions(unittest.TestCase):

    # Tests for montreal_to_canonical function
    def test_montreal_to_canonical_single_element(self):
        self.assertEqual(montreal_to_canonical(['A']), ([0], {'A': 0}))

    def test_montreal_to_canonical_multiple_elements(self):
        self.assertEqual(montreal_to_canonical(['B', 'A', 'C']), ([1, 0, 2], {'A': 0, 'B': 1, 'C': 2}))

    def test_montreal_to_canonical_duplicate_elements(self):
        self.assertEqual(montreal_to_canonical(['A', 'B', 'A']), ([0, 1, 0], {'A': 0, 'B': 1}))

    def test_montreal_to_canonical_empty(self):
        self.assertEqual(montreal_to_canonical([]), ([], {}))

    def test_montreal_to_canonical_integer_elements(self):
        self.assertEqual(montreal_to_canonical([3, 2, 1]), ([2, 1, 0], {1: 0, 2: 1, 3: 2}))

    # Tests for canonical_to_montreal function
    def test_canonical_to_montreal_single_element(self):
        self.assertEqual(canonical_to_montreal([0], {'A': 0}), ['A'])

    def test_canonical_to_montreal_multiple_elements(self):
        self.assertEqual(canonical_to_montreal([1, 0, 2], {'A': 0, 'B': 1, 'C': 2}), ['B', 'A', 'C'])

    def test_canonical_to_montreal_duplicate_elements(self):
        self.assertEqual(canonical_to_montreal([0, 1, 0], {'A': 0, 'B': 1}), ['A', 'B', 'A'])

    def test_canonical_to_montreal_empty(self):
        self.assertEqual(canonical_to_montreal([], {}), [])

    def test_canonical_to_montreal_integer_elements(self):
        self.assertEqual(canonical_to_montreal([2, 1, 0], {1: 0, 2: 1, 3: 2}), [3, 2, 1])

    # More tests
    def test_montreal_to_canonical_and_back(self):
        montreal_sol = [0, 5, 10, 15, 0, 25, 30, 0]
        canonical_sol, node_to_canonical = montreal_to_canonical(montreal_sol)
        montreal_sol_back = canonical_to_montreal(canonical_sol, node_to_canonical)
        self.assertEqual(montreal_sol, montreal_sol_back)

if __name__ == '__main__':
    unittest.main()
