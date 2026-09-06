#!/usr/bin/env python3
"""Optional exact discovery LP; the published certificate needs no solver."""

import argparse
import itertools as it
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

from witness import E, H, X, base, canonical, require


def system():
    _, classes = base()
    triples = tuple(it.combinations(range(43), 3))
    groups = sorted({canonical(t, classes)[0] for t in triples})
    ids = {key: i for i, key in enumerate(groups)}
    representatives, decode = {}, {}
    for triple in triples:
        key, order = canonical(triple, classes)
        gid = ids[key]
        representatives.setdefault(gid, order)
        decode[triple] = gid, order

    def form(triple, red=(), blue=()):
        gid, order = decode[tuple(sorted(triple))]
        pairs = [frozenset(p) for p in it.combinations(order, 2)]
        rr = [pairs.index(frozenset(pair)) for pair in red]
        bb = [pairs.index(frozenset(pair)) for pair in blue]
        return Counter({8*gid+mask: 1 for mask in range(8)
                        if all(mask >> i & 1 for i in rr)
                        and all(not (mask >> i & 1) for i in bb)})

    def plus(parts):
        row = Counter()
        for part in parts:
            row.update(part)
        return row

    rows = []
    for order in representatives.values():
        rows.append((form(order), "=", F(1)))
        for pair in it.combinations(order, 2):
            rows.append((form(order, red=[pair]), "=", classes.edge_value(*pair)))
        active = [h for h in order if h in H and set(order)-{h} <= X]
        if active:
            h = active[0]
            a, b = sorted(set(order)-{h})
            m = (F(1, 7), F(14, 65), F(7, 26))[(a in E)+(b in E)]
            rows.append((form(order, blue=[(a, h), (b, h)]), "=", m))
    for h in range(43):
        others = [v for v in range(43) if v != h]
        row = plus(form((a, b, h), red=tuple(it.combinations((a, b, h), 2)))
                   for a, b in it.combinations(others, 2))
        rows.append((row, "=", F(93 if h in E else 100)))
        for a in others:
            row = plus(form((a, b, h), red=[(h, a), (h, b)]) for b in others if b != a)
            rows.append((row, "=", (19 if h in E else 20)*classes.edge_value(a, h)))
    for a, b in it.combinations(range(43), 2):
        others = [h for h in range(43) if h not in (a, b)]
        row = plus(form((a, b, h), red=tuple(it.combinations((a, b, h), 2))) for h in others)
        rows.append((row, "<=", 13*classes.edge_value(a, b)))
        row = plus(form((a, b, h), blue=tuple(it.combinations((a, b, h), 2))) for h in others)
        rows.append((row, "<=", 13*(1-classes.edge_value(a, b))))
        if a in H and b in H and classes.edge_value(a, b) == 1:
            row = plus(form((a, b, h), red=tuple(it.combinations((a, b, h), 2))) for h in X)
            rows.append((row, "=", F(7)))
    require(len(groups) == 171 and len(rows) == 4389, "discovery scope")
    return groups, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lp", type=Path)
    parser.add_argument("--solution", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    groups, rows = system()
    variables = 8*len(groups)
    if args.lp is not None:
        lines = ["Minimize", " obj: 0 p0", "Subject To"]
        for i, (row, relation, rhs) in enumerate(rows):
            terms = "".join(f" + {coefficient} p{j}" for j, coefficient in sorted(row.items())
                            if coefficient)
            lines.append(f" row{i}:"+terms+f" {relation} {rhs}")
        lines += ["Bounds"] + [f" 0 <= p{j} <= 1" for j in range(variables)] + ["End"]
        args.lp.write_text("\n".join(lines)+"\n", encoding="ascii")
    if args.solution is not None:
        require(args.output is not None, "solution needs output")
        values, seen = [F(0)]*variables, set()
        for line in args.solution.read_text().splitlines():
            if line.startswith("p"):
                name, value = line.split()
                index = int(name[1:])
                require(0 <= index < variables and index not in seen, "solution coordinate")
                seen.add(index)
                values[index] = F(value)
        require(seen and min(values) >= 0 and max(values) <= 1, "solution box")
        for i, (row, relation, rhs) in enumerate(rows):
            observed = sum(c*values[j] for j, c in row.items())
            require(observed == rhs if relation == "=" else observed <= rhs, f"discovery row {i}")
        table = [{"types": list(key[0]), "edges": list(map(str, key[1])),
                  "atoms": list(map(str, values[8*i:8*i+8]))} for i, key in enumerate(groups)]
        args.output.write_text(json.dumps(table, separators=(",", ":"))+"\n", encoding="ascii")
    require(args.lp is not None or args.solution is not None, "no requested output")
    print("PASS templates=171 discovery_variables=1368 discovery_rows=4389")


if __name__ == "__main__":
    main()
