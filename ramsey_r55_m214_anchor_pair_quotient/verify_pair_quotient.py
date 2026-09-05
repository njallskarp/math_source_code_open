#!/usr/bin/env python3
"""Definition-level audit of the high-codegree anchor-pair quotient."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def choose(n: int, k: int) -> int:
    if not 0 <= k <= n:
        return 0
    return len(tuple(itertools.combinations(range(n), k)))


def audit_local_double_count() -> tuple[int, int]:
    """Check sum_{uv red} q_R(u,v)=2e_R(N_R(u)) definitionally."""
    graphs = rooted_checks = 0
    for n in range(1, 7):
        pairs = tuple(itertools.combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            red = {
                pair for index, pair in enumerate(pairs) if mask & (1 << index)
            }
            graphs += 1
            for anchor in range(n):
                neighbourhood = {
                    other for other in range(n)
                    if other != anchor and tuple(sorted((anchor, other))) in red
                }
                local_edges = sum(
                    tuple(sorted((left, right))) in red
                    for left, right in itertools.combinations(neighbourhood, 2)
                )
                codegree_sum = 0
                for partner in neighbourhood:
                    codegree_sum += sum(
                        tuple(sorted((partner, other))) in red
                        for other in neighbourhood if other != partner
                    )
                require(codegree_sum == 2 * local_edges, "local double count failed")
                rooted_checks += 1
    return graphs, rooted_checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("types", type=Path)
    args = parser.parse_args()

    # The local double count and the R(3,5)=14 edge-codegree cap.
    local_red_edges = 100
    incident_codegree_sum = 2 * local_red_edges
    cross_neighbours = 6
    central_neighbours = 15
    edge_codegree_cap = 13
    central_sum_lower = incident_codegree_sum - cross_neighbours * edge_codegree_cap
    maximum_if_below_nine = (
        cross_neighbours * edge_codegree_cap + central_neighbours * 8
    )
    require(central_sum_lower == 122, "central lower bound failed")
    require(
        maximum_if_below_nine == 198 < incident_codegree_sum,
        "codegree-nine forcing failed",
    )
    graphs, rooted_checks = audit_local_double_count()

    # Enumerate all possible six-subsets in E.  The residual S5 x S7 orbit is
    # determined exactly by exception membership s and the ordinary-red count k.
    orbit_counts: dict[tuple[int, int], int] = {}
    for subset in itertools.combinations(range(13), 6):
        chosen = frozenset(subset)
        signature = (int(5 in chosen), len(chosen & frozenset(range(5))))
        orbit_counts[signature] = orbit_counts.get(signature, 0) + 1
    expected_orbits = {(s, k) for s in range(2) for k in range(6)}
    require(set(orbit_counts) == expected_orbits, "E orbit keys failed")
    for (s, k), observed in orbit_counts.items():
        p = s + k
        require(
            observed == choose(5, k) * choose(7, 6 - p),
            "E orbit size failed",
        )
    require(sum(orbit_counts.values()) == choose(13, 6) == 1716, "E cover failed")

    with args.types.open(newline="", encoding="ascii") as source:
        rows = list(csv.DictReader(source))
    require(len(rows) == 60, "type row count failed")
    require(len({(r["c"], r["s"], r["k"]) for r in rows}) == 60, "type keys failed")
    for raw in rows:
        values = {key: int(value) for key, value in raw.items() if key != "unit_sha256"}
        c, s, k, p = (values[key] for key in ("c", "s", "k", "p"))
        require(
            9 <= c <= 13 and s in (0, 1) and 0 <= k <= 5 and p == s + k,
            "type parameter failed",
        )
        e_cells = (p, 6 - p, 6 - p, 1 + p)
        c_cells = (c - p, 14 - c + p, 14 - c + p, c - p)
        require(tuple(values[key] for key in (
            "e_both_red", "e_anchor_only", "e_partner_only", "e_both_blue"
        )) == e_cells, "E cells failed")
        require(tuple(values[key] for key in (
            "c_both_red", "c_anchor_only", "c_partner_only", "c_both_blue"
        )) == c_cells, "central cells failed")
        require(sum(e_cells) == 13 and sum(c_cells) == 28, "partition totals failed")
        require(e_cells[0] + c_cells[0] == c, "codegree partition failed")
        require(all(value >= 0 for value in e_cells + c_cells), "negative cell size")
        expected_orbit = (
            choose(5, k) * choose(7, 6 - p)
            * choose(14, c - p) * choose(14, 14 - c + p)
        )
        require(values["orbit_size"] == expected_orbit, "full orbit size failed")

        # Reconstruct the literal stream independently of the generator.
        e_red = set(range(k)) | ({5} if s else set()) | set(range(6, 6 + 6 - p))
        c_red = {13} | set(range(15, 15 + c - p)) | set(range(29, 29 + 14 - c + p))
        neighbours = e_red | c_red
        require(len(neighbours) == 21, "partner degree failed")
        literals = []
        for vertex in range(43):
            if vertex in (13, 14):
                continue
            i, j = sorted((14, vertex))
            variable = i * (86 - i - 1) // 2 + (j - i - 1) + 1
            literals.append(variable if vertex in neighbours else -variable)
        digest = hashlib.sha256((" ".join(map(str, literals)) + "\n").encode("ascii")).hexdigest()
        require(digest == raw["unit_sha256"], "unit digest failed")

    file_hash = hashlib.sha256(args.types.read_bytes()).hexdigest()
    print(
        "PASS anchor_pair_force "
        f"incident_sum={incident_codegree_sum} central_sum_lower={central_sum_lower} "
        f"max_if_all_central_at_most_8={maximum_if_below_nine} forced_codegree=9"
    )
    print(f"PASS local_double_count graphs={graphs} rooted_checks={rooted_checks}")
    print(
        "PASS e_neighbour_orbits "
        f"subsets={sum(orbit_counts.values())} orbits={len(orbit_counts)}"
    )
    print(f"PASS pair_types rows={len(rows)} sha256={file_hash}")


if __name__ == "__main__":
    main()
