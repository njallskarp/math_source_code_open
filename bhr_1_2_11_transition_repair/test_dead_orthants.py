#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from audit_source_certificate import transported_cut
from verify import VerificationError
from verify_dead_orthants import verify_certificate

HERE = Path(__file__).resolve().parent


class DeadOrthantTests(unittest.TestCase):
    def test_transport_cut(self) -> None:
        self.assertEqual(transported_cut(1, 0, 1), 2)
        self.assertEqual(transported_cut(0, 1, 2), 0)
        self.assertEqual(transported_cut(7, 7, 2), 7)

    def test_certificate_grid(self) -> None:
        summary = verify_certificate(HERE / "dead_orthant_certificate.json", 2)
        self.assertEqual(summary["repairs"], 8)
        self.assertEqual(summary["boundary_losses_reproduced"], 11)
        self.assertEqual(summary["commuting_squares_checked"], 72)

    def test_tampered_interior_seed_is_rejected(self) -> None:
        data = json.loads((HERE / "dead_orthant_certificate.json").read_text())
        path = data["repairs"][0]["interior_seed"]["path"]
        path[0], path[1] = path[1], path[0]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1)


if __name__ == "__main__":
    unittest.main()
