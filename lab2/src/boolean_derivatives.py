from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .minimization import minimize_sdnf_calculation
from .truth_table import TruthTable, TruthTableRow, build_truth_table

MAX_DERIVATIVE_ORDER = 4


@dataclass(frozen=True)
class BooleanDerivative:
    variables: tuple[str, ...]
    derivative_variables: tuple[str, ...]
    values: tuple[int, ...]
    vector: str
    index: int
    expression: str


def build_partial_derivative(table: TruthTable, variable: str) -> BooleanDerivative:
    return build_mixed_derivative(table, (variable,))


def build_mixed_derivative(
    table: TruthTable,
    derivative_variables: tuple[str, ...],
) -> BooleanDerivative:
    _validate_derivative_variables(table.variables, derivative_variables)

    values = [1 if row.result else 0 for row in table.rows]
    mask = _variables_mask(table.variables, derivative_variables)
    derivative_values = tuple(_derivative_at(values, index, mask) for index in range(len(values)))
    vector = "".join(str(value) for value in derivative_values)
    derivative_index = int(vector, 2)
    derivative_table = _build_derivative_table(table, derivative_values)
    derivative_expression = minimize_sdnf_calculation(derivative_table).minimized_expression
    return BooleanDerivative(
        variables=table.variables,
        derivative_variables=derivative_variables,
        values=derivative_values,
        vector=vector,
        index=derivative_index,
        expression=derivative_expression,
    )


def build_all_derivatives(
    table: TruthTable,
    max_order: int = MAX_DERIVATIVE_ORDER,
) -> tuple[BooleanDerivative, ...]:
    order_limit = min(max_order, len(table.variables), MAX_DERIVATIVE_ORDER)
    derivatives: list[BooleanDerivative] = []
    for order in range(1, order_limit + 1):
        for variable_group in combinations(table.variables, order):
            derivatives.append(build_mixed_derivative(table, variable_group))
    return tuple(derivatives)


def build_all_derivatives_from_expression(
    expression: str,
    max_order: int = MAX_DERIVATIVE_ORDER,
) -> tuple[BooleanDerivative, ...]:
    table = build_truth_table(expression)
    return build_all_derivatives(table, max_order=max_order)


def _validate_derivative_variables(
    variables: tuple[str, ...],
    derivative_variables: tuple[str, ...],
) -> None:
    if not derivative_variables:
        raise ValueError("Derivative requires at least one variable")
    if len(derivative_variables) > MAX_DERIVATIVE_ORDER:
        raise ValueError(
            f"Derivative order cannot exceed {MAX_DERIVATIVE_ORDER}"
        )

    seen = set()
    for variable in derivative_variables:
        if variable not in variables:
            raise ValueError(f"Unknown derivative variable '{variable}'")
        if variable in seen:
            raise ValueError(f"Duplicate derivative variable '{variable}'")
        seen.add(variable)


def _variables_mask(
    variables: tuple[str, ...],
    derivative_variables: tuple[str, ...],
) -> int:
    mask = 0
    variable_count = len(variables)
    for variable in derivative_variables:
        position = variables.index(variable)
        bit_position = variable_count - 1 - position
        mask |= 1 << bit_position
    return mask


def _derivative_at(values: list[int], index: int, mask: int) -> int:
    total = 0
    submask = mask
    while True:
        total ^= values[index ^ submask]
        if submask == 0:
            break
        submask = (submask - 1) & mask
    return total


def _build_derivative_table(
    source_table: TruthTable,
    derivative_values: tuple[int, ...],
) -> TruthTable:
    rows = tuple(
        TruthTableRow(values=row.values, result=bool(derivative_values[index]))
        for index, row in enumerate(source_table.rows)
    )
    return TruthTable(variables=source_table.variables, rows=rows)
