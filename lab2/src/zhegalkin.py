from __future__ import annotations

from dataclasses import dataclass

from .truth_table import TruthTable, build_truth_table

XOR_OPERATOR = " ^ "
AND_OPERATOR = "*"
CONST_ONE = "1"
CONST_ZERO = "0"


@dataclass(frozen=True)
class ZhegalkinPolynomial:
    variables: tuple[str, ...]
    coefficients: tuple[int, ...]
    expression: str
    max_degree: int


def build_zhegalkin_polynomial(table: TruthTable) -> ZhegalkinPolynomial:
    values = [1 if row.result else 0 for row in table.rows]
    coefficients = _mobius_transform(values)
    expression = _format_expression(table.variables, coefficients)
    max_degree = _max_degree(coefficients)
    return ZhegalkinPolynomial(
        variables=table.variables,
        coefficients=tuple(coefficients),
        expression=expression,
        max_degree=max_degree,
    )


def build_zhegalkin_polynomial_from_expression(expression: str) -> ZhegalkinPolynomial:
    table = build_truth_table(expression)
    return build_zhegalkin_polynomial(table)


def _mobius_transform(values: list[int]) -> list[int]:
    transformed = values.copy()
    if not transformed:
        return transformed

    variable_count = (len(transformed) - 1).bit_length()
    for bit in range(variable_count):
        bit_mask = 1 << bit
        for index in range(len(transformed)):
            if index & bit_mask:
                transformed[index] ^= transformed[index ^ bit_mask]
    return transformed


def _format_expression(variables: tuple[str, ...], coefficients: list[int]) -> str:
    term_indices = [
        index
        for index, coefficient in enumerate(coefficients)
        if coefficient == 1
    ]
    term_indices.sort(key=lambda index: _term_sort_key(variables, index))
    terms = [_format_term(variables, index) for index in term_indices]
    if not terms:
        return CONST_ZERO
    return XOR_OPERATOR.join(terms)


def _format_term(variables: tuple[str, ...], index: int) -> str:
    if index == 0:
        return CONST_ONE

    literals = []
    for variable_position, variable in enumerate(variables):
        bit_position = len(variables) - 1 - variable_position
        if index & (1 << bit_position):
            literals.append(variable)
    return AND_OPERATOR.join(literals)


def _term_sort_key(variables: tuple[str, ...], index: int) -> tuple[int, tuple[int, ...]]:
    degree = index.bit_count()
    positions = tuple(
        variable_position
        for variable_position in range(len(variables))
        if index & (1 << (len(variables) - 1 - variable_position))
    )
    return degree, positions


def _max_degree(coefficients: list[int]) -> int:
    degree = 0
    for index, coefficient in enumerate(coefficients):
        if coefficient == 1:
            degree = max(degree, index.bit_count())
    return degree
