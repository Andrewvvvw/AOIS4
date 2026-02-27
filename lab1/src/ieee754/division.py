from typing import List
from src.models import BinaryNumber
from src.config import ZERO_BIT
from src.ieee754.utils import unpack_ieee754, pack_ieee754


def _bits_to_int(bits: List[int]) -> int:
    return sum(bit * (2 ** i) for i, bit in enumerate(reversed(bits)))


def _int_to_bits(value: int, length: int) -> List[int]:
    return [(value >> i) & 1 for i in range(length - 1, -1, -1)]


def divide_ieee754(a: BinaryNumber, b: BinaryNumber) -> BinaryNumber:
    s1, e1, m1 = unpack_ieee754(a)
    s2, e2, m2 = unpack_ieee754(b)

    if not any(m2):
        raise ZeroDivisionError("IEEE-754 Division by zero")
    if not any(m1):
        return BinaryNumber([s1 ^ s2] + [ZERO_BIT] * 31)

    s_res = s1 ^ s2
    e_res = e1 - e2

    # Для получения 24 бит точности дробной части, сдвигаем делимое на 24 бита влево
    val1 = _bits_to_int(m1) << 24
    val2 = _bits_to_int(m2)

    quotient = val1 // val2
    m_res = _int_to_bits(quotient, 25)

    return pack_ieee754(s_res, e_res, m_res)