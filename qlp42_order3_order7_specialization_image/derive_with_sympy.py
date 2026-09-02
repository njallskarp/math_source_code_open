#!/usr/bin/env python3
"""Independent exact SymPy derivation of the interpolation formula."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    x = sp.symbols("x")
    a0, a1, *tail = sp.symbols("a0 a1 b0 b1 b2 b3 b4 b5 c")
    *bs, c = tail

    phi3 = x**2 + x + 1
    phi7 = sum(x**j for j in range(7))
    assert sp.expand(phi7 - (x**4 + x) * phi3) == 1
    assert sp.resultant(phi3, phi7, x) == 1

    a = a0 + a1 * x
    b = sum(bs[j] * x**j for j in range(6))
    f0 = sp.expand(a * phi7 + b * (1 - phi7))
    f = sp.expand(f0 + c * phi3 * phi7)

    assert sp.rem(f, phi3, x, domain=sp.EX) == a
    assert sp.rem(f, phi7, x, domain=sp.EX) == b
    expected = 7 * (a0 + a1) - 6 * sum(bs) + 21 * c
    assert sp.expand(f.subs(x, 1) - expected) == 0
    assert sp.degree(f, x) <= 11

    print(f"python_sympy={sp.__version__}")
    print("resultant_phi3_phi7=1")
    print("universal_remainders=verified")
    print("universal_value_at_one=verified")
    print(f"degree_bound={sp.degree(f, x)}<21")
    print("sympy_derivation=verified")


if __name__ == "__main__":
    main()
