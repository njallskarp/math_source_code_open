#!/usr/bin/env python3
"""Exact audit for equal CRT images with disjoint sum-one fibers."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def polynomial_degree(value: int) -> int:
    return value.bit_length() - 1


def polynomial_remainder(dividend: int, divisor: int) -> int:
    assert divisor
    divisor_degree = polynomial_degree(divisor)
    while dividend and polynomial_degree(dividend) >= divisor_degree:
        dividend ^= divisor << (polynomial_degree(dividend) - divisor_degree)
    return dividend


def polynomial_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, polynomial_remainder(left, right)
    return left


def syndrome(n: int, axis: int, signs: int) -> int:
    result = 0
    for shift in range(1, (n + 1) // 2):
        coordinate = 0
        for index in range(n):
            shifted = (index + shift) % n
            coordinate ^= (
                ((signs >> index) ^ (signs >> shifted))
                & ((axis >> index) ^ (axis >> shifted))
                & 1
            )
        result |= coordinate << (shift - 1)
    return result


def binary_rank(columns: list[int]) -> int:
    basis: dict[int, int] = {}
    for value in columns:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def syndrome_rank(n: int, axis: int) -> int:
    return binary_rank([syndrome(n, axis, 1 << index) for index in range(n)])


def gaussian_sum(n: int, axis: int, signs: int) -> tuple[int, int]:
    real = 0
    imaginary = 0
    for index in range(n):
        value = -1 if (signs >> index) & 1 else 1
        if (axis >> index) & 1:
            imaginary += value
        else:
            real += value
    return real, imaginary


def witnesses(n: int) -> tuple[int, int]:
    # b=1+x: one negative imaginary position, and (n-3)/2 negative
    # real positions.
    b_signs = 1
    for index in range(2, 2 + (n - 3) // 2):
        b_signs |= 1 << index

    # c=1+x+x^2+x^3: two negative imaginary positions, and
    # (n-5)/2 negative real positions.
    c_signs = 0b0011
    for index in range(4, 4 + (n - 5) // 2):
        c_signs |= 1 << index
    return b_signs, c_signs


def exact_fiber(n: int, axis: int) -> set[int]:
    return {
        syndrome(n, axis, signs)
        for signs in range(1 << n)
        if gaussian_sum(n, axis, signs) == (1, 0)
    }


def main() -> None:
    b_axis = 0b0011
    c_axis = 0b1111
    x_plus_one = 0b11
    records: list[str] = []

    for n in range(5, 102, 2):
        modulus = (1 << n) | 1  # x^n+1 = x^n-1 over F_2
        assert polynomial_gcd(b_axis, modulus) == x_plus_one
        assert polynomial_gcd(c_axis, modulus) == x_plus_one
        expected_rank = (n - 1) // 2
        b_rank = syndrome_rank(n, b_axis)
        c_rank = syndrome_rank(n, c_axis)
        assert b_rank == c_rank == expected_rank

        b_signs, c_signs = witnesses(n)
        assert gaussian_sum(n, b_axis, b_signs) == (1, 0)
        assert gaussian_sum(n, c_axis, c_signs) == (1, 0)
        b_syndrome = syndrome(n, b_axis, b_signs)
        c_syndrome = syndrome(n, c_axis, c_signs)
        assert b_syndrome.bit_count() % 2 == 1
        assert c_syndrome.bit_count() % 2 == 0
        records.append(
            f"{n}\t{b_rank}\t{c_rank}\t{b_syndrome:x}\t{c_syndrome:x}"
        )

    exhaustive_records = []
    for n in (5, 7, 9, 11):
        b_fiber = exact_fiber(n, b_axis)
        c_fiber = exact_fiber(n, c_axis)
        assert b_fiber
        assert c_fiber
        assert b_fiber.isdisjoint(c_fiber)
        assert all(value.bit_count() % 2 == 1 for value in b_fiber)
        assert all(value.bit_count() % 2 == 0 for value in c_fiber)
        exhaustive_records.append(f"{n}:{len(b_fiber)}:{len(c_fiber)}")

    stream = "\n".join(records) + "\n"
    digest = hashlib.sha256(stream.encode("ascii")).hexdigest()
    output = [
        f"python={sys.version.split()[0]}",
        "audited_odd_lengths=5..101",
        "common_image=full_syndrome_space",
        "constructed_sum_one_witnesses=98",
        f"exhaustive_fiber_counts={','.join(exhaustive_records)}",
        f"audit_stream_sha256={digest}",
        "theorem_audit=verified",
    ]
    expected = (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="ascii"
    )
    assert expected == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
