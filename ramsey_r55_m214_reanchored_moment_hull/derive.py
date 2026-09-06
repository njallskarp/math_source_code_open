#!/usr/bin/env python3
"""Optional 171-variable discovery LP; exact verification does not need SoPlex."""

import argparse
import itertools as it
from fractions import Fraction as F
from pathlib import Path

from witness import load, require


def system():
    w = load("ramsey_r55_m214_pair_column_hull/derive_fractional_certificate.py", "classes")
    orbits = w.orbit_table()
    orbit_index = {o[0]: j for j, o in enumerate(orbits)}
    ids = {t: orbit_index[w.signature(t)] for t in it.combinations(range(43), 3)}
    equalities = [[o[2][k] for o in orbits] for k in range(10)]
    targets = [93 if t in {"p", "a", "b", "o"} else 100 for t in w.TYPE_ORDER]
    common = [0]*len(orbits)
    for z in range(2, 43):
        if z not in w.H:
            common[ids[tuple(sorted((z, 15, 16)))]] += 1
    equalities.append(common)
    targets.append(7)
    inequalities, bounds = [], []
    for i, j in it.combinations(range(43), 2):
        row = [0]*len(orbits)
        for k in range(43):
            if k not in (i, j):
                row[ids[tuple(sorted((i, j, k)))]] += 1
        inequalities.append(row)
        bounds.append(13*w.edge_value(i, j))
    return w, orbits, equalities, targets, inequalities, bounds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lp", type=Path)
    parser.add_argument("--solution", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    w, orbits, eq, b, ub, rhs = system()
    if args.lp is not None:
        lines = ["Minimize", " obj: 0 z0", "Subject To"]
        for name, rows, targets, relation in [("eq", eq, b, "="), ("codegree", ub, rhs, "<=")]:
            for index, (row, target) in enumerate(zip(rows, targets)):
                terms = "".join(f" + {c} z{j}" for j, c in enumerate(row) if c)
                lines.append(f" {name}{index}:"+terms+f" {relation} {target}")
        lines.append("Bounds")
        for j, orbit in enumerate(orbits):
            lines.append(f" {orbit[3]} <= z{j} <= {orbit[4]}")
        lines.append("End")
        args.lp.write_text("\n".join(lines)+"\n", encoding="ascii")
    if args.solution is not None:
        require(args.output is not None, "solution requires output")
        values = w.parse_solution(args.solution, orbits)
        require(all(sum(F(c)*v for c, v in zip(row, values)) == target
                    for row, target in zip(eq, b)), "repaired equalities")
        require(all(sum(F(c)*v for c, v in zip(row, values)) <= target
                    for row, target in zip(ub, rhs)), "red codegree bounds")
        args.output.write_bytes(w.certificate(orbits, values))
    require(args.lp is not None or args.solution is not None, "no requested output")
    print("PASS discovery_variables=171 equalities=11 inequalities=903")


if __name__ == "__main__":
    main()
