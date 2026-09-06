#!/usr/bin/env python3
"""Independent exact audit of Discovery Net h3535.

This checker imports no reviewed module.  It enumerates profiles by an
exceptional-weight recursion, subsets by a centre-out bounded recursion, and
cut violations by the number of missing internal edges.  It compares the
complete candidate set with the reviewed producer stream.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


N = 43
DEGREES = tuple(range(18, 25))
CAPS = (78, 85, 93, 100, 107, 115, 125)
WEIGHTS = (21, 12, 3, 0, 3, 12, 21)
EXCEPTIONAL = (0, 6, 1, 5, 2, 4)
SIDE_ORDER = (3, 0, 6, 1, 5, 2, 4)


def need(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def cut_bound(a: int) -> int:
    return 18 * a - 2 * ((3 * a * a) // 8)


def balanced_squares(total: int, bins: int) -> int:
    q, r = divmod(total, bins)
    return (bins - r) * q * q + r * (q + 1) * (q + 1)


def balanced_pairs(total: int, bins: int) -> int:
    q, r = divmod(total, bins)
    return bins * comb(q, 2) + r * q


def enumerate_profiles() -> tuple[tuple[int, ...], ...]:
    """Enumerate the complete W <= 39 envelope from positive-cost classes."""
    counts = [0] * 7
    answer: list[tuple[int, ...]] = []

    def visit(position: int, used_vertices: int, used_weight: int) -> None:
        if position == len(EXCEPTIONAL):
            counts[3] = N - used_vertices
            degree_sum = sum(d * n for d, n in zip(DEGREES, counts))
            if degree_sum % 2 == 0 and degree_sum <= 902:
                answer.append(tuple(counts))
            counts[3] = 0
            return
        index = EXCEPTIONAL[position]
        maximum = min(N - used_vertices, (39 - used_weight) // WEIGHTS[index])
        for multiplicity in range(maximum + 1):
            counts[index] = multiplicity
            visit(
                position + 1,
                used_vertices + multiplicity,
                used_weight + multiplicity * WEIGHTS[index],
            )
        counts[index] = 0

    visit(0, 0, 0)
    result = tuple(sorted(answer))
    need(len(result) == len(set(result)), "duplicate degree profiles")
    return result


def enumerate_sides(profile: tuple[int, ...]):
    """Yield every nonempty degree-class submultiset of size at most 21."""
    side = [0] * 7

    def visit(position: int, used: int):
        if position == len(SIDE_ORDER):
            if used:
                yield tuple(side)
            return
        index = SIDE_ORDER[position]
        for multiplicity in range(min(profile[index], 21 - used) + 1):
            side[index] = multiplicity
            yield from visit(position + 1, used + multiplicity)
        side[index] = 0

    yield from visit(0, 0)


@lru_cache(maxsize=None)
def largest_missing_weights(side: tuple[int, ...]) -> tuple[int, ...]:
    """Prefix sums of the h largest pair weights, via a pair-weight census."""
    multiplicities: Counter[int] = Counter()
    for i in range(7):
        for j in range(i, 7):
            number = side[i] * side[j] if i != j else comb(side[i], 2)
            multiplicities[(3 - i) + (3 - j)] += number
    prefix = [0]
    for weight in sorted(multiplicities, reverse=True):
        for _ in range(multiplicities[weight]):
            prefix.append(prefix[-1] + weight)
    need(len(prefix) == comb(sum(side), 2) + 1, "pair-weight census")
    return tuple(prefix)


def cap_deficit(profile: tuple[int, ...]) -> int:
    weight = sum(n * w for n, w in zip(profile, WEIGHTS))
    cap_total = sum(n * (CAPS[i] + CAPS[6 - i]) for i, n in enumerate(profile))
    mixed_total = (
        3 * comb(N, 3)
        - Fraction(3, 2)
        * sum(n * d * (42 - d) for n, d in zip(profile, DEGREES))
    )
    deficit = Fraction(cap_total) - mixed_total
    need(deficit == Fraction(43 - weight, 2), "cap-deficit identity")
    need(deficit.denominator == 1 and deficit >= 0, "integral nonnegative deficit")
    need((weight // 3) % 2 == 1, "handshake parity of W/3")
    need(weight <= 39, "sharp exceptional-weight envelope")
    need(
        sum(n * abs(d - 21) for n, d in zip(profile, DEGREES)) <= 13,
        "absolute degree deviation",
    )
    return int(deficit)


def h_value(index: int, total_edges: int) -> int:
    degree = DEGREES[index]
    return (
        21 * degree
        + comb(42 - degree, 2)
        - total_edges
        - CAPS[index]
        - CAPS[6 - index]
    )


def candidate_gap(
    profile: tuple[int, ...],
    side: tuple[int, ...],
    total_edges: int,
    deficit: int,
    missing: int,
) -> tuple[str, int]:
    a = sum(side)
    b = N - a
    degree_sum = sum(d * n for d, n in zip(DEGREES, side))
    internal_edges = comb(a, 2) - missing
    cut = degree_sum - 2 * internal_edges
    cap_sum = sum(n * c for n, c in zip(side, CAPS))

    internal_gap = (
        balanced_squares(2 * internal_edges, a)
        - a * internal_edges
        - cap_sum
    )
    if internal_gap > 0:
        return "internal", internal_gap

    crossing_gap = (
        3 * comb(a, 3)
        + 2 * balanced_pairs(cut, b)
        - (a + 80) * missing
        - cap_sum
    )
    if crossing_gap > 0:
        return "cross", crossing_gap

    side_weight = sum((3 - i) * n for i, n in enumerate(side))
    outside_negative = sum(
        min(0, 3 - i) * (profile[i] - side[i]) for i in range(7)
    )
    local_h = sum(n * h_value(i, total_edges) for i, n in enumerate(side))
    required = (
        (a - 1) * side_weight
        + a * outside_negative
        - local_h
        - deficit
    )
    weighted_gap = required - largest_missing_weights(side)[missing]
    return "weighted", weighted_gap


def reconstruct():
    profiles = enumerate_profiles()
    profile_counts: Counter[int] = Counter()
    route_counts: Counter[str] = Counter()
    by_slice: dict[int, Counter[str]] = {}
    by_size: dict[int, Counter[str]] = {}
    by_color: dict[int, Counter[str]] = {}
    minimum: dict[str, int] = {}
    minimum_witness: dict[str, tuple] = {}
    records: set[tuple] = set()
    placements = 0
    survivors = []

    for index, oriented in enumerate(profiles):
        red_edges = sum(d * n for d, n in zip(DEGREES, oriented)) // 2
        slice_index = red_edges - 231
        need(214 <= slice_index <= 220, "M-slice range")
        profile_counts[slice_index] += 1
        deficit = cap_deficit(oriented)
        for color in (0, 1):
            profile = oriented if color == 0 else oriented[::-1]
            total_edges = sum(d * n for d, n in zip(DEGREES, profile)) // 2
            for side in enumerate_sides(profile):
                placements += 1
                a = sum(side)
                degree_sum = sum(d * n for d, n in zip(DEGREES, side))
                # Parameterize by h, not q: e=C(a,2)-h and
                # q=D_A-a(a-1)+2h.
                for missing in range(comb(a, 2) + 1):
                    edge_count = comb(a, 2) - missing
                    cut = degree_sum - 2 * edge_count
                    if cut < 0 or cut >= cut_bound(a):
                        continue
                    route, gap = candidate_gap(
                        profile, side, total_edges, deficit, missing
                    )
                    record = (
                        index,
                        color,
                        *side,
                        cut,
                        route,
                        gap,
                    )
                    need(record not in records, "duplicate candidate record")
                    records.add(record)
                    if gap <= 0:
                        survivors.append(record)
                    route_counts[route] += 1
                    by_slice.setdefault(slice_index, Counter())[route] += 1
                    by_size.setdefault(a, Counter())[route] += 1
                    by_color.setdefault(color, Counter())[route] += 1
                    if route not in minimum or gap < minimum[route]:
                        minimum[route] = gap
                        minimum_witness[route] = record

    need(not survivors, f"unexcluded candidates: {survivors[:3]}")
    digest = sha256()
    for record in sorted(records):
        digest.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
    return {
        "profiles": profiles,
        "profile_counts_by_M": dict(sorted(profile_counts.items())),
        "oriented_side_placements": placements,
        "candidate_violations": len(records),
        "closed_by": dict(route_counts),
        "closed_by_M": {m: dict(v) for m, v in sorted(by_slice.items())},
        "closed_by_size": {a: dict(v) for a, v in sorted(by_size.items())},
        "closed_by_color": {c: dict(v) for c, v in sorted(by_color.items())},
        "minimum_positive_gaps": minimum,
        "minimum_gap_witness": minimum_witness,
        "independent_sorted_record_sha256": digest.hexdigest(),
        "records": records,
    }


def compare_target(source: Path, target_stream: Path, audit: dict) -> dict:
    certificate_bytes = (source / "certificate.json").read_bytes()
    certificate = json.loads(certificate_bytes)
    expected = json.loads((source / "EXPECTED.json").read_text())

    need(
        certificate["profiles"] == [list(profile) for profile in audit["profiles"]],
        "profile list differs",
    )
    scalar_fields = (
        "oriented_side_placements",
        "candidate_violations",
        "closed_by",
        "minimum_positive_gaps",
    )
    for field in scalar_fields:
        need(certificate[field] == audit[field], f"certificate field {field}")
    need(
        certificate["profile_counts_by_M"]
        == {str(k): v for k, v in audit["profile_counts_by_M"].items()},
        "profile counts by M",
    )
    need(
        certificate["closed_by_M"]
        == {str(k): v for k, v in audit["closed_by_M"].items()},
        "route counts by M",
    )
    need(
        certificate["q_by_size"] == [cut_bound(a) for a in range(1, 22)],
        "cut threshold table",
    )
    need(certificate["unexcluded_candidates"] == 0, "certificate survivor count")

    profile_index = audit["profiles"].index((0, 2, 5, 36, 0, 0, 0))
    for route, example in certificate["M216_examples"].items():
        record = (
            profile_index,
            0,
            *example["side"],
            example["q"],
            route,
            example["gap"],
        )
        need(record in audit["records"], f"M216 example {route}")

    target_digest = sha256()
    target_records = set()
    lines = 0
    with target_stream.open("rb") as handle:
        for raw in handle:
            target_digest.update(raw)
            value = json.loads(raw)
            need(isinstance(value, list) and len(value) == 12, "target stream record")
            record = tuple(value)
            need(record not in target_records, "duplicate target stream record")
            target_records.add(record)
            lines += 1
    need(
        target_digest.hexdigest() == certificate["candidate_stream_sha256"],
        "target stream identity",
    )
    missing = audit["records"] - target_records
    extra = target_records - audit["records"]
    need(not missing and not extra, f"candidate-set mismatch {len(missing)}/{len(extra)}")

    certificate_hash = sha256(certificate_bytes).hexdigest()
    need(certificate_hash == expected["certificate_sha256"], "certificate hash")
    for field in (
        "profiles",
        "oriented_side_placements",
        "candidate_violations",
        "closed_by",
    ):
        target_value = len(certificate["profiles"]) if field == "profiles" else certificate[field]
        need(expected[field] == target_value, f"expected field {field}")
    return {
        "certificate_sha256": certificate_hash,
        "target_stream_sha256": target_digest.hexdigest(),
        "complete_candidate_records_compared": lines,
    }


def small_graph_controls() -> dict:
    """Check the three inequalities directly on every labeled graph through n=6."""
    graphs = cuts = 0
    for n in range(1, 7):
        pairs = tuple(combinations(range(n), 2))
        full = (1 << n) - 1
        subset_data = [
            (
                mask,
                tuple(v for v in range(n) if mask >> v & 1),
                tuple(v for v in range(n) if not (mask >> v & 1)),
            )
            for mask in range(1, full)
        ]
        for graph_mask in range(1 << len(pairs)):
            adjacency = [0] * n
            for bit, (u, v) in enumerate(pairs):
                if graph_mask >> bit & 1:
                    adjacency[u] |= 1 << v
                    adjacency[v] |= 1 << u
            degrees = [row.bit_count() for row in adjacency]
            edge_total = sum(degrees) // 2
            red_triangles = []
            blue_triangles = []
            for v in range(n):
                red_neighbors = [u for u in range(n) if adjacency[v] >> u & 1]
                blue_mask = (full ^ adjacency[v]) & ~(1 << v)
                blue_neighbors = [u for u in range(n) if blue_mask >> u & 1]
                red_triangles.append(
                    sum(adjacency[u] >> w & 1 for u, w in combinations(red_neighbors, 2))
                )
                blue_triangles.append(
                    sum(not (adjacency[u] >> w & 1) for u, w in combinations(blue_neighbors, 2))
                )
                identity = (
                    comb(n - 1 - degrees[v], 2)
                    - edge_total
                    + sum(degrees[u] for u in red_neighbors)
                )
                need(
                    red_triangles[v] + blue_triangles[v] == identity,
                    "small-graph local identity",
                )
            gamma = n // 2
            weights = [gamma - degree for degree in degrees]
            local_h = [
                gamma * degrees[v]
                + comb(n - 1 - degrees[v], 2)
                - edge_total
                - red_triangles[v]
                - blue_triangles[v]
                for v in range(n)
            ]
            for mask, side_vertices, outside_vertices in subset_data:
                a = len(side_vertices)
                b = n - a
                side_set = set(side_vertices)
                edge_count = sum(
                    adjacency[u] >> v & 1 for u, v in combinations(side_vertices, 2)
                )
                missing = comb(a, 2) - edge_count
                cut = sum(
                    adjacency[u] >> v & 1
                    for u in side_vertices
                    for v in outside_vertices
                )
                cap_sum = sum(red_triangles[v] for v in side_vertices)
                need(
                    balanced_squares(2 * edge_count, a) - a * edge_count
                    <= cap_sum,
                    "small-graph internal inequality",
                )
                need(
                    3 * comb(a, 3)
                    + 2 * balanced_pairs(cut, b)
                    - (3 * (a - 2) + 2 * b) * missing
                    <= cap_sum,
                    "small-graph crossing inequality",
                )
                actual_missing = sum(
                    weights[u] + weights[v]
                    for u, v in combinations(side_vertices, 2)
                    if not (adjacency[u] >> v & 1)
                )
                required = (
                    (a - 1) * sum(weights[v] for v in side_vertices)
                    + a * sum(min(0, weights[v]) for v in outside_vertices)
                    - sum(local_h[v] for v in side_vertices)
                )
                top = sorted(
                    (
                        weights[u] + weights[v]
                        for u, v in combinations(side_vertices, 2)
                    ),
                    reverse=True,
                )
                need(required <= actual_missing, "small-graph weighted lower bound")
                need(actual_missing <= sum(top[:missing]), "small-graph weighted upper bound")
                cuts += 1
            graphs += 1
    return {"small_labeled_graphs": graphs, "small_physical_cuts": cuts}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--target-stream", type=Path, required=True)
    args = parser.parse_args()

    audit = reconstruct()
    target = compare_target(args.source, args.target_stream, audit)
    controls = small_graph_controls()
    output = {
        "status": "INDEPENDENT_H3535_COMPLETE_HARD_CUT_PASS",
        **target,
        "profiles": len(audit["profiles"]),
        "profile_counts_by_M": audit["profile_counts_by_M"],
        "oriented_side_placements": audit["oriented_side_placements"],
        "candidate_violations": audit["candidate_violations"],
        "closed_by": audit["closed_by"],
        "closed_by_M": audit["closed_by_M"],
        "closed_by_color": audit["closed_by_color"],
        "minimum_positive_gaps": audit["minimum_positive_gaps"],
        "minimum_gap_witness": audit["minimum_gap_witness"],
        "boundary_sizes_13_16": {
            a: audit["closed_by_size"].get(a, {}) for a in range(13, 17)
        },
        "independent_sorted_record_sha256": audit[
            "independent_sorted_record_sha256"
        ],
        **controls,
        "inherited_not_reproved": [
            "translation of the displayed triangle caps from the hard-deficiency Ramsey branch",
            "the degree window 18 through 24 for a hypothetical Ramsey(5,5;43) graph",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
