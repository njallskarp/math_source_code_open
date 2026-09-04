#!/usr/bin/env python3
"""Exact audit of the flip-depth canonical-clique packing theorem."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import comb


def flip_count(signs: tuple[int, ...]) -> int:
    return sum(a != b for a, b in zip(signs, signs[1:]))


def weak_multisets(r: int, s: int):
    return combinations_with_replacement(range(r + 1), s)


def omitted_positions(m: int, q_values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(q * m + t for t, q in enumerate(q_values, start=1))


def direct_clique(
    r: int, m: int, signs: tuple[int, ...], q_values: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    n = r * m + len(q_values)
    omitted = set(omitted_positions(m, q_values))
    kept = [vertex for vertex in range(1, n + 1) if vertex not in omitted]
    assert len(kept) == r * m
    return tuple(
        tuple(
            kept[i * m + (j if sign == 1 else m - 1 - j)]
            for i, sign in enumerate(signs)
        )
        for j in range(m)
    )


def formula_clique(
    r: int, m: int, signs: tuple[int, ...], q_values: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            i * m
            + (j + 1 if sign == 1 else m - j)
            + sum(q < i + 1 for q in q_values)
            for i, sign in enumerate(signs)
        )
        for j in range(m)
    )


def gap_counts(signs: tuple[int, ...]) -> tuple[int, ...]:
    gaps = [
        int(signs[i] == 1) + int(signs[i + 1] == -1)
        for i in range(len(signs) - 1)
    ]
    gaps.append(int(signs[-1] == 1))
    assert sum(gaps) == len(signs)
    return tuple(gaps)


def deleted_edges(r: int, m: int, s: int, signs: tuple[int, ...]):
    gaps = gap_counts(signs)
    deleted = set()
    for y_values in combinations(range(1, r + s + 1), r):
        edge = tuple(
            y + (m - 1) * sum(gaps[:i]) for i, y in enumerate(y_values)
        )
        assert all(
            edge[i + 1] - edge[i] > gaps[i] * (m - 1)
            for i in range(r - 1)
        )
        assert edge[-1] <= r * m + s - gaps[-1] * (m - 1)
        deleted.add(edge)
    assert len(deleted) == comb(r + s, r)
    return deleted


def sharp_collision_multisets(signs: tuple[int, ...]):
    delta = [signs[0]]
    delta.extend(b - a for a, b in zip(signs, signs[1:]))
    delta.append(-signs[-1])
    positive = tuple(
        value for value, multiplicity in enumerate(delta) for _ in range(max(0, multiplicity))
    )
    negative = tuple(
        value for value, multiplicity in enumerate(delta) for _ in range(max(0, -multiplicity))
    )
    expected = flip_count(signs) + 1
    assert len(positive) == len(negative) == expected
    return negative, positive


def main() -> None:
    rows: list[str] = []
    packing_instances = 0
    selected_copies = 0
    selected_edges = 0

    for r in range(2, 8):
        for signs_tail in product((1, -1), repeat=r - 1):
            signs = (1,) + signs_tail
            flips = flip_count(signs)
            for m in range(2, 6):
                for s in range(flips + 1):
                    seen = {}
                    copies = 0
                    for q_values_raw in weak_multisets(r, s):
                        q_values = tuple(q_values_raw)
                        omitted = omitted_positions(m, q_values)
                        assert tuple(sorted(omitted)) == omitted
                        assert len(set(omitted)) == s
                        assert all(1 <= x <= r * m + s for x in omitted)
                        direct = direct_clique(r, m, signs, q_values)
                        formula = formula_clique(r, m, signs, q_values)
                        assert direct == formula
                        for j, edge in enumerate(direct, start=1):
                            assert edge not in seen, (r, m, signs, s, q_values, j, seen[edge])
                            seen[edge] = (q_values, j)
                        copies += 1
                    assert copies == comb(r + s, r)
                    assert len(seen) == m * copies
                    packing_instances += 1
                    selected_copies += copies
                    selected_edges += len(seen)

    row = (
        f"packing_box_r=2..7_m=2..5 instances={packing_instances} "
        f"copies={selected_copies} edges={selected_edges} status=disjoint"
    )
    print(row)
    rows.append(row)

    lower_instances = 0
    all_omission_copies = 0
    for r in range(2, 6):
        for signs_tail in product((1, -1), repeat=r - 1):
            signs = (1,) + signs_tail
            flips = flip_count(signs)
            for m in range(2, 5):
                for s in range(min(flips, 2) + 1):
                    deleted = deleted_edges(r, m, s, signs)
                    n = r * m + s
                    for omitted in combinations(range(1, n + 1), s):
                        kept = [x for x in range(1, n + 1) if x not in omitted]
                        first_edge = tuple(
                            kept[i * m + (0 if sign == 1 else m - 1)]
                            for i, sign in enumerate(signs)
                        )
                        assert first_edge in deleted
                        all_omission_copies += 1
                    lower_instances += 1

    row = (
        f"lower_construction_r=2..5_m=2..4 instances={lower_instances} "
        f"canonical_copies={all_omission_copies} status=hit"
    )
    print(row)
    rows.append(row)

    sharp_instances = 0
    for r in range(2, 9):
        for signs_tail in product((1, -1), repeat=r - 1):
            signs = (1,) + signs_tail
            q_values, r_values = sharp_collision_multisets(signs)
            s = flip_count(signs) + 1
            assert len(q_values) == len(r_values) == s
            for m in range(2, 6):
                edge_q = formula_clique(r, m, signs, q_values)[1]
                edge_r = formula_clique(r, m, signs, r_values)[0]
                assert edge_q == edge_r
                assert q_values != r_values
                sharp_instances += 1

    row = f"sharp_depth_collisions_r=2..8_m=2..5 instances={sharp_instances} status=verified"
    print(row)
    rows.append(row)

    digest = sha256("\n".join(rows).encode()).hexdigest()
    print(f"audit_sha256={digest}")


if __name__ == "__main__":
    main()
