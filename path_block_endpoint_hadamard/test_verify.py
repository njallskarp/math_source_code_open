"""Unit tests for the endpoint-Hadamard verifier."""

from __future__ import annotations

import unittest

import verify


class EndpointHadamardTests(unittest.TestCase):
    def test_definition_level_counts(self) -> None:
        self.assertEqual(verify.verify_direct_counts(), 32)

    def test_middle_cycle_type_cancels(self) -> None:
        self.assertEqual(verify.verify_middle_cancellation(maximum=12), 35)

    def test_least_width_formulas(self) -> None:
        self.assertEqual(verify.hstar_polynomial((1, 1), (1, 1)), [1, 4, 1])
        self.assertEqual(verify.hstar_polynomial((2,), (2,)), [1, 0, 1])
        self.assertIsNone(verify.hstar_polynomial((2,), (1, 1)))

    def test_rectangular_formula(self) -> None:
        for width in range(1, 9):
            for length in range(1, width + 1):
                if width % length == 0:
                    cycle_type = (length,) * (width // length)
                    self.assertEqual(
                        verify.hstar_polynomial(cycle_type, cycle_type),
                        verify.rectangular_formula(width, length),
                    )

    def test_synchronized_pole_witness(self) -> None:
        self.assertIsNone(verify.synchronized_pole_witness((3, 3, 3)))
        self.assertEqual(verify.synchronized_pole_witness((2, 1)), (1, 2, 1, 1))
        self.assertEqual(verify.synchronized_pole_witness((4, 2)), (2, 2, 1, 1))

    def test_full_report(self) -> None:
        report = verify.verify()
        self.assertEqual(report["classification_width"], 10)
        self.assertEqual(report["endpoint_pairs"], 3582)
        self.assertEqual(report["polynomial_pairs"], 27)
        self.assertEqual(report["one_sided_failures"], 128)
        self.assertEqual(report["synchronized_nonrectangular"], 2647)


if __name__ == "__main__":
    unittest.main()
