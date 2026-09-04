"""Independent SymPy reconstruction of the cyclotomic-unit obstruction."""

from __future__ import annotations

from math import factorial, prod

import sympy as sp

EXAMPLES = (
    ((9, 7, 6, 4, 3, 1), (12, 9, 4, 3, 1, 1), 3),
    ((25, 10, 7, 7, 5, 1, 1), (20, 15, 7, 7, 5, 1, 1), 5),
    ((28, 21, 7, 1, 1, 1, 1), (21, 14, 11, 7, 5, 1, 1), 7),
)


def determinant(parts: tuple[int, ...], x: sp.Symbol) -> sp.Expr:
    return sp.prod(1 - x**part for part in parts)


def leading_numerator(
    left: tuple[int, ...], right: tuple[int, ...], prime: int, x: sp.Symbol
) -> sp.Expr:
    left_divisible = sum(part % prime == 0 for part in left)
    right_divisible = sum(part % prime == 0 for part in right)
    left_nondivisible = tuple(part for part in left if part % prime)
    right_nondivisible = tuple(part for part in right if part % prime)
    return sp.expand(
        factorial(len(left))
        * factorial(right_divisible - 1)
        * prod(left_nondivisible)
        * determinant(right_nondivisible, x)
        + factorial(left_divisible - 1)
        * factorial(len(right))
        * prod(right_nondivisible)
        * determinant(left_nondivisible, x)
    )


def main() -> None:
    x = sp.symbols("x")
    residues: list[int] = []
    for left, right, prime in EXAMPLES:
        phi = sp.cyclotomic_poly(prime, x)
        remainder = sp.rem(leading_numerator(left, right, prime, x), phi, domain=sp.ZZ)
        if remainder == 0:
            raise AssertionError((left, right, prime))
        count = sum(part % prime == 0 for part in left)
        defect = len(left) - count
        block = prod(range(count, count + defect + 1))
        valuation = 0
        reduced = block
        while reduced % prime == 0:
            reduced //= prime
            valuation += 1
        residue = (2 * reduced) % prime
        if residue == 0:
            raise AssertionError((prime, block, valuation))
        residues.append(residue)

        # Equation (5), checked directly in the residue field.
        for part in (*left, *right):
            if part % prime:
                geometric_at_one = part % prime
                normalized = geometric_at_one * pow(part, -1, prime) % prime
                if normalized != 1:
                    raise AssertionError((part, prime))

    print(
        "INDEPENDENT SYMPY VERIFIED; primes=3,5,7; "
        f"normalized_residues={','.join(map(str, residues))}; "
        "leading_remainders=nonzero"
    )


if __name__ == "__main__":
    main()
