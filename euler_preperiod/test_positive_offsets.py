#!/usr/bin/env python3

import unittest

from verify_positive_offsets import (
    OFFSET_LIMIT,
    euler_up_down,
    factorization,
    predicted_preperiod,
    secant_even_mod,
    top_two_criterion,
    verify,
)


class PositiveOffsetTests(unittest.TestCase):
    def test_initial_values_and_gcd_frontier(self) -> None:
        values = euler_up_down(13)
        self.assertEqual(
            values,
            [
                1,
                1,
                1,
                2,
                5,
                16,
                61,
                272,
                1385,
                7936,
                50521,
                353792,
                2702765,
                22368256,
            ],
        )
        import math

        self.assertTrue(
            all(math.gcd(values[t - 1], values[t]) == 1 for t in range(1, 13))
        )
        self.assertEqual(math.gcd(values[12], values[13]), 43)

    def test_factorization(self) -> None:
        self.assertEqual(factorization(1), [])
        self.assertEqual(factorization(50521), [[19, 1], [2659, 1]])
        self.assertEqual(
            factorization(2702765), [[5, 1], [13, 1], [43, 1], [967, 1]]
        )
        self.assertEqual(
            factorization(22368256), [[2, 12], [43, 1], [127, 1]]
        )

    def test_known_offset_exceptions(self) -> None:
        values = euler_up_down(100)
        self.assertEqual(predicted_preperiod(5, 4, values), 8)
        self.assertEqual(top_two_criterion(5, 9, values), 8)
        self.assertEqual(predicted_preperiod(61, 6, values), 66)
        self.assertEqual(top_two_criterion(61, 67, values), 66)
        self.assertEqual(predicted_preperiod(17, 7, values), 23)
        self.assertEqual(top_two_criterion(17, 24, values), 23)

    def test_exceptional_p2_lift_two_recurrences(self) -> None:
        values = euler_up_down(56)
        self.assertEqual(values[54] % (43 * 43), 774)
        self.assertEqual(secant_even_mod(54, 43 * 43)[54], 774)
        self.assertEqual(top_two_criterion(43, 56, values), 55)

    def test_invalid_offset(self) -> None:
        values = euler_up_down(20)
        with self.assertRaises(ValueError):
            predicted_preperiod(5, 0, values)
        with self.assertRaises(ValueError):
            predicted_preperiod(5, OFFSET_LIMIT + 1, values)

    def test_finite_regression(self) -> None:
        record = verify(200)
        self.assertEqual(record["prime_count"], 45)
        self.assertEqual(record["classification_checks"], 45 * OFFSET_LIMIT)
        self.assertEqual(record["shift_congruence_checks"], 45 * 25)
        self.assertEqual(
            record["exceptional_p2_lift"]["residue"], 774
        )


if __name__ == "__main__":
    unittest.main()
