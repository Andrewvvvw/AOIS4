import unittest
from src.ieee754.converters import float_to_ieee754


class TestIEEE754Converters(unittest.TestCase):
    def test_zero(self):
        result = float_to_ieee754(0.0)
        self.assertEqual(result.bits, [0] * 32)

    def test_positive_integer(self):
        result = float_to_ieee754(5.0)
        bits = result.bits
        self.assertEqual(bits[0], 0)
        self.assertEqual(bits[1:9], [1, 0, 0, 0, 0, 0, 0, 1])
        expected_mantissa = [0, 1] + [0] * 21
        self.assertEqual(bits[9:], expected_mantissa)

    def test_negative_fraction(self):
        result = float_to_ieee754(-0.15625)
        bits = result.bits
        self.assertEqual(bits[0], 1)
        self.assertEqual(bits[1:9], [0, 1, 1, 1, 1, 1, 0, 0])
        expected_mantissa = [0, 1] + [0] * 21
        self.assertEqual(bits[9:], expected_mantissa)

    def test_positive_float(self):
        result = float_to_ieee754(85.125)
        bits = result.bits
        self.assertEqual(bits[0], 0)
        self.assertEqual(bits[1:9], [1, 0, 0, 0, 0, 1, 0, 1])
        expected_mantissa = [0, 1, 0, 1, 0, 1, 0, 0, 1, ] + [0] * 14
        self.assertEqual(bits[9:], expected_mantissa)


if __name__ == "__main__":
    unittest.main()