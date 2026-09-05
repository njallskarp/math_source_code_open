#!/usr/bin/env python3
"""Mutation and boundary tests for verify_cross_boundary_222.py."""

from __future__ import annotations

import unittest

import verify_cross_boundary_222 as verifier


class CrossBoundary222Tests(unittest.TestCase):
    def test_base_certificate(self) -> None:
        sides, parts = verifier.construct(1, 1)
        self.assertEqual(
            verifier.validate(1, 1, sides, parts),
            {"parts": 19, "line_parts": 18, "nonlinear_parts": 1, "cells": 98},
        )

    def test_translated_core(self) -> None:
        sides, parts = verifier.construct(3, 2)
        stats = verifier.validate(3, 2, sides, parts)
        self.assertEqual(stats["parts"], 81)
        self.assertEqual(stats["cells"], 408)

    def test_invalid_parameters(self) -> None:
        with self.assertRaises(ValueError):
            verifier.construct(0, 1)

    def test_missing_cell_rejected(self) -> None:
        sides, parts = verifier.construct(1, 1)
        mutated = list(parts)
        mutated[0] = mutated[0][:-1]
        with self.assertRaises(AssertionError):
            verifier.validate(1, 1, sides, mutated)

    def test_wrong_owner_rejected(self) -> None:
        sides, parts = verifier.construct(1, 1)
        mutated = list(parts)
        mutated[1] = mutated[1][:-1] + (mutated[2][0],)
        with self.assertRaises(AssertionError):
            verifier.validate(1, 1, sides, mutated)


if __name__ == "__main__":
    unittest.main()
