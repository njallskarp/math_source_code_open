#!/usr/bin/env python3
"""Tamper-rejection tests for the exceptional-ray residue certificate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from verify_residues import verify

HERE = Path(__file__).resolve().parent


class ResidueProfileTests(unittest.TestCase):
    def run_verify(self, profiles: Path) -> str:
        return verify(HERE / "certificate.txt", profiles)

    def with_corruption(self, text: str) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_residues.txt"
            path.write_text(text, encoding="ascii")
            with self.assertRaises(ValueError):
                self.run_verify(path)

    def test_committed_certificate(self) -> None:
        output = self.run_verify(HERE / "residue_profiles.txt")
        expected = (HERE / "EXPECTED_RESIDUE_OUTPUT.txt").read_text(encoding="ascii").strip()
        self.assertEqual(output, expected)

    def test_duplicate_order_is_rejected(self) -> None:
        lines = (HERE / "residue_profiles.txt").read_text(encoding="ascii").splitlines()
        fields = lines[2].split("profile=", 1)
        terms = fields[1].split(",")
        terms[0] = terms[1]
        lines[2] = fields[0] + "profile=" + ",".join(terms)
        self.with_corruption("\n".join(lines) + "\n")

    def test_declared_deficit_tamper_is_rejected(self) -> None:
        text = (HERE / "residue_profiles.txt").read_text(encoding="ascii")
        self.with_corruption(text.replace(" deficit=4 ", " deficit=3 ", 1))

    def test_missing_profile_is_rejected(self) -> None:
        lines = (HERE / "residue_profiles.txt").read_text(encoding="ascii").splitlines()
        self.with_corruption("\n".join(lines[:-1]) + "\n")


if __name__ == "__main__":
    unittest.main()
