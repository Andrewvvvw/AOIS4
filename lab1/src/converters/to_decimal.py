from src.models import BinaryNumber
from src.config import BIT_COUNT, ONE_BIT, INTEGER_BITS


def additional_to_decimal(binary: BinaryNumber) -> int:
    result = 0
    for i in range(1, BIT_COUNT):
        result += binary[i] * (2 ** (BIT_COUNT - 1 - i))
    if binary[0] == ONE_BIT:
        result -= 2 ** (BIT_COUNT - 1)
    return result


def direct_to_decimal(binary: BinaryNumber) -> int:
    magnitude = 0
    for i in range(1, BIT_COUNT):
        magnitude += binary[i] * (2 ** (BIT_COUNT - 1 - i))
    return -magnitude if binary[0] == ONE_BIT else magnitude


def fixed_point_to_decimal(binary: BinaryNumber) -> float:
    int_part = 0
    for i in range(1, INTEGER_BITS + 1):
        power = INTEGER_BITS - i
        int_part += binary[i] * (2 ** power)

    frac_part = 0.0
    for i in range(INTEGER_BITS + 1, BIT_COUNT):
        power = -(i - INTEGER_BITS)
        frac_part += binary[i] * (2 ** power)

    total = float(int_part) + frac_part
    return -total if binary[0] == ONE_BIT else total
