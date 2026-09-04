"""Tests for the independent equal-cycle audit."""

import unittest
from math import comb

import independent_check as audit


class IndependentAuditTests(unittest.TestCase):
    def test_small_direct_grid(self) -> None:
        report = audit.direct_grid(7)
        self.assertEqual(report["polynomial_pairs"], report["predicted_rectangular_pairs"])
        self.assertEqual(report["unequal_width_polynomial_pairs"], 0)
        self.assertEqual(report["equal_width_nonrectangular_polynomial_pairs"], 0)

    def test_matching_rectangle_has_binomial_square_numerator(self) -> None:
        parts = (3, 3, 3)
        observed = audit.endpoint_numerator(parts, parts)
        expected = [0] * 10
        for index in range(4):
            expected[3 * index] = comb(3, index) ** 2
        self.assertEqual(observed, expected)

    def test_unequal_width_rectangles_are_not_polynomial(self) -> None:
        self.assertIsNone(audit.endpoint_numerator((2, 2), (3, 3)))

    def test_equal_width_nonrectangle_is_not_polynomial(self) -> None:
        self.assertIsNone(audit.endpoint_numerator((3, 2, 1), (2, 2, 2)))

    def test_height_2095_is_outside_equal_cycle_obstruction(self) -> None:
        report = audit.boundary_check()
        self.assertEqual(report["normalized_sum_mod_p"], 0)
        self.assertTrue(report["leading_cancels"])
        self.assertNotEqual(len(audit.HEIGHT_2095_LEFT), len(audit.HEIGHT_2095_RIGHT))


if __name__ == "__main__":
    unittest.main()
