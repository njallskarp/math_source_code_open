#!/usr/bin/env python3
"""Exact audit for equal CRT/parity data with distinct exact fibers."""

from __future__ import annotations

import hashlib
import math
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
        sign = -1 if (signs >> index) & 1 else 1
        if (axis >> index) & 1:
            imaginary += sign
        else:
            real += sign
    return real, imaginary


def exact_fiber(n: int, axis: int, target: tuple[int, int]) -> set[int]:
    return {
        syndrome(n, axis, signs)
        for signs in range(1 << n)
        if gaussian_sum(n, axis, signs) == target
    }


def main() -> None:
    records: list[str] = []
    audited_witnesses = 0
    for n in range(5, 102, 2):
        modulus = (1 << n) | 1  # x^n+1 = x^n-1 over F_2
        expected_rank = (n - 1) // 2
        row = [str(n)]
        fibers = []
        for distance in (1, 2):
            assert math.gcd(distance, n) == 1
            axis = 1 | (1 << distance)
            assert polynomial_gcd(axis, modulus) == 0b11
            rank = syndrome_rank(n, axis)
            assert rank == expected_rank

            expected_syndrome = 1 << (distance - 1)
            witnessed = set()
            for signs in (1, 1 << distance):
                assert gaussian_sum(n, axis, signs) == (n - 2, 0)
                value = syndrome(n, axis, signs)
                assert value == expected_syndrome
                assert value.bit_count() % 2 == 1
                witnessed.add(value)
                audited_witnesses += 1
            assert witnessed == {expected_syndrome}
            fibers.append(witnessed)
            row.extend((str(rank), f"{expected_syndrome:x}"))
        assert fibers[0].isdisjoint(fibers[1])
        records.append("\t".join(row))

    exhaustive_records = []
    for n in (5, 7, 9, 11, 13):
        target = (n - 2, 0)
        fibers = []
        for distance in (1, 2):
            axis = 1 | (1 << distance)
            fiber = exact_fiber(n, axis, target)
            assert fiber == {1 << (distance - 1)}
            fibers.append(fiber)
        assert fibers[0].isdisjoint(fibers[1])
        exhaustive_records.append(f"{n}:1:1")

    stream = "\n".join(records) + "\n"
    digest = hashlib.sha256(stream.encode("ascii")).hexdigest()
    output = [
        f"python={sys.version.split()[0]}",
        "audited_odd_lengths=5..101",
        "shared_data=full_image,weight_2,target_n_minus_2,odd_parity_coset",
        f"direct_exact_witness_checks={audited_witnesses}",
        f"exhaustive_fiber_counts={','.join(exhaustive_records)}",
        f"audit_stream_sha256={digest}",
        "same_parity_obstruction=verified",
    ]
    expected = (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="ascii"
    )
    assert expected == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
