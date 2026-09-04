#!/usr/bin/env python3

import unittest

import independent_check as check


class SixClusterTests(unittest.TestCase):
    def test_quotient_orbits(self) -> None:
        self.assertEqual(len(check.quotient_orbit_representatives()), 56)

    def test_published_witness(self) -> None:
        rows = check.blowup(check.PUBLISHED_SIZES, check.published_quotient())
        check.check_tournament(rows)
        self.assertEqual(check.strong_vertices(rows), [])

    def test_transitive_fixture(self) -> None:
        rows = check.blowup((1, 1, 1, 1, 1, 1), (1 << 15) - 1)
        check.check_tournament(rows)
        self.assertTrue(check.strong_vertices(rows))

    def test_invalid_cluster(self) -> None:
        with self.assertRaises(ValueError):
            check.blowup((1, 1, 1, 1, 1, 0), 0)


if __name__ == "__main__":
    unittest.main()
