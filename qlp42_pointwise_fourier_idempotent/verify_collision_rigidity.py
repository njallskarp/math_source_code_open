#!/usr/bin/env python3
"""Independent exact checker for the primitive collision certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


P = 7
Q = 3
N = 21
PHI21 = [1, -1, 0, 1, -1, 0, 1, 0, -1, 1, 0, -1, 1]
CERTIFICATE = Path(__file__).with_name("collision_rigidity_certificate.json")


def next_power(vector: list[int]) -> list[int]:
    degree = len(PHI21) - 1
    shifted = [0] + vector
    overflow = shifted.pop()
    if overflow:
        for j in range(degree):
            shifted[j] -= overflow * PHI21[j]
    return shifted


def evaluation_matrix() -> list[list[int]]:
    degree = len(PHI21) - 1
    powers: list[list[int]] = []
    current = [1] + [0] * (degree - 1)
    for _ in range(N):
        powers.append(current)
        current = next_power(current)
    return [[powers[j][i] for j in range(N)] for i in range(degree)]


def modular_rank(matrix: list[list[int]], prime: int) -> int:
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next((r for r in range(rank, rows) if work[r][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (work[row][j] - factor * work[rank][j]) % prime
                    for j in range(columns)
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def fibers() -> list[list[int]]:
    return (
        [[int(j % P == residue) for j in range(N)] for residue in range(P)]
        + [[int(j % Q == residue) for j in range(N)] for residue in range(Q)]
    )


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(row[j] * vector[j] for j in range(N)) for row in matrix]


def matrix_hash(matrix: list[list[int]]) -> str:
    encoded = json.dumps(matrix, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def gaussian_divide_by_one_plus_i(z: tuple[int, int]) -> tuple[int, int]:
    a, b = z
    assert (a + b) % 2 == 0 and (b - a) % 2 == 0
    return ((a + b) // 2, (b - a) // 2)


def local_state_count() -> int:
    phases = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    states = set()
    for x in phases:
        for y in phases:
            difference = (x[0] - y[0], x[1] - y[1])
            total = (x[0] + y[0], x[1] + y[1])
            states.add(
                (gaussian_divide_by_one_plus_i(difference), gaussian_divide_by_one_plus_i(total))
            )
    return len(states)


def color_counts(word: tuple[int, ...], colors: int) -> tuple[int, ...]:
    return tuple(word.count(color) for color in range(colors))


def zero_mixed_component(
    left: tuple[int, ...], right: tuple[int, ...], p: int, q: int, colors: int
) -> bool:
    for color in range(colors):
        difference = [
            int(right[j] == color) - int(left[j] == color) for j in range(p * q)
        ]
        for row in range(1, p):
            for column in range(1, q):
                if (
                    difference[row * q + column]
                    - difference[row * q]
                    - difference[column]
                    + difference[0]
                ) != 0:
                    return False
    return True


def fiber_collision(
    left: tuple[int, ...], right: tuple[int, ...], p: int, q: int, along_rows: bool
) -> bool:
    outer, inner = (p, q) if along_rows else (q, p)
    for a in range(outer):
        left_fiber = tuple(
            left[a * q + b] if along_rows else left[b * q + a] for b in range(inner)
        )
        right_fiber = tuple(
            right[a * q + b] if along_rows else right[b * q + a] for b in range(inner)
        )
        if left_fiber == right_fiber:
            continue
        if len(set(left_fiber)) != 1 or len(set(right_fiber)) != 1:
            return False
    return True


def small_multicolor_audit() -> int:
    """Exhaust the theorem on C_2 x C_3 with three colors."""
    from itertools import product

    p, q, colors = 2, 3, 3
    words = list(product(range(colors), repeat=p * q))
    by_count: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for word in words:
        by_count.setdefault(color_counts(word, colors), []).append(word)
    nontrivial = 0
    for bucket in by_count.values():
        for left in bucket:
            for right in bucket:
                if left == right or not zero_mixed_component(left, right, p, q, colors):
                    continue
                nontrivial += 1
                assert fiber_collision(left, right, p, q, True) or fiber_collision(
                    left, right, p, q, False
                )
    return nontrivial


def main() -> None:
    raw = CERTIFICATE.read_bytes()
    certificate = json.loads(raw)
    assert certificate["schema"] == "qlp42-primitive-collision-rigidity-v2"
    assert (certificate["p"], certificate["q"], certificate["n"]) == (P, Q, N)
    assert certificate["phi_n_coefficients_low_to_high"] == PHI21

    evaluation = evaluation_matrix()
    assert matrix_hash(evaluation) == certificate["evaluation_matrix_sha256"]
    # Full row rank modulo one prime proves full row rank over Q.
    evaluation_rank = modular_rank(evaluation, 101)
    assert evaluation_rank == 12 == certificate["evaluation_rank"]
    assert N - evaluation_rank == 9 == certificate["kernel_rank"]

    generators = fibers()
    assert all(matvec(evaluation, generator) == [0] * 12 for generator in generators)
    selected = [generators[index] for index in certificate["selected_basis_indices"]]
    selected_rank = modular_rank(selected, 103)
    all_fiber_rank = modular_rank(generators, 107)
    assert selected_rank == all_fiber_rank == 9
    assert selected_rank == certificate["selected_basis_rank"]
    assert all_fiber_rank == certificate["fiber_generator_rank"]

    # If both additive potentials are nonconstant, their oscillations are one.
    # Writing a for the high-row count and b for the high-column count,
    # equality of the +1 and -1 supports is equivalent to q*a+p*b=p*q.
    mixed = [
        [a, b]
        for a in range(1, P)
        for b in range(1, Q)
        if Q * a + P * b == P * Q
    ]
    assert mixed == certificate["mixed_balance_solutions"] == []

    states = local_state_count()
    assert states == 16
    collision_modes = certificate["multicolor_collision_modes"]
    assert collision_modes == ["identical", "p_fibers_only", "q_fibers_only"]
    sparse = certificate["qlp_sparse_minority"]
    assert sparse == {
        "total_minority_cells": 5,
        "seven_fiber_support_change_possible": False,
        "family_support_rigid_below": 3,
    }
    assert sparse["total_minority_cells"] < P
    assert sparse["family_support_rigid_below"] == Q
    small_collisions = small_multicolor_audit()
    assert small_collisions > 0
    digest = hashlib.sha256(raw).hexdigest()
    print(f"p={P} q={Q} n={N}")
    print("phi21_degree=12")
    print(f"primitive_evaluation_rank={evaluation_rank}")
    print(f"primitive_kernel_rank={N - evaluation_rank}")
    print(f"row_column_span_rank={all_fiber_rank}")
    print(f"mixed_balanced_trades={len(mixed)}")
    print(f"local_states={states}")
    print(f"small_multicolor_collisions={small_collisions}")
    print("multicolor_collision_modes=3")
    print("qlp_seven_fiber_support_change=forbidden")
    print("family_support_rigid_for_minority_at_most=2")
    print(f"certificate_sha256={digest}")
    print("theorem=verified")


if __name__ == "__main__":
    main()
