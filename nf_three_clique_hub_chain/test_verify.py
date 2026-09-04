#!/usr/bin/env python3
"""Unit tests for the all-parameter hubbed clique-chain certificate."""

from __future__ import annotations

import unittest

import verify


class HubCliqueChainTests(unittest.TestCase):
    def test_base_poset_and_weight(self) -> None:
        self.assertEqual(len(verify.BASES), 72)
        self.assertEqual(set(verify.WEIGHT.values()), set(range(-9, 1)))
        self.assertEqual(verify.verify_weight_order(), 204)

    def test_symbolic_prefix(self) -> None:
        self.assertEqual(verify.verify_symbolic_prefix(), 9)
        self.assertEqual(verify.verify_small_prefix_exceptions(), 63)

    def test_wave_and_endpoints(self) -> None:
        self.assertEqual(verify.verify_wave_regimes(), 15)
        self.assertEqual(verify.verify_endpoints(), 5)

    def test_boundary_orbits(self) -> None:
        for m in (3, 4, 9, 12):
            q = m - 1
            orbit = verify.predicted_orbit(q)
            self.assertEqual(len(orbit), m + 8)
            for step, state in enumerate(orbit):
                self.assertEqual(
                    verify.delta_types(state, q), orbit[(step + 1) % len(orbit)]
                )

    def test_no_early_graph_state(self) -> None:
        for q in range(2, 13):
            orbit = verify.predicted_orbit(q)
            self.assertTrue(all(sum(type_) == 2 for type_ in orbit[0]))
            self.assertTrue(
                all(
                    any(sum(type_) != 2 for type_ in state)
                    for state in orbit[1:]
                )
            )


if __name__ == "__main__":
    unittest.main()
