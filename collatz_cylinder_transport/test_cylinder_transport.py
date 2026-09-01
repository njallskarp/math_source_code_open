import unittest
from fractions import Fraction

from verify_cylinder_transport import (
    affine_offset,
    cylinder_base,
    lifted_pair,
    prefix_cap,
    upper_christoffel_word,
    verify_christoffel_gap,
    verify_transport,
)


class CylinderTransportTests(unittest.TestCase):
    def test_trivial_cycle_cylinder(self) -> None:
        self.assertEqual(cylinder_base((1, 0)), (1, 1))
        self.assertEqual(lifted_pair((1, 0), 2), (9, 7))

    def test_paradoxical_example_seven_to_eight(self) -> None:
        word = (1, 1, 1, 0, 1, 0, 0, 1)
        self.assertEqual(cylinder_base(word), (7, 8))
        self.assertEqual(affine_offset(word), 347)

    def test_christoffel_example_has_residue_gap(self) -> None:
        word = upper_christoffel_word(8, 5)
        self.assertEqual(affine_offset(word), 319)
        self.assertEqual(prefix_cap(word), Fraction(319, 13))
        residue, _ = cylinder_base(word)
        self.assertGreater(residue, Fraction(319, 13))

    def test_small_exhaustive_transport(self) -> None:
        report = verify_transport(max_word_length=8, max_lift=3)
        self.assertEqual(report["transport_words_checked"], 510)

    def test_small_christoffel_screen(self) -> None:
        report = verify_christoffel_gap(max_length=60)
        self.assertEqual(report["christoffel_gap_counterexamples"], 0)
        self.assertGreater(report["christoffel_high_density_pairs_checked"], 0)


if __name__ == "__main__":
    unittest.main()
