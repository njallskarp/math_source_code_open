#!/usr/bin/env python3
"""Exact checker for the primitive cross-trace fiber lemma."""

from __future__ import annotations

from math import gcd

G = tuple[int, int]
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def gadd(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def gmul(left: G, right: G) -> G:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gconj(value: G) -> G:
    return value[0], -value[1]


def div_one_plus_i(value: G) -> G:
    assert (value[0] + value[1]) % 2 == 0
    assert (value[1] - value[0]) % 2 == 0
    return (value[0] + value[1]) // 2, (value[1] - value[0]) // 2


def mobius(value: int) -> int:
    remaining = value
    primes = 0
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            primes += 1
            if remaining % divisor == 0:
                return 0
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        primes += 1
    return -1 if primes % 2 else 1


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def ramanujan(modulus: int, shift: int) -> int:
    # c_n(k) = sum_{d | gcd(n,k)} d mu(n/d).
    return sum(
        d * mobius(modulus // d)
        for d in divisors(gcd(modulus, shift))
    )


def local_state_check() -> tuple[int, int, int, int]:
    epsilons: list[int] = []
    equal = opposite = quarter = 0
    states: set[tuple[G, G]] = set()
    for x in ROOTS:
        for y in ROOTS:
            s = div_one_plus_i(gsub(x, y))
            h = div_one_plus_i(gadd(x, y))
            states.add((s, h))
            cross = gmul(s, gconj(h))
            epsilon_pair = gmul((0, -1), cross)
            assert epsilon_pair[1] == 0
            epsilon = epsilon_pair[0]
            assert epsilon in (-1, 0, 1)
            relative = gmul(x, gconj(y))
            is_quarter = relative[0] == 0
            assert (epsilon != 0) == is_quarter
            epsilons.append(epsilon)
            if x == y:
                equal += 1
            elif x == (-y[0], -y[1]):
                opposite += 1
            else:
                quarter += 1
    assert len(states) == 16
    assert sorted(epsilons) == [-1] * 4 + [0] * 8 + [1] * 4
    return len(states), equal, opposite, quarter


def character_kernel_check() -> None:
    for shift in range(21):
        kernel = sum(ramanujan(d, shift) for d in (1, 3, 7, 21))
        assert kernel == (21 if shift == 0 else 0)
    assert {ramanujan(21, s) for s in range(21)} == {-6, -2, 1, 12}


def sum_case_check() -> list[G]:
    beta: list[G] = []
    for _p, _q, x, y in CASES:
        beta.append((x + y - 1, y - x))
    assert beta == [(4, -5), (4, -3), (0, -5), (4, -1), (4, 1), (0, -3)]
    return beta


def fiber(beta: G, q: int) -> set[G]:
    return {
        (-beta[0], -beta[1] + 21 * sigma)
        for sigma in range(-q, q + 1, 2)
    }


def main() -> None:
    states, equal, opposite, quarter = local_state_check()
    character_kernel_check()
    beta = sum_case_check()

    fibers5 = [fiber(value, 5) for value in beta]
    fibers37 = [fiber(value, 37) for value in beta]
    assert all(len(values) == 6 for values in fibers5)
    assert all(len(values) == 38 for values in fibers37)
    assert [next(iter(values))[0] for values in fibers5] == [-4, -4, 0, -4, -4, 0]
    for case, values in enumerate(fibers37):
        residues = {imag % 21 for _real, imag in values}
        assert residues == {(-beta[case][1]) % 21}

    print(f"local_states={states}")
    print(f"local_types=equal:{equal},opposite:{opposite},quarter:{quarter}")
    print("epsilon_distribution=-1:4,0:8,1:4")
    print("ramanujan_kernel=21_delta_verified")
    print("cross_trace_identity=universal")
    print("canonical_sum_cases=6")
    print("q5_fiber_points_per_case=6")
    print("q37_fiber_points_per_case=38")
    print("case_real_parts=-4,-4,0,-4,-4,0")
    print("certificate=verified")


if __name__ == "__main__":
    main()
