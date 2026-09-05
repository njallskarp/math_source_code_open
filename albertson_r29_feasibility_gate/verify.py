#!/usr/bin/env python3
"""Exact pass-1 feasibility gate for the Albertson r=29 frontier.

The program uses Python integers and fractions.Fraction only.  It does not
import an r=27 or r=28 terminal result, a drawing database, or an external
crossing-number table.  The only numerical inputs are the six published
universal affine crossing inequalities recorded in BASE_LINES.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from math import comb


R = 29
RECURSIVE_MAX_ORDER = 59
CANDIDATE_ORDERS = (34, 35, *range(52, 82))


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def z_complete(r: int) -> int:
    """Zarankiewicz drawing upper bound for cr(K_r)."""
    return (
        (r // 2)
        * ((r - 1) // 2)
        * ((r - 2) // 2)
        * ((r - 3) // 2)
        // 4
    )


# Each entry is name, edge coefficient, coefficient of (n-2).
BASE_LINES = (
    ("zero", Fraction(0), Fraction(0)),
    ("Euler", Fraction(1), Fraction(-3)),
    ("PRTT-7/3", Fraction(7, 3), Fraction(-25, 3)),
    ("PRTT-4", Fraction(4), Fraction(-103, 6)),
    ("BK-37/9", Fraction(37, 9), Fraction(-155, 9)),
    ("BK-5", Fraction(5), Fraction(-203, 9)),
)


def base_candidates(n: int, q: int) -> tuple[tuple[str, int], ...]:
    return tuple(
        (name, ceil_fraction(a * q + b * (n - 2)))
        for name, a, b in BASE_LINES
    )


def base_values(n: int) -> list[int]:
    return [
        max(value for _, value in base_candidates(n, q))
        for q in range(comb(n, 2) + 1)
    ]


def lower_hull(values: list[int]) -> list[int]:
    """Indices of the greatest convex minorant of integer point values."""
    hull: list[int] = []
    for x in range(len(values)):
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            left = Fraction(values[b] - values[a], b - a)
            right = Fraction(values[x] - values[b], x - b)
            if left < right:
                break
            hull.pop()
        hull.append(x)
    assert hull[0] == 0 and hull[-1] == len(values) - 1
    return hull


def hull_value(
    values: list[int], hull: list[int], x: Fraction
) -> tuple[Fraction, int, int]:
    """Evaluate the piecewise-linear lower hull and return its endpoints."""
    if x.denominator == 1 and x.numerator in hull:
        q = x.numerator
        return Fraction(values[q]), q, q
    j = bisect_right(hull, x) - 1
    if j == len(hull) - 1:
        j -= 1
    q0, q1 = hull[j], hull[j + 1]
    assert q0 <= x <= q1
    y = Fraction(values[q0])
    y += Fraction(values[q1] - values[q0], q1 - q0) * (x - q0)
    return y, q0, q1


@dataclass(frozen=True)
class SampleWitness:
    sample_order: int
    left_q: int
    right_q: int
    mean_q: Fraction
    multiplier: Fraction
    unrounded: Fraction
    rounded: int


def build_base_tables(
    max_n: int,
) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[int]] = {}
    for n in range(4, max_n + 1):
        tables[n] = base_values(n)
        hulls[n] = lower_hull(tables[n])
    return tables, hulls


def build_recursive_tables(
    max_n: int,
) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    """Build the reviewed convex deletion recurrence in increasing order."""
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[int]] = {}
    for n in range(4, max_n + 1):
        values = base_values(n)
        for s in range(4, n):
            multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
            for q in range(len(values)):
                mean_q = Fraction(q * s * (s - 1), n * (n - 1))
                y, _, _ = hull_value(tables[s], hulls[s], mean_q)
                values[q] = max(values[q], ceil_fraction(multiplier * y))
        tables[n] = values
        hulls[n] = lower_hull(values)
    return tables, hulls


def direct_best(
    n: int,
    q: int,
    base_tables: dict[int, list[int]],
    base_hulls: dict[int, list[int]],
) -> tuple[Fraction, tuple[SampleWitness, ...]]:
    candidates = []
    for s in range(4, n + 1):
        multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
        mean_q = Fraction(q * s * (s - 1), n * (n - 1))
        y, q0, q1 = hull_value(base_tables[s], base_hulls[s], mean_q)
        unrounded = multiplier * y
        candidates.append(
            SampleWitness(
                s, q0, q1, mean_q, multiplier, unrounded,
                ceil_fraction(unrounded),
            )
        )
    best = max(w.unrounded for w in candidates)
    return best, tuple(w for w in candidates if w.unrounded == best)


def active_recursive_witnesses(
    n: int,
    q: int,
    tables: dict[int, list[int]],
    hulls: dict[int, list[int]],
) -> tuple[tuple[str, ...], tuple[SampleWitness, ...]]:
    target = tables[n][q]
    bases = tuple(name for name, value in base_candidates(n, q) if value == target)
    samples = []
    for s in range(4, n):
        multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
        mean_q = Fraction(q * s * (s - 1), n * (n - 1))
        y, q0, q1 = hull_value(tables[s], hulls[s], mean_q)
        unrounded = multiplier * y
        rounded = ceil_fraction(unrounded)
        if rounded == target:
            samples.append(
                SampleWitness(s, q0, q1, mean_q, multiplier, unrounded, rounded)
            )
    return bases, tuple(samples)


def sparse_dependency_nodes(
    roots: tuple[tuple[int, int], ...],
    tables: dict[int, list[int]],
    hulls: dict[int, list[int]],
) -> list[tuple[int, int, int, tuple[str, ...], tuple[SampleWitness, ...]]]:
    pending = list(roots)
    seen: set[tuple[int, int]] = set()
    records = []
    while pending:
        n, q = pending.pop()
        if (n, q) in seen:
            continue
        seen.add((n, q))
        bases, samples = active_recursive_witnesses(n, q, tables, hulls)
        records.append((n, q, tables[n][q], bases, samples))
        for witness in samples:
            pending.append((witness.sample_order, witness.left_q))
            pending.append((witness.sample_order, witness.right_q))
    records.sort()
    return records


def critical_edge_candidates(r: int, n: int) -> tuple[tuple[str, Fraction], ...]:
    """Published lower bounds on twice the number of edges."""
    bounds = [
        (
            "Kostochka-Yancey",
            Fraction((r + 1) * (r - 2) * n - r * (r - 3), r - 1),
        ),
        ("Cranston-Lemma-E", Fraction((r - 1) * n + 2 * r - 6)),
    ]
    if r + 2 <= n <= 2 * r - 2:
        bounds.append(
            (
                "Gallai",
                Fraction((r - 1) * n + (n - r) * (2 * r - n) - 2),
            )
        )
    return tuple(bounds)


def critical_edge_floor(r: int, n: int) -> int:
    return ceil_fraction(
        max(value for _, value in critical_edge_candidates(r, n)) / 2
    )


def critical_sources(r: int, n: int) -> tuple[str, ...]:
    bounds = critical_edge_candidates(r, n)
    best = max(value for _, value in bounds)
    return tuple(name for name, value in bounds if value == best)


def disconnected_complement_floor(r: int, n: int) -> int:
    """Two-branch join lower bound from Sadhu's Proposition 3.2 proof."""
    singleton = (
        (n - 1)
        + ceil_fraction(Fraction((r - 2) * (n - 1), 2))
        + r
        - 4
    )
    no_singleton = r * r + 3 * r - 19
    return min(singleton, no_singleton)


