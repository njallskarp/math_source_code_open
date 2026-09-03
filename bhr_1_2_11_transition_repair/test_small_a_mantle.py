#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from audit_small_a_mantle_coverage import audit_mantle_coverage
from independent_small_a_mantle_check import check as independent_check
from verify import VerificationError, verify_realization
from verify_small_a_mantle import advance, normalize_cuts, verify_certificate

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "small_a_mantle_certificate.json"
SOURCE_ENV = os.environ.get("BHR_SOURCE_CERTIFICATE")
SOURCE = Path(SOURCE_ENV) if SOURCE_ENV else None


class SmallAMantleTests(unittest.TestCase):
    def test_certificate_small_grid(self) -> None:
        summary = verify_certificate(CERTIFICATE, 1)
        self.assertEqual(summary["residue_classes"], 11)
        self.assertEqual(summary["source_derivation_steps"], 44)
        self.assertEqual(summary["family_paths_checked"], 99)
        self.assertEqual(summary["coordinate_transitions_checked"], 88)
        self.assertEqual(summary["commuting_squares_checked"], 44)

    def test_independent_small_grid(self) -> None:
        summary = independent_check(CERTIFICATE, 1)
        self.assertEqual(summary["residue_classes"], 11)
        self.assertEqual(summary["minimum_seed_order"], 36)
        self.assertEqual(summary["safe_margin"], "35<=36")

    def test_large_family_state(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        seed = data["cases"][7]["safe_seed"]
        state = (seed["path"], normalize_cuts(seed["selected_growth_cuts"]))
        for _ in range(20):
            state = advance(*state, 2)
        for _ in range(20):
            state = advance(*state, 11)
        verify_realization(state[0], (1, 49, 250))

    def test_tampered_seed_is_rejected(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        data["cases"][4]["safe_seed"]["selected_growth_cuts"]["2"] += 1
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)

    def test_duplicate_residue_is_rejected(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        data["cases"][10]["residue_case"] = [1, 1, 10]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)

    @unittest.skipUnless(
        SOURCE is not None and SOURCE.is_file(),
        "set BHR_SOURCE_CERTIFICATE to the pinned external certificate",
    )
    def test_coverage_gain(self) -> None:
        summary = audit_mantle_coverage(
            SOURCE,  # type: ignore[arg-type]
            HERE / "dead_orthant_certificate.json",
            HERE / "trimodal_certificate.json",
            HERE / "residual_slab_certificate.json",
            HERE / "even_b_c1_certificate.json",
            HERE / "target_orthant_certificate.json",
            HERE / "small_a_c3_slab_certificate.json",
            CERTIFICATE,
        )
        self.assertEqual(summary["newly_covered"], 60)
        self.assertEqual(summary["after_small_a_mantle"], 8211)
        self.assertEqual(summary["residual_symbolic_patterns"], 1333)


if __name__ == "__main__":
    unittest.main()
