#!/usr/bin/env python3

from __future__ import annotations

import itertools
import random
import unittest

import verify


class DumbbellAllWidthsTests(unittest.TestCase):
    def test_fast_maximal_matches_definition(self) -> None:
        rng = random.Random(20260904)
        for k in range(3, 8):
            universe = list(itertools.product((0, 1), range(k), (0, 1), range(6)))
            for _ in range(40):
                sample = frozenset(rng.sample(universe, rng.randrange(len(universe) + 1)))
                slow = frozenset(
                    x
                    for x in sample
                    if not any(x != y and verify.leq(x, y) for y in sample)
                )
                self.assertEqual(verify.maximal(sample, k), slow)

    def test_equal_width_collision_boundary(self) -> None:
        for k in range(3, 13):
            orbit = verify.predicted_orbit(k, k)
            self.assertEqual(len(orbit), 2 * k + 2)
            for left, right in itertools.pairwise(orbit):
                self.assertEqual(verify.delta_types(left, k, k), right)
            self.assertEqual(verify.delta_types(orbit[-1], k, k), orbit[0])

    def test_width_five_required_specialization(self) -> None:
        for m in range(5, 31):
            orbit = verify.predicted_orbit(5, m)
            self.assertEqual(len(orbit), m + 7)
            actual = orbit[0]
            for expected in orbit[1:]:
                actual = verify.delta_types(actual, 5, m)
                self.assertEqual(actual, expected)
            self.assertEqual(verify.delta_types(actual, 5, m), orbit[0])

    def test_wave_and_tail_rules(self) -> None:
        for k in range(3, 16):
            m = k + 12
            q = m - 1
            for s in range(2, q - k + 3):
                self.assertEqual(
                    verify.delta_types(verify.wave_state(k, m, s), k, m),
                    verify.wave_state(k, m, s - 1),
                )
            self.assertEqual(
                verify.delta_types(verify.wave_state(k, m, 1), k, m),
                verify.tail_state(k, m, k - 2),
            )
            for r in range(k - 2, 1, -1):
                self.assertEqual(
                    verify.delta_types(verify.tail_state(k, m, r), k, m),
                    verify.tail_state(k, m, r - 1),
                )

    def test_no_early_graph_after_step_one(self) -> None:
        for k in range(3, 12):
            for m in (k, k + 7):
                orbit = verify.predicted_orbit(k, m)
                self.assertTrue(all(sum(x) == 2 for x in orbit[0] | orbit[1]))
                self.assertTrue(
                    all(max(map(sum, state)) >= 3 for state in orbit[2:])
                )


if __name__ == "__main__":
    unittest.main()
