from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Optional

from .minimization import Implicant
from .truth_table import TruthTable, build_truth_table

MAX_KARNAUGH_VARIABLES = 4


@dataclass(frozen=True)
class KarnaughMap:
    variables: tuple[str, ...]
    row_variables: tuple[str, ...]
    col_variables: tuple[str, ...]
    row_gray_codes: tuple[str, ...]
    col_gray_codes: tuple[str, ...]
    values: tuple[tuple[int, ...], ...]
    minterms: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class KarnaughMinimizationResult:
    form: str
    variables: tuple[str, ...]
    term_indexes: tuple[int, ...]
    kmap: KarnaughMap
    prime_implicants: tuple[Implicant, ...]
    selected_implicants: tuple[Implicant, ...]
    minimized_expression: str

    @property
    def minterms(self) -> tuple[int, ...]:
        """Backward-compatible alias for existing SDNF-oriented callers."""
        return self.term_indexes


def minimize_sdnf_karnaugh(table: TruthTable) -> KarnaughMinimizationResult:
    return _minimize_karnaugh(table, form="SDNF")


def minimize_sknf_karnaugh(table: TruthTable) -> KarnaughMinimizationResult:
    return _minimize_karnaugh(table, form="SKNF")


def _minimize_karnaugh(table: TruthTable, form: str) -> KarnaughMinimizationResult:
    variable_count = len(table.variables)
    if variable_count > MAX_KARNAUGH_VARIABLES:
        raise ValueError(
            f"Karnaugh map minimization supports up to {MAX_KARNAUGH_VARIABLES} variables"
        )

    kmap = _build_karnaugh_map(table)
    target_value = 1 if form == "SDNF" else 0
    term_indexes = tuple(
        index
        for index, row in enumerate(table.rows)
        if (1 if row.result else 0) == target_value
    )

    if not term_indexes:
        return KarnaughMinimizationResult(
            form=form,
            variables=table.variables,
            term_indexes=term_indexes,
            kmap=kmap,
            prime_implicants=tuple(),
            selected_implicants=tuple(),
            minimized_expression="0" if form == "SDNF" else "1",
        )

    if len(term_indexes) == len(table.rows):
        universal_implicant = Implicant(
            pattern=tuple(None for _ in table.variables),
            covered_minterms=term_indexes,
        )
        return KarnaughMinimizationResult(
            form=form,
            variables=table.variables,
            term_indexes=term_indexes,
            kmap=kmap,
            prime_implicants=(universal_implicant,),
            selected_implicants=(universal_implicant,),
            minimized_expression="1" if form == "SDNF" else "0",
        )

    groups = _all_groups(kmap, target_value)
    prime_implicants = _groups_to_prime_implicants(groups, len(table.variables))
    selected = _select_cover(prime_implicants, set(term_indexes), len(table.variables))
    expression = _implicants_to_expression(selected, table.variables, form)

    return KarnaughMinimizationResult(
        form=form,
        variables=table.variables,
        term_indexes=term_indexes,
        kmap=kmap,
        prime_implicants=prime_implicants,
        selected_implicants=selected,
        minimized_expression=expression,
    )


def minimize_sdnf_karnaugh_from_expression(expression: str) -> KarnaughMinimizationResult:
    table = build_truth_table(expression)
    return minimize_sdnf_karnaugh(table)


def minimize_sknf_karnaugh_from_expression(expression: str) -> KarnaughMinimizationResult:
    table = build_truth_table(expression)
    return minimize_sknf_karnaugh(table)


def format_karnaugh_report(result: KarnaughMinimizationResult) -> str:
    lines = ["Karnaugh map method"]
    lines.append(
        f"Variables: {', '.join(result.variables) if result.variables else '<none>'}"
    )
    lines.extend(_format_map_table(result.kmap))
    lines.append(
        "Prime implicants: "
        + _implicants_to_expression(result.prime_implicants, result.variables, result.form)
    )
    lines.append(
        "Selected implicants: "
        + _implicants_to_expression(result.selected_implicants, result.variables, result.form)
    )
    lines.append(f"Minimized {result.form}: {result.minimized_expression}")
    return "\n".join(lines)


