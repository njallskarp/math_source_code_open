#!/usr/bin/env python3
"""Exact affine-cell certificate for canonical Lucas (a,b)=(3,5).

All symbolic arithmetic is over QQ.  The certificate proves the adjacent
Gaussian-layer inequalities used by the two-row Lucas Schur pairing; it does
not infer a universal statement from interpolation or a finite experiment.
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
U_EPSILON_NUMERATORS = (3, 2, 1)
EXPECTED_CERTIFICATE_SHA256 = "b15738db8e9f1041b95d72eda84807d858d29ca5616b504e275f5d1d9f127b1b"

j, t, x, z = sp.symbols("j t x z")


def t_polynomial(n: sp.Expr) -> sp.Expr:
    return n**3 / sp.Integer(180) + sp.Rational(11, 120) * n**2 + sp.Rational(9, 20) * n


def u_polynomial(n: sp.Expr) -> sp.Expr:
    return n / sp.Integer(3)


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
    """Partitions of n using parts 2,3,4,5."""
    if n < 0:
        return 0
    if n % 2 == 0:
        half = n // 2
        return T(half) + T(half - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def S(n: int) -> int:
    """Partitions of n using parts 2,3."""
    if n < 0:
        return 0
    if n % 2 == 0:
        return U(n // 2)
    return U((n - 1) // 2 - 1)


def g(k: int, i: int) -> int:
    """Lower-half Schur layer [q^i](1-q)J_k(q)."""
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
    """Prove the residue tables by rational generating-function identities."""
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
    denominator = (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) * (1 - qvar**5)
    assert sp.cancel(t_series * denominator - 1) == 0

    u_series = 0
    y = qvar**3
    for residue, epsilon in enumerate(U_EPSILON_NUMERATORS):
        expression = sp.Poly(
            sp.expand(u_polynomial(3 * m + residue) + sp.Rational(epsilon, 3)),
            m,
            domain=sp.QQ,
        )
        residue_series = sum(
            coefficient * power_sum(power[0], y)
            for power, coefficient in expression.terms()
        )
        u_series += qvar**residue * residue_series
    denominator = (1 - qvar) * (1 - qvar**3)
    assert sp.cancel(u_series * denominator - 1) == 0


# A term is (function, coefficient, (coefficient_of_j, coefficient_of_t, constant)).
Term = tuple[str, int, tuple[int, int, int]]


def p_terms(
    i_parity: int,
    k_residue: int,
    coefficient: int,
    k_multiplier: int,
    shift: int,
) -> list[Term]:
    """Expand P(i-k_multiplier*k-shift), with i=2j+i_parity, k=4t+r."""
    constant = i_parity - k_multiplier * k_residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            ("T", coefficient, (1, -2 * k_multiplier, half)),
            ("T", coefficient, (1, -2 * k_multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        ("T", coefficient, (1, -2 * k_multiplier, half - 1)),
        ("T", coefficient, (1, -2 * k_multiplier, half - 2)),
    ]


def s_terms(
    i_parity: int,
    k_residue: int,
    coefficient: int,
    k_multiplier: int,
    shift: int,
) -> list[Term]:
    """Expand S(i-k_multiplier*k-shift), using U(n)=#[a+3b=n]."""
    constant = i_parity - k_multiplier * k_residue - shift
    if constant % 2 == 0:
        half = constant // 2
    else:
        half = (constant - 3) // 2
    return [("U", coefficient, (1, -2 * k_multiplier, half))]


def layer_terms(i_parity: int, k_residue: int) -> list[Term]:
    # P(n)-S(n)=P(n-4)+P(n-5)-P(n-9), exactly.  Keeping this
    # denominator factorization intact avoids throwing away the correlated
    # periodic cancellation in P-S.
    result = p_terms(i_parity, k_residue, 1, 0, 4)
    result += p_terms(i_parity, k_residue, 1, 0, 5)
    result += p_terms(i_parity, k_residue, -1, 0, 9)
    for nu in range(1, 6):
        result += p_terms(i_parity, k_residue, -1, 3, nu)
    for mu in range(1, 6):
        for nu in range(mu + 1, 6):
            result += p_terms(i_parity, k_residue, 1, 6, mu + nu)
    for nu in range(1, 4):
        result += s_terms(i_parity, k_residue, 1, 5, nu)
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


def quantity_terms(k_residue: int, quantity: str) -> list[Term]:
    even = layer_terms(0, k_residue)
    if quantity == "A":
        return consolidate(even)
    odd = layer_terms(1, k_residue)
    return consolidate(
        [(function, 2 * coefficient, argument) for function, coefficient, argument in even]
        + [(function, -coefficient, argument) for function, coefficient, argument in odd]
    )


def domain_end(k_residue: int, quantity: str) -> tuple[int, int]:
    """Exclusive upper boundary for even layers A or paired layers C."""
    paired = ((15, 0), (15, 4), (15, 8), (15, 11))[k_residue]
    if quantity == "C":
        return paired
    return ((15, 1), (15, 4), (15, 8), (15, 12))[k_residue]


def coefficients_nonnegative(expression: sp.Expr, variable: sp.Symbol) -> bool:
    polynomial = sp.Poly(sp.expand(expression), variable, domain=sp.QQ)
    return all(coefficient >= 0 for _, coefficient in polynomial.terms())


