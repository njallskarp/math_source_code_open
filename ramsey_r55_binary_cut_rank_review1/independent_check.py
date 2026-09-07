#!/usr/bin/env python3
"""Independent exact checks for the Ramsey43 binary cut-rank lemma.

This does not import the researcher's package.  It checks the finite arithmetic
and identities used by the proof, using a rank-count recurrence rather than the
researcher's full-rank-factorization formula.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product


EXPECTED_PROFILE = (1, 2, 2, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def gf2_rank(rows: list[int]) -> int:
    """Definition-level elimination on integer bit rows."""
    pivots: dict[int, int] = {}
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


def matrix_count_recurrence(m: int, n: int) -> list[int]:
    """Counts binary m-by-n matrices by rank, adding one row at a time.

    If an (m-1)-row matrix has rank k, 2^k appended rows preserve rank k.
    If it has rank k-1, exactly 2^n-2^(k-1) appended rows raise the rank.
    """
    old = [1]
    for _ in range(m):
        new = [0] * (min(len(old), n + 1) + 1)
        for rank, count in enumerate(old):
            new[rank] += count * (1 << rank)
            if rank < n:
                new[rank + 1] += count * ((1 << n) - (1 << rank))
        old = new
    return old[: min(m, n) + 1]


def exhaustive_small_matrix_counts() -> tuple[int, dict[str, list[int]]]:
    total = 0
    summaries: dict[str, list[int]] = {}
    for m in range(1, 5):
        for n in range(1, 5):
            observed = Counter()
            mask = (1 << n) - 1
            for word in range(1 << (m * n)):
                observed[gf2_rank([(word >> (i * n)) & mask for i in range(m)])] += 1
                total += 1
            expected = matrix_count_recurrence(m, n)
            require([observed[k] for k in range(len(expected))] == expected,
                    f"rank-count mismatch for {m}x{n}")
            summaries[f"{m}x{n}"] = expected
    return total, summaries


def has_mono_clique(n: int, word: int, size: int, color: int) -> bool:
    pairs = list(combinations(range(n), 2))
    position = {edge: i for i, edge in enumerate(pairs)}
    return any(
        all(((word >> position[edge]) & 1) == color for edge in combinations(vertices, 2))
        for vertices in combinations(range(n), size)
    )


def check_r33() -> int:
    """Exhaust all labelled 2-colourings of K6."""
    checked = 0
    for word in range(1 << 15):
        require(has_mono_clique(6, word, 3, 0) or has_mono_clique(6, word, 3, 1),
                "counterexample to R(3,3)<=6")
        checked += 1
    return checked


def check_signature_bounds() -> dict[str, int]:
    # A pair signature contributes 2xy internally plus one when x != y.
    for x, y in product((0, 1), repeat=2):
        require(x + y == 2 * x * y + int(x != y), "pair identity")

    # The mixed triple is red on 01 and 02, blue on 12.
    for x0, x1, x2 in product((0, 1), repeat=3):
        left = x0 * x1 + x0 * x2 + (1 - x1) * (1 - x2)
        right = int(x0 == x1 == x2) + x0
        require(left == right, "mixed-triple identity")

    pair_candidates = [d0 + d1 - 2 - 2 * t
                       for d0 in range(18, 25)
                       for d1 in range(18, 25)
                       for t in range(14)]
    require(min(pair_candidates) == 8, "pair distinguisher minimum")

    # The degree-sum inequality is 54 <= 6 + 3t + 2D.
    triangle_minimum = min((54 - 6 - 3 * t + 1) // 2 for t in range(5))
    require(triangle_minimum == 18, "monochromatic-triple minimum")

    # For the mixed triple, D >= d_red(0)-1.
    mixed_minimum = min(d - 1 for d in range(18, 25))
    require(mixed_minimum == 17, "mixed-triple minimum")
    return {
        "pair_signature_words": 4,
        "mixed_triple_signature_words": 8,
        "pair_distinguisher_minimum": min(pair_candidates),
        "monochromatic_triple_distinguisher_minimum": triangle_minimum,
        "mixed_triple_distinguisher_minimum": mixed_minimum,
    }


def row_caps(a: int, rank: int) -> list[int]:
    slots = 1 << rank
    if a <= 9:
        return [0] + [1] * (slots - 1)
    if a <= 18:
        return [0] + [2] * (slots - 1)
    if a == 19:
        return [2] * slots
    return [4] + [5] * (slots - 1)


def attainable_totals(caps: list[int]) -> set[int]:
    totals = {0}
    for cap in caps:
        totals = {subtotal + value for subtotal in totals for value in range(cap + 1)}
    return totals


def check_profile() -> tuple[list[int], int]:
    profile = []
    checked_cells = 0
    for a in range(1, 22):
        first = None
        for rank in range(6):
            caps = row_caps(a, rank)
            reachable = attainable_totals(caps)
            require(reachable == set(range(sum(caps) + 1)), "occupancy reachability gap")
            checked_cells += 1
            if first is None and a in reachable:
                first = rank
        require(first is not None, "profile search did not terminate")
        profile.append(first)
    require(tuple(profile) == EXPECTED_PROFILE, "cut-rank profile mismatch")

    # Boundary arithmetic used only for the a=20,21 row-class argument.
    for a in (20, 21):
        b = 43 - a
        require(b - 4 >= 18 and b >= 14, "large-side Ramsey threshold")
        require(sum(row_caps(a, 2)) == 19 < a, "rank-two boundary capacity")
    return profile, checked_cells


def check_centroid() -> tuple[int, int, int]:
    triples = [(x, y, z) for x, y, z in product(range(1, 22), repeat=3)
               if x + y + z == 43]
    require(triples, "no centroid triples")
    maxima = [max(t) for t in triples]
    require(min(maxima) == 15 and max(maxima) == 21, "centroid cut range")
    return len(triples), min(maxima), max(maxima)


def check_f27_arithmetic() -> dict[str, int]:
    vertices = set(range(43))
    side_a = set(range(7, 27))
    side_b = vertices - side_a
    pins: set[tuple[int, int]] = set()
    for start in (2, 7, 12, 17, 22):
        pins.update(combinations(range(start, start + 5), 2))
    pins.add((0, 1))
    pins.update((u, v) for u in (0, 1) for v in range(2, 7))
    cross = {tuple(sorted((u, v))) for u in side_a for v in side_b}
    internal_a = set(combinations(sorted(side_a), 2))
    internal_b = set(combinations(sorted(side_b), 2))
    require(len(pins) == 61 and not (pins & cross), "F27 pin count or cross freedom")
    free_a = len(internal_a - pins)
    free_b = len(internal_b - pins)
    require((len(cross), free_a, free_b, free_a + free_b) == (460, 150, 232, 382),
            "F27 physical-bit count")

    counts = matrix_count_recurrence(20, 23)[:3]
    expected = [1, 8_796_083_585_025, 12_895_167_237_418_895_565_739_350]
    require(counts == expected, "20x23 rank count")
    total = sum(counts)
    require(total == 12_895_167_237_427_691_649_324_376, "rank<=2 total")
    return {
        "pins": len(pins),
        "cross_pairs": len(cross),
        "internal_free_pairs": free_a + free_b,
        "rank_0_matrices": counts[0],
        "rank_1_matrices": counts[1],
        "rank_2_matrices": counts[2],
        "rank_at_most_2_matrices": total,
        "factor_bits": 2 * 20 + 2 * 23,
    }


def main() -> None:
    matrix_cases, histograms = exhaustive_small_matrix_counts()
    profile, capacity_cells = check_profile()
    centroid_count, centroid_min, centroid_max = check_centroid()
    output = {
        "status": "INDEPENDENT_CUT_RANK_CHECKS_PASSED",
        "exactness": "Python integers and exhaustive finite loops; no third-party packages",
        "R33_labelled_K6_colorings": check_r33(),
        "signature_bounds": check_signature_bounds(),
        "profile": profile,
        "occupancy_capacity_cells": capacity_cells,
        "centroid_component_triples": centroid_count,
        "centroid_largest_component_range": [centroid_min, centroid_max],
        "small_binary_matrices": matrix_cases,
        "small_matrix_rank_histograms": histograms,
        "F27": check_f27_arithmetic(),
        "trust_boundary": (
            "Checks finite identities and arithmetic only; the universal theorem still depends "
            "on the written proof and imported R(4,5)=25."
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
