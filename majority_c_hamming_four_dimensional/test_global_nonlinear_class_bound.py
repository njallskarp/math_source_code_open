#!/usr/bin/env python3
"""Unit tests for verify_global_nonlinear_class_bound.py."""

from __future__ import annotations

import unittest

import verify_global_nonlinear_class_bound as verify


class GlobalNonlinearClassBoundTests(unittest.TestCase):
    def test_prism_recognized(self) -> None:
        cells = tuple((x, z, 0) for z in range(2) for x in range(4))
        self.assertTrue(verify.is_prism(cells, 4))

    def test_coordinate_square_recognized(self) -> None:
        cells = ((0, 0), (0, 1), (1, 0), (1, 1))
        self.assertTrue(verify.is_prism(cells, 2))

    def test_misaligned_lines_rejected(self) -> None:
        cells = ((0, 0), (1, 0), (1, 1), (2, 1))
        self.assertFalse(verify.is_prism(cells, 2))

    def test_line_containment(self) -> None:
        cells = verify.vertices((5, 3))
        lines = verify.coordinate_line_masks(cells)
        line_mask = sum(1 << cells.index((x, 1)) for x in range(5))
        self.assertTrue(verify.contained_in_line(line_mask, lines))
        line_mask |= 1 << cells.index((0, 2))
        self.assertFalse(verify.contained_in_line(line_mask, lines))

    def test_small_exhaustive_audit(self) -> None:
        result = verify.audit_small_hosts(3, 3, 12)
        self.assertGreater(result["claims"], 0)
        self.assertGreater(result["equality"], 0)

    def test_first_carry_boundary_present(self) -> None:
        result = verify.audit_first_carry(12)
        self.assertGreater(result["below"], 0)
        self.assertGreater(result["equality_illegal_tail"], 0)

    def test_invalid_prism_size_rejected(self) -> None:
        self.assertFalse(verify.is_prism(((0, 0), (1, 0), (0, 1)), 2))


if __name__ == "__main__":
    unittest.main()
