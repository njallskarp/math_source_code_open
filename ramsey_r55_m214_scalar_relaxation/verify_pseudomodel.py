#!/usr/bin/env python3
"""Exact checker for the M=214 aggregate-relaxation pseudomodel.

The certificate is not a Ramsey graph.  It simultaneously realizes the degree
and exceptional-signature data by a simple graph and assigns scalar local-edge
variables satisfying the deficiency identities.  The relaxation intentionally
does not equate those scalar variables with induced-edge counts in the simple
graph.  The checker reports this missing compatibility explicitly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import combinations
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "PSEUDOMODEL.json"
EXTREMA = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
BASE = {18: 220, 19: 221, 20: 220, 21: 220, 22: 221, 23: 223, 24: 223}


def vertices(mask: int, order: int) -> list[int]:
    return [i for i in range(order) if mask >> i & 1]


def is_clique(mask: int, adjacency: list[int], red: bool) -> bool:
    return all(bool(adjacency[i] >> j & 1) == red for i, j in combinations(vertices(mask, len(adjacency)), 2))


def clique_number(mask: int, adjacency: list[int], red: bool) -> int:
    vs = vertices(mask, len(adjacency))
    for size in range(min(5, len(vs)), 0, -1):
        for subset in combinations(vs, size):
            if is_clique(sum(1 << i for i in subset), adjacency, red):
                return size
    return 0


def ramsey_upper_table() -> dict[tuple[int, int], int]:
    """The parity-improved recurrence used by the committed union-cut lemma."""
    table = {(1, q): 1 for q in range(1, 6)}
    table.update({(p, 1): 1 for p in range(1, 6)})
    for p in range(2, 6):
        for q in range(2, 6):
            left, right = table[p - 1, q], table[p, q - 1]
            table[p, q] = left + right - int(left % 2 == 0 and right % 2 == 0)
    return table


def build_exceptional_core(data: dict) -> list[int]:
    core = data["exceptional_core"]
    order = core["order"]
    residues = set(core["red_difference_set_mod_13"])
    assert order == 13
    assert residues == {1, 3, 4, 9, 10, 12}
    adjacency = [0] * order
    for i in range(order):
        for j in range(order):
            if i != j and (j - i) % order in residues:
                adjacency[i] |= 1 << j
    assert all((adjacency[i] >> j & 1) == (adjacency[j] >> i & 1) for i in range(order) for j in range(order))
    return adjacency


def build_central_graph(data: dict) -> list[int]:
    spec = data["central_red_graph"]
    order = spec["order"]
    distances = set(spec["cyclic_distances"])
    deleted = tuple(spec["deleted_edge"])
    assert order == 30 and distances == set(range(1, 8)) | {15} and deleted == (28, 29)
    adjacency = [0] * order
    for i, j in combinations(range(order), 2):
        delta = (j - i) % order
        if min(delta, order - delta) in distances and (i, j) != deleted:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    return adjacency


def connected_after_deletions(adjacency: list[int], deleted: tuple[int, ...]) -> bool:
    remaining = [v for v in range(len(adjacency)) if v not in deleted]
    if not remaining:
        return True
    allowed = sum(1 << v for v in remaining)
    seen = 1 << remaining[0]
    queue = deque([remaining[0]])
    while queue:
        v = queue.popleft()
        new = adjacency[v] & allowed & ~seen
        while new:
            bit = new & -new
            w = bit.bit_length() - 1
            seen |= bit
            new ^= bit
            queue.append(w)
    return seen == allowed


def diameter(adjacency: list[int]) -> int:
    answer = 0
    for source in range(len(adjacency)):
        distance = {source: 0}
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for w in vertices(adjacency[v], len(adjacency)):
                if w not in distance:
                    distance[w] = distance[v] + 1
                    queue.append(w)
        assert len(distance) == len(adjacency)
        answer = max(answer, max(distance.values()))
    return answer


def induced(adjacency: list[int], keep: list[int], red: bool) -> list[int]:
    index = {v: i for i, v in enumerate(keep)}
    result = [0] * len(keep)
    for old_i in keep:
        for old_j in keep:
            if old_i == old_j:
                continue
            edge = bool(adjacency[old_i] >> old_j & 1)
            if edge == red:
                result[index[old_i]] |= 1 << index[old_j]
    return result


def first_monochromatic_five(adjacency: list[int]) -> tuple[str, tuple[int, ...]] | None:
    for subset in combinations(range(len(adjacency)), 5):
        mask = sum(1 << i for i in subset)
        if is_clique(mask, adjacency, True):
            return "red", subset
        if is_clique(mask, adjacency, False):
            return "blue", subset
    return None


def verify(data: dict, emit: bool = True) -> list[str]:
    assert data["schema"] == "r55-m214-aggregate-pseudomodel-v1"
    assert data["M"] == 214
    F = build_exceptional_core(data)
    assert [row.bit_count() for row in F] == [6] * 13
    assert clique_number((1 << 13) - 1, F, True) <= 4
    assert clique_number((1 << 13) - 1, F, False) <= 4
    assert not any(is_clique(sum(1 << i for i in ss), F, color) for color in (True, False) for ss in combinations(range(13), 5))

    signatures = data["central_signatures"]
    assert len(signatures) == 30 and len(set(signatures)) == 30
    assert all(0 <= mask < 1 << 13 for mask in signatures)
    assert Counter(mask.bit_count() for mask in signatures) == Counter({6: 28, 7: 2})
    assert [sum(mask >> i & 1 for mask in signatures) for i in range(13)] == [14] * 13

    all_exceptional = (1 << 13) - 1
    multiplicities = Counter(signatures)
    allowed_count = 0
    minimum_capacity_slack = 30
    for mask in range(1 << 13):
        if mask.bit_count() not in (6, 7):
            continue
        r = clique_number(mask, F, True)
        s = clique_number(all_exceptional ^ mask, F, False)
        if r <= 3 and s <= 3:
            capacity = min(30, comb(8 - r - s, 4 - r) - 1)
            if capacity > 0:
                allowed_count += 1
                if mask in multiplicities:
                    minimum_capacity_slack = min(minimum_capacity_slack, capacity - multiplicities[mask])
        if mask in multiplicities:
            assert -mask.bit_count() <= data["M"] - BASE[21]
            assert r <= 3 and s <= 3
            assert multiplicities[mask] <= capacity
    assert allowed_count == 3432

    upper = ramsey_upper_table()
    red_roots = [m for m in range(1 << 13) if m.bit_count() <= 4 and is_clique(m, F, True)]
    blue_roots = [m for m in range(1 << 13) if m.bit_count() <= 4 and is_clique(m, F, False)]
    root_count = tight_count = 0
    minimum_cut_slack = 10**9
    for A in red_roots:
        for B in blue_roots:
            if not (A | B) or A & B:
                continue
            root_count += 1
            outside = all_exceptional ^ (A | B)
            common_exceptional = 0
            for v in vertices(outside, 13):
                red_to_A = all(F[a] >> v & 1 for a in vertices(A, 13))
                blue_to_B = all(not (F[b] >> v & 1) for b in vertices(B, 13))
                common_exceptional += int(red_to_A and blue_to_B)
            rhs = upper[5 - A.bit_count(), 5 - B.bit_count()] - 1 - common_exceptional
            lhs = sum(count for mask, count in multiplicities.items() if mask & A == A and not mask & B)
            assert lhs <= rhs
            slack = rhs - lhs
            minimum_cut_slack = min(minimum_cut_slack, slack)
            tight_count += int(slack == 0)
    assert root_count == 4043

    C = build_central_graph(data)
    assert [row.bit_count() for row in C[:28]] == [15] * 28
    assert [row.bit_count() for row in C[28:]] == [14] * 2
    full = [0] * 43
    for i in range(13):
        full[i] |= F[i]
    for c, mask in enumerate(signatures):
        cv = 13 + c
        for e in vertices(mask, 13):
            full[e] |= 1 << cv
            full[cv] |= 1 << e
        for d in vertices(C[c], 30):
            full[cv] |= 1 << (13 + d)
    degrees = [row.bit_count() for row in full]
    assert degrees == [20] * 13 + [21] * 30
    edges = sum(degrees) // 2
    assert edges == 445 and edges - 231 == data["M"]

    profile_spec = data["assigned_local_profiles"]
    profiles: list[tuple[int, int]] = []
    profiles.extend([tuple(profile_spec["exceptional_degree_20"])] * 13)
    profiles.extend(tuple(profile_spec["central_signature_size_6"] if mask.bit_count() == 6 else profile_spec["central_signature_size_7"]) for mask in signatures)
    deficiencies = []
    for v, (t_red, t_blue) in enumerate(profiles):
        d = degrees[v]
        neighbor_degree_sum = sum(degrees[w] for w in vertices(full[v], 43))
        rhs = comb(42 - d, 2) - edges + neighbor_degree_sum
        assert t_red + t_blue == rhs
        assert t_red <= EXTREMA[d] - 7
        assert t_blue <= EXTREMA[42 - d] - 7
        deficiencies.extend((EXTREMA[d] - t_red, EXTREMA[42 - d] - t_blue))
    assert sum(deficiencies) == 604
    assert sum(t[0] for t in profiles) == 4209
    assert sum(t[1] for t in profiles) == 4389
    assert 4209 // 3 == 1403 and 4389 // 3 == 1463

    q = sum(row.bit_count() for row in F) // 2
    class_S = -2 * q
    assert q == 39
    assert class_S <= 13 * (data["M"] - BASE[20])
    assert class_S >= (-1) * 13 * 20 - 30 * (data["M"] - BASE[21])

    D = list(range(28))
    red_D = induced(C, D, True)
    blue_D = induced(C, D, False)
    assert min(row.bit_count() for row in red_D) == 13
    assert min(row.bit_count() for row in blue_D) == 12
    assert all(connected_after_deletions(red_D, removed) for size in range(4) for removed in combinations(range(28), size))
    assert all(connected_after_deletions(blue_D, removed) for size in range(2) for removed in combinations(range(28), size))
    assert diameter(red_D) <= 5 and diameter(blue_D) <= 5
    for c in D:
        assert signatures[c].bit_count() == 6
        assert C[c].bit_count() == 15
        assert 29 - C[c].bit_count() == 14
        assert profiles[13 + c] == (100, 100)

    actual_profiles = []
    for v in range(43):
        red_neighbors = vertices(full[v], 43)
        blue_neighbors = [w for w in range(43) if w != v and not (full[v] >> w & 1)]
        actual_red = sum(bool(full[i] >> j & 1) for i, j in combinations(red_neighbors, 2))
        actual_blue = sum(not bool(full[i] >> j & 1) for i, j in combinations(blue_neighbors, 2))
        actual_profiles.append((actual_red, actual_blue))
    mismatch_count = sum(actual_profiles[v] != profiles[v] for v in range(43))
    assert mismatch_count > 0
    obstruction = first_monochromatic_five(full)
    assert obstruction is not None

    lines = [
        "PASS certificate schema=r55-m214-aggregate-pseudomodel-v1",
        "PASS exceptional_core order=13 edges=39 degree=6 red_K5=0 blue_K5=0",
        f"PASS signatures count=30 size6=28 size7=2 incidence=14^13 allowed={allowed_count} capacity_min_slack={minimum_capacity_slack}",
        f"PASS union_cuts roots={root_count} tight={tight_count} min_slack={minimum_cut_slack}",
        "PASS degree_fixture edges=445 degrees=20^13,21^30 M=214",
        "PASS scalar_profiles W=39 Delta=604 T_red=1403 T_blue=1463 D=28",
        "PASS class_sieve q_20,20=39 S_20=-78 bounds=[-80,-78]",
        f"PASS backbone red_delta=13 blue_delta=12 red_diameter={diameter(red_D)} blue_diameter={diameter(blue_D)} kappa_red>=4 kappa_blue>=2",
        f"LIMITATION assigned_profiles_are_aggregate mismatch_vertices={mismatch_count} monochromatic_{obstruction[0]}_K5={','.join(map(str, obstruction[1]))}",
    ]
    if emit:
        print("\n".join(lines))
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    verify(data)
    print(f"CERTIFICATE_SHA256 {hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
