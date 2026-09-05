#!/usr/bin/env python3
"""Unit tests for the Q6 modular-gap arithmetic certificate."""

from fractions import Fraction
import unittest

import verify


class ModularGapTests(unittest.TestCase):
    def test_small_delta_residue_classes(self) -> None:
        self.assertEqual(
            [e for e in range(1, 57) if verify.least_positive_delta(e) == 1],
            [7, 24, 41],
        )
        self.assertEqual(
            [e for e in range(1, 57) if verify.least_positive_delta(e) == 2],
            [14, 31, 48],
        )
        self.assertEqual(
            [e for e in range(1, 57) if verify.least_positive_delta(e) == 3],
            [4, 21, 38, 55],
        )
        self.assertEqual(
            [e for e in range(1, 57) if verify.least_positive_delta(e) == 4],
            [11, 28, 45],
        )

    def test_refined_eleven_facet_cap(self) -> None:
        self.assertEqual(verify.EDGE_CAP_BY_LIVE_COUNT[11], 32 + 56)

    def test_exact_arithmetic_minima(self) -> None:
        audit, audit_hash = verify.arithmetic_audit()
        self.assertEqual(
            {k: row["minimum_W"] for k, row in audit.items()},
            {5: 274, 6: 148, 7: 122, 8: 70, 9: 66, 10: 58, 11: 41, 12: 37},
        )
        self.assertEqual(len(audit_hash), 64)

    def test_equality_classification_and_bound(self) -> None:
        data = verify.certificate()
        self.assertEqual(data["strict_q6_modular_gap"], 37)
        self.assertEqual(data["arithmetic_equality_E_D_k"], [95, 12, 12])
        self.assertEqual(data["arithmetic_equality_facet_edges"], [24] + [41] * 11)
        self.assertEqual(data["arithmetic_equality_profile_count"], 1)
        self.assertEqual(
            data["local_slack_edge_ratio"], str(Fraction(87_289, 148_104))
        )
        self.assertEqual(
            data["improvement_over_39270_21779"],
            str(Fraction(1_452_990, 62_610_073_189)),
        )

    def test_invalid_inputs_are_rejected(self) -> None:
        for edge_count in (0, 57):
            with self.assertRaises(ValueError):
                verify.least_positive_delta(edge_count)
        for live_count in (0, 1, 4, 13):
            with self.assertRaises(ValueError):
                verify.arithmetic_minimum(live_count)


if __name__ == "__main__":
    unittest.main()
