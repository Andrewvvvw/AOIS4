import unittest
from src.converters.to_binary import to_additional
from src.converters.to_decimal import additional_to_decimal
from src.arithmetic.addition import add_binary


class TestAddition(unittest.TestCase):
    def test_add_positive_numbers(self):
        a = to_additional(15)
        b = to_additional(25)
        result = add_binary(a, b)
        self.assertEqual(additional_to_decimal(result), 40)

    def test_add_negative_and_positive(self):
        a = to_additional(-15)
        b = to_additional(25)
        result = add_binary(a, b)
        self.assertEqual(additional_to_decimal(result), 10)

    def test_add_negative_numbers(self):
        a = to_additional(-10)
        b = to_additional(-20)
        result = add_binary(a, b)
        self.assertEqual(additional_to_decimal(result), -30)

    def test_add_zero(self):
        a = to_additional(42)
        b = to_additional(0)
        result = add_binary(a, b)
        self.assertEqual(additional_to_decimal(result), 42)


if __name__ == "__main__":
    unittest.main()