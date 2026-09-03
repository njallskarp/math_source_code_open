#!/usr/bin/env python3
"""Rigorous finite-step audit for the finite-radius extremizer theorem.

All graphon quantities use ``fractions.Fraction``.  Square and fourth roots
are enclosed by decimal-rational intervals whose endpoints are certified by
integer powers; no floating point or external interval library is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import math
import platform
from typing import Iterable, Sequence


Matrix = tuple[tuple[Fraction, ...], ...]
ROOT_DIGITS = 70


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("interval endpoints are reversed")

    @classmethod
    def point(cls, value: Fraction | int) -> "Interval":
        value = Fraction(value)
        return cls(value, value)

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: "Interval") -> "Interval":
        return self + (-other)

    def __mul__(self, other: "Interval") -> "Interval":
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return Interval(Fraction(1, 1) / self.hi, Fraction(1, 1) / self.lo)

    def __truediv__(self, other: "Interval") -> "Interval":
        return self * other.reciprocal()

    def __pow__(self, exponent: int) -> "Interval":
        if exponent < 0:
            return (self.reciprocal()) ** (-exponent)
        result = Interval.point(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval_text(value: Interval) -> str:
    return f"[{fraction_text(value.lo)},{fraction_text(value.hi)}]"


def integer_nth_root(value: int, degree: int) -> int:
    if value < 0 or degree not in (2, 4):
        raise ValueError("only nonnegative square and fourth roots are supported")
    root = math.isqrt(value)
    if degree == 4:
        root = math.isqrt(root)
    while (root + 1) ** degree <= value:
        root += 1
    while root**degree > value:
        root -= 1
    return root


def root_interval(value: Fraction, degree: int, digits: int = ROOT_DIGITS) -> Interval:
    """Enclose a rational square or fourth root by exact integer comparison."""
    if value < 0:
        raise ValueError("root input must be nonnegative")
    scale = 10**digits
    scaled_floor = value.numerator * scale**degree // value.denominator
    lower_integer = integer_nth_root(scaled_floor, degree)
    lower = Fraction(lower_integer, scale)
    if lower**degree == value:
        return Interval.point(lower)
    upper = Fraction(lower_integer + 1, scale)
    if not lower**degree < value < upper**degree:
        raise AssertionError("root enclosure failed its exact power check")
    return Interval(lower, upper)


def interval_root(value: Interval, degree: int) -> Interval:
    if value.lo < 0:
        raise ValueError("interval root input must be nonnegative")
    return Interval(
        root_interval(value.lo, degree).lo,
        root_interval(value.hi, degree).hi,
    )


def interval_abs(value: Interval) -> Interval:
    if value.lo >= 0:
        return value
    if value.hi <= 0:
        return -value
    return Interval(Fraction(0), max(-value.lo, value.hi))


def interval_max(first: Interval, second: Interval) -> Interval:
    return Interval(max(first.lo, second.lo), max(first.hi, second.hi))


def scaled(interval: Interval, value: Fraction | int) -> Interval:
    return interval * Interval.point(Fraction(value))


def theorem_envelope(
    s: int, t: int, p: Fraction, r: Fraction, tau: Fraction
) -> dict[str, Fraction | Interval]:
    """Certified enclosure of every explicit theorem constant."""
    if s < 2 or t < 2 or not 0 < p < 1 or not 0 < r <= Fraction(1, 3):
        raise ValueError("parameters are outside the theorem domain")
    if not 0 <= tau < 1:
        raise ValueError("tau must lie in [0,1)")

    e = s * t
    adjacent = s * math.comb(t, 2) + t * math.comb(s, 2)
    cycles = math.comb(s, 2) * math.comb(t, 2)
    x = 3 * r
    error_v = 6**e * x + e * 2 ** (e - 1) * x**2
    error_4 = (2**e + e * 2 ** (e - 1)) * x**2
    rho = max(error_v / adjacent, error_4 / cycles)
    if rho >= 1:
        raise ValueError("relative expansion error is not below one")

    minus = Fraction(1, 1) / (1 + rho)
    plus = Fraction(1, 1) / (1 - rho)
    plus_fourth = root_interval(plus, 4)
    plus_three_fourths = plus_fourth**3

    gamma_fourth = Fraction(256 * 2**e * cycles, adjacent**2) * r**2
    gamma = root_interval(gamma_fourth, 4)
    h_value = Interval.point(tau - 1) + plus_fourth
    inner = gamma**2 + h_value / plus_three_fourths
    y_value = scaled(
        plus_three_fourths
        * (gamma + interval_root(inner, 2)),
        2,
    )

    epsilon = Interval.point(1) - (
        Interval.point(1 - tau) - gamma * y_value
    ) / plus_fourth
    beta_lower = Interval.point(minus) - y_value**2
    if beta_lower.lo <= 0:
        raise ValueError("certified beta lower bound is not positive")
    theta = interval_max(
        plus_fourth - Interval.point(1),
        Interval.point(1) - interval_root(beta_lower, 4),
    )

    omega_factor_fourth = (
        Fraction(2**e, adjacent**2) * p ** (4 - e) * r**2
    )
    omega = root_interval(omega_factor_fourth, 4) * y_value
    forcing_scale = root_interval(
        Fraction(1, cycles) * p ** (4 - e), 4
    )

    return {
        "e": Fraction(e),
        "adjacent": Fraction(adjacent),
        "cycles": Fraction(cycles),
        "rho": rho,
        "minus": minus,
        "plus": plus,
        "plus_fourth": plus_fourth,
        "gamma": gamma,
        "h": h_value,
        "y": y_value,
        "epsilon": epsilon,
        "theta": theta,
        "omega": omega,
        "forcing_scale": forcing_scale,
    }


def all_subsets(size: int) -> Iterable[tuple[int, ...]]:
    for mask in range(1 << size):
        yield tuple(index for index in range(size) if mask & (1 << index))


def cut_norm(matrix: Matrix) -> Fraction:
    size = len(matrix)
    best = Fraction(0)
    subsets = tuple(all_subsets(size))
    for rows in subsets:
        for columns in subsets:
            total = sum(matrix[i][j] for i in rows for j in columns)
            best = max(best, abs(total) / size**2)
    return best


def kst_density(matrix: Matrix, s: int, t: int) -> Fraction:
    size = len(matrix)
    total = Fraction(0)
    for assignment in itertools.product(range(size), repeat=s + t):
        value = Fraction(1)
        left = assignment[:s]
        right = assignment[s:]
        for i in left:
            for j in right:
                value *= matrix[i][j]
        total += value
    return total / size ** (s + t)


def degree_decomposition(matrix: Matrix) -> tuple[tuple[Fraction, ...], Matrix, Matrix]:
    size = len(matrix)
    degree = tuple(sum(row) / size for row in matrix)
    degree_kernel = tuple(
        tuple(degree[i] + degree[j] for j in range(size)) for i in range(size)
    )
    regular = tuple(
        tuple(matrix[i][j] - degree_kernel[i][j] for j in range(size))
        for i in range(size)
    )
    return degree, degree_kernel, regular


def add_constant(matrix: Matrix, constant: Fraction) -> Matrix:
    return tuple(tuple(constant + value for value in row) for row in matrix)


def base_signs() -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    return (
        (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1)),
        (Fraction(1), Fraction(-1), Fraction(1), Fraction(-1)),
    )


def profile_matrix(
    regular_amplitude: Fraction,
    degree_amplitude: Fraction,
    tail_amplitude: Fraction = Fraction(0),
) -> Matrix:
    first, second = base_signs()
    return tuple(
        tuple(
            regular_amplitude * first[i] * first[j]
            + tail_amplitude * second[i] * second[j]
            + degree_amplitude * (second[i] + second[j])
            for j in range(4)
        )
        for i in range(4)
    )


def certified_tau(relative_ratio_fourth: Fraction) -> Fraction:
    """Return rational tau with 1-tau <= fourth_root(relative_ratio_fourth)."""
    if relative_ratio_fourth >= 1:
        return Fraction(0)
    lower = root_interval(relative_ratio_fourth, 4).lo
    return 1 - lower


def require_interval_leq(left: Interval, right: Interval, label: str) -> None:
    if left.hi > right.lo:
        raise AssertionError(
            f"{label}: intervals do not certify inequality: "
            f"{interval_text(left)} > {interval_text(right)}"
        )


def direct_profile(
    s: int,
    t: int,
    denominator: int,
    degree_weight: Fraction = Fraction(0),
    tail_weight: Fraction = Fraction(0),
) -> tuple[Fraction, ...]:
    p = Fraction(2, 5)
    eta = p / denominator
    xi = degree_weight * eta**2 / p
    tail = tail_weight * eta
    perturbation = profile_matrix(eta, xi, tail)
    graphon = add_constant(perturbation, p)
    if any(not 0 <= value <= 1 for row in graphon for value in row):
        raise AssertionError("finite profile is not a graphon")

    edge_count = s * t
    cycles = math.comb(s, 2) * math.comb(t, 2)
    density = kst_density(graphon, s, t)
    delta = density - p**edge_count
    if delta <= 0:
        raise AssertionError("profile has nonpositive homomorphism excess")
    cut = cut_norm(perturbation)
    degree, degree_kernel, regular = degree_decomposition(perturbation)
    if any(sum(row) for row in regular):
        raise AssertionError("regular core has a nonzero row sum")
    v = sum(value**2 for value in degree) / 4
    z = kst_density(regular, 2, 2)
    relative_ratio_fourth = cycles * p ** (edge_count - 4) * (4 * cut) ** 4 / delta
    tau = certified_tau(relative_ratio_fourth)
    if (1 - tau) ** 4 > relative_ratio_fourth:
        raise AssertionError("certified tau does not imply the ratio hypothesis")
    radius = max(abs(value) for row in perturbation for value in row) / p
    envelope = theorem_envelope(s, t, p, radius, tau)

    y_value = envelope["y"]
    epsilon = envelope["epsilon"]
    assert isinstance(y_value, Interval) and isinstance(epsilon, Interval)
    if y_value.hi**2 >= envelope["minus"]:
        raise AssertionError("Y^2 < m_- side condition was not certified")
    if epsilon.lo < 0 or epsilon.hi > Fraction(1, 128):
        raise AssertionError("epsilon_* side condition was not certified")

    adjacent = int(envelope["adjacent"])
    alpha = Fraction(adjacent) * p ** (edge_count - 2) * v / delta
    beta = Fraction(cycles) * p ** (edge_count - 4) * z / delta
    leading = (
        Fraction(adjacent) * p ** (edge_count - 2) * v
        + Fraction(cycles) * p ** (edge_count - 4) * z
    )
    if abs(delta - leading) > envelope["rho"] * leading:
        raise AssertionError("direct profile escaped the relative expansion envelope")
    gamma = envelope["gamma"]
    assert isinstance(gamma, Interval)
    scalar_rhs = interval_root(Interval.point(beta), 4) + (
        gamma * interval_root(Interval.point(alpha), 2)
    )
    require_interval_leq(Interval.point(1 - tau), scalar_rhs, "scalar bridge")
    energy_rhs = scaled(y_value**2, Fraction(1, adjacent) * p ** (2 - edge_count))
    require_interval_leq(Interval.point(v / delta), energy_rhs, "degree energy")
    share_rhs = y_value**2 + Interval.point(envelope["rho"] / (1 - envelope["rho"]))
    require_interval_leq(Interval.point(abs(beta - 1)), share_rhs, "cycle share")

    delta_fourth = root_interval(delta, 4)
    degree_operator = interval_root(Interval.point(v), 2) / delta_fourth
    omega = envelope["omega"]
    assert isinstance(omega, Interval)
    require_interval_leq(degree_operator, omega, "degree operator")

    forcing_scale = envelope["forcing_scale"]
    plus_fourth = envelope["plus_fourth"]
    theta = envelope["theta"]
    assert isinstance(forcing_scale, Interval)
    assert isinstance(plus_fourth, Interval)
    assert isinstance(theta, Interval)
    epsilon_fourth = interval_root(epsilon, 4)
    theorem_rhs = (
        omega
        + scaled(forcing_scale * plus_fourth * epsilon_fourth, 10)
        + forcing_scale * theta
    )

    regular_coefficient = Interval.point(eta) / delta_fourth
    model_difference = interval_abs(regular_coefficient - forcing_scale)
    tail_coefficient = Interval.point(abs(tail)) / delta_fourth
    degree_coefficient = degree_operator
    actual_distance = interval_max(
        model_difference,
        interval_max(tail_coefficient, degree_coefficient),
    )
    require_interval_leq(actual_distance, theorem_rhs, "full operator distance")

    if alpha > y_value.lo**2:
        raise AssertionError("alpha escaped the certified quadratic envelope")
    return (
        Fraction(s),
        Fraction(t),
        Fraction(denominator),
        degree_weight,
        tail_weight,
        radius,
        tau,
        delta,
        cut,
        v,
        z,
        alpha,
        beta,
        envelope["rho"],
        y_value.hi,
        epsilon.hi,
        actual_distance.hi,
        theorem_rhs.lo,
    )


def run_checks() -> tuple[int, int, str]:
    digest = hashlib.sha256()
    degree_profiles = 0
    spectral_profiles = 0

    for denominator in (10**10, 10**12):
        for s, t in ((2, 2), (2, 3), (3, 3)):
            values = direct_profile(
                s, t, denominator, degree_weight=Fraction(1, 20)
            )
            digest.update(
                ("D:" + ":".join(fraction_text(value) for value in values) + "\n").encode()
            )
            degree_profiles += 1

    for denominator in (10**10, 10**12):
        for tail_weight in (Fraction(1, 8), Fraction(1, 16), Fraction(1, 32)):
            values = direct_profile(
                3, 3, denominator, tail_weight=tail_weight
            )
            digest.update(
                ("S:" + ":".join(fraction_text(value) for value in values) + "\n").encode()
            )
            spectral_profiles += 1

    return degree_profiles, spectral_profiles, digest.hexdigest()


def main() -> None:
    degree_profiles, spectral_profiles, digest = run_checks()
    print(f"python={platform.python_version()}")
    print("arithmetic=fractions.Fraction")
    print(f"root_digits={ROOT_DIGITS}")
    print(f"degree_profiles={degree_profiles}")
    print(f"spectral_profiles={spectral_profiles}")
    print(f"record_sha256={digest}")
    print("status=PASS")


if __name__ == "__main__":
    main()
