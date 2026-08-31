#!/usr/bin/env python3

import unittest
from fractions import Fraction

from verify_published_bound import (
    LOWER,
    PREVIOUS_UPPER,
    TARGET,
    certify,
    log_bounds,
)


class PublishedBoundCertificateTests(unittest.TestCase):
    def test_log_intervals_are_nested_when_refined(self) -> None:
        for x in (Fraction(2), Fraction(3)):
            coarse_lo, coarse_hi = log_bounds(x, 80)
            fine_lo, fine_hi = log_bounds(x, 120)
            self.assertLessEqual(coarse_lo, fine_lo)
            self.assertLessEqual(fine_lo, fine_hi)
            self.assertLessEqual(fine_hi, coarse_hi)

    def test_farey_neighbor_identities(self) -> None:
        self.assertEqual(
            TARGET.numerator * LOWER.denominator
            - LOWER.numerator * TARGET.denominator,
            1,
        )
        self.assertEqual(
            PREVIOUS_UPPER.numerator * TARGET.denominator
            - TARGET.numerator * PREVIOUS_UPPER.denominator,
            1,
        )

    def test_published_bounds(self) -> None:
        result = certify()
        self.assertEqual(result["minimum_odd_entries"], 137_528_045_312)
        self.assertEqual(result["minimum_shortcut_entries"], 217_976_794_617)
        self.assertEqual(result["minimum_classical_entries"], 355_504_839_929)


if __name__ == "__main__":
    unittest.main()
