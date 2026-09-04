"""Tests for the complete cubic-root lift modulo pi^3."""

from __future__ import annotations

import unittest

import verify


class CubicLiftTests(unittest.TestCase):
    def test_cyclotomic_field_and_valuation(self) -> None:
        self.assertEqual(verify.mul(verify.ZETA, verify.ZETA), (-1, -1))
        self.assertEqual(verify.pi_valuation(verify.PI), 1)
        self.assertEqual(verify.pi_valuation(verify.scale(verify.ONE, 3)), 2)
        self.assertEqual(verify.unit_residue_after_division(verify.PI, 1), 1)

    def test_divisible_factor_is_weight_independent(self) -> None:
        model = verify.cubic_divisible_factor()
        for multiplier in (1, 2, 3, 4, 9, 10):
            weight = 3 * multiplier
            exact = [
                verify.scale(
                    verify.power(verify.PI, degree),
                    verify.Fraction((-1) ** degree * verify.comb(weight, degree + 1), weight),
                )
                for degree in range(weight)
            ]
            for degree, coefficient in enumerate(exact):
                expected = model[degree] if degree < len(model) else verify.ZERO
                self.assertTrue(verify.congruent(coefficient, expected, 3))

    def test_lift_matches_exact_wave(self) -> None:
        left, right = verify.family(0)
        for partition in (left, right):
            exact = verify.exact_scaled_h(partition, verify.DEFECT)
            lifted = verify.lifted_scaled_h(partition, verify.DEFECT)
            self.assertTrue(
                all(verify.congruent(a, b, 3) for a, b in zip(exact, lifted, strict=True))
            )

    def test_complete_associated_graded_difference(self) -> None:
        expected = (0, 0, 0, 1) + (0,) * 10
        for parameter in (0, 1, 2, 7):
            left, right = verify.family(parameter)
            self.assertEqual(
                verify.complete_difference_layer(left, right, verify.DEFECT, 2),
                expected,
            )


if __name__ == "__main__":
    unittest.main()
