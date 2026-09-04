#!/usr/bin/env python3

import unittest

import verify


class RectangularInflationTests(unittest.TestCase):
    def test_tensor_scales_all_three_blocks(self) -> None:
        for a in range(1, 4):
            for b in range(1, 4):
                for c in range(4):
                    for k in range(1, 4):
                        self.assertEqual(
                            verify.tensor_identity(verify.rectangle_permutation(a, b, c), k),
                            verify.rectangle_permutation(k * a, k * b, k * c),
                        )

    def test_hook_content_equals_macmahon(self) -> None:
        for a in range(1, 5):
            for b in range(1, 5):
                for c in range(5):
                    self.assertEqual(
                        verify.hook_content_rectangle(a, b, a + c),
                        verify.macmahon(a, b, c),
                    )

    def test_reflection_certificate(self) -> None:
        for a in range(1, 4):
            for b in range(1, 4):
                for c in range(4):
                    for k in range(1, 5):
                        verify.verify_reflection_blocks(a, b, c, k)

    def test_simple_transpositions(self) -> None:
        for r in range(1, 10):
            w = tuple(range(r - 1)) + (r, r - 1)
            self.assertEqual(verify.upsilon_transition(w), r)
            self.assertEqual(w, verify.rectangle_permutation(1, 1, r - 1))


if __name__ == "__main__":
    unittest.main()
