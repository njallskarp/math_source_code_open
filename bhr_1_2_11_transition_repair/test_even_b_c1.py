#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verify import VerificationError, verify_realization
from verify_even_b_c1 import family_a_path, family_b_path, verify_certificate

HERE = Path(__file__).resolve().parent


class EvenBC1Tests(unittest.TestCase):
    def test_formula_seeds(self) -> None:
        data = json.loads((HERE / "even_b_c1_certificate.json").read_text())
        self.assertEqual(family_a_path(0), data["families"][0]["path_at_q_zero"])
        self.assertEqual(family_b_path(0), data["families"][1]["path_at_q_zero"])

    def test_certificate_small_grid(self) -> None:
        summary = verify_certificate(HERE / "even_b_c1_certificate.json", 1)
        self.assertEqual(summary["family_paths_checked"], 6)
        self.assertEqual(summary["transitions_checked"], 4)

    def test_large_formula_states(self) -> None:
        verify_realization(family_a_path(1000), (1, 2020, 1))
        verify_realization(family_b_path(1000), (2, 2018, 1))

    def test_tampered_seed_is_rejected(self) -> None:
        data = json.loads((HERE / "even_b_c1_certificate.json").read_text())
        seed = data["families"][0]["path_at_q_zero"]
        seed[0], seed[1] = seed[1], seed[0]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)


if __name__ == "__main__":
    unittest.main()
