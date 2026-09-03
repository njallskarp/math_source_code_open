#!/usr/bin/env python3
"""Exact affine-cell/Bernstein certificate for the Lucas (a,b)=(4,5) family.

The coefficient domain is QQ throughout.  No numerical approximation,
interpolation, root finding, or modular reconstruction is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction

import sympy as sp


T_START = 7
T_EPSILON_NUMERATORS = (
    360, 163, 248, 243, 136, 275, 288, 163, 248, 171,
    280, 203, 288, 163, 176, 315, 208, 203, 288, 91,
    320, 243, 208, 203, 216, 235, 248, 243, 208, 131,
)
R_EPSILON_NUMERATORS = (12, 5, 8, 9, 8, 5)
EXPECTED_CERTIFICATE_SHA256 = "f5f0756fce46c6c69c319a5895369ed15fd5a1cd14c7e36a3052250c9a8a13a4"

j, t, x, z = sp.symbols("j t x z")


def t_polynomial(n: sp.Expr) -> sp.Expr:
    return n**3 / sp.Integer(180) + sp.Rational(11, 120) * n**2 + sp.Rational(9, 20) * n


def r_polynomial(n: sp.Expr) -> sp.Expr:
    return n**2 / sp.Integer(12) + n / sp.Integer(2)


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


def R(n: int) -> int:
    if n < 0:
        return 0
    value = Fraction(n**2 + 6 * n, 12) + Fraction(R_EPSILON_NUMERATORS[n % 6], 12)
    assert value.denominator == 1
    return value.numerator


def P(n: int) -> int:
    """Partitions of n using parts 2,3,4,5."""
    if n < 0:
        return 0
    if n % 2 == 0:
        half = n // 2
        return T(half) + T(half - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def Q(n: int) -> int:
    """Partitions of n using parts 2,3,4."""
    if n < 0:
        return 0
    if n % 2 == 0:
        return R(n // 2)
    return R((n - 1) // 2 - 1)


def g(k: int, i: int) -> int:
    return (
        P(i - 5)
        - sum(P(i - 4 * k - nu) for nu in range(1, 6))
        + sum(
            P(i - 8 * k - mu - nu)
            for mu in range(1, 6)
            for nu in range(mu + 1, 6)
        )
        + sum(Q(i - 5 * k - nu) for nu in range(1, 5))
    )


def power_sum(power: int, y: sp.Expr) -> sp.Expr:
    if power == 0:
        return 1 / (1 - y)
    if power == 1:
        return y / (1 - y) ** 2
    if power == 2:
        return y * (1 + y) / (1 - y) ** 3
    if power == 3:
        return y * (1 + 4 * y + y**2) / (1 - y) ** 4
    raise ValueError(power)


def verify_quasipolynomials() -> None:
    """Verify both residue tables as identities of rational generating functions."""
    qvar, m = sp.symbols("qvar m")

    t_series = 0
    y = qvar**30
    for residue, epsilon in enumerate(T_EPSILON_NUMERATORS):
        expression = sp.Poly(
            sp.expand(t_polynomial(30 * m + residue) + sp.Rational(epsilon, 360)),
            m,
            domain=sp.QQ,
        )
        residue_series = sum(
            coefficient * power_sum(power[0], y)
            for power, coefficient in expression.terms()
        )
        t_series += qvar**residue * residue_series
    t_denominator = (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) * (1 - qvar**5)
    assert sp.cancel(t_series * t_denominator - 1) == 0

    r_series = 0
    y = qvar**6
    for residue, epsilon in enumerate(R_EPSILON_NUMERATORS):
        expression = sp.Poly(
            sp.expand(r_polynomial(6 * m + residue) + sp.Rational(epsilon, 12)),
            m,
            domain=sp.QQ,
        )
        residue_series = sum(
            coefficient * power_sum(power[0], y)
            for power, coefficient in expression.terms()
        )
        r_series += qvar**residue * residue_series
    r_denominator = (1 - qvar) * (1 - qvar**2) * (1 - qvar**3)
    assert sp.cancel(r_series * r_denominator - 1) == 0


# A term is (function, coefficient, (coefficient_of_j, coefficient_of_t, constant)).
Term = tuple[str, int, tuple[int, int, int]]


def p_terms(i_parity: int, k_parity: int, coefficient: int, k_multiplier: int, shift: int) -> list[Term]:
    constant = i_parity - k_multiplier * k_parity - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            ("T", coefficient, (1, -k_multiplier, half)),
            ("T", coefficient, (1, -k_multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        ("T", coefficient, (1, -k_multiplier, half - 1)),
        ("T", coefficient, (1, -k_multiplier, half - 2)),
    ]


def q_terms(i_parity: int, k_parity: int, coefficient: int, k_multiplier: int, shift: int) -> list[Term]:
    constant = i_parity - k_multiplier * k_parity - shift
    half = constant // 2 if constant % 2 == 0 else (constant - 1) // 2 - 1
    return [("R", coefficient, (1, -k_multiplier, half))]


def layer_terms(i_parity: int, k_parity: int) -> list[Term]:
    result = p_terms(i_parity, k_parity, 1, 0, 5)
    for nu in range(1, 6):
        result += p_terms(i_parity, k_parity, -1, 4, nu)
    for mu in range(1, 6):
        for nu in range(mu + 1, 6):
            result += p_terms(i_parity, k_parity, 1, 8, mu + nu)
    for nu in range(1, 5):
        result += q_terms(i_parity, k_parity, 1, 5, nu)
    return result


def consolidate(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[str, tuple[int, int, int]], int] = defaultdict(int)
    for function, coefficient, argument in terms:
        coefficients[(function, argument)] += coefficient
    return sorted(
        (function, coefficient, argument)
        for (function, argument), coefficient in coefficients.items()
        if coefficient
    )


def quantity_terms(k_parity: int, quantity: str) -> list[Term]:
    odd = layer_terms(1, k_parity)
    if quantity == "A":
        return consolidate(odd)
    even = layer_terms(2, k_parity)
    return consolidate(
        [(function, 2 * coefficient, argument) for function, coefficient, argument in odd]
        + [(function, -coefficient, argument) for function, coefficient, argument in even]
    )


def coefficients_nonnegative(expression: sp.Expr, variable: sp.Symbol) -> bool:
    polynomial = sp.Poly(sp.expand(expression), variable, domain=sp.QQ)
    return all(coefficient >= 0 for _, coefficient in polynomial.terms())


def affine_string(slope: int, constant: int) -> str:
    return str(sp.expand(slope * t + constant))


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    epsilon_min = {"T": sp.Rational(91, 360), "R": sp.Rational(5, 12)}
    epsilon_max = {"T": sp.Integer(1), "R": sp.Integer(1)}

    for k_parity in (0, 1):
        end = (10, 0 if k_parity == 0 else 5)
        for quantity in ("A", "C"):
            terms = quantity_terms(k_parity, quantity)
            boundaries = {(0, 0), end} | {
                (-argument[1], -argument[2])
                for _, _, argument in terms
            }
            ordered = sorted(
                boundaries,
                key=lambda bound: (
                    bound[0] * T_START + bound[1], bound[0], bound[1]
                ),
            )
            assert ordered[0] == (0, 0) and ordered[-1] == end

            for left, right in zip(ordered, ordered[1:]):
                gap = (right[0] - left[0]) * (T_START + x) + right[1] - left[1]
                assert coefficients_nonnegative(gap - 1, x), ("unstable cell", k_parity, quantity, left, right)

                lower = left[0] * t + left[1]
                upper = right[0] * t + right[1] - 1
                active: list[Term] = []
                for function, coefficient, argument in terms:
                    threshold = -argument[1] * t - argument[2]
                    if coefficients_nonnegative((lower - threshold).subs(t, T_START + x), x):
                        active.append((function, coefficient, argument))

                polynomial = sp.Integer(0)
                error_lower = sp.Integer(0)
                for function, coefficient, argument in active:
                    argument_expression = j + argument[1] * t + argument[2]
                    polynomial += coefficient * (
                        t_polynomial(argument_expression)
                        if function == "T"
                        else r_polynomial(argument_expression)
                    )
                    error_lower += coefficient * (
                        epsilon_min[function] if coefficient > 0 else epsilon_max[function]
                    )

                width = upper - lower
                assert coefficients_nonnegative(width.subs(t, T_START + x), x)
                on_unit_interval = sp.expand(polynomial + error_lower).subs(
                    j, lower + width * z
                ).subs(t, T_START + x)
                power = sp.Poly(sp.expand(on_unit_interval), z, domain=sp.QQ.frac_field(x))
                assert power.degree() <= 3
                power_coefficients = [power.coeff_monomial(z**degree) for degree in range(4)]
                bernstein = []
                for index in range(4):
                    coefficient = sp.expand(sum(
                        power_coefficients[degree]
                        * sp.binomial(index, degree)
                        / sp.binomial(3, degree)
                        for degree in range(index + 1)
                    ))
                    coefficient = sp.cancel(coefficient)
                    coefficient_polynomial = sp.Poly(coefficient, x, domain=sp.QQ)
                    assert coefficients_nonnegative(coefficient_polynomial.as_expr(), x), (
                        "negative Bernstein coefficient", k_parity, quantity, left, right, index, coefficient
                    )
                    bernstein.append(str(coefficient_polynomial.as_expr()))

                records.append({
                    "k_parity": k_parity,
                    "quantity": quantity,
                    "lower": affine_string(*left),
                    "upper": affine_string(right[0], right[1] - 1),
                    "active_terms": len(active),
                    "bernstein_QQ[x]": bernstein,
                })
    return records


def verify_finite_bases() -> None:
    for k in range(2, 2 * T_START + 1):
        for pair in range(5 * k):
            A = g(k, 2 * pair + 1)
            C = 2 * A - g(k, 2 * pair + 2)
            assert A >= 0, ("finite A", k, pair, A)
            assert C >= 0, ("finite C", k, pair, C)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-certificate", action="store_true")
    args = parser.parse_args()

    assert sp.__version__ == "1.14.0", sp.__version__
    assert min(T_EPSILON_NUMERATORS) == 91 and max(T_EPSILON_NUMERATORS) == 360
    assert min(R_EPSILON_NUMERATORS) == 5 and max(R_EPSILON_NUMERATORS) == 12
    verify_quasipolynomials()
    verify_finite_bases()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    if args.show_certificate:
        print(json.dumps(records, indent=2, sort_keys=True))
    print("exact QQ affine-cell/Bernstein certificate passed")
    print("quasipolynomial generating-function identities verified exactly")
    print(f"finite bases verified for 2 <= k <= {2 * T_START}")
    print(f"affine cells: {len(records)}; Bernstein polynomials: {4 * len(records)}")
    print(f"certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
