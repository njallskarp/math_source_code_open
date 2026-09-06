#!/usr/bin/env python3
"""Expand exact triangle atoms into a full old vector and all wedge moments."""

import argparse
import hashlib
import importlib.util
import itertools as it
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PINS = {
    "ramsey_r55_m214_reanchored_moment_hull/witness.py":
        "90c9ce236e52c157f18dba18b91144f8a1ff9869e63ad35120e407b1984f393e",
    "ramsey_r55_m214_reanchored_moment_hull/check.py":
        "e71b51d8485b23a955cba03c88b7a6db794780455682a9a1d1cde30e534e47ed",
}
H = frozenset(range(15, 28))
X = frozenset(range(2, 43)) - H
E = frozenset(range(2, 15))
MOMENT_HEADER = "a\tb\tc\tm_a\tm_b\tm_c\n"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(relative, name):
    path = REPO / relative
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[relative], "changed " + relative)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base():
    prior = load("ramsey_r55_m214_reanchored_moment_hull/witness.py", "previous_producer")
    classes = prior.load("ramsey_r55_m214_pair_column_hull/derive_fractional_certificate.py",
                         "edge_classes")
    return prior, classes


def canonical(triple, classes):
    def key(order):
        return (tuple(classes.TYPE_INDEX[classes.VERTEX_TYPE[v]] for v in order),
                tuple(classes.edge_value(a, b) for a, b in it.combinations(order, 2)))
    order = min(it.permutations(triple), key=key)
    return key(order), order


def read_atoms():
    result = {}
    for row in json.loads((HERE / "moment_atoms.json").read_text()):
        require(set(row) == {"types", "edges", "atoms"}, "atom fields")
        key = (tuple(row["types"]), tuple(map(F, row["edges"])))
        atoms = tuple(map(F, row["atoms"]))
        require(key not in result and len(atoms) == 8, "atom template")
        require(min(atoms) >= 0 and sum(atoms) == 1, "atom probability")
        result[key] = atoms
    require(len(result) == 171, "template count")
    return result


def values():
    prior, classes = base()
    decoder = load("ramsey_r55_m214_reanchored_moment_hull/check.py", "previous_decoder")
    _, _, missed, q = decoder.decoder()
    old = prior.values()
    vector = [old[0]] + [list(row) for row in old[1:]]
    templates, moments, used = read_atoms(), {}, set()
    for index, triple in enumerate(it.combinations(range(43), 3), 904):
        key, order = canonical(triple, classes)
        probabilities = templates[key]
        used.add(key)
        pairs = tuple(it.combinations(order, 2))
        for i, pair in enumerate(pairs):
            require(sum(p for mask, p in enumerate(probabilities) if mask >> i & 1)
                    == classes.edge_value(*pair), "edge marginal")
        vector[index][1:] = [probabilities[7]] * 2
        for h in triple:
            outside = tuple(v for v in triple if v != h)
            incident = [i for i, pair in enumerate(pairs) if h in pair]
            moments[outside + (h,)] = sum(p for mask, p in enumerate(probabilities)
                                         if all(not (mask >> i & 1) for i in incident))
    require(used == set(templates), "unused template")
    for key, index in missed.items():
        vector[index][1:] = [moments[key]] * 2
    for (a, b, i, j), index in q.items():
        edge = classes.edge_value(i, j)
        if {i, j} <= H and {a, b} <= X:
            m = moments[a, b, i]
            require(m == moments[a, b, j], "active equal column values")
            vector[index][1:] = [F(3, 14)*edge*m, F(10, 39)*edge*m]
        else:
            value = min(moments[a, b, i], moments[a, b, j], edge)
            vector[index][1:] = [value, value]
    require(len(vector) == 98_759 and len(moments) == 37_023, "coordinate count")
    return prior.HEADER, vector, moments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vector", type=Path, required=True)
    parser.add_argument("--moments", type=Path, required=True)
    args = parser.parse_args()
    header, vector, moments = values()
    with args.vector.open("w", encoding="ascii") as handle:
        handle.write(header)
        for index, row in enumerate(vector[1:], 1):
            handle.write(str(index) + "\t" + "\t".join(map(str, row)) + "\n")
    with args.moments.open("w", encoding="ascii") as handle:
        handle.write(MOMENT_HEADER)
        for triple in it.combinations(range(43), 3):
            row = tuple(moments[tuple(v for v in triple if v != h) + (h,)] for h in triple)
            handle.write("\t".join(map(str, triple + row)) + "\n")
    print("PASS old_coordinates=98758 full_wedges=37023 new_coordinates=26411")


if __name__ == "__main__":
    main()
