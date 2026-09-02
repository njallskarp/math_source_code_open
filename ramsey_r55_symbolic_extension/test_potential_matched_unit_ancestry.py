#!/usr/bin/env python3
"""Boundary tests for the potential-matched unit-ancestry construction."""

import unittest

from ramsey_r55_symbolic_extension.verify_potential_matched_unit_ancestry import (
    dp_reduce,
    inverse_unit_extension,
    potential,
    schedule,
    terminal_deletion_witnesses,
    terminal_formula,
    verify_parameter,
)


class PotentialMatchedUnitAncestryTests(unittest.TestCase):
    def test_schedule_extremes(self) -> None:
        self.assertEqual(schedule(3).count(4), 18)
        self.assertEqual(schedule(3).count(3), 16)
        self.assertEqual(schedule(33), [8, 8, 7, 7])

    def test_schedule_charge(self) -> None:
        for p in range(3, 34):
            self.assertEqual(sum(m - 1 for m in schedule(p)), 92 - 2 * p)

    def test_one_inverse_step_and_witnesses(self) -> None:
        p = 5
        terminal = terminal_formula(p)
        extended, _, _ = inverse_unit_extension(
            terminal,
            terminal_deletion_witnesses(p),
            p + 1,
            tuple(sorted(terminal, key=lambda c: (len(c), tuple(sorted(c))))[:4]),
        )
        self.assertEqual(dp_reduce(extended, p + 1), terminal)
        self.assertEqual(potential(extended) - potential(terminal), 3)

    def test_full_boundary_parameters(self) -> None:
        for p in (3, 17, 33):
            record = verify_parameter(p)
            self.assertEqual(record["steps"], 42 - p)
            self.assertEqual(record["initial_potential"], 88)


if __name__ == "__main__":
    unittest.main()
