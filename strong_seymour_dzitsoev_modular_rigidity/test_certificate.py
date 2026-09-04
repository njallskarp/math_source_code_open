#!/usr/bin/env python3
"""Unit tests for the compact modular-rigidity certificate."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import generate_certificate as generator


class ModularRigidityTests(unittest.TestCase):
    def test_exact_regeneration(self) -> None:
        path = Path(__file__).with_name("certificate.json")
        self.assertEqual(json.loads(path.read_text()), generator.build_certificate())

    def test_every_quotient_pair_forces_all_vertices(self) -> None:
        rows = generator.quotient_rows()
        for first, second in generator.PAIRS:
            self.assertEqual(
                generator.closure_trace(rows, (1 << first) | (1 << second))[-1],
                (1 << generator.QUOTIENT_ORDER) - 1,
            )

    def test_expanded_cross_pairs_force_whole_tournament(self) -> None:
        rows, fibers = generator.expand(
            generator.quotient_rows(), generator.MINIMUM_SIZES
        )
        owner = {
            vertex: index
            for index, fiber in enumerate(fibers)
            for vertex in range(len(rows))
            if fiber >> vertex & 1
        }
        full = (1 << len(rows)) - 1
        for first, second, closed in generator.pair_closure_records(rows):
            if owner[first] != owner[second]:
                self.assertEqual(closed, full)

    def test_module_count_and_maximal_modules(self) -> None:
        rows, fibers = generator.expand(
            generator.quotient_rows(), generator.MINIMUM_SIZES
        )
        modules = generator.interval_modules(fibers)
        self.assertEqual(len(modules), 159)
        self.assertEqual(
            generator.maximal_proper_modules(modules, (1 << len(rows)) - 1),
            fibers,
        )


if __name__ == "__main__":
    unittest.main()
