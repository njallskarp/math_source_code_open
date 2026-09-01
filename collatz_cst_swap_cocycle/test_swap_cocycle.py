import unittest

from audit_phase_lag import audit as audit_phase_lag
from audit_split_barrier import (
    audit as audit_split_barrier,
)
from audit_split_barrier import (
    first_suffix_parity_mismatch,
)
from audit_split_barrier import (
    relative_coefficient_crossing,
)
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

    def test_phase_lag_and_minimal_unrestricted_defect(self) -> None:
        report = audit_phase_lag(10)
        self.assertEqual(report["phase_lag_failures"], 0)
        self.assertEqual(report["window_failures"], 0)
        self.assertEqual(report["zero_index_source_antidominance_failures"], 0)
        self.assertEqual(
            report["first_zero_index_source_strict_defect"],
            "K=5;source=01101;target=10101;j=0;q=3;d=5;"
            "source_r=22;source_z=20;source_B=46;source_mu=2;"
            "source_kappa=0;target_r=1;target_z=2;target_B=37;"
            "target_mu=4;target_kappa=1;delta=11;E=9;J=2;W=1;C=0",
        )

    def test_split_barrier_certificate_hierarchy(self) -> None:
        report = audit_split_barrier(16)
        self.assertEqual(report["first_crossings"], 791)
        self.assertEqual(report["candidate_edges"], 2132)
        self.assertEqual(report["wrapped_edges"], 830)
        self.assertEqual(report["positive_prefix_surplus"], 737)
        self.assertEqual(report["nonpositive_prefix_surplus"], 93)
        self.assertEqual(report["low_two_bit_certificates"], 31)
        self.assertEqual(report["base_shadow_certificates"], 62)
        self.assertEqual(report["base_shadow_prefixes"], 2)
        self.assertEqual(report["unresolved_after_base_shadow"], 0)
        self.assertEqual(report["adaptive_shadow_certificates"], 62)
        self.assertEqual(report["excluded_lift_ladder_certificates"], 62)
        self.assertEqual(report["excluded_lift_ladder_candidates"], 62)
        self.assertEqual(report["excluded_lift_ladder_parity_bits"], 127)
        self.assertEqual(report["maximum_excluded_lift_ladder_steps"], 1)
        self.assertEqual(report["maximum_excluded_lift_mismatch_depth"], 3)
        self.assertEqual(report["descent_failures"], 0)
        self.assertEqual(
            report["certificate_bits"], {0: 737, 2: 31, 3: 9, 4: 41, 5: 12}
        )
        self.assertEqual(report["symbolic_certificate_bits"], {0: 737, 2: 93})

    def test_length_27_fixed_bit_obstruction(self) -> None:
        word = "111101011011101111010011000"
        position = 5
        bits = sum(int(bit) << index for index, bit in enumerate(word))
        target = cylinder_from_bits(bits, len(word))
        prefix = cylinder_from_bits(bits, position)
        suffix = cylinder_from_bits(
            bits >> (position + 2), len(word) - position - 2
        )
        local_modulus = 1 << (len(word) - position)
        target_lift = (target.residue - prefix.residue) // (1 << position)
        gap = target.pow2 - target.pow3
        prefix_surplus = (
            local_modulus * prefix.residue
            - suffix.pow3 * (3 * prefix.endpoint + 1)
            - 4 * suffix.numerator
        )

        self.assertEqual((gap, local_modulus), (5_077_565, 4_194_304))
        self.assertEqual(relative_coefficient_crossing(prefix, 1), 47)
        suffix_bits = bits >> (position + 2)
        suffix_length = len(word) - position - 2
        self.assertEqual(
            first_suffix_parity_mismatch(
                prefix, 1, suffix_bits, suffix_length
            ),
            18,
        )
        self.assertEqual((target_lift, prefix_surplus), (2_621_441, -5_601_853))
        self.assertEqual(target_lift % (1 << 19), 1)
        self.assertEqual(gap + prefix_surplus, -524_288)
        self.assertEqual(target_lift % (1 << 20), 524_289)
        self.assertGreater(gap * (target_lift % (1 << 20)) + prefix_surplus, 0)
        self.assertEqual(
            gap * target_lift + prefix_surplus,
            local_modulus * target.margin,
        )


if __name__ == "__main__":
    unittest.main()
