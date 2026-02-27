import unittest
from src.converters.to_binary import to_direct
from src.converters.to_decimal import direct_to_decimal
from src.arithmetic.multiplication import multiply_binary


class TestMultiplication(unittest.TestCase):
    def test_multiply_positive_numbers(self):
        a = to_direct(5)
        b = to_direct(6)
        result = multiply_binary(a, b)
        self.assertEqual(direct_to_decimal(result), 30)

    def test_multiply_negative_and_positive(self):
        a = to_direct(-4)
        b = to_direct(7)
        result = multiply_binary(a, b)
        self.assertEqual(direct_to_decimal(result), -28)

    def test_multiply_negative_numbers(self):
        a = to_direct(-8)
        b = to_direct(-3)
        result = multiply_binary(a, b)
        self.assertEqual(direct_to_decimal(result), 24)

    def test_multiply_by_zero(self):
        a = to_direct(-15)
        b = to_direct(0)
        result = multiply_binary(a, b)
        self.assertEqual(direct_to_decimal(result), 0)
        self.assertEqual(result.bits[0], 0)

    def test_multiply_large_numbers(self):
        a = to_direct(1024)
        b = to_direct(20)
        result = multiply_binary(a, b)
        self.assertEqual(direct_to_decimal(result), 20480)


if __name__ == "__main__":
    unittest.main()