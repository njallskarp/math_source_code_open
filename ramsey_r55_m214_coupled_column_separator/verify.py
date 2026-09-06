#!/usr/bin/env python3
"""Exact OPB evaluation and physical decoding of all coupled-column rows.

No producer, predecessor Python module, optimization solver, or floating point
is imported. Vector coordinates are arbitrary until every check succeeds.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
import math
from fractions import Fraction as F
from pathlib import Path

FORMULA_SHA256 = "9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609"
HEADER = b"* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64\n"
N = 43
E = frozenset(range(2, 15))
H = frozenset(range(15, 28))
X = frozenset(range(2, 43)) - H


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_vector(path):
    values = [None]
    with path.open(encoding="ascii") as handle:
        require(next(handle, "") == "variable\trho=3/14\trho=1\n", "vector header")
        for expected, line in enumerate(handle, 1):
            fields = line.split()
            require(len(fields) == 3 and fields[0] == str(expected), "coordinate order")
            a, b = map(F, fields[1:])
            require(0 <= a <= 1 and 0 <= b <= 1, "coordinate box")
            values.append((a, b))
    require(len(values) == 98_759, "coordinate count")
    denominator = math.lcm(*(v.denominator for row in values[1:] for v in row))
    lo = [0] + [int(a * denominator) for a, _ in values[1:]]
    delta = [0] + [int((b-a) * denominator) for a, b in values[1:]]
    return values, denominator, lo, delta


def evaluate_row(raw, lo, delta, denominator):
    fields = raw.split()
    require(len(fields) >= 5 and len(fields) % 2 == 1 and fields[-1] == b";",
            "row syntax")
    relation = fields[-3]
    require(relation in (b"=", b">="), "row relation")
    rhs = int(fields[-2]) * denominator
    value, change = -rhs, 0
    for pos in range(0, len(fields)-3, 2):
        coefficient = int(fields[pos])
        token = fields[pos+1]
        require(token.startswith(b"x"), "variable token")
        index = int(token[1:])
        require(1 <= index < len(lo), "variable index")
        value += coefficient * lo[index]
        change += coefficient * delta[index]
    valid = value == change == 0 if relation == b"=" else min(value, value+change) >= 0
    require(valid, "unsatisfied endpoint row")
    return relation


def check_opb(path, lo, delta, denominator):
    digest = hashlib.sha256()
    rows = equalities = size = 0
    with path.open("rb") as handle:
        header = handle.readline()
        require(header == HEADER, "formula header")
        digest.update(header)
        size += len(header)
        for raw in handle:
            digest.update(raw)
            size += len(raw)
            try:
                relation = evaluate_row(raw, lo, delta, denominator)
            except ValueError as error:
                raise ValueError(f"OPB row {rows+1}: {error}") from error
            equalities += relation == b"="
            rows += 1
    require((rows, equalities, size) == (2_983_003, 87, 511_537_255), "formula coverage")
    require(digest.hexdigest() == FORMULA_SHA256, "formula digest")
    return rows, equalities


def physical_maps():
    """Rebuild the published coordinate convention from physical vertex sets."""
    edge = {ij: k for k, ij in enumerate(it.combinations(range(43), 2), 1)}
    roots = []
    patterns = (("H", "A"), ("BB", "BO", "OO"), ("B", "O"),
                ("BB", "BO", "OO"), ("HO", "AB"))
    for family in range(5):
        for c in range(9, 14):
            for k in range(7):
                sizes = (k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k)
                cells = []
                first = 2
                for size in sizes:
                    cells.append(tuple(range(first, first+size)))
                    first += size
                require(first == 43, "root partition")
                for pattern in patterns[family]:
                    offset = 0 if family < 2 else 4
                    if any(pattern.count(label) > sizes[offset+i]
                           for i, label in enumerate("HABO")):
                        continue
                    core = tuple(sorted(cells[0] + cells[4]))
                    outside = tuple(v for v in range(2, 43) if v not in core)
                    roots.append(((family, c, k, pattern), core, outside))
    require(len(roots) == 389 and roots[48][0] == (0, 13, 0, "A"), "root order")
    missed_support, q_support = set(), set()
    for _, core, outside in roots:
        for a, b in it.combinations(outside, 2):
            missed_support.update((a, b, h) for h in core)
            q_support.update((a, b, i, j) for i, j in it.combinations(core, 2))
    require((len(missed_support), len(q_support)) == (10_612, 74_513), "lift support")
    missed = {key: 13_634+k for k, key in enumerate(sorted(missed_support))}
    q = {key: 24_246+k for k, key in enumerate(sorted(q_support))}
    return edge, roots, missed, q


def check_separator(values, denominator, lo, delta):
    edge, roots, missed, q = physical_maps()
    # Directly confirm the active object and the one-dimensional interpolation.
    def value(i, j):
        return values[edge[min(i, j), max(i, j)]][0]
    for h in H:
        require(sum(value(h, j) for j in H if j != h) == 4, "active core degree")
        for a, b in it.combinations(sorted(X), 2):
            m = (F(1, 7), F(14, 65), F(7, 26))[(a in E)+(b in E)]
            require(values[missed[a, b, h]] == (m, m), "active pair moment")
        require(sum(values[missed[a, b, h]][0]
                    for a, b in it.combinations(sorted(X), 2)) == 78, "column sum")
    require(all(values[13_245+r] == (F(r == 48), F(r == 48))
                for r in range(389)), "one-hot selectors")
    varying = set()
    for (a, b, i, j), index in q.items():
        if {i, j} <= H and {a, b} <= X and value(i, j) == 1:
            m = values[missed[a, b, i]][0]
            require(values[index] == (F(3, 14)*m, m), "active q interpolation")
            varying.add(index)
    require({i for i in range(1, len(delta)) if delta[i]} == varying, "only active q varies")
    require(len(varying) == 26*378, "varying coordinate count")

    rows = 0
    violations = []
    # rho=6/13 lies 45/143 of the way from 3/14 to 1.
    for r, (_, core, outside) in enumerate(roots):
        c = len(core)
        pairs = tuple(it.combinations(outside, 2))
        p = len(pairs)
        for i, j in it.combinations(core, 2):
            maximum = 64-c-(20 if i in E else 21)-(20 if j in E else 21)
            bound = math.comb(maximum, 2)
            require(9 <= maximum <= 15 and bound < p, "bound domain")
            x, y = edge[i, j], 13_245+r
            base = bound*lo[x] + (p-bound)*(denominator-lo[y])
            change = bound*delta[x] - (p-bound)*delta[y]
            for a, b in pairs:
                index = q[a, b, i, j]
                base -= lo[index]
                change -= delta[index]
            require(base >= 0 and 143*base+45*change >= 0, "new interval infeasible")
            if base+change < 0:
                violations.append((r, i, j, F(base+change, denominator)))
            rows += 1
    require(len(violations) == 26 and all(r == 48 and slack == -42
                                        for r, i, j, slack in violations), "strict separator")
    # These exact rows certify that the stated parameter intervals are sharp.
    require(value(2, 14) == 0, "lower-endpoint exterior blue pair")
    require(13*F(7, 26)-2 == F(3, 2), "lower endpoint threshold")
    require(26*F(7, 26)*F(3, 14) == F(3, 2), "lower endpoint tight")
    require(78*F(6, 13) == 36, "upper endpoint tight")
    return {"coupled_rows": rows, "old_rho_interval": ["3/14", "1"],
            "new_rho_interval": ["3/14", "6/13"], "violations_at_rho_1": 26,
            "violation_slack": "-42", "active_column_moment": "78",
            "varying_q_coordinates": len(varying)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vector", type=Path, required=True)
    parser.add_argument("--opb", type=Path, required=True)
    args = parser.parse_args()
    values, denominator, lo, delta = read_vector(args.vector)
    rows, equalities = check_opb(args.opb, lo, delta, denominator)
    result = check_separator(values, denominator, lo, delta)
    result.update(status="PASS", variables=98_758, old_constraints=rows,
                  old_equalities=equalities, formula_sha256=FORMULA_SHA256,
                  common_denominator=denominator)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
