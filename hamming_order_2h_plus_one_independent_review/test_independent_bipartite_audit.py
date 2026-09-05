#!/usr/bin/env python3
"""Tests for the clean-room degree-sequence audit."""

from __future__ import annotations

import unittest

import independent_bipartite_audit as audit


class IndependentBipartiteAuditTests(unittest.TestCase):
    def test_partitions(self) -> None:
        self.assertEqual(
            tuple(audit.partitions(5)),
            ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)),
        )

    def test_known_forms_are_realizable(self) -> None:
        for h in range(2, 9):
            for left, right in audit.expected_pairs(h):
                self.assertTrue(audit.has_allowed_realization(left, right, h))

    def test_forbidden_degree_pair(self) -> None:
        self.assertFalse(audit.has_allowed_realization((3, 2, 2), (3, 2, 2), 3))

    def test_small_complete_audit(self) -> None:
        result = audit.audit(5)
        self.assertEqual(result["realizable"], 13)
        self.assertEqual(
            [record["realizable"] for record in result["summary"]],
            [3, 3, 4, 3],
        )


if __name__ == "__main__":
    unittest.main()
