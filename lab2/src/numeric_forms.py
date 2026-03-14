from __future__ import annotations

from dataclasses import dataclass

from .truth_table import TruthTable, build_truth_table

SDNF_PREFIX = "V"
SKNF_PREFIX = "^"


@dataclass(frozen=True)
class NumericForms:
    sdnf_indices: tuple[int, ...]
    sknf_indices: tuple[int, ...]
    sdnf: str
    sknf: str


def build_numeric_forms(table: TruthTable) -> NumericForms:
    sdnf_indices = tuple(index for index, row in enumerate(table.rows) if row.result)
    sknf_indices = tuple(index for index, row in enumerate(table.rows) if not row.result)

    return NumericForms(
        sdnf_indices=sdnf_indices,
        sknf_indices=sknf_indices,
        sdnf=_format_numeric_form(SDNF_PREFIX, sdnf_indices),
        sknf=_format_numeric_form(SKNF_PREFIX, sknf_indices),
    )


def build_numeric_forms_from_expression(expression: str) -> NumericForms:
    table = build_truth_table(expression)
    return build_numeric_forms(table)


def _format_numeric_form(prefix: str, indices: tuple[int, ...]) -> str:
    if not indices:
        return f"{prefix}()"
    body = ",".join(str(index) for index in indices)
    return f"{prefix}({body})"
