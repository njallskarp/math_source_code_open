#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from independent_a2_mantle_check import check as independent_check
from verify import VerificationError, verify_realization
from verify_a2_mantle import advance, normalize_cuts, verify_certificate

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "a2_mantle_certificate.json"
SOURCE_ENV = os.environ.get("BHR_SOURCE_CERTIFICATE")
SOURCE = Path(SOURCE_ENV) if SOURCE_ENV else None


class A2MantleTests(unittest.TestCase):
    def test_certificate_small_grid(self) -> None:
        summary = verify_certificate(CERTIFICATE, 1)
        self.assertEqual(summary["residue_classes"], 11)
        self.assertEqual(summary["source_derivation_steps"], 72)
        self.assertEqual(summary["family_paths_checked"], 297)
        self.assertEqual(summary["coordinate_transitions_checked"], 264)
        self.assertEqual(summary["commuting_squares_checked"], 264)

    def test_independent_small_grid(self) -> None:
        summary = independent_check(CERTIFICATE, 1)
        self.assertEqual(summary["two_mode_sources"], 9)
        self.assertEqual(summary["existing_safe_residues_rederived"], 2)
        self.assertEqual(summary["minimum_seed_order"], 36)
        self.assertEqual(summary["safe_margin"], "35<=36")

    def test_large_trimodal_family_state(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        seed = data["cases"][7]["safe_seed"]
        state = (seed["path"], normalize_cuts(seed["selected_growth_cuts"]))
        for mode in (1, 2, 11):
            for _ in range(20):
                state = advance(*state, mode)
        verify_realization(state[0], (22, 49, 250))

    def test_tampered_retained_cut_is_rejected(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        data["cases"][4]["safe_seed"]["selected_growth_cuts"]["1"] += 1
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
    def test_external_provenance_and_successor_links(self) -> None:
        summary = verify_certificate(
            CERTIFICATE,
            1,
            source_path=SOURCE,
            trimodal_path=HERE / "trimodal_certificate.json",
        )
        self.assertTrue(summary["external_provenance_checked"])
        self.assertEqual(summary["trimodal_successor_links_checked"], 11)


if __name__ == "__main__":
    unittest.main()
