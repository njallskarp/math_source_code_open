#!/usr/bin/env python3
"""Exact moment bounds and the complete two-color hard-branch pair cover.

The proof is in PROOF.md. This builds compact arithmetic evidence, not a
Boolean backend or a catalog of globally realizable graphs.
"""
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

CORE_COUNTS = {10: 313, 11: 105, 12: 12, 13: 1}


def lower_bound(n, k):
    if n < 1 or n % 2 != 1 or not 0 <= k <= n:
        raise ValueError("odd graph order and valid subset order required")
    parity = k if k % 2 == 0 else n - k
    numerator = (n - 4) * k * k - (2 * n - 5) * k + parity
    return -((-numerator) // 8)


def gram_audit(adjacency, selected):
    n = len(adjacency)
    if n % 2 != 1 or len(set(selected)) != len(selected):
        raise ValueError("invalid graph order or duplicate selected vertex")
    h = (n - 1) // 2
    if any(len(adjacency[v]) != h for v in selected):
        raise ValueError("selected vertex is not balanced")
    rows = [[0 if v == w else 1 if w in adjacency[v] else -1
             for w in range(n)] for v in selected]
    qsum = 0
    for i, j in combinations(range(len(selected)), 2):
        dot = sum(x * y for x, y in zip(rows[i], rows[j]))
        u, v = selected[i], selected[j]
        if v in adjacency[u]:
            q = len(adjacency[u] & adjacency[v])
        else:
            q = sum(w != u and w != v and w not in adjacency[u]
                    and w not in adjacency[v] for w in range(n))
        if dot != 4 * q - (n - 4):
            raise ValueError("pair Gram identity failed")
        qsum += q
    norm = sum(sum(row[w] for row in rows) ** 2 for w in range(n))
    k = len(selected)
    if 8 * qsum != (n - 4) * k * k - (2 * n - 5) * k + norm:
        raise ValueError("summed Gram identity failed")
    if qsum < lower_bound(n, k):
        raise ValueError("parity bound failed")
    return qsum, norm


def certificate():
    bounds = []
    for k in range(15, 43):
        q = lower_bound(43, k)
        margin = q - 9 * comb(k, 2)
        bounds.append({"balanced_vertices": k, "pair_sum_lower": q,
                       "margin_above_all_codegrees_9": margin,
                       "high_pairs_lower_if_codegrees_at_most_13": (margin + 3) // 4})
    roots = []
    for m, color, c in ((m, color, c) for m in range(214, 221)
                         for color in ("red", "blue") for c in range(10, 14)):
        roots.append({"M": m, "red_edges": 231 + m, "pair_color": color,
                      "codegree": c, "cell_sizes": [c, 20 - c, 20 - c, c + 1],
                      "common_core_types_imported": CORE_COUNTS[c],
                      "free_edges_after_pinning_common_core": 820 - comb(c, 2)})
    return {"schema": 1, "bounds": bounds, "scalar_roots": roots}


def payload():
    return (json.dumps(certificate(), sort_keys=True, indent=2) + "\n").encode()


def report():
    obj = certificate()
    return {"bounds_checked": len(obj["bounds"]),
            "threshold_15_pair_sum": lower_bound(43, 15),
            "threshold_15_all_at_most_9": 9 * comb(15, 2),
            "hard_branch_exact_anchors_at_least": 22,
            "hard_branch_high_pairs_at_least": 16,
            "scalar_roots": len(obj["scalar_roots"]),
            "coarse_core_templates_conditional_on_catalogs":
                sum(row["common_core_types_imported"] for row in obj["scalar_roots"]),
            "certificate_sha256": hashlib.sha256(payload()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    if args.write:
        args.write.write_bytes(payload())
    print(json.dumps(report(), sort_keys=True, indent=2))
