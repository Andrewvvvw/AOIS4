from __future__ import annotations

import circuits


def _print_equations(section_title: str, equation_list, include_sdnf: bool = False) -> None:
    print(section_title)
    for equation in equation_list:
        if include_sdnf:
            print(
                f"{equation.name}:\nSDNF: {equation.sdnf}\nMinimized: {equation.minimized}\n"
            )
        else:
            print(f"{equation.name} = {equation.minimized}")
    print()


def main() -> None:
    _print_equations("ОДС-3 (Одноразрядный двоичный сумматор)", circuits.get_adder_equations(), True)
    _print_equations("5421 BCD -> Двоичный", circuits.get_decoder_5421_equations())
    _print_equations("Сумматор двоичных -> двоичная сумма", circuits.get_bcd_adder_equations())
    _print_equations(
        "Двоичный -> 5421 BCD (смещение n=1, десятки/единицы)",
        circuits.get_encoder_5421_equations_offset_n(),
    )
    _print_equations(
        "Двоичный счетчик вычитающего типа на 8 внутренних состояний в базисе НЕ-И ИЛИ и Т-триггер.",
        circuits.get_counter_equations(),
    )


if __name__ == "__main__":
    main()