import unittest
from src.converters.to_binary import to_additional
from src.converters.to_decimal import additional_to_decimal
from src.arithmetic.subtraction import subtract_binary


class TestSubtraction(unittest.TestCase):
    def test_subtract_positive(self):
        a = to_additional(50)
        b = to_additional(20)
        result = subtract_binary(a, b)
        self.assertEqual(additional_to_decimal(result), 30)

    def test_subtract_to_negative(self):
        a = to_additional(20)
        b = to_additional(50)
        result = subtract_binary(a, b)
        self.assertEqual(additional_to_decimal(result), -30)

    def test_subtract_negative_from_positive(self):
        a = to_additional(10)
        b = to_additional(-5)
        result = subtract_binary(a, b)
        self.assertEqual(additional_to_decimal(result), 15)

    def test_subtract_negative(self):
        a = to_additional(-10)
        b = to_additional(-5)
        result = subtract_binary(a, b)
        self.assertEqual(additional_to_decimal(result), -5)

    def test_subtract_same_number(self):
        a = to_additional(100)
        result = subtract_binary(a, a)
        self.assertEqual(additional_to_decimal(result), 0)


if __name__ == "__main__":
    unittest.main()