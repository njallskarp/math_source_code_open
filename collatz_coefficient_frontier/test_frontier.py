import unittest
from itertools import product

from verify_frontier import (
    affine_offset,
    brute_force_distribution,
    certificate,
    coefficient_safe,
    cylinder_residue,
    frontier_rows,
    verify_small,
)


class CoefficientFrontierTests(unittest.TestCase):
    def test_coefficient_safe_examples(self) -> None:
        self.assertTrue(coefficient_safe(()))
        self.assertTrue(coefficient_safe((1, 1, 0)))
        self.assertFalse(coefficient_safe((0,)))
        self.assertFalse(coefficient_safe((1, 0, 0)))

    def test_affine_offset_and_residue_examples(self) -> None:
        self.assertEqual(affine_offset((1, 1, 1, 0, 1, 0, 0, 1)), 347)
        self.assertEqual(cylinder_residue((1, 1, 1, 0, 1, 0, 0, 1)), 7)

    def test_dp_equals_brute_force_through_depth_ten(self) -> None:
        for depth, frontier, _ in frontier_rows(10):
            self.assertEqual(frontier, brute_force_distribution(depth))

    def test_residue_map_is_bijective_through_depth_ten(self) -> None:
        for depth in range(11):
            residues = {
                cylinder_residue(word) for word in product((0, 1), repeat=depth)
            }
            self.assertEqual(len(residues), 2**depth)

    def test_depth_300_certificate(self) -> None:
        report = certificate(300)
        self.assertEqual(
            report["safe_words"],
            111358800986904242131297286221730529252986567662022866509378290558038512175289008981,
        )
        self.assertEqual(report["active_q_states"], 111)
        self.assertEqual(report["minimum_q"], 190)
        self.assertEqual(report["maximum_q"], 300)
        self.assertEqual(report["safe_words_decimal_digits"], 84)
        self.assertEqual(
            report["first_crossings_at_depth"],
            6206542678025330760041752690001599487835420188604033597109748906463205053156170491,
        )
        self.assertEqual(
            report["cumulative_first_crossings"],
            10284792983412195745385360038650916821428153534944615861149592459183121508216685005,
        )
        self.assertEqual(
            report["distribution_sha256"],
            "a2387d04d44100716302089b1b5b53055debdedec60c468f5bd1568782d7d989",
        )
        self.assertEqual(report["rational_ballot_weight"], 190)
        self.assertEqual(
            report["rational_ballot_lower_bound"],
            6635510034197968091686228009120772324133879705860517338469319939807111040176385952,
        )

    def test_small_integrated_verification(self) -> None:
        self.assertEqual(verify_small(5)["words_checked"], 63)


if __name__ == "__main__":
    unittest.main()
