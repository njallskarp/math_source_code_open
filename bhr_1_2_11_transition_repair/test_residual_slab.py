#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verify import VerificationError, verify_realization
from verify_residual_slab import residual_slab_path, verify_certificate

HERE = Path(__file__).resolve().parent


class ResidualSlabTests(unittest.TestCase):
    def test_formula_seed(self) -> None:
        self.assertEqual(
            residual_slab_path(0, 0),
            [
                1, 3, 5, 7, 9, 11, 13, 14, 16, 18, 20, 22, 24,
                0, 2, 4, 6, 8, 10, 12, 23, 21, 19, 17, 15,
            ],
        )

    def test_certificate_small_grid(self) -> None:
        summary = verify_certificate(HERE / "residual_slab_certificate.json", 1)
        self.assertEqual(summary["family_paths_checked"], 9)
        self.assertEqual(summary["coordinate_transitions_checked"], 8)
        self.assertEqual(summary["commuting_squares_checked"], 4)

    def test_large_formula_state(self) -> None:
        verify_realization(residual_slab_path(1000, 1000), (1002, 2021, 1))

    def test_tampered_seed_is_rejected(self) -> None:
        data = json.loads((HERE / "residual_slab_certificate.json").read_text())
        path = data["seed"]["path"]
        path[0], path[1] = path[1], path[0]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)


if __name__ == "__main__":
    unittest.main()
