#!/usr/bin/env python3
"""Exact certificate for the r=28 factor-critical/Hall deletion barrier."""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import comb


N = 55
BASE_LINES = (
    (Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(-3)),
    (Fraction(7, 3), Fraction(-25, 3)),
    (Fraction(37, 9), Fraction(-155, 9)),
    (Fraction(5), Fraction(-203, 9)),
)


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def lower_hull(values: list[int]) -> list[int]:
    hull: list[int] = []
    for x in range(len(values)):
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            if Fraction(values[b] - values[a], b - a) < Fraction(values[x] - values[b], x - b):
                break
            hull.pop()
        hull.append(x)
    return hull


def hull_value(values: list[int], hull: list[int], x: Fraction) -> Fraction:
    if x.denominator == 1 and x.numerator in hull:
        return Fraction(values[x.numerator])
    j = max(0, bisect_right(hull, x) - 1)
    if j == len(hull) - 1:
        j -= 1
    left, right = hull[j], hull[j + 1]
    assert left <= x <= right
    return Fraction(values[left]) + Fraction(values[right] - values[left], right - left) * (x - left)


def build_tables(max_n: int) -> dict[int, list[int]]:
    """Reviewed integer-rounded convex recurrence, using exact fractions."""
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[int]] = {}
    for n in range(4, max_n + 1):
        values = [
            max(ceil_fraction(slope * q + intercept * (n - 2)) for slope, intercept in BASE_LINES)
            for q in range(comb(n, 2) + 1)
        ]
        for s in range(4, n):
            multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
            for q in range(len(values)):
                mean = Fraction(q * s * (s - 1), n * (n - 1))
                values[q] = max(values[q], ceil_fraction(multiplier * hull_value(tables[s], hulls[s], mean)))
        tables[n] = values
        hulls[n] = lower_hull(values)
    return tables


def edge(a: int, b: int) -> tuple[int, int]:
    assert a != b
    return (a, b) if a < b else (b, a)


def circulant(chords: tuple[tuple[int, int], ...]) -> set[tuple[int, int]]:
    edges = {
        (a, b)
        for a in range(N)
        for b in range(a + 1, N)
        if min(b - a, N - (b - a)) <= 13
    }
    edges.update(edge(a, b) for a, b in chords)
    return edges


