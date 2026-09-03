from fractions import Fraction
import unittest

from verify_regular_local_constant import (
    adjacency_matrix,
    c4_density,
    check_instance,
    cut_norm,
    double_center,
    kst_density,
    matrix_rank,
    remainder_factor,
    run_checks,
)


class RegularLocalConstantTests(unittest.TestCase):
    def test_double_centering(self) -> None:
        centered = double_center(adjacency_matrix(3, 0b101))
        self.assertTrue(all(sum(row) == 0 for row in centered))
        self.assertEqual(centered, tuple(zip(*centered)))

    def test_balanced_rank_one_saturates_centered_cut_bound(self) -> None:
        eta = Fraction(1, 10)
        matrix = ((eta, -eta), (-eta, eta))
        self.assertEqual(c4_density(matrix), eta**4)
        self.assertEqual(cut_norm(matrix), eta / 4)
        self.assertEqual(256 * cut_norm(matrix) ** 4, c4_density(matrix))
        self.assertEqual(matrix_rank(matrix), 1)

    def test_regular_c4_expansion_is_exact(self) -> None:
        p = Fraction(2, 5)
        eta = Fraction(1, 20)
        matrix = ((eta, -eta), (-eta, eta))
        self.assertEqual(kst_density(tuple(tuple(p + x for x in row) for row in matrix), 2, 2) - p**4, c4_density(matrix))

    def test_non_rank_one_instance(self) -> None:
        p = Fraction(2, 5)
        r = Fraction(1, 50)
        centered = double_center(adjacency_matrix(3, 0b101))
        maximum = max(abs(value) for row in centered for value in row)
        matrix = tuple(tuple(r * p * value / maximum for value in row) for row in centered)
        check_instance(matrix, p, r, 3, 4)

    def test_remainder_boundary(self) -> None:
        self.assertEqual(remainder_factor(4, Fraction(1, 10)), 0)
        self.assertEqual(remainder_factor(6, Fraction(1, 10)), Fraction(1, 100))

    def test_small_run(self) -> None:
        kernels, higher_rank_kernels, instances, digest = run_checks(3, 3)
        self.assertEqual(kernels, 8)
        self.assertEqual(higher_rank_kernels, 4)
        self.assertEqual(instances, 64)
        self.assertEqual(len(digest), 64)

    def test_invalid_atom_count(self) -> None:
        with self.assertRaises(ValueError):
            run_checks(1, 3)


if __name__ == "__main__":
    unittest.main()
