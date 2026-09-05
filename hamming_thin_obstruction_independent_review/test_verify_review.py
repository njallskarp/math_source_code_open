#!/usr/bin/env python3
"""Unit tests for the independent thin-obstruction checker."""

from __future__ import annotations

import unittest

from verify_review import (
    assign,
    balanced_rectangle_owner,
    bipartite_incidence,
    check_balanced_rectangle,
    check_hamming_family,
    check_thin_box,
    invert_owner,
    line_axis,
)


class ReviewTests(unittest.TestCase):
    def test_flow_realizes_nonnegligible_exception(self) -> None:
        # s=6,a=5,b=1 has rho=4: four corner rows must be large.
        parts, cells, large = check_balanced_rectangle(11, 7, 6)
        self.assertEqual((parts, cells, large), (12, 77, 5))

    def test_transposed_rectangle(self) -> None:
        left = sorted(len(part) for part in invert_owner(balanced_rectangle_owner(8, 13, 5)).values())
        right = sorted(len(part) for part in invert_owner(balanced_rectangle_owner(13, 8, 5)).values())
        self.assertEqual(left, right)

    def test_thin_positive_deficit(self) -> None:
        parts, cells, deficit = check_thin_box(5, 4, 2, 3)
        self.assertEqual((parts, cells, deficit), (12, 40, 1))

    def test_base_hamming_separation(self) -> None:
        self.assertEqual(check_hamming_family(3, full_lift=True), (13, 12, 4))

    def test_flow_rejects_impossible_degrees(self) -> None:
        with self.assertRaises(AssertionError):
            bipartite_incidence([3, 1], [2, 2, 0])

    def test_owner_rejects_duplicate_cell(self) -> None:
        owner: dict[tuple[int, ...], tuple[object, ...]] = {}
        assign(owner, ("first",), [(0, 0), (0, 1)])
        with self.assertRaises(AssertionError):
            assign(owner, ("second",), [(0, 1), (1, 1)])

    def test_line_checker_rejects_rectangle(self) -> None:
        with self.assertRaises(AssertionError):
            line_axis(((0, 0), (0, 1), (1, 1)))


if __name__ == "__main__":
    unittest.main()
