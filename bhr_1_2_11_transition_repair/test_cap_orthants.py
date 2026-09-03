#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verify import VerificationError
from verify_cap_orthants import verify_certificate

HERE = Path(__file__).resolve().parent


class CapOrthantTests(unittest.TestCase):
    def test_all_faces_on_small_grid(self) -> None:
        summary = verify_certificate(HERE / "trimodal_certificate.json", 1)
        self.assertEqual(summary["cap_orthants"], 22)
        self.assertEqual(summary["partition_strata"], 176)
        self.assertEqual(summary["face_seeds"], 66)
        self.assertEqual(summary["face_derivation_steps"], 264)
        self.assertEqual(summary["tri_seed_links_checked"], 66)
        self.assertEqual(summary["ray_paths_checked"], 198)
        self.assertEqual(summary["face_family_paths_checked"], 594)
        self.assertEqual(summary["face_coordinate_transitions_checked"], 528)
        self.assertEqual(summary["face_commuting_squares_checked"], 264)

    def test_tampered_cap_cut_is_rejected(self) -> None:
        data = json.loads((HERE / "trimodal_certificate.json").read_text())
        data["cases"][0]["cap_seed"]["selected_growth_cuts"]["11"] += 1
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)

    def test_tampered_face_source_path_is_rejected(self) -> None:
        data = json.loads((HERE / "trimodal_certificate.json").read_text())
        path = data["cases"][7]["cap_seed"]["path"]
        path[0], path[1] = path[1], path[0]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1, enforce_pinned_hash=False)


if __name__ == "__main__":
    unittest.main()
