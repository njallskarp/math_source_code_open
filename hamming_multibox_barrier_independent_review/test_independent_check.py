import unittest

from independent_check import (
    adjacency_masks,
    audit_cube_bipartitions,
    audit_general_volume_classification,
    audit_volume_classification,
    cells,
    induced_min_degree,
    verify_exceptional_partition,
)


class IndependentCheckTests(unittest.TestCase):
    def test_square_has_minimum_degree_two(self) -> None:
        vertices = cells((2, 2))
        full = (1 << len(vertices)) - 1
        self.assertEqual(induced_min_degree(full, adjacency_masks(vertices)), 2)

    def test_cube_has_three_legal_unordered_face_splits(self) -> None:
        self.assertEqual(audit_cube_bipartitions(), 3)

    def test_volume_screen_has_unique_survivor(self) -> None:
        _, survivors = audit_volume_classification(max_s=8)
        self.assertEqual(survivors, ((3, 2, 2, 2),))

    def test_general_volume_screen_has_same_normalized_survivor(self) -> None:
        _, survivors = audit_general_volume_classification(max_s=8, max_dimension=6)
        self.assertEqual(survivors, ((3, (2, 2, 2)),))

    def test_advertised_minor_box_has_sixteen_parts(self) -> None:
        self.assertEqual(verify_exceptional_partition((5, 5, 2)), 16)


if __name__ == "__main__":
    unittest.main()
