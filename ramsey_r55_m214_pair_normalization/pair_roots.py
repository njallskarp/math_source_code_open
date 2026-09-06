#!/usr/bin/env python3
"""Complete marked pair-incidence roots, not a search or a Ramsey witness."""

import argparse
import hashlib
import itertools
import json
import sys

CELLS = "HABO"
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")
HEADER = "family\tc\tk\tpattern\tE_cells\tC_cells\tanomalies\troot_sha256"


def require(value, message):
    if not value:
        raise ValueError(message)


def definitions():
    for family in FAMILIES:
        for c in range(9, 14):
            for k in range(7):
                e = (k, 6-k, 6-k, 1+k)
                central = (c-k, 14-c+k, 14-c+k, c-k)
                options = {
                    "E8": ("H", "A"), "E77": ("BB", "BO", "OO"),
                    "C8": ("B", "O"), "C77": ("BB", "BO", "OO"),
                    "C77partition": ("HO", "AB"),
                }[family]
                sizes = e if family.startswith("E") else central
                for pattern in options:
                    if all(pattern.count(cell) <= sizes[i]
                           for i, cell in enumerate(CELLS)):
                        yield family, c, k, pattern


def root(family, c, k, pattern):
    require((family, c, k, pattern) in set(definitions()), "invalid root key")
    e = (k, 6-k, 6-k, 1+k)
    central = (c-k, 14-c+k, 14-c+k, c-k)
    cells = []
    cursor = 2
    for size in e + central:
        cells.append(list(range(cursor, cursor + size)))
        cursor += size
    require(cursor == 43, "cell partition")
    anomaly_class = 0 if family.startswith("E") else 4
    anomalies = []
    for i, name in enumerate(CELLS):
        anomalies.extend(cells[anomaly_class+i][:pattern.count(name)])
    excess = 2 if family in ("E8", "C8") else 1
    units = [[0, 1, 1]]
    bits = ((1, 1), (1, 0), (0, 1), (0, 0))
    for i, cell in enumerate(cells):
        for vertex in cell:
            units.extend([[0, vertex, bits[i % 4][0]],
                          [1, vertex, bits[i % 4][1]]])
    units.sort()
    # Anomaly-status refinement is essential: sorting may not move a named
    # anomalous vertex to a position constrained to have a=6.
    buckets = []
    for cell in cells:
        for status in (0, 1):
            bucket = [v for v in cell if int(v in anomalies) == status]
            if bucket:
                buckets.append(bucket)
    partition = None
    if family == "C77partition":
        p, q = anomalies
        partition = {"blue_pair": [p, q],
                     "one_red_to_pair": [0, 1] + [
                         v for v in range(15, 43) if v not in anomalies]}
    return {
        "key": [family, c, k, pattern],
        "E_cells": list(e), "C_cells": list(central),
        "anchors": [0, 1], "E": list(range(2, 15)),
        "cells": cells, "anomalies": anomalies,
        "edge_units": units,
        "a_equalities": [[v, 6 + (excess if v in anomalies else 0)]
                         for v in range(43)],
        "partition": partition,
        "ordering_buckets": buckets,
    }


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def table():
    lines = [HEADER]
    for key in definitions():
        record = root(*key)
        fields = [*map(str, key),
                  ",".join(map(str, record["E_cells"])),
                  ",".join(map(str, record["C_cells"])),
                  ",".join(map(str, record["anomalies"])),
                  hashlib.sha256(canonical_bytes(record)).hexdigest()]
        lines.append("\t".join(fields))
    return "\n".join(lines) + "\n"


def normalize_adorned(adj, e_vertices, anomalies, u, v, family):
    """Relabel a supplied eligible adorned graph; does NOT certify eligibility.

    Preconditions are the theorem's branch/anchor hypotheses. This helper
    validates the pair-incidence projection, transports all edges, and sorts
    only in the proved residual buckets. It does not check degrees, triangles,
    or all K5 constraints. Callers must not use it as a Ramsey-graph checker.
    """
    n = len(adj)
    require(n == 43 and all(len(row) == n for row in adj), "matrix shape")
    require(all(adj[i][i] == 0 for i in range(n)), "diagonal")
    require(all(adj[i][j] in (0, 1) and adj[i][j] == adj[j][i]
                for i in range(n) for j in range(n)), "simple adjacency")
    e_vertices = set(e_vertices)
    anomalies = set(anomalies)
    require(len(e_vertices) == 13 and all(vv in range(n) for vv in e_vertices),
            "E class")
    require(u in range(n) and v in range(n) and u != v and adj[u][v] == 1,
            "anchor edge")
    require(u not in e_vertices and v not in e_vertices
            and u not in anomalies and v not in anomalies, "exact anchors")
    require(family in FAMILIES, "family")
    require(len(anomalies) == (1 if family in ("E8", "C8") else 2),
            "anomaly count")
    require(all(vv in range(n) for vv in anomalies), "anomaly vertices")
    require(all((vv in e_vertices) == family.startswith("E")
                for vv in anomalies), "anomaly class")
    if family == "C77partition":
        p, q = sorted(anomalies)
        require(adj[p][q] == 0 and all(
            adj[w][p] + adj[w][q] == 1
            for w in range(n) if w not in e_vertices and w not in anomalies),
            "universal C77 partition")
    bit_index = {(1, 1): 0, (1, 0): 1, (0, 1): 2, (0, 0): 3}
    old_cells = [[] for _ in range(8)]
    for w in range(n):
        if w not in (u, v):
            old_cells[(0 if w in e_vertices else 4)
                      + bit_index[adj[u][w], adj[v][w]]].append(w)
    c = len(old_cells[0]) + len(old_cells[4])
    k = len(old_cells[0])
    pattern = "".join(CELLS[i % 4] * len(set(cell) & anomalies)
                      for i, cell in enumerate(old_cells))
    # HABO cell order gives AB or HO for the partition case, as documented.
    record = root(family, c, k, pattern)
    require([len(cell) for cell in old_cells]
            == record["E_cells"] + record["C_cells"], "pair degree margins")
    old_buckets = []
    for cell in old_cells:
        for status in (0, 1):
            bucket = [w for w in cell if int(w in anomalies) == status]
            if bucket:
                old_buckets.append(bucket)
    permutation = {u: 0, v: 1}
    for old_bucket, new_bucket in zip(old_buckets, record["ordering_buckets"]):
        def signature(w):
            return tuple(sum(adj[w][z] for z in bucket) for bucket in old_buckets)
        for old, new in zip(sorted(old_bucket, key=lambda w: (signature(w), w)),
                            new_bucket):
            permutation[old] = new
    require(set(permutation) == set(range(n))
            and set(permutation.values()) == set(range(n)), "bijection")
    normalized = [[0] * n for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        normalized[permutation[i]][permutation[j]] = adj[i][j]
        normalized[permutation[j]][permutation[i]] = adj[i][j]
    return record, permutation, normalized


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", nargs=4, metavar=("FAMILY", "C", "K", "PATTERN"))
    args = parser.parse_args()
    if args.root:
        family, c, k, pattern = args.root
        sys.stdout.buffer.write(canonical_bytes(root(family, int(c), int(k), pattern)))
    else:
        sys.stdout.write(table())


if __name__ == "__main__":
    main()
