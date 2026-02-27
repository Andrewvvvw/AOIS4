from typing import List
from src.models import BinaryNumber
from src.config import ZERO_BIT, ONE_BIT
from src.ieee754.utils import unpack_ieee754, pack_ieee754


def _align_mantissas(m1: List[int], m2: List[int], diff: int) -> List[int]:
    if diff == 0:
        return list(m2)

    if diff >= len(m2):
        return [ZERO_BIT] * len(m2)
    return [ZERO_BIT] * diff + m2[:-diff]


def _add_mantissas(m1: List[int], m2: List[int]) -> List[int]:
    result = []
    carry = 0
    for i in range(len(m1) - 1, -1, -1):
        total = m1[i] + m2[i] + carry
        result.append(total % 2)
        carry = total // 2

    if carry:
        result.append(carry)
    return result[::-1]


def _sub_mantissas(m1: List[int], m2: List[int]) -> List[int]:
    result = []
    borrow = 0
    for i in range(len(m1) - 1, -1, -1):
        diff = m1[i] - m2[i] - borrow
        if diff < 0:
            diff += 2
            borrow = 1
        else:
            borrow = 0
        result.append(diff)
    return result[::-1]


def add_ieee754(a: BinaryNumber, b: BinaryNumber) -> BinaryNumber:
    s1, e1, m1 = unpack_ieee754(a)
    s2, e2, m2 = unpack_ieee754(b)

    if e2 > e1 or (e1 == e2 and _bits_to_int(m2) > _bits_to_int(m1)):
        s1, s2, e1, e2, m1, m2 = s2, s1, e2, e1, m2, m1

    exp_diff = e1 - e2
    m2_aligned = _align_mantissas(m1, m2, exp_diff)

    if s1 == s2:
        m_res = _add_mantissas(m1, m2_aligned)
        s_res = s1
        if len(m_res) > len(m1):
            e1 += 1
    else:
        m_res = _sub_mantissas(m1, m2_aligned)
        s_res = s1
    return pack_ieee754(s_res, e1, m_res)


def subtract_ieee754(a: BinaryNumber, b: BinaryNumber) -> BinaryNumber:
    neg_b_bits = list(b.bits)
    neg_b_bits[0] = ONE_BIT if b[0] == ZERO_BIT else ZERO_BIT
    return add_ieee754(a, BinaryNumber(neg_b_bits))


def _bits_to_int(bits: List[int]) -> int:
    result = 0
    for i, bit in enumerate(reversed(bits)):
        result += bit * (2 ** i)
    return result
