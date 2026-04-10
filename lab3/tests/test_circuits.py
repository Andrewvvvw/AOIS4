import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import circuits
import constants


def eval_expr(expr: str, mapping: dict[str, bool]) -> bool:
    expr = expr.strip()
    if expr == "1":
        return True
    if expr in {"0", ""}:
        return False

    python_expr = expr.replace("!", " not ").replace("&", " and ").replace("|", " or ")
    tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", python_expr))
    for token in sorted(tokens, key=len, reverse=True):
        if token in {"and", "or", "not"}:
            continue
        python_expr = re.sub(rf"\b{token}\b", f"mapping['{token}']", python_expr)

    return bool(eval(python_expr, {"__builtins__": {}}, {"mapping": mapping}))


class TestCircuits(unittest.TestCase):
    def test_decode_5421_valid_and_invalid(self):
        valid_pairs = {
            0b0000: 0,
            0b0001: 1,
            0b0010: 2,
            0b0011: 3,
            0b0100: 4,
            0b1000: 5,
            0b1001: 6,
            0b1010: 7,
            0b1011: 8,
            0b1100: 9,
        }
        for encoded, expected in valid_pairs.items():
            value, is_valid = circuits.decode_5421(encoded)
            self.assertTrue(is_valid)
            self.assertEqual(value, expected)

        invalid_values = set(range(16)) - set(valid_pairs.keys())
        for encoded in invalid_values:
            value, is_valid = circuits.decode_5421(encoded)
            self.assertFalse(is_valid)
            self.assertEqual(value, -1)

        value, is_valid = circuits.decode_5421(99)
        self.assertFalse(is_valid)
        self.assertEqual(value, -1)

    def test_encode_5421_valid_and_invalid(self):
        for digit in range(10):
            encoded = circuits.encode_5421(digit)
            decoded, is_valid = circuits.decode_5421(encoded)
            self.assertTrue(is_valid)
            self.assertEqual(decoded, digit)

        self.assertEqual(circuits.encode_5421(-1), 0)
        self.assertEqual(circuits.encode_5421(10), 0)
        self.assertEqual(circuits.encode_5421(42), 0)

    def test_get_adder_equations(self):
        equations = circuits.get_adder_equations()
        self.assertEqual(len(equations), 2)

        sum_equation = next(eq for eq in equations if eq.name.startswith("S"))
        carry_equation = next(eq for eq in equations if eq.name.startswith("C"))
        self.assertTrue(sum_equation.sdnf)
        self.assertTrue(carry_equation.sdnf)

        sum_minterms = {1, 2, 4, 7}
        carry_minterms = {3, 5, 6, 7}
        for value in range(8):
            mapping = {
                "X1": bool((value >> 2) & 1),
                "X2": bool((value >> 1) & 1),
                "X3": bool(value & 1),
            }
            self.assertEqual(eval_expr(sum_equation.sdnf, mapping), value in sum_minterms)
            self.assertEqual(
                eval_expr(sum_equation.minimized, mapping),
                value in sum_minterms,
            )
            self.assertEqual(eval_expr(carry_equation.sdnf, mapping), value in carry_minterms)
            self.assertEqual(
                eval_expr(carry_equation.minimized, mapping),
                value in carry_minterms,
            )

    def test_get_decoder_5421_equations(self):
        equations = circuits.get_decoder_5421_equations()
        self.assertEqual(len(equations), 4)
        eq_map = {eq.name: eq for eq in equations}
        self.assertEqual(set(eq_map), {"O3", "O2", "O1", "O0"})
        self.assertTrue(all(eq.sdnf == "" for eq in equations))

        for encoded in range(16):
            mapping = {
                "I3": bool((encoded >> 3) & 1),
                "I2": bool((encoded >> 2) & 1),
                "I1": bool((encoded >> 1) & 1),
                "I0": bool(encoded & 1),
            }
            decoded, is_valid = circuits.decode_5421(encoded)
            if not is_valid:
                continue
            expected = {
                "O3": bool(decoded & 8),
                "O2": bool(decoded & 4),
                "O1": bool(decoded & 2),
                "O0": bool(decoded & 1),
            }
            for output_name, expected_value in expected.items():
                self.assertEqual(
                    eval_expr(eq_map[output_name].minimized, mapping),
                    expected_value,
                )

    def test_get_bcd_adder_equations(self):
        equations = circuits.get_bcd_adder_equations()
        self.assertEqual(len(equations), 5)
        eq_map = {eq.name: eq for eq in equations}
        self.assertEqual(set(eq_map), {"S4", "S3", "S2", "S1", "S0"})
        self.assertTrue(all(eq.sdnf == "" for eq in equations))

        for left_digit in range(16):
            for right_digit in range(16):
                mapping = {
                    "A3": bool((left_digit >> 3) & 1),
                    "A2": bool((left_digit >> 2) & 1),
                    "A1": bool((left_digit >> 1) & 1),
                    "A0": bool(left_digit & 1),
                    "B3": bool((right_digit >> 3) & 1),
                    "B2": bool((right_digit >> 2) & 1),
                    "B1": bool((right_digit >> 1) & 1),
                    "B0": bool(right_digit & 1),
                }
                if left_digit > 9 or right_digit > 9:
                    continue

                total = left_digit + right_digit
                expected = {
                    "S4": bool(total & 16),
                    "S3": bool(total & 8),
                    "S2": bool(total & 4),
                    "S1": bool(total & 2),
                    "S0": bool(total & 1),
                }
                for output_name, expected_value in expected.items():
                    self.assertEqual(
                        eval_expr(eq_map[output_name].minimized, mapping),
                        expected_value,
                    )

    def test_get_encoder_5421_equations_and_wrapper(self):
        for offset in (0, constants.OFFSET_N, 20, 40):
            equations = circuits.get_encoder_5421_equations(offset)
            self.assertEqual(len(equations), 8)
            eq_map = {eq.name: eq for eq in equations}
            self.assertEqual(
                set(eq_map),
                {"T3", "T2", "T1", "T0", "U3", "U2", "U1", "U0"},
            )
            self.assertTrue(all(eq.sdnf == "" for eq in equations))

            for input_value in range(19):
                mapping = {
                    "S4": bool((input_value >> 4) & 1),
                    "S3": bool((input_value >> 3) & 1),
                    "S2": bool((input_value >> 2) & 1),
                    "S1": bool((input_value >> 1) & 1),
                    "S0": bool(input_value & 1),
                }
                shifted = input_value + offset
                tens = shifted // 10
                units = shifted % 10
                tens_bcd = circuits.encode_5421(tens)
                units_bcd = circuits.encode_5421(units)
                expected = {
                    "T3": bool(tens_bcd & 8),
                    "T2": bool(tens_bcd & 4),
                    "T1": bool(tens_bcd & 2),
                    "T0": bool(tens_bcd & 1),
                    "U3": bool(units_bcd & 8),
                    "U2": bool(units_bcd & 4),
                    "U1": bool(units_bcd & 2),
                    "U0": bool(units_bcd & 1),
                }
                for output_name, expected_value in expected.items():
                    self.assertEqual(
                        eval_expr(eq_map[output_name].minimized, mapping),
                        expected_value,
                    )

        wrapped = circuits.get_encoder_5421_equations_offset_n()
        direct = circuits.get_encoder_5421_equations(constants.OFFSET_N)
        self.assertEqual(
            [equation.minimized for equation in wrapped],
            [equation.minimized for equation in direct],
        )

    def test_get_counter_equations(self):
        equations = circuits.get_counter_equations()
        self.assertEqual(len(equations), 3)
        eq_map = {eq.name: eq for eq in equations}
        self.assertEqual(set(eq_map), {"T2", "T1", "T0"})
        self.assertTrue(all(eq.sdnf == "" for eq in equations))

        for current_state in range(constants.COUNTER_MAX_STATE):
            mapping = {
                "Q2": bool((current_state >> 2) & 1),
                "Q1": bool((current_state >> 1) & 1),
                "Q0": bool(current_state & 1),
            }
            next_state = (
                current_state - 1 + constants.COUNTER_MAX_STATE
            ) % constants.COUNTER_MAX_STATE
            toggles = current_state ^ next_state
            expected = {
                "T2": bool((toggles >> 2) & 1),
                "T1": bool((toggles >> 1) & 1),
                "T0": bool(toggles & 1),
            }
            for output_name, expected_value in expected.items():
                self.assertEqual(
                    eval_expr(eq_map[output_name].minimized, mapping),
                    expected_value,
                )
