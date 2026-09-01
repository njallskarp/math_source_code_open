#!/usr/bin/env python3

import json
import unittest
from fractions import Fraction
from pathlib import Path

from verify_strict_edge_arb import verify as verify_arb
from verify_strict_edge_exact import edge_count_rows, sin_interval, verify as verify_exact
from verify_strict_edge_identities import verify as verify_identities


HERE = Path(__file__).resolve().parent


class StrictEdgeReductionTests(unittest.TestCase):
    def test_dependency_free_exact_certificate(self) -> None:
        result = verify_exact()
        self.assertTrue(result["exact_strict_edge_certificate"])
        self.assertEqual(result["nonstrict_edge_count_upper"], 30)

    def test_recorded_exact_output(self) -> None:
        recorded = json.loads(
            (HERE / "strict_edge_verification_exact.json").read_text()
        )
        self.assertEqual(recorded, verify_exact())

    def test_independent_arb_certificate(self) -> None:
        self.assertTrue(verify_arb()["arb_strict_edge_certificate"])

    def test_recorded_arb_output(self) -> None:
        recorded = json.loads(
            (HERE / "strict_edge_verification_arb.json").read_text()
        )
        self.assertEqual(recorded, verify_arb())

    def test_exact_symbolic_identities(self) -> None:
        self.assertTrue(verify_identities()["exact_strict_edge_identities"])

    def test_recorded_identity_output(self) -> None:
        recorded = json.loads(
            (HERE / "strict_edge_identities_output.json").read_text()
        )
        self.assertEqual(recorded, verify_identities())

    def test_edge_merge_dichotomy(self) -> None:
        rows = edge_count_rows(16)
        self.assertEqual([row for row in rows if row[2] == 32], [(16, 0, 32)])
        self.assertLessEqual(max(row[2] for row in rows if row[2] != 32), 30)

    def test_sine_checker_rejects_bad_domain(self) -> None:
        with self.assertRaises(ValueError):
            sin_interval(Fraction(-1), Fraction(1, 10), 10)


if __name__ == "__main__":
    unittest.main()
