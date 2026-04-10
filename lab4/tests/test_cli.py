import io
import os
import sys
import unittest
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import main


def _run_cli_scripted(inputs: list[str]) -> str:
    input_iterator = iter(inputs)
    captured_output = io.StringIO()

    def fake_input(_: str = "") -> str:
        return next(input_iterator)

    def fake_output(message: str = "") -> None:
        print(message, file=captured_output)

    main.run_cli(input_fn=fake_input, output_fn=fake_output)
    return captured_output.getvalue()


class CliTests(unittest.TestCase):
    def test_cli_crud_flow(self) -> None:
        output = _run_cli_scripted(
            [
                "1",
                "AA",
                "first",
                "2",
                "AA",
                "3",
                "AA",
                "second",
                "2",
                "AA",
                "4",
                "AA",
                "2",
                "AA",
                "6",
                "0",
            ]
        )
        self.assertIn("Created.", output)
        self.assertIn("Found: first", output)
        self.assertIn("Updated.", output)
        self.assertIn("Found: second", output)
        self.assertIn("Deleted.", output)
        self.assertIn("Not found.", output)
        self.assertIn("Load factor:", output)
        self.assertIn("Goodbye.", output)

    def test_cli_reports_errors_and_unknown_command(self) -> None:
        output = _run_cli_scripted(
            [
                "1",
                "AA",
                "first",
                "1",
                "AA",
                "duplicate",
                "3",
                "Missing",
                "value",
                "99",
                "0",
            ]
        )
        self.assertIn("Error:", output)
        self.assertIn("already exists", output)
        self.assertIn("does not exist", output)
        self.assertIn("Unknown command.", output)

    def test_main_calls_run_cli(self) -> None:
        with patch.object(main, "run_cli") as mocked_run_cli:
            main.main()
        mocked_run_cli.assert_called_once()


if __name__ == "__main__":
    unittest.main()
