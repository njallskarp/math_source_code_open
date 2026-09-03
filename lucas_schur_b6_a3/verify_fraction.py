#!/usr/bin/env python3
"""Standard-library Fraction rebuild of the canonical (3,6) certificate."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from math import comb


T_START = 60
T_ALPHA_NUMERATORS = (279, 239, 259)
T_BETA_NUMERATORS = (
    2160, 905, 928, 2025, 608, 1225, 2160, 473, 1360, 1593,
    1040, 1225, 1728, 905, 928, 2025, 1040, 793, 2160, 473,
    1360, 2025, 608, 1225, 1728, 905, 1360, 1593, 1040, 793,
)
EXPECTED_CERTIFICATE_SHA256 = "0c44943d1ed5f03f72644d7d2876768948251d7f7145ec4d6eada6ea60eb211a"

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


POWER_SUM_NUMERATORS: tuple[Uni, ...] = (
    {0: Fraction(1)},
    {1: Fraction(1)},
    {1: Fraction(1), 2: Fraction(1)},
    {1: Fraction(1), 2: Fraction(4), 3: Fraction(1)},
    {1: Fraction(1), 2: Fraction(11), 3: Fraction(11), 4: Fraction(1)},
)


def residue_series_numerator(power_coefficients: Uni) -> Uni:
    result: Uni = {}
    for degree, coefficient in power_coefficients.items():
        correction = uni_pow(one_minus_power(1), 4 - degree)
        result = uni_add(
            result,
            uni_scale(uni_mul(POWER_SUM_NUMERATORS[degree], correction), coefficient),
        )
    return result


def t_expression(n: Uni, residue: int) -> Uni:
    return uni_add(
        uni_scale(uni_pow(n, 4), Fraction(1, 2160)),
        uni_scale(uni_pow(n, 3), Fraction(7, 540)),
        uni_scale(uni_pow(n, 2), Fraction(1, 8)),
        uni_scale(n, Fraction(T_ALPHA_NUMERATORS[residue % 3], 540)),
        {0: Fraction(T_BETA_NUMERATORS[residue], 2160)},
    )


def verify_quasipolynomial() -> None:
    numerator: Uni = {}
    for residue in range(30):
        n: Uni = {0: Fraction(residue), 1: Fraction(30)}
        residue_numerator = residue_series_numerator(t_expression(n, residue))
        lifted = {30 * degree + residue: value for degree, value in residue_numerator.items()}
        numerator = uni_add(numerator, lifted)
    target_denominator: Uni = {0: Fraction(1)}
    for part in (1, 2, 3, 3, 5):
        target_denominator = uni_mul(target_denominator, one_minus_power(part))
    assert uni_mul(numerator, target_denominator) == uni_pow(one_minus_power(30), 5)

    u_numerator: Uni = {}
    for residue in range(3):
        # U(3m+r)=m+1, with common denominator (1-y)^2.
        lifted = {3 * degree + residue: value for degree, value in {0: Fraction(1)}.items()}
        u_numerator = uni_add(u_numerator, lifted)
    u_denominator = uni_mul(one_minus_power(1), one_minus_power(3))
    assert uni_mul(u_numerator, u_denominator) == uni_pow(one_minus_power(3), 2)


def T(n: int) -> int:
    if n < 0:
        return 0
    result = (
        Fraction(n**4, 2160)
        + Fraction(7 * n**3, 540)
        + Fraction(n**2, 8)
        + Fraction(T_ALPHA_NUMERATORS[n % 3] * n, 540)
        + Fraction(T_BETA_NUMERATORS[n % 30], 2160)
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


def U(n: int) -> int:
    return n // 3 + 1 if n >= 0 else 0


def Q(n: int) -> int:
    if n < 0:
        return 0
    if n % 2 == 0:
        return U(n // 2)
    return U((n - 1) // 2 - 1)


def gaussian_layer(c: int, i: int) -> int:
    return (
        P(i)
        - Q(i)
        - sum(P(i - c - nu) for nu in range(1, 7))
        + sum(
            P(i - 2 * c - mu - nu)
            for mu in range(1, 7)
            for nu in range(mu + 1, 7)
        )
        + sum(Q(i - 2 * c - nu) for nu in range(1, 4))
    )


def remainder_layer(c: int, r: int) -> int:
    return gaussian_layer(c, r + 4) - gaussian_layer(c - 10, r - 26)


def p_terms(
    parity: int, residue: int, coefficient: int, multiplier: int, shift: int
) -> list[tuple[str, int, tuple[int, int, int]]]:
    constant = parity - multiplier * residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            ("T", coefficient, (1, -multiplier, half)),
            ("T", coefficient, (1, -multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        ("T", coefficient, (1, -multiplier, half - 1)),
        ("T", coefficient, (1, -multiplier, half - 2)),
    ]


def q_terms(
    parity: int, residue: int, coefficient: int, multiplier: int, shift: int
) -> list[Term]:
    constant = parity - multiplier * residue - shift
    if constant % 2 == 0:
        return [("U", coefficient, (1, -multiplier, constant // 2))]
    half = (constant - 1) // 2
    return [("U", coefficient, (1, -multiplier, half - 1))]


def k_terms(parity: int, residue: int) -> list[Term]:
    i_parity = parity + 4
    terms = p_terms(i_parity, residue, 1, 0, 0)
    terms += p_terms(i_parity, residue, -1, 0, 30)
    for nu in range(1, 7):
        terms += p_terms(i_parity, residue, -1, 1, nu)
        terms += p_terms(i_parity, residue, 1, 1, nu + 20)
    for mu in range(1, 7):
        for nu in range(mu + 1, 7):
            terms += p_terms(i_parity, residue, 1, 2, mu + nu)
            terms += p_terms(i_parity, residue, -1, 2, mu + nu + 10)
    terms += q_terms(i_parity, residue, -1, 0, 0)
    terms += q_terms(i_parity, residue, 1, 0, 30)
    for nu in range(1, 4):
        terms += q_terms(i_parity, residue, 1, 2, nu)
        terms += q_terms(i_parity, residue, -1, 2, nu + 10)
    return terms


def consolidate(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[str, tuple[int, int, int]], int] = defaultdict(int)
    for kind, coefficient, argument in terms:
        coefficients[(kind, argument)] += coefficient
    return sorted(
        (kind, coefficient, argument)
        for (kind, argument), coefficient in coefficients.items()
        if coefficient
    )


def quantity_terms(residue: int, quantity: str) -> list[Term]:
    even = k_terms(0, residue)
    if quantity == "A":
        return consolidate(even)
    odd = k_terms(1, residue)
    return consolidate(
        [(kind, 2 * coefficient, argument) for kind, coefficient, argument in even]
        + [(kind, -coefficient, argument) for kind, coefficient, argument in odd]
    )


def quantity_constant(quantity: str, pair: int) -> int:
    return 0


def domain_end(residue: int, quantity: str) -> tuple[int, int]:
    if residue == 0:
        return (3, -1 if quantity == "A" else -2)
    return (3, 0)


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


def t_common(argument: Bi) -> Bi:
    return bi_add(
        bi_scale(bi_pow(argument, 4), Fraction(1, 2160)),
        bi_scale(bi_pow(argument, 3), Fraction(7, 540)),
        bi_scale(bi_pow(argument, 2), Fraction(1, 8)),
    )


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    alpha_min = Fraction(min(T_ALPHA_NUMERATORS), 540)
    alpha_max = Fraction(max(T_ALPHA_NUMERATORS), 540)
    beta_min = Fraction(min(T_BETA_NUMERATORS), 2160)
    beta_max = Fraction(max(T_BETA_NUMERATORS), 2160)
    for residue in (0, 1):
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
                for kind, coefficient, argument in terms:
                    threshold = (-argument[1], -argument[2])
                    if nonnegative_after_shift(left[0] - threshold[0], left[1] - threshold[1]):
                        active.append((kind, coefficient, argument))
                record: dict[str, object] = {
                    "r": residue,
                    "q": quantity,
                    "l": list(left),
                    "u": [right[0], right[1] - 1],
                    "a": len(active),
                }
                if left[0] == 0 and right[0] == 0:
                    # These cells are checked at t=T_START below.  This is
                    # universal only because every active restricted-partition
                    # argument has zero t-slope; make that quantifier bridge an
                    # explicit executable obligation.
                    assert all(argument[1] == 0 for _, _, argument in active)
                    c = 2 * T_START + residue
                    values = []
                    for pair in range(left[1], right[1]):
                        current = remainder_layer(c, 2 * pair)
                        if quantity == "C":
                            current = 2 * current - remainder_layer(c, 2 * pair + 1)
                        assert current >= 0
                        values.append(current)
                    record["v"] = values
                    records.append(record)
                    continue

                bound: Bi = {}
                for kind, coefficient, argument in active:
                    affine = substituted_argument(left, right, argument)
                    if kind == "T":
                        term_bound = t_common(affine)
                    else:
                        term_bound = bi_scale(affine, Fraction(1, 3))
                    if kind == "T" and coefficient > 0:
                        term_bound = bi_add(
                            term_bound,
                            bi_scale(affine, alpha_min),
                            {(0, 0): beta_min},
                        )
                    elif kind == "T":
                        term_bound = bi_add(
                            term_bound,
                            bi_scale(affine, alpha_max),
                            {(0, 0): beta_max},
                        )
                    elif coefficient > 0:
                        term_bound = bi_add(term_bound, {(0, 0): Fraction(1, 3)})
                    else:
                        term_bound = bi_add(term_bound, {(0, 0): Fraction(1)})
                    bound = bi_add(bound, bi_scale(term_bound, Fraction(coefficient)))
                assert max((z_degree for _, z_degree in bound), default=0) <= 4

                power: list[Uni] = []
                for z_degree in range(5):
                    power.append({
                        x_degree: coefficient
                        for (x_degree, current_z), coefficient in bound.items()
                        if current_z == z_degree
                    })
                bernstein = []
                for index in range(5):
                    coefficient: Uni = {}
                    for degree in range(index + 1):
                        coefficient = uni_add(
                            coefficient,
                            uni_scale(power[degree], Fraction(comb(index, degree), comb(4, degree))),
                        )
                    assert all(value >= 0 for value in coefficient.values())
                    bernstein.append([
                        [degree, value.numerator, value.denominator]
                        for degree, value in sorted(coefficient.items())
                    ])
                record["b"] = bernstein
                records.append(record)
    return records


def evaluate_terms(terms: list[Term], quantity: str, parameter: int, pair: int) -> int:
    return quantity_constant(quantity, pair) + sum(
        coefficient * (T if kind == "T" else U)(
            pair + argument[1] * parameter + argument[2]
        )
        for kind, coefficient, argument in terms
    )


def verify_term_translation(max_c: int = 200) -> None:
    for c in range(16, max_c + 1):
        residue = c % 2
        parameter = (c - residue) // 2
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            for pair in range(end[0] * parameter + end[1]):
                expected = remainder_layer(c, 2 * pair)
                if quantity == "C":
                    expected = 2 * expected - remainder_layer(c, 2 * pair + 1)
                assert evaluate_terms(terms, quantity, parameter, pair) == expected


def verify_finite_parameters() -> None:
    for c in range(16, 2 * T_START):
        residue = c % 2
        parameter = (c - residue) // 2
        for quantity in ("A", "C"):
            end = domain_end(residue, quantity)
            for pair in range(end[0] * parameter + end[1]):
                current = remainder_layer(c, 2 * pair)
                if quantity == "C":
                    current = 2 * current - remainder_layer(c, 2 * pair + 1)
                assert current >= 0


def main() -> None:
    verify_quasipolynomial()
    verify_term_translation()
    verify_finite_parameters()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    exact_cells = sum("v" in record for record in records)
    bernstein_count = sum(5 for record in records if "b" in record)
    print("standard-library Fraction certificate passed")
    print("T and U quasipolynomial rational generating functions verified exactly")
    print("constant-cell t-independence verified from zero active slopes")
    print("affine T/U translation checked definitionally through c=200")
    print(f"finite recurrence parameters verified for 16 <= c < {2 * T_START}")
    print(
        f"affine cells: {len(records)}; exact initial cells: {exact_cells}; "
        f"Bernstein polynomials: {bernstein_count}"
    )
    print(f"independent certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
