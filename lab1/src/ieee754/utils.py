from typing import List, Tuple
from src.models import BinaryNumber
from src.config import BIT_COUNT, EXPONENT_START, MANTISSA_SIZE, MANTISSA_START, ZERO_BIT, ONE_BIT, EXPONENT_BITS, BASE_BIAS


def _bits_to_int(bits: List[int]) -> int:
    result = 0
    for i, bit in enumerate(reversed(bits)):
        result += bit * (2 ** i)
    return result


def _int_to_bits(value: int, length: int) -> List[int]:
    bits = []
    temp = value
    for _ in range(length):
        bits.append(temp % 2)
        temp //= 2
    return bits[::-1]


def unpack_ieee754(binary: BinaryNumber) -> Tuple[int, int, List[int]]:
    sign = binary[0]
    exp_bits = binary.bits[EXPONENT_START:MANTISSA_START]
    mantissa_bits = binary.bits[MANTISSA_START:]

    exp_val = _bits_to_int(exp_bits)

    if exp_val == 0 and not any(mantissa_bits):
        return sign, 0, [ZERO_BIT] * (BIT_COUNT - EXPONENT_BITS)

    real_exp = exp_val - BASE_BIAS
    mantissa = [ONE_BIT] + mantissa_bits

    return sign, real_exp, mantissa


def pack_ieee754(sign: int, exp_val: int, mantissa: List[int]) -> BinaryNumber:
    if not any(mantissa):
        return BinaryNumber([sign] + [ZERO_BIT] * (BIT_COUNT - 1))

    first_one_idx = mantissa.index(ONE_BIT)
    shift = first_one_idx

    normalized_mantissa = mantissa[shift + 1:]
    normalized_mantissa = normalized_mantissa[:MANTISSA_SIZE]

    padding = MANTISSA_SIZE - len(normalized_mantissa)
    normalized_mantissa += [ZERO_BIT] * padding

    final_exp = exp_val - shift + BASE_BIAS

    if final_exp <= 0 or final_exp >= 2 ** EXPONENT_BITS - 1:
        return BinaryNumber([sign] + [ZERO_BIT] * (BIT_COUNT - 1))

    exp_bits = _int_to_bits(final_exp, EXPONENT_BITS)

    return BinaryNumber([sign] + exp_bits + normalized_mantissa)
