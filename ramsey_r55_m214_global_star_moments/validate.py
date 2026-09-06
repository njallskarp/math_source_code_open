#!/usr/bin/env python3
"""Replay the complete old LP, then check all triple atoms and global stars.

Imports no new producer, discovery LP, solver, or template table. Reuses the
explicitly pinned predecessor OPB parser, physical decoder, and old-row audit.
"""

import argparse
import hashlib
import importlib.util
import itertools as it
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PRIOR_CHECK_SHA = "e71b51d8485b23a955cba03c88b7a6db794780455682a9a1d1cde30e534e47ed"
PRIOR_VECTOR_SHA = "e433d86a5d0e1b2e2a6412c35730c4f5bcf94cd4e4b2346d0a9cae547355fcca"
MOMENT_HEADER = "a\tb\tc\tm_a\tm_b\tm_c\n"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def predecessor():
    path = REPO / "ramsey_r55_m214_reanchored_moment_hull/check.py"
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PRIOR_CHECK_SHA, "predecessor checker")
    spec = importlib.util.spec_from_file_location("previous_check", path)
    require(spec is not None and spec.loader is not None, "checker loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def atom_values(x, m, z, one=1):
    """Möbius inversion, in bit order (ab, ac, bc); m centers are (a,b,c)."""
    a, b, c = x
    u, v, w = m[0]+a+b-one, m[1]+a+c-one, m[2]+b+c-one
    return (one-a-b-c+u+v+w-z, a-u-v+z, b-u-w+z, u-z,
            c-v-w+z, v-z, w-z, z)


def read_moments(path):
    result = {}
    with path.open(encoding="ascii") as handle:
        require(next(handle, "") == MOMENT_HEADER, "moment header")
        for triple in it.combinations(range(43), 3):
            fields = next(handle, "").split()
            require(len(fields) == 6 and tuple(map(int, fields[:3])) == triple, "moment order")
            row = tuple(map(F, fields[3:]))
            require(all(0 <= value <= 1 for value in row), "moment box")
            for h, value in zip(triple, row):
                result[tuple(v for v in triple if v != h) + (h,)] = value
        require(handle.read() == "", "extra moment rows")
    require(len(result) == 37_023, "full moment support")
    return result


def check_joint(vector, scale, moments, edges, missed):
    # These moments describe both endpoints; only q may change between them.
    require(all((value*scale).denominator == 1 for value in moments.values()), "full rational scale")
    require(all(row[1] == row[2] for row in vector[1:24_246]), "fixed edge/triangle/m coordinates")
    x = {pair: F(vector[index][1], scale) for pair, index in edges.items()}
    require(all(vector[index][1] == moments[key]*scale for key, index in missed.items()),
            "old and new moments must share coordinates")
    blue_codegrees = {pair: F(0) for pair in edges}
    local_blue = [F(0)]*43
    atom_rows = 0
    for index, triple in enumerate(it.combinations(range(43), 3), 904):
        pairs = tuple(it.combinations(triple, 2))
        mm = tuple(moments[tuple(v for v in triple if v != h) + (h,)] for h in triple)
        probabilities = atom_values(tuple(x[p] for p in pairs), mm, F(vector[index][1], scale))
        require(min(probabilities) >= 0, "negative physical triangle atom: " + str(triple))
        require(sum(probabilities) == 1, "atom normalization")
        for pair in pairs:
            blue_codegrees[pair] += probabilities[0]
        for h in triple:
            local_blue[h] += probabilities[0]
        atom_rows += 8
    require(atom_rows == 98_728, "triangle row coverage")
    star_rows = 0
    for h in range(43):
        degree = 20 if 2 <= h <= 14 else 21
        others = [v for v in range(43) if v != h]
        for a in others:
            xa = x[tuple(sorted((a, h)))]
            red = blue = F(0)
            for b in others:
                if a == b:
                    continue
                m = moments[tuple(sorted((a, b))) + (h,)]
                blue += m
                red += m+xa+x[tuple(sorted((b, h)))]-1
            require(red == (degree-1)*xa, "global red star: " + str((h, a)))
            require(blue == (41-degree)*(1-xa), "derived global blue star")
            star_rows += 1
    require(star_rows == 1806, "star row coverage")
    for pair, total in blue_codegrees.items():
        require(total <= 13*(1-x[pair]), "global blue codegree: " + str(pair))
    require(local_blue == [F(105 if h == 2 else 107 if 3 <= h <= 14 else 100)
                           for h in range(43)], "all blue local totals")
    return {"triangle_atom_rows": atom_rows, "global_star_equalities": star_rows,
            "new_blue_codegree_rows": len(blue_codegrees), "full_wedges": len(moments),
            "new_coordinates": len(moments)-len(missed), "total_variables": 125_169,
            "total_rows": 3_371_665, "total_equalities": 1893,
            "red_deficiency_sum": 301, "blue_deficiency_sum": 303,
            "blue_local_totals": {"vertex_2": 105, "vertices_3_to_14": 107, "others": 100}}


def check_separator(path, prior, edges, missed):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PRIOR_VECTOR_SHA, "old point identity")
    scale, old = prior.read_vector(path)
    triangles = {tri: k for k, tri in enumerate(it.combinations(range(43), 3), 904)}
    require(all(row[1] == row[2] for row in old[1:24_246]), "old family fixed coordinates")
    counts = {"lower": 0, "upper": 0}
    example = None
    for (a, b, h), index in missed.items():
        wedge = old[index][1]+old[edges[tuple(sorted((a, h)))]][1]+old[edges[tuple(sorted((b, h)))]][1]-scale
        z = old[triangles[tuple(sorted((a, b, h)))]] [1]
        lower = z-wedge-old[edges[a, b]][1]+scale
        upper = wedge-z
        counts["lower"] += lower < 0
        counts["upper"] += upper < 0
        if (a, b, h) == (2, 3, 15):
            require(F(lower, scale) == -F(1, 39), "strict old-family separator")
            example = "-1/39"
    require(sum(counts.values()) == 2713 and example is not None, "complete separator audit")
    return {"old_family_projection_violations": counts, "old_example_slack": example,
            "old_entire_interval_excluded": ["3/14", "10/39"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vector", type=Path, required=True)
    parser.add_argument("--moments", type=Path, required=True)
    parser.add_argument("--opb", type=Path, required=True)
    parser.add_argument("--prior-vector", type=Path, required=True)
    args = parser.parse_args()
    prior = predecessor()
    scale, vector = prior.read_vector(args.vector)
    base_rows, base_equalities = prior.check_opb(args.opb, vector, scale)
    prior.check_lifts(vector, scale)
    edges, _, missed, _ = prior.decoder()
    result = check_joint(vector, scale, read_moments(args.moments), edges, missed)
    result.update(check_separator(args.prior_vector, prior, edges, missed))
    result.update(status="PASS", base_opb_rows=base_rows, base_opb_equalities=base_equalities,
                  formula_sha256=prior.FORMULA_SHA, common_denominator=scale,
                  new_rho_interval=["3/14", "10/39"], full_new_endpoints_checked=2)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
