import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import qm


class TestQM(unittest.TestCase):
    def test_implicant_methods(self):
        first = qm.Implicant(1, 2)
        same = qm.Implicant(1, 2)
        different = qm.Implicant(2, 2)
        self.assertTrue(first.is_equal(same))
        self.assertFalse(first.is_equal(different))

        imp = qm.Implicant(0b10, 0b01)
        self.assertTrue(imp.covers(0b10))
        self.assertTrue(imp.covers(0b11))
        self.assertFalse(imp.covers(0b00))
        self.assertFalse(imp.covers(0b01))

    def test_differ_by_one_bit_variants(self):
        left = qm.Implicant(0, 0)
        right = qm.Implicant(1, 0)
        can_merge, merged = qm.differ_by_one_bit(left, right)
        self.assertTrue(can_merge)
        self.assertEqual(merged.value, 0)
        self.assertEqual(merged.mask, 1)

        can_merge, merged = qm.differ_by_one_bit(qm.Implicant(3, 0), qm.Implicant(3, 0))
        self.assertFalse(can_merge)
        self.assertEqual(merged, qm.Implicant(0, 0))

        can_merge, merged = qm.differ_by_one_bit(qm.Implicant(0, 0), qm.Implicant(3, 0))
        self.assertFalse(can_merge)
        self.assertEqual(merged, qm.Implicant(0, 0))

        can_merge, merged = qm.differ_by_one_bit(qm.Implicant(0, 1), qm.Implicant(1, 0))
        self.assertFalse(can_merge)
        self.assertEqual(merged, qm.Implicant(0, 0))

    def test_generate_sdnf(self):
        self.assertEqual(qm.generate_sdnf(2, [1, 3], ["A", "B"]), "(!A & B) | (A & B)")
        self.assertEqual(qm.generate_sdnf(2, [], ["A", "B"]), "0")

    def test_minimize_public_cases(self):
        self.assertEqual(qm.minimize(2, [0, 1, 2, 3], None, ["A", "B"]), "1")
        self.assertEqual(qm.minimize(2, [], None, ["A", "B"]), "0")
        self.assertEqual(qm.minimize(2, [1, 3], None, ["A", "B"]), "(B)")
        self.assertEqual(qm.minimize(2, [1], [0], ["A", "B"]), "(!A)")

        result = qm.minimize(3, [0, 1, 2, 5, 6, 7], [3], ["A", "B", "C"])
        self.assertTrue(len(result) > 0)

    def test_internal_helpers(self):
        initialized = qm._init_implicants([0, 1], [2])
        self.assertEqual(initialized, [qm.Implicant(0, 0), qm.Implicant(1, 0), qm.Implicant(2, 0)])

        no_merge_primes = qm._find_prime_implicants([0, 3], [])
        self.assertEqual(set(no_merge_primes), {qm.Implicant(0, 0), qm.Implicant(3, 0)})

        merge_primes = qm._find_prime_implicants([0, 1], [])
        self.assertEqual(merge_primes, [qm.Implicant(0, 1)])

        prime_list = [qm.Implicant(0, 1), qm.Implicant(2, 1), qm.Implicant(0, 0)]
        essentials, remaining = qm._find_essential_primes(prime_list, [0, 2])
        self.assertEqual(essentials, [qm.Implicant(2, 1)])
        self.assertEqual(remaining, [0])

        covers = qm._get_covers(prime_list, 0)
        self.assertEqual(covers, [qm.Implicant(0, 1), qm.Implicant(0, 0)])

        with_duplicate = qm._append_unique([qm.Implicant(0, 1)], qm.Implicant(0, 1))
        self.assertEqual(with_duplicate, [qm.Implicant(0, 1)])
        with_new_item = qm._append_unique(with_duplicate, qm.Implicant(2, 1))
        self.assertEqual(with_new_item, [qm.Implicant(0, 1), qm.Implicant(2, 1)])

        covered_only_by_essentials = qm._cover_remaining([], prime_list, [qm.Implicant(0, 1)])
        self.assertEqual(covered_only_by_essentials, [qm.Implicant(0, 1)])

        needs_extra_cover = qm._cover_remaining([2], prime_list, [])
        self.assertTrue(any(imp.covers(2) for imp in needs_extra_cover))

        best_prime = qm._find_best_prime([qm.Implicant(0, 1), qm.Implicant(2, 1)], [0, 1, 2])
        self.assertEqual(best_prime, qm.Implicant(0, 1))

        self.assertEqual(
            qm._format_implicant(qm.Implicant(0, 0), 2, ["A", "B"]),
            "(!A & !B)",
        )
        self.assertEqual(
            qm._format_implicant(qm.Implicant(2, 1), 2, ["A", "B"]),
            "(A)",
        )
        self.assertEqual(
            qm._format_solution([qm.Implicant(0, 0), qm.Implicant(1, 0)], 2, ["A", "B"]),
            "(!A & !B) | (!A & B)",
        )
        self.assertEqual(qm._format_solution([qm.Implicant(0, 3)], 2, ["A", "B"]), "1")

