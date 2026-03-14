from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, Tuple

from .logic_parser import ParsedExpression, parse_logical_expression


@dataclass(frozen=True)
class TruthTableRow:
    values: Tuple[bool, ...]
    result: bool

    def as_mapping(self, variables: Tuple[str, ...]) -> Dict[str, bool]:
        return dict(zip(variables, self.values))


@dataclass(frozen=True)
class TruthTable:
    variables: Tuple[str, ...]
    rows: Tuple[TruthTableRow, ...]


def build_truth_table(expression: str | ParsedExpression) -> TruthTable:
    parsed_expression = _as_parsed_expression(expression)
    variables = parsed_expression.variables
    combinations = _value_combinations(len(variables))

    rows = tuple(_build_row(parsed_expression, variables, values) for values in combinations)
    return TruthTable(variables=variables, rows=rows)


def _as_parsed_expression(expression: str | ParsedExpression) -> ParsedExpression:
    if isinstance(expression, ParsedExpression):
        return expression
    return parse_logical_expression(expression)


def _value_combinations(variable_count: int) -> Iterable[Tuple[bool, ...]]:
    if variable_count == 0:
        return [tuple()]
    return product((False, True), repeat=variable_count)


def _build_row(
    parsed_expression: ParsedExpression,
    variables: Tuple[str, ...],
    values: Tuple[bool, ...],
) -> TruthTableRow:
    assignment = dict(zip(variables, values))
    result = parsed_expression.evaluate(assignment)
    return TruthTableRow(values=values, result=result)
