#!/usr/bin/env python3

import unittest

import verify


class AdjacentFibreOrientationTests(unittest.TestCase):
    def test_positive_h_orientations(self) -> None:
        self.assertEqual(verify.valid_orientations((6, 3, 1), 10), ((6, 3, 1), (6, 1, 3)))

    def test_negative_h_orientations(self) -> None:
        self.assertEqual(verify.valid_orientations((5, 3, 0), 8), ((5, 3, 0), (3, 5, 0)))

    def test_first_reversal_is_unique_cross_pair(self) -> None:
        rows = verify.audit_within_transition((6, 1, 0), (5, 2, 0), 7)
        reversed_rows = [row for row in rows if row[-1]]
        self.assertEqual(len(reversed_rows), 1)
        self.assertEqual(reversed_rows[0][4:7], [[6, 1, 0], [5, 0, 2], 130])

    def test_diagonal_agreement(self) -> None:
        rows = verify.audit_within_transition((5, 1, 1), (4, 2, 1), 7)
        self.assertFalse(any(row[-1] for row in rows))
        special = [row for row in rows if row[5] == [4, 1, 2]][0]
        self.assertEqual(special[6], -36)

    def test_low_h_transition_has_only_agreements(self) -> None:
        rows = verify.audit_within_transition((3, 1, 0), (2, 2, 0), 4)
        self.assertFalse(any(row[-1] for row in rows))

    def test_negative_h_transition_has_only_agreements(self) -> None:
        rows = verify.audit_within_transition((5, 3, 0), (4, 4, 0), 8)
        self.assertFalse(any(row[-1] for row in rows))

    def test_even_inter_layer_agrees(self) -> None:
        rows = verify.audit_inter_transition((2, 2, 0), (2, 1, 1), 4)
        self.assertEqual(len(rows), 1)
        self.assertLess(rows[0][6], 0)

    def test_odd_inter_layer_agrees_for_both_upper_orders(self) -> None:
        rows = verify.audit_inter_transition((3, 2, 0), (3, 1, 1), 5)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row[6] < 0 for row in rows))


if __name__ == "__main__":
    unittest.main()
