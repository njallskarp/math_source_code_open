#!/usr/bin/env python3
"""Solver-free, exact audit of a joint-three / external-lifting separation."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


ORIGINAL_SHA256 = "21826676370f1bf4a974a7ea71b1e4fd786f254ce3878baa4841a88d323590cc"
CORE = tuple(range(11))
CORE_ROWS = (2046, 1, 1, 241, 361, 921, 1433, 1641, 1649, 1441, 961)
EXPECTED_SIGNATURES = (1,) * 8 + (2,) * 9 + (3,) * 4 + (4,) * 9 + (5,) * 4 + (6,) * 4 + (7,) * 2
DISPLAYED_U = (
    (1, 1, 1, 1, 1),
    (1, 2, 3, 4, 5),
    (1, 3, 6, 9, 14),
    (1, 4, 9, 18, 31),
    (1, 5, 14, 31, 62),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ramsey_table():
    u = [[1] * 6 for _ in range(6)]
    for p in range(2, 6):
        for q in range(2, 6):
            r, s = u[p - 1][q], u[p][q - 1]
            u[p][q] = r + s - int(r % 2 == 0 and s % 2 == 0)
    require(tuple(tuple(u[p][1:]) for p in range(1, 6)) == DISPLAYED_U, "Ramsey table")
    return u


def decode(data):
    require(set(data) == {"n", "red_rows", "gap"}, "fixture fields")
    n, rows = data["n"], data["red_rows"]
    require(type(n) is int and n == 43, "order")
    require(type(rows) is list and len(rows) == n, "row count")
    for v, row in enumerate(rows):
        require(type(row) is int and 0 <= row < 1 << n, "row type/range")
        require(not (row >> v) & 1, "loop")
    for a, b in itertools.combinations(range(n), 2):
        require((rows[a] >> b) & 1 == (rows[b] >> a) & 1, "asymmetry")
    # A set-of-pairs representation for the literal checks.
    edges = {(a, b) for a, b in itertools.combinations(range(n), 2) if rows[a] >> b & 1}
    return n, rows, edges


def pair(a, b):
    return (a, b) if a < b else (b, a)


def literal_clique(vertices, edges, red):
    return all((pair(a, b) in edges) == red for a, b in itertools.combinations(vertices, 2))


def literal_union(n, edges, a, b):
    return tuple(v for v in range(n) if v not in a and v not in b
                 and all(pair(v, w) in edges for w in a)
                 and all(pair(v, w) not in edges for w in b))


def bit_cliques(rows, size):
    """Enumerate clique masks by increasing-vertex adjacency intersections."""
    def visit(prefix, candidates, remaining):
        if remaining == 0:
            yield prefix
            return
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            yield from visit(prefix | bit, candidates & rows[vertex], remaining - 1)
    return set(visit(0, (1 << len(rows)) - 1, size))


def audit_gap(n, edges, gap, utable):
    require(set(gap) == {"A", "B", "u", "S", "T", "cap", "red_K5"}, "gap fields")
    for name in ("A", "B", "S", "T", "red_K5"):
        values = gap[name]
        require(type(values) is list and all(type(v) is int and 0 <= v < n for v in values),
                "gap vertex type/range")
        require(values == sorted(set(values)), "noncanonical vertex set")
    a, b, u = tuple(gap["A"]), tuple(gap["B"]), gap["u"]
    require(1 <= len(a) <= 3 and 1 <= len(b) <= 3, "mixed-root sizes")
    require(set(a + b) <= set(CORE) and not set(a) & set(b), "disjoint core roots")
    require(type(u) is int and 0 <= u < n and u not in CORE, "external vertex")
    require(literal_clique(a, edges, True) and literal_clique(b, edges, False), "root cliques")
    require(all(pair(u, v) in edges for v in a), "red antecedent")
    s = literal_union(n, edges, a, b)
    t = tuple(v for v in s if v != u and pair(u, v) in edges)
    require(list(s) == gap["S"] and list(t) == gap["T"], "exact S/T membership")
    require(u not in s, "genuinely external to S")
    cap = utable[4 - len(a)][5 - len(b)] - 1
    require(type(gap["cap"]) is int and gap["cap"] == cap and len(t) > cap, "strict lift violation")
    k5 = gap["red_K5"]
    require(len(k5) == 5 and literal_clique(k5, edges, True), "red K5 certificate")
    require(set(a) | {u} <= set(k5) and set(k5) - set(a) - {u} <= set(t), "lift obstruction")
    require(sum(v not in CORE for v in k5) == 4, "four-outside certificate")
    return {"A": list(a), "B": list(b), "u": u, "S": list(s), "T": list(t),
            "lhs": len(t), "rhs": cap, "u_in_S": u in s, "red_K5": k5}


def negative_controls(data, n, edges, utable):
    controls = 0
    malformed = []
    for field, value in (("n", 42), ("red_rows", data["red_rows"][:-1])):
        d = copy.deepcopy(data)
        d[field] = value
        malformed.append(d)
    for v, value in ((0, True), (0, 1 << 43), (0, data["red_rows"][0] | 1),
                     (0, data["red_rows"][0] ^ (1 << 1))):
        d = copy.deepcopy(data)
        d["red_rows"][v] = value
        malformed.append(d)
    for d in malformed:
        try:
            decode(d)
        except ValueError:
            controls += 1
        else:
            raise ValueError("malformed graph accepted")
    for field, value in (
        ("A", [0]), ("B", [1]), ("u", 20),
        ("S", data["gap"]["S"][:-1]), ("T", data["gap"]["T"][:-1]),
        ("cap", 9), ("cap", 10), ("red_K5", [1, 11, 13, 14, 37]),
        ("S", list(reversed(data["gap"]["S"]))), ("u", 1),
    ):
        g = copy.deepcopy(data["gap"])
        g[field] = value
        try:
            audit_gap(n, edges, g, utable)
        except ValueError:
            controls += 1
        else:
            raise ValueError("incorrect gap certificate accepted")
    return controls


def check(data):
    n, rows, edges = decode(data)
    utable = ramsey_table()
    full = (1 << n) - 1
    blue = [full ^ row ^ (1 << v) for v, row in enumerate(rows)]
    reconstructed = (json.dumps({"n": n, "red_edges": [list(e) for e in sorted(edges)]},
                               indent=2) + "\n").encode()
    original_hash = hashlib.sha256(reconstructed).hexdigest()
    require(original_hash == ORIGINAL_SHA256, "not the pinned upstream graph")
    degrees = [sum(pair(v, w) in edges for w in range(n) if w != v) for v in range(n)]
    require(degrees == [20] * 3 + [21] * 40, "degree sequence")
    require(degrees == [row.bit_count() for row in rows], "degree algorithm disagreement")
    core_rows = [sum(1 << w for w in CORE if pair(v, w) in edges) for v in CORE]
    require(tuple(core_rows) == CORE_ROWS, "literal core")
    require(core_rows == [rows[v] & ((1 << 11) - 1) for v in CORE], "bit core disagreement")
    signatures = [sum(1 << w for w in range(3) if pair(v, w) in edges) for v in range(3, n)]
    require(tuple(signatures) == EXPECTED_SIGNATURES, "root signatures")
    profiles = []
    for v in range(3):
        r = [w for w in range(n) if w != v and pair(v, w) in edges]
        b = [w for w in range(n) if w != v and pair(v, w) not in edges]
        tr = sum(pair(i, j) in edges for i, j in itertools.combinations(r, 2))
        tb = sum(pair(i, j) not in edges for i, j in itertools.combinations(b, 2))
        require(tr == sum((rows[w] & rows[v]).bit_count() for w in r) // 2, "red profile disagreement")
        require(tb == sum((blue[w] & blue[v]).bit_count() for w in b) // 2, "blue profile disagreement")
        profiles.append([len(r), tr, tb])
    require(profiles == [[20, 92, 107], [20, 93, 107], [20, 93, 107]], "root profiles")

    # Literal five-set inspection versus adjacency-intersection recursion.
    literal = [set(), set()]
    inspected = 0
    for five in itertools.combinations(range(n), 5):
        inspected += 1
        mask = sum(1 << v for v in five)
        if literal_clique(five, edges, True):
            literal[0].add(mask)
        if literal_clique(five, edges, False):
            literal[1].add(mask)
    bitsets = [bit_cliques(rows, 5), bit_cliques(blue, 5)]
    require(literal == bitsets, "entry-level K5 disagreement")
    census = [[sum((mask >> 11).bit_count() == k for mask in family) for k in range(6)]
              for family in literal]
    require(census == [[0, 0, 0, 0, 215, 86], [0, 0, 0, 0, 202, 85]], "joint-three layer")

    # Independently generate the domain of every retained root-union row.
    literal_roots = [
        [c for k in range(4) for c in itertools.combinations(CORE, k)
         if literal_clique(c, edges, color)]
        for color in (True, False)
    ]
    bit_roots = []
    for color_rows in (rows, blue):
        restricted = [row & ((1 << 11) - 1) for row in color_rows[:11]]
        bit_roots.append(set().union(*(bit_cliques(restricted, k) for k in range(4))))
    literal_bounds, bit_bounds = {}, {}
    for a in literal_roots[0]:
        for b in literal_roots[1]:
            if (not a and not b) or set(a) & set(b):
                continue
            s = literal_union(n, edges, a, b)
            bound = utable[5 - len(a)][5 - len(b)] - 1
            require(len(s) <= bound, "literal union bound failed")
            literal_bounds[(sum(1 << v for v in a), sum(1 << v for v in b))] = (sum(1 << v for v in s), bound)
    for amask in bit_roots[0]:
        for bmask in bit_roots[1]:
            if amask & bmask or not amask | bmask:
                continue
            smask = full & ~(amask | bmask)
            for v in CORE:
                if amask >> v & 1:
                    smask &= rows[v]
                if bmask >> v & 1:
                    smask &= blue[v]
            bound = DISPLAYED_U[4 - amask.bit_count()][4 - bmask.bit_count()] - 1
            require(smask.bit_count() <= bound, "bit union bound failed")
            bit_bounds[(amask, bmask)] = (smask, bound)
    require(literal_bounds == bit_bounds and len(literal_bounds) == 3140, "entry-level union disagreement")
    gap = audit_gap(n, edges, data["gap"], utable)
    # A second derivation of the specific interface row from masks.
    a, b, v = 1, 2, 37
    s_mask = rows[a] & blue[b] & ~(1 << a | 1 << b)
    t_mask = s_mask & rows[v]
    require(s_mask == sum(1 << i for i in gap["S"])
            and t_mask == sum(1 << i for i in gap["T"]), "bit lift disagreement")
    require(rows[v] >> a & 1 and rows[v] >> b & 1, "external-root guard")
    controls = negative_controls(data, n, edges, utable)
    return {
        "original_graph_sha256": original_hash,
        "order": n,
        "red_edges": len(edges),
        "degree_multiplicities": {"20": 3, "21": 40},
        "root_profiles": profiles,
        "five_sets_inspected": inspected,
        "monochromatic_K5_by_outside_count": {"red": census[0], "blue": census[1]},
        "root_union_rows": len(literal_bounds),
        "entry_level_algorithms_agree": True,
        "gap": gap,
        "negative_controls_rejected": controls,
        "solver_used": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("witness.json"))
    args = parser.parse_args()
    result = check(json.loads(args.fixture.read_text()))
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
