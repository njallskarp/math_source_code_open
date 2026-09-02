#!/usr/bin/env python3
"""Independent audit of the C(13,6,3) heavy-triple degree-profile gap.

The producer and objection enumerated canonical orbit signatures.  This
checker instead counts fixed colored mask-count arrays for every element of
the row-permutation group and applies Burnside's lemma.  It reads no producer
source, certificate, or orbit list.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations
import json
from math import comb


ROW_PERMUTATIONS = tuple(permutations(range(3)))
ROW_PAIRS = ((0, 1), (0, 2), (1, 2))


def weak_compositions(total: int, parts: int):
    """Yield all ordered weak compositions of total into parts parts."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first,) + tail


def permute_mask(mask: int, permutation: tuple[int, int, int]) -> int:
    """Reorder the three block-incidence coordinates of a mask."""
    return sum(((mask >> permutation[row]) & 1) << row for row in range(3))


def summarized_invariant_arrays(
    class_size: int,
    permutation: tuple[int, int, int],
) -> Counter[tuple[int, int, int, int]]:
    """Count invariant mask arrays by row totals and row-distinctness flags."""
    summaries: Counter[tuple[int, int, int, int]] = Counter()
    mask_image = tuple(permute_mask(mask, permutation) for mask in range(8))
    for counts in weak_compositions(class_size, 8):
        if any(counts[mask] != counts[mask_image[mask]] for mask in range(8)):
            continue

        row_totals = tuple(
            sum(counts[mask] for mask in range(8) if (mask >> row) & 1)
            for row in range(3)
        )
        if any(total > 3 for total in row_totals):
            continue

        distinctness = 0
        for pair_index, (left, right) in enumerate(ROW_PAIRS):
            if any(
                counts[mask] > 0
                and ((mask >> left) & 1) != ((mask >> right) & 1)
                for mask in range(8)
            ):
                distinctness |= 1 << pair_index
        summaries[(*row_totals, distinctness)] += 1
    return summaries


def fixed_colored_arrays(
    class_sizes: tuple[int, ...],
    permutation: tuple[int, int, int],
) -> int:
    """Count valid colored count-arrays fixed by one row permutation."""
    dynamic: Counter[tuple[int, int, int, int]] = Counter({(0, 0, 0, 0): 1})
    for class_size in class_sizes:
        local = summarized_invariant_arrays(class_size, permutation)
        updated: Counter[tuple[int, int, int, int]] = Counter()
        for (a0, a1, a2, adiff), multiplicity_a in dynamic.items():
            for (b0, b1, b2, bdiff), multiplicity_b in local.items():
                totals = (a0 + b0, a1 + b1, a2 + b2)
                if any(total > 3 for total in totals):
                    continue
                updated[(*totals, adiff | bdiff)] += multiplicity_a * multiplicity_b
        dynamic = updated
    return dynamic[(3, 3, 3, 0b111)]


def burnside_orbits(class_sizes: tuple[int, ...]) -> tuple[int, list[int]]:
    """Count unordered triples of distinct 3-sets modulo colored points."""
    assert sum(class_sizes) == 10
    fixed = [fixed_colored_arrays(class_sizes, p) for p in ROW_PERMUTATIONS]
    assert sum(fixed) % len(ROW_PERMUTATIONS) == 0
    return sum(fixed) // len(ROW_PERMUTATIONS), fixed


def degree_profile_audit() -> list[dict[str, object]]:
    """Derive every degree multiset from d_x>=9 and sum d_x=120."""
    excess_partitions = ((1, 1, 1), (2, 1), (3,))
    profiles: list[dict[str, object]] = []
    for partition in excess_partitions:
        degrees = sorted(
            [9 + excess for excess in partition] + [9] * (13 - len(partition)),
            reverse=True,
        )
        assert len(degrees) == 13 and sum(degrees) == 120
        block_pair_intersection_sum = sum(comb(degree, 2) for degree in degrees)
        heavy_triple_lower_bound = block_pair_intersection_sum - 2 * comb(20, 2)
        assert heavy_triple_lower_bound >= 115 > 114
        profiles.append(
            {
                "excess_partition": list(partition),
                "degrees": degrees,
                "block_pair_intersection_sum": block_pair_intersection_sum,
                "heavy_triple_pair_lower_bound": heavy_triple_lower_bound,
            }
        )
    return profiles


def main() -> None:
    # Class sizes are the numbers of outside points in each global degree
    # class, after fixing a heavy triple and three blocks through it.
    expected = {
        (3, 7): 177,
        (2, 8): 103,
        (1, 9): 44,
        (0, 10): 12,
        (1, 1, 8): 169,
    }
    orbit_data: dict[str, dict[str, object]] = {}
    for class_sizes, expected_count in expected.items():
        count, fixed = burnside_orbits(class_sizes)
        assert count == expected_count
        orbit_data["+".join(map(str, class_sizes))] = {
            "fixed_counts_by_row_permutation": fixed,
            "orbits": count,
        }

    profile_10_10_10 = sum(expected[sizes] for sizes in ((3, 7), (2, 8), (1, 9), (0, 10)))
    profile_11_10 = expected[(1, 1, 8)] + 2 * expected[(1, 9)] + expected[(0, 10)]
    profile_12 = expected[(1, 9)] + expected[(0, 10)]
    assert (profile_10_10_10, profile_11_10, profile_12) == (336, 269, 56)
    assert profile_10_10_10 + profile_11_10 + profile_12 == 661

    result = {
        "degree_profiles": degree_profile_audit(),
        "burnside_orbit_data": orbit_data,
        "profile_orbit_totals": [profile_10_10_10, profile_11_10, profile_12],
        "corrected_total": 661,
        "original_336_is_exhaustive": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("independent_audit=PASS")


if __name__ == "__main__":
    main()
