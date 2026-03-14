import unittest

from src.dummy_variables import find_dummy_variables
from src.truth_table import build_truth_table


class DummyVariablesTests(unittest.TestCase):
    def test_finds_no_dummy_variables_for_and(self) -> None:
        analysis = find_dummy_variables(build_truth_table("a & b"))

        self.assertEqual(analysis.dummy_variables, tuple())
        self.assertEqual(analysis.essential_variables, ("a", "b"))

    def test_finds_dummy_variable_in_absorption_case(self) -> None:
        analysis = find_dummy_variables(build_truth_table("a | (b & !b)"))

        self.assertEqual(analysis.dummy_variables, ("b",))
        self.assertEqual(analysis.essential_variables, ("a",))

    def test_finds_dummy_variable_in_tautology(self) -> None:
        analysis = find_dummy_variables(build_truth_table("a -> a"))

        self.assertEqual(analysis.dummy_variables, ("a",))
        self.assertEqual(analysis.essential_variables, tuple())

    def test_handles_constant_expression(self) -> None:
        analysis = find_dummy_variables(build_truth_table("1"))

        self.assertEqual(analysis.dummy_variables, tuple())
        self.assertEqual(analysis.essential_variables, tuple())


if __name__ == "__main__":
    unittest.main()
