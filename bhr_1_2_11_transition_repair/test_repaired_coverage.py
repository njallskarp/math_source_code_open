#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from audit_repaired_coverage import audit_coverage
from verify import VerificationError

HERE = Path(__file__).resolve().parent
SOURCE_ENV = os.environ.get("BHR_SOURCE_CERTIFICATE")
SOURCE = Path(SOURCE_ENV) if SOURCE_ENV else None


@unittest.skipUnless(
    SOURCE is not None and SOURCE.is_file(),
    "set BHR_SOURCE_CERTIFICATE to the pinned external certificate",
)
class RepairedCoverageTests(unittest.TestCase):
    def test_repaired_coverage_counts(self) -> None:
        summary = audit_coverage(
            SOURCE,  # type: ignore[arg-type]
            HERE / "dead_orthant_certificate.json",
            HERE / "trimodal_certificate.json",
        )
        self.assertEqual(summary["admissible_symbolic_patterns"], 9544)
        self.assertEqual(summary["after_twenty_two_cap_orthants"], 8052)
        self.assertEqual(summary["residual_symbolic_patterns"], 1492)

    def test_tampered_dead_certificate_is_rejected(self) -> None:
        data = json.loads((HERE / "dead_orthant_certificate.json").read_text())
        data["repairs"][0]["boundary_seed"]["counts"][0] += 1
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                audit_coverage(
                    SOURCE,  # type: ignore[arg-type]
                    bad,
                    HERE / "trimodal_certificate.json",
                )


if __name__ == "__main__":
    unittest.main()
