#!/usr/bin/env python3
"""Separate core/column construction and Menger vertex-flow audit.

Imports no producer and enumerates no deletions. Instead, it proves each
graph minus its degree-five vertex is six-connected. Its only cut of size
at most five must therefore be that vertex's complete neighborhood.
"""
import hashlib
import json
from collections import deque
from itertools import combinations, product
from pathlib import Path


def insist(ok, message):
    if not ok:
        raise ValueError(message)


def unpack(s):
    insist(isinstance(s, str) and len(s) > 0, "empty encoding")
    vals = [ord(c) - 63 for c in s]
    insist(all(0 <= x < 64 for x in vals) and vals[0] < 63, "invalid encoding")
    n = vals[0]
    count = n * (n - 1) // 2
    insist(len(vals) == 1 + (count + 5) // 6, "invalid length")
    packed = 0
    for v in vals[1:]:
        packed = packed * 64 + v
    padding = 6 * (len(vals) - 1) - count
    insist(packed % (1 << padding) == 0, "invalid padding")
    packed >>= padding
    matrix = [[False] * n for _ in range(n)]
    for w in range(n - 1, -1, -1):
        for v in range(w - 1, -1, -1):
            matrix[v][w] = matrix[w][v] = bool(packed % 2)
            packed //= 2
    insist(packed == 0, "unused graph bits")
    return matrix


def reconstruct(data, rep):
    core = unpack(data["cores"][rep["core"]])
    insist(len(core) == 16, "wrong core order")
    mat = [[False] * 22 for _ in range(22)]
    for v in range(16):
        for w in range(16):
            mat[v][w] = core[v][w]
    insist(len(rep["columns"]) == 5, "wrong column count")
    for i, column in enumerate(rep["columns"]):
        insist(type(column) is int and 0 <= column < 65536, "invalid column")
        for a in range(16):
            mat[a][16 + i] = mat[16 + i][a] = bool(column & (1 << a))
        mat[21][16 + i] = mat[16 + i][21] = True
    for v, w in data["types"][str(rep["type"])]:
        insist(0 <= v < w < 5, "invalid neighbor-graph edge")
        mat[16 + v][16 + w] = mat[16 + w][16 + v] = True
    return mat


def has_clique(rows, allowed, size):
    if size == 0:
        return True
    while allowed.bit_count() >= size:
        bit = allowed & -allowed
        allowed ^= bit
        if has_clique(rows, allowed & rows[bit.bit_length() - 1], size - 1):
            return True
    return False


def paths(mat, source, target, limit):
    """Integral flow capped at limit, for nonadjacent terminals.

    Split vertices in/out, with internal capacity one. Terminals and
    original undirected edges have capacity n. Augment by one each time.
    """
    n = len(mat)
    insist(source != target and not mat[source][target], "nonadjacent terminals required")
    residual = [[0] * (2 * n) for _ in range(2 * n)]
    for v in range(n):
        residual[2 * v][2 * v + 1] = n if v in (source, target) else 1
        for w in range(n):
            if mat[v][w]:
                residual[2 * v + 1][2 * w] = n
    start, end = 2 * source + 1, 2 * target
    total = 0
    while total < limit:
        parent = [-1] * (2 * n)
        parent[start] = start
        queue = deque([start])
        while queue and parent[end] == -1:
            v = queue.popleft()
            for w in range(2 * n):
                if parent[w] == -1 and residual[v][w] > 0:
                    parent[w] = v
                    queue.append(w)
        if parent[end] == -1:
            break
        w = end
        while w != start:
            v = parent[w]
            residual[v][w] -= 1
            residual[w][v] += 1
            w = v
        total += 1
    return total


def component_audit():
    bounds = [0, 3, 8, 17]
    profiles = set()
    for number in range(2, 5):
        for alphas in product(range(1, 4), repeat=number):
            if sum(alphas) > 4 or sum(bounds[a] for a in alphas) < 17:
                continue
            insist(sorted(alphas) == [1, 3], "unexpected independence partition")
            for sizes in product(*(range(1, bounds[a] + 1) for a in alphas)):
                s = 22 - sum(sizes)
                if 0 <= s <= 5:
                    profiles.add((s, sizes[alphas.index(3)], sizes[alphas.index(1)]))
    # Direct exhaustion of local B--S incidences with degree >= 6 on B.
    for s, a, b in profiles:
        masks = [m for m in range(1 << s) if m.bit_count() + b - 1 >= 6]
        for columns in product(masks, repeat=b):
            if b == 3 and (columns[0] & columns[1] & columns[2]):
                continue  # A common S vertex with the red B triangle is K4.
            insist(b == 2 and s == 5 and columns == (31, 31),
                    "unhandled degree-six local case")
            # Any red S edge gives K4 with B; no red S edge gives I5.
            pairs = list(combinations(range(2, 7), 2))
            for edge_mask in range(1 << 10):
                edges = {(0, 1)} | {(v, w) for v in (0, 1) for w in range(2, 7)}
                edges.update(p for j, p in enumerate(pairs) if edge_mask >> j & 1)
                forbidden = any(all((p in edges) == red for p in combinations(c, 2))
                                for k, red in ((4, True), (5, False))
                                for c in combinations(range(7), k))
                insist(forbidden, "local forbidden-set failure")
    return [list(p) for p in sorted(profiles)]


def check(data):
    insist(len(data["representatives"]) == 13, "wrong imported family size")
    records = []
    for i, rep in enumerate(data["representatives"]):
        mat = reconstruct(data, rep)
        degrees = [sum(row) for row in mat]
        insist(degrees[21] == 5 and min(degrees[:21]) >= 9, "degree gap failed")
        for red, k in ((True, 4), (False, 5)):
            rows = [sum(1 << w for w in range(22) if w != v and mat[v][w] == red)
                    for v in range(22)]
            insist(not has_clique(rows, (1 << 22) - 1, k), "forbidden clique")
        hubless = [row[:21] for row in mat[:21]]
        for v, w in combinations(range(21), 2):
            if not hubless[v][w]:
                insist(paths(hubless, v, w, 6) == 6, "hubless connectivity failed")
        edges = [[v, w] for v in range(22) for w in range(v + 1, 22) if mat[v][w]]
        insist(len(edges) == 109, "wrong density")
        raw = (json.dumps(edges, separators=(",", ":")) + "\n").encode()
        records.append({"id": i, "edge_sha256": hashlib.sha256(raw).hexdigest(),
                        "degree_sequence": sorted(degrees),
                        "cuts": [[v for v in range(22) if mat[21][v]]]})
    return {"component_cases_s_a_b": component_audit(), "graphs": records,
            "classes": 13, "connectivity": 5, "five_cuts_per_graph": 1,
            "outside_edges_per_interface": 630}


if __name__ == "__main__":
    data = json.loads(Path(__file__).with_name("inputs.json").read_text())
    print(json.dumps(check(data), sort_keys=True, separators=(",", ":")))
