#!/usr/bin/env python3
"""Exact affine-cell certificate for canonical Lucas (a,b)=(2,5)."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction

import sympy as sp


T_START = 14
T_EPSILON_NUMERATORS = (
    360, 163, 248, 243, 136, 275, 288, 163, 248, 171,
    280, 203, 288, 163, 176, 315, 208, 203, 288, 91,
    320, 243, 208, 203, 216, 235, 248, 243, 208, 131,
)
EXPECTED_CERTIFICATE_SHA256 = "73b29979e55d22ac28008c5b3f2f9298386623186a1972238b8c21bba3a57c64"

j, t, x, z = sp.symbols("j t x z")


def t_polynomial(n: sp.Expr) -> sp.Expr:
    return n**3 / sp.Integer(180) + sp.Rational(11, 120) * n**2 + sp.Rational(9, 20) * n


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
    """Partitions of n using parts 2,3,4,5."""
    if n < 0:
        return 0
    if n % 2 == 0:
        return T(n // 2) + T(n // 2 - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def V(n: int) -> int:
    """Partitions of n using the single part 2."""
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


def verify_quasipolynomial() -> None:
    qvar, m = sp.symbols("qvar m")
    series = 0
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
        series += qvar**residue * residue_series
    denominator = (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) * (1 - qvar**5)
    assert sp.cancel(series * denominator - 1) == 0


# A term is (coefficient, (coefficient_of_j, coefficient_of_t, constant)).
Term = tuple[int, tuple[int, int, int]]


def p_terms(
    i_parity: int,
    k_residue: int,
    coefficient: int,
    k_multiplier: int,
    shift: int,
) -> list[Term]:
    """Expand P(i-k_multiplier*k-shift), with i=2j+p and k=2t+r."""
    constant = i_parity - k_multiplier * k_residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            (coefficient, (1, -k_multiplier, half)),
            (coefficient, (1, -k_multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        (coefficient, (1, -k_multiplier, half - 1)),
        (coefficient, (1, -k_multiplier, half - 2)),
    ]


def layer_terms(i_parity: int, k_residue: int) -> list[Term]:
    result = p_terms(i_parity, k_residue, 1, 0, 0)
    for nu in range(1, 6):
        result += p_terms(i_parity, k_residue, -1, 2, nu)
    for mu in range(1, 6):
        for nu in range(mu + 1, 6):
            result += p_terms(i_parity, k_residue, 1, 4, mu + nu)
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


def quantity_terms(k_residue: int, quantity: str) -> tuple[list[Term], int]:
    odd = layer_terms(1, k_residue)
    if quantity == "A":
        return consolidate(odd), 0
    even = layer_terms(2, k_residue)
    # V(2j+1)=0 and V(2j+2)=1, hence 2g(2j+1)-g(2j+2)
    # has the exact additional constant +1.
    return consolidate(
        [(2 * coefficient, argument) for coefficient, argument in odd]
        + [(-coefficient, argument) for coefficient, argument in even]
    ), 1


def domain_end(k_residue: int, quantity: str) -> tuple[int, int]:
    if k_residue == 0:
        return (5, 0)
    return (5, 3 if quantity == "A" else 2)


def coefficients_nonnegative(expression: sp.Expr, variable: sp.Symbol) -> bool:
    polynomial = sp.Poly(sp.expand(expression), variable, domain=sp.QQ)
    return all(coefficient >= 0 for _, coefficient in polynomial.terms())


def affine_string(slope: int, constant: int) -> str:
    return str(sp.expand(slope * t + constant))


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    epsilon_min = sp.Rational(91, 360)
    epsilon_max = sp.Integer(1)

    for residue in (0, 1):
        for quantity in ("A", "C"):
            terms, exact_constant = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            candidates = {(0, 0), end} | {
                (-argument[1], -argument[2]) for _, argument in terms
            }
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
                    assert all(argument[1] == 0 for _, argument in active)
                    k = 2 * T_START + residue
                    values = []
                    for pair in range(left[1], right[1]):
                        current = g(k, 2 * pair + 1)
                        if quantity == "C":
                            current = 2 * current - g(k, 2 * pair + 2)
                        assert current >= 0
                        values.append(current)
                    records.append({
                        "k_mod_2": residue,
                        "quantity": quantity,
                        "lower": affine_string(*left),
                        "upper": affine_string(right[0], right[1] - 1),
                        "active_terms": len(active),
                        "exact_values": values,
                    })
                    continue

                polynomial = sp.Integer(exact_constant)
                error_lower = sp.Integer(0)
                for coefficient, argument in active:
                    argument_expression = j + argument[1] * t + argument[2]
                    polynomial += coefficient * t_polynomial(argument_expression)
                    error_lower += coefficient * (epsilon_min if coefficient > 0 else epsilon_max)

                width = upper - lower
                assert coefficients_nonnegative(width.subs(t, T_START + x), x)
                on_unit_interval = sp.expand(polynomial + error_lower).subs(
                    j, lower + width * z
                ).subs(t, T_START + x)
                power = sp.Poly(sp.expand(on_unit_interval), z, domain=sp.QQ.frac_field(x))
                assert power.degree() <= 3
                power_coefficients = [power.coeff_monomial(z**degree) for degree in range(4)]
                bernstein: list[str] = []
                for index in range(4):
                    coefficient = sp.cancel(sum(
                        power_coefficients[degree]
                        * sp.binomial(index, degree)
                        / sp.binomial(3, degree)
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
                    "k_mod_2": residue,
                    "quantity": quantity,
                    "lower": affine_string(*left),
                    "upper": affine_string(right[0], right[1] - 1),
                    "active_terms": len(active),
                    "bernstein_QQ[x]": bernstein,
                })
    return records


def evaluate_terms(terms: list[Term], constant: int, parameter: int, pair: int) -> int:
    return constant + sum(
        coefficient * T(pair + argument[1] * parameter + argument[2])
        for coefficient, argument in terms
    )


def verify_term_translation(max_k: int = 200) -> None:
    for k in range(3, max_k + 1):
        residue = k % 2
        parameter = (k - residue) // 2
        for quantity in ("A", "C"):
            terms, constant = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            pair_count = end[0] * parameter + end[1]
            for pair in range(pair_count):
                expected = g(k, 2 * pair + 1)
                if quantity == "C":
                    expected = 2 * expected - g(k, 2 * pair + 2)
                assert evaluate_terms(terms, constant, parameter, pair) == expected, (
                    "term translation", k, quantity, pair
                )


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
                assert current >= 0, ("finite sign", k, quantity, pair, current)


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
    print("affine T translation checked definitionally through k=200")
    print(f"finite bases verified for 3 <= k < {2 * T_START}")
    print(
        f"affine cells: {len(records)}; exact initial cells: {exact_cells}; "
        f"Bernstein polynomials: {bernstein_count}"
    )
    print(f"certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
