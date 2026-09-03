from fractions import Fraction
import unittest

from verify_nonregular_local_constant import (
    add_matrices,
    check_instance,
    check_two_scale,
    degree_regular_decomposition,
    expansion_constants,
    mean_center,
    run_checks,
)
from verify_regular_local_constant import adjacency_matrix, double_center


class NonregularLocalConstantTests(unittest.TestCase):
    def test_degree_regular_decomposition(self) -> None:
        matrix = mean_center(adjacency_matrix(3, 0b001))
        degree, degree_kernel, regular = degree_regular_decomposition(matrix)
        self.assertEqual(sum(degree), 0)
        self.assertTrue(all(sum(row) == 0 for row in regular))
        self.assertEqual(add_matrices(degree_kernel, regular), matrix)

    def test_component_norm_bound(self) -> None:
        matrix = mean_center(adjacency_matrix(3, 0b001))
        degree, _, regular = degree_regular_decomposition(matrix)
        eta = max(abs(value) for row in matrix for value in row)
        self.assertLessEqual(max(abs(value) for value in degree), eta)
        self.assertLessEqual(max(abs(value) for row in regular for value in row), 3 * eta)

    def test_two_scale_fourth_coefficient(self) -> None:
        regular = double_center(adjacency_matrix(3, 0b101))
        seed = (Fraction(-1), Fraction(0), Fraction(1))
        coefficients = check_two_scale(regular, seed, Fraction(2, 5), 3, 4)
        self.assertEqual(coefficients[1:4], (0, 0, 0))
        self.assertGreater(coefficients[4], 0)

    def test_pure_degree_two_scale_coefficient(self) -> None:
        zero = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
        coefficients = check_two_scale(
            zero, (Fraction(-1), Fraction(1)), Fraction(2, 5), 2, 3
        )
        self.assertEqual(coefficients[1:4], (0, 0, 0))
        self.assertGreater(coefficients[4], 0)

    def test_general_irregular_instance(self) -> None:
        p = Fraction(2, 5)
        r = Fraction(1, 50)
        centered = mean_center(adjacency_matrix(3, 0b001))
        maximum = max(abs(value) for row in centered for value in row)
        matrix = tuple(
            tuple(r * p * value / maximum for value in row) for row in centered
        )
        check_instance(matrix, p, r, 3, 4)

    def test_error_constants_at_zero(self) -> None:
        self.assertEqual(expansion_constants(6, Fraction(0)), (0, 0))

    def test_small_run(self) -> None:
        kernels, irregular, instances, two_scale, digest = run_checks(3, 3)
        self.assertGreater(kernels, 0)
        self.assertGreater(irregular, 0)
        self.assertEqual(instances, 2 * 4 * kernels)
        self.assertGreater(two_scale, 0)
        self.assertEqual(len(digest), 64)

    def test_invalid_atom_count(self) -> None:
        with self.assertRaises(ValueError):
            run_checks(1, 3)


if __name__ == "__main__":
    unittest.main()
