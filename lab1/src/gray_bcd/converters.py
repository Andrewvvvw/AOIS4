from typing import List
from src.models import BinaryNumber
from src.config import BIT_COUNT


def _digit_to_gray(digit: int) -> List[int]:
    b = [(digit >> i) & 1 for i in range(3, -1, -1)]

    g = [b[0]]
    for i in range(1, 4):
        g.append(b[i - 1] ^ b[i])
    return g


def _gray_to_digit(g: List[int]) -> int:
    b = [g[0]]
    for i in range(1, 4):
        b.append(b[i - 1] ^ g[i])

    return sum(bit * (2 ** (3 - i)) for i, bit in enumerate(b))


def decimal_to_gray_bcd(val: int) -> BinaryNumber:
    max_digits = BIT_COUNT // 4
    if val < 0 or val >= 10 ** max_digits:
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
    for i in range(0, BIT_COUNT, 4):
        nibble = bn.bits[i:i + 4]
        digits.append(str(_gray_to_digit(nibble)))

    return int("".join(digits))
