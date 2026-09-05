#!/usr/bin/env python3
"""Unit tests for the exact Q5 compatibility corroboration."""

from fractions import Fraction
import unittest

import verify


class CompatibilityTests(unittest.TestCase):
    def test_q5_incidence(self) -> None:
        self.assertEqual(len(verify.Vertices), 32)
        self.assertEqual(len(verify.Edges), 80)
        self.assertEqual(len(verify.Squares), 80)
        self.assertEqual(len(verify.Facets), 10)
        self.assertEqual({len(x) for x in verify.EdgeFacets.values()}, {4})

    def test_live_facet_capacities(self) -> None:
        self.assertEqual(verify.capacity_distribution(4), {0: 130, 1: 80})
        self.assertEqual(verify.capacity_distribution(8), {16: 5, 28: 40})

    def test_certificate_constants(self) -> None:
        data = verify.certificate()
        self.assertEqual(data["strict_q5_delta_lower_bound"], 1)
        self.assertEqual(data["q5_slack_edge_ratio"], str(Fraction(673, 1904)))
        self.assertEqual(
            data["global_slack_coefficient"], str(Fraction(673, 22848))
        )
        self.assertEqual(
            data["improvement_over_119_66"], str(Fraction(119, 1463550))
        )


if __name__ == "__main__":
    unittest.main()
