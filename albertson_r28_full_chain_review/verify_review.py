#!/usr/bin/env python3
"""Clean-room exact audit of the height-2711 Albertson r=28 proof attempt.

The two finite calculations use representations different from r28.py:

* an additive marked-part dynamic program for the disconnected-complement
  join decomposition; and
* a forward state graph for Gallai block multisets, rather than recursive
  integer partitions.

Only Python integers and deterministic finite state exploration are used.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256


R = 28
N = 55
LOW_DEGREE = 27
Z28 = 7098


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def ky_floor(r: int, n: int) -> int:
    """Kostochka--Yancey lower edge bound, rounded to an integer."""
    if r <= 1:
        return 0
    if r == 2:
        return 1
    return ceil_div((r + 1) * (r - 2) * n - r * (r - 3), 2 * (r - 1))


def topological_floor(r: int, n: int) -> int:
    """Barat--Toth/Cranston Lemma E for a critical graph with no TK_r."""
    return ceil_div(n * (r - 1) + 2 * (r - 3), 2)


# Exact output of the height-2711 recursive-sampling calculation.  Its source
# was replayed separately; here we independently audit the structural join
# step against every one of these ceilings.
OPEN_ROWS = {
    33: (471, 494),
    34: (484, 509),
    50: (700, 712),
    51: (714, 724),
    52: (727, 735),
    53: (741, 746),
    54: (754, 757),
    55: (768, 769),
}


def join_minimum(n: int) -> tuple[int, tuple[tuple[int, int, bool], ...]]:
    """Minimum necessary edge count over every admissible Gallai join.

    A component of the complement contributes a critical part (r_i,n_i),
    either (1,1) or r_i>=3 and n_i>=2r_i-1.  At least one part with r_i>=4
    has no TK_(r_i) and is marked; it receives the topological edge floor.

    Twice the total edge lower bound is additive after extracting n^2:

      2e >= n^2 + sum_i (2 floor_i - n_i^2).

    The forward DP deliberately permits ordered decompositions.  This adds
    duplicates but cannot omit a multiset.
    """
    types = [(1, 1)]
    for chromatic in range(3, R + 1):
        types.extend((chromatic, order) for order in range(2 * chromatic - 1, n + 1))

    # state = (chromatic sum, order sum, marked?, number of parts capped at 2)
    states: dict[
        tuple[int, int, bool, int],
        tuple[int, tuple[tuple[int, int, bool], ...]],
    ] = {(0, 0, False, 0): (0, ())}

    for rsum in range(R + 1):
        for nsum in range(n + 1):
            for marked in (False, True):
                for part_count in range(3):
                    key = (rsum, nsum, marked, part_count)
                    if key not in states:
                        continue
                    cost, witness = states[key]
                    for ri, ni in types:
                        if rsum + ri > R or nsum + ni > n:
                            continue
                        base = 2 * ky_floor(ri, ni) - ni * ni
                        next_count = min(2, part_count + 1)
                        choices = [(marked, 0, False)]
                        if not marked and ri >= 4:
                            extra = 2 * (max(ky_floor(ri, ni), topological_floor(ri, ni))
                                         - ky_floor(ri, ni))
                            choices.append((True, extra, True))
                        for next_marked, extra, is_marked in choices:
                            new_key = (rsum + ri, nsum + ni, next_marked, next_count)
                            candidate = (cost + base + extra, witness + ((ri, ni, is_marked),))
                            old = states.get(new_key)
                            if old is None or candidate < old:
                                states[new_key] = candidate

    doubled_additive, witness = states[(R, n, True, 2)]
    assert (n * n + doubled_additive) % 2 == 0
    return (n * n + doubled_additive) // 2, witness


def join_witness_text(witness: tuple[tuple[int, int, bool], ...]) -> str:
    counts = Counter(witness)
    fields = []
    for (ri, ni, marked), count in sorted(counts.items()):
        item = f"({ri},{ni})" + ("*" if marked else "")
        fields.append(item + (f"^{count}" if count > 1 else ""))
    return "+".join(fields)


K12_BASE = {
    5: 1,
    6: 3,
    7: 9,
    8: 18,
    9: 36,
    10: 60,
    11: 100,
    12: 150,
}
CCCG_BASE = {**K12_BASE, 13: 225, 14: 315}


def complete_crossing_bounds(base: dict[int, int], maximum: int) -> dict[int, int]:
    """Standard induced-subgraph lower recursion for complete graphs."""
    values = {q: 0 for q in range(5)}
    values.update(base)
    for q in range(5, maximum + 1):
        if q not in values:
            values[q] = ceil_div(q * values[q - 1], q - 4)
    return values


def forward_block_states(
    maximum_vertices: int,
    complete_bounds: dict[int, int],
) -> list[dict[int, tuple[int, tuple[str, ...]]]]:
    """All relaxed Gallai-block states by used increment and edge count.

    A clique K_(u+1) uses increment u and contributes C(u+1,2) edges.  A
    non-complete odd cycle uses even increment u>=4 and contributes u+1.
    States retain the least sum of complete-graph crossing lower bounds.
    Blocks are appended in arbitrary order, unlike the source partition
    recursion.  Duplicate orderings are harmless.
    """
    states: list[dict[int, tuple[int, tuple[str, ...]]]] = [
        {} for _ in range(maximum_vertices)
    ]
    states[0][0] = (0, ())
    block_types = []
    for increment in range(1, maximum_vertices):
        order = increment + 1
        block_types.append((increment, increment * order // 2,
                            complete_bounds[order] if order >= 15 else 0,
                            f"K{order}"))
        if order >= 5 and order % 2 == 1:
            block_types.append((increment, order, 0, f"C{order}"))

    for used in range(maximum_vertices):
        for edges, (cost, witness) in list(states[used].items()):
            for increment, new_edges, new_cost, name in block_types:
                if used + increment >= maximum_vertices:
                    continue
                candidate = (cost + new_cost, witness + (name,))
                target = states[used + increment]
                old = target.get(edges + new_edges)
                if old is None or candidate < old:
                    target[edges + new_edges] = candidate
    return states


def split_minimum(
    low_vertices: int,
    edge_floor: int,
    states: list[dict[int, tuple[int, tuple[str, ...]]]],
) -> tuple[int, int, int, tuple[str, ...]]:
    candidates = []
    for used in range(low_vertices):
        for edges, (cost, witness) in states[used].items():
            if edges >= edge_floor:
                candidates.append((cost, edges, used, witness))
    return min(candidates)


def tight_high_edge_minimum(extra_high: int) -> int:
    """Enumerate locations of high vertices outside the two singletons.

    In the tight local orbit, a high C-vertex contributes two forced edges to
    the singleton pair, a high triangle vertex contributes one, s contributes
    none, and every simultaneous s--triangle pair contributes one.
    """
    values = []
    for sigma in (0, 1):
        for tau in range(4):
            in_component = extra_high - sigma - tau
            if in_component < 0:
                continue
            values.append(1 + 2 * in_component + tau + sigma * tau)
    return min(values)


SOURCE_SPLITS = {
    (768, 2): (664, 10270),
    (768, 3): (637, 9448),
    (768, 4): (612, 8721),
    (769, 2): (663, 10270),
    (769, 3): (636, 9448),
    (769, 4): (609, 8721),
    (769, 5): (582, 7856),
    (769, 6): (560, 7354),
}


def main() -> None:
    lines = ["PASS independent Albertson r=28 full-chain audit"]

    # Replace r28.py's floating-point order-band comparisons by exact integer
    # arithmetic.  The same open-order set must result.
    candidate_orders = range(R + 5, 79)
    exact_open = [
        n for n in candidate_orders
        if not (1228 * R <= 1000 * n <= 1768 * R)
    ]
    assert exact_open == [33, 34, *range(50, 79)]
    lines.append("exact_Cranston_dispatch=33,34,50..78")

    # The source replay says recursive sampling closes 56..78 and leaves the
    # eight rows below.  Check all lower endpoints directly and independently
    # eliminate every disconnected-complement order through 54.
    for n, (lower, upper) in OPEN_ROWS.items():
        assert lower == max(ky_floor(R, n), topological_floor(R, n))
        if n <= 54:
            necessary, witness = join_minimum(n)
            assert necessary > upper
            lines.append(
                f"join n={n} ceiling={upper} minimum={necessary} "
                f"margin={necessary-upper} witness={join_witness_text(witness)}"
            )
    lines.append("frontier_after_join=(55,768),(55,769)")

    # Reconstruct the exact degree-identity floors in Part B.
    assert tight_high_edge_minimum(2) == 3
    assert tight_high_edge_minimum(4) == 6
    lines.append("tight_eGR=row768_R4:3,row769_R6:6")

    tables = {}
    for label, base in (("CCCG", CCCG_BASE), ("K12", K12_BASE)):
        complete = complete_crossing_bounds(base, 53)
        states = forward_block_states(53, complete)
        values = []
        for (m, high_vertices), (expected_floor, expected_cccg) in SOURCE_SPLITS.items():
            excess = 2 * m - N * LOW_DEGREE
            tight = high_vertices - 2 == excess - 49
            e_high = tight_high_edge_minimum(high_vertices - 2) if tight else 1
            edge_floor = m - (LOW_DEGREE * high_vertices + excess) + e_high
            assert edge_floor == expected_floor
            low_vertices = N - high_vertices
            result = split_minimum(low_vertices, edge_floor, states)
            if label == "CCCG":
                assert result[0] == expected_cccg
            values.append(result[0])
        tables[label] = tuple(values)
        assert min(values) > Z28

    lines.append("split_CCCG=" + ",".join(map(str, tables["CCCG"])))
    lines.append("split_K12_only=" + ",".join(map(str, tables["K12"])))
    lines.append(f"minimum_K12_margin={min(tables['K12'])-Z28}")
    lines.append("all_rows_eliminated_without_clique_caps=YES")
    lines.append("scope=conditional_on_cited_theorems_and_two_recent_preprints")
    lines.append("minor_correction=r28.py_float_order_band_has_exact_integer_replacement")
    lines.append("verdict=ACCEPT_CONDITIONAL")

    digest = sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    lines.append(f"certificate_sha256={digest}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
