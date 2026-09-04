"""Tests for the whole-jet factorial-block unit obstruction."""

import unittest

import verify


class WholeJetUnitTests(unittest.TestCase):
    def test_hard_witness_profile(self) -> None:
        self.assertEqual(sum(verify.LEFT), sum(verify.RIGHT))
        self.assertEqual(verify.maximal_prime_profile(verify.LEFT), (4, (7,)))
        self.assertEqual(verify.maximal_prime_profile(verify.RIGHT), (4, (7,)))

    def test_complete_jet_separates_counts(self) -> None:
        left = verify.whole_jet_polynomial(8, 4, 7)
        right = verify.whole_jet_polynomial(9, 4, 7)
        self.assertNotEqual(left, right)
        self.assertNotEqual(left[1], right[1])

    def test_leading_wave_cancels_but_full_jet_does_not(self) -> None:
        report = verify.cross_report(verify.LEFT, verify.RIGHT, 4)
        self.assertEqual(report["cancelled_orders"], 1)
        self.assertEqual(report["residual_order"], 3)

    def test_report_is_deterministic(self) -> None:
        self.assertEqual(verify.verify(), verify.verify())


if __name__ == "__main__":
    unittest.main()
