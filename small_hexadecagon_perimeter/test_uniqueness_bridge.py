#!/usr/bin/env python3

import unittest
from fractions import Fraction

from verify_uniqueness_bridge_arb import verify as verify_arb
from verify_uniqueness_bridge_symbolic import (
    sqrt_interval,
    switch_set,
    verify as verify_symbolic,
)
from verify_uniqueness_identities import verify as verify_identities


class UniquenessBridgeTests(unittest.TestCase):
    def test_dependency_free_rational_certificate(self) -> None:
        result = verify_symbolic()
        self.assertTrue(result["rational_certificate"])
        self.assertEqual(result["switch_set"], [1, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15])

    def test_independent_arb_certificate(self) -> None:
        self.assertTrue(verify_arb()["arb_certificate"])

    def test_exact_symbolic_identities(self) -> None:
        self.assertTrue(verify_identities()["exact_symbolic_identities"])

    def test_square_root_interval(self) -> None:
        lower, upper = sqrt_interval(Fraction(2), 30)
        self.assertLessEqual(lower * lower, 2)
        self.assertGreater(upper * upper, 2)

    def test_square_root_rejects_negative_input(self) -> None:
        with self.assertRaises(ValueError):
            sqrt_interval(Fraction(-1), 30)

    def test_switch_set_rejects_wrong_length(self) -> None:
        with self.assertRaises(ValueError):
            switch_set("+-")


if __name__ == "__main__":
    unittest.main()
