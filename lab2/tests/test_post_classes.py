import unittest

from src.post_classes import analyze_post_classes
from src.truth_table import build_truth_table


class PostClassesTests(unittest.TestCase):
    def test_and_class_membership(self) -> None:
        classes = analyze_post_classes(build_truth_table("a & b"))

        self.assertTrue(classes.preserves_zero)
        self.assertTrue(classes.preserves_one)
        self.assertFalse(classes.self_dual)
        self.assertTrue(classes.monotonic)
        self.assertFalse(classes.linear)

    def test_not_a_class_membership(self) -> None:
        classes = analyze_post_classes(build_truth_table("!a"))

        self.assertFalse(classes.preserves_zero)
        self.assertFalse(classes.preserves_one)
        self.assertTrue(classes.self_dual)
        self.assertFalse(classes.monotonic)
        self.assertTrue(classes.linear)

    def test_constant_one_class_membership(self) -> None:
        classes = analyze_post_classes(build_truth_table("1"))

        self.assertFalse(classes.preserves_zero)
        self.assertTrue(classes.preserves_one)
        self.assertFalse(classes.self_dual)
        self.assertTrue(classes.monotonic)
        self.assertTrue(classes.linear)


if __name__ == "__main__":
    unittest.main()
