"""Independent verification by literal five-set sums, with no quotient formulas.

This module does not import the producer, its graph decoder, or its checker.
"""
import base64
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def insist(value, message):
    if not value:
        raise ValueError(message)


def decode(text):
    raw = base64.b64decode(text, validate=True)
    n = raw[0] - 63
    payload = "".join(f"{c-63:06b}" for c in raw[1:])
    insist(0 <= n < 63 and len(payload) == 6*((n*(n-1)//2+5)//6), "graph6 length")
    insist(all(63 <= c <= 126 for c in raw[1:]), "graph6 alphabet")
    insist(set(payload[n*(n-1)//2:]) <= {"0"}, "padding")
    return [set(j for j in range(n) if j != i and
                payload[max(i,j)*(max(i,j)-1)//2 + min(i,j)] == "1")
            for i in range(n)]


def run(data):
    red_core = decode(data["red_core_parent_graph6_base64"])
    blue_core = decode(data["blue_core_graph6_base64"])
    insist(len(red_core) == 22 and len(blue_core) == 20, "core orders")
    for u,v in data["red_core_delete_edges"]:
        red_core[u].remove(v)
        red_core[v].remove(u)
    adj = [set() for _ in range(43)]
    for u in range(43):
        for v in range(u+1,43):
            if u == 0:
                red = v <= 22
            elif v <= 22:
                red = v-1 in red_core[u-1]
            elif u >= 23:
                red = v-23 not in blue_core[u-23]
            else:
                red = data["cross_rows"][u-1][v-23] == "1"
            if red:
                adj[u].add(v)
                adj[v].add(u)
    roots = [0,3,9]
    insist(data["anchors"] == roots, "root labels")
    labels = [8+roots.index(v) if v in roots else int("".join("1" if v in adj[r] else "0" for r in roots),2)
              for v in range(43)]
    insist(Counter(labels) == Counter(dict(enumerate([6,4,4,6,5,6,6,3,1,1,1]))), "cells")
    insist(Counter(map(len,adj)) == Counter({20:8,21:26,22:9}), "degree profile")
    neighborhoods = []
    local = []
    for r in roots:
        for color in (1,0):
            vertices = sorted(adj[r] if color else set(range(43)) - adj[r] - {r})
            for four in combinations(vertices,4):
                insist(any(int(v in adj[u]) != color for u,v in combinations(four,2)), "local monochromatic K4")
            neighborhoods.append((set(vertices),1-color))
            local.append([r,color,len(vertices),sum(int(v in adj[u]) == color for u,v in combinations(vertices,2))])
    grouped = defaultdict(lambda: [0,0,0,0])
    all_defects = Counter()
    for subset in combinations(range(43),5):
        number = sum(v in adj[u] for u,v in combinations(subset,2))
        pattern = tuple(sorted(labels[v] for v in subset))
        row = grouped[pattern]
        row[0] += 1
        row[1] += number
        if number in (0,10):
            row[2 if number == 10 else 3] += 1
            insist(not (set(subset) & set(roots)), "no anchored global defect")
            for neighborhood,color in neighborhoods:
                insist(not (set(subset) <= neighborhood and number == 10*color), "local opposite K5")
            all_defects["red" if number else "blue"] += 1
    for pattern,(n,total,_r,_b) in grouped.items():
        insist(n <= total <= 9*n, "expected K5 clauses")
    text = "".join(f"{','.join(map(str,p))}|{row[0]}|{row[1]}\n" for p,row in sorted(grouped.items()))
    digest = sha256(text.encode()).hexdigest()
    insist(digest == "0fd57a5b7956be05b42c016062f8065d380b944b9657a1e9d0d805490d5e94c6", "entry-level average agreement")
    edges = "".join(f"{u} {v}\n" for u in range(43) for v in sorted(adj[u]) if u<v)
    edge_digest = sha256(edges.encode()).hexdigest()
    insist(edge_digest == "1a976bedb69fa94cdf0500e4087bf4e395585812c298b3095794468e004b279f", "same seed")
    # These original defect patterns pinpoint the missing joint events.
    events = []
    for pattern,color in [((1,2,4,4,7),"red"), ((3,5,5,6,7),"blue")]:
        row = grouped[pattern]
        defects = row[2 if color == "red" else 3]
        insist(defects > 0, "positive forbidden event")
        events.append({"pattern":list(pattern),"color":color,"sets":row[0],"defects":defects,
                       "mean_red_edges":str(Fraction(row[1],row[0])),
                       "monochromatic_probability":str(Fraction(defects,row[0]))})
    return {"status":"PASS_LITERAL_FIVE_SET_AVERAGES", "five_sets":sum(row[0] for row in grouped.values()),
            "five_set_patterns":len(grouped),"pattern_average_sha256":digest,
            "seed_edge_sha256":edge_digest,"local_profiles":local,"seed_defects":dict(sorted(all_defects.items())),
            "omitted_joint_events":events}


if __name__ == "__main__":
    source = json.loads((Path(__file__).resolve().parent / "SEED.json").read_text())
    print(json.dumps(run(source),indent=2,sort_keys=True))
