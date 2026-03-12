from typing import List, Tuple
from src.models import BinaryNumber
from src.config import (
    BIT_COUNT,
    ZERO_BIT,
    ONE_BIT,
    MANTISSA_SIZE,
    BASE_BIAS,
    EXPONENT_BITS,
    EXPONENT_START,
    MANTISSA_START,
    FRACTION_LIMIT
)

def _get_fraction_bits(fraction: float, limit: int = FRACTION_LIMIT) -> List[int]:
    bits = []
    current = fraction
    for _ in range(limit):
        if current == 0.0:
            break
        current *= 2
        bit = int(current)
        bits.append(bit)
        current -= bit
    return bits


def _get_integer_bits(value: int) -> List[int]:
    if value == 0:
        return []
    bits = []
    while value > 0:
        bits.append(value % 2)
        value //= 2
    return bits[::-1]


def _normalize(int_bits: List[int], frac_bits: List[int]) -> Tuple[int, List[int]]:
    if int_bits:
        exponent = len(int_bits) - 1
        mantissa = int_bits[1:] + frac_bits
    else:
        try:
            first_one = frac_bits.index(ONE_BIT)
            exponent = -(first_one + 1)
            mantissa = frac_bits[first_one + 1:]
        except ValueError:
            return 0, []

    mantissa = mantissa[:MANTISSA_SIZE]
    return exponent, mantissa + [ZERO_BIT] * (MANTISSA_SIZE - len(mantissa))


def float_to_ieee754(value: float) -> BinaryNumber:
    if value == 0.0:
        return BinaryNumber([ZERO_BIT] * BIT_COUNT)

    sign = ONE_BIT if value < 0 else ZERO_BIT
    abs_value = abs(value)

    int_bits = _get_integer_bits(int(abs_value))
    frac_bits = _get_fraction_bits(abs_value - int(abs_value))

    exponent_val, mantissa = _normalize(int_bits, frac_bits)

    biased_exponent = exponent_val + BASE_BIAS
    exp_bits = _get_integer_bits(biased_exponent)
    exp_bits = [ZERO_BIT] * (EXPONENT_BITS - len(exp_bits)) + exp_bits

    return BinaryNumber([sign] + exp_bits + mantissa)


def ieee754_to_float(binary: BinaryNumber) -> float:
    sign = binary[0]
    exp_bits = binary.bits[EXPONENT_START:MANTISSA_START]
    mantissa_bits = binary.bits[MANTISSA_START:]

    exp_val = sum(bit * (2 ** i) for i, bit in enumerate(reversed(exp_bits)))

    if exp_val == 0 and not any(mantissa_bits):
        return 0.0

    real_exp = exp_val - BASE_BIAS
    mantissa_val = 1.0
    for i, bit in enumerate(mantissa_bits):
        mantissa_val += bit * (2 ** -(i + 1))

    result = mantissa_val * (2 ** real_exp)
    return -result if sign == 1 else result