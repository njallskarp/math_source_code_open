from __future__ import annotations

import unittest
from fractions import Fraction

import independent_check as check


class IndependentPrimeDefectTests(unittest.TestCase):
    def test_berlekamp_massey_fibonacci(self) -> None:
        sequence = [0, 1]
        for _ in range(18):
            sequence.append(sequence[-1] + sequence[-2])
        self.assertEqual(
            check.berlekamp_massey(sequence),
            [Fraction(1), Fraction(-1), Fraction(-1)],
        )

    def test_tail_decision_boundaries(self) -> None:
        self.assertTrue(check.tail_polynomiality((1,), (1, 1)))
        self.assertTrue(check.tail_polynomiality((2,), (2, 2)))
        self.assertFalse(check.tail_polynomiality((2, 1), (1, 1, 1, 1)))

    def test_base_and_unequal_hard_poles(self) -> None:
        self.assertEqual(check.phi3_pole_order(check.BASE_LEFT, check.BASE_RIGHT)[1], 2)
        for left, right in check.HARD_UNEQUAL_CASES:
            self.assertEqual(check.phi3_pole_order(left, right)[1], 2)

    def test_quotient_ring_cancellation_scan(self) -> None:
        scan = check.first_leading_cancellation()
        self.assertEqual(scan["checked"], 4527)
        self.assertEqual(scan["first_width"], 21)
        self.assertEqual(scan["found"], [(check.BASE_LEFT, check.BASE_RIGHT, 3)])

    def test_full_audit(self) -> None:
        result = check.audit()
        self.assertEqual(result["mismatches"], [])
        self.assertEqual(result["predicted_polynomial"], result["observed_polynomial"])
        self.assertTrue(all(item["phi3_pole_order"] == 2 for item in result["hard_cases"]))
        self.assertEqual(result["cancellation_scan"]["checked"], 4527)


if __name__ == "__main__":
    unittest.main()
