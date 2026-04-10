import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from exceptions import InvalidKeyError
from hashing import compute_base_hash, compute_v_value, normalize_key


class HashingTests(unittest.TestCase):
    def test_normalize_key_uppercases_and_trims(self) -> None:
        self.assertEqual(normalize_key("  абв  "), "АБВ")
        self.assertEqual(normalize_key("  tree "), "TREE")

    def test_normalize_key_rejects_empty_key(self) -> None:
        with self.assertRaises(InvalidKeyError):
            normalize_key("   ")

    def test_compute_v_value_for_russian_key(self) -> None:
        self.assertEqual(compute_v_value("Вяткин"), 98)

    def test_compute_v_value_for_english_key(self) -> None:
        self.assertEqual(compute_v_value("tree"), 511)

    def test_compute_v_value_rejects_mixed_first_two_letters(self) -> None:
        with self.assertRaises(InvalidKeyError):
            compute_v_value("AЯндекс")

    def test_compute_v_value_requires_two_supported_letters(self) -> None:
        with self.assertRaises(InvalidKeyError):
            compute_v_value("1!")

    def test_compute_base_hash_uses_formula(self) -> None:
        self.assertEqual(compute_base_hash(644, 20, 0), 4)
        self.assertEqual(compute_base_hash(98, 20, 3), 1)

    def test_compute_base_hash_validates_capacity(self) -> None:
        with self.assertRaises(ValueError):
            compute_base_hash(10, 0)


if __name__ == "__main__":
    unittest.main()
