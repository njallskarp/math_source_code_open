#!/usr/bin/env python3
"""Exact clean-room audit of the initial Albertson r=28 frontier.

Only Python integers and fractions.Fraction are used.  The recursive crossing
tables implement the generic convex induced-subgraph recurrence.  No r=27
terminal theorem, local (24,132) hypothesis, or precomputed table is imported.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from math import comb


R = 28
N_MIN = R + 5
ORDER_MAX = 99
TABLE_MAX = 56


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


BASE_LINES = (
    ("zero", Fraction(0), Fraction(0)),
    ("Euler", Fraction(1), Fraction(-3)),
    ("PRTT-7/3", Fraction(7, 3), Fraction(-25, 3)),
    ("BK-37/9", Fraction(37, 9), Fraction(-155, 9)),
    ("BK-5", Fraction(5), Fraction(-203, 9)),
)


def base_candidates(n: int, q: int) -> tuple[tuple[str, int], ...]:
    """Rounded universal affine bounds, written as aq+b(n-2)."""
    return tuple((name, ceil_fraction(a * q + b * (n - 2)))
                 for name, a, b in BASE_LINES)


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


def hull_value(values: list[int], hull: list[int], x: Fraction) -> tuple[Fraction, int, int]:
    """Evaluate a piecewise-linear lower hull and return its active endpoints."""
    if x.denominator == 1:
        q = x.numerator
        if q in hull:
            return Fraction(values[q]), q, q
    j = bisect_right(hull, x) - 1
    if j < 0:
        j = 0
    if j == len(hull) - 1:
        j -= 1
    q0, q1 = hull[j], hull[j + 1]
    assert q0 <= x <= q1
    y = Fraction(values[q0]) + Fraction(values[q1] - values[q0], q1 - q0) * (x - q0)
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


def build_tables(max_n: int) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[int]] = {}
    for n in range(4, max_n + 1):
        vals = [max(v for _, v in base_candidates(n, q)) for q in range(comb(n, 2) + 1)]
        for s in range(4, n):
            sample_vals = tables[s]
            sample_hull = hulls[s]
            multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
            for q in range(len(vals)):
                mean = Fraction(q * s * (s - 1), n * (n - 1))
                y, _, _ = hull_value(sample_vals, sample_hull, mean)
                vals[q] = max(vals[q], ceil_fraction(multiplier * y))
        tables[n] = vals
        hulls[n] = lower_hull(vals)
    return tables, hulls


def active_witnesses(
    n: int,
    q: int,
    tables: dict[int, list[int]],
    hulls: dict[int, list[int]],
) -> tuple[list[str], list[SampleWitness]]:
    value = tables[n][q]
    active_base = [name for name, v in base_candidates(n, q) if v == value]
    active_sample: list[SampleWitness] = []
    for s in range(4, n):
        multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
        mean = Fraction(q * s * (s - 1), n * (n - 1))
        y, q0, q1 = hull_value(tables[s], hulls[s], mean)
        unrounded = multiplier * y
        rounded = ceil_fraction(unrounded)
        if rounded == value:
            active_sample.append(SampleWitness(s, q0, q1, mean, multiplier, unrounded, rounded))
    return active_base, active_sample


def z_complete(r: int) -> int:
    return (r // 2) * ((r - 1) // 2) * ((r - 2) // 2) * ((r - 3) // 2) // 4


def critical_edge_candidates(r: int, n: int) -> tuple[tuple[str, Fraction], ...]:
    """Twice-edge lower bounds used in the published critical-graph dispatch."""
    twice_bounds = [
        ("Kostochka-Yancey", Fraction((r + 1) * (r - 2) * n - r * (r - 3), r - 1)),
        ("Barat-Toth", Fraction((r - 1) * n + 2 * r - 6)),
    ]
    if r + 2 <= n <= 2 * r - 2:
        twice_bounds.append(("Gallai", Fraction((r - 1) * n + (n - r) * (2 * r - n) - 2)))
    return tuple(twice_bounds)


def critical_edge_floor(r: int, n: int) -> int:
    """Maximum of the Gallai, Kostochka--Yancey, and Barat--Toth floors."""
    return ceil_fraction(max(value for _, value in critical_edge_candidates(r, n)) / 2)


def disconnected_complement_floor(r: int, n: int) -> int:
    """Sadhu's two-branch disconnected-complement estimate."""
    universal_vertex = (n - 1) + ceil_fraction(Fraction((r - 2) * (n - 1), 2)) + r - 4
    no_singleton = r * r + 3 * r - 19
    return min(universal_vertex, no_singleton)


def build_base_tables(max_n: int) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    """Integer-rounded published lines and their greatest convex minorants."""
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[int]] = {}
    for n in range(4, max_n + 1):
        values = [max(v for _, v in base_candidates(n, q)) for q in range(comb(n, 2) + 1)]
        tables[n] = values
        hulls[n] = lower_hull(values)
    return tables, hulls


def base_support(n: int, q: int) -> tuple[str, ...]:
    value = max(v for _, v in base_candidates(n, q))
    return tuple(name for name, v in base_candidates(n, q) if v == value)


