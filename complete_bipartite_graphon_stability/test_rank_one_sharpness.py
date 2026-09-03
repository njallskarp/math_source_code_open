from fractions import Fraction
import unittest

from verify_rank_one_sharpness import (
    density_polynomial,
    direct_cut_coefficient,
    moment,
    run_checks,
)


VALUES = (Fraction(-2), Fraction(1))
WEIGHTS = (Fraction(1, 3), Fraction(2, 3))
P = Fraction(2, 5)


class RankOneSharpnessTests(unittest.TestCase):
    def test_asymmetric_distribution_moments(self) -> None:
        self.assertEqual(moment(VALUES, WEIGHTS, 1), 0)
        self.assertEqual(moment(VALUES, WEIGHTS, 2), 2)
        self.assertEqual(moment(VALUES, WEIGHTS, 3), -2)

    def test_k22_polynomial_is_exactly_quartic(self) -> None:
        polynomial = density_polynomial(2, 2, P, VALUES, WEIGHTS)
        self.assertEqual(polynomial, (P**4, 0, 0, 0, Fraction(16)))

    def test_k23_fifth_order_vanishes_despite_nonzero_third_moment(self) -> None:
        polynomial = density_polynomial(2, 3, P, VALUES, WEIGHTS)
        self.assertEqual(polynomial[:6], (P**6, 0, 0, 0, Fraction(192, 25), 0))
        self.assertEqual(polynomial[6], 32)

    def test_cut_coefficient(self) -> None:
        self.assertEqual(direct_cut_coefficient(VALUES, WEIGHTS), Fraction(4, 9))

    def test_small_run(self) -> None:
        count, digest = run_checks(3)
        self.assertEqual(count, 4)
        self.assertEqual(len(digest), 64)

    def test_invalid_part_size(self) -> None:
        with self.assertRaises(ValueError):
            density_polynomial(1, 2, P, VALUES, WEIGHTS)


if __name__ == "__main__":
    unittest.main()
