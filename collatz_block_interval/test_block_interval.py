import unittest

from verify_block_interval import (
    LiftInterval,
    affine_offset,
    canonical_interval_digest,
    compose_blocks,
    cylinder,
    first_crossing_audit,
    safe_lift_interval,
    verify,
)


class BlockIntervalTests(unittest.TestCase):
    def test_paradoxical_length_eight_word(self) -> None:
        word = tuple(map(int, "11101001"))
        data = cylinder(word)
        self.assertEqual(data.residue, 7)
        self.assertEqual(data.endpoint, 8)
        self.assertEqual(affine_offset(word), 347)
        self.assertIsNone(safe_lift_interval(word))

    def test_trivial_cycle_prefix(self) -> None:
        self.assertEqual(safe_lift_interval((1, 0)), LiftInterval(0, 0))

    def test_coefficient_safe_word_has_unbounded_interval(self) -> None:
        self.assertEqual(safe_lift_interval((1, 1, 0)), LiftInterval(0, None))

    def test_all_even_positive_cylinder_is_empty(self) -> None:
        self.assertIsNone(safe_lift_interval((0, 0, 0)))

    def test_composition_example(self) -> None:
        whole = tuple(map(int, "11101001"))
        composition = compose_blocks(whole[:3], whole[3:])
        data = cylinder(whole)
        self.assertEqual(composition["residue"], data.residue)
        self.assertEqual(composition["endpoint"], data.endpoint)
        self.assertEqual(composition["offset"], data.offset)

    def test_exhaustive_small(self) -> None:
        report = verify(8, 12)
        self.assertEqual(report["words_checked"], 511)
        self.assertEqual(
            report["length_10_interval_sha256"], canonical_interval_digest(10)
        )

    def test_coefficient_stopping_audit(self) -> None:
        report = first_crossing_audit(20)
        self.assertEqual(report["cst_first_crossings_checked"], 4404)
        self.assertEqual(report["cst_trivial_intervals"], 1)
        self.assertEqual(report["cst_unexpected_intervals"], 0)
        self.assertEqual(report["cst_safe_frontier_at_depth"], 27328)


if __name__ == "__main__":
    unittest.main()
