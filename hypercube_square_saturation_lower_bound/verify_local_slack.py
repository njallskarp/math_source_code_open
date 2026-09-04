#!/usr/bin/env python3
"""Exact audit for the local Q_3 slack lemma and the first small cases.

No part of the universal proof depends on this enumeration.  All arithmetic
here is integer arithmetic and the largest search has 2^12 = 4096 masks.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction


def cube(d: int) -> tuple[list[tuple[int, int]], list[tuple[int, ...]]]:
    """Return canonically ordered edges and square faces of Q_d."""
    edges: list[tuple[int, int]] = []
    for direction in range(d):
        for vertex in range(1 << d):
            if (vertex >> direction) & 1 == 0:
                edges.append((vertex, vertex ^ (1 << direction)))
    edge_index = {tuple(sorted(edge)): i for i, edge in enumerate(edges)}

    faces: set[tuple[int, ...]] = set()
    for i in range(d):
        for j in range(i + 1, d):
            for base in range(1 << d):
                if (base >> i) & 1 or (base >> j) & 1:
                    continue
                vi = base ^ (1 << i)
                vj = base ^ (1 << j)
                vij = vi ^ (1 << j)
                face_edges = (
                    edge_index[tuple(sorted((base, vi)))],
                    edge_index[tuple(sorted((base, vj)))],
                    edge_index[tuple(sorted((vi, vij)))],
                    edge_index[tuple(sorted((vj, vij)))],
                )
                faces.add(tuple(sorted(face_edges)))
    return edges, sorted(faces)


def selected_count(mask: int, face: tuple[int, ...]) -> int:
    return sum((mask >> edge) & 1 for edge in face)


def audit_local_lemma() -> tuple[int, int, Counter[int], int, int]:
    edges, faces = cube(3)
    assert len(edges) == 12
    assert len(faces) == 6
    assert all(sum(edge in face for face in faces) == 2 for edge in range(12))

    square_free = 0
    active_patterns = 0
    active_profile: Counter[int] = Counter()
    minimum_twice_slack: int | None = None
    equality_patterns = 0

    for mask in range(1 << len(edges)):
        counts = [selected_count(mask, face) for face in faces]
        if 4 in counts:
            continue
        square_free += 1
        active = [face for face, count in zip(faces, counts) if count == 3]
        t = len(active)
        if t == 0:
            continue
        active_patterns += 1
        active_profile[t] += 1
        missing_edges = [
            next(edge for edge in face if (mask >> edge) & 1 == 0)
            for face in active
        ]
        r = len(set(missing_edges))
        b = sum(count for count in counts if count < 3)

        # Twice (b + 2(t-r) - t/2), kept integral.
        twice_slack = 2 * b + 4 * (t - r) - t
        assert twice_slack >= 0
        if minimum_twice_slack is None or twice_slack < minimum_twice_slack:
            minimum_twice_slack = twice_slack
            equality_patterns = 1
        elif twice_slack == minimum_twice_slack:
            equality_patterns += 1

    assert minimum_twice_slack is not None
    return (
        square_free,
        active_patterns,
        active_profile,
        minimum_twice_slack,
        equality_patterns,
    )


def saturated_statistics(d: int) -> tuple[int, int, Counter[int]]:
    edges, faces = cube(d)
    assert len(edges) <= 12, "small-case audit is intentionally bounded"
    edge_faces = [
        [face for face in faces if edge in face] for edge in range(len(edges))
    ]
    sizes: Counter[int] = Counter()
    for mask in range(1 << len(edges)):
        counts = {face: selected_count(mask, face) for face in faces}
        if any(count == 4 for count in counts.values()):
            continue
        saturated = True
        for edge in range(len(edges)):
            if (mask >> edge) & 1:
                continue
            if not any(counts[face] == 3 for face in edge_faces[edge]):
                saturated = False
                break
        if saturated:
            sizes[mask.bit_count()] += 1
    assert sizes
    return sum(sizes.values()), min(sizes), sizes


def ceiling(value: Fraction) -> int:
    return (value.numerator + value.denominator - 1) // value.denominator


def main() -> None:
    square_free, active, profile, min_slack, equality = audit_local_lemma()
    print("q3_edges=12 q3_faces=6")
    print(f"square_free_patterns={square_free} active_patterns={active}")
    print(
        "active_face_profile="
        + ",".join(f"t{t}:{profile[t]}" for t in sorted(profile))
    )
    print(
        f"local_min_twice_slack={min_slack} "
        f"local_equality_patterns={equality}"
    )

    for d in (2, 3):
        count, minimum, sizes = saturated_statistics(d)
        distribution = ",".join(f"e{e}:{sizes[e]}" for e in sorted(sizes))
        print(
            f"square_saturated_q{d}=count:{count},min:{minimum},"
            f"distribution:{distribution}"
        )

    bounds = []
    for d in range(3, 11):
        exact = Fraction(7 * d * (1 << (d - 1)), 2 * d + 5)
        bounds.append(f"d{d}:{ceiling(exact)}")
    print("theorem_integer_bounds=" + ",".join(bounds))
    print("status=PASS")


if __name__ == "__main__":
    main()
