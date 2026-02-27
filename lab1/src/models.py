from typing import List, Iterable
from src.config import BIT_COUNT, ALLOWED_BITS


class BinaryNumber:
    def __init__(self, bits: Iterable[int]):
        bit_list = list(bits)
        self._validate(bit_list)
        self._bits = tuple(bit_list)

    def _validate(self, bit_list: List[int]) -> None:
        if len(bit_list) != BIT_COUNT:
            raise ValueError(f"BinaryNumber must have exactly {BIT_COUNT} bits.")

        for bit in bit_list:
            if bit not in ALLOWED_BITS:
                raise ValueError(f"Invalid bit value detected: {bit}. Only 0 and 1 are allowed.")

    @property
    def bits(self) -> List[int]:
        return list(self._bits)

    def __getitem__(self, index: int) -> int:
        return self._bits[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryNumber):
            return False
        return self._bits == other._bits

    def __str__(self) -> str:
        return "".join(map(str, self._bits))

    def __repr__(self) -> str:
        return f"BinaryNumber({self.__str__()})"

    def __len__(self) -> int:
        return BIT_COUNT
