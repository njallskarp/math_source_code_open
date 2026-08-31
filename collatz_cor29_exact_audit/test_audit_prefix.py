#!/usr/bin/env python3

import unittest
from fractions import Fraction

from audit_prefix import (
    correction_factor_exact,
    correction_factor_float,
    audit_prefix,
    ceil_fraction,
)


class ExactPrefixAuditTests(unittest.TestCase):
    def test_ceil_fraction(self) -> None:
        self.assertEqual(ceil_fraction(Fraction(7, 3)), 3)
        self.assertEqual(ceil_fraction(Fraction(-7, 3)), -2)
        self.assertEqual(ceil_fraction(Fraction(6, 3)), 2)

    def test_correction_factor_base_and_recursive_cases(self) -> None:
        self.assertEqual(correction_factor_exact(0, 1, False), 1)
        exact = correction_factor_exact(6, 91, False)
        approximate = correction_factor_float(6, 91, False)
        self.assertAlmostEqual(float(exact), approximate, places=15)

    def test_small_prefix_has_no_binary64_disagreement(self) -> None:
        audit = audit_prefix(depth=16, c=1536)
        self.assertEqual(audit.generated, 4_782)
        self.assertEqual(audit.pruned_exact, 900)
        self.assertEqual(audit.frontier, 1_492)
        self.assertEqual(audit.decision_disagreements, 0)
        self.assertEqual(audit.second_branch_disagreements, 0)


if __name__ == "__main__":
    unittest.main()
