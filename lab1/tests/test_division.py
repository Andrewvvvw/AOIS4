import unittest
from src.converters.to_binary import to_direct
from src.arithmetic.division import divide_binary
from src.config import BIT_COUNT


class TestDivision(unittest.TestCase):
    def test_divide_clean(self):
        a = to_direct(10)
        b = to_direct(2)
        result = divide_binary(a, b)

        expected = [0] * BIT_COUNT
        expected[26] = 1
        expected[25] = 0
        expected[24] = 1

        self.assertEqual(result.bits, expected)

    def test_divide_with_fraction(self):
        a = to_direct(10)
        b = to_direct(3)
        result = divide_binary(a, b)

        expected = [0] * BIT_COUNT
        expected[25] = 1
        expected[26] = 1
        expected[28] = 1
        expected[30] = 1

        self.assertEqual(result.bits, expected)

    def test_divide_negative_and_positive(self):
        a = to_direct(-15)
        b = to_direct(4)
        result = divide_binary(a, b)

        expected = [0] * BIT_COUNT
        expected[0] = 1
        expected[25] = 1

        expected[26] = 1
        expected[27] = 1
        expected[28] = 1

        self.assertEqual(result.bits, expected)

    def test_zero_division(self):
        a = to_direct(5)
        b = to_direct(0)
        with self.assertRaises(ZeroDivisionError):
            divide_binary(a, b)


if __name__ == "__main__":
    unittest.main()