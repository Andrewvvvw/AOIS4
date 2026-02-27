import unittest
from src.ieee754.converters import float_to_ieee754
from src.ieee754.multiplication import multiply_ieee754
from src.ieee754.division import divide_ieee754


class TestIEEE754MultDiv(unittest.TestCase):
    def test_multiply_positive(self):
        a = float_to_ieee754(2.5)
        b = float_to_ieee754(3.0)
        expected = float_to_ieee754(7.5)
        self.assertEqual(multiply_ieee754(a, b), expected)

    def test_multiply_mixed_signs(self):
        a = float_to_ieee754(-1.5)
        b = float_to_ieee754(1.5)
        expected = float_to_ieee754(-2.25)
        self.assertEqual(multiply_ieee754(a, b), expected)

    def test_multiply_by_zero(self):
        a = float_to_ieee754(42.0)
        b = float_to_ieee754(0.0)
        expected = float_to_ieee754(0.0)
        self.assertEqual(multiply_ieee754(a, b), expected)

    def test_divide_clean(self):
        a = float_to_ieee754(10.0)
        b = float_to_ieee754(2.0)
        expected = float_to_ieee754(5.0)
        self.assertEqual(divide_ieee754(a, b), expected)

    def test_divide_fractional(self):
        a = float_to_ieee754(1.0)
        b = float_to_ieee754(4.0)
        expected = float_to_ieee754(0.25)
        self.assertEqual(divide_ieee754(a, b), expected)

    def test_zero_division(self):
        a = float_to_ieee754(5.0)
        b = float_to_ieee754(0.0)
        with self.assertRaises(ZeroDivisionError):
            divide_ieee754(a, b)


if __name__ == "__main__":
    unittest.main()