#!/usr/bin/env python3
"""Regression tests for the genealogical four-incidence certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import unittest


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_genealogical_four_incidence_cut",
    HERE / "verify_genealogical_four_incidence_cut.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GenealogicalFourIncidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(
            (HERE / "genealogical-four-incidence-cut-certificate.json").read_text()
        )

    def test_certificate(self) -> None:
        result = MODULE.verify(copy.deepcopy(self.data))
        self.assertEqual(result["root_clause"], (1, 2, 3))
        self.assertEqual(result["bichromatic_edges"], 4)
        self.assertEqual(result["four_incidence_cuts"], 3)
        self.assertEqual(result["monochromatic_k5"], 0)

    def test_broken_resolution_rejected(self) -> None:
        corrupted = copy.deepcopy(self.data)
        corrupted["resolutions"][1]["pivot"] = -6
        with self.assertRaises(AssertionError):
            MODULE.verify(corrupted)

    def test_opposite_color_double_intersection_rejected(self) -> None:
        corrupted = copy.deepcopy(self.data)
        corrupted["leaves"][1]["clause"] = [-3, -4, -5, -6]
        with self.assertRaises(AssertionError):
            MODULE.verify(corrupted)


if __name__ == "__main__":
    unittest.main()
