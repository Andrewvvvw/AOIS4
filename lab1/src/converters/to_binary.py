from typing import List
from src.config import BIT_COUNT, ZERO_BIT, ONE_BIT
from src.models import BinaryNumber


def get_magnitude_bits(value: int) -> List[int]:
    abs_value = abs(value)
    bits = []
    while abs_value > 0:
        bits.append(abs_value % 2)
        abs_value //= 2
    if not bits:
        bits.append(ZERO_BIT)
    return bits


def pad_bits(bits: List[int], target_len: int) -> List[int]:
    padding_size = target_len - len(bits)
    if padding_size < 0:
        raise ValueError("Number exceeds bit capacity")
    return bits + [ZERO_BIT] * padding_size


def invert_bits(bits: List[int]) -> List[int]:
    return [ONE_BIT if b == ZERO_BIT else ZERO_BIT for b in bits]


def increment_bits(bits: List[int]) -> List[int]:
    result = list(bits)
    carry = ONE_BIT
    for i in range(BIT_COUNT - 1, -1, -1):
        if carry == ZERO_BIT:
            break
        sum_val = result[i] + carry
        result[i] = sum_val % 2
        carry = sum_val // 2
    return result


def to_direct(value: int) -> BinaryNumber:
    magnitude = get_magnitude_bits(value)
    padded = pad_bits(magnitude, BIT_COUNT - 1)
    sign = ONE_BIT if value < 0 else ZERO_BIT
    return BinaryNumber((padded + [sign])[::-1])


def to_reverse(value: int) -> BinaryNumber:
    if value >= 0:
        return to_direct(value)
    positive_direct = to_direct(abs(value))
    inverted = invert_bits(positive_direct.bits)
    return BinaryNumber(inverted)


def to_additional(value: int) -> BinaryNumber:
    if value >= 0:
        return to_direct(value)
    reverse = to_reverse(value)
    incremented = increment_bits(reverse.bits)
    return BinaryNumber(incremented)