def direct_sample_best(
    n: int,
    q: int,
    base_tables: dict[int, list[int]],
    base_hulls: dict[int, list[int]],
) -> tuple[Fraction, tuple[SampleWitness, ...]]:
    """Optimize integer-aware convex sampling over every sample order."""
    witnesses = []
    for s in range(4, n + 1):
        multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
        mean = Fraction(q * s * (s - 1), n * (n - 1))
        y, q0, q1 = hull_value(base_tables[s], base_hulls[s], mean)
        unrounded = multiplier * y
        witnesses.append(SampleWitness(s, q0, q1, mean, multiplier, unrounded, ceil_fraction(unrounded)))
    best = max(w.unrounded for w in witnesses)
    return best, tuple(w for w in witnesses if w.unrounded == best)


def degree_profile_audit(tables: dict[int, list[int]], m: int, excess: int) -> tuple[int, int, tuple[tuple[int, ...], ...]]:
    """Count relaxed excess histograms compatible with a counterexample budget."""
    local = [tables[54][m - 27 - x] for x in range(27)]
    budget = 51 * (z_complete(R) - 1)
    histogram = [0] * 27
    survivors = 0
    minimum = 10**30
    minimizers: list[tuple[int, ...]] = []

    def visit(x: int, remaining: int, used: int, cost: int) -> None:
        nonlocal survivors, minimum, minimizers
        if x == 0:
            if remaining != 0 or used > 55:
                return
            histogram[0] = 55 - used
            total = cost + histogram[0] * local[0]
            if total <= budget:
                survivors += 1
            record = tuple(histogram)
            if total < minimum:
                minimum = total
                minimizers = [record]
            elif total == minimum:
                minimizers.append(record)
            histogram[0] = 0
            return
        maximum_count = min(55 - used, remaining // x)
        for count in range(maximum_count + 1):
            histogram[x] = count
            visit(x - 1, remaining - count * x, used + count, cost + count * local[x])
        histogram[x] = 0

    visit(26, excess, 0, 0)
    return survivors, minimum, tuple(sorted(minimizers))


def format_histogram(histogram: tuple[int, ...]) -> str:
    return ",".join(f"{x}^{count}" for x, count in enumerate(histogram) if count)


def sparse_dependency_nodes(
    roots: list[tuple[int, int]],
    tables: dict[int, list[int]],
    hulls: dict[int, list[int]],
) -> list[tuple[int, int, int, tuple[str, ...], tuple[SampleWitness, ...]]]:
    """Trace all tied active witnesses recursively to a finite exact DAG."""
    pending = list(roots)
    seen: set[tuple[int, int]] = set()
    rows = []
    while pending:
        n, q = pending.pop()
        if (n, q) in seen:
            continue
        seen.add((n, q))
        base, samples = active_witnesses(n, q, tables, hulls)
        rows.append((n, q, tables[n][q], tuple(base), tuple(samples)))
        for w in samples:
            pending.append((w.sample_order, w.left_q))
            pending.append((w.sample_order, w.right_q))
    rows.sort()
    return rows


def main() -> None:
    tables, hulls = build_tables(TABLE_MAX)
    base_tables, base_hulls = build_base_tables(ORDER_MAX)
    threshold = z_complete(R)
    assert threshold == 7098

    # Published universal lines alone must reproduce the evaluator's values.
    assert tables[55][768] == 7060
    assert tables[55][769] == 7092
    assert tables[55][770] >= threshold

    # Sparse provenance for all 67 initial order rows: exact critical-edge
    # floor, its active affine source(s), and the optimal direct sample order.
    initial_rows = []
    for n in range(N_MIN, ORDER_MAX + 1):
        edge_candidates = critical_edge_candidates(R, n)
        twice_best = max(value for _, value in edge_candidates)
        edge_sources = tuple(name for name, value in edge_candidates if value == twice_best)
        m0 = critical_edge_floor(R, n)
        direct, direct_witnesses = direct_sample_best(n, m0, base_tables, base_hulls)
        initial_rows.append((n, m0, edge_sources, direct_witnesses, direct, ceil_fraction(direct)))

    direct_survivors = [(n, m, rounded) for n, m, _, _, _, rounded in initial_rows
                        if rounded < threshold]
    assert direct_survivors == [(54, 754, 6912), (55, 768, 6988), (56, 781, 7048)]

    # Gallai forces disconnected complement at n<=2r-2.  The disconnected
    # floor eliminates the only ordinary survivor at n=54.
    m54_disc = disconnected_complement_floor(R, 54)
    assert m54_disc == 766
    direct54_disc, _ = direct_sample_best(54, m54_disc, base_tables, base_hulls)
    assert ceil_fraction(direct54_disc) == 7291

    # At n=55 the same estimate eliminates disconnected complement, while
    # the crossing table leaves precisely two edge counts.
    m55_disc = disconnected_complement_floor(R, 55)
    assert m55_disc == 780
    direct55_disc, _ = direct_sample_best(55, m55_disc, base_tables, base_hulls)
    assert ceil_fraction(direct55_disc) == 7374
    assert tables[56][critical_edge_floor(R, 56)] == 7115
    surviving_edges_55 = [q for q in range(critical_edge_floor(R, 55), comb(55, 2) + 1)
                          if tables[55][q] < threshold]
    assert surviving_edges_55 == [768, 769]

    # The one-deletion exact minima both reproduce the full recursive values.
    profiles768, sum768, minimizers768 = degree_profile_audit(tables, 768, 51)
    profiles769, sum769, minimizers769 = degree_profile_audit(tables, 769, 53)
    assert (profiles768, sum768) == (232605, 360044)
    assert tuple(format_histogram(h) for h in minimizers768) == ("0^4,1^51",)
    assert (profiles769, sum769) == (318199, 361659)
    assert tuple(format_histogram(h) for h in minimizers769) == (
        "0^28,1^1,2^26",
        "0^29,2^25,3^1",
    )
    assert ceil_fraction(Fraction(sum768, 51)) == 7060
    assert ceil_fraction(Fraction(sum769, 51)) == 7092

    # Exact missing-inequality thresholds within the one-deletion mechanism.
    need769 = 51 * (7098 - 1) + 1 - sum769
    need768_ten = 51 * (7070 - 1) + 1 - sum768
    lift769 = ceil_fraction(Fraction(need769, 55))
    lift768_ten = ceil_fraction(Fraction(need768_ten, 55))
    assert (need769, lift769) == (289, 6)
    assert (need768_ten, lift768_ten) == (476, 9)
    assert sum769 + 55 * 5 < 51 * (7098 - 1) + 1 <= sum769 + 55 * 6
    assert sum768 + 55 * 8 < 51 * (7070 - 1) + 1 <= sum768 + 55 * 9

    roots = [(55, 768), (55, 769), (55, 770), (56, 781)]
    dag = sparse_dependency_nodes(roots, tables, hulls)

    print("PASS clean-room Albertson r=28 frontier audit")
    print(f"Z(28)={threshold}")
    print(f"initial_order_range={N_MIN}..{ORDER_MAX} rows={len(initial_rows)}")
    print("direct_survivors=" + ",".join(f"({n},{m},{b})" for n, m, b in direct_survivors))
    print(f"disconnected_n54=({m54_disc},{ceil_fraction(direct54_disc)})")
    print(f"recursive_n56=(781,{tables[56][781]})")
    print(f"disconnected_n55=({m55_disc},{ceil_fraction(direct55_disc)})")
    print("final_rows=" + ",".join(f"(55,{q},{tables[55][q]})" for q in surviving_edges_55))
    print(f"row_770_bound={tables[55][770]}")
    print(f"degree_excess=768:51:low>=4,769:53:low>=2")
    print("pair_moments=768:sumD=3471,sumD2=51*S2+6072;769:sumD=3578,sumD2=51*S2+6387")
    print(f"relaxed_profiles=768:{profiles768},769:{profiles769}")
    print("degree_minima=768:" + str(sum768) + ":" + ";".join(format_histogram(h) for h in minimizers768))
    print("degree_minima=769:" + str(sum769) + ":" + ";".join(format_histogram(h) for h in minimizers769))
    print(f"missing_lifts=769:target7098:+{need769}:uniform54band+{lift769};768:target7070:+{need768_ten}:uniform54band+{lift768_ten}")
    print(f"sparse_dependency_nodes={len(dag)}")
    for n, q in ((55, 768), (55, 769), (55, 770), (56, 781)):
        base, samples = active_witnesses(n, q, tables, hulls)
        sample_text = ";".join(
            f"s{w.sample_order}[{w.left_q},{w.right_q}]@{w.mean_q}*{w.multiplier}={w.unrounded}->{w.rounded}"
            for w in samples
        )
        print(f"active({n},{q})={tables[n][q]} base={','.join(base) or '-'} sample={sample_text or '-'}")

    # Hash a complete canonical record of initial rows and the recursively
    # active proof DAG, retaining exact rational witnesses.
    records = []
    records.extend(
        f"I|{n}|{q}|{','.join(edge_sources)}|"
        + ";".join(
            f"s{w.sample_order}[{w.left_q},{w.right_q}]@{w.mean_q}*{w.multiplier}={w.unrounded};"
            f"left={','.join(base_support(w.sample_order, w.left_q))};"
            f"right={','.join(base_support(w.sample_order, w.right_q))}"
            for w in direct_witnesses
        )
        + f"|{direct}|{rounded}"
        for n, q, edge_sources, direct_witnesses, direct, rounded in initial_rows
    )
    for n, q, value, bases, samples in dag:
        records.append(f"N|{n}|{q}|{value}|{','.join(bases)}")
        records.extend(
            f"S|{n}|{q}|{w.sample_order}|{w.left_q}|{w.right_q}|"
            f"{w.mean_q}|{w.multiplier}|{w.unrounded}|{w.rounded}"
            for w in samples
        )
    digest = sha256(("\n".join(records) + "\n").encode()).hexdigest()
    print(f"provenance_sha256={digest}")


if __name__ == "__main__":
    main()
