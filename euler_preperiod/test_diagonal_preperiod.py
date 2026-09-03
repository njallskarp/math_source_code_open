#!/usr/bin/env python3

import unittest

from verify_diagonal_preperiod import (
    criterion_class,
    euler_up_down,
    primes_up_to,
    theorem_class,
    valuation,
    verify,
)


class DiagonalPreperiodTests(unittest.TestCase):
    def test_entringer_initial_values(self) -> None:
        self.assertEqual(
            euler_up_down(10),
            [1, 1, 1, 2, 5, 16, 61, 272, 1385, 7936, 50521],
        )

    def test_prime_sieve(self) -> None:
        self.assertEqual(primes_up_to(20), [3, 5, 7, 11, 13, 17, 19])

    def test_valuation(self) -> None:
        self.assertEqual(valuation(3**4 * 10, 3), 4)
        self.assertEqual(valuation(2**10 - 1, 3), 1)

    def test_small_diagonal_classes(self) -> None:
        values = euler_up_down(50)
        self.assertEqual(criterion_class(3, values), "p")
        self.assertEqual(theorem_class(3, values), "p")
        self.assertEqual(criterion_class(5, values), "p-1")
        self.assertEqual(theorem_class(5, values), "p-1")
        self.assertEqual(criterion_class(7, values), "p")
        self.assertEqual(theorem_class(7, values), "p")

    def test_finite_regression(self) -> None:
        record = verify(200)
        self.assertEqual(record["prime_count"], 45)
        self.assertEqual(record["endpoint_checks"], 45)
        self.assertEqual(record["valuation_checks"], 45)
        self.assertEqual(record["classification_checks"], 45)


if __name__ == "__main__":
    unittest.main()
