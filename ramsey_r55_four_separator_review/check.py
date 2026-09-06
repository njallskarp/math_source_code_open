"""Independent clause-level and first-column-orbit coverage review.

CPython 3.12, standard library; no producer, solver, or graph-library import.
Primary catalogue completeness is external, never inferred from file checks.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
from urllib.request import urlopen


PIN = {
    15: ("53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1", 640),
    16: ("b9a7c89cf999d64c976c877891d06f828ce2e846f5ddfa72bb402f2ddd57b927", 2),
    17: ("23f8802eed6281e1b40c7ec157f687d67624c6a327a513b003bce93e33e9214c", 1),
}
CATALOG_TO_PALEY = (0, 1, 9, 2, 16, 4, 13, 15, 8, 5, 14, 3, 10, 12, 6, 11, 7)
SEED = ((0, 1, 3, 4, 6, 10, 11, 15), (0, 2, 3, 6, 7, 9, 12, 14),
        (1, 2, 5, 7, 8, 12, 13, 15), (2, 4, 5, 8, 9, 11, 14, 16))
SQUARES = {x*x % 17 for x in range(1, 17)}
PALEY = {(i, j) for i, j in combinations(range(17), 2) if (j-i) % 17 in SQUARES}
CYCLE = {(17, 18), (18, 19), (19, 20), (17, 20)}
HUB = {(i, 21) for i in range(17, 21)}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(obj):
    return sha256((json.dumps(obj, separators=(",", ":"))+"\n").encode()).hexdigest()


def edge(i, j):
    return (i, j) if i < j else (j, i)


def decode(raw):
    require(type(raw) is bytes and bool(raw), "graph6 bytes")
    require(all(63 <= x <= 126 for x in raw), "graph6 alphabet")
    n = raw[0]-63
    require(n < 63, "short graph6 only")
    needed = n*(n-1)//2
    require(len(raw) == 1+(needed+5)//6, "graph6 length")
    bits = "".join(format(c-63, "06b") for c in raw[1:])
    require(set(bits[needed:]) <= {"0"}, "graph6 padding")
    edges = set()
    pos = 0
    for j in range(n):
        for i in range(j):
            if bits[pos] == "1":
                edges.add((i, j))
            pos += 1
    return n, edges


def forbidden(n, edges, size, red=True):
    return [s for s in combinations(range(n), size)
            if all((e in edges) == red for e in combinations(s, 2))]


def identify(source, permutation):
    require(sorted(permutation) == list(range(17)), "catalogue bijection")
    require({edge(permutation[i], permutation[j]) for i, j in source} == PALEY,
            "catalogue Paley correspondence")


def catalogues(directory):
    answer = {}
    for n, (identity, count) in PIN.items():
        name = f"r44_{n}.g6"
        if directory is None:
            with urlopen("https://users.cecs.anu.edu.au/~bdm/data/"+name, timeout=30) as r:
                raw = r.read()
        else:
            raw = (directory/name).read_bytes()
        require(sha256(raw).hexdigest() == identity, "primary input identity")
        records = [decode(line) for line in raw.splitlines()]
        require(len(records) == count, "primary record count")
        hist = Counter()
        for order, edges in records:
            require(order == n, "primary order")
            require(not forbidden(n, edges, 4) and not forbidden(n, edges, 4, False),
                    "primary Ramsey property")
            hist[len(edges)] += 1
        if n == 17:
            identify(records[0][1], CATALOG_TO_PALEY)
        answer[str(n)] = {"records": len(records), "edge_histogram": dict(sorted(hist.items())),
                          "sha256": identity}
    return answer


def literal_index(i, a):
    return 17*i+a+1


def reduce_forbidden(vertices, red):
    """Simplify a PHYSICAL forbidden clique under every fixed edge."""
    literals = []
    fixed_red = PALEY | CYCLE | HUB
    for a, b in combinations(vertices, 2):
        if a < 17 and 17 <= b < 21:
            var = literal_index(b-17, a)
            literals.append(-var if red else var)
        elif ((a, b) in fixed_red) != red:
            return None
    return tuple(sorted(literals))


def semantic_clauses():
    full = Counter()
    scanned = {}
    for k, red in ((4, True), (5, False)):
        scanned[str(k)] = 0
        for q in combinations(range(22), k):
            scanned[str(k)] += 1
            row = reduce_forbidden(q, red)
            if row is not None:
                require(bool(row), "fixed graph already forbidden")
                full[row] += 1
    triangles = forbidden(17, PALEY, 3)
    independent = forbidden(17, PALEY, 3, False)
    criterion = Counter()
    for i in range(4):
        for t in triangles:
            criterion[tuple(sorted(-literal_index(i, a) for a in t))] += 1
    for s, t in CYCLE:
        for a, b in PALEY:
            criterion[tuple(sorted(-literal_index(i-17, x)
                                   for i in (s, t) for x in (a, b)))] += 1
    for i, j in ((0, 2), (1, 3)):
        for t in independent:
            criterion[tuple(sorted(literal_index(k, a) for k in (i, j) for a in t))] += 1
    require(full == criterion, "physical forbidden-clique/criterion equality")
    require(all(v == 1 for v in full.values()), "unexpected repeated residual")
    return full, triangles, independent, scanned


def build_graph(columns):
    require(len(columns) == 4, "four columns")
    require(all(len(c) == 8 and tuple(c) == tuple(sorted(set(c))) and
                all(type(v) is int and 0 <= v < 17 for v in c) for c in columns),
            "column schema")
    return PALEY | CYCLE | HUB | {(a, 17+i) for i, c in enumerate(columns) for a in c}


def check_graph(columns):
    edges = build_graph(columns)
    require(len(edges) == 108, "seed edge total")
    require(not forbidden(22, edges, 4), "seed red K4")
    require(not forbidden(22, edges, 5, False), "seed blue K5")
    return edges


def transport_column(column, permutation):
    return tuple(sorted(permutation[x] for x in column))


def classify(triangles, independent):
    cols = [tuple(s) for s in combinations(range(17), 8)
            if not any(set(t) <= set(s) for t in triangles)]
    sets = {c: frozenset(c) for c in cols}
    perms = [tuple((a*x+b) % 17 for x in range(17))
             for a in sorted(SQUARES) for b in range(17)]
    for p in perms:
        require(sorted(p) == list(range(17)), "affine bijection")
        require({edge(p[i], p[j]) for i, j in PALEY} == PALEY, "affine graph action")
    remaining = set(cols)
    first_orbits = []
    while remaining:
        rep = min(remaining)
        orbit = {transport_column(rep, p) for p in perms}
        require(orbit <= remaining, "first-column orbit disjoint coverage")
        remaining -= orbit
        first_orbits.append((rep, orbit))
    adjacent = {(a, b): not any(i in sets[a] & sets[b] and j in sets[a] & sets[b]
                                for i, j in PALEY) for a in cols for b in cols}
    opposite = {(a, b): not any(set(t).isdisjoint(sets[a] | sets[b]) for t in independent)
                for a in cols for b in cols}
    # Exhaust THREE columns for one representative per first-column orbit.
    fibers = {}
    for a, _ in first_orbits:
        fibers[a] = {(a, b, c, d) for b, c, d in product(cols, repeat=3)
                     if adjacent[a, b] and adjacent[b, c] and adjacent[c, d]
                     and adjacent[d, a] and opposite[a, c] and opposite[b, d]}
    seed_orbit = set()
    for p in perms:
        for start in range(4):
            for step in (-1, 1):
                seed_orbit.add(tuple(transport_column(SEED[(start+step*i) % 4], p)
                                     for i in range(4)))
    for rep, orbit in first_orbits:
        require(fibers[rep] == {t for t in seed_orbit if t[0] == rep},
                "entrywise representative fiber equality")
    lifted = {tuple(transport_column(c, p) for c in t)
              for fiber in fibers.values() for t in fiber for p in perms}
    require(lifted == seed_orbit, "full lifted set equality")
    return {"individual_columns": len(cols),
            "first_column_orbits": [{"representative": rep, "orbit_size": len(orbit),
                                     "complete_fiber_size": len(fibers[rep])}
                                    for rep, orbit in first_orbits],
            "ordered_tuples": len(lifted), "tuple_sha256": digest(sorted(lifted)),
            "fiber_set_equality": True, "lifted_set_equality": True}


def cuts(edges):
    adj = [{j for j in range(22) if edge(i, j) in edges} for i in range(22)]
    found = []
    visited = 0
    for size in range(5):
        for cut in combinations(range(22), size):
            visited += 1
            rest = set(range(22))-set(cut)
            seen = {min(rest)}
            stack = list(seen)
            while stack:
                v = stack.pop()
                for w in (adj[v] & rest)-seen:
                    seen.add(w)
                    stack.append(w)
            if seen != rest:
                found.append(cut)
    require(found == [(17, 18, 19, 20)], "unique cut through size four")
    return {"subsets_checked": visited, "all_cuts_through_four": found}


def controls(clauses):
    cases = []
    def reject(label, f):
        try:
            f()
        except (ValueError, TypeError):
            cases.append(label)
        else:
            raise ValueError("control accepted: "+label)
    for raw in (b"", b"\x00", b"~", b"A", b"A??", bytes((65, 96))):
        reject("bad graph6 "+repr(raw), lambda raw=raw: decode(raw))
    reject("nonbijective catalogue map", lambda: identify(PALEY, (0,)*17))
    reject("wrong catalogue map", lambda: identify(PALEY, (1,0)+tuple(range(2,17))))
    reject("missing column", lambda: check_graph(SEED[:3]))
    reject("short column", lambda: check_graph((SEED[0][:-1],)+SEED[1:]))
    reject("duplicate vertex", lambda: check_graph(((0,)*8,)+SEED[1:]))
    reject("out of range", lambda: check_graph(((0,1,3,4,6,10,11,17),)+SEED[1:]))
    reject("repeated column Ramsey violation", lambda: check_graph((SEED[0],)*4))
    for name in ("missing", "duplicate", "wrong sign", "wrong variable"):
        changed = clauses.copy()
        row = min(changed)
        if name == "missing":
            del changed[row]
        elif name == "duplicate":
            changed[row] += 1
        elif name == "wrong sign":
            del changed[row]
            changed[tuple(sorted((-row[0],)+row[1:]))] += 1
        else:
            del changed[row]
            changed[tuple(sorted((69,)+row[1:]))] += 1
        reject(name+" residual clause", lambda changed=changed:
               require(changed == clauses, "clause multiset mismatch"))
    require(decode(b"?") == (0, set()) and decode(b"@") == (1, set())
            and decode(b"A?") == (2, set()) and decode(b"A_") == (2, {(0,1)}),
            "graph6 positive controls")
    return {"rejected_components": len(cases), "labels": cases}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog-dir", type=Path, help="optional original pinned primary inputs")
    args = p.parse_args()
    primary = catalogues(args.catalog_dir)
    rows, triangles, independent, scanned = semantic_clauses()
    edges = check_graph(SEED)
    result = {"catalogues": primary, "physical_subsets_scanned": scanned,
              "residual_clause_histogram": dict(sorted(Counter(map(len, rows)).items())),
              "residual_clause_sha256": digest(sorted(rows)),
              "classification": classify(triangles, independent),
              "seed": {"edges": len(edges), "edge_sha256": digest(sorted(edges)),
                       "degree_histogram": dict(sorted(Counter(sum(v in e for e in edges)
                                                               for v in range(22)).items())),
                       "cuts": cuts(edges)},
              "controls": controls(rows), "status": "PASS"}
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
