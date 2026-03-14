import unittest

from src.logic_parser import LogicSyntaxError, parse_logical_expression


class LogicParserTests(unittest.TestCase):
    def test_accepts_example_in_free_format(self) -> None:
        parsed = parse_logical_expression("!(!a→!b)∨c")
        self.assertEqual(parsed.normalized, "!(!a->!b)|c")
        self.assertEqual(parsed.variables, ("a", "b", "c"))

    def test_supports_all_required_operators(self) -> None:
        parsed = parse_logical_expression("!(a & b) | c -> d ~ e")
        self.assertEqual(parsed.variables, ("a", "b", "c", "d", "e"))

    def test_eval_respects_operator_precedence(self) -> None:
        parsed = parse_logical_expression("!a & b | c")
        result = parsed.evaluate({"a": False, "b": True, "c": False})
        self.assertTrue(result)

    def test_implication_is_right_associative(self) -> None:
        parsed = parse_logical_expression("a -> b -> c")

        value = parsed.evaluate({"a": True, "b": True, "c": False})
        self.assertFalse(value)

    def test_rejects_unsupported_variable(self) -> None:
        with self.assertRaises(LogicSyntaxError):
            parse_logical_expression("x & a")

    def test_rejects_invalid_symbol(self) -> None:
        with self.assertRaises(LogicSyntaxError):
            parse_logical_expression("a + b")

    def test_rejects_unbalanced_parentheses(self) -> None:
        with self.assertRaises(LogicSyntaxError):
            parse_logical_expression("(a & b")

    def test_rejects_empty_expression(self) -> None:
        with self.assertRaises(LogicSyntaxError):
            parse_logical_expression("  \n\t")

    def test_rejects_more_than_five_variables(self) -> None:
        with self.assertRaises(LogicSyntaxError):
            parse_logical_expression("a & b & c & d & e & f")

    def test_requires_value_for_used_variable(self) -> None:
        parsed = parse_logical_expression("a & b")
        with self.assertRaises(LogicSyntaxError):
            parsed.evaluate({"a": True})


if __name__ == "__main__":
    unittest.main()
