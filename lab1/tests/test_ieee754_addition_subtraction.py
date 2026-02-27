import unittest
from src.ieee754.converters import float_to_ieee754
from src.ieee754.addition_subtraction import add_ieee754, subtract_ieee754


class TestIEEE754Addition(unittest.TestCase):
    def test_add_positive(self):
        a = float_to_ieee754(5.5)
        b = float_to_ieee754(3.25)
        expected = float_to_ieee754(8.75)
        result = add_ieee754(a, b)
        self.assertEqual(result, expected)

    def test_add_mixed_signs(self):
        a = float_to_ieee754(10.0)
        b = float_to_ieee754(-2.5)
        expected = float_to_ieee754(7.5)
        result = add_ieee754(a, b)
        self.assertEqual(result, expected)

    def test_add_negatives(self):
        a = float_to_ieee754(-1.125)
        b = float_to_ieee754(-2.0)
        expected = float_to_ieee754(-3.125)
        result = add_ieee754(a, b)
        self.assertEqual(result, expected)

    def test_subtract_positive(self):
        a = float_to_ieee754(15.5)
        b = float_to_ieee754(5.25)
        expected = float_to_ieee754(10.25)
        result = subtract_ieee754(a, b)
        self.assertEqual(result, expected)

    def test_subtract_to_negative(self):
        a = float_to_ieee754(2.0)
        b = float_to_ieee754(5.0)
        expected = float_to_ieee754(-3.0)
        result = subtract_ieee754(a, b)
        self.assertEqual(result, expected)

    def test_add_zero(self):
        a = float_to_ieee754(42.0)
        b = float_to_ieee754(0.0)
        result = add_ieee754(a, b)
        self.assertEqual(result, a)

    def test_exponent_alignment(self):
        a = float_to_ieee754(1024.0)
        b = float_to_ieee754(1.0)
        expected = float_to_ieee754(1025.0)
        result = add_ieee754(a, b)
        self.assertEqual(result, expected)

    def test_carry_in_mantissa(self):
        a = float_to_ieee754(1.5)
        b = float_to_ieee754(1.5)
        expected = float_to_ieee754(3.0)
        result = add_ieee754(a, b)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()