from src.models import BinaryNumber
from src.config import BIT_COUNT, ZERO_BIT, ONE_BIT
from src.arithmetic.addition import add_binary


def _shift_left(number: BinaryNumber) -> BinaryNumber:
    bits = number.bits
    shifted_bits = [ZERO_BIT] + bits[2:] + [ZERO_BIT]
    return BinaryNumber(shifted_bits)


def multiply_binary(a: BinaryNumber, b: BinaryNumber) -> BinaryNumber:
    result = BinaryNumber([ZERO_BIT] * BIT_COUNT)
    current_a = BinaryNumber([ZERO_BIT] + a.bits[1:])

    for i in range(BIT_COUNT - 1, 0, -1):
        if b[i] == ONE_BIT:
            result = add_binary(result, current_a)
        current_a = _shift_left(current_a)

    final_bits = result.bits
    final_bits[0] = a[0] ^ b[0]

    if not any(final_bits[1:]):
        final_bits[0] = ZERO_BIT

    return BinaryNumber(final_bits)