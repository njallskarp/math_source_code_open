#!/usr/bin/env python3
"""Clean-room checks for the hard-branch two-color high-pair cover.

This program imports no target Python. Its sole external input is the target's
compact certificate, whose bytes and every entry are checked. Arithmetic is
exact Python integer arithmetic throughout.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
from json import dumps, loads
from math import comb
from pathlib import Path
import sys


TARGET_CERTIFICATE_SHA256 = (
    "92af1173b28d905d808ef40cac1dd644ceb60b7569b478f5681f873e97fe6572"
)
CATALOG_COUNTS_IMPORTED = {10: 313, 11: 105, 12: 12, 13: 1}
DEGREE_WEIGHTS = ((18, 21), (19, 12), (20, 3), (22, 3), (23, 12), (24, 21))
ALL_EDGES = tuple(combinations(range(43), 2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def convex_binomial_minimum(total: int, slots: int, cap: int) -> int:
    """Minimize sum binom(x_i,2) by selecting exact marginal costs."""
    require(slots > 0 and 0 <= total <= slots * cap, "invalid incidence total")
    marginal_costs = sorted(level for level in range(cap) for _ in range(slots))
    return sum(marginal_costs[:total])


def incidence_lower_bound(k: int) -> int:
    """Independent degree-incidence relaxation for n=43 and degree 21."""
    outside = 43 - k
    require(1 <= outside and 0 <= k <= 42, "unsupported subset order")
    values = []
    for internal_edges in range(comb(k, 2) + 1):
        crossing = 21 * k - 2 * internal_edges
        if not 0 <= crossing <= k * outside:
            continue
        inside_cost = convex_binomial_minimum(2 * internal_edges, k, k - 1)
        outside_cost = convex_binomial_minimum(crossing, outside, k)
        values.append(inside_cost + outside_cost - comb(k, 2) + internal_edges)
    require(values, "empty incidence relaxation")
    return min(values)


def reconstructed_certificate() -> dict:
    bounds = []
    for k in range(15, 43):
        lower = incidence_lower_bound(k)
        margin = lower - 9 * comb(k, 2)
        bounds.append(
            {
                "balanced_vertices": k,
                "pair_sum_lower": lower,
                "margin_above_all_codegrees_9": margin,
                "high_pairs_lower_if_codegrees_at_most_13": (margin + 3) // 4,
            }
        )

    roots = []
    for cross_total in range(214, 221):
        for pair_color in ("red", "blue"):
            for codegree in range(10, 14):
                roots.append(
                    {
                        "M": cross_total,
                        "red_edges": 231 + cross_total,
                        "pair_color": pair_color,
                        "codegree": codegree,
                        "cell_sizes": [
                            codegree,
                            20 - codegree,
                            20 - codegree,
                            codegree + 1,
                        ],
                        "common_core_types_imported": CATALOG_COUNTS_IMPORTED[codegree],
                        "free_edges_after_pinning_common_core": 820 - comb(codegree, 2),
                    }
                )
    return {"schema": 1, "bounds": bounds, "scalar_roots": roots}


def check_certificate(path: Path) -> tuple[dict, int]:
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == TARGET_CERTIFICATE_SHA256,
            "target certificate hash mismatch")
    target = loads(raw)
    expected = reconstructed_certificate()
    require(target == expected, "target certificate differs entry-by-entry")

    mutations = []
    mutation = loads(dumps(target))
    mutation["bounds"].pop()
    mutations.append(mutation)
    mutation = loads(dumps(target))
    mutation["scalar_roots"].pop()
    mutations.append(mutation)
    mutation = loads(dumps(target))
    mutation["scalar_roots"][0]["cell_sizes"][3] -= 1
    mutations.append(mutation)
    mutation = loads(dumps(target))
    mutation["scalar_roots"][4]["red_edges"] = 903 - mutation["scalar_roots"][4]["red_edges"]
    mutations.append(mutation)
    mutation = loads(dumps(target))
    mutation["scalar_roots"].append(loads(dumps(mutation["scalar_roots"][0])))
    mutations.append(mutation)
    rejected = sum(candidate != expected for candidate in mutations)
    require(rejected == len(mutations), "certificate mutation was accepted")
    return target, rejected


def enumerate_hard_degree_profiles() -> tuple[dict[int, int], dict[int, int], int]:
    """Enumerate unordered degree histograms by a recursive weight budget."""
    counts: Counter[int] = Counter()
    exact_minimum: defaultdict[int, int] = defaultdict(lambda: 44)
    profiles = set()

    def visit(index: int, remaining_vertices: int, weight: int,
              signed_deviation: int, noncentral: tuple[int, ...]) -> None:
        if index == len(DEGREE_WEIGHTS):
            n21 = remaining_vertices
            degree_sum = 903 + signed_deviation
            if degree_sum % 2 or degree_sum > 902:
                return
            require(weight <= 39 and weight % 6 == 3, "hard-profile parity failure")
            cross_total = degree_sum // 2 - 231
            excess = (43 - weight) // 2
            doubly_exact_lower = n21 - excess
            require(214 <= cross_total <= 220, "hard profile escaped M range")
            require(doubly_exact_lower >= 22, "hard profile lost 22 exact anchors")
            record = noncentral + (n21,)
            require(record not in profiles, "duplicate degree histogram")
            profiles.add(record)
            counts[cross_total] += 1
            exact_minimum[cross_total] = min(
                exact_minimum[cross_total], doubly_exact_lower
            )
            return

        degree, cost = DEGREE_WEIGHTS[index]
        maximum = min(remaining_vertices, (39 - weight) // cost)
        for multiplicity in range(maximum + 1):
            visit(
                index + 1,
                remaining_vertices - multiplicity,
                weight + cost * multiplicity,
                signed_deviation + (degree - 21) * multiplicity,
                noncentral + (multiplicity,),
            )

    visit(0, 43, 0, 0, ())
    require(len(profiles) == 104, "unexpected hard degree-profile total")
    return dict(sorted(counts.items())), dict(sorted(exact_minimum.items())), len(profiles)


def is_red(red_edges: set[tuple[int, int]], u: int, v: int) -> bool:
    return (u, v) in red_edges if u < v else (v, u) in red_edges


def pair_codegree(red_edges: set[tuple[int, int]], u: int, v: int) -> int:
    pair_is_red = is_red(red_edges, u, v)
    return sum(
        is_red(red_edges, u, w) == pair_is_red
        and is_red(red_edges, v, w) == pair_is_red
        for w in range(43)
        if w not in (u, v)
    )


def synthetic_root(M: int, pair_color: str, c: int) -> set[tuple[int, int]]:
    """Make a transport-only assignment, deliberately not a Ramsey witness."""
    rest = [2 + (17 * i) % 41 for i in range(41)]
    common = rest[:c]
    u_only = rest[c:20]
    v_only = rest[20:40 - c]
    neither = rest[40 - c:]
    require(list(map(len, (common, u_only, v_only, neither))) ==
            [c, 20 - c, 20 - c, c + 1], "synthetic cell partition failed")

    red_edges: set[tuple[int, int]] = set()

    def add(u: int, v: int) -> None:
        red_edges.add((min(u, v), max(u, v)))

    if pair_color == "red":
        add(0, 1)
        for w in common + u_only:
            add(0, w)
        for w in common + v_only:
            add(1, w)
    else:
        require(pair_color == "blue", "invalid pair color")
        for w in v_only + neither:
            add(0, w)
        for w in u_only + neither:
            add(1, w)

    target_total = 231 + M
    needed = target_total - len(red_edges)
    internal_edges = list(combinations(range(2, 43), 2))
    require(0 <= needed <= len(internal_edges), "synthetic red total impossible")
    red_edges.update(internal_edges[:needed])
    require(len(red_edges) == target_total, "synthetic red total mismatch")
    require(sum(is_red(red_edges, 0, w) for w in range(43) if w != 0) == 21,
            "first endpoint not balanced")
    require(sum(is_red(red_edges, 1, w) for w in range(43) if w != 1) == 21,
            "second endpoint not balanced")
    require(pair_codegree(red_edges, 0, 1) == c, "synthetic codegree mismatch")
    return red_edges


def transport_roundtrip(red_edges: set[tuple[int, int]], expected_color: str,
                        expected_c: int, expected_total: int) -> tuple[int, int]:
    sigma_red = is_red(red_edges, 0, 1)
    require(("red" if sigma_red else "blue") == expected_color, "pair color mismatch")
    cells = [[], [], [], []]
    for w in range(2, 43):
        left = is_red(red_edges, 0, w) == sigma_red
        right = is_red(red_edges, 1, w) == sigma_red
        cell = 0 if left and right else 1 if left else 2 if right else 3
        cells[cell].append(w)
    c = len(cells[0])
    require(c == expected_c, "transport codegree mismatch")
    require(list(map(len, cells)) == [c, 20 - c, 20 - c, c + 1],
            "transport cell sizes mismatch")

    order = [0, 1] + [w for cell in cells for w in reversed(cell)]
    transported = {
        (i, j): is_red(red_edges, order[i], order[j]) for i, j in ALL_EDGES
    }
    fixed: dict[tuple[int, int], bool] = {}
    free: dict[tuple[int, int], bool] = {}
    cell_starts = (2, 2 + c, 22, 42 - c, 43)

    for i, j in ALL_EDGES:
        if i < 2:
            if (i, j) == (0, 1):
                same_sigma = True
            elif i == 0:
                same_sigma = j < 22
            else:
                same_sigma = j < 2 + c or 22 <= j < 42 - c
            expected_red = same_sigma if sigma_red else not same_sigma
            require(transported[i, j] == expected_red,
                    "canonical endpoint-star pin mismatch")
            fixed[i, j] = expected_red
        elif 2 <= i < j < 2 + c:
            fixed[i, j] = transported[i, j]
        else:
            free[i, j] = transported[i, j]
    require(len(fixed) == 83 + comb(c, 2), "fixed physical-edge count mismatch")
    require(len(free) == 820 - comb(c, 2), "free physical-edge count mismatch")
    require(set(fixed).isdisjoint(free) and set(fixed) | set(free) == set(ALL_EDGES),
            "physical-edge partition incomplete")
    rebuilt = dict(fixed)
    rebuilt.update(free)
    require(rebuilt == transported, "physical-edge transport is not bijective")
    require(sum(rebuilt.values()) == expected_total, "transport changed global red total")

    for left_cell in range(4):
        for right_cell in range(left_cell, 4):
            lo1, hi1 = cell_starts[left_cell], cell_starts[left_cell + 1]
            lo2, hi2 = cell_starts[right_cell], cell_starts[right_cell + 1]
            candidates = [
                (i, j)
                for i in range(lo1, hi1)
                for j in range(lo2, hi2)
                if i < j
            ]
            if left_cell == right_cell == 0:
                require(all(edge in fixed for edge in candidates), "common core not pinned")
            elif candidates:
                require(all(edge in free for edge in candidates), "shared cell edge omitted")

    neither_start = cell_starts[3]
    omitted = next(combinations(range(neither_start, 43), 2))
    damaged_free = dict(free)
    damaged_free.pop(omitted)
    require(set(fixed) | set(damaged_free) != set(ALL_EDGES),
            "neither-cell omission mutation escaped")
    return len(rebuilt), len(free)


def transport_controls() -> dict:
    assignments = 0
    physical_edges = 0
    blue_complement_rejections = 0
    free_counts = set()
    for M in range(214, 221):
        for color in ("red", "blue"):
            for c in range(10, 14):
                red_edges = synthetic_root(M, color, c)
                checked, free = transport_roundtrip(red_edges, color, c, 231 + M)
                assignments += 1
                physical_edges += checked
                free_counts.add(free)
                if color == "blue":
                    complemented_total = 903 - len(red_edges)
                    require(complemented_total != 231 + M,
                            "global complement preserved a blue root's M slice")
                    blue_complement_rejections += 1
    require(assignments == 56 and physical_edges == 56 * 903, "root coverage mismatch")
    return {
        "transport_only_assignments": assignments,
        "physical_edge_values_roundtripped": physical_edges,
        "free_edge_counts": sorted(free_counts),
        "blue_global_complement_mutations_rejected": blue_complement_rejections,
        "neither_cell_omission_mutations_rejected": assignments,
    }


def logical_truth_tables() -> tuple[int, int, int]:
    five_set_rejected = 0
    for mask in range(1 << 10):
        red_count = mask.bit_count()
        accepted = 1 <= red_count <= 9
        if not accepted:
            five_set_rejected += 1
    require(five_set_rejected == 2, "five-set clause has wrong semantics")

    conjunction_rows = 0
    conjunction_models = 0
    for edge_mask in range(8):
        desired = edge_mask == 7
        for auxiliary in (False, True):
            conjunction_rows += 1
            conjunction_models += auxiliary == desired
    require(conjunction_models == 8, "triple equivalence has wrong semantics")
    return 1 << 10, five_set_rejected, conjunction_rows


def blue_only_control() -> int:
    red_edges = {(u, v) for u in range(21) for v in range(21, 43)}
    selected = range(21, 43)
    pairs = list(combinations(selected, 2))
    require(all(not is_red(red_edges, u, v) for u, v in pairs),
            "blue-only control has a red selected pair")
    require(all(pair_codegree(red_edges, u, v) == 20 for u, v in pairs),
            "blue-only control codegree mismatch")
    return len(pairs)


def main() -> None:
    require(len(sys.argv) == 2, "usage: verify_review.py TARGET_CERTIFICATE.json")
    target, certificate_mutations = check_certificate(Path(sys.argv[1]))
    profile_counts, exact_minima, profile_total = enumerate_hard_degree_profiles()
    transport = transport_controls()
    five_rows, five_rejected, conjunction_rows = logical_truth_tables()
    k14_lower = incidence_lower_bound(14)
    require(k14_lower <= 9 * comb(14, 2), "claimed 15-vertex method boundary vanished")
    require(target["bounds"][0]["pair_sum_lower"] == 949, "k=15 threshold mismatch")
    require(target["bounds"][7]["high_pairs_lower_if_codegrees_at_most_13"] == 16,
            "22-anchor high-pair bound mismatch")

    report = {
        "status": "INDEPENDENTLY_VERIFIED_HARD_TWO_COLOR_PAIR_COVER",
        "target_certificate_sha256": TARGET_CERTIFICATE_SHA256,
        "moment_bounds_checked": len(target["bounds"]),
        "k14_method_lower_vs_all_9": [k14_lower, 9 * comb(14, 2)],
        "k15_lower_vs_all_9": [949, 9 * comb(15, 2)],
        "high_pairs_for_22_exact_anchors": 16,
        "hard_degree_profiles_checked": profile_total,
        "hard_profiles_by_M": profile_counts,
        "aggregate_exact_anchor_minima_by_M": exact_minima,
        "scalar_roots_checked": len(target["scalar_roots"]),
        "catalog_template_total_imported_not_reverified": 6034,
        "certificate_mutations_rejected": certificate_mutations,
        "five_set_truth_rows": five_rows,
        "five_set_monochromatic_rows_rejected": five_rejected,
        "triple_equivalence_truth_rows": conjunction_rows,
        "blue_only_control_pairs": blue_only_control(),
        **transport,
    }
    print(dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
