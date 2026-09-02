#!/usr/bin/env python3
"""Regression tests for the clause-genealogy overlap-debt checker."""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import unittest


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_clause_genealogy_overlap",
    HERE / "verify_clause_genealogy_overlap.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ClauseGenealogyOverlapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((HERE / "clause-genealogy-overlap-certificate.json").read_text())

    def test_certificate(self) -> None:
        counts = MODULE.verify_certificate(copy.deepcopy(self.data))
        self.assertEqual(counts["local_cases"], 16807)
        self.assertEqual(counts["tree_shapes"], 6918)
        self.assertEqual(counts["threshold_cases"], 1533)
        self.assertEqual(counts["parameter_pairs"], 380)

    def test_wrong_leaf_length_rejected(self) -> None:
        corrupted = copy.deepcopy(self.data)
        corrupted["claim"]["leaf_clause_length"] = 5
        with self.assertRaises(AssertionError):
            MODULE.verify_certificate(corrupted)

    def test_wrong_tree_count_rejected(self) -> None:
        corrupted = copy.deepcopy(self.data)
        corrupted["tree_audit"]["ordered_full_binary_tree_shapes"] += 1
        with self.assertRaises(AssertionError):
            MODULE.verify_certificate(corrupted)


if __name__ == "__main__":
    unittest.main()
