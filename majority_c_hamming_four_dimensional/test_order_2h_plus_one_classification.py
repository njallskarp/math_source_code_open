#!/usr/bin/env python3
"""Unit tests for verify_order_2h_plus_one_classification.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_order_2h_plus_one_classification as verify


class OrderTwoHPlusOneClassificationTests(unittest.TestCase):
    def test_normal_forms(self) -> None:
        for h in (2, 3, 4, 7):
            for expected, cells in verify.family_instances(h).items():
                rows, columns = verify.host_size(cells)
                self.assertEqual(verify.classify_core(cells, h, rows, columns), expected)
                self.assertGreaterEqual(verify.minimum_degree(cells, rows, columns), h)

    def test_endpoint_degree_identity(self) -> None:
        cells = verify.family_instances(6)["parallel"]
        rows, columns = verify.host_size(cells)
        row_degrees, column_degrees = verify.line_degrees(cells, rows, columns)
        induced = [row_degrees[row] + column_degrees[column] - 2 for row, column in cells]
        self.assertEqual(min(induced), verify.minimum_degree(cells, rows, columns))

    def test_direction_pair_boundary(self) -> None:
        self.assertEqual(set(verify.feasible_direction_pairs(2)), {(1, 1)})
        self.assertEqual(set(verify.feasible_direction_pairs(3)), {(2, 1), (2, 2)})
        self.assertEqual(set(verify.feasible_direction_pairs(4)), {(3, 1), (2, 2)})
        self.assertEqual(set(verify.feasible_direction_pairs(12)), {(11, 1)})

    def test_small_exhaustive_audit(self) -> None:
        result = verify.audit_exhaustive(((3, 3, 2), (3, 3, 4)))
        self.assertEqual(result["subsets"], 127)
        self.assertEqual(result["cores"], 46)
        self.assertEqual(result["parallel"], 36)
        self.assertEqual(result["perpendicular"], 9)
        self.assertEqual(result["grid"], 1)

    def test_wrong_order_and_damaged_core(self) -> None:
        cells = verify.family_instances(5)["parallel"]
        rows, columns = verify.host_size(cells)
        self.assertEqual(verify.classify_core(cells[:-1], 5, rows, columns), "wrong_order")
        damaged = list(cells)
        damaged[-1] = (1, 6)
        self.assertEqual(verify.classify_core(tuple(damaged), 5, 2, 7), "not_core")

    def test_malformed_cells_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify.line_degrees((), 1, 1)
        with self.assertRaises(ValueError):
            verify.line_degrees(((0, 0), (0, 0)), 1, 1)
        with self.assertRaises(ValueError):
            verify.line_degrees(((1, 0),), 1, 1)


if __name__ == "__main__":
    unittest.main()
