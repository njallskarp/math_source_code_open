#!/usr/bin/env python3

import unittest

import independent_check


def path(runs: tuple[int, int, int]) -> tuple[str, ...]:
    r, s, t = runs
    return tuple("R" * r + "U" + "R" * s + "U" + "R" * t + "U")


class IndependentDefinitionTests(unittest.TestCase):
    def test_first_reversal_scores(self) -> None:
        self.assertEqual(independent_check.matching_score(path((6, 1, 0))), 3241)
        self.assertEqual(independent_check.matching_score(path((5, 0, 2))), 3371)

    def test_lagrange_fibre_collision(self) -> None:
        self.assertEqual(
            independent_check.lagrange_square(path((5, 0, 2))),
            independent_check.lagrange_square(path((5, 2, 0))),
        )

    def test_small_endpoint_census(self) -> None:
        paths, levels, within, inter, reversals, rows = independent_check.check_endpoint(7)
        self.assertEqual((paths, levels, within, inter, reversals, len(rows)), (12, 8, 5, 2, 1, 17))

    def test_run_decoder(self) -> None:
        for runs in ((6, 1, 0), (5, 0, 2), (3, 2, 0), (3, 1, 1)):
            self.assertEqual(independent_check.run_triple(path(runs)), runs)


if __name__ == "__main__":
    unittest.main()
