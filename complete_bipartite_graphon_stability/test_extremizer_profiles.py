from fractions import Fraction
import unittest

from verify_extremizer_profiles import (
    base_signs,
    degree_profile,
    run_checks,
    scaled_density_coefficients,
    spectral_tail_profile,
)
from verify_regular_local_constant import c4_density


class ExtremizerProfileTests(unittest.TestCase):
    def test_orthogonal_balanced_signs(self) -> None:
        first, second = base_signs()
        self.assertEqual(sum(first), 0)
        self.assertEqual(sum(second), 0)
        self.assertEqual(sum(x * y for x, y in zip(first, second)), 0)

    def test_spectral_tail_exact_profile(self) -> None:
        rho, c4, cut, tail_cut, relative_cut, relative_tail = spectral_tail_profile(8)
        self.assertEqual(c4, 1 + rho**4)
        self.assertEqual(cut, Fraction(1, 4))
        self.assertEqual(tail_cut, rho / 4)
        self.assertEqual(relative_cut + relative_tail, 1)

    def test_critical_degree_changes_fourth_coefficient(self) -> None:
        p = Fraction(2, 5)
        critical = degree_profile(16, 2, p, 2, 3)
        negligible = degree_profile(16, 3, p, 2, 3)
        self.assertGreater(critical[-1], negligible[-1])

    def test_negligible_degree_has_regular_fourth_coefficient(self) -> None:
        p = Fraction(2, 5)
        regular_sign, degree_seed = base_signs()
        regular = tuple(tuple(x * y for y in regular_sign) for x in regular_sign)
        coefficients = scaled_density_coefficients(
            regular, degree_seed, 3, p, 3, 3
        )
        expected = Fraction(3 * 3) * p**5
        self.assertEqual(coefficients[4], expected)

    def test_invalid_scales(self) -> None:
        with self.assertRaises(ValueError):
            spectral_tail_profile(1)
        regular_sign, degree_seed = base_signs()
        regular = tuple(tuple(x * y for y in regular_sign) for x in regular_sign)
        with self.assertRaises(ValueError):
            scaled_density_coefficients(
                regular, degree_seed, 1, Fraction(2, 5), 2, 2
            )

    def test_full_run(self) -> None:
        tail_instances, degree_instances, digest = run_checks()
        self.assertEqual(tail_instances, 5)
        self.assertEqual(degree_instances, 24)
        self.assertEqual(len(digest), 64)


if __name__ == "__main__":
    unittest.main()
