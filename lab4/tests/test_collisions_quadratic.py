import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from constants import ACTIVE_SLOT_STATUS
from hash_table import QuadraticProbingHashTable


class QuadraticCollisionTests(unittest.TestCase):
    def test_quadratic_probe_positions_for_same_hash(self) -> None:
        table = QuadraticProbingHashTable(initial_capacity=7, max_load_factor=0.95)
        table.create("AA", "v1")
        table.create("AH", "v2")
        table.create("AO", "v3")
        table.create("AV", "v4")

        index_by_key = {
            row.key: row.index
            for row in table.to_rows()
            if row.status == ACTIVE_SLOT_STATUS
        }

        self.assertEqual(index_by_key["AA"], 0)
        self.assertEqual(index_by_key["AH"], 1)
        self.assertEqual(index_by_key["AO"], 4)
        self.assertEqual(index_by_key["AV"], 2)

    def test_quadratic_probe_wraps_around_table(self) -> None:
        table = QuadraticProbingHashTable(initial_capacity=7, max_load_factor=0.95)
        table.create("AG", "v1")
        table.create("AN", "v2")
        table.create("AU", "v3")

        index_by_key = {
            row.key: row.index
            for row in table.to_rows()
            if row.status == ACTIVE_SLOT_STATUS
        }

        self.assertEqual(index_by_key["AG"], 6)
        self.assertEqual(index_by_key["AN"], 0)
        self.assertEqual(index_by_key["AU"], 3)


if __name__ == "__main__":
    unittest.main()
