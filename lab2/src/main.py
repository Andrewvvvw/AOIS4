from __future__ import annotations

from .boolean_derivatives import build_all_derivatives
from .canonical_forms import build_canonical_forms
from .dummy_variables import find_dummy_variables
from .index_form import build_index_form
from .karnaugh import (
    format_karnaugh_report,
    minimize_sdnf_karnaugh,
    minimize_sknf_karnaugh,
)
from .logic_parser import LogicSyntaxError, parse_logical_expression
from .minimization import (
    format_minimization_report,
    minimize_sdnf_calculation,
    minimize_sknf_calculation,
)
from .numeric_forms import build_numeric_forms
from .post_classes import analyze_post_classes
from .tabular_minimization import (
    format_tabular_minimization_report,
    minimize_sdnf_tabular,
    minimize_sknf_tabular,
)
from .truth_table import TruthTable, build_truth_table
from .zhegalkin import build_zhegalkin_polynomial

def main() -> int:
    expression = input("Expression: ").strip()
    if not expression:
        print("Syntax error: expression is empty")
        return 1

    try:
        parsed = parse_logical_expression(expression)
    except LogicSyntaxError as error:
        print(f"Syntax error: {error}")
        return 1

    print("Expression is valid")
    print(f"Normalized: {parsed.normalized}\n")
    print(f"Variables: {', '.join(parsed.variables) if parsed.variables else '<none>'}\n")
    print("Truth table:")
    table = build_truth_table(parsed)
    _print_truth_table(table)
    
    forms = build_canonical_forms(table)
    print(f"\nSDNF: {forms.sdnf}")
    print(f"SKNF: {forms.sknf}\n")

    numeric_forms = build_numeric_forms(table)
    print(f"SDNF numeric: {numeric_forms.sdnf}")
    print(f"SKNF numeric: {numeric_forms.sknf}\n")

    index_form = build_index_form(table)
    print(f"Function vector: {index_form.vector}")
    print(f"Function index: {index_form.index}\n")

    zhegalkin = build_zhegalkin_polynomial(table)
    print(f"Zhegalkin polynomial: {zhegalkin.expression}\n")

    post_classes = analyze_post_classes(table)
    print(f"Post class T0 (preserves 0): {post_classes.preserves_zero}")
    print(f"Post class T1 (preserves 1): {post_classes.preserves_one}")
    print(f"Post class S (self-dual): {post_classes.self_dual}")
    print(f"Post class M (monotonic): {post_classes.monotonic}")
    print(f"Post class L (linear): {post_classes.linear}\n")

    dummy_analysis = find_dummy_variables(table)
    print(
        "Dummy variables: "
        f"{', '.join(dummy_analysis.dummy_variables) if dummy_analysis.dummy_variables else '<none>'}"
    )
    print(
        "Essential variables: "
        f"{', '.join(dummy_analysis.essential_variables) if dummy_analysis.essential_variables else '<none>'}"
    )

    print("\nBoolean derivatives (orders 1..4):")
    derivatives = build_all_derivatives(table)
    if not derivatives:
        print("<none>")
    for derivative in derivatives:
        variables_part = ",".join(derivative.derivative_variables)
        print(f"d[{variables_part}] = {derivative.expression}")

    minimization_sdnf = minimize_sdnf_calculation(table)
    print(format_minimization_report(minimization_sdnf), "\n")

    minimization_sknf = minimize_sknf_calculation(table)
    print(format_minimization_report(minimization_sknf), "\n")

    tabular_minimization_sdnf = minimize_sdnf_tabular(table)
    print(format_tabular_minimization_report(tabular_minimization_sdnf), "\n")

    tabular_minimization_sknf = minimize_sknf_tabular(table)
    print(format_tabular_minimization_report(tabular_minimization_sknf), "\n")

    try:
        karnaugh_sdnf = minimize_sdnf_karnaugh(table)
        print(format_karnaugh_report(karnaugh_sdnf), "\n")

        karnaugh_sknf = minimize_sknf_karnaugh(table)
        print(format_karnaugh_report(karnaugh_sknf))
    except ValueError as error:
        print(f"Karnaugh map method: {error}")
    return 0


def _print_truth_table(table: TruthTable) -> None:
    variable_headers = list(table.variables)
    header = " | ".join(variable_headers + ["f"])
    separator = "-" * len(header)
    print(header)
    print(separator)

    for row in table.rows:
        value_bits = [_bool_to_bit(value) for value in row.values]
        print(" | ".join(value_bits + [_bool_to_bit(row.result)]))


def _bool_to_bit(value: bool) -> str:
    return "1" if value else "0"


if __name__ == "__main__":
    raise SystemExit(main())
