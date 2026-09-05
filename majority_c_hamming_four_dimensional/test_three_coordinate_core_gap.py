#!/usr/bin/env python3
"""Unit tests for verify_three_coordinate_core_gap.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_three_coordinate_core_gap as verify


class ThreeCoordinateCoreGapTests(unittest.TestCase):
    def test_six_cycle_is_sharp(self) -> None:
        cells = verify.vertices((2, 2, 2))
        chosen = tuple(cell for cell in cells if cell not in ((0, 0, 0), (1, 1, 1)))
        mask = verify.mask_for(cells, chosen)
        adjacency = verify.neighbor_masks(cells)
        self.assertEqual(verify.minimum_degree(mask, adjacency), 2)
        self.assertEqual(verify.support_dimension(mask, cells), 3)
        self.assertEqual(mask.bit_count(), 2 * 2 + 2)

    def test_cube_is_sharp(self) -> None:
        cells = verify.vertices((2, 2, 2))
        mask = (1 << len(cells)) - 1
        self.assertEqual(verify.minimum_degree(mask, verify.neighbor_masks(cells)), 3)
        self.assertEqual(verify.support_dimension(mask, cells), 3)

    def test_grid_is_two_dimensional_control(self) -> None:
        cells = verify.vertices((3, 3))
        mask = (1 << len(cells)) - 1
        self.assertEqual(verify.minimum_degree(mask, verify.neighbor_masks(cells)), 4)
        self.assertEqual(mask.bit_count(), 2 * 4 + 1)
        self.assertEqual(verify.support_dimension(mask, cells), 2)

    def test_shell_profiles(self) -> None:
        self.assertEqual(set(verify.feasible_shell_profiles(3)), verify.expected_profiles(3))
        self.assertEqual(set(verify.feasible_shell_profiles(4)), verify.expected_profiles(4))
        self.assertEqual(set(verify.feasible_shell_profiles(9)), {(8, 1)})

    def test_small_host_audit(self) -> None:
        result = verify.audit_hosts(((2, 2, 2), (3, 2, 2)))
        self.assertGreater(result["three_coordinate_cores"], 0)
        self.assertGreater(result["equality"], 0)

    def test_empty_mask_rejected(self) -> None:
        cells = verify.vertices((2, 2, 2))
        with self.assertRaises(ValueError):
            verify.minimum_degree(0, verify.neighbor_masks(cells))


if __name__ == "__main__":
    unittest.main()
