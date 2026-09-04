import unittest

from independent_check import (
    audit_infinite_family,
    exact_cover_rectangle,
    has_old_layer_order,
    has_residue_slab_order,
    is_coordinate_line,
    prior_criteria,
    residue_slab_extend,
    smallest_new_hamming_cases,
    verify_partition,
)


class IndependentCheckTests(unittest.TestCase):
    def test_line_predicate(self) -> None:
        self.assertTrue(is_coordinate_line(((0, 1, 2), (0, 4, 2))))
        self.assertFalse(is_coordinate_line(((0, 1), (1, 2))))
        self.assertFalse(is_coordinate_line(()))

    def test_clean_room_rectangle_cover(self) -> None:
        parts, _ = exact_cover_rectangle(3, 3, 2)
        verify_partition((3, 3), parts, 2)
        self.assertEqual(len(parts), 4)

    def test_composition_beyond_old_layering(self) -> None:
        base, _ = exact_cover_rectangle(3, 3, 2)
        extended = residue_slab_extend(base, (3, 3), 3, 2)
        verify_partition((3, 3, 3), extended, 2)
        self.assertTrue(has_residue_slab_order((3, 3, 3), 2))
        self.assertFalse(has_old_layer_order((3, 3, 3), 2))

    def test_failed_criterion_has_positive_scheme_deficit(self) -> None:
        s, volume, p = 5, 13, 4
        quotient, tau = divmod(volume, s)
        slabs, c = divmod(p, s)
        made = slabs * volume + c * quotient
        self.assertEqual((volume * p) // s - made, (c * tau) // s)
        self.assertGreater((c * tau) // s, 0)

    def test_smallest_new_hamming_cases(self) -> None:
        self.assertEqual(
            smallest_new_hamming_cases(11),
            (((11, 7, 7, 5), 4, 61), ((11, 8, 7, 6), 5, 67)),
        )

    def test_displayed_family_base_case(self) -> None:
        self.assertEqual(audit_infinite_family(2), 1)
        self.assertEqual(6 * 2 * 2 + 19 * 2 + 16, 78)
        self.assertFalse(any(prior_criteria((8, 7, 7), 5)))


if __name__ == "__main__":
    unittest.main()
