#!/usr/bin/env python3
"""Independent checks for the R(5,5) neighbourhood-edge reduction.

The exact-arithmetic and small-case checks use only the Python standard
library.  ``--catalogue-dir`` additionally uses NetworkX's graph6 parser so
that the catalogue decoding does not share code with the reviewed program.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path


EMAX = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
EXPECTED = {
    43: [((18, 24), 212, 5), ((19, 23), 205, 9),
         ((20, 22), 200, 14), ((21, 21), 99, 8)],
    44: [((19, 24), 218, 6), ((20, 23), 212, 10),
         ((21, 22), 209, 12)],
    45: [((20, 24), 225, 7), ((21, 23), 221, 8),
         ((22, 22), 109, 5)],
}
EXTREME_FILES = [
    (18, 50), (18, 85), (19, 57), (19, 92), (20, 68), (20, 100),
    (21, 77), (21, 107), (22, 88), (22, 114), (23, 101), (23, 122),
]
ARCHIVE_SHA256 = "9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6"
ORDER24_SHA256 = "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"
ORDER24_TAIL = {116: 9, 117: 90, 118: 806, 119: 4358,
                129: 147, 130: 32, 131: 3, 132: 2}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def edge_count(mask: int) -> int:
    return mask.bit_count()


def graph_from_mask(n: int, mask: int) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for bit, (u, v) in enumerate(combinations(range(n), 2)):
        if mask >> bit & 1:
            adj[u].add(v)
            adj[v].add(u)
    return adj


def check_counting_identity(max_order: int = 6) -> dict[str, int]:
    graphs = vertex_cases = 0
    for n in range(max_order + 1):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = graph_from_mask(n, mask)
            degree = [len(a) for a in adj]
            e = edge_count(mask)
            sum_s = 0
            for v in range(n):
                neighbourhood = adj[v]
                outside = set(range(n)) - neighbourhood - {v}
                e_n = sum(u in adj[w] for w, u in combinations(neighbourhood, 2))
                e_m = sum(u in adj[w] for w, u in combinations(outside, 2))
                s_v = sum(degree[u] for u in neighbourhood)
                require(e_m == e + e_n - s_v,
                        f"local identity failed at n={n}, mask={mask}, v={v}")
                sum_s += s_v
                vertex_cases += 1
            require(sum_s == sum(d * d for d in degree),
                    f"summed identity failed at n={n}, mask={mask}")
            graphs += 1
    return {"graphs": graphs, "vertex_cases": vertex_cases, "max_order": max_order}


def integer_below(value: Fraction) -> int:
    """Largest integer strictly below value."""
    return (value.numerator - 1) // value.denominator


def reduction_checks() -> dict[str, object]:
    rows = []
    slack = {}
    for n, expected_rows in EXPECTED.items():
        got = []
        gaps = []
        for (d, m), expected_cap, expected_drop in expected_rows:
            require(d + m == n - 1, f"bad degree pair {(d, m)} for n={n}")
            rhs = Fraction(d * d) - Fraction(n * d, 2) + comb(m, 2)
            pair_cap = integer_below(rhs)
            unconditional_pair = EMAX[d] + EMAX[m]
            gap = Fraction(unconditional_pair) - rhs
            gaps.append(gap)
            if d == m:
                cap = pair_cap // 2
                drop = EMAX[d] - cap
                label = f"beta({d})"
            else:
                cap = pair_cap
                drop = unconditional_pair - cap
                label = f"beta({d})+beta({m})"
            require((cap, drop) == (expected_cap, expected_drop),
                    f"cap mismatch for n={n}, pair={(d, m)}")
            got.append({"term": label, "cap": cap, "drop": drop,
                        "strict_rhs": str(rhs)})
        slack[str(n)] = {
            "aggregate_at_least": str(n * min(gaps)),
            "worst_per_vertex": str(max(gaps)),
        }
        rows.extend({"n": n, **item} for item in got)
    require(slack == {
        "43": {"aggregate_at_least": "172", "worst_per_vertex": "29/2"},
        "44": {"aggregate_at_least": "220", "worst_per_vertex": "11"},
        "45": {"aggregate_at_least": "270", "worst_per_vertex": "8"},
    }, "unconditional slack mismatch")
    return {"conditional_caps": rows, "unconditional_slack": slack}


def is_good(adj: list[set[int]], clique: int, independent: int) -> bool:
    vertices = range(len(adj))
    for chosen in combinations(vertices, clique):
        if all(v in adj[u] for u, v in combinations(chosen, 2)):
            return False
    for chosen in combinations(vertices, independent):
        if all(v not in adj[u] for u, v in combinations(chosen, 2)):
            return False
    return True


def exact_bounds(clique: int, independent: int, max_order: int) -> dict[int, tuple[int, int]]:
    bounds = {}
    for n in range(max_order + 1):
        values = []
        for mask in range(1 << comb(n, 2)):
            adj = graph_from_mask(n, mask)
            if is_good(adj, clique, independent):
                values.append(edge_count(mask))
        if values:
            bounds[n] = (min(values), max(values))
    return bounds


def corrected_small_case() -> dict[str, object]:
    # In a (3,4,n)-graph, N(v) is (2,4) and M(v) is (3,3).
    n_bounds = exact_bounds(2, 4, 3)
    m_bounds = exact_bounds(3, 3, 5)
    verdicts = {}
    coefficients = {}
    for n in range(4, 10):
        admissible = [d for d in n_bounds if n - 1 - d in m_bounds]
        coeff = {
            str(d): Fraction(d * d - n_bounds[d][1] + m_bounds[n - 1 - d][0])
                    - Fraction(n * d, 2)
            for d in admissible
        }
        coefficients[str(n)] = {d: str(c) for d, c in coeff.items()}
        verdicts[str(n)] = "contradiction" if coeff and all(c > 0 for c in coeff.values()) else "no contradiction"
    require(all(verdicts[str(n)] == "no contradiction" for n in range(4, 9)),
            "correct reduction falsely excludes an existing (3,4,n)-graph")
    require(verdicts["9"] == "contradiction", "correct reduction did not exclude n=9")
    require(coefficients["9"] == {"3": "1/2"}, "unexpected n=9 coefficient")
    return {
        "neighbourhood_bounds_2_4": n_bounds,
        "outside_bounds_3_3": m_bounds,
        "coefficients": coefficients,
        "verdicts": verdicts,
        "note": "The correctly specialized reduction excludes n=9 with coefficient 1/2.",
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def direct_goodness(graph) -> bool:
    nodes = tuple(graph)
    adj = {u: set(graph[u]) for u in nodes}
    for chosen in combinations(nodes, 4):
        if all(v in adj[u] for u, v in combinations(chosen, 2)):
            return False
    for chosen in combinations(nodes, 5):
        if all(v not in adj[u] for u, v in combinations(chosen, 2)):
            return False
    return True


def catalogue_checks(root: Path) -> dict[str, object]:
    import networkx as nx

    archive = root / "r45extreme.tar.gz"
    order24 = root / "r45_24.g6"
    extreme_root = root / "r45extreme"
    require(sha256(archive) == ARCHIVE_SHA256, "extreme archive hash mismatch")
    require(sha256(order24) == ORDER24_SHA256, "order-24 catalogue hash mismatch")

    extreme_summary = []
    endpoint_graphs = 0
    for n, edges in EXTREME_FILES:
        path = extreme_root / f"r45{n}.{edges}.g6"
        count = 0
        with path.open("rb") as handle:
            for line in handle:
                graph = nx.from_graph6_bytes(line.rstrip())
                require(len(graph) == n, f"order mismatch in {path.name}")
                require(graph.number_of_edges() == edges,
                        f"edge-count mismatch in {path.name}")
                require(direct_goodness(graph), f"non-Ramsey graph in {path.name}")
                count += 1
        endpoint_graphs += count
        extreme_summary.append({"file": path.name, "graphs": count, "bad": 0})

    distribution = Counter()
    endpoint24_good = 0
    with order24.open("rb") as handle:
        for line in handle:
            graph = nx.from_graph6_bytes(line.rstrip())
            require(len(graph) == 24, "order mismatch in r45_24.g6")
            edges = graph.number_of_edges()
            distribution[edges] += 1
            if edges in (116, 132):
                require(direct_goodness(graph),
                        f"non-Ramsey endpoint graph in r45_24.g6 at {edges} edges")
                endpoint24_good += 1
    require(sum(distribution.values()) == 352_366, "order-24 row-count mismatch")
    require(min(distribution) == 116 and max(distribution) == 132,
            "order-24 edge-range mismatch")
    require({e: distribution[e] for e in ORDER24_TAIL} == ORDER24_TAIL,
            "order-24 tail mismatch")
    require(endpoint24_good == 11, "order-24 endpoint count mismatch")
    return {
        "python": sys.version.split()[0],
        "networkx": nx.__version__,
        "archive_sha256": ARCHIVE_SHA256,
        "order24_sha256": ORDER24_SHA256,
        "extreme_files": extreme_summary,
        "extreme_graphs_checked_definitionally": endpoint_graphs,
        "order24_graphs_parsed": sum(distribution.values()),
        "order24_range": [min(distribution), max(distribution)],
        "order24_tail": dict(sorted(ORDER24_TAIL.items())),
        "order24_endpoint_graphs_checked_definitionally": endpoint24_good,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--catalogue-dir", type=Path,
        help="directory containing r45extreme.tar.gz, extracted r45extreme/, and r45_24.g6",
    )
    args = parser.parse_args()
    result = {
        "counting_identity": check_counting_identity(),
        "reduction": reduction_checks(),
        "corrected_3_4_test": corrected_small_case(),
    }
    if args.catalogue_dir:
        result["catalogues"] = catalogue_checks(args.catalogue_dir)
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(json.dumps(result, indent=2, sort_keys=True))
    print("certificate_sha256", hashlib.sha256(canonical.encode()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
