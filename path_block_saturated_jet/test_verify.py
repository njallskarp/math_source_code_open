"""Unit tests for the saturated cyclotomic whole-jet invariant."""

from __future__ import annotations

import unittest

import verify


class SaturatedJetTests(unittest.TestCase):
    def test_full_transform_equals_closed_formula(self) -> None:
        for prime in (3, 5, 7):
            for defect in range(1, 2 * prime + 1):
                for q in range(1, 2 * prime + 1):
                    self.assertEqual(
                        verify.saturated_residue_jet(q, defect, prime),
                        verify.saturated_residue_closed(q, defect, prime),
                    )

    def test_divisible_factors_have_universal_residue(self) -> None:
        for prime in (3, 5, 7):
            for multiplier in (1, 2, prime, prime + 1):
                residues = verify.normalized_vanishing_factor_residues(prime * multiplier, prime)
                expected = [0] * len(residues)
                expected[0] = 1
                expected[prime - 1] = -1 % prime
                self.assertEqual(residues, tuple(expected))

    def test_exact_saturated_witness(self) -> None:
        self.assertEqual(verify.maximal_prime_profile(verify.LEFT), (3, (5,)))
        self.assertEqual(verify.maximal_prime_profile(verify.RIGHT), (3, (5,)))
        self.assertEqual(verify.saturated_residue_closed(3, 3, 5), (1, 2, 0))
        self.assertEqual(verify.saturated_residue_closed(4, 3, 5), (1, 3, 0))
        self.assertEqual(verify.denominator_remainder((12, 7, 1), 5), (-1, -2, -3, 1))
        self.assertEqual(verify.denominator_remainder((4, 3, 3), 5), (1, 2, 3, -1))
        self.assertEqual(verify.cross_report(verify.LEFT, verify.RIGHT, 3)["cancelled_orders"], 1)

    def test_height_2095_family_is_residue_blind(self) -> None:
        expected = (1,) + (0,) * 13
        self.assertEqual(verify.saturated_residue_closed(8, 14, 3), expected)
        self.assertEqual(verify.saturated_residue_closed(6, 14, 3), expected)


if __name__ == "__main__":
    unittest.main()
