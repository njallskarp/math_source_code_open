#!/usr/bin/env python3
"""Small boundary tests for the singular-DP excess-potential formulas."""

import unittest

from ramsey_r55_symbolic_extension.verify_singular_dp_excess_contraction import ceiling_div


class ExcessContractionTests(unittest.TestCase):
    def test_smallest_parameter_pair_still_forces_three(self) -> None:
        p, fan = 3, 1
        self.assertEqual(ceiling_div(90 + 2 * fan - 2 * p, 41 - p), 3)

    def test_exceptional_top_stratum(self) -> None:
        p, fan = 33, 10
        self.assertEqual(90 + 2 * fan - 2 * p, 44)
        self.assertEqual(41 - p, 8)
        self.assertEqual(ceiling_div(44, 8), 6)

    def test_charge_four_boundary_is_strict(self) -> None:
        self.assertEqual(ceiling_div(90 + 2 * 10 - 2 * 13, 41 - 13), 3)
        self.assertEqual(ceiling_div(90 + 2 * 10 - 2 * 14, 41 - 14), 4)

    def test_ceiling_division(self) -> None:
        self.assertEqual(ceiling_div(6, 3), 2)
        self.assertEqual(ceiling_div(7, 3), 3)


if __name__ == "__main__":
    unittest.main()
