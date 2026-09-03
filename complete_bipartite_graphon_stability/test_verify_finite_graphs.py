from fractions import Fraction
import unittest

from verify_finite_graphs import (
    brute_hom_density,
    check_cut_reduction_components,
    neighbor_masks,
    oriented_moments,
    run_exhaustion,
)


class QuantitativeKstTests(unittest.TestCase):
    def test_empty_graph(self) -> None:
        moments = oriented_moments(neighbor_masks(4, 0), 2, 3)
        self.assertEqual(moments.density, 0)
        self.assertEqual(moments.nonlinear_bound, 0)

    def test_complete_graph_matches_brute_force(self) -> None:
        neighbors = neighbor_masks(4, (1 << 6) - 1)
        moments = oriented_moments(neighbors, 2, 3)
        self.assertEqual(moments.density, brute_hom_density(neighbors, 2, 3))
        self.assertGreaterEqual(moments.density, moments.nonlinear_bound)

    def test_path_on_three_vertices(self) -> None:
        # Lexicographic bits are (0,1), (0,2), (1,2); mask 0b101 is P3.
        neighbors = neighbor_masks(3, 0b101)
        moments = oriented_moments(neighbors, 2, 2)
        self.assertEqual(moments.p, Fraction(4, 9))
        self.assertEqual(moments.density, brute_hom_density(neighbors, 2, 2))
        self.assertGreaterEqual(moments.nonlinear_bound, moments.linear_bound)
        check_cut_reduction_components(neighbors, 4)

    def test_small_exhaustion(self) -> None:
        graph_count, inequality_count, digest = run_exhaustion(3, 3)
        self.assertEqual(graph_count, 11)
        self.assertEqual(inequality_count, 44)
        self.assertEqual(len(digest), 64)

    def test_invalid_part_size(self) -> None:
        with self.assertRaises(ValueError):
            oriented_moments(neighbor_masks(2, 0), 1, 2)


if __name__ == "__main__":
    unittest.main()
