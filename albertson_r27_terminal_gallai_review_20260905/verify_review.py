#!/usr/bin/env python3
"""Independent exact audit of Discovery Net height-2659 Albertson r=27 proof.

This is an independent, target-specific checker.  It imports no campaign code
and uses only Python integers and fractions.Fraction.  It independently rebuilds
the recursive crossing lower bounds, enumerates every relaxed Tutte-barrier
component multiset at (n,m,r)=(53,713,27), and enumerates Gallai block-increment
partitions by a representation different from the target's dynamic program.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json


N = 53
R = 27
M = 713
X = 2 * M - N * (R - 1)


def ceil_fraction(value):
    return -((-value.numerator) // value.denominator)


def falling(n, length):
    product = 1
    for offset in range(length):
        product *= n - offset
    return product


def hill(n):
    return (
        (n // 2)
        * ((n - 1) // 2)
        * ((n - 2) // 2)
        * ((n - 3) // 2)
        // 4
    )


def base_crossing_bound(n, edges):
    candidates = (
        0,
        edges - (3 * n - 6),
        ceil_fraction(Fraction(7 * edges - 25 * (n - 2), 3)),
        ceil_fraction(Fraction(24 * edges - 103 * (n - 2), 6)),
        ceil_fraction(Fraction(45 * edges - 203 * (n - 2), 9)),
    )
    return max(candidates)


def lower_hull(values):
    """Vertices of the greatest convex minorant of integer-indexed values."""
    hull = []
    for point in enumerate(values):
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            if (y1 - y0) * (x2 - x0) >= (y2 - y0) * (x1 - x0):
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def hull_value(hull, x):
    if x.denominator == 1:
        # The hull can pass strictly below an integer data point, so do not
        # return that data point without locating the containing hull edge.
        pass
    left = 0
    right = len(hull) - 1
    while right - left > 1:
        middle = (left + right) // 2
        if hull[middle][0] <= x:
            left = middle
        else:
            right = middle
    x0, y0 = hull[left]
    x1, y1 = hull[right]
    if x0 == x1:
        return Fraction(y0)
    return Fraction(y0) + Fraction(y1 - y0, x1 - x0) * (x - x0)


def brute_convex_closure(values, x):
    """Definition-level two-support LP, used to test the hull evaluator."""
    best = None
    for i in range(len(values)):
        if i > x:
            break
        for j in range(i, len(values)):
            if x > j:
                continue
            if i == j:
                candidate = Fraction(values[i])
            else:
                candidate = (
                    Fraction(j - x, j - i) * values[i]
                    + Fraction(x - i, j - i) * values[j]
                )
            if best is None or candidate < best:
                best = candidate
    return best


def recursive_bounds(limit):
    bounds = {
        n: [base_crossing_bound(n, q) for q in range(n * (n - 1) // 2 + 1)]
        for n in range(3, limit + 1)
    }
    sweeps = 0
    while True:
        changed = False
        sweeps += 1
        for n in range(5, limit + 1):
            updated = list(bounds[n])
            scale_n = falling(n, 4)
            for sample_size in range(4, n):
                hull = lower_hull(bounds[sample_size])
                amplification = Fraction(scale_n, falling(sample_size, 4))
                for q in range(len(updated)):
                    mean_edges = Fraction(
                        q * sample_size * (sample_size - 1), n * (n - 1)
                    )
                    candidate = ceil_fraction(
                        hull_value(hull, mean_edges) * amplification
                    )
                    if candidate > updated[q]:
                        updated[q] = candidate
                        changed = True
            bounds[n] = updated
        if not changed:
            return bounds, sweeps
        if sweeps >= 8:
            raise AssertionError("recursive lower bounds did not stabilize")


EXACT_COMPLETE = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 1,
    6: 3,
    7: 9,
    8: 18,
    9: 36,
    10: 60,
    11: 100,
    12: 150,
    13: 225,
    14: 315,
}


@lru_cache(maxsize=None)
def complete_lower(order):
    if order in EXACT_COMPLETE:
        return EXACT_COMPLETE[order]
    return ceil_fraction(Fraction(order * complete_lower(order - 1), order - 4))


@lru_cache(maxsize=None)
def complete_lower_through_12(order):
    """Conservative variant that does not use the exact K_13 and K_14 values."""
    if order <= 12:
        return EXACT_COMPLETE[order]
    return ceil_fraction(
        Fraction(order * complete_lower_through_12(order - 1), order - 4)
    )


def bipartite_lower(a, b):
    answer = 0
    for six_side, other_side in ((a, b), (b, a)):
        if six_side >= 6:
            k6n = 6 * (other_side // 2) * ((other_side - 1) // 2)
            answer = max(answer, six_side * (six_side - 1) * k6n // 30)
    return answer


def best_component_bipartition(parts):
    subset_sums = {0}
    for size in parts:
        subset_sums |= {old + size for old in tuple(subset_sums)}
    total = sum(parts)
    return max(bipartite_lower(side, total - side) for side in subset_sums)


def component_partitions(total, minimum_odd, boundary_size, budget):
    """All nonincreasing component-size multisets allowed by the relaxation."""
    result = []
    free_degree = R - boundary_size

    def visit(remaining, cap, current, forced_excess):
        if remaining == 0:
            if sum(size % 2 for size in current) >= minimum_odd:
                result.append(tuple(current))
            return
        for size in range(min(cap, remaining), 0, -1):
            new_excess = forced_excess + size * max(0, free_degree - size)
            if new_excess <= budget:
                visit(remaining - size, size, current + (size,), new_excess)

    visit(total, total, (), 0)
    return result


def crossing_lower(table, vertices, edges):
    if vertices < 3 or edges <= 0:
        return 0
    assert edges <= vertices * (vertices - 1) // 2
    return table[vertices][edges]


def barrier_survivors(table, complete_bound=complete_lower):
    complement_edges = N * (N - 1) // 2 - M
    target = hill(R)
    survivors = {}

    for b in range(3, N + 1):
        component_total = N - b
        if component_total < b - 1:
            continue
        parts_list = component_partitions(component_total, b - 1, b, X)
        live = []
        for parts in parts_list:
            D = sum(parts)
            cross_upper = (
                D * (b - R + 1)
                + X
                + 2 * sum(size * (size - 1) // 2 for size in parts)
            )
            cross_lower = max(b * max(0, R - b), D * max(0, R - D))
            if cross_lower > cross_upper:
                continue

            part_count = len(parts)
            if part_count >= R:
                continue
            if part_count == R - 1 and sorted(parts) == [1] * (R - 2) + [2]:
                forced_g_edges = ceil_fraction(
                    Fraction(b * (R - 1) - cross_upper, 2)
                )
                if forced_g_edges > (b - 1) * (b - 2) // 2:
                    continue

            bipartite = best_component_bipartition(parts)
            if bipartite > target:
                continue

            y_min = sum(size * max(0, R - size - b) for size in parts)
            p_min = sum(size - 1 for size in parts)
            p_max = sum(size * (size - 1) // 2 for size in parts)
            complete_D = D * (D - 1) // 2
            complete_B = b * (b - 1) // 2
            best_split = None
            for y in range(y_min, X + 1):
                q_B = min(
                    complete_B,
                    p_max - D * (R - 1) + y + complement_edges,
                )
                if q_B < 3:
                    continue
                p_D = D * (R - 1) - y - complement_edges + q_B
                if not p_min <= p_D <= p_max:
                    continue
                lower_D = max(
                    complete_bound(part_count),
                    crossing_lower(table, D, complete_D - p_D),
                    bipartite,
                )
                lower_B = crossing_lower(table, b, complete_B - q_B)
                split = lower_D + lower_B
                if best_split is None or split < best_split:
                    best_split = split
            if best_split is not None and best_split <= target:
                live.append(parts)
        if live:
            survivors[b] = live
    return survivors


def triangle_free_totals(table, complete_bound=complete_lower):
    complement_edges = N * (N - 1) // 2 - M
    totals = []
    for minimum_excess in range(R):
        if N * minimum_excess > X:
            break
        clique_order = (R - 1) - minimum_excess
        rest_order = N - clique_order
        rest_edges = (
            rest_order * (rest_order - 1) // 2
            - complement_edges
            + clique_order * (R - 1)
            - X
        )
        totals.append(
            (
                minimum_excess,
                complete_bound(clique_order)
                + crossing_lower(table, rest_order, rest_edges),
            )
        )
    return totals


def integer_partitions(total, cap=None):
    """Nonincreasing positive integer partitions of total."""
    if total == 0:
        yield ()
        return
    if cap is None or cap > total:
        cap = total
    for first in range(cap, 0, -1):
        for tail in integer_partitions(total - first, first):
            yield (first,) + tail


def relaxed_block_edges(increments):
    """Largest edges for this block-increment multiset, or None if invalid.

    A clique block with increment u=|Q|-1 is allowed for u<=23; one u=24
    may be promoted from a 25-cycle to K_25.  For larger u only an odd cycle,
    equivalently even u, is allowed.
    """
    edges = 0
    promotable_24 = 0
    for u in increments:
        if u <= 23:
            edges += u * (u + 1) // 2
        elif u == 24:
            edges += 25
            promotable_24 += 1
        elif u % 2 == 0:
            edges += u + 1
        else:
            return None
    if promotable_24:
        edges += 300 - 25
    return edges


def gallai_capacity(vertices):
    best = -1
    witness = None
    best_components = None
    for components in range(1, vertices + 1):
        increment_total = vertices - components
        for increments in integer_partitions(increment_total):
            edges = relaxed_block_edges(increments)
            if edges is not None and edges > best:
                best = edges
                witness = increments
                best_components = components
    return best, best_components, witness


def main():
    table, sweeps = recursive_bounds(54)

    # Definition-level checks of the convex-envelope implementation.
    for sample_order in range(4, 11):
        values = table[sample_order]
        hull = lower_hull(values)
        last = len(values) - 1
        probes = {
            Fraction(0),
            Fraction(last),
            Fraction(last, 2),
            Fraction(last, 3),
            Fraction(2 * last, 3),
        }
        for probe in probes:
            assert hull_value(hull, probe) == brute_convex_closure(values, probe)

    frontier = {
        "L53_713": table[53][713],
        "L53_714": table[53][714],
        "L54_725": table[54][725],
        "L54_726": table[54][726],
        "floor53": ceil_fraction(Fraction(53 * 26 + 48, 2)),
        "floor54": ceil_fraction(Fraction(54 * 26 + 48, 2)),
    }
    assert frontier == {
        "L53_713": 6071,
        "L53_714": 6100,
        "L54_725": 6106,
        "L54_726": 6134,
        "floor53": 713,
        "floor54": 726,
    }

    triangle = triangle_free_totals(table)
    assert triangle == [(0, 7249)]

    barriers = barrier_survivors(table)
    expected_barriers = {3: [(49, 1), (48, 1, 1)], 4: [(47, 1, 1)]}
    assert barriers == expected_barriers
    conservative_barriers = barrier_survivors(table, complete_lower_through_12)
    assert conservative_barriers == expected_barriers
    conservative_triangle = triangle_free_totals(table, complete_lower_through_12)
    assert conservative_triangle == [(0, 7088)]
    assert conservative_triangle[0][1] > hill(R)

    cap51 = gallai_capacity(51)
    cap50 = gallai_capacity(50)
    assert cap51 == (582, 1, (24, 23, 3))
    assert cap50 == (579, 1, (24, 23, 2))

    forced_R2 = 665 - 26 * 2 + 1
    forced_R3 = 665 - 26 * 3 + 1
    assert (forced_R2, forced_R3) == (614, 588)
    assert forced_R2 > cap51[0] and forced_R3 > cap50[0]

    certificate = {
        "target": "bafkreicotrvsknilumgyiep3mvbl4aa6qaxsiuhh5q5oovm5mz2n74g5ri",
        "recursive_sweeps_including_final_no_change": sweeps,
        "frontier": frontier,
        "triangle_free": triangle,
        "triangle_free_with_complete_base_through_12": conservative_triangle,
        "barriers": {str(k): v for k, v in barriers.items()},
        "barriers_with_complete_base_through_12": {
            str(k): v for k, v in conservative_barriers.items()
        },
        "gallai": {
            "V51": cap51,
            "V50": cap50,
            "forced_R2": forced_R2,
            "forced_R3": forced_R3,
        },
    }
    digest = sha256(
        json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    print("target=" + certificate["target"])
    print("arithmetic=exact_python_int_and_Fraction")
    print("recursive_sweeps_including_final_no_change=" + str(sweeps))
    print(
        "frontier="
        + ",".join(f"{key}:{frontier[key]}" for key in sorted(frontier))
    )
    print("triangle_free=" + repr(triangle))
    print("barrier_survivors=" + repr(barriers))
    print("same_with_complete_graph_base_through_K12=True")
    print("triangle_free_with_complete_graph_base_through_K12="
          + repr(conservative_triangle))
    print("gallai_V51=" + repr(cap51) + ";forced=614")
    print("gallai_V50=" + repr(cap50) + ";forced=588")
    print("certificate_sha256=" + digest)
    print("STATUS=PASS")


if __name__ == "__main__":
    main()
