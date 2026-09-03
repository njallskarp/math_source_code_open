#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verify import VerificationError
from independent_target_check import check as independent_check
from verify_target_orthant import verify_certificate

HERE = Path(__file__).resolve().parent


class TargetOrthantTests(unittest.TestCase):
    def test_independent_seed_check(self) -> None:
        summary = independent_check(HERE / "target_orthant_certificate.json")
        self.assertEqual(summary["order"], 35)
        self.assertEqual(
            summary["path_sha256"],
            "5b42c507459a1633675821b84935894dea9f14a959e70e2d11760172f399227b",
        )

    def test_certificate_small_grid(self) -> None:
        summary = verify_certificate(HERE / "target_orthant_certificate.json", 1)
        self.assertEqual(summary["seed_order"], 35)
        self.assertEqual(summary["source_derivation_steps"], 18)
        self.assertEqual(summary["family_paths_checked"], 27)
        self.assertEqual(summary["coordinate_transitions_checked"], 24)
        self.assertEqual(summary["commuting_squares_checked"], 24)

    def test_tampered_seed_is_rejected(self) -> None:
        data = json.loads(
            (HERE / "target_orthant_certificate.json").read_text()
        )
        data["seed"]["path"][0], data["seed"]["path"][1] = (
            data["seed"]["path"][1],
            data["seed"]["path"][0],
        )
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)

    def test_tampered_cut_is_rejected(self) -> None:
        data = json.loads(
            (HERE / "target_orthant_certificate.json").read_text()
        )
        data["seed"]["selected_growth_cuts"]["11"] += 1
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)


if __name__ == "__main__":
    unittest.main()
