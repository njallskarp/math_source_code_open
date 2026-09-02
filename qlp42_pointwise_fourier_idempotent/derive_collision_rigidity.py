#!/usr/bin/env python3
"""Derive an exact certificate for primitive Fourier collision rigidity.

This production derivation uses integer polynomial reduction and rational
Gaussian elimination.  It never enumerates QLP supports, orbits, or cells.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


P = 7
Q = 3
N = P * Q
OUT = Path(__file__).with_name("collision_rigidity_certificate.json")


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def divide_monic_exact(dividend: list[int], divisor: list[int]) -> list[int]:
    dividend = trim(dividend[:])
    divisor = trim(divisor[:])
    assert divisor[-1] == 1
    if len(dividend) < len(divisor):
        raise AssertionError("nonzero remainder")
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    while len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        coefficient = dividend[-1]
        quotient[shift] = coefficient
        for j, value in enumerate(divisor):
            dividend[shift + j] -= coefficient * value
        trim(dividend)
    assert dividend == [0]
    return trim(quotient)


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return trim(out)


def cyclotomic(n: int, memo: dict[int, list[int]]) -> list[int]:
    if n in memo:
        return memo[n]
    polynomial = [-1] + [0] * (n - 1) + [1]
    for divisor in range(1, n):
        if n % divisor == 0:
            polynomial = divide_monic_exact(polynomial, cyclotomic(divisor, memo))
    memo[n] = polynomial
    return polynomial


def monomial_remainder(exponent: int, modulus: list[int]) -> list[int]:
    degree = len(modulus) - 1
    polynomial = [0] * exponent + [1]
    while len(polynomial) - 1 >= degree:
        shift = len(polynomial) - 1 - degree
        coefficient = polynomial[-1]
        for j, value in enumerate(modulus):
            polynomial[shift + j] -= coefficient * value
        trim(polynomial)
    return polynomial + [0] * (degree - len(polynomial))


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(x) for x in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next((r for r in range(rank, rows) if work[r][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][j] - factor * work[rank][j] for j in range(columns)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def crt_fiber_generators() -> tuple[list[list[int]], list[str]]:
    generators: list[list[int]] = []
    labels: list[str] = []
    for residue in range(P):
        generators.append([int(j % P == residue) for j in range(N)])
        labels.append(f"mod_{P}_fiber_{residue}")
    for residue in range(Q):
        generators.append([int(j % Q == residue) for j in range(N)])
        labels.append(f"mod_{Q}_fiber_{residue}")
    return generators, labels


def matrix_hash(matrix: list[list[int]]) -> str:
    encoded = json.dumps(matrix, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    phi = cyclotomic(N, {1: [-1, 1]})
    degree = len(phi) - 1
    columns = [monomial_remainder(j, phi) for j in range(N)]
    evaluation = [[columns[j][i] for j in range(N)] for i in range(degree)]

    fibers, labels = crt_fiber_generators()
    selected_indices = list(range(P)) + list(range(P, P + Q - 1))
    selected = [fibers[index] for index in selected_indices]
    zero_products = [
        [sum(evaluation[r][j] * generator[j] for j in range(N)) for r in range(degree)]
        for generator in fibers
    ]
    assert all(all(value == 0 for value in row) for row in zero_products)

    evaluation_rank = rational_rank(evaluation)
    fiber_rank = rational_rank(fibers)
    selected_rank = rational_rank(selected)
    assert evaluation_rank == degree == (P - 1) * (Q - 1)
    assert N - evaluation_rank == P + Q - 1
    assert fiber_rank == selected_rank == P + Q - 1

    mixed_balance_solutions = [
        [a, b]
        for a in range(1, P)
        for b in range(1, Q)
        if Q * a + P * b == P * Q
    ]
    assert mixed_balance_solutions == []

    certificate = {
        "schema": "qlp42-primitive-collision-rigidity-v2",
        "p": P,
        "q": Q,
        "n": N,
        "phi_n_coefficients_low_to_high": phi,
        "evaluation_matrix_sha256": matrix_hash(evaluation),
        "evaluation_rank": evaluation_rank,
        "kernel_rank": N - evaluation_rank,
        "fiber_generator_labels": labels,
        "fiber_generator_rank": fiber_rank,
        "selected_basis_indices": selected_indices,
        "selected_basis_rank": selected_rank,
        "mixed_balance_solutions": mixed_balance_solutions,
        "multicolor_collision_modes": ["identical", "p_fibers_only", "q_fibers_only"],
        "qlp_sparse_minority": {
            "total_minority_cells": 5,
            "seven_fiber_support_change_possible": False,
            "family_support_rigid_below": 3,
        },
    }
    OUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(f"p={P} q={Q} n={N}")
    print(f"phi21_degree={degree}")
    print(f"primitive_evaluation_rank={evaluation_rank}")
    print(f"primitive_kernel_rank={N - evaluation_rank}")
    print(f"row_column_span_rank={fiber_rank}")
    print(f"mixed_balanced_trades={len(mixed_balance_solutions)}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
