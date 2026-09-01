#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

from verify_symmetry_quotient_exact import (
    antiperiodic_extension,
    code_action,
    normalized_half,
    parse_code,
    signed_half_edge,
    verify as verify_exact,
)
from verify_symmetry_quotient_sympy import verify as verify_sympy


HERE = Path(__file__).resolve().parent


class SymmetryQuotientTests(unittest.TestCase):
    def test_dependency_free_exact_certificate(self) -> None:
        result = verify_exact()
        self.assertTrue(result["exact_symmetry_quotient"])
        self.assertEqual(result["normalized_survivor_count"], 16)
        self.assertTrue(result["cyclic_orbit_already_complete"])

    def test_recorded_exact_output(self) -> None:
        recorded = json.loads(
            (HERE / "symmetry_quotient_verification_exact.json").read_text()
        )
        self.assertEqual(recorded, verify_exact())

    def test_independent_sympy_certificate(self) -> None:
        result = verify_sympy()
        self.assertTrue(result["sympy_symmetry_quotient"])
        self.assertEqual(result["symbolic_closure_identities"], 64)

    def test_recorded_sympy_output(self) -> None:
        recorded = json.loads(
            (HERE / "symmetry_quotient_verification_sympy.json").read_text()
        )
        self.assertEqual(recorded, verify_sympy())

    def test_antiperiodic_extension(self) -> None:
        half = parse_code("+--+-++-+--+-++-")
        full = antiperiodic_extension(half)
        self.assertEqual(full[16:], tuple(-entry for entry in full[:16]))

    def test_odd_shift_and_normalization(self) -> None:
        half = parse_code("+--+-++-+--+-++-")
        full = antiperiodic_extension(half)
        transformed = code_action(full, 1, False)
        normalized, multiplier = normalized_half(transformed)
        self.assertEqual(multiplier, -1)
        self.assertEqual(normalized[0], 1)

    def test_reflected_endpoint_action(self) -> None:
        half = parse_code("+--+-++-+--+-++-")
        full = antiperiodic_extension(half)
        transformed = code_action(full, 31, True)
        normalized, _ = normalized_half(transformed)
        self.assertEqual(len(normalized), 16)

    def test_signed_edge_endpoint(self) -> None:
        self.assertEqual(signed_half_edge(15), (15, 1))
        self.assertEqual(signed_half_edge(16), (0, -1))
        self.assertEqual(signed_half_edge(31), (15, -1))

    def test_bad_half_code_rejected(self) -> None:
        with self.assertRaises(ValueError):
            parse_code("+-")


if __name__ == "__main__":
    unittest.main()
