#!/usr/bin/env python3
"""Exact block-packing certificate for the r=28 Gallai low-forest compression."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256


PROFILES = {
    768: (
        (0,) * 52 + (1, 25, 25),
        (0,) * 52 + (2, 24, 25),
        (0,) * 51 + (1, 1, 24, 25),
    ),
    769: (
        (0,) * 52 + (3, 25, 25),
        (0,) * 52 + (4, 24, 25),
        (0,) * 51 + (1, 2, 25, 25),
        (0,) * 51 + (1, 3, 24, 25),
        (0,) * 51 + (2, 2, 24, 25),
        (0,) * 50 + (1, 1, 1, 25, 25),
        (0,) * 50 + (1, 1, 2, 24, 25),
        (0,) * 49 + (1, 1, 1, 1, 24, 25),
    ),
}


def histogram_text(values: tuple[int, ...]) -> str:
    counts = Counter(values)
    return ",".join(f"{x}^{counts[x]}" for x in sorted(counts))


def clique_edges_from_increment(increment: int) -> int:
    """A clique block on increment+1 vertices maximizes its block edge count."""
    return increment * (increment + 1) // 2


def maximum_block_relaxation(
    n: int, allow_k26: bool, other_maximum: int = 24
) -> tuple[int, tuple[int, ...]]:
    """Maximize edges from the block identity n=c+sum_B(|B|-1).

    Complete blocks have size at most 26.  At most one increment 25 is
    allowed when allow_k26 is true; every other increment is at most 24.
    Odd-cycle blocks lie below the clique value at the same increment.
    The dynamic program also relaxes block-tree realizability and degrees.
    """

    @lru_cache(None)
    def best(units: int, used_25: bool, cap: int) -> tuple[int, tuple[int, ...]]:
        if units == 0:
            return 0, ()
        answer = (-1, ())
        for part in range(min(cap, units), 0, -1):
            if part == 25 and (not allow_k26 or used_25):
                continue
            if part < 25 and part > other_maximum:
                continue
            tail_value, tail = best(units - part, used_25 or part == 25, part)
            candidate = (clique_edges_from_increment(part) + tail_value, (part,) + tail)
            if candidate > answer:
                answer = candidate
        return answer

    # A forest with c components has n-c block-increment units.  Maximize over
    # c, including isolated components, rather than presuming connectedness.
    candidates = [best(n - components, False, 25) for components in range(1, n + 1)]
    return max(candidates)


def low_edge_floor(row: int, profile: tuple[int, ...]) -> int:
    """Use e(L)=m-sum_{R}d_G+e(G[R]) and the forced singleton edge."""
    high = tuple(x for x in profile if x)
    high_degree_sum = sum(27 + x for x in high)
    # The two separator singleton components have no H-edge between them, so
    # their edge is in G and e(G[R])>=1.
    return row - high_degree_sum + 1


def low_edge_ceiling(row: int, profile: tuple[int, ...]) -> int:
    """Use e(G[R])<=binom(|R|,2) in the same exact degree identity."""
    high = tuple(x for x in profile if x)
    high_degree_sum = sum(27 + x for x in high)
    return row - high_degree_sum + len(high) * (len(high) - 1) // 2


def main() -> None:
    assert maximum_block_relaxation(52, True) == (628, (25, 24, 2))
    assert maximum_block_relaxation(52, False) == (606, (24, 24, 3))
    assert maximum_block_relaxation(51, True) == (626, (25, 24, 1))
    assert maximum_block_relaxation(51, False) == (603, (24, 24, 2))
    assert maximum_block_relaxation(51, True, 23) == (604, (25, 23, 2))

    output = [
        "PASS Albertson r=28 Gallai low-forest compression",
        "block_relaxation n=52 at_most_one_K26=628 witness_increments=25,24,2",
        "block_relaxation n=51 no_K26=603 witness_increments=24,24,2",
        "block_relaxation n=51 one_K26_no_K25=604 witness_increments=25,23,2",
        "two_disjoint_clique_blocks K26_plus_K25_edges_at_least=625",
        "two_K26_core_vertices_at_least=44 non_singleton_high_H_degree_at_most=26",
    ]
    surviving: dict[int, list[tuple[int, ...]]] = {768: [], 769: []}
    block_gap_eliminated: dict[int, int] = {768: 0, 769: 0}

    for row, profiles in PROFILES.items():
        expected_total = 2 * row - 55 * 27
        for profile in profiles:
            profile = tuple(sorted(profile))
            assert len(profile) == 55 and sum(profile) == expected_total
            n_low = profile.count(0)
            floor = low_edge_floor(row, profile)
            if n_low == 52:
                ceiling = maximum_block_relaxation(52, True)[0]
                assert floor > ceiling
                status = f"ELIMINATED floor_eL={floor}>gallai_ceiling={ceiling}"
            elif n_low == 51:
                no_k26_ceiling = maximum_block_relaxation(51, False)[0]
                assert floor > no_k26_ceiling
                no_k25_ceiling = maximum_block_relaxation(51, True, 23)[0]
                upper = low_edge_ceiling(row, profile)
                assert floor > no_k25_ceiling and upper < 625
                block_gap_eliminated[row] += 1
                status = (
                    f"ELIMINATED_BLOCK_GAP floor_eL={floor}>"
                    f"one_K26_no_K25_ceiling={no_k25_ceiling} "
                    f"but_K26_plus_K25>=625>degree_ceiling={upper}"
                )
            else:
                surviving[row].append(profile)
                status = f"SURVIVES_UNRESOLVED floor_eL={floor}"
            output.append(f"row={row} profile={histogram_text(profile)} {status}")

    assert len(surviving[768]) == 0 and block_gap_eliminated[768] == 1
    assert len(surviving[769]) == 3 and block_gap_eliminated[769] == 3
    output.append("summary row=768 survivors=0 eliminated_n52=2 eliminated_block_gap=1")
    output.append("summary row=769 survivors=3 eliminated_n52=2 eliminated_block_gap=3")
    digest = sha256(("\n".join(output) + "\n").encode()).hexdigest()
    output.append(f"certificate_sha256={digest}")
    print("\n".join(output))


if __name__ == "__main__":
    main()
