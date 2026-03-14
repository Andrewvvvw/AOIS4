import unittest

from src.truth_table import build_truth_table
from src.zhegalkin import build_zhegalkin_polynomial


class ZhegalkinTests(unittest.TestCase):
    def test_builds_polynomial_for_and(self) -> None:
        table = build_truth_table("a & b")
        polynomial = build_zhegalkin_polynomial(table)

        self.assertEqual(polynomial.expression, "a*b")
        self.assertEqual(polynomial.max_degree, 2)

    def test_builds_polynomial_for_or(self) -> None:
        table = build_truth_table("a | b")
        polynomial = build_zhegalkin_polynomial(table)

        self.assertEqual(polynomial.expression, "a ^ b ^ a*b")
        self.assertEqual(polynomial.max_degree, 2)

    def test_builds_polynomial_for_not_a(self) -> None:
        table = build_truth_table("!a")
        polynomial = build_zhegalkin_polynomial(table)

        self.assertEqual(polynomial.expression, "1 ^ a")
        self.assertEqual(polynomial.max_degree, 1)

    def test_builds_polynomial_for_constant_zero(self) -> None:
        table = build_truth_table("0")
        polynomial = build_zhegalkin_polynomial(table)

        self.assertEqual(polynomial.expression, "0")
        self.assertEqual(polynomial.max_degree, 0)


if __name__ == "__main__":
    unittest.main()
