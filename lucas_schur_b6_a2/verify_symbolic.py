#!/usr/bin/env python3
"""Exact affine-cell certificate for the width-six KOH remainder.

This is initially an executable research certificate.  The accompanying
mathematical write-up records how its two inequalities imply Lucas-Schur
positivity for the canonical (a,b)=(2,6) ray.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction

import sympy as sp


T_START = 60
T_ALPHA_NUMERATORS = (279, 239, 259)
T_BETA_NUMERATORS = (
    2160, 905, 928, 2025, 608, 1225, 2160, 473, 1360, 1593,
    1040, 1225, 1728, 905, 928, 2025, 1040, 793, 2160, 473,
    1360, 2025, 608, 1225, 1728, 905, 1360, 1593, 1040, 793,
)
EXPECTED_CERTIFICATE_SHA256 = "ea8e69d642ad4d74cc3d0b83c3b35ace1061317414013c41e366c17113da35da"

j, t, x, z = sp.symbols("j t x z")


def t_common(n: sp.Expr) -> sp.Expr:
    return n**4 / sp.Integer(2160) + sp.Rational(7, 540) * n**3 + n**2 / sp.Integer(8)


def t_residue_polynomial(n: sp.Expr, residue: int) -> sp.Expr:
    return (
        t_common(n)
        + sp.Rational(T_ALPHA_NUMERATORS[residue % 3], 540) * n
        + sp.Rational(T_BETA_NUMERATORS[residue], 2160)
    )


def T(n: int) -> int:
    """Partitions of n using parts 1,2,3,3,5."""
    if n < 0:
        return 0
    value = (
        Fraction(n**4, 2160)
        + Fraction(7 * n**3, 540)
        + Fraction(n**2, 8)
        + Fraction(T_ALPHA_NUMERATORS[n % 3] * n, 540)
        + Fraction(T_BETA_NUMERATORS[n % 30], 2160)
    )
    assert value.denominator == 1
    return value.numerator


def P(n: int) -> int:
    """Partitions of n using parts 2,3,4,5,6."""
    if n < 0:
        return 0
    if n % 2 == 0:
        return T(n // 2) + T(n // 2 - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def gaussian_layer(c: int, i: int) -> int:
    """[q^i](1-q)({c+6 choose 6}_q-{3c+2 choose 2}_q), i<=3c."""
    return (
        P(i)
        - sum(P(i - c - nu) for nu in range(1, 7))
        + sum(
            P(i - 2 * c - mu - nu)
            for mu in range(1, 7)
            for nu in range(mu + 1, 7)
        )
        - int(i >= 0 and i % 2 == 0)
    )


def remainder_layer(c: int, r: int) -> int:
    """Schur layer k(c,r) of the ordinary 10-step recurrence remainder."""
    return gaussian_layer(c, r + 3) - gaussian_layer(c - 10, r - 27)


def power_sum(power: int, y: sp.Expr) -> sp.Expr:
    if power == 0:
        return 1 / (1 - y)
    if power == 1:
        return y / (1 - y) ** 2
    if power == 2:
        return y * (1 + y) / (1 - y) ** 3
    if power == 3:
        return y * (1 + 4 * y + y**2) / (1 - y) ** 4
    if power == 4:
        return y * (1 + 11 * y + 11 * y**2 + y**3) / (1 - y) ** 5
    raise ValueError(power)


def verify_quasipolynomial() -> None:
    qvar, m = sp.symbols("qvar m")
    series = 0
    y = qvar**30
    for residue in range(30):
        expression = sp.Poly(
            sp.expand(t_residue_polynomial(30 * m + residue, residue)),
            m,
            domain=sp.QQ,
        )
        residue_series = sum(
            coefficient * power_sum(power[0], y)
            for power, coefficient in expression.terms()
        )
        series += qvar**residue * residue_series
    denominator = (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) ** 2 * (1 - qvar**5)
    assert sp.cancel(series * denominator - 1) == 0


# A term is (coefficient, (coefficient_of_j, coefficient_of_t, constant)).
Term = tuple[int, tuple[int, int, int]]


def p_terms(
    r_parity: int,
    c_residue: int,
    coefficient: int,
    c_multiplier: int,
    shift: int,
) -> list[Term]:
    """Expand P(2j+r_parity-c_multiplier*c-shift), c=2t+rho."""
    constant = r_parity - c_multiplier * c_residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            (coefficient, (1, -c_multiplier, half)),
            (coefficient, (1, -c_multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        (coefficient, (1, -c_multiplier, half - 1)),
        (coefficient, (1, -c_multiplier, half - 2)),
    ]


def k_terms(r_parity: int, c_residue: int) -> list[Term]:
    """Translate k(c,r), where r=2j for parity 0 or r=2j+1 for parity 1."""
    # i=r+3.  The width-two V terms cancel between i and i-30.
    i_parity = r_parity + 3
    result = p_terms(i_parity, c_residue, 1, 0, 0)
    result += p_terms(i_parity, c_residue, -1, 0, 30)
    for nu in range(1, 7):
        result += p_terms(i_parity, c_residue, -1, 1, nu)
        result += p_terms(i_parity, c_residue, 1, 1, nu + 20)
    for mu in range(1, 7):
        for nu in range(mu + 1, 7):
            result += p_terms(i_parity, c_residue, 1, 2, mu + nu)
            result += p_terms(i_parity, c_residue, -1, 2, mu + nu + 10)
    return result


def consolidate(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[int, int, int], int] = defaultdict(int)
    for coefficient, argument in terms:
        coefficients[argument] += coefficient
    return sorted(
        (coefficient, argument)
        for argument, coefficient in coefficients.items()
        if coefficient
    )


def quantity_terms(c_residue: int, quantity: str) -> list[Term]:
    even = k_terms(0, c_residue)
    if quantity == "A":
        return consolidate(even)
    odd = k_terms(1, c_residue)
    return consolidate(
        [(2 * coefficient, argument) for coefficient, argument in even]
        + [(-coefficient, argument) for coefficient, argument in odd]
    )


def quantity_constant(quantity: str, pair: int) -> int:
    """The uncancelled width-two layer for r+3<30."""
    return int(quantity == "C" and pair < 13)


def domain_end(c_residue: int, quantity: str) -> tuple[int, int]:
    # Exclusive upper bounds for even layers and complete even/odd pairs.
    if c_residue == 0:
        return (3, -1)
    return (3, 1 if quantity == "A" else 0)


def coefficients_nonnegative(expression: sp.Expr, variable: sp.Symbol) -> bool:
    polynomial = sp.Poly(sp.expand(expression), variable, domain=sp.QQ)
    return all(coefficient >= 0 for _, coefficient in polynomial.terms())


def affine_string(slope: int, constant: int) -> str:
    return str(sp.expand(slope * t + constant))


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    alpha_min = sp.Rational(min(T_ALPHA_NUMERATORS), 540)
    alpha_max = sp.Rational(max(T_ALPHA_NUMERATORS), 540)
    beta_min = sp.Rational(min(T_BETA_NUMERATORS), 2160)
    beta_max = sp.Rational(max(T_BETA_NUMERATORS), 2160)

    for residue in (0, 1):
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            candidates = {(0, 0), end} | {
                (-argument[1], -argument[2]) for _, argument in terms
            }
            if quantity == "C":
                candidates.add((0, 13))
            boundaries: set[tuple[int, int]] = set()
            for bound in candidates:
                lower_test = bound[0] * (T_START + x) + bound[1]
                end_test = (end[0] - bound[0]) * (T_START + x) + end[1] - bound[1]
                if coefficients_nonnegative(lower_test, x) and coefficients_nonnegative(end_test, x):
                    boundaries.add(bound)
            ordered = sorted(
                boundaries,
                key=lambda bound: (bound[0] * T_START + bound[1], bound[0], bound[1]),
            )
            assert ordered[0] == (0, 0) and ordered[-1] == end

            for left, right in zip(ordered, ordered[1:]):
                gap = (right[0] - left[0]) * (T_START + x) + right[1] - left[1]
                assert coefficients_nonnegative(gap - 1, x), (
                    "unstable cell", residue, quantity, left, right, gap
                )
                lower = left[0] * t + left[1]
                upper = right[0] * t + right[1] - 1
                active: list[Term] = []
                for coefficient, argument in terms:
                    threshold = -argument[1] * t - argument[2]
                    if coefficients_nonnegative((lower - threshold).subs(t, T_START + x), x):
                        active.append((coefficient, argument))

                if left[0] == 0 and right[0] == 0:
                    c = 2 * T_START + residue
                    values = []
                    for pair in range(left[1], right[1]):
                        current = remainder_layer(c, 2 * pair)
                        if quantity == "C":
                            current = 2 * current - remainder_layer(c, 2 * pair + 1)
                        assert current >= 0
                        values.append(current)
                    records.append({
                        "c_mod_2": residue,
                        "quantity": quantity,
                        "lower": affine_string(*left),
                        "upper": affine_string(right[0], right[1] - 1),
                        "active_terms": len(active),
                        "exact_values": values,
                    })
                    continue

                polynomial = sp.Integer(0)
                for coefficient, argument in active:
                    argument_expression = j + argument[1] * t + argument[2]
                    if coefficient > 0:
                        bound = t_common(argument_expression) + alpha_min * argument_expression + beta_min
                    else:
                        bound = t_common(argument_expression) + alpha_max * argument_expression + beta_max
                    polynomial += coefficient * bound

                width = upper - lower
                assert coefficients_nonnegative(width.subs(t, T_START + x), x)
                on_unit_interval = sp.expand(polynomial).subs(
                    j, lower + width * z
                ).subs(t, T_START + x)
                power = sp.Poly(sp.expand(on_unit_interval), z, domain=sp.QQ.frac_field(x))
                assert power.degree() <= 4
                power_coefficients = [power.coeff_monomial(z**degree) for degree in range(5)]
                bernstein: list[str] = []
                for index in range(5):
                    coefficient = sp.cancel(sum(
                        power_coefficients[degree]
                        * sp.binomial(index, degree)
                        / sp.binomial(4, degree)
                        for degree in range(index + 1)
                    ))
                    coefficient_polynomial = sp.Poly(coefficient, x, domain=sp.QQ)
                    assert coefficients_nonnegative(coefficient_polynomial.as_expr(), x), (
                        "negative Bernstein coefficient",
                        residue,
                        quantity,
                        left,
                        right,
                        index,
                        coefficient,
                    )
                    bernstein.append(str(coefficient_polynomial.as_expr()))
                records.append({
                    "c_mod_2": residue,
                    "quantity": quantity,
                    "lower": affine_string(*left),
                    "upper": affine_string(right[0], right[1] - 1),
                    "active_terms": len(active),
                    "bernstein_QQ[x]": bernstein,
                })
    return records


def evaluate_terms(terms: list[Term], quantity: str, parameter: int, pair: int) -> int:
    return quantity_constant(quantity, pair) + sum(
        coefficient * T(pair + argument[1] * parameter + argument[2])
        for coefficient, argument in terms
    )


def verify_term_translation(max_c: int = 200) -> None:
    for c in range(16, max_c + 1):
        residue = c % 2
        parameter = (c - residue) // 2
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            pair_count = end[0] * parameter + end[1]
            for pair in range(pair_count):
                expected = remainder_layer(c, 2 * pair)
                if quantity == "C":
                    expected = 2 * expected - remainder_layer(c, 2 * pair + 1)
                assert evaluate_terms(terms, quantity, parameter, pair) == expected, (
                    "term translation", c, quantity, pair
                )


def verify_finite_bases() -> None:
    for c in range(16, 2 * T_START):
        residue = c % 2
        parameter = (c - residue) // 2
        for quantity in ("A", "C"):
            end = domain_end(residue, quantity)
            for pair in range(end[0] * parameter + end[1]):
                current = remainder_layer(c, 2 * pair)
                if quantity == "C":
                    current = 2 * current - remainder_layer(c, 2 * pair + 1)
                assert current >= 0, ("finite sign", c, quantity, pair, current)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-certificate", action="store_true")
    args = parser.parse_args()

    assert sp.__version__ == "1.14.0", sp.__version__
    verify_quasipolynomial()
    verify_term_translation()
    verify_finite_bases()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    if args.show_certificate:
        print(json.dumps(records, indent=2, sort_keys=True))
    exact_cells = sum("exact_values" in record for record in records)
    bernstein_count = sum(len(record.get("bernstein_QQ[x]", [])) for record in records)
    print("exact QQ affine-cell/Bernstein certificate passed")
    print("T quasipolynomial generating-function identity verified exactly")
    print("affine T translation checked definitionally through c=200")
    print(f"finite recurrence parameters verified for 16 <= c < {2 * T_START}")
    print(
        f"affine cells: {len(records)}; exact initial cells: {exact_cells}; "
        f"Bernstein polynomials: {bernstein_count}"
    )
    print(f"certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
