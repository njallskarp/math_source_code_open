#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verify import VerificationError
from verify_trimodal import verify_certificate

HERE = Path(__file__).resolve().parent


class TrimodalTests(unittest.TestCase):
    def test_certificate_grid(self) -> None:
        summary = verify_certificate(HERE / "trimodal_certificate.json", 1)
        self.assertEqual(summary["cases"], 22)
        self.assertEqual(summary["source_derivation_steps"], 396)
        self.assertEqual(summary["family_paths_checked"], 594)
        self.assertEqual(summary["coordinate_transitions_checked"], 528)
        self.assertEqual(summary["commuting_squares_checked"], 528)

    def test_tampered_cap_is_rejected(self) -> None:
        data = json.loads((HERE / "trimodal_certificate.json").read_text())
        path = data["cases"][0]["cap_seed"]["path"]
        path[0], path[1] = path[1], path[0]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1)

    def test_tampered_safe_seed_is_rejected(self) -> None:
        data = json.loads((HERE / "trimodal_certificate.json").read_text())
        data["cases"][3]["safe_seed"]["selected_growth_cuts"]["11"] += 1
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1)


if __name__ == "__main__":
    unittest.main()
