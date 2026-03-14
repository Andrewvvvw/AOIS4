import unittest

from src.karnaugh import (
    format_karnaugh_report,
    minimize_sdnf_karnaugh,
    minimize_sdnf_karnaugh_from_expression,
    minimize_sknf_karnaugh,
    minimize_sknf_karnaugh_from_expression,
)
from src.truth_table import build_truth_table


class KarnaughTests(unittest.TestCase):
    def test_karnaugh_minimizes_to_a_or_bc(self) -> None:
        result = minimize_sdnf_karnaugh_from_expression("a | (b & c)")

        self.assertEqual(result.minimized_expression, "a | (b & c)")

    def test_karnaugh_map_shape_for_three_variables(self) -> None:
        result = minimize_sdnf_karnaugh_from_expression("a | (b & c)")

        self.assertEqual(len(result.kmap.values), 2)
        self.assertEqual(len(result.kmap.values[0]), 4)
        self.assertEqual(result.kmap.row_variables, ("a",))
        self.assertEqual(result.kmap.col_variables, ("b", "c"))

    def test_karnaugh_constant_zero(self) -> None:
        result = minimize_sdnf_karnaugh(build_truth_table("0"))

        self.assertEqual(result.minimized_expression, "0")
        self.assertEqual(result.selected_implicants, tuple())

    def test_karnaugh_rejects_more_than_four_variables(self) -> None:
        table = build_truth_table("a & b & c & d & e")
        with self.assertRaises(ValueError):
            minimize_sdnf_karnaugh(table)

    def test_karnaugh_report_contains_table(self) -> None:
        result = minimize_sdnf_karnaugh_from_expression("a | (b & c)")
        report = format_karnaugh_report(result)

        self.assertIn("Karnaugh map method", report)
        self.assertIn("rows\\cols", report)
        self.assertIn("Minimized SDNF", report)

    def test_karnaugh_sknf_minimizes_to_a_or_b_and_a_or_c(self) -> None:
        result = minimize_sknf_karnaugh_from_expression("a | (b & c)")

        self.assertEqual(result.minimized_expression, "(a | b) & (a | c)")

    def test_karnaugh_sknf_constant_one(self) -> None:
        result = minimize_sknf_karnaugh(build_truth_table("1"))

        self.assertEqual(result.minimized_expression, "1")

    def test_karnaugh_sknf_report_contains_label(self) -> None:
        result = minimize_sknf_karnaugh_from_expression("a | (b & c)")
        report = format_karnaugh_report(result)

        self.assertIn("Minimized SKNF", report)


if __name__ == "__main__":
    unittest.main()
