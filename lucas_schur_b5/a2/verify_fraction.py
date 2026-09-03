#!/usr/bin/env python3
"""Standard-library Fraction rebuild of the canonical Lucas (2,5) certificate."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from math import comb


T_START = 14
T_EPSILON_NUMERATORS = (
    360, 163, 248, 243, 136, 275, 288, 163, 248, 171,
    280, 203, 288, 163, 176, 315, 208, 203, 288, 91,
    320, 243, 208, 203, 216, 235, 248, 243, 208, 131,
)
EXPECTED_CERTIFICATE_SHA256 = "212b4173408454f6c75298a484dad40abcab29aacd319644d8c1a5ea9cd5023d"

Uni = dict[int, Fraction]
Bi = dict[tuple[int, int], Fraction]
Term = tuple[int, tuple[int, int, int]]


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


POWER_SUM_NUMERATORS: tuple[Uni, ...] = (
    {0: Fraction(1)},
    {1: Fraction(1)},
    {1: Fraction(1), 2: Fraction(1)},
    {1: Fraction(1), 2: Fraction(4), 3: Fraction(1)},
)


def residue_series_numerator(power_coefficients: Uni) -> Uni:
    result: Uni = {}
    for degree, coefficient in power_coefficients.items():
        correction = uni_pow(one_minus_power(1), 3 - degree)
        result = uni_add(
            result,
            uni_scale(uni_mul(POWER_SUM_NUMERATORS[degree], correction), coefficient),
        )
    return result


def verify_quasipolynomial() -> None:
    numerator: Uni = {}
    for residue, epsilon in enumerate(T_EPSILON_NUMERATORS):
        n: Uni = {0: Fraction(residue), 1: Fraction(30)}
        expression = uni_add(
            uni_scale(uni_pow(n, 3), Fraction(1, 180)),
            uni_scale(uni_pow(n, 2), Fraction(11, 120)),
            uni_scale(n, Fraction(9, 20)),
            {0: Fraction(epsilon, 360)},
        )
        residue_numerator = residue_series_numerator(expression)
        lifted = {30 * degree + residue: value for degree, value in residue_numerator.items()}
        numerator = uni_add(numerator, lifted)
    target_denominator: Uni = {0: Fraction(1)}
    for part in (1, 2, 3, 5):
        target_denominator = uni_mul(target_denominator, one_minus_power(part))
    assert uni_mul(numerator, target_denominator) == uni_pow(one_minus_power(30), 4)


def T(n: int) -> int:
    if n < 0:
        return 0
    result = (
        Fraction(n**3, 180)
        + Fraction(11 * n**2, 120)
        + Fraction(9 * n, 20)
        + Fraction(T_EPSILON_NUMERATORS[n % 30], 360)
    )
    assert result.denominator == 1
    return result.numerator


def P(n: int) -> int:
    if n < 0:
        return 0
    if n % 2 == 0:
        return T(n // 2) + T(n // 2 - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def V(n: int) -> int:
    return int(n >= 0 and n % 2 == 0)


def g(k: int, i: int) -> int:
    return (
        P(i)
        - V(i)
        - sum(P(i - 2 * k - nu) for nu in range(1, 6))
        + sum(
            P(i - 4 * k - mu - nu)
            for mu in range(1, 6)
            for nu in range(mu + 1, 6)
        )
    )


def p_terms(
    parity: int, residue: int, coefficient: int, multiplier: int, shift: int
) -> list[Term]:
    constant = parity - multiplier * residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            (coefficient, (1, -multiplier, half)),
            (coefficient, (1, -multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        (coefficient, (1, -multiplier, half - 1)),
        (coefficient, (1, -multiplier, half - 2)),
    ]


def layer_terms(parity: int, residue: int) -> list[Term]:
    terms = p_terms(parity, residue, 1, 0, 0)
    for nu in range(1, 6):
        terms += p_terms(parity, residue, -1, 2, nu)
    for mu in range(1, 6):
        for nu in range(mu + 1, 6):
            terms += p_terms(parity, residue, 1, 4, mu + nu)
    return terms


def consolidate(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[int, int, int], int] = defaultdict(int)
    for coefficient, argument in terms:
        coefficients[argument] += coefficient
    return sorted(
        (coefficient, argument)
        for argument, coefficient in coefficients.items()
        if coefficient
    )


def quantity_terms(residue: int, quantity: str) -> tuple[list[Term], int]:
    odd = layer_terms(1, residue)
    if quantity == "A":
        return consolidate(odd), 0
    even = layer_terms(2, residue)
    return consolidate(
        [(2 * coefficient, argument) for coefficient, argument in odd]
        + [(-coefficient, argument) for coefficient, argument in even]
    ), 1


def domain_end(residue: int, quantity: str) -> tuple[int, int]:
    if residue == 0:
        return (5, 0)
    return (5, 3 if quantity == "A" else 2)


def nonnegative_after_shift(slope: int, constant: int) -> bool:
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


def t_polynomial(argument: Bi) -> Bi:
    return bi_add(
        bi_scale(bi_pow(argument, 3), Fraction(1, 180)),
        bi_scale(bi_pow(argument, 2), Fraction(11, 120)),
        bi_scale(argument, Fraction(9, 20)),
    )


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    epsilon_min = Fraction(91, 360)
    epsilon_max = Fraction(1)
    for residue in (0, 1):
        for quantity in ("A", "C"):
            terms, exact_constant = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            candidates = {(0, 0), end} | {
                (-argument[1], -argument[2]) for _, argument in terms
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
                for coefficient, argument in terms:
                    threshold = (-argument[1], -argument[2])
                    if nonnegative_after_shift(left[0] - threshold[0], left[1] - threshold[1]):
                        active.append((coefficient, argument))
                record: dict[str, object] = {
                    "r": residue,
                    "q": quantity,
                    "l": list(left),
                    "u": [right[0], right[1] - 1],
                    "a": len(active),
                }
                if left[0] == 0 and right[0] == 0:
                    assert all(argument[1] == 0 for _, argument in active)
                    k = 2 * T_START + residue
                    values = []
                    for pair in range(left[1], right[1]):
                        current = g(k, 2 * pair + 1)
                        if quantity == "C":
                            current = 2 * current - g(k, 2 * pair + 2)
                        assert current >= 0
                        values.append(current)
                    record["v"] = values
                    records.append(record)
                    continue

                bound: Bi = {(0, 0): Fraction(exact_constant)}
                error = Fraction(0)
                for coefficient, argument in active:
                    bound = bi_add(
                        bound,
                        bi_scale(t_polynomial(substituted_argument(left, right, argument)), Fraction(coefficient)),
                    )
                    error += coefficient * (epsilon_min if coefficient > 0 else epsilon_max)
                bound = bi_add(bound, {(0, 0): error})
                assert max((z_degree for _, z_degree in bound), default=0) <= 3

                power: list[Uni] = []
                for z_degree in range(4):
                    power.append({
                        x_degree: coefficient
                        for (x_degree, current_z), coefficient in bound.items()
                        if current_z == z_degree
                    })
                bernstein = []
                for index in range(4):
                    coefficient: Uni = {}
                    for degree in range(index + 1):
                        coefficient = uni_add(
                            coefficient,
                            uni_scale(power[degree], Fraction(comb(index, degree), comb(3, degree))),
                        )
                    assert all(value >= 0 for value in coefficient.values())
                    bernstein.append([
                        [degree, value.numerator, value.denominator]
                        for degree, value in sorted(coefficient.items())
                    ])
                record["b"] = bernstein
                records.append(record)
    return records


def verify_finite_bases() -> None:
    for k in range(3, 2 * T_START):
        residue = k % 2
        parameter = (k - residue) // 2
        for quantity in ("A", "C"):
            end = domain_end(residue, quantity)
            for pair in range(end[0] * parameter + end[1]):
                current = g(k, 2 * pair + 1)
                if quantity == "C":
                    current = 2 * current - g(k, 2 * pair + 2)
                assert current >= 0


def main() -> None:
    verify_quasipolynomial()
    verify_finite_bases()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    exact_cells = sum("v" in record for record in records)
    bernstein_count = sum(4 for record in records if "b" in record)
    print("standard-library Fraction certificate passed")
    print("T quasipolynomial rational generating function verified exactly")
    print(f"finite bases verified for 3 <= k < {2 * T_START}")
    print(
        f"affine cells: {len(records)}; exact initial cells: {exact_cells}; "
        f"Bernstein polynomials: {bernstein_count}"
    )
    print(f"independent certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
