from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, Optional

from .truth_table import TruthTable, build_truth_table

BIT_ZERO = 0
BIT_ONE = 1


@dataclass(frozen=True)
class Implicant:
    pattern: tuple[Optional[int], ...]
    covered_minterms: tuple[int, ...]


@dataclass(frozen=True)
class GluingRecord:
    left: Implicant
    right: Implicant
    result: Implicant


@dataclass(frozen=True)
class GluingStage:
    input_implicants: tuple[Implicant, ...]
    gluing_records: tuple[GluingRecord, ...]
    result_implicants: tuple[Implicant, ...]


@dataclass(frozen=True)
class MinimizationResult:
    form: str
    variables: tuple[str, ...]
    term_indexes: tuple[int, ...]
    stages: tuple[GluingStage, ...]
    prime_implicants: tuple[Implicant, ...]
    selected_implicants: tuple[Implicant, ...]
    minimized_expression: str

    @property
    def minterms(self) -> tuple[int, ...]:
        """Backward-compatible alias for existing SDNF-oriented callers."""
        return self.term_indexes


def minimize_sdnf_calculation(table: TruthTable) -> MinimizationResult:
    return _minimize_calculation(table, form="SDNF")


def minimize_sknf_calculation(table: TruthTable) -> MinimizationResult:
    return _minimize_calculation(table, form="SKNF")


def minimize_sdnf_calculation_from_expression(expression: str) -> MinimizationResult:
    table = build_truth_table(expression)
    return minimize_sdnf_calculation(table)


def minimize_sknf_calculation_from_expression(expression: str) -> MinimizationResult:
    table = build_truth_table(expression)
    return minimize_sknf_calculation(table)


def format_minimization_report(result: MinimizationResult) -> str:
    lines = ["Calculation method"]
    if not result.term_indexes:
        empty_value = "0" if result.form == "SDNF" else "1"
        lines.append(f"{result.form} is empty -> minimized: {empty_value}")
        return "\n".join(lines)

    label = "Minterms" if result.form == "SDNF" else "Maxterms"
    join_symbol = " + " if result.form == "SDNF" else " * "
    lines.append(f"{label}: {', '.join(str(value) for value in result.term_indexes)}")
    for stage_number, stage in enumerate(result.stages, start=1):
        lines.append(f"Gluing stage {stage_number}")
        if not stage.gluing_records:
            lines.append("  no pairs to glue")
        for record in stage.gluing_records:
            left = _implicant_to_term(record.left.pattern, result.variables, result.form)
            right = _implicant_to_term(record.right.pattern, result.variables, result.form)
            glued = _implicant_to_term(record.result.pattern, result.variables, result.form)
            lines.append(f"  {left}{join_symbol}{right} -> {glued}")
        stage_result = _implicants_to_expression(stage.result_implicants, result.variables, result.form)
        lines.append(f"  result: {stage_result}")

    lines.append(
        "Prime implicants: "
        + _implicants_to_expression(result.prime_implicants, result.variables, result.form)
    )
    lines.append(f"Minimized {result.form}: {result.minimized_expression}")
    return "\n".join(lines)


def _minimize_calculation(table: TruthTable, form: str) -> MinimizationResult:
    variables = table.variables
    if form == "SDNF":
        term_indexes = tuple(index for index, row in enumerate(table.rows) if row.result)
    else:
        term_indexes = tuple(index for index, row in enumerate(table.rows) if not row.result)

    if not term_indexes:
        return MinimizationResult(
            form=form,
            variables=variables,
            term_indexes=term_indexes,
            stages=tuple(),
            prime_implicants=tuple(),
            selected_implicants=tuple(),
            minimized_expression="0" if form == "SDNF" else "1",
        )

    initial_implicants = tuple(
        _implicant_from_minterm(index, len(variables)) for index in term_indexes
    )
    stages, prime_implicants = _build_gluing_stages(initial_implicants)
    selected_implicants = _select_cover(prime_implicants, set(term_indexes), len(variables))
    expression = _implicants_to_expression(selected_implicants, variables, form)

    return MinimizationResult(
        form=form,
        variables=variables,
        term_indexes=term_indexes,
        stages=stages,
        prime_implicants=prime_implicants,
        selected_implicants=selected_implicants,
        minimized_expression=expression,
    )


def _implicant_from_minterm(index: int, variable_count: int) -> Implicant:
    pattern = []
    for position in range(variable_count):
        bit_position = variable_count - 1 - position
        bit = (index >> bit_position) & 1
        pattern.append(bit)
    return Implicant(pattern=tuple(pattern), covered_minterms=(index,))


def _build_gluing_stages(
    initial_implicants: tuple[Implicant, ...],
) -> tuple[tuple[GluingStage, ...], tuple[Implicant, ...]]:
    stages: list[GluingStage] = []
    prime_map: Dict[tuple[Optional[int], ...], Implicant] = {}
    current = initial_implicants

    while current:
        gluing_records: list[GluingRecord] = []
        used_indices: set[int] = set()
        next_map: Dict[tuple[Optional[int], ...], Implicant] = {}

        for left_index, right_index in combinations(range(len(current)), 2):
            left = current[left_index]
            right = current[right_index]
            combined = _combine_implicants(left, right)
            if combined is None:
                continue
            gluing_records.append(GluingRecord(left=left, right=right, result=combined))
            used_indices.add(left_index)
            used_indices.add(right_index)
            _add_implicant(next_map, combined)

        for implicant_index, implicant in enumerate(current):
            if implicant_index not in used_indices:
                _add_implicant(prime_map, implicant)

        next_implicants = tuple(next_map.values())
        stages.append(
            GluingStage(
                input_implicants=current,
                gluing_records=tuple(gluing_records),
                result_implicants=next_implicants,
            )
        )

        if not next_implicants:
            break
        current = next_implicants

    return tuple(stages), tuple(prime_map.values())


