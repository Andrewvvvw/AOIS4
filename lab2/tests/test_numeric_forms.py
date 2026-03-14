import unittest

from src.numeric_forms import build_numeric_forms
from src.truth_table import build_truth_table


class NumericFormsTests(unittest.TestCase):
    def test_numeric_forms_for_and(self) -> None:
        table = build_truth_table("a & b")
        forms = build_numeric_forms(table)

        self.assertEqual(forms.sdnf_indices, (3,))
        self.assertEqual(forms.sknf_indices, (0, 1, 2))
        self.assertEqual(forms.sdnf, "V(3)")
        self.assertEqual(forms.sknf, "^(0,1,2)")

    def test_numeric_forms_for_or(self) -> None:
        table = build_truth_table("a | b")
        forms = build_numeric_forms(table)

        self.assertEqual(forms.sdnf_indices, (1, 2, 3))
        self.assertEqual(forms.sknf_indices, (0,))
        self.assertEqual(forms.sdnf, "V(1,2,3)")
        self.assertEqual(forms.sknf, "^(0)")

    def test_numeric_forms_for_constant_one(self) -> None:
        table = build_truth_table("1")
        forms = build_numeric_forms(table)

        self.assertEqual(forms.sdnf_indices, (0,))
        self.assertEqual(forms.sknf_indices, tuple())
        self.assertEqual(forms.sdnf, "V(0)")
        self.assertEqual(forms.sknf, "^()")

    def test_numeric_forms_for_constant_zero(self) -> None:
        table = build_truth_table("0")
        forms = build_numeric_forms(table)

        self.assertEqual(forms.sdnf_indices, tuple())
        self.assertEqual(forms.sknf_indices, (0,))
        self.assertEqual(forms.sdnf, "V()")
        self.assertEqual(forms.sknf, "^(0)")


if __name__ == "__main__":
    unittest.main()
