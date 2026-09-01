#!/usr/bin/env python3

import unittest

from reconstruct_candidate import reconstruct
from verify_local_certificate import verify


class LocalCertificateTests(unittest.TestCase):
    def test_independent_reconstruction(self) -> None:
        _, _, residual, iterations = reconstruct()
        self.assertLess(float(residual), 1e-140)
        self.assertLess(iterations, 10)

    def test_arb_certificate(self) -> None:
        result = verify()
        self.assertTrue(result["krawczyk_strict_inclusion"])
        self.assertEqual(result["ldl_pivot_signs"], "+" * 15 + "--")
        self.assertTrue(result["angle_gaps_strictly_positive"])


if __name__ == "__main__":
    unittest.main()
