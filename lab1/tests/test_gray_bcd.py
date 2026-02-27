import unittest
from src.gray_bcd.converters import decimal_to_gray_bcd, gray_bcd_to_decimal
from src.gray_bcd.addition import add_gray_bcd


class TestGrayBCD(unittest.TestCase):
    def test_direct_gray_conversion(self):
        val = 59
        gray_bcd = decimal_to_gray_bcd(val)
        nibble_5 = gray_bcd.bits[-8:-4]
        nibble_9 = gray_bcd.bits[-4:]

        self.assertEqual(nibble_5, [0, 1, 1, 1])
        self.assertEqual(nibble_9, [1, 1, 0, 1])
        self.assertEqual(gray_bcd_to_decimal(gray_bcd), 59)

    def test_addition_simple(self):
        a = decimal_to_gray_bcd(12)
        b = decimal_to_gray_bcd(34)
        res = add_gray_bcd(a, b)
        self.assertEqual(gray_bcd_to_decimal(res), 46)

    def test_addition_with_carry(self):
        a = decimal_to_gray_bcd(59)
        b = decimal_to_gray_bcd(23)
        res = add_gray_bcd(a, b)
        self.assertEqual(gray_bcd_to_decimal(res), 82)

    def test_addition_cascade_carry(self):
        a = decimal_to_gray_bcd(999)
        b = decimal_to_gray_bcd(1)
        res = add_gray_bcd(a, b)
        self.assertEqual(gray_bcd_to_decimal(res), 1000)

    def test_bounds(self):
        with self.assertRaises(ValueError):
            decimal_to_gray_bcd(100000000)


if __name__ == '__main__':
    unittest.main()
