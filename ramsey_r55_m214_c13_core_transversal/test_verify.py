#!/usr/bin/env python3
"""Small positive and negative controls for verify.py."""

from __future__ import annotations

import unittest
import io
import sys

import verify


class CoreTransversalTests(unittest.TestCase):
    def test_seed_orbits_are_transversals(self) -> None:
        fours = verify.independent_four_masks()
        for _, seed in verify.SEEDS:
            for image in verify.affine_orbit(seed):
                self.assertTrue(verify.is_transversal(image, fours))

    def test_four_vertices_never_hit_every_independent_four(self) -> None:
        fours = verify.independent_four_masks()
        for subset in __import__("itertools").combinations(range(verify.N_CORE), 4):
            self.assertFalse(verify.is_transversal(verify.mask(subset), fours))

    def test_nonautomorphism_multiplier_is_detected(self) -> None:
        self.assertTrue(
            any(
                verify.core_edge(i, j)
                != verify.core_edge((2 * i) % 13, (2 * j) % 13)
                for i in range(13)
                for j in range(i + 1, 13)
            )
        )

    def test_graph6_corruption_changes_model_provenance(self) -> None:
        damaged = verify.MODEL_GRAPH6[:10] + "?" + verify.MODEL_GRAPH6[11:]
        _, edges = verify.decode_graph6(damaged)
        stream = "".join(f"{i} {j}\n" for i, j in sorted(edges)).encode("ascii")
        self.assertNotEqual(__import__("hashlib").sha256(stream).hexdigest(), verify.MODEL_EDGE_SHA256)

    def test_first_model_obstruction_is_blue(self) -> None:
        result = verify.audit_previous_model(verify.independent_four_masks())
        self.assertEqual(result["first_blue_five"], (8, 15, 19, 20, 25))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CoreTransversalTests)
    diagnostics = io.StringIO()
    result = unittest.TextTestRunner(stream=diagnostics, verbosity=0).run(suite)
    if not result.wasSuccessful():
        sys.stderr.write(diagnostics.getvalue())
        raise SystemExit(1)
    print(f"PASS controls tests={result.testsRun}")
