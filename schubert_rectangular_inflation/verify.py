#!/usr/bin/env python3
"""Exact verifier for rectangular Grassmannian identity inflation."""

from __future__ import annotations

import functools
import hashlib
from fractions import Fraction


def swap(w: tuple[int, ...], i: int, j: int) -> tuple[int, ...]:
    result = list(w)
    result[i], result[j] = result[j], result[i]
    return tuple(result)


def inversions(w: tuple[int, ...]) -> int:
    return sum(x > y for i, x in enumerate(w) for y in w[i + 1 :])


@functools.cache
def upsilon_transition(w: tuple[int, ...]) -> int:
    """Evaluate the Schubert polynomial at all ones by transition."""
    descents = [i for i in range(len(w) - 1) if w[i] > w[i + 1]]
    if not descents:
        return 1
    r = descents[-1]
    s = max(i for i in range(r + 1, len(w)) if w[i] < w[r])
    v = swap(w, r, s)
    length_v = inversions(v)
    return upsilon_transition(v) + sum(
        upsilon_transition(swap(v, q, r))
        for q in range(r)
        if inversions(swap(v, q, r)) == length_v + 1
    )


def rectangle_permutation(a: int, b: int, c: int) -> tuple[int, ...]:
    """Grassmannian permutation for (b^a) in a+c variables."""
    assert a >= 1 and b >= 1 and c >= 0
    return tuple(
        list(range(c))
        + list(range(c + b, c + b + a))
        + list(range(c, c + b))
    )


def tensor_identity(w: tuple[int, ...], k: int) -> tuple[int, ...]:
    assert k >= 1
    return tuple(k * value + residue for value in w for residue in range(k))


def macmahon(a: int, b: int, c: int) -> int:
    value = Fraction(1)
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            value *= Fraction(c + i + j - 1, i + j - 1)
    assert value.denominator == 1
    return value.numerator


def hook_content_rectangle(a: int, b: int, variables: int) -> int:
    value = Fraction(1)
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            value *= Fraction(variables + j - i, a + b - i - j + 1)
    assert value.denominator == 1
    return value.numerator


def verify_reflection_blocks(a: int, b: int, c: int, k: int) -> None:
    """Check the exact per-cell reflected-factor proof."""
    assert k >= 1
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            q = i + j - 2
            base = Fraction(c + q + 1, q + 1)
            block = Fraction(1)
            for alpha in range(1, k + 1):
                for beta in range(1, k + 1):
                    t = alpha + beta - 1
                    block *= Fraction(k * (c + q) + t, k * q + t)
                    reflected_t = 2 * k - t
                    left = Fraction(k * (c + q) + t, k * q + t)
                    right = Fraction(k * (c + q) + reflected_t, k * q + reflected_t)
                    assert left * right >= base * base
            assert block >= base ** (k * k)
            if c > 0 and k > 1:
                assert block > base ** (k * k)


def main() -> None:
    cases = [
        (1, 1, 0, 4),
        (1, 1, 1, 4),
        (1, 1, 2, 3),
        (1, 1, 3, 2),
        (1, 2, 1, 3),
        (2, 1, 1, 3),
        (2, 2, 1, 2),
        (2, 2, 2, 2),
        (2, 3, 1, 2),
        (3, 2, 1, 2),
    ]
    digest = hashlib.sha256()
    for a, b, c, k in cases:
        w = rectangle_permutation(a, b, c)
        inflated = tensor_identity(w, k)
        expected_inflated = rectangle_permutation(k * a, k * b, k * c)
        assert inflated == expected_inflated

        base = macmahon(a, b, c)
        large = macmahon(k * a, k * b, k * c)
        assert base == hook_content_rectangle(a, b, a + c)
        assert large == hook_content_rectangle(k * a, k * b, k * (a + c))
        assert upsilon_transition(w) == base
        assert upsilon_transition(inflated) == large
        assert large >= base ** (k * k)
        if a * b * c > 0 and k > 1:
            assert large > base ** (k * k)
        verify_reflection_blocks(a, b, c, k)

        line = f"a={a} b={b} c={c} k={k} base={base} inflated={large} bound={base ** (k*k)}"
        digest.update((line + "\n").encode())
        print(line)

    # The simple-transposition specialization is a=b=1, c=r-1.
    for r in range(1, 9):
        assert rectangle_permutation(1, 1, r - 1) == tuple(
            list(range(r - 1)) + [r, r - 1]
        )
        assert macmahon(1, 1, r - 1) == r

    print(
        f"PASS cases={len(cases)} digest={digest.hexdigest()} "
        f"transition_cache={upsilon_transition.cache_info().currsize} python={'.'.join(map(str, __import__('sys').version_info[:3]))}"
    )


if __name__ == "__main__":
    main()
