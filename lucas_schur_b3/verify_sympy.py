#!/usr/bin/env python3
"""Exact factorial-quotient checks for the complete Lucas b=3 slice."""

from __future__ import annotations

import argparse

import sympy as sp

S, T = sp.symbols("s t")


def lucas_table(limit: int) -> list[sp.Poly]:
    values = [sp.Poly(0, S, T, domain=sp.QQ), sp.Poly(1, S, T, domain=sp.QQ)]
    for _ in range(1, limit):
        expression = S * values[-1].as_expr() + T * values[-2].as_expr()
        values.append(sp.Poly(expression, S, T, domain=sp.QQ))
    return values


def lucas_binomial(values: list[sp.Poly], n: int, k: int) -> sp.Poly:
    if k < 0 or k > n:
        return sp.Poly(0, S, T, domain=sp.QQ)
    k = min(k, n - k)
    numerator = sp.Poly(1, S, T, domain=sp.QQ)
    denominator = sp.Poly(1, S, T, domain=sp.QQ)
    for index in range(1, k + 1):
        numerator *= values[n - k + index]
        denominator *= values[index]
    return numerator.exquo(denominator)


def shifted(poly: sp.Poly, power: int) -> sp.Poly:
    return sp.Poly(T**power * poly.as_expr(), S, T, domain=sp.QQ)


def nonnegative(poly: sp.Poly) -> bool:
    return all(coefficient >= 0 for coefficient in poly.coeffs())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-c", type=int, default=14)
    parser.add_argument("--max-k", type=int, default=12)
    args = parser.parse_args()
    if args.max_c < 3 or args.max_k < 2:
        parser.error("need --max-c >= 3 and --max-k >= 2")

    limit = max(3 * args.max_c + 2, 6 * args.max_k + 2)
    f = lucas_table(limit)

    # Fixed-width KOH identities (1) and (2).
    for r in range(0, max(args.max_c, 3 * args.max_k) + 1):
        lhs = lucas_binomial(f, r + 2, 2)
        rhs = f[2 * r + 1] + shifted(lucas_binomial(f, r, 2), 2)
        assert lhs == rhs, ("width two", r)
    for r in range(1, max(args.max_c, 2 * args.max_k) + 1):
        lhs = lucas_binomial(f, r + 3, 3)
        rhs = (
            f[3 * r + 1]
            + shifted(f[r - 1] * f[2 * r - 1], 2)
            + shifted(lucas_binomial(f, r - 1, 3), 6)
        )
        assert lhs == rhs, ("width three", r)

    # The a=1 expansion (3).
    for c in range(3, args.max_c + 1):
        lhs = lucas_binomial(f, c + 3, 3) - f[3 * c + 1]
        rhs = shifted(f[c - 1] * f[2 * c - 1] + shifted(lucas_binomial(f, c - 1, 3), 4), 2)
        assert lhs == rhs, ("a=1", c)
        assert nonnegative(lhs), ("a=1 positivity", c)

    # The a=2 expansion (6).
    for k in range(2, args.max_k + 1):
        lhs = lucas_binomial(f, 3 * k + 2, 2) - lucas_binomial(f, 2 * k + 3, 3)
        rhs = sp.Poly(0, S, T, domain=sp.QQ)
        for j in range(k // 2):
            n = 2 * k - 4 * j - 1
            summand = f[n - 1] * f[2 * n] + shifted(f[3 * n - 4], 1)
            rhs += shifted(summand, 6 * j + 3)
        assert lhs == rhs, ("a=2", k)
        assert nonnegative(lhs), ("a=2 positivity", k)

    print(f"SymPy {sp.__version__}: exact QQ[s,t] verification passed")
    print(f"a=1 checked for 3 <= c <= {args.max_c}")
    print(f"a=2 checked for 2 <= k <= {args.max_k}")


if __name__ == "__main__":
    main()
