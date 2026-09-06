#!/usr/bin/env python3
"""Produce the old survivor and two exactly repaired endpoints."""

import argparse
import hashlib
import importlib.util
import itertools as it
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PINS = {
    "ramsey_r55_m214_coupled_column_separator/witness.py":
        "3aa2b69e190a52bdff12f34c20ba3a6d0bde3d6fb5a2eeec343d538093013cf9",
    "ramsey_r55_m214_pair_column_hull/derive_fractional_certificate.py":
        "e4508d3d79b5af10b5b195c76f84cfb96f8a2ed4fffc5a774db5bbf5268c145e",
}
HEADER = "variable\tbaseline_rho=3/14\trepaired_rho=3/14\trepaired_rho=10/39\n"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(relative, name):
    path = REPO / relative
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[relative],
            "changed predecessor: " + relative)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def values():
    old = load("ramsey_r55_m214_coupled_column_separator/witness.py", "old_witness")
    classes = load("ramsey_r55_m214_pair_column_hull/derive_fractional_certificate.py",
                   "triangle_classes")
    previous = old.endpoints()
    result = [None]
    for a, b in previous[1:]:
        result.append((a, a, F(10, 39)*b if a != b else a))
    rows = (HERE / "triangle_orbits.tsv").read_text().splitlines()
    require(rows[0] == "signature\ttriples\tlower\tupper\tz", "triangle header")
    orbits = classes.orbit_table()
    require(len(rows) == len(orbits)+1 == 172, "triangle table size")
    replacement = {}
    for line, orbit in zip(rows[1:], orbits):
        sig, count, low, high, z = line.split("\t")
        require(sig == classes.signature_text(orbit[0]) and int(count) == orbit[1],
                "triangle class")
        require((F(low), F(high)) == (orbit[3], orbit[4]) and F(low) <= F(z) <= F(high),
                "triangle bounds")
        replacement[sig] = F(z)
    for index, triple in enumerate(it.combinations(range(43), 3), 904):
        z = replacement[classes.signature_text(classes.signature(triple))]
        result[index] = (result[index][0], z, z)
    require(len(result) == 98_759, "coordinate count")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    vector = values()
    with args.output.open("w", encoding="ascii") as handle:
        handle.write(HEADER)
        for index, row in enumerate(vector[1:], 1):
            handle.write(str(index)+"\t"+"\t".join(map(str, row))+"\n")
    print("PASS variables=98758 points=3")


if __name__ == "__main__":
    main()