def recursive_ceiling(values: list[int], threshold: int) -> int:
    return max((q for q, value in enumerate(values) if value < threshold), default=-1)


def main() -> None:
    threshold = z_complete(R)
    assert threshold == 8281
    assert tuple(CANDIDATE_ORDERS) == (34, 35, *range(52, 82))

    base_tables, base_hulls = build_base_tables(max(CANDIDATE_ORDERS))
    recursive, recursive_hulls = build_recursive_tables(RECURSIVE_MAX_ORDER)

    # Independent soundness controls against exact known drawings.
    assert all(
        recursive[n][comb(n, 2)] <= z_complete(n)
        for n in range(5, RECURSIVE_MAX_ORDER + 1)
    )
    assert all(
        recursive[n][q] <= recursive[n][q + 1]
        for n in range(5, RECURSIVE_MAX_ORDER + 1)
        for q in range(comb(n, 2))
    )
    assert all(
        recursive[n][q] == 0
        for n in range(5, RECURSIVE_MAX_ORDER + 1)
        for q in range(0, 3 * n - 6)
    )

    # Direct published-line sampling dispatch over every candidate order.
    initial_rows = []
    for n in CANDIDATE_ORDERS:
        m0 = critical_edge_floor(R, n)
        direct, witnesses = direct_best(n, m0, base_tables, base_hulls)
        initial_rows.append(
            (n, m0, critical_sources(R, n), direct, ceil_fraction(direct), witnesses)
        )
    direct_survivors = tuple(
        (n, m, rounded)
        for n, m, _, _, rounded, _ in initial_rows
        if rounded < threshold
    )
    assert direct_survivors == (
        (56, 810, 7979),
        (57, 824, 8048),
        (58, 838, 8132),
        (59, 852, 8237),
    )

    # Recursive deletion closes n=59 and fixes the exact row ceilings.
    expected_frontier = {
        56: tuple(range(810, 817)),
        57: tuple(range(824, 829)),
        58: tuple(range(838, 841)),
        59: (),
    }
    for n, expected in expected_frontier.items():
        lo = critical_edge_floor(R, n)
        hi = recursive_ceiling(recursive[n], threshold)
        actual = tuple(range(lo, hi + 1)) if lo <= hi else ()
        assert actual == expected

    # Gallai forces a disconnected complement through order 56.  At order 56
    # its stronger edge floor closes the only residual family.  At 57 and 58,
    # the same conditional estimate rules out a disconnected complement.
    disconnected = {}
    for n, expected_floor in ((56, 823), (57, 837), (58, 852)):
        floor = disconnected_complement_floor(R, n)
        value = recursive[n][floor]
        assert floor == expected_floor and value >= threshold
        disconnected[n] = (floor, value)

    final_rows = tuple(
        (n, q, recursive[n][q])
        for n in (57, 58)
        for q in expected_frontier[n]
    )
    assert final_rows == (
        (57, 824, 8131),
        (57, 825, 8164),
        (57, 826, 8198),
        (57, 827, 8232),
        (57, 828, 8266),
        (58, 838, 8210),
        (58, 839, 8243),
        (58, 840, 8276),
    )

    # Degree excess over the critical minimum d=28.
    excess_rows = tuple((n, q, 2 * q - 28 * n) for n, q, _ in final_rows)
    assert excess_rows == (
        (57, 824, 52),
        (57, 825, 54),
        (57, 826, 56),
        (57, 827, 58),
        (57, 828, 60),
        (58, 838, 52),
        (58, 839, 54),
        (58, 840, 56),
    )
    # The elementary forced counts of degree-28 vertices are max(0,n-X).
    degree_28_minima = tuple((n, q, max(0, n - x)) for n, q, x in excess_rows)

    roots = (
        (56, 810), (56, 816), (56, 823),
        (57, 824), (57, 828), (57, 829), (57, 837),
        (58, 838), (58, 840), (58, 841), (58, 852),
        (59, 852),
    )
    dag = sparse_dependency_nodes(roots, recursive, recursive_hulls)

    canonical = []
    for n, m, sources, direct, rounded, witnesses in initial_rows:
        canonical.append(
            f"I|{n}|{m}|{','.join(sources)}|{direct}|{rounded}|"
            + ";".join(
                f"s{w.sample_order}[{w.left_q},{w.right_q}]"
                f"@{w.mean_q}*{w.multiplier}={w.unrounded}->{w.rounded}"
                for w in witnesses
            )
        )
    for n, q, value, bases, samples in dag:
        canonical.append(f"N|{n}|{q}|{value}|{','.join(bases)}")
        canonical.extend(
            f"S|{n}|{q}|{w.sample_order}|{w.left_q}|{w.right_q}|"
            f"{w.mean_q}|{w.multiplier}|{w.unrounded}|{w.rounded}"
            for w in samples
        )
    digest = sha256(("\n".join(canonical) + "\n").encode()).hexdigest()

    print("PASS clean-room Albertson r=29 feasibility gate")
    print(f"Z(29)={threshold}; counterexample_budget<={threshold - 1}")
    print("candidate_orders=34,35,52..81 (32 orders)")
    print(
        "direct_survivors="
        + ",".join(f"({n},{m},{value})" for n, m, value in direct_survivors)
    )
    print(
        "recursive_pre_join="
        + ",".join(
            f"n{n}:{expected_frontier[n][0]}..{expected_frontier[n][-1]}"
            if expected_frontier[n]
            else f"n{n}:closed"
            for n in (56, 57, 58, 59)
        )
    )
    print(
        "disconnected_bounds="
        + ",".join(
            f"n{n}:m>={floor}->cr>={value}"
            for n, (floor, value) in disconnected.items()
        )
    )
    print(
        "final_rows="
        + ",".join(f"({n},{q},{value})" for n, q, value in final_rows)
    )
    print(
        "degree_excess="
        + ",".join(f"({n},{q}):{x}" for n, q, x in excess_rows)
    )
    print(
        "forced_degree28_min="
        + ",".join(f"({n},{q}):{count}" for n, q, count in degree_28_minima)
    )
    print("complement_structure=n57:factor-critical;n58:each H-v has K3+27K2 factor")
    print(f"sparse_dependency_nodes={len(dag)}")
    print(f"provenance_sha256={digest}")


if __name__ == "__main__":
    main()
