from src.models import BinaryNumber
from src.config import BIT_COUNT, ZERO_BIT


def add_binary(a: BinaryNumber, b: BinaryNumber) -> BinaryNumber:
    result = [ZERO_BIT] * BIT_COUNT
    carry = ZERO_BIT

    for i in range(BIT_COUNT - 1, -1, -1):
        sum_val = a[i] + b[i] + carry
        result[i] = sum_val % 2
        carry = sum_val // 2

    return BinaryNumber(result)