def _build_karnaugh_map(table: TruthTable) -> KarnaughMap:
    variable_count = len(table.variables)
    row_var_count = variable_count // 2
    col_var_count = variable_count - row_var_count

    row_gray = _gray_codes(row_var_count)
    col_gray = _gray_codes(col_var_count)
    row_variables = table.variables[:row_var_count]
    col_variables = table.variables[row_var_count:]

    values: list[tuple[int, ...]] = []
    minterm_matrix: list[tuple[int, ...]] = []

    for row_code in row_gray:
        row_values: list[int] = []
        row_minterms: list[int] = []
        row_code_value = int(row_code, 2) if row_code else 0

        for col_code in col_gray:
            col_code_value = int(col_code, 2) if col_code else 0
            minterm = (row_code_value << col_var_count) | col_code_value
            row_minterms.append(minterm)
            row_values.append(1 if table.rows[minterm].result else 0)

        values.append(tuple(row_values))
        minterm_matrix.append(tuple(row_minterms))

    return KarnaughMap(
        variables=table.variables,
        row_variables=row_variables,
        col_variables=col_variables,
        row_gray_codes=tuple(row_gray),
        col_gray_codes=tuple(col_gray),
        values=tuple(values),
        minterms=tuple(minterm_matrix),
    )


def _gray_codes(bit_count: int) -> list[str]:
    if bit_count == 0:
        return [""]
    return [format(number ^ (number >> 1), f"0{bit_count}b") for number in range(1 << bit_count)]


def _all_groups(kmap: KarnaughMap, target_value: int) -> tuple[tuple[int, ...], ...]:
    row_count = len(kmap.values)
    col_count = len(kmap.values[0]) if row_count > 0 else 0
    row_sizes = _powers_of_two(row_count)
    col_sizes = _powers_of_two(col_count)

    group_set: set[tuple[int, ...]] = set()

    for height in row_sizes:
        for width in col_sizes:
            for start_row in range(row_count):
                for start_col in range(col_count):
                    minterms = []
                    all_ones = True

                    for row_offset in range(height):
                        row_index = (start_row + row_offset) % row_count
                        for col_offset in range(width):
                            col_index = (start_col + col_offset) % col_count
                            if kmap.values[row_index][col_index] != target_value:
                                all_ones = False
                                break
                            minterms.append(kmap.minterms[row_index][col_index])
                        if not all_ones:
                            break

                    if all_ones:
                        group_set.add(tuple(sorted(set(minterms))))

    return tuple(sorted(group_set, key=lambda group: (len(group), group)))


def _powers_of_two(limit: int) -> tuple[int, ...]:
    sizes: list[int] = []
    size = 1
    while size <= limit:
        sizes.append(size)
        size *= 2
    return tuple(sizes)


def _groups_to_prime_implicants(
    groups: tuple[tuple[int, ...], ...],
    variable_count: int,
) -> tuple[Implicant, ...]:
    maximal_groups = []
    for group in groups:
        is_subset = False
        group_set = set(group)
        for other in groups:
            if group == other:
                continue
            other_set = set(other)
            if group_set < other_set:
                is_subset = True
                break
        if not is_subset:
            maximal_groups.append(group)

    implicants_map: dict[tuple[Optional[int], ...], Implicant] = {}
    for group in maximal_groups:
        implicant = _group_to_implicant(group, variable_count)
        existing = implicants_map.get(implicant.pattern)
        if existing is None:
            implicants_map[implicant.pattern] = implicant
            continue
        merged = tuple(sorted(set(existing.covered_minterms) | set(implicant.covered_minterms)))
        implicants_map[implicant.pattern] = Implicant(
            pattern=implicant.pattern,
            covered_minterms=merged,
        )

    return _sort_implicants(tuple(implicants_map.values()))


