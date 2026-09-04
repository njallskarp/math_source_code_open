#!/usr/bin/env python3
"""Tamper-rejection tests for the exact certificate verifier."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from verify_certificate import verify


HERE = Path(__file__).resolve().parent


class CertificateTests(unittest.TestCase):
    def test_committed_certificate(self) -> None:
        output = verify(HERE / "certificate.txt", HERE / "obstructions.txt")
        self.assertIn("classes=96", output)
        self.assertIn("stable_rate=7/6", output)

    def test_primal_tamper_is_rejected(self) -> None:
        text = (HERE / "certificate.txt").read_text(encoding="ascii")
        class_start = text.index("\nCLASS ")
        marker = "primal="
        location = text.index(marker, class_start) + len(marker)
        term_end = text.index(",", location)
        term = text[location:term_end]
        order, _ = term.split(":")
        corrupted = text[:location] + f"{order}:1/1" + text[term_end:]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            path.write_text(corrupted, encoding="ascii")
            with self.assertRaises(ValueError):
                verify(path, HERE / "obstructions.txt")

    def test_dual_tamper_is_rejected(self) -> None:
        text = (HERE / "certificate.txt").read_text(encoding="ascii")
        class_start = text.index("\nCLASS ")
        location = text.index("dual=", class_start)
        corrupted = text[:location] + text[location:].replace("dual=", "dual=0,", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            path.write_text(corrupted, encoding="ascii")
            with self.assertRaises(ValueError):
                verify(path, HERE / "obstructions.txt")


if __name__ == "__main__":
    unittest.main()