def affine_string(slope: int, constant: int) -> str:
    return str(sp.expand(slope * t + constant))


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    epsilon_min = {"T": sp.Rational(91, 360), "U": sp.Rational(1, 3)}
    epsilon_max = {"T": sp.Integer(1), "U": sp.Integer(1)}

    for k_residue in range(4):
        for quantity in ("A", "C"):
            terms = quantity_terms(k_residue, quantity)
            end = domain_end(k_residue, quantity)
            candidate_boundaries = {(0, 0), end} | {
                (-argument[1], -argument[2])
                for _, _, argument in terms
            }
            # All activation thresholds relevant for t>=T_START lie inside
            # the half-degree domain; discard thresholds uniformly outside it.
            boundaries: set[tuple[int, int]] = set()
            for bound in candidate_boundaries:
                lower_test = (bound[0] * (T_START + x) + bound[1])
                end_test = ((end[0] - bound[0]) * (T_START + x) + end[1] - bound[1])
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
                    "unstable cell", k_residue, quantity, left, right, gap
                )

                lower = left[0] * t + left[1]
                upper = right[0] * t + right[1] - 1
                active: list[Term] = []
                for function, coefficient, argument in terms:
                    threshold = -argument[1] * t - argument[2]
                    if coefficients_nonnegative((lower - threshold).subs(t, T_START + x), x):
                        active.append((function, coefficient, argument))

                # The initial constant-width cells precede every shifted
                # numerator activation.  Their values are independent of t,
                # so certify them directly instead of destroying exact
                # residue correlations with separate epsilon extrema.
                if left[0] == 0 and right[0] == 0:
                    assert all(argument[1] == 0 for _, _, argument in active)
                    representative_k = 4 * T_START + k_residue
                    exact_values = []
                    for pair in range(left[1], right[1]):
                        value = g(representative_k, 2 * pair)
                        if quantity == "C":
                            value = 2 * value - g(representative_k, 2 * pair + 1)
                        assert value >= 0, (
                            "negative exact initial cell",
                            k_residue,
                            quantity,
                            pair,
                            value,
                        )
                        exact_values.append(value)
                    records.append({
                        "k_mod_4": k_residue,
                        "quantity": quantity,
                        "lower": affine_string(*left),
                        "upper": affine_string(right[0], right[1] - 1),
                        "active_terms": len(active),
                        "exact_values": exact_values,
                    })
                    continue

                polynomial = sp.Integer(0)
                error_lower = sp.Integer(0)
                for function, coefficient, argument in active:
                    argument_expression = j + argument[1] * t + argument[2]
                    polynomial += coefficient * (
                        t_polynomial(argument_expression)
                        if function == "T"
                        else u_polynomial(argument_expression)
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
                        k_residue,
                        quantity,
                        left,
                        right,
                        index,
                        coefficient,
                    )
                    bernstein.append(str(coefficient_polynomial.as_expr()))

                records.append({
                    "k_mod_4": k_residue,
                    "quantity": quantity,
                    "lower": affine_string(*left),
                    "upper": affine_string(right[0], right[1] - 1),
                    "active_terms": len(active),
                    "bernstein_QQ[x]": bernstein,
                })
    return records


def verify_finite_bases() -> None:
    for k in range(2, 4 * T_START + 4):
        residue = k % 4
        parameter = (k - residue) // 4
        if parameter >= T_START:
            continue
        half = 15 * k // 2
        for i in range(0, half + 1, 2):
            assert g(k, i) >= 0, ("finite A", k, i, g(k, i))
            if i + 1 <= half:
                difference = 2 * g(k, i) - g(k, i + 1)
                assert difference >= 0, ("finite C", k, i // 2, difference)


def evaluate_terms(terms: list[Term], parameter: int, pair: int) -> int:
    result = 0
    for function, coefficient, argument in terms:
        index = pair + argument[1] * parameter + argument[2]
        result += coefficient * (T(index) if function == "T" else U(index))
    return result


def verify_term_translation(max_k: int = 100) -> None:
    """Audit the affine T/U translation directly against the layer formula."""
    for k in range(2, max_k + 1):
        residue = k % 4
        parameter = (k - residue) // 4
        half = 15 * k // 2
        a_terms = quantity_terms(residue, "A")
        c_terms = quantity_terms(residue, "C")
        for i in range(0, half + 1, 2):
            pair = i // 2
            assert evaluate_terms(a_terms, parameter, pair) == g(k, i), (
                "A translation",
                k,
                pair,
            )
            if i + 1 <= half:
                assert evaluate_terms(c_terms, parameter, pair) == 2 * g(k, i) - g(k, i + 1), (
                    "C translation",
                    k,
                    pair,
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-certificate", action="store_true")
    args = parser.parse_args()

    assert sp.__version__ == "1.14.0", sp.__version__
    assert min(T_EPSILON_NUMERATORS) == 91 and max(T_EPSILON_NUMERATORS) == 360
    assert min(U_EPSILON_NUMERATORS) == 1 and max(U_EPSILON_NUMERATORS) == 3
    verify_quasipolynomials()
    verify_term_translation()
    verify_finite_bases()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    if args.show_certificate:
        print(json.dumps(records, indent=2, sort_keys=True))
    print("exact QQ affine-cell/Bernstein certificate passed")
    print("T and U quasipolynomial generating-function identities verified exactly")
    print("affine T/U translation checked definitionally through k=100")
    print(f"finite bases verified below t={T_START} in every class k mod 4")
    bernstein_count = sum(len(record.get("bernstein_QQ[x]", [])) for record in records)
    exact_cell_count = sum("exact_values" in record for record in records)
    print(
        f"affine cells: {len(records)}; exact initial cells: {exact_cell_count}; "
        f"Bernstein polynomials: {bernstein_count}"
    )
    print(f"certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
