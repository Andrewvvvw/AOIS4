import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from constants import ACTIVE_SLOT_STATUS
from hash_table import QuadraticProbingHashTable


class DeleteTombstoneTests(unittest.TestCase):
    def test_delete_keeps_chain_searchable_and_reuses_tombstone(self) -> None:
        table = QuadraticProbingHashTable(initial_capacity=7, max_load_factor=0.95)
        table.create("AA", "v1")
        table.create("AH", "v2")
        table.create("AO", "v3")

        table.delete("AH")
        self.assertEqual(table.read("AO"), "v3")

        table.create("AV", "v4")
        self.assertEqual(table.read("AV"), "v4")
        self.assertEqual(table.read("AO"), "v3")

        index_by_key = {
            row.key: row.index
            for row in table.to_rows()
            if row.status == ACTIVE_SLOT_STATUS
        }
        self.assertEqual(index_by_key["AV"], 1)


if __name__ == "__main__":
    unittest.main()
