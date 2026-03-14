from __future__ import annotations

from dataclasses import dataclass

from .truth_table import TruthTable, build_truth_table


@dataclass(frozen=True)
class DummyVariableAnalysis:
    dummy_variables: tuple[str, ...]
    essential_variables: tuple[str, ...]


def find_dummy_variables(table: TruthTable) -> DummyVariableAnalysis:
    variable_count = len(table.variables)
    if variable_count == 0:
        return DummyVariableAnalysis(dummy_variables=tuple(), essential_variables=tuple())

    values = [1 if row.result else 0 for row in table.rows]
    dummy_variables = tuple(
        variable
        for position, variable in enumerate(table.variables)
        if _is_dummy_variable(values, variable_count, position)
    )
    essential_variables = tuple(
        variable for variable in table.variables if variable not in dummy_variables
    )
    return DummyVariableAnalysis(
        dummy_variables=dummy_variables,
        essential_variables=essential_variables,
    )


def find_dummy_variables_from_expression(expression: str) -> DummyVariableAnalysis:
    table = build_truth_table(expression)
    return find_dummy_variables(table)


def _is_dummy_variable(values: list[int], variable_count: int, position: int) -> bool:
    toggle_mask = 1 << (variable_count - 1 - position)

    for index, value in enumerate(values):
        paired_index = index ^ toggle_mask
        if value != values[paired_index]:
            return False
    return True
