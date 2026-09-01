#!/usr/bin/env python3
"""Dependency-free exact certificate for the n=16 code exclusion.

This implementation differs from the proof candidate's nested-radical scan.
It constructs roots of unity from rational Machin/Taylor enclosures, then
uses a three-stage structural certificate: a switch-count bound, a trace
bound, and only finally a 2-by-2 spectral calculation.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from verify_boundary_band_symbolic import pi_interval


HERE = Path(__file__).resolve().parent
N = 16


def rational(text: str) -> Fraction:
    return Fraction(text)


def sine_partial(x: Fraction, last_index: int) -> Fraction:
    term = x
    total = term
    for k in range(1, last_index + 1):
        term *= -x * x / ((2 * k) * (2 * k + 1))
        total += term
    return total


def sine_interval_wide(
    lower: Fraction, upper: Fraction, pairs: int
) -> tuple[Fraction, Fraction]:
    """Enclose sine on a subinterval of [0,pi/2] by alternating sums."""
    if not (0 <= lower <= upper <= Fraction(8, 5)):
        raise ValueError("the sine enclosure requires [0,8/5]")
    return sine_partial(lower, 2 * pairs + 1), sine_partial(upper, 2 * pairs)


def sqrt_interval(value: Fraction, decimal_digits: int) -> tuple[Fraction, Fraction]:
    if value < 0:
        raise ValueError("square root requires a nonnegative rational")
    scale = 10**decimal_digits
    quotient = value.numerator * scale * scale // value.denominator
    root = math.isqrt(quotient)
    lower = Fraction(root, scale)
    upper = Fraction(root + 1, scale)
    if not lower * lower <= value < upper * upper:
        raise AssertionError("integer square-root enclosure failed")
    return lower, upper


def floor_scaled(value: Fraction, scale: int) -> int:
    return value.numerator * scale // value.denominator


def ceil_scaled(value: Fraction, scale: int) -> int:
    return -((-value.numerator * scale) // value.denominator)


def interval_add(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def interval_neg(x: tuple[int, int]) -> tuple[int, int]:
    return -x[1], -x[0]


def interval_sub(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return interval_add(x, interval_neg(y))


def interval_scale(x: tuple[int, int], coefficient: int) -> tuple[int, int]:
    if coefficient >= 0:
        return coefficient * x[0], coefficient * x[1]
    return coefficient * x[1], coefficient * x[0]


def raw_product(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    values = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(values), max(values)


def min_abs(x: tuple[int, int]) -> int:
    if x[0] <= 0 <= x[1]:
        return 0
    return min(abs(x[0]), abs(x[1]))


def max_abs(x: tuple[int, int]) -> int:
    return max(abs(x[0]), abs(x[1]))


def ceil_sqrt_integer(value: int) -> int:
    root = math.isqrt(value)
    return root if root * root == value else root + 1


def code_from_bits(bits: int) -> tuple[int, ...]:
    return (1,) + tuple(
        1 if ((bits >> (j - 1)) & 1) == 0 else -1 for j in range(1, N)
    )


def code_string(code: tuple[int, ...]) -> str:
    return "".join("+" if value == 1 else "-" for value in code)


def dihedral_orbit(representative: tuple[int, ...]) -> set[tuple[int, ...]]:
    full = representative + tuple(-value for value in representative)
    orbit: set[tuple[int, ...]] = set()
    for shift in range(2 * N):
        rotated = full[shift:] + full[:shift]
        reflected = tuple(rotated[(-j) % (2 * N)] for j in range(2 * N))
        for transformed in (rotated, reflected):
            half = transformed[:N]
            if half[0] < 0:
                half = tuple(-value for value in half)
            orbit.add(half)
    return orbit


def verify() -> dict[str, object]:
    data = json.loads((HERE / "code_exclusion_certificate.json").read_text())
    radius_squared = rational(data["squared_gap_radius_upper"])
    expected_codes = int(data["normalized_code_count"])
    expected_universal = int(data["universal_screen_survivor_count"])
    expected_trace = int(data["trace_screen_survivor_count"])
    expected_final = int(data["spectral_screen_survivor_count"])
    universal_margin_claim = rational(data["universal_screen_margin_lower"])
    trace_margin_claim = rational(data["trace_screen_margin_lower"])
    spectral_margin_claim = rational(data["spectral_screen_margin_lower"])
    sine_pairs = int(data["sine_series_pairs"])
    fixed_digits = int(data["fixed_point_decimal_digits"])
    sqrt_digits = int(data["sqrt_decimal_digits"])
    pi_lower, pi_upper = pi_interval(int(data["machin_arctan_pairs"]))
    scale = 10**fixed_digits

    # Construct sin(k*pi/16), 0<=k<=8, directly from rational series.
    sine_fixed: list[tuple[int, int]] = []
    for k in range(9):
        lower, upper = sine_interval_wide(
            k * pi_lower / 16, k * pi_upper / 16, sine_pairs
        )
        sine_fixed.append((floor_scaled(lower, scale), ceil_scaled(upper, scale)))

    roots: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for j in range(17):
        if j <= 8:
            sine = sine_fixed[j]
            cosine = sine_fixed[8 - j]
        else:
            sine = sine_fixed[16 - j]
            cosine = interval_neg(sine_fixed[j - 8])
        roots.append((cosine, sine))

    edges = [
        (interval_sub(roots[j + 1][0], roots[j][0]),
         interval_sub(roots[j + 1][1], roots[j][1]))
        for j in range(N)
    ]
    sin_pi_32 = sine_interval_wide(pi_lower / 32, pi_upper / 32, sine_pairs)
    dirichlet_constant_upper = Fraction(1, 4 * sin_pi_32[0] * sin_pi_32[0])
    radius_upper = sqrt_interval(radius_squared, sqrt_digits)[1]
    remainder_upper = dirichlet_constant_upper * radius_squared
    # Round all code-dependent comparisons onto one integer lattice.  This is
    # still outward-rounded exact arithmetic, but avoids repeatedly forming a
    # Fraction whose denominator contains the full Taylor-series denominator.
    radius_upper_fixed = ceil_scaled(radius_upper, scale)
    remainder_upper_fixed = ceil_scaled(remainder_upper, scale)
    universal_margin_claim_fixed = ceil_scaled(universal_margin_claim, scale)
    trace_margin_claim_fixed = ceil_scaled(trace_margin_claim, scale)
    spectral_margin_claim_fixed = ceil_scaled(spectral_margin_claim, scale)

    def product_upper_fixed(left: int, right: int) -> int:
        """Ceiling of (left/S)*(right/S), represented again at scale S."""
        return (left * right + scale - 1) // scale

    green_numerators = [
        [min(j, k) * (N - max(j, k)) for k in range(1, N)]
        for j in range(1, N)
    ]

    def residual_lower_fixed(code: tuple[int, ...]) -> int:
        real = (0, 0)
        imag = (0, 0)
        for coefficient, edge in zip(code, edges):
            real = interval_add(real, interval_scale(edge[0], coefficient))
            imag = interval_add(imag, interval_scale(edge[1], coefficient))
        squared = min_abs(real) ** 2 + min_abs(imag) ** 2
        return math.isqrt(squared)

    def linear_columns(code: tuple[int, ...]) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        real: list[tuple[int, int]] = []
        imag: list[tuple[int, int]] = []
        for j in range(1, N):
            coefficient = code[j - 1] - code[j]
            real.append(interval_scale(interval_neg(roots[j][1]), coefficient))
            imag.append(interval_scale(roots[j][0], coefficient))
        return real, imag

    def green_entry(
        left: list[tuple[int, int]], right: list[tuple[int, int]]
    ) -> tuple[int, int]:
        lower = 0
        upper = 0
        for j in range(N - 1):
            for k in range(N - 1):
                product_interval = raw_product(left[j], right[k])
                weight = green_numerators[j][k]
                lower += weight * product_interval[0]
                upper += weight * product_interval[1]
        return lower, upper

    switch_sigma_upper_fixed = []
    for switches in range(N):
        sigma_upper = sqrt_interval(
            4 * dirichlet_constant_upper * switches, sqrt_digits
        )[1]
        switch_sigma_upper_fixed.append(ceil_scaled(sigma_upper, scale))

    universal_survivors: list[tuple[int, ...]] = []
    for bits in range(1 << (N - 1)):
        code = code_from_bits(bits)
        switches = sum(code[j - 1] != code[j] for j in range(1, N))
        sigma_upper_fixed = switch_sigma_upper_fixed[switches]
        threshold_fixed = (
            product_upper_fixed(radius_upper_fixed, sigma_upper_fixed)
            + remainder_upper_fixed
        )
        margin_fixed = residual_lower_fixed(code) - threshold_fixed
        if margin_fixed > 0:
            if not margin_fixed > universal_margin_claim_fixed:
                raise AssertionError("universal-screen margin is too small")
        else:
            universal_survivors.append(code)

    if (1 << (N - 1)) != expected_codes:
        raise AssertionError("normalized code enumeration is incomplete")
    if len(universal_survivors) != expected_universal:
        raise AssertionError("unexpected universal-screen survivor count")

    trace_survivors: list[tuple[int, ...]] = []
    for code in universal_survivors:
        real, imag = linear_columns(code)
        real_gram = green_entry(real, real)
        imag_gram = green_entry(imag, imag)
        trace_upper = Fraction(real_gram[1] + imag_gram[1], 16 * scale * scale)
        sigma_upper_fixed = ceil_scaled(
            sqrt_interval(trace_upper, sqrt_digits)[1], scale
        )
        threshold_fixed = (
            product_upper_fixed(radius_upper_fixed, sigma_upper_fixed)
            + remainder_upper_fixed
        )
        margin_fixed = residual_lower_fixed(code) - threshold_fixed
        if margin_fixed > 0:
            if not margin_fixed > trace_margin_claim_fixed:
                raise AssertionError("trace-screen margin is too small")
        else:
            trace_survivors.append(code)

    if len(trace_survivors) != expected_trace:
        raise AssertionError("unexpected trace-screen survivor count")

    final_survivors: list[tuple[int, ...]] = []
    for code in trace_survivors:
        real, imag = linear_columns(code)
        gram_00 = green_entry(real, real)
        gram_11 = green_entry(imag, imag)
        gram_01 = green_entry(real, imag)
        trace_upper_numerator = gram_00[1] + gram_11[1]
        difference = (gram_00[0] - gram_11[1], gram_00[1] - gram_11[0])
        radical_upper = ceil_sqrt_integer(
            max_abs(difference) ** 2 + 4 * max_abs(gram_01) ** 2
        )
        eigenvalue_upper_numerator = (
            trace_upper_numerator + radical_upper + 1
        ) // 2
        sigma_upper_fixed = (
            ceil_sqrt_integer(eigenvalue_upper_numerator) + 3
        ) // 4
        threshold_fixed = (
            product_upper_fixed(radius_upper_fixed, sigma_upper_fixed)
            + remainder_upper_fixed
        )
        margin_fixed = residual_lower_fixed(code) - threshold_fixed
        if margin_fixed > 0:
            if not margin_fixed > spectral_margin_claim_fixed:
                raise AssertionError("spectral-screen margin is too small")
        else:
            final_survivors.append(code)

    if len(final_survivors) != expected_final:
        raise AssertionError("unexpected final survivor count")

    representative = tuple(
        1 if symbol == "+" else -1 for symbol in data["representative_half_code"]
    )
    orbit = dihedral_orbit(representative)
    if len(orbit) != expected_final or set(final_survivors) != orbit:
        raise AssertionError("survivors are not exactly the stated dihedral orbit")

    return {
        "exact_certificate": True,
        "arithmetic": "integer intervals from Fraction/Machin/Taylor bounds",
        "normalized_codes_checked": expected_codes,
        "universal_screen_survivors": len(universal_survivors),
        "trace_screen_survivors": len(trace_survivors),
        "spectral_screen_survivors": len(final_survivors),
        "survivors": sorted(code_string(code) for code in final_survivors),
        "dihedral_orbit_size": len(orbit),
        "universal_screen_margin_lower": data["universal_screen_margin_lower"],
        "trace_screen_margin_lower": data["trace_screen_margin_lower"],
        "spectral_screen_margin_lower": data["spectral_screen_margin_lower"],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
