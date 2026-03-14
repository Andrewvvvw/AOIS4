from __future__ import annotations

from dataclasses import dataclass

from .truth_table import TruthTable, build_truth_table

LITERAL_NEGATION = "!"
OP_AND = " & "
OP_OR = " | "
CONST_ZERO = "0"
CONST_ONE = "1"


@dataclass(frozen=True)
class CanonicalForms:
    sdnf: str
    sknf: str


def build_canonical_forms(table: TruthTable) -> CanonicalForms:
    if not table.variables:
        value = CONST_ONE if table.rows[0].result else CONST_ZERO
        return CanonicalForms(sdnf=value, sknf=value)

    sdnf = _build_sdnf(table)
    sknf = _build_sknf(table)
    return CanonicalForms(sdnf=sdnf, sknf=sknf)


def build_canonical_forms_from_expression(expression: str) -> CanonicalForms:
    table = build_truth_table(expression)
    return build_canonical_forms(table)


def _build_sdnf(table: TruthTable) -> str:
    terms = [
        _minterm(table.variables, row.values)
        for row in table.rows
        if row.result
    ]
    if not terms:
        return CONST_ZERO
    return OP_OR.join(terms)


def _build_sknf(table: TruthTable) -> str:
    terms = [
        _maxterm(table.variables, row.values)
        for row in table.rows
        if not row.result
    ]
    if not terms:
        return CONST_ONE
    return OP_AND.join(terms)


def _minterm(variables: tuple[str, ...], values: tuple[bool, ...]) -> str:
    literals = [
        variable if value else f"{LITERAL_NEGATION}{variable}"
        for variable, value in zip(variables, values)
    ]
    return _term_with_parentheses(literals, OP_AND)


def _maxterm(variables: tuple[str, ...], values: tuple[bool, ...]) -> str:
    literals = [
        variable if not value else f"{LITERAL_NEGATION}{variable}"
        for variable, value in zip(variables, values)
    ]
    return _term_with_parentheses(literals, OP_OR)


def _term_with_parentheses(literals: list[str], operator: str) -> str:
    if len(literals) == 1:
        return literals[0]
    return f"({operator.join(literals)})"
