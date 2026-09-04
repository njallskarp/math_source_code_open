"""Tests for the cyclotomic-unit endpoint obstruction."""

import unittest

import verify


class CyclotomicUnitTests(unittest.TestCase):
    def test_equal_cycle_examples(self) -> None:
        for left, right, prime in verify.EQUAL_CYCLE_EXAMPLES:
            self.assertEqual(sum(left), sum(right))
            self.assertEqual(len(left), len(right))
            self.assertTrue(verify.unit_obstruction(left, right, prime)["obstructed"])
            self.assertFalse(verify.leading_cross_cancels(left, right, prime))

    def test_equal_cycle_normalized_residue_is_twice_a_unit(self) -> None:
        for left, right, prime in verify.EQUAL_CYCLE_EXAMPLES:
            report = verify.unit_obstruction(left, right, prime)
            self.assertEqual(report["left_block"], report["right_block"])
            self.assertNotEqual(report["normalized_sum_mod_p"], 0)

    def test_height_2095_is_exact_boundary(self) -> None:
        left = verify.HEIGHT_2095_LEFT
        right = verify.HEIGHT_2095_RIGHT
        report = verify.unit_obstruction(left, right, 3)
        self.assertFalse(report["obstructed"])
        self.assertEqual(report["normalized_sum_mod_p"], 0)
        self.assertTrue(verify.leading_cross_cancels(left, right, 3))

    def test_full_report_is_deterministic(self) -> None:
        self.assertEqual(verify.verify(), verify.verify())


if __name__ == "__main__":
    unittest.main()
