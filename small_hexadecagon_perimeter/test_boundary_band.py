#!/usr/bin/env python3

import unittest
from fractions import Fraction

from verify_boundary_band_arb import verify as verify_arb
from verify_boundary_band_symbolic import sin_interval, verify as verify_symbolic
from verify_boundary_identities import verify as verify_identities


class BoundaryBandTests(unittest.TestCase):
    def test_dependency_free_rational_certificate(self) -> None:
        self.assertTrue(verify_symbolic()["rational_certificate"])

    def test_independent_arb_certificate(self) -> None:
        self.assertTrue(verify_arb()["arb_certificate"])

    def test_exact_symbolic_identities(self) -> None:
        self.assertTrue(verify_identities()["exact_symbolic_identities"])

    def test_sine_checker_rejects_out_of_domain_interval(self) -> None:
        with self.assertRaises(ValueError):
            sin_interval(Fraction(-1, 10), Fraction(1, 10), 10)


if __name__ == "__main__":
    unittest.main()
