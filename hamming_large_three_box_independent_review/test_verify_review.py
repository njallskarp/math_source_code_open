#!/usr/bin/env python3
"""Boundary and negative tests for the independent three-box audit."""

from itertools import permutations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_review


class IndependentReviewTests(unittest.TestCase):
    def test_first_positive_carry(self) -> None:
        # mn=20=3*6+2 and p=3+2, so the two-by-two residual product
        # creates one carry and leaves one large part.
        self.assertEqual(verify_review.verify_box(4, 5, 5, 3), (33, 100, 1, 1))

    def test_maximum_carry_boundary(self) -> None:
        # tau=c=s-1 realizes floor((s-1)^2/s)=s-2 exchanges.
        self.assertEqual(verify_review.verify_box(8, 13, 13, 7), (193, 1352, 1, 5))

    def test_axis_permutations(self) -> None:
        for dimensions in set(permutations((5, 7, 8))):
            result = verify_review.verify_box(*dimensions, 4)
            self.assertEqual(result[0], 70)
            self.assertEqual(result[1], 280)

    def test_shifted_anchor_columns(self) -> None:
        certificate = verify_review.rectangle_certificate(8, 9, 5, shift=7)
        self.assertEqual(set(certificate.large_label_by_column), {7, 8})
        for column, label in certificate.large_label_by_column.items():
            self.assertIn((certificate.anchor_row, column), certificate.parts[label])
        self.assertEqual(verify_review.verify_rectangle(8, 9, 5, shift=7), (14, 72, 2))

    def test_missing_cell_is_rejected(self) -> None:
        parts = verify_review.box_certificate(4, 5, 5, 3)
        first_label = next(iter(parts))
        parts[first_label].pop()
        with self.assertRaises(AssertionError):
            verify_review.validate_partition(parts, (4, 5, 5), 3)

    def test_family_remainder_is_k(self) -> None:
        for k in range(3, 30):
            s = k * k - k
            quotient, remainder = divmod(k**6, s)
            self.assertEqual(quotient, k**4 + k**3 + k**2 + k + 1)
            self.assertEqual(remainder, k)

    def test_invalid_dimensions_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify_review.rectangle_certificate(2, 3, 3)
        with self.assertRaises(ValueError):
            verify_review.box_certificate(3, 4, 2, 3)


if __name__ == "__main__":
    unittest.main()
