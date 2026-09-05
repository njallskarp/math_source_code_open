#!/usr/bin/env python3
"""Unit tests for the Q6 live-facet capacity checker."""

from fractions import Fraction
import unittest

import verify


class Q6LiftTests(unittest.TestCase):
    def test_q6_incidence(self) -> None:
        self.assertEqual(len(verify.VERTICES), 64)
        self.assertEqual(len(verify.EDGES), 192)
        self.assertEqual(len(verify.SQUARES), 240)
        self.assertEqual(len(verify.FACETS), 12)
        self.assertEqual(verify.Q3_SUBCUBE_COUNT, 160)
        self.assertEqual({len(x) for x in verify.EDGE_FACETS.values()}, {5})

    def test_hand_checkable_profiles(self) -> None:
        six_singletons = frozenset((coordinate, 0) for coordinate in range(6))
        self.assertEqual(verify.pair_profile(six_singletons), (0, 6, 0))
        self.assertEqual(verify.enumerated_capacity(six_singletons), 6)
        eleven_live = frozenset(verify.FACETS) - {(5, 1)}
        self.assertEqual(verify.pair_profile(eleven_live), (5, 1, 0))
        self.assertEqual(verify.enumerated_capacity(eleven_live), 112)

    def test_all_facet_sets_match_structural_formula(self) -> None:
        maxima, audit_hash = verify.capacity_audit()
        self.assertEqual(maxima[5], 1)
        self.assertEqual(maxima[10], 64)
        self.assertEqual(maxima[11], 112)
        self.assertEqual(len(audit_hash), 64)

    def test_bound_constants(self) -> None:
        data = verify.certificate()
        self.assertEqual(data["q6_deficit_per_edge"], "1/11")
        self.assertEqual(data["q6_slack_edge_ratio"], str(Fraction(661, 1122)))
        self.assertEqual(
            data["global_slack_coefficient"], str(Fraction(661, 22440))
        )
        self.assertEqual(
            data["improvement_over_39984_22175"],
            str(Fraction(714, 482949325)),
        )

    def test_invalid_mask_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify.live_facets(-1)
        with self.assertRaises(ValueError):
            verify.live_facets(1 << 12)


if __name__ == "__main__":
    unittest.main()
