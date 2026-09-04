#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

import generate_certificate as generator
import independent_check as independent


class SixQuotientRigidityTests(unittest.TestCase):
    def test_quotient_orbit_count(self) -> None:
        representatives = generator.quotient_representatives()
        self.assertEqual(len(representatives), 56)
        self.assertIn(generator.DZITSOEV_CANONICAL_MASK, representatives)

    def test_published_relabeling(self) -> None:
        permutation = (5, 4, 0, 1, 3, 2)
        self.assertEqual(generator.relabel(generator.PUBLISHED_MASK, permutation), 345)

    def test_dzitsoev_closure_profile(self) -> None:
        out = generator.tournament_out(345)
        self.assertEqual(
            tuple(len(generator.closed_rows(out, root)) for root in range(6)),
            (2, 3, 3, 2, 3, 3),
        )

    def test_certificate_regeneration(self) -> None:
        path = Path(__file__).with_name("certificate.json")
        self.assertEqual(json.loads(path.read_text()), generator.build_certificate())

    def test_direct_minimum_witness(self) -> None:
        arcs = independent.expanded_tournament(345, (11, 3, 3, 9, 3, 7))
        self.assertEqual(independent.strong_vertices(arcs), ())


if __name__ == "__main__":
    unittest.main()
