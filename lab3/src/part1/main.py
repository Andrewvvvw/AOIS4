try:
    from . import adder_logic
except ImportError:
    import adder_logic


def print_variant_info() -> None:
    print("Часть 1. Одноразрядный двоичный сумматор на 3 входа (ОДС-3) в СДНФ.")


def print_truth_table(truth_table: list[dict]) -> None:
    print("\nТаблица истинности:")
    print("a | b | cin || sum | cout")
    for row in truth_table:
        print(f"{row['a']} | {row['b']} |  {row['cin']}  ||  {row['sum']}  |  {row['cout']}")


def print_results(truth_table: list[dict]) -> None:
    sum_sdnf = adder_logic.get_sdnf(truth_table, "sum")
    cout_sdnf = adder_logic.get_sdnf(truth_table, "cout")

    cout_minterms = adder_logic.get_minterms_binary(truth_table, "cout")
    cout_minimized = adder_logic.minimize(cout_minterms)

    print("\nСДНФ суммы (sum):", sum_sdnf)
    print("СДНФ переноса (cout):", cout_sdnf)
    print("\nМинимизированная функция переноса (бинарные термы):", cout_minimized)
    print("Примечание: функция суммы для ОДС-3 не минимизируется.")


def run_part1() -> None:
    print_variant_info()
    truth_table = adder_logic.generate_truth_table()
    print_truth_table(truth_table)
    print_results(truth_table)


def main() -> None:
    run_part1()


if __name__ == "__main__":
    main()
