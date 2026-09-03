#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

try:
    from .construct import construct, interior_path
    from .verify import (
        VerificationError,
        grow_once,
        verify_certificate,
        verify_realization,
    )
except ImportError:  # Direct unittest execution from this directory.
    from construct import construct, interior_path
    from verify import VerificationError, grow_once, verify_certificate, verify_realization

HERE = Path(__file__).resolve().parent


class RepairTests(unittest.TestCase):
    def test_certificate_and_grid(self) -> None:
        summary = verify_certificate(HERE / "certificate.json", 4)
        self.assertEqual(summary["commuting_squares_checked"], 25)

    def test_closed_transition_square(self) -> None:
        path = interior_path(3, 2)
        self.assertEqual(grow_once(path, 1, 18), interior_path(4, 2))
        self.assertEqual(grow_once(path, 2, 22), interior_path(3, 3))

    def test_constructor_partition(self) -> None:
        for counts in ((1, 16, 4), (1, 28, 4), (9, 16, 4), (9, 28, 4)):
            _, path = construct(*counts)
            verify_realization(path, counts)

    def test_tampered_seed_is_rejected(self) -> None:
        data = json.loads((HERE / "certificate.json").read_text())
        data["interior_seed"]["path"][0], data["interior_seed"]["path"][1] = (
            data["interior_seed"]["path"][1],
            data["interior_seed"]["path"][0],
        )
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify_certificate(bad, 1)


if __name__ == "__main__":
    unittest.main()
