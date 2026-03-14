import unittest

from src.truth_table import build_truth_table


class TruthTableTests(unittest.TestCase):
    def test_builds_table_for_two_variables(self) -> None:
        table = build_truth_table("a & b")

        self.assertEqual(table.variables, ("a", "b"))
        self.assertEqual(len(table.rows), 4)

        expected = [
            ((False, False), False),
            ((False, True), False),
            ((True, False), False),
            ((True, True), True),
        ]
        actual = [(row.values, row.result) for row in table.rows]
        self.assertEqual(actual, expected)

    def test_builds_table_for_expression_with_unicode_operators(self) -> None:
        table = build_truth_table("!(!a→!b)∨c")

        self.assertEqual(table.variables, ("a", "b", "c"))
        self.assertEqual(len(table.rows), 8)

        row = table.rows[4]
        self.assertEqual(row.values, (True, False, False))
        self.assertFalse(row.result)

    def test_builds_table_for_constant_expression(self) -> None:
        table = build_truth_table("1")

        self.assertEqual(table.variables, tuple())
        self.assertEqual(len(table.rows), 1)
        self.assertEqual(table.rows[0].values, tuple())
        self.assertTrue(table.rows[0].result)


if __name__ == "__main__":
    unittest.main()
