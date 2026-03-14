import unittest

from src.tabular_minimization import (
    format_tabular_minimization_report,
    minimize_sdnf_tabular,
    minimize_sdnf_tabular_from_expression,
)
from src.truth_table import build_truth_table


class TabularMinimizationTests(unittest.TestCase):
    def test_tabular_minimizes_to_a_or_bc(self) -> None:
        result = minimize_sdnf_tabular_from_expression("a | (b & c)")

        self.assertEqual(result.base_result.minimized_expression, "a | (b & c)")

    def test_tabular_builds_coverage_table(self) -> None:
        result = minimize_sdnf_tabular_from_expression("a | (b & c)")

        self.assertEqual(result.coverage_table.minterms, (3, 4, 5, 6, 7))
        self.assertTrue(len(result.coverage_table.implicants) >= 2)
        self.assertEqual(
            len(result.coverage_table.matrix),
            len(result.coverage_table.implicants),
        )

    def test_tabular_constant_zero(self) -> None:
        result = minimize_sdnf_tabular(build_truth_table("0"))

        self.assertEqual(result.base_result.minimized_expression, "0")
        self.assertEqual(result.coverage_table.minterms, tuple())

    def test_tabular_report_contains_table(self) -> None:
        result = minimize_sdnf_tabular_from_expression("a | (b & c)")
        report = format_tabular_minimization_report(result)

        self.assertIn("Coverage table", report)
        self.assertIn("Minimized SDNF", report)


if __name__ == "__main__":
    unittest.main()
