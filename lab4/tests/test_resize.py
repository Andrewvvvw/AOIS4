import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from hash_table import QuadraticProbingHashTable


class ResizeTests(unittest.TestCase):
    def test_resize_happens_on_projected_load(self) -> None:
        table = QuadraticProbingHashTable(initial_capacity=5, max_load_factor=0.6)
        initial_capacity = table.capacity

        table.create("AA", "v1")
        table.create("AB", "v2")
        table.create("AC", "v3")
        table.create("AD", "v4")

        self.assertGreater(table.capacity, initial_capacity)
        self.assertEqual(table.read("AA"), "v1")
        self.assertEqual(table.read("AB"), "v2")
        self.assertEqual(table.read("AC"), "v3")
        self.assertEqual(table.read("AD"), "v4")

    def test_resize_happens_when_probe_cannot_find_slot(self) -> None:
        table = QuadraticProbingHashTable(initial_capacity=7, max_load_factor=0.95)
        initial_capacity = table.capacity

        table.create("AA", "v1")
        table.create("AH", "v2")
        table.create("AO", "v3")
        table.create("AV", "v4")
        table.create("BC", "v5")

        self.assertGreater(table.capacity, initial_capacity)
        self.assertEqual(table.read("BC"), "v5")


if __name__ == "__main__":
    unittest.main()
