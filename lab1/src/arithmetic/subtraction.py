from src.models import BinaryNumber
from src.arithmetic.addition import add_binary
from src.converters.to_binary import invert_bits, increment_bits


def negate(number: BinaryNumber) -> BinaryNumber:
    inverted = invert_bits(number.bits)
    return BinaryNumber(increment_bits(inverted))


def subtract_binary(minuend: BinaryNumber, subtrahend: BinaryNumber) -> BinaryNumber:
    negative_subtrahend = negate(subtrahend)
    return add_binary(minuend, negative_subtrahend)