#!/usr/bin/env python3
"""Standard-library rebuild of the canonical Lucas (3,5) certificate.

This checker shares the mathematical formulas with verify_symbolic.py but not
its CAS or polynomial representation.  It uses only Fraction arithmetic and
small sparse polynomial dictionaries.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from math import comb


T_START = 7
T_EPSILON_NUMERATORS = (
    360, 163, 248, 243, 136, 275, 288, 163, 248, 171,
    280, 203, 288, 163, 176, 315, 208, 203, 288, 91,
    320, 243, 208, 203, 216, 235, 248, 243, 208, 131,
)
U_EPSILON_NUMERATORS = (3, 2, 1)
EXPECTED_CERTIFICATE_SHA256 = "30b60ee3c72ace0c5e95848d171f8602218bc9bfd10e7fdaa58afda14378bf20"

# Sparse univariate polynomials and bivariate polynomials in (x,z).
Uni = dict[int, Fraction]
Bi = dict[tuple[int, int], Fraction]
Term = tuple[str, int, tuple[int, int, int]]


def uni_clean(poly: Uni) -> Uni:
    return {degree: coefficient for degree, coefficient in poly.items() if coefficient}


def uni_add(*polys: Uni) -> Uni:
    result: dict[int, Fraction] = defaultdict(Fraction)
    for poly in polys:
        for degree, coefficient in poly.items():
            result[degree] += coefficient
    return uni_clean(dict(result))


def uni_scale(poly: Uni, scalar: Fraction) -> Uni:
    return uni_clean({degree: scalar * coefficient for degree, coefficient in poly.items()})


def uni_mul(left: Uni, right: Uni) -> Uni:
    result: dict[int, Fraction] = defaultdict(Fraction)
    for a, x in left.items():
        for b, y in right.items():
            result[a + b] += x * y
    return uni_clean(dict(result))


def uni_pow(poly: Uni, exponent: int) -> Uni:
    result: Uni = {0: Fraction(1)}
    for _ in range(exponent):
        result = uni_mul(result, poly)
    return result


def one_minus_power(power: int) -> Uni:
    return {0: Fraction(1), power: Fraction(-1)}


def lift_period(poly: Uni, period: int, shift: int = 0) -> Uni:
    return {period * degree + shift: coefficient for degree, coefficient in poly.items()}


POWER_SUM_NUMERATORS: tuple[Uni, ...] = (
    {0: Fraction(1)},
    {1: Fraction(1)},
    {1: Fraction(1), 2: Fraction(1)},
    {1: Fraction(1), 2: Fraction(4), 3: Fraction(1)},
)


def residue_series_numerator(power_coefficients: Uni, max_degree: int) -> Uni:
    """Numerator over (1-y)^(max_degree+1)."""
    result: Uni = {}
    for degree, coefficient in power_coefficients.items():
        numerator = POWER_SUM_NUMERATORS[degree]
        correction = uni_pow(one_minus_power(1), max_degree - degree)
        result = uni_add(result, uni_scale(uni_mul(numerator, correction), coefficient))
    return result


def verify_quasipolynomials() -> None:
    # Expand T(30m+r) as a polynomial in m over QQ.
    t_numerator: Uni = {}
    for residue, epsilon in enumerate(T_EPSILON_NUMERATORS):
        n: Uni = {0: Fraction(residue), 1: Fraction(30)}
        expression = uni_add(
            uni_scale(uni_pow(n, 3), Fraction(1, 180)),
            uni_scale(uni_pow(n, 2), Fraction(11, 120)),
            uni_scale(n, Fraction(9, 20)),
            {0: Fraction(epsilon, 360)},
        )
        numerator_y = residue_series_numerator(expression, 3)
        t_numerator = uni_add(t_numerator, lift_period(numerator_y, 30, residue))
    target_denominator: Uni = {0: Fraction(1)}
    for part in (1, 2, 3, 5):
        target_denominator = uni_mul(target_denominator, one_minus_power(part))
    expected = uni_pow(one_minus_power(30), 4)
    assert uni_mul(t_numerator, target_denominator) == expected

    # Expand U(3m+r) as a polynomial in m over QQ.
    u_numerator: Uni = {}
    for residue, epsilon in enumerate(U_EPSILON_NUMERATORS):
        expression: Uni = {
            0: Fraction(residue + epsilon, 3),
            1: Fraction(1),
        }
        numerator_y = residue_series_numerator(expression, 1)
        u_numerator = uni_add(u_numerator, lift_period(numerator_y, 3, residue))
    target_denominator = uni_mul(one_minus_power(1), one_minus_power(3))
    expected = uni_pow(one_minus_power(3), 2)
    assert uni_mul(u_numerator, target_denominator) == expected


def T(n: int) -> int:
    if n < 0:
        return 0
    value = (
        Fraction(n**3, 180)
        + Fraction(11 * n**2, 120)
        + Fraction(9 * n, 20)
        + Fraction(T_EPSILON_NUMERATORS[n % 30], 360)
    )
    assert value.denominator == 1
    return value.numerator


def U(n: int) -> int:
    if n < 0:
        return 0
    value = Fraction(n, 3) + Fraction(U_EPSILON_NUMERATORS[n % 3], 3)
    assert value.denominator == 1
    return value.numerator


def P(n: int) -> int:
    if n < 0:
        return 0
    if n % 2 == 0:
        return T(n // 2) + T(n // 2 - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def S(n: int) -> int:
    if n < 0:
        return 0
    if n % 2 == 0:
        return U(n // 2)
    return U((n - 1) // 2 - 1)


def g(k: int, i: int) -> int:
    return (
        P(i)
        - S(i)
        - sum(P(i - 3 * k - nu) for nu in range(1, 6))
        + sum(
            P(i - 6 * k - mu - nu)
            for mu in range(1, 6)
            for nu in range(mu + 1, 6)
        )
        + sum(S(i - 5 * k - nu) for nu in range(1, 4))
    )


def p_terms(
    parity: int, residue: int, coefficient: int, multiplier: int, shift: int
) -> list[Term]:
    constant = parity - multiplier * residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            ("T", coefficient, (1, -2 * multiplier, half)),
            ("T", coefficient, (1, -2 * multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        ("T", coefficient, (1, -2 * multiplier, half - 1)),
        ("T", coefficient, (1, -2 * multiplier, half - 2)),
    ]


def s_terms(
    parity: int, residue: int, coefficient: int, multiplier: int, shift: int
) -> list[Term]:
    constant = parity - multiplier * residue - shift
    half = constant // 2 if constant % 2 == 0 else (constant - 3) // 2
    return [("U", coefficient, (1, -2 * multiplier, half))]


def consolidate(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[str, tuple[int, int, int]], int] = defaultdict(int)
    for function, coefficient, argument in terms:
        coefficients[(function, argument)] += coefficient
    return sorted(
        (function, coefficient, argument)
        for (function, argument), coefficient in coefficients.items()
        if coefficient
    )


def layer_terms(parity: int, residue: int) -> list[Term]:
    terms = p_terms(parity, residue, 1, 0, 4)
    terms += p_terms(parity, residue, 1, 0, 5)
    terms += p_terms(parity, residue, -1, 0, 9)
    for nu in range(1, 6):
        terms += p_terms(parity, residue, -1, 3, nu)
    for mu in range(1, 6):
        for nu in range(mu + 1, 6):
            terms += p_terms(parity, residue, 1, 6, mu + nu)
    for nu in range(1, 4):
        terms += s_terms(parity, residue, 1, 5, nu)
    return terms


def quantity_terms(residue: int, quantity: str) -> list[Term]:
    even = layer_terms(0, residue)
    if quantity == "A":
        return consolidate(even)
    odd = layer_terms(1, residue)
    return consolidate(
        [(function, 2 * coefficient, argument) for function, coefficient, argument in even]
        + [(function, -coefficient, argument) for function, coefficient, argument in odd]
    )


def domain_end(residue: int, quantity: str) -> tuple[int, int]:
    if quantity == "C":
        return ((15, 0), (15, 4), (15, 8), (15, 11))[residue]
    return ((15, 1), (15, 4), (15, 8), (15, 12))[residue]


def nonnegative_after_shift(slope: int, constant: int) -> bool:
    """Whether slope*(7+x)+constant has nonnegative x-coefficients."""
    return slope >= 0 and slope * T_START + constant >= 0


def bi_clean(poly: Bi) -> Bi:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def bi_add(*polys: Bi) -> Bi:
    result: dict[tuple[int, int], Fraction] = defaultdict(Fraction)
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] += coefficient
    return bi_clean(dict(result))


def bi_scale(poly: Bi, scalar: Fraction) -> Bi:
    return bi_clean({monomial: scalar * coefficient for monomial, coefficient in poly.items()})


def bi_mul(left: Bi, right: Bi) -> Bi:
    result: dict[tuple[int, int], Fraction] = defaultdict(Fraction)
    for (ax, az), a in left.items():
        for (bx, bz), b in right.items():
            result[(ax + bx, az + bz)] += a * b
    return bi_clean(dict(result))


def bi_pow(poly: Bi, exponent: int) -> Bi:
    result: Bi = {(0, 0): Fraction(1)}
    for _ in range(exponent):
        result = bi_mul(result, poly)
    return result


def substituted_argument(
    left: tuple[int, int], right: tuple[int, int], argument: tuple[int, int, int]
) -> Bi:
    _, argument_t, argument_constant = argument
    left_slope, left_constant = left
    right_slope, right_constant = right
    width_slope = right_slope - left_slope
    width_constant = right_constant - left_constant - 1
    return bi_clean({
        (0, 0): Fraction((left_slope + argument_t) * T_START + left_constant + argument_constant),
        (1, 0): Fraction(left_slope + argument_t),
        (0, 1): Fraction(width_slope * T_START + width_constant),
        (1, 1): Fraction(width_slope),
    })


def polynomial_part(function: str, argument: Bi) -> Bi:
    if function == "U":
        return bi_scale(argument, Fraction(1, 3))
    return bi_add(
        bi_scale(bi_pow(argument, 3), Fraction(1, 180)),
        bi_scale(bi_pow(argument, 2), Fraction(11, 120)),
        bi_scale(argument, Fraction(9, 20)),
    )


def fraction_record(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    epsilon_min = {"T": Fraction(91, 360), "U": Fraction(1, 3)}
    epsilon_max = {"T": Fraction(1), "U": Fraction(1)}

    for residue in range(4):
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            candidates = {(0, 0), end} | {
                (-argument[1], -argument[2]) for _, _, argument in terms
            }
            boundaries = {
                bound
                for bound in candidates
                if nonnegative_after_shift(bound[0], bound[1])
                and nonnegative_after_shift(end[0] - bound[0], end[1] - bound[1])
            }
            ordered = sorted(boundaries, key=lambda bound: (bound[0] * T_START + bound[1], *bound))
            assert ordered[0] == (0, 0) and ordered[-1] == end

            for left, right in zip(ordered, ordered[1:]):
                assert nonnegative_after_shift(right[0] - left[0], right[1] - left[1] - 1)
                active = []
                for function, coefficient, argument in terms:
                    threshold = (-argument[1], -argument[2])
                    if nonnegative_after_shift(left[0] - threshold[0], left[1] - threshold[1]):
                        active.append((function, coefficient, argument))

                record: dict[str, object] = {
                    "r": residue,
                    "q": quantity,
                    "l": list(left),
                    "u": [right[0], right[1] - 1],
                    "a": len(active),
                }
                if left[0] == 0 and right[0] == 0:
                    assert all(argument[1] == 0 for _, _, argument in active)
                    k = 4 * T_START + residue
                    values = []
                    for pair in range(left[1], right[1]):
                        current = g(k, 2 * pair)
                        if quantity == "C":
                            current = 2 * current - g(k, 2 * pair + 1)
                        assert current >= 0
                        values.append(current)
                    record["v"] = values
                    records.append(record)
                    continue

                bound: Bi = {}
                error = Fraction(0)
                for function, coefficient, argument in active:
                    term = polynomial_part(function, substituted_argument(left, right, argument))
                    bound = bi_add(bound, bi_scale(term, Fraction(coefficient)))
                    error += coefficient * (
                        epsilon_min[function] if coefficient > 0 else epsilon_max[function]
                    )
                bound = bi_add(bound, {(0, 0): error})
                assert max((z_degree for _, z_degree in bound), default=0) <= 3

                power_coefficients: list[Uni] = []
                for z_degree in range(4):
                    power_coefficients.append({
                        x_degree: coefficient
                        for (x_degree, current_z), coefficient in bound.items()
                        if current_z == z_degree
                    })
                bernstein = []
                for index in range(4):
                    coefficient: Uni = {}
                    for degree in range(index + 1):
                        scalar = Fraction(comb(index, degree), comb(3, degree))
                        coefficient = uni_add(
                            coefficient,
                            uni_scale(power_coefficients[degree], scalar),
                        )
                    assert all(value >= 0 for value in coefficient.values())
                    bernstein.append([
                        [degree, *fraction_record(value)]
                        for degree, value in sorted(coefficient.items())
                    ])
                record["b"] = bernstein
                records.append(record)
    return records


def verify_finite_bases() -> None:
    for k in range(2, 28):
        half = 15 * k // 2
        for i in range(0, half + 1, 2):
            assert g(k, i) >= 0
            if i + 1 <= half:
                assert 2 * g(k, i) - g(k, i + 1) >= 0


def main() -> None:
    verify_quasipolynomials()
    verify_finite_bases()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    exact_cells = sum("v" in record for record in records)
    bernstein = sum(4 for record in records if "b" in record)
    print("standard-library Fraction certificate passed")
    print("quasipolynomial rational generating functions verified exactly")
    print(f"affine cells: {len(records)}; exact initial cells: {exact_cells}; Bernstein polynomials: {bernstein}")
    print(f"independent certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
