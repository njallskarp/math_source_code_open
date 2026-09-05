#!/usr/bin/env python3
"""Tamper-rejection tests for the scale-six G8 certificate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from verify_m6 import verify

HERE = Path(__file__).resolve().parent


class ScaleSixTests(unittest.TestCase):
    def run_verify(self, profiles: Path, maps: Path) -> str:
        return verify(HERE / "certificate.txt", profiles, maps)

    def test_committed_certificate(self) -> None:
        output = self.run_verify(HERE / "m6_profiles.txt", HERE / "g8_maps.txt")
        self.assertIn("exact_ray=m(6qT)=7q_for_all_q>=1", output)

    def test_profile_tamper_is_rejected(self) -> None:
        text = (HERE / "m6_profiles.txt").read_text(encoding="ascii")
        start = text.index("\nCLASS ")
        location = text.index("profile=", start) + len("profile=")
        term_end = text.index(",", location)
        order, multiplicity = text[location:term_end].split(":")
        corrupted = text[:location] + f"{order}:{int(multiplicity) + 1}" + text[term_end:]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_profiles.txt"
            path.write_text(corrupted, encoding="ascii")
            with self.assertRaises(ValueError):
                self.run_verify(path, HERE / "g8_maps.txt")

    def test_map_tamper_is_rejected(self) -> None:
        text = (HERE / "g8_maps.txt").read_text(encoding="ascii")
        start = text.index("\nSUPPORT ")
        location = text.index("g8_to_t=", start) + len("g8_to_t=")
        values = text[location:text.index("\n", location)].split(",")
        values[0], values[1] = values[1], values[0]
        corrupted = text[:location] + ",".join(values) + text[text.index("\n", location):]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_maps.txt"
            path.write_text(corrupted, encoding="ascii")
            with self.assertRaises(ValueError):
                self.run_verify(HERE / "m6_profiles.txt", path)


if __name__ == "__main__":
    unittest.main()
