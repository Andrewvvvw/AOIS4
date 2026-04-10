import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from constants import ACTIVE_SLOT_STATUS
from exceptions import DuplicateKeyError, KeyNotFoundError
from hash_table import QuadraticProbingHashTable


class HashTableCrudTests(unittest.TestCase):
    def setUp(self) -> None:
        self.table = QuadraticProbingHashTable(initial_capacity=23, max_load_factor=0.9)

    def test_create_and_read(self) -> None:
        self.table.create("Абаев", "Сергей")
        self.assertEqual(self.table.read("Абаев"), "Сергей")
        self.assertIsNone(self.table.read("Несуществующий"))

    def test_create_rejects_duplicate_keys(self) -> None:
        self.table.create("Tree", "Oak")
        with self.assertRaises(DuplicateKeyError):
            self.table.create("tree", "Maple")

    def test_update_existing_key(self) -> None:
        self.table.create("Tree", "Oak")
        self.table.update("Tree", "Pine")
        self.assertEqual(self.table.read("Tree"), "Pine")

    def test_update_missing_key_raises(self) -> None:
        with self.assertRaises(KeyNotFoundError):
            self.table.update("Missing", "value")

    def test_delete_existing_key(self) -> None:
        self.table.create("Tree", "Oak")
        self.table.delete("Tree")
        self.assertIsNone(self.table.read("Tree"))

    def test_delete_missing_key_raises(self) -> None:
        with self.assertRaises(KeyNotFoundError):
            self.table.delete("Missing")

    def test_to_rows_contains_active_slot_data(self) -> None:
        self.table.create("Tree", "Oak")
        rows = self.table.to_rows()
        active_rows = [row for row in rows if row.status == ACTIVE_SLOT_STATUS]
        self.assertEqual(len(active_rows), 1)
        self.assertEqual(active_rows[0].key, "TREE")
        self.assertEqual(active_rows[0].value, "Oak")

    def test_to_rows_contains_lab6_style_columns(self) -> None:
        self.table.create("AA", "value")
        row = next(item for item in self.table.to_rows() if item.id_value == "AA")
        self.assertEqual(row.id_value, "AA")
        self.assertEqual(row.used_flag, 1)
        self.assertEqual(row.deleted_flag, 0)
        self.assertEqual(row.link_flag, 0)
        self.assertEqual(row.pointer_or_data, "value")


if __name__ == "__main__":
    unittest.main()
