import unittest

from audit_swap_cocycle import (
    Cylinder,
    audit,
    coefficient_gap_coordinates,
    cylinder_from_bits,
    first_crossing_cylinders,
    verify_split_coordinate,
)


class SwapCocycleTests(unittest.TestCase):
    def test_affine_numerator_identity(self) -> None:
        source = Cylinder.empty()
        for bit in (1, 1, 0, 1, 1, 0, 0):
            source = source.extend(bit)
        target = Cylinder.empty()
        for bit in (1, 1, 1, 0, 1, 0, 0):
            target = target.extend(bit)
        self.assertEqual(source.numerator - target.numerator, 4 * 3)
        self.assertEqual(source.margin, 21)
        self.assertEqual(target.margin, 2)

    def test_first_crossing_counts(self) -> None:
        groups = first_crossing_cylinders(16)
        self.assertEqual(len(groups[8]), 7)
        self.assertEqual(len(groups[13]), 85)
        self.assertEqual(len(groups[16]), 476)

    def test_small_audit(self) -> None:
        report = audit(16)
        self.assertEqual(report["first_crossing_cylinders"], 791)
        self.assertEqual(report["adjacent_edges"], 2132)
        self.assertEqual(report["unwrapped_edges"], 1302)
        self.assertEqual(report["wrapped_edges"], 830)
        self.assertEqual(report["minimum_jump"], 2)
        self.assertEqual(
            report["sha256"],
            "54b943055b0867d15f3eef4a234c4d8ddff7aa3d75f5a13b2e0778c6a80602d5",
        )

    def test_split_coordinates_exhaustively(self) -> None:
        for length, states in first_crossing_cylinders(16).items():
            for bits, source in states.items():
                for position in range(length - 1):
                    if ((bits >> position) & 3) != 2:
                        continue
                    target = states[bits ^ (3 << position)]
                    verify_split_coordinate(length, bits, position, source, target)

    def test_coefficient_gap_coordinates(self) -> None:
        for states in first_crossing_cylinders(16).values():
            for state in states.values():
                gap, margin_residue, window_index = coefficient_gap_coordinates(state)
                self.assertEqual(state.margin, margin_residue - gap * window_index)
                self.assertGreaterEqual(margin_residue, 0)
                self.assertLess(margin_residue, gap)

        # A contracting word outside the first-crossing family exercises a
        # genuinely nonzero window index and a negative descent margin.
        state = cylinder_from_bits(21, 5)
        self.assertEqual(state.margin, -1)
        self.assertEqual(coefficient_gap_coordinates(state), (5, 4, 1))


if __name__ == "__main__":
    unittest.main()
