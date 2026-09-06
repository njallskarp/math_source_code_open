#!/usr/bin/env python3
"""Generate the two rational endpoints; verification does not import this file."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PINS = {
    "ramsey_r55_m214_pair_column_hull/derive_fractional_certificate.py":
        "e4508d3d79b5af10b5b195c76f84cfb96f8a2ed4fffc5a774db5bbf5268c145e",
    "ramsey_r55_m214_pair_column_hull/edge_parameters.tsv":
        "4f86eeac21d5d71dbc7b0fa86617d2f2eb8d02b893e2da8c9327a0a4e682d131",
    "ramsey_r55_m214_pair_column_hull/triangle_orbits.tsv":
        "babe43ae1337b5ea19ba0dcb83a3d597d764427949e3929f94a55c15a1ae7249",
    "ramsey_r55_m214_pair_cell_c5_lift/build.py":
        "e8e769e58c5ce34419a9f8bdb252e275aabd9b1ae2a69865efcd916d6e4b90e4",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(relative, name):
    path = REPO / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def endpoints():
    for relative, digest in PINS.items():
        require(hashlib.sha256((REPO / relative).read_bytes()).hexdigest() == digest,
                "changed predecessor: " + relative)
    edges = load("ramsey_r55_m214_pair_column_hull/derive_fractional_certificate.py",
                 "column_edges")
    lift = load("ramsey_r55_m214_pair_cell_c5_lift/build.py", "pair_lift")
    parameters = dict(line.split("\t") for line in
                      (REPO / "ramsey_r55_m214_pair_column_hull/edge_parameters.tsv")
                      .read_text().splitlines()[1:])
    require({k: F(v) for k, v in parameters.items()} == edges.EDGE_PARAMETERS,
            "edge parameter table")
    triangle_values = {}
    for line in (REPO / "ramsey_r55_m214_pair_column_hull/triangle_orbits.tsv")\
            .read_text().splitlines()[1:]:
        sig, count, lower, upper, value = line.split("\t")
        require(sig not in triangle_values, "duplicate triangle signature")
        require(F(lower) <= F(value) <= F(upper) and int(count) > 0,
                "triangle table bounds")
        triangle_values[sig] = F(value)
    require(len(triangle_values) == 171, "triangle table size")

    edge = {ij: edges.edge_value(*ij) for ij in itertools.combinations(range(43), 2)}
    def x(i, j):
        return edge[min(i, j), max(i, j)]

    values = [None] + [(v, v) for v in edge.values()]
    for triple in itertools.combinations(range(43), 3):
        z = triangle_values[edges.signature_text(edges.signature(triple))]
        values.append((z, z))
    require(lift.ROOT_KEYS[48] == ("E8", 13, 0, "A"), "selected root")
    values.extend((F(i == 48), F(i == 48)) for i in range(389))

    exceptional = set(range(2, 15))
    core = set(range(15, 28))
    missed = {}
    for left, right, h in lift.MISSED_KEYS:
        if h in core and left not in core and right not in core:
            exceptional_count = (left in exceptional) + (right in exceptional)
            m = (F(1, 7), F(14, 65), F(7, 26))[exceptional_count]
        else:
            m = max(F(0), 1 - x(left, h) - x(right, h))
        missed[left, right, h] = m
        values.append((m, m))
    for left, right, i, j in lift.RED_INSIDE_KEYS:
        q = min(missed[left, right, i], missed[left, right, j], x(i, j))
        active = i in core and j in core and left not in core and right not in core
        values.append((F(3, 14) * q if active else q, q))
    require(len(values) == 98_759, "complete coordinate vector")
    require(all(0 <= a <= 1 and 0 <= b <= 1 for a, b in values[1:]), "box")
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    values = endpoints()
    with args.output.open("w", encoding="ascii") as out:
        out.write("variable\trho=3/14\trho=1\n")
        for i, (a, b) in enumerate(values[1:], 1):
            out.write(f"{i}\t{a}\t{b}\n")
    print("PASS endpoints=3/14,1 variables=98758")


if __name__ == "__main__":
    main()
