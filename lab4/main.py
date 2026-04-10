from __future__ import annotations

from constants import (
    MENU_CREATE_OPTION,
    MENU_DELETE_OPTION,
    MENU_EXIT_OPTION,
    MENU_PRINT_OPTION,
    MENU_READ_OPTION,
    MENU_STATS_OPTION,
    MENU_TEXT,
    MENU_UPDATE_OPTION,
)
from exceptions import DuplicateKeyError, InvalidKeyError, KeyNotFoundError
from hash_table import QuadraticProbingHashTable
from models import TableRow


def _print_rows(rows: list[TableRow], output_fn=print) -> None:
    output_fn("\nIdx | ID | C | U | T | L | D | Po | Pi | V | h(V)")
    for row in rows:
        output_fn(
            f"{row.index:3} | "
            f"{row.id_value or '-'} | "
            f"{row.collision_flag} | "
            f"{row.used_flag} | "
            f"{row.terminal_flag} | "
            f"{row.link_flag} | "
            f"{row.deleted_flag} | "
            f"{row.overflow_pointer if row.overflow_pointer is not None else '-'} | "
            f"{row.pointer_or_data or '-'} | "
            f"{row.v_value if row.v_value is not None else '-'} | "
            f"{row.base_hash if row.base_hash is not None else '-'} | "
        )


def _print_stats(table: QuadraticProbingHashTable, output_fn=print) -> None:
    output_fn(f"Capacity: {table.capacity}")
    output_fn(f"Load factor: {table.load_factor():.2f}")


def _read_key_and_value(input_fn=input) -> tuple[str, str]:
    key = input_fn("Enter key: ")
    value = input_fn("Enter value: ")
    return key, value


def _handle_create(table: QuadraticProbingHashTable, input_fn=input, output_fn=print) -> None:
    key, value = _read_key_and_value(input_fn)
    table.create(key, value)
    output_fn("Created.")


def _handle_read(table: QuadraticProbingHashTable, input_fn=input, output_fn=print) -> None:
    key = input_fn("Enter key: ")
    value = table.read(key)
    if value is None:
        output_fn("Not found.")
        return
    output_fn(f"Found: {value}")


def _handle_update(table: QuadraticProbingHashTable, input_fn=input, output_fn=print) -> None:
    key, value = _read_key_and_value(input_fn)
    table.update(key, value)
    output_fn("Updated.")


def _handle_delete(table: QuadraticProbingHashTable, input_fn=input, output_fn=print) -> None:
    key = input_fn("Enter key: ")
    table.delete(key)
    output_fn("Deleted.")


def _process_choice(
    choice: str,
    table: QuadraticProbingHashTable,
    input_fn=input,
    output_fn=print,
) -> bool:
    if choice == MENU_CREATE_OPTION:
        _handle_create(table, input_fn, output_fn)
        return True
    if choice == MENU_READ_OPTION:
        _handle_read(table, input_fn, output_fn)
        return True
    if choice == MENU_UPDATE_OPTION:
        _handle_update(table, input_fn, output_fn)
        return True
    if choice == MENU_DELETE_OPTION:
        _handle_delete(table, input_fn, output_fn)
        return True
    if choice == MENU_PRINT_OPTION:
        _print_rows(table.to_rows(), output_fn)
        return True
    if choice == MENU_STATS_OPTION:
        _print_stats(table, output_fn)
        return True
    if choice == MENU_EXIT_OPTION:
        output_fn("Goodbye.")
        return False
    output_fn("Unknown command.")
    return True


def run_cli(
    table: QuadraticProbingHashTable | None = None,
    input_fn=input,
    output_fn=print,
) -> None:
    active_table = table or QuadraticProbingHashTable()
    should_continue = True
    while should_continue:
        output_fn(MENU_TEXT)
        choice = input_fn("Choose option: ").strip()
        try:
            should_continue = _process_choice(choice, active_table, input_fn, output_fn)
        except (InvalidKeyError, DuplicateKeyError, KeyNotFoundError, ValueError) as error:
            output_fn(f"Error: {error}")


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()
