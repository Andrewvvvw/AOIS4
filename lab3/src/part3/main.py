try:
    from .part3_counter import solve_part3
except ImportError:
    from part3_counter import solve_part3


def run_part3() -> None:
    print("Часть 3. Синтез двоичного вычитающего счетчика на Т-триггерах.")
    solve_part3()


def main() -> None:
    run_part3()


if __name__ == "__main__":
    main()