def _combine_implicants(left: Implicant, right: Implicant) -> Optional[Implicant]:
    differences = 0
    combined_pattern: list[Optional[int]] = []

    for left_bit, right_bit in zip(left.pattern, right.pattern):
        if left_bit == right_bit:
            combined_pattern.append(left_bit)
            continue
        if left_bit is None or right_bit is None:
            return None
        differences += 1
        combined_pattern.append(None)
        if differences > 1:
            return None

    if differences != 1:
        return None

    covered = tuple(sorted(set(left.covered_minterms) | set(right.covered_minterms)))
    return Implicant(pattern=tuple(combined_pattern), covered_minterms=covered)


def _add_implicant(
    target_map: Dict[tuple[Optional[int], ...], Implicant],
    implicant: Implicant,
) -> None:
    existing = target_map.get(implicant.pattern)
    if existing is None:
        target_map[implicant.pattern] = implicant
        return

    merged_covered = tuple(sorted(set(existing.covered_minterms) | set(implicant.covered_minterms)))
    target_map[implicant.pattern] = Implicant(
        pattern=implicant.pattern,
        covered_minterms=merged_covered,
    )


def _select_cover(
    prime_implicants: tuple[Implicant, ...],
    minterms: set[int],
    variable_count: int,
) -> tuple[Implicant, ...]:
    coverage_map = {
        minterm: [
            implicant
            for implicant in prime_implicants
            if _covers_minterm(implicant.pattern, minterm, variable_count)
        ]
        for minterm in minterms
    }

    essential_patterns: dict[tuple[Optional[int], ...], Implicant] = {}
    covered_by_essential: set[int] = set()

    for minterm, covering in coverage_map.items():
        if len(covering) == 1:
            implicant = covering[0]
            essential_patterns[implicant.pattern] = implicant
            covered_by_essential.update(implicant.covered_minterms)

    remaining_minterms = minterms.difference(covered_by_essential)
    essential = tuple(essential_patterns.values())
    if not remaining_minterms:
        return _sort_implicants(essential)

    candidates = tuple(
        implicant
        for implicant in prime_implicants
        if implicant.pattern not in essential_patterns
    )

    best_extra = _best_cover_subset(candidates, remaining_minterms, variable_count)
    selected_map: dict[tuple[Optional[int], ...], Implicant] = {
        implicant.pattern: implicant for implicant in essential + best_extra
    }
    selected = tuple(selected_map.values())
    return _sort_implicants(selected)


def _best_cover_subset(
    candidates: tuple[Implicant, ...],
    target_minterms: set[int],
    variable_count: int,
) -> tuple[Implicant, ...]:
    coverage_cache = {
        implicant.pattern: {
            minterm
            for minterm in target_minterms
            if _covers_minterm(implicant.pattern, minterm, variable_count)
        }
        for implicant in candidates
    }

    best_solution: tuple[Implicant, ...] | None = None
    best_score: tuple[int, int] | None = None

    def search(remaining: set[int], chosen: tuple[Implicant, ...]) -> None:
        nonlocal best_solution, best_score

        if not remaining:
            score = (len(chosen), _total_literals(chosen))
            if best_score is None or score < best_score:
                best_score = score
                best_solution = chosen
            return

        if best_score is not None and len(chosen) >= best_score[0]:
            return

        pivot = min(
            remaining,
            key=lambda minterm: len(
                [
                    implicant
                    for implicant in candidates
                    if minterm in coverage_cache[implicant.pattern]
                ]
            ),
        )

        pivot_candidates = [
            implicant
            for implicant in candidates
            if minterm_in_set(pivot, coverage_cache[implicant.pattern])
        ]

        for implicant in pivot_candidates:
            covered = coverage_cache[implicant.pattern]
            search(remaining.difference(covered), chosen + (implicant,))

    search(set(target_minterms), tuple())

    if best_solution is None:
        return tuple()
    return _sort_implicants(best_solution)


def minterm_in_set(minterm: int, covered: set[int]) -> bool:
    return minterm in covered


def _covers_minterm(
    pattern: tuple[Optional[int], ...],
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


def _sort_implicants(implicants: Iterable[Implicant]) -> tuple[Implicant, ...]:
    return tuple(
        sorted(
            implicants,
            key=lambda item: (
                sum(1 for bit in item.pattern if bit is not None),
                tuple(2 if bit is None else bit for bit in item.pattern),
            ),
        )
    )


def _total_literals(implicants: tuple[Implicant, ...]) -> int:
    return sum(sum(1 for bit in implicant.pattern if bit is not None) for implicant in implicants)


def _implicants_to_expression(
    implicants: Iterable[Implicant],
    variables: tuple[str, ...],
    form: str,
) -> str:
    terms = [_implicant_to_term(implicant.pattern, variables, form) for implicant in implicants]
    if not terms:
        return "0" if form == "SDNF" else "1"
    if form == "SDNF":
        if all(term == "1" for term in terms):
            return "1"
        return " | ".join(terms)
    if all(term == "0" for term in terms):
        return "0"
    return " & ".join(terms)


def _implicant_to_term(
    pattern: tuple[Optional[int], ...],
    variables: tuple[str, ...],
    form: str,
) -> str:
    literals: list[str] = []
    for variable, bit in zip(variables, pattern):
        if bit is None:
            continue
        if form == "SDNF":
            literals.append(variable if bit == BIT_ONE else f"!{variable}")
        else:
            literals.append(f"!{variable}" if bit == BIT_ONE else variable)

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
