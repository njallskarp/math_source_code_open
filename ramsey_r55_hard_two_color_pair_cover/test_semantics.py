#!/usr/bin/env python3
"""Cross-check the signed and incidence representations and hard-branch budget.

This author-written control imports both implementations. The independent
certificate checker, check.py, does not import the producer.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

from build import gram_audit, lower_bound
from check import moment_audit, need, pair_codegree


def compare(a, chosen):
    q, norm = gram_audit(a, chosen)
    need(q == moment_audit(a, chosen), "representations disagree")
    n, k = len(a), len(chosen)
    need(norm >= (k if k % 2 == 0 else n - k), "column parity")


def all_small():
    count = 0
    for n in (1, 3, 5):
        edges = list(combinations(range(n), 2))
        for mask in range(1 << len(edges)):
            a = [set() for _ in range(n)]
            for bit, (u, v) in enumerate(edges):
                if mask >> bit & 1:
                    a[u].add(v)
                    a[v].add(u)
            balanced = [v for v in range(n) if len(a[v]) == (n - 1) // 2]
            for bits in range(1 << len(balanced)):
                compare(a, [v for bit, v in enumerate(balanced) if bits >> bit & 1])
                count += 1
    residues = {x * x % 13 for x in range(1, 13)}
    a = [{v for v in range(13) if (v - u) % 13 in residues} for u in range(13)]
    for bits in range(1 << 13):
        compare(a, [v for v in range(13) if bits >> v & 1])
        count += 1
    return count


def hard_budget():
    # Exhaust all degree histograms under the deficiency weight and parity.
    # No triangle-divisibility or later local screens are applied here.
    U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
    weights = {18: 21, 19: 12, 20: 3, 22: 3, 23: 12, 24: 21}
    for d in U:
        coefficient = 2 * (U[d] + U[42 - d]) + 3 * d * (42 - d) - 42 * 41
        need(coefficient == 29 - weights.get(d, 0), "deficiency identity coefficient")
    counts = Counter()
    minima = defaultdict(lambda: 43)
    for ns in product(*(range(39 // weights[d] + 1) for d in weights)):
        profile = dict(zip(weights, ns))
        w = sum(weights[d] * profile[d] for d in weights)
        if w > 39:
            continue
        profile[21] = 43 - sum(profile.values())
        if profile[21] < 0:
            continue
        degree_sum = sum(d * v for d, v in profile.items())
        if degree_sum % 2 or degree_sum > 902:
            continue
        need(w % 6 == 3, "weight parity")
        M = degree_sum // 2 - 231
        exact_lower = profile[21] - (43 - w) // 2
        need(214 <= M <= 220 and exact_lower >= 242 - M, "hard coverage")
        counts[M] += 1
        minima[M] = min(minima[M], exact_lower)
    need(sum(counts.values()) == 104, "unfiltered degree budget coverage")
    return dict(sorted(counts.items())), dict(sorted(minima.items()))


if __name__ == "__main__":
    small = all_small()
    data = json.loads((Path(__file__).resolve().parent / "fixture.json").read_text())
    a = [set(row) for row in data["red_adjacency"]]
    for k in range(15, 34):
        compare(a, list(range(10, 10 + k)))
    # A degree-only countercontrol to silently demanding a RED high pair:
    # the 22-vertex side of K_{21,22} is balanced and all its pairs are blue.
    # This graph has independent five-sets and is not a Ramsey witness.
    bipartite = [set(range(21, 43)) if v < 21 else set(range(21)) for v in range(43)]
    selected = list(range(21, 43))
    compare(bipartite, selected)
    need(all(v not in bipartite[u] and pair_codegree(bipartite, u, v) == 20
             for u, v in combinations(selected, 2)), "pair-color scope control")
    counts, minima = hard_budget()
    print(json.dumps({"signed_and_incidence_subsets_compared": small + 20,
                      "unfiltered_degree_profiles_by_M": counts,
                      "budget_exact_anchor_minima_by_M": minima,
                      "blue_only_degree_control_pairs": comb(22, 2),
                      "codegree_ten_15_vertex_margin": lower_bound(43, 15) - 9 * comb(15, 2)},
                     sort_keys=True, indent=2))
