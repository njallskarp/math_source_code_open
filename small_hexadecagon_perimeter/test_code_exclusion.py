#!/usr/bin/env python3

import unittest
from fractions import Fraction

from verify_code_exclusion_arb import verify as verify_arb
from verify_code_exclusion_exact import (
    code_from_bits,
    dihedral_orbit,
    sine_interval_wide,
    sqrt_interval,
    verify as verify_exact,
)
from verify_code_exclusion_identities import verify as verify_identities


class CodeExclusionTests(unittest.TestCase):
    def test_dependency_free_exact_certificate(self) -> None:
        result = verify_exact()
        self.assertTrue(result["exact_certificate"])
        self.assertEqual(result["spectral_screen_survivors"], 16)

    def test_independent_arb_certificate(self) -> None:
        result = verify_arb()
        self.assertTrue(result["arb_certificate"])
        self.assertEqual(result["spectral_screen_survivors"], 16)

    def test_exact_symbolic_identities(self) -> None:
        self.assertTrue(verify_identities()["exact_symbolic_identities"])

    def test_code_normalization(self) -> None:
        self.assertEqual(code_from_bits(0), (1,) * 16)
        self.assertEqual(code_from_bits((1 << 15) - 1), (1,) + (-1,) * 15)

    def test_dihedral_orbit(self) -> None:
        representative = tuple(1 if char == "+" else -1 for char in "+--+-++-+--+-++-")
        orbit = dihedral_orbit(representative)
        self.assertEqual(len(orbit), 16)
        self.assertTrue(all(code[0] == 1 for code in orbit))

    def test_interval_helpers_reject_bad_input(self) -> None:
        with self.assertRaises(ValueError):
            sine_interval_wide(Fraction(-1), Fraction(0), 10)
        with self.assertRaises(ValueError):
            sqrt_interval(Fraction(-1), 10)


if __name__ == "__main__":
    unittest.main()
