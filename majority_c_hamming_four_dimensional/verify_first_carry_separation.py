#!/usr/bin/env python3
"""Exact audit of the first-carry thin-coordinate separation theorem.

CPython 3.12+, standard library only.  Universal validity rests on the proof
in FIRST_CARRY_SEPARATION.md and its cited prerequisites; this checker audits
the arithmetic, boundary hypotheses, embeddings, and bounded cell partitions.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Iterable, Sequence


Cell = tuple[int, int, int]
Part = tuple[Cell, ...]


def first_carry_conditions(s: int, r: int, u: int, p: int) -> bool:
    """Return the two exact conditions for one-box quotient completion."""
    return s <= r * u * p < 2 * s and r + u + p >= s + 2


def validate_parameters(s: int, r: int, u: int, p: int) -> None:
    if not (s >= 3 and 1 <= r < s and 1 <= u < s and 2 <= p < s):
        raise ValueError("need s>=3, 1<=r,u<s, and 2<=p<s")


def sequential_partition(m: int, n: int, p: int, s: int) -> tuple[list[Part], Part]:
    """Strip x-lines, then y-lines, and return them with the residual tail."""
    if not (m >= s and n >= s and 1 <= p < s):
        raise ValueError("need m,n>=s and 1<=p<s")

    a, r = divmod(m, s)
    b, u = divmod(n, s)
    if r == 0 or u == 0:
        raise ValueError("this checker targets positive first-two residues")

    lines: list[Part] = []
    for block in range(a):
        for y in range(n):
            for z in range(p):
                lines.append(tuple((x, y, z) for x in range(block * s, (block + 1) * s)))

    x_tail = range(a * s, m)
    for x in x_tail:
        for block in range(b):
            for z in range(p):
                lines.append(tuple((x, y, z) for y in range(block * s, (block + 1) * s)))

    tail = tuple(
        (x, y, z)
        for x in x_tail
        for y in range(b * s, n)
        for z in range(p)
    )
    return lines, tail


def induced_degree(part: Sequence[Cell], vertex: Cell) -> int:
    return sum(
        sum(left != right for left, right in zip(vertex, other, strict=True)) == 1
        for other in part
    )


def is_coordinate_line(part: Sequence[Cell]) -> bool:
    varying = sum(len({cell[axis] for cell in part}) > 1 for axis in range(3))
    return varying == 1


def check_cell_partition(m: int, n: int, p: int, s: int) -> tuple[int, int]:
    r, u = m % s, n % s
    if not first_carry_conditions(s, r, u, p):
        raise ValueError("first-carry hypotheses are false")

    lines, tail = sequential_partition(m, n, p, s)
    expected = set(itertools.product(range(m), range(n), range(p)))
    seen: set[Cell] = set()

    for part in lines:
        assert len(part) == s
        assert is_coordinate_line(part)
        assert min(induced_degree(part, vertex) for vertex in part) == s - 1
        assert seen.isdisjoint(part)
        seen.update(part)

    assert len(tail) == r * u * p
    assert min(induced_degree(tail, vertex) for vertex in tail) == r + u + p - 3
    assert min(induced_degree(tail, vertex) for vertex in tail) >= s - 1
    assert seen.isdisjoint(tail)
    seen.update(tail)
    assert seen == expected
    assert len(lines) + 1 == m * n * p // s
    return len(lines) + 1, len(expected)


def residue_domain(max_s: int) -> Iterable[tuple[int, int, int, int]]:
    for s in range(3, max_s + 1):
        for r in range(1, s):
            for u in range(1, s):
                # Enumerate exactly the p satisfying p<s and r*u*p<2*s,
                # rather than scanning the ambient cubic parameter box.
                p_max = min(s - 1, (2 * s - 1) // (r * u))
                for p in range(2, p_max + 1):
                    yield s, r, u, p


def audit_classification(max_s: int) -> tuple[int, int, int, int]:
    domain = 0
    volume_carries = 0
    legal_tails = 0
    separations = 0

    for s, r, u, p in residue_domain(max_s):
        validate_parameters(s, r, u, p)
        domain += 1
        volume = r * u * p
        tail_degree = r + u + p - 3
        volume_carry = volume >= s
        tail_legal = tail_degree >= s - 1
        classified = first_carry_conditions(s, r, u, p)

        # The theorem's iff: one new quotient part is required and the whole
        # tail is itself legal exactly under the displayed two conditions.
        assert classified == (volume_carry and tail_legal)
        volume_carries += volume_carry
        legal_tails += tail_legal

        # Use two nontrivial quotient coefficients to audit the mixed-radix
        # count independently of the residue-only predicates.
        m, n = 3 * s + r, 2 * s + u
        residue = m * n % s
        line_maximum = p * (m * n // s)
        quotient = m * n * p // s
        stripped = (m * n * p - volume) // s
        assert residue == r * u  # p>=2 and volume<2s force r*u<s.
        assert stripped * s + volume == m * n * p

        if classified:
            assert quotient == stripped + 1
            assert line_maximum == quotient - 1
            assert quotient - line_maximum == (p * residue) // s == 1
            separations += 1
        elif volume_carry:
            assert tail_degree < s - 1

    return domain, volume_carries, legal_tails, separations


def audit_embeddings(max_s: int, q_max: int) -> tuple[int, int]:
    embeddings = 0
    family_indices = 0
    for s, r0, u0, p in residue_domain(max_s):
        if not first_carry_conditions(s, r0, u0, p):
            continue
        r, u = max(r0, u0), min(r0, u0)
        for q in range(2, q_max + 1):
            n2 = s * q + r
            n3 = s * q + u
            n4 = p
            n1 = 2 * s * q + r + u + p - 2 * s
            assert n1 >= n2 >= n3 >= n4 >= 2

            deficits = (n1 - 1, n2 - 1, n3 - 1, n4 - 1)
            h = (sum(deficits) + 1) // 2
            assert sum(deficits) % 2 == 0
            assert h == n2 + n3 + p - s - 2
            assert h - deficits[0] + 1 == s
            assert h >= deficits[0]

            quotient = n2 * n3 * p // s
            formula = s * p * q * q + p * q * (r + u) + 1
            line_ceiling = p * (n2 * n3 // s)
            assert quotient == formula
            assert line_ceiling == formula - 1
            assert deficits[0] + (r + u + p - 3) >= h
            embeddings += 1
        family_indices += 1
    return family_indices, embeddings


def audit_cell_partitions(max_s: int) -> tuple[int, int, int]:
    partitions = 0
    parts = 0
    cells = 0
    for s, r, u, p in residue_domain(max_s):
        if not first_carry_conditions(s, r, u, p):
            continue
        count, order = check_cell_partition(s + r, s + u, p, s)
        partitions += 1
        parts += count
        cells += order
    return partitions, parts, cells


def audit_sharp_boundaries() -> tuple[str, str, str]:
    # p=1: the tail is legal and gives one carry, but a rectangle line
    # partition also attains the quotient, so there is no method separation.
    s, r, u, p = 4, 3, 2, 1
    m, n = s + r, s + u
    assert s <= r * u * p < 2 * s
    assert r + u + p >= s + 2
    assert m * n * p // s == p * (m * n // s)
    p_one = f"p=1 boundary: ({s},{r},{u},{p}) has gap 0"

    # First carry without enough tail degree.
    s, r, u, p = 4, 2, 1, 2
    assert s <= r * u * p < 2 * s
    assert r + u + p - 3 < s - 1
    low_degree = f"degree boundary: ({s},{r},{u},{p}) tail degree 2 < 3"

    # The first-carry upper boundary: one tail part cannot supply two quotient
    # increments (the known 2x2x2, s=3 case needs two nonlinear parts).
    s, r, u, p = 3, 2, 2, 2
    assert r * u * p // s == 2
    second_carry = f"second-carry boundary: ({s},{r},{u},{p}) needs 2 parts"
    return p_one, low_degree, second_carry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-s", type=int, default=160)
    parser.add_argument("--cell-max-s", type=int, default=12)
    parser.add_argument("--q-max", type=int, default=8)
    args = parser.parse_args()
    if args.max_s < 4 or args.cell_max_s < 3 or args.q_max < 2:
        parser.error("need max-s>=4, cell-max-s>=3, and q-max>=2")

    domain, carries, legal, separations = audit_classification(args.max_s)
    family_indices, embeddings = audit_embeddings(args.max_s, args.q_max)
    cell_partitions, parts, cells = audit_cell_partitions(args.cell_max_s)
    boundaries = audit_sharp_boundaries()

    print(f"first-carry residue tuples through s={args.max_s}: {domain}")
    print(f"volume-carry tuples: {carries}")
    print(f"legal whole-tail tuples: {legal}")
    print(f"exact nonlinear/line separations: {separations}")
    print(f"admissible ordered residue patterns: {family_indices}")
    print(f"near-triangle embeddings through q={args.q_max}: {embeddings}")
    print(f"cell-level partitions through s={args.cell_max_s}: {cell_partitions}")
    print(f"cell-level parts checked: {parts}")
    print(f"cell-level cells checked: {cells}")
    for boundary in boundaries:
        print(boundary)
    print("base realization: K_11 square K_8 square K_7 square K_2 = 37; line ceiling 36")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
