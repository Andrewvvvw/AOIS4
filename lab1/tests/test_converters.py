import unittest
from src.converters.to_binary import to_direct, to_reverse, to_additional
from src.config import BIT_COUNT


class TestConverters(unittest.TestCase):
    def test_positive_is_identical(self):
        val = 10
        direct = to_direct(val)
        reverse = to_reverse(val)
        additional = to_additional(val)
        self.assertEqual(direct, reverse)
        self.assertEqual(reverse, additional)

    def test_reverse_negative(self):
        result = to_reverse(-5)
        bits = result.bits

        correct_bits = [1] * BIT_COUNT
        correct_bits[-1] = 0
        correct_bits[-3] = 0

        self.assertEqual(bits, correct_bits)

    def test_additional_negative(self):
        result = to_additional(-5)
        bits = result.bits

        correct_bits = [1] * BIT_COUNT
        correct_bits[-3] = 0

        self.assertEqual(bits, correct_bits)

    def test_zero_additional(self):
        result = to_additional(0)
        self.assertEqual(result.bits, [0] * BIT_COUNT)


if __name__ == "__main__":
    unittest.main()