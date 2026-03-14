from __future__ import annotations

from dataclasses import dataclass

from .truth_table import TruthTable, build_truth_table


@dataclass(frozen=True)
class IndexForm:
    vector: str
    index: int


def build_index_form(table: TruthTable) -> IndexForm:
    vector = _build_vector(table)
    index = int(vector, 2)
    return IndexForm(vector=vector, index=index)


def build_index_form_from_expression(expression: str) -> IndexForm:
    table = build_truth_table(expression)
    return build_index_form(table)


def _build_vector(table: TruthTable) -> str:
    return "".join("1" if row.result else "0" for row in table.rows)
