import unittest

from src.boolean_derivatives import (
    build_all_derivatives,
    build_mixed_derivative,
    build_partial_derivative,
)
from src.truth_table import build_truth_table


class BooleanDerivativesTests(unittest.TestCase):
    def test_partial_derivative_for_and(self) -> None:
        table = build_truth_table("a & b")
        derivative = build_partial_derivative(table, "a")

        self.assertEqual(derivative.derivative_variables, ("a",))
        self.assertEqual(derivative.vector, "0101")
        self.assertEqual(derivative.index, 5)
        self.assertEqual(derivative.expression, "b")

    def test_mixed_derivative_for_and(self) -> None:
        table = build_truth_table("a & b")
        derivative = build_mixed_derivative(table, ("a", "b"))

        self.assertEqual(derivative.vector, "1111")
        self.assertEqual(derivative.index, 15)
        self.assertEqual(derivative.expression, "1")

    def test_partial_derivative_for_xor_is_constant_one(self) -> None:
        table = build_truth_table("a ~ !b")
        derivative = build_partial_derivative(table, "a")

        self.assertEqual(derivative.vector, "1111")
        self.assertEqual(derivative.index, 15)
        self.assertEqual(derivative.expression, "1")

    def test_fourth_order_derivative_for_four_way_and(self) -> None:
        table = build_truth_table("a & b & c & d")
        derivative = build_mixed_derivative(table, ("a", "b", "c", "d"))

        self.assertEqual(derivative.vector, "1" * 16)
        self.assertEqual(derivative.index, 65535)
        self.assertEqual(derivative.expression, "1")

    def test_build_all_derivatives_respects_order_limit(self) -> None:
        table = build_truth_table("a & b & c")
        derivatives = build_all_derivatives(table, max_order=2)

        # C(3,1) + C(3,2) = 3 + 3 = 6
        self.assertEqual(len(derivatives), 6)

    def test_rejects_unknown_variable(self) -> None:
        table = build_truth_table("a & b")
        with self.assertRaises(ValueError):
            build_mixed_derivative(table, ("c",))


if __name__ == "__main__":
    unittest.main()
