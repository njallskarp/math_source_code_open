"""Decode and check the compact height-2907 seed without a graph catalog."""
import base64
from collections import Counter
from hashlib import sha256
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph6(encoded):
    raw = base64.b64decode(encoded, validate=True)
    require(bool(raw), "empty graph6")
    n = raw[0] - 63
    require(0 <= n <= 62, "small graph6")
    size = n * (n - 1) // 2
    require(len(raw) == 1 + (size + 5) // 6, "graph6 length")
    bits = []
    for value in raw[1:]:
        require(63 <= value <= 126, "graph6 alphabet")
        bits.extend(((value - 63) >> i) & 1 for i in range(5, -1, -1))
    require(not any(bits[size:]), "graph6 padding")
    pairs = ((u, v) for v in range(n) for u in range(v))
    return n, {pair for pair, bit in zip(pairs, bits) if bit}


def construct(data):
    require(data["format"] == "r55-d22-three-anchor-survivor-v1", "format")
    require(data["anchors"] == [0, 3, 9], "anchors")
    n, red_core = graph6(data["red_core_parent_graph6_base64"])
    require(n == 22 and len(red_core) == 114, "red parent")
    deletions = [tuple(e) for e in data["red_core_delete_edges"]]
    require(len(deletions) == len(set(deletions)) == 6, "six distinct deletions")
    for pair in deletions:
        require(pair in red_core, "deleted red edge")
        red_core.remove(pair)
    n, blue_core = graph6(data["blue_core_graph6_base64"])
    require(n == 20 and len(blue_core) == 100, "blue core")
    rows = data["cross_rows"]
    require(len(rows) == 22 and all(len(r) == 20 and set(r) <= {"0", "1"} for r in rows), "cross matrix")
    red = {(0, v) for v in range(1, 23)}
    red.update((u + 1, v + 1) for u, v in red_core)
    red.update((u + 23, v + 23) for u, v in combinations(range(20), 2) if (u, v) not in blue_core)
    red.update((u + 1, v + 23) for u, row in enumerate(rows) for v, bit in enumerate(row) if bit == "1")
    return red


def audit(red):
    require(all(0 <= u < v < 43 for u, v in red), "edges")
    adjacency = [[False] * 43 for _ in range(43)]
    for u, v in red:
        adjacency[u][v] = adjacency[v][u] = True
    require(len(red) == 452, "452 edges")
    require(Counter(map(sum, adjacency)) == Counter({20: 8, 21: 26, 22: 9}), "degree profile")
    local = []
    for root in (0, 3, 9):
        for color in (True, False):
            vertices = [v for v in range(43) if v != root and adjacency[root][v] == color]
            count = sum(adjacency[u][v] == color for u, v in combinations(vertices, 2))
            for size, forbidden in ((4, color), (5, not color)):
                require(not any(all(adjacency[u][v] == forbidden for u, v in combinations(subset, 2))
                                for subset in combinations(vertices, size)), "local Ramsey condition")
            local.append([root, int(color), len(vertices), count])
    require(local == [[0,1,22,108],[0,0,20,100],[3,1,21,99],[3,0,21,96],[9,1,21,97],[9,0,21,97]], "local profiles")
    require(all(adjacency[u][v] for u, v in combinations((0,3,9), 2)), "anchor triangle")
    require([sum(adjacency[r][v] for v in range(1,23)) for r in (3,9)] == [10,10], "high partners")
    digest = sha256("".join(f"{u} {v}\n" for u,v in sorted(red)).encode()).hexdigest()
    require(digest == "1a976bedb69fa94cdf0500e4087bf4e395585812c298b3095794468e004b279f", "seed identity")
    return adjacency, local, digest
