import unittest

from src.index_form import build_index_form
from src.truth_table import build_truth_table


class IndexFormTests(unittest.TestCase):
    def test_builds_index_form_for_and(self) -> None:
        table = build_truth_table("a & b")
        form = build_index_form(table)

        self.assertEqual(form.vector, "0001")
        self.assertEqual(form.index, 1)

    def test_builds_index_form_for_or(self) -> None:
        table = build_truth_table("a | b")
        form = build_index_form(table)

        self.assertEqual(form.vector, "0111")
        self.assertEqual(form.index, 7)

    def test_builds_index_form_for_constant_one(self) -> None:
        table = build_truth_table("1")
        form = build_index_form(table)

        self.assertEqual(form.vector, "1")
        self.assertEqual(form.index, 1)

    def test_builds_index_form_for_constant_zero(self) -> None:
        table = build_truth_table("0")
        form = build_index_form(table)

        self.assertEqual(form.vector, "0")
        self.assertEqual(form.index, 0)


if __name__ == "__main__":
    unittest.main()
