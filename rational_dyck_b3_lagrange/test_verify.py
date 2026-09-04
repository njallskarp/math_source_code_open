#!/usr/bin/env python3

import json
import unittest
from fractions import Fraction
from pathlib import Path

import independent_check as independent
import verify


class SymbolicCertificateTests(unittest.TestCase):
    def test_qphi_exact_signs(self) -> None:
        self.assertEqual((27 * verify.PHI - 36).sign(), 1)
        self.assertEqual((verify.PHI - 2).sign(), -1)
        self.assertEqual(verify.QPhi(Fraction(0)).sign(), 0)

    def test_committed_certificate_recomputes(self) -> None:
        path = Path(__file__).with_name("CERTIFICATE.json")
        self.assertEqual(json.loads(path.read_text()), verify.build_certificate())

    def test_nonpositive_polynomial_is_rejected(self) -> None:
        bad = verify.Laurent.constant(-1) + verify.X
        with self.assertRaises(AssertionError):
            bad.positivity_summary()


class IndependentDefinitionTests(unittest.TestCase):
    def test_apruzzese_cong_lagrange_example(self) -> None:
        first = tuple("RRRUURURU")
        second = tuple("RRRUURRUU")
        self.assertEqual(
            independent.lagrange_square(first),
            Fraction(11390621, 1055**2),
        )
        self.assertEqual(
            independent.lagrange_square(second),
            Fraction(17**2 * 48893, 1177**2),
        )

    def test_small_endpoints(self) -> None:
        rows4 = independent.check_endpoint(4)
        rows5 = independent.check_endpoint(5)
        self.assertEqual([tuple(row[1]) for row in rows4], independent.partitions(4))
        self.assertEqual([tuple(row[1]) for row in rows5], independent.partitions(5))
        self.assertEqual(len(independent.dyck_paths(4)), 5)
        self.assertEqual(len(independent.dyck_paths(5)), 7)


if __name__ == "__main__":
    unittest.main()
