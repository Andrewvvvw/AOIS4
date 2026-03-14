import unittest

from src.minimization import (
    format_minimization_report,
    minimize_sdnf_calculation,
    minimize_sdnf_calculation_from_expression,
)
from src.truth_table import build_truth_table


class MinimizationTests(unittest.TestCase):
    def test_minimizes_to_a_or_bc(self) -> None:
        result = minimize_sdnf_calculation_from_expression("a | (b & c)")

        self.assertEqual(result.minimized_expression, "a | (b & c)")
        self.assertTrue(len(result.stages) >= 1)

    def test_minimization_for_constant_zero(self) -> None:
        result = minimize_sdnf_calculation(build_truth_table("0"))

        self.assertEqual(result.minimized_expression, "0")
        self.assertEqual(result.stages, tuple())
        self.assertEqual(result.selected_implicants, tuple())

    def test_minimization_for_constant_one(self) -> None:
        result = minimize_sdnf_calculation(build_truth_table("1"))

        self.assertEqual(result.minimized_expression, "1")

    def test_report_contains_gluing_stage(self) -> None:
        result = minimize_sdnf_calculation_from_expression("a | (b & c)")
        report = format_minimization_report(result)

        self.assertIn("Gluing stage", report)
        self.assertIn("Minimized SDNF", report)


if __name__ == "__main__":
    unittest.main()
