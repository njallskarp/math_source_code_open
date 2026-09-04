#!/usr/bin/env python3

import unittest

import verify


class CoverReversalTests(unittest.TestCase):
    def test_first_pair(self) -> None:
        row = verify.audit_pair(6, 1)
        self.assertEqual(row[2], 7)
        self.assertEqual(row[-2:], [130, 130])

    def test_first_noncoatom_pair(self) -> None:
        row = verify.audit_pair(8, 2)
        self.assertEqual(row[2], 10)
        self.assertEqual(row[-2], 3534)
        self.assertGreater(row[-2], row[-1])

    def test_paths_are_distinct_and_valid(self) -> None:
        p, q = verify.path_p(12, 3), verify.path_q(12, 3)
        self.assertNotEqual(p, q)
        self.assertTrue(verify.is_rational_dyck(p, 15))
        self.assertTrue(verify.is_rational_dyck(q, 15))

    def test_invalid_parameters_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify.audit_pair(6, 2)

    def test_matrix_and_literal_matching_agree(self) -> None:
        for x, y in ((6, 1), (8, 2), (11, 3), (20, 5)):
            self.assertEqual(
                verify.matching_number(verify.path_p(x, y)),
                verify.q_score((x, y, 0)),
            )
            self.assertEqual(
                verify.matching_number(verify.path_q(x, y)),
                verify.q_score((x - 1, 0, y + 1)),
            )


if __name__ == "__main__":
    unittest.main()
