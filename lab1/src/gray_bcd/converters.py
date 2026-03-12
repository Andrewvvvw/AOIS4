from typing import List
from src.models import BinaryNumber
from src.config import BIT_COUNT, BCD_DECAD_SIZE, MAX_DECAD_POWER, DECIMAL_BASE


def _digit_to_gray(digit: int) -> List[int]:
    b = [(digit >> i) & 1 for i in range(MAX_DECAD_POWER, -1, -1)]

    g = [b[0]]
    for i in range(1, BCD_DECAD_SIZE):
        g.append(b[i - 1] ^ b[i])
    return g


def _gray_to_digit(g: List[int]) -> int:
    b = [g[0]]
    for i in range(1, BCD_DECAD_SIZE):
        b.append(b[i - 1] ^ g[i])

    return sum(bit * (2 ** (MAX_DECAD_POWER - i)) for i, bit in enumerate(b))


def decimal_to_gray_bcd(val: int) -> BinaryNumber:
    max_digits = BIT_COUNT // BCD_DECAD_SIZE
    if val < 0 or val >= DECIMAL_BASE ** max_digits:
        raise ValueError(
            f"Number out of range (max 8 digits with no sign): {val}"
        )

    bits = []
    val_str = str(val).zfill(max_digits)

    for char in val_str:
        bits.extend(_digit_to_gray(int(char)))

    return BinaryNumber(bits)


def gray_bcd_to_decimal(bn: BinaryNumber) -> int:
    digits = []
    for i in range(0, BIT_COUNT, BCD_DECAD_SIZE):
        nibble = bn.bits[i:i + BCD_DECAD_SIZE]
        digits.append(str(_gray_to_digit(nibble)))

    return int("".join(digits))
