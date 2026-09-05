#!/usr/bin/env python3
"""Exact arithmetic verifier for the Q6 modular-gap refinement.

The checker enumerates only the finite arithmetic relaxation induced by the
proved live-facet capacities, edge-incidence identity, and mod-17 residue.
It does not enumerate square-free subgraphs.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
import json


Q5_SQUAREFREE_EDGE_CAP = 56
Q6_SQUAREFREE_EDGE_CAP = 132

# Maximum selected Q6 edges compatible with k live Q5 facets.  Entries through
# k=10 are the exact support capacities from the preceding Q6 lift.  At k=11,
# one empty facet leaves at most 32 transverse edges plus a square-free Q5 in
# the opposite facet.  The k=12 entry is the exact external Q6 cap.
EDGE_CAP_BY_LIVE_COUNT = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 1,
    6: 6,
    7: 11,
    8: 20,
    9: 36,
    10: 64,
    11: 32 + Q5_SQUAREFREE_EDGE_CAP,
    12: Q6_SQUAREFREE_EDGE_CAP,
}


def least_positive_delta(edge_count: int) -> int:
    """Least positive delta congruent to 5*edge_count modulo 17."""

    if not 1 <= edge_count <= Q5_SQUAREFREE_EDGE_CAP:
        raise ValueError("a live Q5 facet must have between 1 and 56 edges")
    residue = (5 * edge_count) % 17
    return residue if residue else 17


def arithmetic_minimum(live_count: int) -> tuple[int, int, int, tuple[int, ...]]:
    """Minimize W=11D-E in the exact facet-arithmetic relaxation.

    A state records the least possible D=sum(delta_K) for each sum of facet
    edge counts, along with a lexicographically least attaining profile.
    The identity sum_K e_K=5E enforces divisibility by five.
    """

    if live_count not in EDGE_CAP_BY_LIVE_COUNT or live_count == 0:
        raise ValueError("live_count must lie between 1 and 12")
    edge_cap = EDGE_CAP_BY_LIVE_COUNT[live_count]
    if edge_cap == 0:
        raise ValueError("fewer than five Q5 facets cannot support a Q6 edge")

    states: dict[int, tuple[int, tuple[int, ...]]] = {0: (0, ())}
    for _ in range(live_count):
        next_states: dict[int, tuple[int, tuple[int, ...]]] = {}
        for edge_sum, (delta_sum, profile) in states.items():
            for facet_edges in range(1, Q5_SQUAREFREE_EDGE_CAP + 1):
                new_edge_sum = edge_sum + facet_edges
                if new_edge_sum > 5 * edge_cap:
                    continue
                candidate = (
                    delta_sum + least_positive_delta(facet_edges),
                    profile + (facet_edges,),
                )
                incumbent = next_states.get(new_edge_sum)
                if incumbent is None or candidate < incumbent:
                    next_states[new_edge_sum] = candidate
        states = next_states

    candidates = []
    for facet_edge_sum, (delta_sum, profile) in states.items():
        if facet_edge_sum % 5:
            continue
        edge_count = facet_edge_sum // 5
        if not 1 <= edge_count <= edge_cap:
            continue
        candidates.append(
            (11 * delta_sum - edge_count, edge_count, delta_sum, profile)
        )
    assert candidates
    return min(candidates)


def arithmetic_audit() -> tuple[dict[int, dict[str, object]], str]:
    rows: dict[int, dict[str, object]] = {}
    for live_count in range(5, 13):
        gap, edges, delta_sum, profile = arithmetic_minimum(live_count)
        rows[live_count] = {
            "minimum_W": gap,
            "E": edges,
            "D": delta_sum,
            "facet_edge_profile": profile,
        }
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return rows, sha256(canonical.encode()).hexdigest()


def certificate() -> dict[str, object]:
    audit, audit_hash = arithmetic_audit()
    minimum_gaps = {k: row["minimum_W"] for k, row in audit.items()}
    expected_gaps = {5: 274, 6: 148, 7: 122, 8: 70, 9: 66, 10: 58, 11: 41, 12: 37}
    equality = audit[12]

    assert minimum_gaps == expected_gaps
    assert equality == {
        "minimum_W": 37,
        "E": 95,
        "D": 12,
        "facet_edge_profile": (24,) + (41,) * 11,
    }
    delta_one_edge_counts = tuple(
        edge_count
        for edge_count in range(1, Q5_SQUAREFREE_EDGE_CAP + 1)
        if least_positive_delta(edge_count) == 1
    )
    equality_profiles = tuple(
        profile
        for profile in combinations_with_replacement(delta_one_edge_counts, 12)
        if sum(profile) == 5 * 95
    )
    assert equality_profiles == ((24,) + (41,) * 11,)
    direction_profile = (95 - (24 + 41),) + (95 - (41 + 41),) * 5
    assert direction_profile == (30, 13, 13, 13, 13, 13)
    assert sum(direction_profile) == 95

    local_slack_edge_ratio = Fraction(661 * 132 + 37, 1122 * 132)
    global_slack_coefficient = local_slack_edge_ratio / 20
    retained_coefficient = 1 - global_slack_coefficient
    asymptotic_constant = Fraction(5_183_640, 2_874_791)
    preceding_constant = Fraction(39_270, 21_779)
    improvement = asymptotic_constant - preceding_constant

    assert local_slack_edge_ratio == Fraction(87_289, 148_104)
    assert global_slack_coefficient == Fraction(87_289, 2_962_080)
    assert retained_coefficient == Fraction(2_874_791, 2_962_080)
    assert improvement == Fraction(1_452_990, 62_610_073_189)
    assert 5_183_640 * 21_779 - 39_270 * 2_874_791 == 1_452_990
    assert 5_183_640 * 56_761 - 39_270 * 7_492_489 == -1_452_990

    return {
        "q5_squarefree_edge_cap": Q5_SQUAREFREE_EDGE_CAP,
        "q6_squarefree_edge_cap": Q6_SQUAREFREE_EDGE_CAP,
        "edge_cap_by_live_count": EDGE_CAP_BY_LIVE_COUNT,
        "minimum_W_by_live_count": minimum_gaps,
        "arithmetic_audit_sha256": audit_hash,
        "strict_q6_modular_gap": 37,
        "arithmetic_equality_E_D_k": [95, 12, 12],
        "arithmetic_equality_facet_edges": [24] + [41] * 11,
        "arithmetic_equality_profile_count": len(equality_profiles),
        "arithmetic_equality_direction_edges": list(direction_profile),
        "equality_realizability": "not asserted",
        "local_slack_edge_ratio": str(local_slack_edge_ratio),
        "global_slack_coefficient": str(global_slack_coefficient),
        "bound": "sat(Q_d,Q_2) >= 5183640*d*2^d/(2874791*d+7492489) for d>=6",
        "asymptotic_constant": str(asymptotic_constant),
        "improvement_over_39270_21779": str(improvement),
        "finite_bound_cross_difference": "1452990*(d-1)",
    }


def main() -> None:
    data = certificate()
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    print(json.dumps(data, sort_keys=True, indent=2))
    print(f"certificate_sha256={sha256(canonical.encode()).hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
