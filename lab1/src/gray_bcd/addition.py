from src.models import BinaryNumber
from src.config import BIT_COUNT
from src.gray_bcd.converters import _digit_to_gray, _gray_to_digit


def add_gray_bcd(a: BinaryNumber, b: BinaryNumber) -> BinaryNumber:
    result_bits = []
    carry = 0
    res_nibbles = []
    nibbles_a = [a.bits[i:i + 4] for i in range(0, BIT_COUNT, 4)]
    nibbles_b = [b.bits[i:i + 4] for i in range(0, BIT_COUNT, 4)]

    for i in range((BIT_COUNT // 4) - 1, -1, -1):
        val_a = _gray_to_digit(nibbles_a[i])
        val_b = _gray_to_digit(nibbles_b[i])
        digit_sum = val_a + val_b + carry
        if digit_sum > 9:
            digit_sum -= 10
            carry = 1
        else:
            carry = 0

        res_nibbles.append(_digit_to_gray(digit_sum))

    for nibble in reversed(res_nibbles):
        result_bits.extend(nibble)
    return BinaryNumber(result_bits)
