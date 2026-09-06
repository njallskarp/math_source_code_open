#!/usr/bin/env python3
"""Check three full LP points and all shared-coordinate moment constraints.

Imports no witness producer or solver. The physical coordinate decoder is
explicitly reused from the pinned h3341 verifier; all new rows are evaluated
below directly from those physical vertex sets.
"""

import argparse
import hashlib
import importlib.util
import itertools as it
import json
import math
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
FORMULA_SHA = "9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609"
DECODER_SHA = "b92a68ebc8d6edeeb7188dd658bbbeb9539d6f00043dd37a1a756867c9699eb2"
VECTOR_HEADER = "variable\tbaseline_rho=3/14\trepaired_rho=3/14\trepaired_rho=10/39\n"
OPB_HEADER = b"* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64\n"
E = frozenset(range(2, 15))
H = frozenset(range(15, 28))
X = frozenset(range(2, 43)) - H


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decoder():
    path = REPO / "ramsey_r55_m214_coupled_column_separator/verify.py"
    require(hashlib.sha256(path.read_bytes()).hexdigest() == DECODER_SHA, "decoder identity")
    spec = importlib.util.spec_from_file_location("prior_decoder", path)
    require(spec is not None and spec.loader is not None, "decoder loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.physical_maps()


def read_vector(path):
    values = [(F(0),)*3]
    with path.open(encoding="ascii") as handle:
        require(next(handle, "") == VECTOR_HEADER, "vector header")
        for expected, line in enumerate(handle, 1):
            fields = line.split()
            require(len(fields) == 4 and fields[0] == str(expected), "coordinate ordering")
            row = tuple(map(F, fields[1:]))
            require(all(0 <= v <= 1 for v in row), "coordinate box")
            values.append(row)
    require(len(values) == 98_759, "coordinate count")
    denominator = math.lcm(*(v.denominator for row in values for v in row))
    scaled = [tuple(int(v*denominator) for v in row) for row in values]
    return denominator, scaled


def row_slacks(raw, vector, denominator):
    fields = raw.split()
    require(len(fields) >= 5 and len(fields) % 2 == 1 and fields[-1] == b";", "row syntax")
    relation = fields[-3]
    require(relation in (b"=", b">="), "row relation")
    a = b = c = -int(fields[-2])*denominator
    for k in range(0, len(fields)-3, 2):
        coefficient = int(fields[k])
        require(fields[k+1].startswith(b"x"), "variable token")
        index = int(fields[k+1][1:])
        require(0 < index < len(vector), "variable index")
        va, vb, vc = vector[index]
        a += coefficient*va
        b += coefficient*vb
        c += coefficient*vc
    return relation, (a, b, c)


def check_opb(path, vector, denominator):
    digest = hashlib.sha256()
    rows = equalities = size = 0
    with path.open("rb") as handle:
        header = handle.readline()
        require(header == OPB_HEADER, "OPB header")
        digest.update(header)
        size += len(header)
        for raw in handle:
            relation, slacks = row_slacks(raw, vector, denominator)
            require(all(s == 0 for s in slacks) if relation == b"=" else min(slacks) >= 0,
                    f"old OPB row {rows+1}")
            digest.update(raw)
            size += len(raw)
            rows += 1
            equalities += relation == b"="
    require((size, rows, equalities) == (511_537_255, 2_983_003, 87), "old formula coverage")
    require(digest.hexdigest() == FORMULA_SHA, "old formula identity")
    return rows, equalities


def sum_coordinates(vector, indices):
    result = [0, 0, 0]
    for index in indices:
        row = vector[index]
        for k in range(3):
            result[k] += row[k]
    return result


def hull_slacks(c, degree_sum, pair_count, S, Q, selector, edge, denominator):
    """Integer-scaled, box-valid guards for the full 0..K binomial hull."""
    constant = 45-c-degree_sum
    K = 64-c-degree_sum
    inactive = 2*denominator-selector-edge
    for tangent in range(K):
        rhs = tangent*constant-math.comb(tangent+1, 2)
        guard = rhs+tangent*(c+39)
        require(guard >= 0, "lower guard")
        yield Q-tangent*S+math.comb(tangent+1, 2)*denominator+guard*inactive
    guard = -(K-1)*constant+2*pair_count
    yield (K-1)*S-2*Q+guard*inactive


def check_lifts(vector, denominator):
    edges, roots, missed, q = decoder()
    triangles = {tri: index for index, tri in enumerate(it.combinations(range(43), 3), 904)}
    for r in range(389):
        require(vector[13_245+r] == (int(r == 48)*denominator,)*3, "selected root")
    for h in H:
        for a, b in it.combinations(sorted(X), 2):
            m = (F(1, 7), F(14, 65), F(7, 26))[(a in E)+(b in E)]
            require(vector[missed[a, b, h]] == (m*denominator,)*3, "fixed active m")
    varying_q = 0
    for (a, b, i, j), index in q.items():
        if {i, j} <= H and {a, b} <= X and vector[edges[i, j]][0] == denominator:
            m = vector[missed[a, b, i]][0]
            require(vector[index] == (F(3, 14)*m, F(3, 14)*m, F(10, 39)*m), "rho convention")
            varying_q += 1
    require(varying_q == 9_828, "active q support")
    require(all(vector[i][0] == vector[i][1] == vector[i][2] for i in edges.values()),
            "fixed edges")

    codegree_bad = []
    for (i, j), index in edges.items():
        T = sum_coordinates(vector, (triangles[tuple(sorted((i, j, k)))]
                                     for k in range(43) if k not in (i, j)))
        slacks = [13*vector[index][k]-T[k] for k in range(3)]
        require(min(slacks[1:]) >= 0, "repaired global codegree")
        if slacks[0] < 0:
            codegree_bad.append(F(slacks[0], denominator))

    old_rows = moment_rows = 0
    hull_bad = []
    active_S, active_Q = [set() for _ in range(3)], [set() for _ in range(3)]
    for r, (_, core, exterior) in enumerate(roots):
        c = len(core)
        pairs = tuple(it.combinations(exterior, 2))
        p = len(pairs)
        y = vector[13_245+r]
        for i, j in it.combinations(core, 2):
            dsum = (20 if i in E else 21)+(20 if j in E else 21)
            K = 64-c-dsum
            bound = math.comb(K, 2)
            x = vector[edges[i, j]]
            Q = sum_coordinates(vector, (q[a, b, i, j] for a, b in pairs))
            A = sum_coordinates(vector, (edges[tuple(sorted((h, v)))]
                                        for h in (i, j) for v in core if h != v))
            T = sum_coordinates(vector, (triangles[tuple(sorted((i, j, v)))] for v in exterior))
            S = [(45-c-dsum)*denominator+A[k]+T[k] for k in range(3)]
            old_slacks = [bound*x[k]+(p-bound)*(denominator-y[k])-Q[k] for k in range(3)]
            require(min(old_slacks) >= 0, "h3341 coupled-column row")
            old_rows += 1
            slacks = [list(hull_slacks(c, dsum, p, S[k], Q[k], y[k], x[k], denominator))
                      for k in range(3)]
            require(min(slacks[1]) >= 0 and min(slacks[2]) >= 0, "repaired moment hull")
            for facet, slack in enumerate(slacks[0]):
                if slack < 0:
                    hull_bad.append((r, i, j, facet, F(slack, denominator)))
            moment_rows += K+1
            if r == 48 and x[0] == denominator:
                for k in range(3):
                    active_S[k].add(F(S[k], denominator))
                    active_Q[k].add(F(Q[k], denominator))
    require(old_rows == 21_762, "h3341 row coverage")
    require(len(codegree_bad) == 182, "old codegree violations")
    require(len(hull_bad) == 26 and all(r == 48 and f == 9 and s == -F(178, 7)
                                       for r, i, j, f, s in hull_bad), "strict hull separator")
    require(active_S == [{F(1)}, {F(5)}, {F(5)}], "active S")
    require(active_Q == [{F(117, 7)}, {F(117, 7)}, {F(20)}], "active Q")
    require(vector[edges[2, 14]] == (0, 0, 0), "sharp lower exterior pair")
    return {"old_coupled_rows": old_rows, "new_global_codegree_rows": len(edges),
            "new_moment_hull_rows": moment_rows, "old_point_hull_violations": len(hull_bad),
            "old_point_hull_slack": "-178/7", "old_point_codegree_violations": len(codegree_bad),
            "new_rho_interval": ["3/14", "10/39"], "active_S_old_new": ["1", "5"],
            "active_Q_new_endpoints": ["117/7", "20"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vector", type=Path, required=True)
    parser.add_argument("--opb", type=Path, required=True)
    args = parser.parse_args()
    denominator, vector = read_vector(args.vector)
    rows, equalities = check_opb(args.opb, vector, denominator)
    result = check_lifts(vector, denominator)
    result.update(status="PASS", old_opb_rows=rows, old_opb_equalities=equalities,
                  variables=98_758, full_points_checked=3, common_denominator=denominator,
                  formula_sha256=FORMULA_SHA)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
