#!/usr/bin/env python3

import unittest

import verify


class InteriorSignRuleTests(unittest.TestCase):
    def test_first_boundary_reversal(self) -> None:
        kind, row = verify.audit_transition(7, 1, 0)
        self.assertEqual(kind, "reversal")
        self.assertEqual(row[-2:], [130, 130])

    def test_first_strict_interior_reversal(self) -> None:
        kind, row = verify.audit_transition(10, 2, 1)
        self.assertEqual(kind, "reversal")
        self.assertEqual(row[-2:], [370, 370])

    def test_diagonal_obstruction(self) -> None:
        kind, row = verify.audit_transition(7, 1, 1)
        self.assertEqual(kind, "diagonal")
        self.assertEqual(row[-2:], [-36, -36])

    def test_invalid_prefix_domain_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify.audit_transition(8, 2, 0)

    def test_literal_and_matrix_matching_agree(self) -> None:
        for a, y, z in ((7, 1, 0), (10, 2, 1), (14, 3, 2), (20, 5, 3)):
            x = a - y - z
            p, q = verify.named_paths(x, y, z)
            self.assertEqual(verify.matching_number(p), verify.q_score((x, y, z)))
            self.assertEqual(verify.matching_number(q), verify.q_score((x - 1, z, y + 1)))

    def test_count_formula_at_one_endpoint(self) -> None:
        a = 20
        n = (a - 3) // 3
        reversals = diagonal = 0
        for y in range(1, n + 1):
            for z in range(y + 1):
                kind, _ = verify.audit_transition(a, y, z)
                reversals += kind == "reversal"
                diagonal += kind == "diagonal"
        self.assertEqual(reversals, n * (n + 1) // 2)
        self.assertEqual(diagonal, n)


if __name__ == "__main__":
    unittest.main()
