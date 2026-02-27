from src.models import BinaryNumber
from src.config import BIT_COUNT, ZERO_BIT, ONE_BIT, FRACTION_PRECISION, INTEGER_BITS
from src.arithmetic.subtraction import subtract_binary


def _shift_left_insert(num: BinaryNumber, bit: int) -> BinaryNumber:
    new_bits = [ZERO_BIT] + num.bits[2:] + [bit]
    return BinaryNumber(new_bits)


def _integer_division_logic(dividend: BinaryNumber, divisor: BinaryNumber) -> tuple:
    remainder = BinaryNumber([ZERO_BIT] * BIT_COUNT)
    quotient_bits = [ZERO_BIT] * INTEGER_BITS

    for i in range(1, BIT_COUNT):
        remainder = _shift_left_insert(remainder, dividend[i])
        diff = subtract_binary(remainder, divisor)

        if diff[0] == ZERO_BIT:
            remainder = diff
            bit_pos = i - (BIT_COUNT - INTEGER_BITS)
            if bit_pos >= 0:
                quotient_bits[bit_pos] = ONE_BIT

    return quotient_bits, remainder


def _fractional_division_logic(remainder: BinaryNumber, divisor: BinaryNumber) -> list:
    frac_bits = []
    current_rem = remainder

    for _ in range(FRACTION_PRECISION):
        current_rem = _shift_left_insert(current_rem, ZERO_BIT)
        diff = subtract_binary(current_rem, divisor)

        if diff[0] == ZERO_BIT:
            current_rem = diff
            frac_bits.append(ONE_BIT)
        else:
            frac_bits.append(ZERO_BIT)

    return frac_bits


def divide_binary(a: BinaryNumber, b: BinaryNumber) -> BinaryNumber:
    if not any(b.bits[1:]):
        raise ZeroDivisionError("Division by zero")

    abs_a = BinaryNumber([ZERO_BIT] + a.bits[1:])
    abs_b = BinaryNumber([ZERO_BIT] + b.bits[1:])

    int_bits, remainder = _integer_division_logic(abs_a, abs_b)
    frac_bits = _fractional_division_logic(remainder, abs_b)

    sign = a[0] ^ b[0]
    result_bits = [sign] + int_bits + frac_bits

    return BinaryNumber(result_bits)