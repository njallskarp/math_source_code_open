#!/usr/bin/env python3
"""Independent degree-moment and literal common-neighbor checks.

No import from build.py. The scalar bound is recovered by balancing integer
degree lists at every possible internal edge total, not by Gram matrices.
"""
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def minimum_pairs(total, count):
    lo, high_count = divmod(total, count)
    return (count - high_count) * comb(lo, 2) + high_count * comb(lo + 1, 2)


def degree_relaxation(k):
    vals = []
    outside = 43 - k
    for edges in range(comb(k, 2) + 1):
        crossing = 21 * k - 2 * edges
        if not 0 <= crossing <= k * outside:
            continue
        vals.append(minimum_pairs(2 * edges, k) + minimum_pairs(crossing, outside)
                    - comb(k, 2) + edges)
    return min(vals)


def expected_certificate():
    bounds = []
    for k in range(15, 43):
        value = degree_relaxation(k)
        margin = value - 9 * comb(k, 2)
        need(margin > 0, "codegree-ten implication lost")
        bounds.append({"balanced_vertices": k, "pair_sum_lower": value,
                       "margin_above_all_codegrees_9": margin,
                       "high_pairs_lower_if_codegrees_at_most_13": -((-margin) // 4)})
    roots = []
    counts = {10: 313, 11: 105, 12: 12, 13: 1}
    for M in range(214, 221):
        for color in ("red", "blue"):
            for c in range(10, 14):
                cells = [c, 21 - 1 - c, 21 - 1 - c, 41 - (42 - 2 - c)]
                need(sum(cells) == 41, "cell count")
                free = comb(43, 2) - (2 * 42 - 1) - comb(c, 2)
                roots.append({"M": M, "red_edges": 231 + M, "pair_color": color,
                              "codegree": c, "cell_sizes": cells,
                              "common_core_types_imported": counts[c],
                              "free_edges_after_pinning_common_core": free})
    return {"schema": 1, "bounds": bounds, "scalar_roots": roots}


def validate(data):
    need(data == expected_certificate(), "certificate differs from independent reconstruction")


def pair_codegree(a, u, v):
    color = v in a[u]
    return sum(w != u and w != v and ((w in a[u]) == color)
               and ((w in a[v]) == color) for w in range(len(a)))


def moment_audit(a, chosen):
    n, k = len(a), len(chosen)
    need(all(len(a[v]) == (n - 1) // 2 for v in chosen), "nonbalanced candidate")
    literal = sum(pair_codegree(a, u, v) for u, v in combinations(chosen, 2))
    incidence = [sum(v in a[w] for v in chosen) for w in range(n)]
    internal = sum(v in a[u] for u, v in combinations(chosen, 2))
    need(literal == sum(comb(x, 2) for x in incidence) - comb(k, 2) + internal,
         "literal pair sum differs from degree moments")
    return literal


def small_graphs():
    graphs = subsets = pairs = 0
    for n in (1, 3, 5):
        edges = list(combinations(range(n), 2))
        for mask in range(1 << len(edges)):
            a = [set() for _ in range(n)]
            for i, (u, v) in enumerate(edges):
                if mask >> i & 1:
                    a[u].add(v)
                    a[v].add(u)
            balanced = [v for v in range(n) if len(a[v]) == (n - 1) // 2]
            for bits in range(1 << len(balanced)):
                chosen = [v for i, v in enumerate(balanced) if bits >> i & 1]
                moment_audit(a, chosen)
                subsets += 1
                pairs += comb(len(chosen), 2)
            graphs += 1
    # The Paley graph on 13 vertices has degree six, and every edge in either
    # color has exactly two common neighbors: a nonvacuous equality control.
    residues = {x * x % 13 for x in range(1, 13)}
    a = [{v for v in range(13) if (v - u) % 13 in residues} for u in range(13)]
    need(all(pair_codegree(a, u, v) == 2 for u, v in combinations(range(13), 2)),
         "Paley equality control")
    for bits in range(1 << 13):
        chosen = [v for v in range(13) if bits >> v & 1]
        moment_audit(a, chosen)
        subsets += 1
        pairs += comb(len(chosen), 2)
    return graphs + 1, subsets, pairs


def transport_audit(a, u, v):
    color = v in a[u]
    cells = [[], [], [], []]
    for w in range(43):
        if w in (u, v):
            continue
        left, right = (w in a[u]) == color, (w in a[v]) == color
        index = 0 if left and right else 1 if left else 2 if right else 3
        cells[index].append(w)
    c = len(cells[0])
    need(list(map(len, cells)) == [c, 20 - c, 20 - c, c + 1], "root cells")
    order = [u, v] + [w for cell in cells for w in reversed(cell)]
    transported = [[order[j] in a[order[i]] for j in range(43)] for i in range(43)]
    fixed, free = {}, {}
    for i, j in combinations(range(43), 2):
        if i < 2:
            if (i, j) == (0, 1):
                same = True
            else:
                pos = j - 2
                same = pos < c or (i == 0 and c <= pos < 20) or (i == 1 and 20 <= pos < 40 - c)
            fixed[i, j] = color if same else not color
        elif j < 2 + c:
            fixed[i, j] = transported[i][j]
        else:
            free[i, j] = transported[i][j]
    need(len(free) == 820 - comb(c, 2), "missing shared edge")
    rebuilt = dict(fixed)
    rebuilt.update(free)
    need(all(rebuilt[i, j] == transported[i][j] for i, j in combinations(range(43), 2)),
         "physical edge lift mismatch")
    need(sum(rebuilt.values()) == 446, "red M changed under pair-color normalization")
    return "red" if color else "blue", c


def fixture_audit():
    data = json.loads((HERE / "fixture.json").read_text())
    a = [set(row) for row in data["red_adjacency"]]
    need(len(a) == 43 and all(v not in a[v] for v in range(43)), "fixture graph order/loops")
    need(all((v in a[u]) == (u in a[v]) for u in range(43) for v in range(43)), "asymmetry")
    need(list(map(len, a)) == [19] + [20] * 9 + [21] * 33, "fixture degree profile")
    balanced = list(range(10, 43))
    for k in range(15, 34):
        got = moment_audit(a, balanced[:k])
        need(got >= degree_relaxation(k), "degree relaxation violated")
    tally = Counter()
    for u, v in combinations(balanced, 2):
        c = pair_codegree(a, u, v)
        if 10 <= c <= 13:
            tally[transport_audit(a, u, v)] += 1
    need(set(tally) == set(product(("red", "blue"), range(10, 14))), "missing color/codegree control")
    # Establish explicitly that this fixture is outside the Ramsey theorem's
    # domain, even though all its degrees and the edge total are correct.
    bad = next((list(s) for s in combinations(range(43), 5)
                if sum(v in a[u] for u, v in combinations(s, 2)) in (0, 10)), None)
    need(bad is not None, "fixture scope control missing")
    return {f"{color}_{c}": tally[color, c] for color, c in sorted(tally)}, bad


if __name__ == "__main__":
    data = json.loads((HERE / "certificate.json").read_text())
    validate(data)
    rejected = 0
    for field in ("bounds", "scalar_roots"):
        mutated = json.loads(json.dumps(data))
        mutated[field].pop()
        try:
            validate(mutated)
        except ValueError:
            rejected += 1
    mutated = json.loads(json.dumps(data))
    mutated["scalar_roots"][4]["red_edges"] = 903 - mutated["scalar_roots"][4]["red_edges"]
    try:
        validate(mutated)
    except ValueError:
        rejected += 1
    need(rejected == 3, "mutated certificate accepted")
    graphs, subsets, pairs = small_graphs()
    transport, bad = fixture_audit()
    print(json.dumps({"bounds_matched": 28, "scalar_roots_matched": 56,
                      "small_graphs": graphs, "balanced_subsets": subsets,
                      "literal_pair_checks": pairs, "transport_counts": transport,
                      "fixture_monochromatic_five_set": bad, "mutations_rejected": rejected,
                      "certificate_sha256": hashlib.sha256((HERE / "certificate.json").read_bytes()).hexdigest()},
                     sort_keys=True, indent=2))
