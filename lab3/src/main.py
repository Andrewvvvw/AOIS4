from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from part1.main import run_part1
from part2.part2_main import run_part2
from part3.main import run_part3


def print_separator(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def main() -> None:
    print_separator("ЧАСТЬ 1")
    run_part1()

    print_separator("ЧАСТЬ 2")
    run_part2()

    print_separator("ЧАСТЬ 3")
    run_part3()


if __name__ == "__main__":
    main()
