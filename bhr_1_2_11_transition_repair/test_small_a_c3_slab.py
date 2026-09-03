#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from independent_small_a_c3_check import check as independent_check
from verify import VerificationError, verify_realization
from verify_small_a_c3_slab import advance, normalize_cuts, verify_certificate

HERE = Path(__file__).resolve().parent


class SmallAC3SlabTests(unittest.TestCase):
    def test_certificate_small_grid(self) -> None:
        summary = verify_certificate(HERE / "small_a_c3_slab_certificate.json", 1)
        self.assertEqual(summary["source_derivation_steps"], 4)
        self.assertEqual(summary["family_paths_checked"], 9)
        self.assertEqual(summary["coordinate_transitions_checked"], 8)
        self.assertEqual(summary["commuting_squares_checked"], 4)

    def test_independent_seed_check(self) -> None:
        summary = independent_check(HERE / "small_a_c3_slab_certificate.json", 1)
        self.assertEqual(summary["seed_order"], 36)
        self.assertEqual(summary["growth_cuts"], {2: 2, 11: 13})
        self.assertEqual(summary["safe_margin"], "35<=36")

    def test_large_family_state(self) -> None:
        data = json.loads((HERE / "small_a_c3_slab_certificate.json").read_text())
        state = (data["seed"]["path"], normalize_cuts(data["seed"]["selected_growth_cuts"]))
        for _ in range(20):
            state = advance(*state, 2)
        for _ in range(20):
            state = advance(*state, 11)
        verify_realization(state[0], (1, 49, 245))

    def test_tampered_seed_is_rejected(self) -> None:
        data = json.loads((HERE / "small_a_c3_slab_certificate.json").read_text())
        seed = data["seed"]["path"]
        seed[0], seed[1] = seed[1], seed[0]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)


if __name__ == "__main__":
    unittest.main()
