#!/usr/bin/env python3

import unittest
from fractions import Fraction

import independent_matrix_audit as audit


class CleanRoomAuditTests(unittest.TestCase):
    def test_complete_small_carrier(self) -> None:
        self.assertEqual(audit.carrier(4), [(2, 1, 1), (2, 2, 0), (3, 0, 1), (3, 1, 0), (4, 0, 0)])

    def test_continued_fraction_numerator(self) -> None:
        self.assertEqual(audit.matching_number((5, 1, 1)), 2989)
        self.assertEqual(audit.matching_number((4, 0, 2)), 1288)

    def test_fixed_point_gap_is_exact(self) -> None:
        score = audit.lagrange_square((5, 1, 1))
        self.assertIsInstance(score, Fraction)
        self.assertEqual(score, Fraction(1676285, 182329))

    def test_first_endpoint_counts(self) -> None:
        paths, reversals, diagonal, rows = audit.audit_endpoint(7)
        self.assertEqual((paths, reversals, diagonal, len(rows)), (12, 1, 1, 2))
        self.assertGreater(rows[0][8], 0)
        self.assertLess(rows[1][8], 0)

    def test_scope_rejection(self) -> None:
        with self.assertRaises(ValueError):
            audit.audit_endpoint(9)

    def test_exhaustive_small_range(self) -> None:
        endpoints, paths, reversals, diagonal, digest = audit.audit(18)
        self.assertEqual((endpoints, paths, reversals, diagonal), (8, 258, 40, 20))
        self.assertEqual(len(digest), 64)


if __name__ == "__main__":
    unittest.main()
