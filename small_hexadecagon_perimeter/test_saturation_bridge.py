#!/usr/bin/env python3

import unittest
from fractions import Fraction

from verify_saturation_bounds_arb import verify as verify_arb
from verify_saturation_bounds_symbolic import cos_interval, verify as verify_symbolic
from verify_saturation_cases import (
    closure_coefficients,
    half_edge_derivatives,
    verify as verify_cases,
)
from verify_saturation_identities import verify as verify_identities


class SaturationBridgeTests(unittest.TestCase):
    def test_exact_incidence_certificate(self) -> None:
        self.assertTrue(verify_cases()["exact_incidence_certificate"])

    def test_dependency_free_rational_certificate(self) -> None:
        self.assertTrue(verify_symbolic()["rational_certificate"])

    def test_independent_arb_certificate(self) -> None:
        self.assertTrue(verify_arb()["arb_certificate"])

    def test_exact_symbolic_identities(self) -> None:
        self.assertTrue(verify_identities()["exact_symbolic_identities"])

    def test_cyclic_endpoint_coefficient(self) -> None:
        code = (1,) * 16
        self.assertEqual(closure_coefficients(code), (-2,) + (0,) * 15)
        self.assertEqual(half_edge_derivatives((1,) * 16)[-1], -2)

    def test_cosine_checker_rejects_out_of_domain_interval(self) -> None:
        with self.assertRaises(ValueError):
            cos_interval(Fraction(-1, 10), Fraction(1, 10), 10)


if __name__ == "__main__":
    unittest.main()
