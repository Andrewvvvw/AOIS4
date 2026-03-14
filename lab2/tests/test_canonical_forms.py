import unittest

from src.canonical_forms import build_canonical_forms
from src.truth_table import build_truth_table


class CanonicalFormsTests(unittest.TestCase):
    def test_builds_sdnf_and_sknf_for_and(self) -> None:
        table = build_truth_table("a & b")
        forms = build_canonical_forms(table)

        self.assertEqual(forms.sdnf, "(a & b)")
        self.assertEqual(forms.sknf, "(a | b) & (a | !b) & (!a | b)")

    def test_builds_sdnf_and_sknf_for_or(self) -> None:
        table = build_truth_table("a | b")
        forms = build_canonical_forms(table)

        self.assertEqual(forms.sdnf, "(!a & b) | (a & !b) | (a & b)")
        self.assertEqual(forms.sknf, "(a | b)")

    def test_constant_one_has_trivial_forms(self) -> None:
        table = build_truth_table("1")
        forms = build_canonical_forms(table)

        self.assertEqual(forms.sdnf, "1")
        self.assertEqual(forms.sknf, "1")

    def test_constant_zero_has_trivial_forms(self) -> None:
        table = build_truth_table("0")
        forms = build_canonical_forms(table)

        self.assertEqual(forms.sdnf, "0")
        self.assertEqual(forms.sknf, "0")


if __name__ == "__main__":
    unittest.main()
