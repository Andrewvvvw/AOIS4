from __future__ import annotations

from dataclasses import dataclass

from .truth_table import TruthTable, build_truth_table
from .zhegalkin import build_zhegalkin_polynomial


@dataclass(frozen=True)
class PostClasses:
    preserves_zero: bool
    preserves_one: bool
    self_dual: bool
    monotonic: bool
    linear: bool


def analyze_post_classes(table: TruthTable) -> PostClasses:
    values = [1 if row.result else 0 for row in table.rows]
    polynomial = build_zhegalkin_polynomial(table)
    return PostClasses(
        preserves_zero=_preserves_zero(values),
        preserves_one=_preserves_one(values),
        self_dual=_is_self_dual(values),
        monotonic=_is_monotonic(values),
        linear=polynomial.max_degree <= 1,
    )


def analyze_post_classes_from_expression(expression: str) -> PostClasses:
    table = build_truth_table(expression)
    return analyze_post_classes(table)


def _preserves_zero(values: list[int]) -> bool:
    return values[0] == 0


def _preserves_one(values: list[int]) -> bool:
    return values[-1] == 1


def _is_self_dual(values: list[int]) -> bool:
    max_mask = len(values) - 1
    for index, value in enumerate(values):
        opposite_index = max_mask ^ index
        if value == values[opposite_index]:
            return False
    return True


def _is_monotonic(values: list[int]) -> bool:
    value_count = len(values)
    for lower in range(value_count):
        for upper in range(value_count):
            if _is_subset(lower, upper) and values[lower] > values[upper]:
                return False
    return True


def _is_subset(lower: int, upper: int) -> bool:
    return (lower & ~upper) == 0
