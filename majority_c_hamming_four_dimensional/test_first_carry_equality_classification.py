#!/usr/bin/env python3
"""Unit tests for verify_first_carry_equality_classification.py."""

from __future__ import annotations

import unittest

import verify_first_carry_equality_classification as verify


class FirstCarryEqualityClassificationTests(unittest.TestCase):
    def test_short_thin_construction(self) -> None:
        parts = verify.construct_short_thin_factor(7, 9, 10)
        stats = verify.validate_partition(7, (9, 10, 2), parts)
        self.assertEqual(stats["nonlinear_parts"], 1)
        self.assertEqual(stats["parts"], 25)

    def test_long_thin_construction(self) -> None:
        parts = verify.construct_long_thin_factor(7, 8, 9)
        stats = verify.validate_partition(7, (8, 9, 6), parts)
        self.assertEqual(stats["nonlinear_parts"], 1)
        self.assertEqual(stats["parts"], 61)

    def test_original_222_case(self) -> None:
        parts = verify.construct_short_thin_factor(5, 7, 7)
        stats = verify.validate_partition(5, (7, 7, 2), parts)
        self.assertEqual(stats["parts"], 19)

    def test_excluded_middle_orientation(self) -> None:
        self.assertEqual(verify.admissible_orientations(7, 2, 2, 3), ())

    def test_two_classified_orientation_types(self) -> None:
        short = verify.admissible_orientations(7, 2, 3, 2)
        long = verify.admissible_orientations(7, 1, 2, 6)
        self.assertEqual(set(short), {(0, 2), (1, 2)})
        self.assertEqual(set(long), {(2, 0), (2, 1)})

    def test_s3_overlap(self) -> None:
        orientations = verify.admissible_orientations(3, 1, 2, 2)
        self.assertEqual(len(orientations), 4)
        self.assertTrue(verify.predicted(3, 1, 2, 2))

    def test_prism_recognition(self) -> None:
        prism = tuple((x, 0, z) for x in range(6) for z in range(2))
        self.assertTrue(verify.is_prism(prism, 7))
        self.assertFalse(verify.is_prism(prism[:-1], 7))

    def test_bounded_orientation_audit(self) -> None:
        audit = verify.audit_orientations(40)
        self.assertGreater(audit["constructive"], 0)
        self.assertGreater(audit["excluded"], 0)

    def test_invalid_parameters_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify.construct_short_thin_factor(7, 9, 9)
        with self.assertRaises(ValueError):
            verify.construct_long_thin_factor(7, 9, 10)


if __name__ == "__main__":
    unittest.main()