def _group_to_implicant(group: tuple[int, ...], variable_count: int) -> Implicant:
    pattern: list[Optional[int]] = []
    for position in range(variable_count):
        bit_position = variable_count - 1 - position
        bits = {((minterm >> bit_position) & 1) for minterm in group}
        if len(bits) == 1:
            pattern.append(next(iter(bits)))
        else:
            pattern.append(None)
    return Implicant(pattern=tuple(pattern), covered_minterms=group)


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

    essential: dict[tuple[Optional[int], ...], Implicant] = {}
    covered: set[int] = set()

    for minterm, covering_implicants in coverage_map.items():
        if len(covering_implicants) == 1:
            implicant = covering_implicants[0]
            essential[implicant.pattern] = implicant
            covered.update(
                item
                for item in minterms
                if _covers_minterm(implicant.pattern, item, variable_count)
            )

    remaining = minterms.difference(covered)
    essential_tuple = _sort_implicants(tuple(essential.values()))
    if not remaining:
        return essential_tuple

    candidates = tuple(
        implicant
        for implicant in prime_implicants
        if implicant.pattern not in essential
    )

    extra = _best_subset_cover(candidates, remaining, variable_count)
    selected_map = {implicant.pattern: implicant for implicant in essential_tuple + extra}
    return _sort_implicants(tuple(selected_map.values()))


def _best_subset_cover(
    candidates: tuple[Implicant, ...],
    remaining: set[int],
    variable_count: int,
) -> tuple[Implicant, ...]:
    coverage_cache = {
        implicant.pattern: {
            minterm
            for minterm in remaining
            if _covers_minterm(implicant.pattern, minterm, variable_count)
        }
        for implicant in candidates
    }

    best_solution: tuple[Implicant, ...] | None = None
    best_score: tuple[int, int] | None = None

    def search(uncovered: set[int], chosen: tuple[Implicant, ...]) -> None:
        nonlocal best_solution, best_score

        if not uncovered:
            score = (len(chosen), _total_literals(chosen))
            if best_score is None or score < best_score:
                best_score = score
                best_solution = chosen
            return

        if best_score is not None and len(chosen) >= best_score[0]:
            return

        pivot = min(
            uncovered,
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
            if pivot in coverage_cache[implicant.pattern]
        ]

        for implicant in pivot_candidates:
            newly_covered = coverage_cache[implicant.pattern]
            search(uncovered.difference(newly_covered), chosen + (implicant,))

    search(set(remaining), tuple())

    if best_solution is None:
        return tuple()
    return _sort_implicants(best_solution)


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


def _sort_implicants(implicants: tuple[Implicant, ...]) -> tuple[Implicant, ...]:
    return tuple(
        sorted(
            implicants,
            key=lambda item: (
                sum(1 for bit in item.pattern if bit is not None),
                tuple(2 if bit is None else bit for bit in item.pattern),
            ),
        )
    )


def _total_literals(implicants: Iterable[Implicant]) -> int:
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


def _format_map_table(kmap: KarnaughMap) -> list[str]:
    row_label = "".join(kmap.row_variables) if kmap.row_variables else "-"
    col_label = "".join(kmap.col_variables) if kmap.col_variables else "-"

    lines = [f"Map axes: rows={row_label}, cols={col_label}"]
    header = "rows\\cols | " + " | ".join(code or "0" for code in kmap.col_gray_codes)
    lines.append(header)
    lines.append("-" * len(header))

    for row_code, row_values in zip(kmap.row_gray_codes, kmap.values):
        display_row_code = row_code or "0"
        row_text = " | ".join(str(value) for value in row_values)
        lines.append(f"{display_row_code:>9} | {row_text}")

    return lines
