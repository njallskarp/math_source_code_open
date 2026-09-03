from fractions import Fraction
import unittest

from verify_finite_radius_extremizers import (
    Interval,
    direct_profile,
    integer_nth_root,
    root_interval,
    run_checks,
    theorem_envelope,
)


class FiniteRadiusExtremizerTests(unittest.TestCase):
    def test_integer_roots(self) -> None:
        self.assertEqual(integer_nth_root(80, 2), 8)
        self.assertEqual(integer_nth_root(80, 4), 2)
        self.assertEqual(integer_nth_root(81, 4), 3)

    def test_exact_rational_root(self) -> None:
        interval = root_interval(Fraction(81, 16), 4)
        self.assertEqual(interval, Interval.point(Fraction(3, 2)))

    def test_inexact_root_is_certified(self) -> None:
        value = Fraction(2, 3)
        interval = root_interval(value, 4, digits=20)
        self.assertLessEqual(interval.lo**4, value)
        self.assertGreaterEqual(interval.hi**4, value)
        self.assertLess(interval.hi - interval.lo, Fraction(1, 10**19))

    def test_envelope_side_conditions(self) -> None:
        envelope = theorem_envelope(
            3, 3, Fraction(2, 5), Fraction(1, 10**10), Fraction(1, 10**4)
        )
        y_value = envelope["y"]
        epsilon = envelope["epsilon"]
        self.assertIsInstance(y_value, Interval)
        self.assertIsInstance(epsilon, Interval)
        assert isinstance(y_value, Interval) and isinstance(epsilon, Interval)
        self.assertLess(y_value.hi**2, envelope["minus"])
        self.assertLess(epsilon.hi, Fraction(1, 128))

    def test_direct_degree_profile(self) -> None:
        values = direct_profile(
            2, 3, 10**10, degree_weight=Fraction(1, 20)
        )
        self.assertEqual(values[0:3], (Fraction(2), Fraction(3), Fraction(10**10)))

    def test_direct_spectral_profile(self) -> None:
        values = direct_profile(
            3, 3, 10**10, tail_weight=Fraction(1, 16)
        )
        self.assertEqual(values[4], Fraction(1, 16))

    def test_invalid_envelope(self) -> None:
        with self.assertRaises(ValueError):
            theorem_envelope(1, 2, Fraction(2, 5), Fraction(1, 10**8), Fraction(0))
        with self.assertRaises(ValueError):
            theorem_envelope(2, 2, Fraction(2, 5), Fraction(1, 2), Fraction(0))

    def test_full_run(self) -> None:
        degree_profiles, spectral_profiles, digest = run_checks()
        self.assertEqual(degree_profiles, 6)
        self.assertEqual(spectral_profiles, 6)
        self.assertEqual(len(digest), 64)


if __name__ == "__main__":
    unittest.main()
