import unittest
from fractions import Fraction
from itertools import product

from verify_symbolic_prefix import (
    affine_offset,
    check_rotation_bridge,
    prefix_cap,
    upper_christoffel_word,
    verify,
)


class SymbolicPrefixTests(unittest.TestCase):
    def test_affine_offsets(self) -> None:
        self.assertEqual(affine_offset((0, 1)), 2)
        self.assertEqual(affine_offset((1, 0)), 1)
        self.assertEqual(affine_offset((1, 1, 0)), 5)

    def test_prefix_caps_depend_on_orientation(self) -> None:
        self.assertEqual(prefix_cap((0, 1)), Fraction(0))
        self.assertEqual(prefix_cap((1, 0)), Fraction(1))

    def test_rotation_bridge_through_length_eight(self) -> None:
        for length in range(1, 9):
            for word in product((0, 1), repeat=length):
                if 3 ** sum(word) < 2**length:
                    check_rotation_bridge(word)

    def test_upper_christoffel_examples(self) -> None:
        self.assertEqual(upper_christoffel_word(2, 1), (1, 0))
        self.assertEqual(upper_christoffel_word(5, 3), (1, 1, 0, 1, 0))

    def test_exhaustive_small_report(self) -> None:
        report = verify(max_length=8, rotation_check_length=8)
        self.assertEqual(report["max_length"], 8)
        self.assertGreater(report["parameter_pairs"], 0)
        self.assertGreater(report["words_checked"], 0)


if __name__ == "__main__":
    unittest.main()
