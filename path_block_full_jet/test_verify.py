"""Unit tests for the exact maximal cube-root cancellation witness."""

from __future__ import annotations

import unittest

import verify
from explore_cube_jet import ONE, ZETA, inv, mul


class JetWitnessTests(unittest.TestCase):
    def test_field_inverse(self) -> None:
        self.assertEqual(mul(ZETA, inv(ZETA)), ONE)

    def test_unique_maximal_profiles(self) -> None:
        for parameter in (0, 1, 2, 9):
            left, right = verify.family(parameter)
            self.assertEqual(verify.maximal_prime_profile(left), (14, (3,)))
            self.assertEqual(verify.maximal_prime_profile(right), (14, (3,)))

    def test_exact_cross_jet(self) -> None:
        report = verify.verify()
        self.assertEqual(report["cancelled_orders"], 3)
        self.assertEqual(report["residual_order"], 11)

    def test_first_surviving_normalized_coefficient(self) -> None:
        differences = verify.normalized_cross_differences(
            verify.LEFT, verify.RIGHT, 3
        )
        self.assertEqual(differences[:2], (("0", "0"), ("0", "0")))
        self.assertEqual(differences[2], ("40895/12", "40895/6"))

    def test_parametric_surviving_coefficient(self) -> None:
        for parameter in (1, 3, 4, 10):
            left, right = verify.family(parameter)
            differences = verify.normalized_cross_differences_exact(left, right, 3)
            self.assertEqual(differences[:2], ((0, 0), (0, 0)))
            self.assertEqual(
                differences[2], verify.first_surviving_difference(parameter)
            )


if __name__ == "__main__":
    unittest.main()
