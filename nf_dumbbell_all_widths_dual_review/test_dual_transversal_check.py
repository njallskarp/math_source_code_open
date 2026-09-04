#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import itertools
import random
import unittest

import dual_transversal_check as check


def brute_minimal_transversals(facets: check.MaskState, vertex_count: int) -> check.MaskState:
    hitting = {
        candidate
        for candidate in range(1 << vertex_count)
        if all(candidate & facet for facet in facets)
    }
    return frozenset(
        candidate
        for candidate in hitting
        if all(
            (candidate ^ bit) not in hitting
            for bit in (1 << index for index in range(vertex_count))
            if candidate & bit
        )
    )


class DualTransversalTests(unittest.TestCase):
    def test_incremental_transversals_against_brute_force(self) -> None:
        rng = random.Random(20260904)
        for vertex_count in range(2, 8):
            nonempty = range(1, 1 << vertex_count)
            for _ in range(30):
                sample_size = rng.randrange(1, min(8, len(nonempty)) + 1)
                facets = frozenset(rng.sample(list(nonempty), sample_size))
                facets = check.inclusion_minimal(facets)
                self.assertEqual(
                    check.minimal_transversals(facets),
                    brute_minimal_transversals(facets, vertex_count),
                )

    def test_k2_clipped_prefix_and_period(self) -> None:
        for m in range(3, 11):
            orbit = check.claimed_types(2, m)
            self.assertNotIn((0, 2, 0, 0), orbit[0])
            self.assertEqual(len(orbit), m + 4)
            digest = hashlib.sha256()
            self.assertEqual(check.check_case(2, m, digest)[0], m + 4)

    def test_small_target_cases(self) -> None:
        digest = hashlib.sha256()
        for k, m in itertools.combinations_with_replacement(range(3, 6), 2):
            states, facets = check.check_case(k, m, digest)
            self.assertEqual(states, k + m + 2)
            self.assertGreater(facets, 0)


if __name__ == "__main__":
    unittest.main()