def adjacency(edges: set[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def translate_matching(pairs: tuple[tuple[int, int], ...], shift: int) -> tuple[tuple[int, int], ...]:
    return tuple(((a + shift) % N, (b + shift) % N) for a, b in pairs)


ROOT_ZERO_MATCHING = (
    tuple((i, i + 13) for i in range(1, 14))
    + ((27, 28),)
    + tuple((i, i - 13) for i in range(42, 55))
)
ROOT_27_MATCHING = (
    ((0, 54),)
    + tuple((i, i - 13) for i in range(14, 27))
    + tuple((i, i + 13) for i in range(28, 41))
)


def factor_critical_matching(deleted: int) -> tuple[tuple[int, int], ...]:
    return tuple(((deleted + 2 * j + 1) % N, (deleted + 2 * j + 2) % N) for j in range(27))


def check_matching(
    pairs: tuple[tuple[int, int], ...],
    deleted: int,
    edges: set[tuple[int, int]],
) -> None:
    flattened = [v for pair in pairs for v in pair]
    assert len(pairs) == 27
    assert len(set(flattened)) == 54
    assert set(flattened) == set(range(N)) - {deleted}
    assert all(edge(a, b) in edges for a, b in pairs)


def root_matching(row: int, root: int) -> tuple[tuple[int, int], ...]:
    if root == 0:
        return ROOT_ZERO_MATCHING
    if root == 27:
        return ROOT_27_MATCHING
    if row == 768 and root == 1:
        return translate_matching(ROOT_ZERO_MATCHING, 1)
    if row == 768 and root == 28:
        return translate_matching(ROOT_27_MATCHING, 1)
    raise AssertionError((row, root))


def histogram_text(counter: Counter[int]) -> str:
    return ",".join(f"{key}:{counter[key]}" for key in sorted(counter))


def audit_row(
    row: int,
    chords: tuple[tuple[int, int], ...],
    tables: dict[int, list[int]],
) -> tuple[str, ...]:
    h_edges = circulant(chords)
    h_adj = adjacency(h_edges)
    g_edges = comb(N, 2) - len(h_edges)
    assert g_edges == row

    # The spanning 55-cycle proves factor-criticality explicitly.
    for deleted in range(N):
        check_matching(factor_critical_matching(deleted), deleted, h_edges)

    x = [27 - len(h_adj[v]) for v in range(N)]
    roots = tuple(v for v in range(N) if x[v] == 0)
    expected_roots = (0, 1, 27, 28) if row == 768 else (0, 27)
    assert roots == expected_roots
    assert Counter(x) == (Counter({0: 4, 1: 51}) if row == 768 else Counter({0: 2, 1: 53}))

    # Every minimum-degree root has the exact balanced Hall matching asserted
    # by the frontier theorem.
    for root in roots:
        pairs = root_matching(row, root)
        check_matching(pairs, root, h_edges)
        neighborhood = h_adj[root]
        assert len(neighborhood) == 27
        assert all((a in neighborhood) != (b in neighborhood) for a, b in pairs)

    # Exact one-vertex deletion functional.
    one_sum = sum(tables[54][row - 27 - value] for value in x)
    one_bound = ceil_fraction(Fraction(one_sum, 51))
    assert (one_sum, one_bound) == ((360044, 7060) if row == 768 else (361685, 7092))

    # Exact pair deficits and the two-vertex deletion functional.
    deficits: Counter[int] = Counter()
    pair_sum = 0
    sum_d = 0
    sum_d2 = 0
    for u in range(N):
        for v in range(u + 1, N):
            d = x[u] + x[v] + int((u, v) in h_edges)
            deficits[d] += 1
            sum_d += d
            sum_d2 += d * d
            pair_sum += tables[53][row - 53 - d]
    pair_bound = ceil_fraction(Fraction(pair_sum, comb(51, 2)))

    if row == 768:
        assert deficits == Counter({0: 2, 1: 108, 2: 762, 3: 613})
        assert (sum_d, sum_d2, pair_sum, pair_bound) == (3471, 8673, 9000908, 7060)
    else:
        assert deficits == Counter({1: 55, 2: 767, 3: 663})
        assert (sum_d, sum_d2, pair_sum, pair_bound) == (3578, 9090, 9040923, 7091)

    # The precise missing invariant: a conformal triangle.  Removing the
    # consecutive triangle {0,1,2} leaves a consecutive-path matching.
    triangle = {(0, 1), (0, 2), (1, 2)}
    assert triangle <= h_edges
    conformal = tuple((v, v + 1) for v in range(3, 55, 2))
    assert len(conformal) == 26
    assert {v for pair in conformal for v in pair} == set(range(3, 55))
    assert all(edge(a, b) in h_edges for a, b in conformal)

    return (
        f"row={row} H_edges={len(h_edges)} G_edges={g_edges} "
        f"excess={histogram_text(Counter(x))} roots={','.join(map(str, roots))}",
        f"row={row} one_deletion_sum={one_sum} bound={one_bound}",
        f"row={row} pair_deficits={histogram_text(deficits)} "
        f"moments={sum_d},{sum_d2} pair_deletion_sum={pair_sum} bound={pair_bound}",
        f"row={row} conformal_triangle=0,1,2 remainder_matching=26",
        "E|" + ";".join(f"{a}-{b}" for a, b in sorted(h_edges)),
        "R|" + ";".join(
            f"{root}:" + ",".join(f"{a}-{b}" for a, b in root_matching(row, root))
            for root in roots
        ),
    )


def main() -> None:
    tables = build_tables(54)
    rows = []
    rows.extend(audit_row(768, ((0, 27), (1, 28)), tables))
    rows.extend(audit_row(769, ((0, 27),), tables))

    print("PASS Albertson r=28 pair-deletion barrier")
    for record in rows:
        if not record.startswith(("E|", "R|")):
            print(record)
    digest = sha256(("\n".join(rows) + "\n").encode()).hexdigest()
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
