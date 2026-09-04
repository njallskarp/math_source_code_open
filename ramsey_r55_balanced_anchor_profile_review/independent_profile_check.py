#!/usr/bin/env python3
"""Independent exact audit of the balanced-anchor profile sieve.

This implementation imports no target code.  It enumerates side profiles as
nondecreasing 21-element degree multisets, rather than by the target's weak
composition recursion, and then joins the two sides by their exact deviations
and total weight.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path


SIDE = 21
DEGREES = tuple(range(18, 25))
DEVIATION = {degree: degree - 21 for degree in DEGREES}
WEIGHT = {18: 21, 19: 12, 20: 3, 21: 0, 22: 3, 23: 12, 24: 21}
ALLOWED_TOTAL_WEIGHTS = tuple(range(3, 40, 6))
TARGET_ESCAPE_DATA_DIGEST = (
    "bf0f2ef8a84453435e00778f04ff0892b16719ba244a7773d02ebddade99ca32"
)
TARGET_ESCAPE_HEADER = (
    "# M W L A_counts_degrees_18_to_24 B_counts_degrees_18_to_24\n"
)


def enumerate_side_profiles() -> tuple[int, tuple[tuple[int, int, tuple[int, ...]], ...]]:
    """Return all low-weight side profiles using degree multisets.

    Each nondecreasing 21-tuple over seven degrees is a unique multiset, hence
    a unique seven-entry count vector.  The total number visited must be
    C(21+7-1, 7-1).
    """
    retained: list[tuple[int, int, tuple[int, ...]]] = []
    visited = 0
    for multiset in itertools.combinations_with_replacement(DEGREES, SIDE):
        visited += 1
        counts_map = Counter(multiset)
        counts = tuple(counts_map[degree] for degree in DEGREES)
        deviation = sum(DEVIATION[degree] * count for degree, count in zip(DEGREES, counts))
        weight = sum(WEIGHT[degree] * count for degree, count in zip(DEGREES, counts))
        if weight <= 39:
            retained.append((deviation, weight, counts))
    assert visited == math.comb(SIDE + len(DEGREES) - 1, len(DEGREES) - 1)
    assert len({counts for _, _, counts in retained}) == len(retained)
    retained.sort(key=lambda item: item[2])
    return visited, tuple(retained)


def join_split_profiles(
    sides: tuple[tuple[int, int, tuple[int, ...]], ...],
) -> dict[int, tuple[tuple[int, tuple[int, ...], tuple[int, ...]], ...]]:
    """Join labeled A/B profiles by the exact deviations and allowed weights."""
    index: dict[tuple[int, int], list[tuple[int, ...]]] = defaultdict(list)
    for deviation, weight, counts in sides:
        index[(deviation, weight)].append(counts)

    result: dict[int, tuple[tuple[int, tuple[int, ...], tuple[int, ...]], ...]] = {}
    for cross_total in range(214, 221):
        joined: list[tuple[int, tuple[int, ...], tuple[int, ...]]] = []
        for total_weight in ALLOWED_TOTAL_WEIGHTS:
            for first_weight in range(total_weight + 1):
                second_weight = total_weight - first_weight
                first_profiles = index.get((cross_total - 220, first_weight), ())
                second_profiles = index.get((cross_total - 221, second_weight), ())
                for first_counts in first_profiles:
                    for second_counts in second_profiles:
                        joined.append((total_weight, first_counts, second_counts))
        joined.sort(key=lambda item: (item[1], item[2]))
        result[cross_total] = tuple(joined)
    return result


def profile_lower_bound(
    weight: int, first_counts: tuple[int, ...], second_counts: tuple[int, ...]
) -> int:
    degree_21_vertices = first_counts[3] + second_counts[3] + 1
    excess_units = (43 - weight) // 2
    return degree_21_vertices - excess_units


def canonical_escape_line(
    cross_total: int,
    weight: int,
    lower_bound: int,
    first_counts: tuple[int, ...],
    second_counts: tuple[int, ...],
) -> str:
    first = ",".join(map(str, first_counts))
    second = ",".join(map(str, second_counts))
    return f"{cross_total} {weight} {lower_bound} {first} {second}\n"


def analyze_profiles(
    split_profiles: dict[int, tuple[tuple[int, tuple[int, ...], tuple[int, ...]], ...]]
) -> dict[str, object]:
    profile_counts: list[int] = []
    connected_counts: list[int] = []
    diameter_eight_counts: list[int] = []
    diameter_five_counts: list[int] = []
    escape_counts: list[int] = []
    escape_histograms: list[dict[int, int]] = []
    escape_lines: list[str] = []

    for cross_total in range(214, 221):
        profiles = split_profiles[cross_total]
        lower_bounds = [profile_lower_bound(*profile) for profile in profiles]
        profile_counts.append(len(profiles))
        connected_counts.append(sum(lower_bound >= 27 for lower_bound in lower_bounds))
        diameter_eight_counts.append(sum(lower_bound >= 29 for lower_bound in lower_bounds))
        diameter_five_counts.append(sum(lower_bound >= 32 for lower_bound in lower_bounds))

        histogram: Counter[int] = Counter()
        for profile, lower_bound in zip(profiles, lower_bounds, strict=True):
            if lower_bound >= 27:
                continue
            weight, first_counts, second_counts = profile
            histogram[lower_bound] += 1
            escape_lines.append(
                canonical_escape_line(
                    cross_total, weight, lower_bound, first_counts, second_counts
                )
            )
        escape_counts.append(sum(histogram.values()))
        escape_histograms.append(dict(sorted(histogram.items())))

    escape_data = "".join(escape_lines)
    return {
        "profile_counts": profile_counts,
        "connected_counts": connected_counts,
        "diameter_eight_counts": diameter_eight_counts,
        "diameter_five_counts": diameter_five_counts,
        "escape_counts": escape_counts,
        "escape_histograms": escape_histograms,
        "escape_data": escape_data,
        "escape_data_sha256": hashlib.sha256(escape_data.encode("ascii")).hexdigest(),
    }


def clique_number(adjacency: tuple[tuple[bool, ...], ...]) -> int:
    """Return the exact clique number by a bitset branch-and-bound search."""
    neighbor_masks = []
    for row in adjacency:
        mask = 0
        for vertex, adjacent in enumerate(row):
            if adjacent:
                mask |= 1 << vertex
        neighbor_masks.append(mask)

    best = 0

    def expand(candidates: int, size: int) -> None:
        nonlocal best
        if size + candidates.bit_count() <= best:
            return
        while candidates:
            vertex_bit = candidates & -candidates
            vertex = vertex_bit.bit_length() - 1
            expand(candidates & neighbor_masks[vertex], size + 1)
            candidates ^= vertex_bit
            if size + candidates.bit_count() <= best:
                break
        if size > best:
            best = size

    expand((1 << len(adjacency)) - 1, 0)
    return best


def component_sizes(adjacency: tuple[tuple[bool, ...], ...]) -> tuple[int, ...]:
    unseen = set(range(len(adjacency)))
    sizes: list[int] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        size = 0
        while queue:
            vertex = queue.popleft()
            size += 1
            neighbors = {other for other in unseen if adjacency[vertex][other]}
            unseen.difference_update(neighbors)
            queue.extend(sorted(neighbors))
        sizes.append(size)
    return tuple(sorted(sizes))


def boundary_witness() -> dict[str, object]:
    """Check the abstract d=26 boundary using Cay(Z_13,{+/-1,+/-5})."""
    steps = {1, 5, 8, 12}
    h = tuple(
        tuple(u != v and (v - u) % 13 in steps for v in range(13))
        for u in range(13)
    )
    h_complement = tuple(
        tuple(u != v and not h[u][v] for v in range(13)) for u in range(13)
    )

    red = tuple(
        tuple(
            u != v
            and (
                (u // 13 != v // 13)
                or h[u % 13][v % 13]
            )
            for v in range(26)
        )
        for u in range(26)
    )
    blue = tuple(
        tuple(u != v and not red[u][v] for v in range(26)) for u in range(26)
    )

    return {
        "h_degree_set": sorted({sum(row) for row in h}),
        "h_clique": clique_number(h),
        "h_independence": clique_number(h_complement),
        "red_degree_set": sorted({sum(row) for row in red}),
        "blue_degree_set": sorted({sum(row) for row in blue}),
        "red_clique": clique_number(red),
        "blue_clique": clique_number(blue),
        "red_components": list(component_sizes(red)),
        "blue_components": list(component_sizes(blue)),
    }


def compare_target_certificate(path: Path, escape_data: str) -> None:
    actual = path.read_text(encoding="ascii")
    expected = TARGET_ESCAPE_HEADER + escape_data
    if actual != expected:
        raise AssertionError(f"target certificate mismatch: {path}")


def compute_audit(target_escape_file: Path | None = None) -> dict[str, object]:
    visited, sides = enumerate_side_profiles()
    split_profiles = join_split_profiles(sides)
    profile_analysis = analyze_profiles(split_profiles)

    expected = {
        "profile_counts": [1, 5, 17, 40, 69, 95, 122],
        "connected_counts": [1, 5, 16, 37, 63, 85, 107],
        "diameter_eight_counts": [0, 2, 11, 30, 52, 70, 88],
        "diameter_five_counts": [0, 0, 5, 16, 28, 37, 49],
        "escape_counts": [0, 0, 1, 3, 6, 10, 15],
        "escape_histograms": [
            {},
            {},
            {26: 1},
            {25: 1, 26: 2},
            {24: 1, 25: 2, 26: 3},
            {23: 1, 24: 2, 25: 3, 26: 4},
            {22: 1, 23: 2, 24: 3, 25: 4, 26: 5},
        ],
    }
    for key, value in expected.items():
        if profile_analysis[key] != value:
            raise AssertionError((key, profile_analysis[key], value))
    if profile_analysis["escape_data_sha256"] != TARGET_ESCAPE_DATA_DIGEST:
        raise AssertionError(profile_analysis["escape_data_sha256"])

    # Closed-neighborhood packing along a geodesic: positions spaced by three
    # have disjoint closed neighborhoods, each of size at least d-21.
    diameter_eight_threshold = next(d for d in range(1, 44) if 4 * (d - 21) > d)
    diameter_five_threshold = next(d for d in range(1, 44) if 3 * (d - 21) > d)
    if (diameter_eight_threshold, diameter_five_threshold) != (29, 32):
        raise AssertionError((diameter_eight_threshold, diameter_five_threshold))

    witness = boundary_witness()
    expected_witness = {
        "h_degree_set": [4],
        "h_clique": 2,
        "h_independence": 4,
        "red_degree_set": [17],
        "blue_degree_set": [8],
        "red_clique": 4,
        "blue_clique": 4,
        "red_components": [26],
        "blue_components": [13, 13],
    }
    if witness != expected_witness:
        raise AssertionError((witness, expected_witness))

    if target_escape_file is not None:
        compare_target_certificate(target_escape_file, profile_analysis["escape_data"])

    compact = {
        "visited_degree_multisets": visited,
        "retained_low_weight_sides": len(sides),
        **{key: profile_analysis[key] for key in expected},
        "escape_data_sha256": profile_analysis["escape_data_sha256"],
        "diameter_thresholds": [diameter_eight_threshold, diameter_five_threshold],
        "boundary_witness": witness,
        "target_certificate_match": target_escape_file is not None,
    }
    audit_digest = hashlib.sha256(
        json.dumps(compact, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    compact["audit_sha256"] = audit_digest
    return compact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--compare-target",
        type=Path,
        help="optionally compare every generated escape line with the target certificate",
    )
    args = parser.parse_args()
    result = compute_audit(args.compare_target)

    print(f"degree_multisets={result['visited_degree_multisets']}")
    print(f"retained_low_weight_sides={result['retained_low_weight_sides']}")
    print("profile_counts=" + ",".join(map(str, result["profile_counts"])))
    print("connected_counts=" + ",".join(map(str, result["connected_counts"])))
    print("diameter_le_8_counts=" + ",".join(map(str, result["diameter_eight_counts"])))
    print("diameter_le_5_counts=" + ",".join(map(str, result["diameter_five_counts"])))
    print("escape_counts=" + ",".join(map(str, result["escape_counts"])))
    print("escape_data_sha256=" + str(result["escape_data_sha256"]))
    print("diameter_thresholds=29,32")
    witness = result["boundary_witness"]
    print(
        "d26_boundary="
        f"red_clique={witness['red_clique']} blue_clique={witness['blue_clique']} "
        f"blue_components={','.join(map(str, witness['blue_components']))}"
    )
    print("target_certificate_match=" + str(result["target_certificate_match"]).lower())
    print("audit_sha256=" + str(result["audit_sha256"]))


if __name__ == "__main__":
    main()
