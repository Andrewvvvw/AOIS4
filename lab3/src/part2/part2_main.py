try:
    from . import part2_adder
except ImportError:
    import part2_adder


OUTPUT_LABELS = [
    "Десятки_Бит3", "Десятки_Бит2", "Десятки_Бит1", "Десятки_Бит0",
    "Единицы_Бит3", "Единицы_Бит2", "Единицы_Бит1", "Единицы_Бит0",
]


def print_task_header() -> None:
    print("Часть 2. 5421 BCD, смещение n=1.")
    print("Метод минимизации: алгоритм Квайна-МакКласки (с учетом избыточных наборов).")


def print_minimized_results(truth_table: dict) -> None:
    for idx, label in enumerate(OUTPUT_LABELS):
        minimized_terms = part2_adder.minimize_function(truth_table, idx)
        formatted_terms = " or ".join(sorted(minimized_terms)) if minimized_terms else "0"
        print(f"Функция {label}: {formatted_terms}")


def run_part2() -> None:
    print_task_header()
    truth_table = part2_adder.generate_truth_table()

    print("\nТаблица истинности сгенерирована (256 строк).")
    print("Выполняется аналитическая минимизация всех 8 выходных битов...\n")
    print_minimized_results(truth_table)


def main() -> None:
    run_part2()


if __name__ == "__main__":
    main()
