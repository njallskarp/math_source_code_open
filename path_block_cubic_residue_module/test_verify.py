"""Unit tests for the cubic endpoint residue module."""

from __future__ import annotations

import unittest

import verify


class CubicResidueModuleTests(unittest.TestCase):
    def test_quotient_ring(self) -> None:
        ring = {verify.reduce_pair(a, b) for a in range(9) for b in range(9)}
        self.assertEqual(len(ring), 27)
        self.assertEqual(verify.ring_power(verify.PI, 3), verify.ZERO)
        self.assertEqual(verify.scale(verify.ONE, 9), verify.ZERO)

    def test_generator_presentation(self) -> None:
        g1, h2, h4, g0 = verify.basis_generators()
        self.assertEqual(verify.pair_power(g1, 27), verify.IDENTITY_PAIR)
        self.assertEqual(verify.pair_power(h2, 3), verify.IDENTITY_PAIR)
        self.assertEqual(verify.pair_power(h4, 3), verify.IDENTITY_PAIR)
        self.assertEqual(verify.pair_power(g0, 9), verify.IDENTITY_PAIR)
        self.assertEqual(len(set(verify.all_normal_forms())), 2187)

    def test_nonrectangular_same_signature_pair(self) -> None:
        left = (6, 5, 1)
        right = (7, 3, 2)
        self.assertEqual(verify.endpoint_signature(left), verify.endpoint_signature(right))
        self.assertEqual(verify.direct_gamma(left), verify.direct_gamma(right))

    def test_transform_period(self) -> None:
        gamma = verify.direct_gamma((21, 14, 8, 4, 2, 1))
        for side in (0, 1):
            for order in range(6, 15):
                self.assertEqual(
                    verify.transform(gamma[side], order),
                    verify.transform(gamma[side], order + 9),
                )

    def test_height_2095_associated_graded_layer(self) -> None:
        left, right = verify.family()
        left_jet = verify.rational_jet(verify.endpoint_signature(left), 14)
        right_jet = verify.rational_jet(verify.endpoint_signature(right), 14)
        difference = tuple(
            verify.add(a, verify.neg(b)) for a, b in zip(left_jet, right_jet, strict=True)
        )
        expected = (verify.ZERO,) * 3 + (verify.mul(verify.PI, verify.PI),) + (
            verify.ZERO,
        ) * 10
        self.assertEqual(difference, expected)


if __name__ == "__main__":
    unittest.main()
