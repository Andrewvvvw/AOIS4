from __future__ import annotations

from dataclasses import dataclass

from .minimization import (
    Implicant,
    MinimizationResult,
    format_minimization_report,
    minimize_sdnf_calculation,
    minimize_sknf_calculation,
)
from .truth_table import TruthTable, build_truth_table


@dataclass(frozen=True)
class CoverageTable:
    term_indexes: tuple[int, ...]
    implicants: tuple[Implicant, ...]
    matrix: tuple[tuple[bool, ...], ...]

    @property
    def minterms(self) -> tuple[int, ...]:
        """Backward-compatible alias for existing SDNF-oriented callers."""
        return self.term_indexes


@dataclass(frozen=True)
class TabularMinimizationResult:
    base_result: MinimizationResult
    coverage_table: CoverageTable
    essential_implicants: tuple[Implicant, ...]


def minimize_sdnf_tabular(table: TruthTable) -> TabularMinimizationResult:
    base_result = minimize_sdnf_calculation(table)
    coverage_table = _build_coverage_table(
        base_result.prime_implicants,
        base_result.minterms,
        len(base_result.variables),
    )
    essential_implicants = _find_essential_implicants(coverage_table)
    return TabularMinimizationResult(
        base_result=base_result,
        coverage_table=coverage_table,
        essential_implicants=essential_implicants,
    )


def minimize_sknf_tabular(table: TruthTable) -> TabularMinimizationResult:
    base_result = minimize_sknf_calculation(table)
    coverage_table = _build_coverage_table(
        base_result.prime_implicants,
        base_result.term_indexes,
        len(base_result.variables),
    )
    essential_implicants = _find_essential_implicants(coverage_table)
    return TabularMinimizationResult(
        base_result=base_result,
        coverage_table=coverage_table,
        essential_implicants=essential_implicants,
    )


def minimize_sdnf_tabular_from_expression(expression: str) -> TabularMinimizationResult:
    table = build_truth_table(expression)
    return minimize_sdnf_tabular(table)


def minimize_sknf_tabular_from_expression(expression: str) -> TabularMinimizationResult:
    table = build_truth_table(expression)
    return minimize_sknf_tabular(table)


def format_tabular_minimization_report(result: TabularMinimizationResult) -> str:
    lines = ["Calculation-tabular method"]
    lines.append(format_minimization_report(result.base_result))

    lines.append("Coverage table")
    if not result.base_result.term_indexes:
        if result.base_result.form == "SDNF":
            lines.append("  no minterms")
            lines.append("Minimized SDNF: 0")
        else:
            lines.append("  no maxterms")
            lines.append("Minimized SKNF: 1")
        return "\n".join(lines)

    axis_label = "minterm" if result.base_result.form == "SDNF" else "maxterm"
    header = (
        f"implicant/{axis_label} | "
        + " | ".join(str(value) for value in result.coverage_table.term_indexes)
    )
    lines.append(header)
    lines.append("-" * len(header))

    for implicant, row in zip(result.coverage_table.implicants, result.coverage_table.matrix):
        term = _implicant_to_term(
            implicant.pattern,
            result.base_result.variables,
            result.base_result.form,
        )
        marks = ["X" if cell else " " for cell in row]
        lines.append(f"{term:>16} | " + " | ".join(marks))

    essential = _implicants_to_expression(
        result.essential_implicants,
        result.base_result.variables,
        result.base_result.form,
    )
    lines.append(f"Essential implicants: {essential}")
    lines.append(
        f"Minimized {result.base_result.form}: {result.base_result.minimized_expression}"
    )
    return "\n".join(lines)


def _build_coverage_table(
    implicants: tuple[Implicant, ...],
    term_indexes: tuple[int, ...],
    variable_count: int,
) -> CoverageTable:
    matrix = []
    for implicant in implicants:
        row = tuple(
            _covers_minterm(implicant.pattern, term_index, variable_count)
            for term_index in term_indexes
        )
        matrix.append(row)
    return CoverageTable(
        term_indexes=term_indexes,
        implicants=implicants,
        matrix=tuple(matrix),
    )


def _find_essential_implicants(table: CoverageTable) -> tuple[Implicant, ...]:
    if not table.term_indexes:
        return tuple()

    essential_map: dict[tuple[int | None, ...], Implicant] = {}
    for column_index in range(len(table.term_indexes)):
        covering_rows = [
            row_index
            for row_index, row in enumerate(table.matrix)
            if row[column_index]
        ]
        if len(covering_rows) == 1:
            implicant = table.implicants[covering_rows[0]]
            essential_map[implicant.pattern] = implicant
    return tuple(essential_map.values())


def _covers_minterm(
    pattern: tuple[int | None, ...],
    minterm: int,
    variable_count: int,
) -> bool:
    for position, bit in enumerate(pattern):
        if bit is None:
            continue
        bit_position = variable_count - 1 - position
        current = (minterm >> bit_position) & 1
        if current != bit:
            return False
    return True


def _implicants_to_expression(
    implicants: tuple[Implicant, ...],
    variables: tuple[str, ...],
    form: str,
) -> str:
    if not implicants:
        return "<none>"
    terms = [_implicant_to_term(item.pattern, variables, form) for item in implicants]
    return " | ".join(terms) if form == "SDNF" else " & ".join(terms)


def _implicant_to_term(
    pattern: tuple[int | None, ...],
    variables: tuple[str, ...],
    form: str,
) -> str:
    literals = []
    for variable, bit in zip(variables, pattern):
        if bit is None:
            continue
        if form == "SDNF":
            literals.append(variable if bit == 1 else f"!{variable}")
        else:
            literals.append(f"!{variable}" if bit == 1 else variable)

    if form == "SDNF":
        if not literals:
            return "1"
        if len(literals) == 1:
            return literals[0]
        return f"({' & '.join(literals)})"

    if not literals:
        return "0"
    if len(literals) == 1:
        return literals[0]
    return f"({' | '.join(literals)})"
