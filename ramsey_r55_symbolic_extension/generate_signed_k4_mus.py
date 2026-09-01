#!/usr/bin/env python3
"""Generate a compact signed-K4 extension obstruction certificate.

This generator uses pinned PySAT backends to emit a DRUP refutation and one
model for every single-clause deletion.  The resulting JSON is checked by the
dependency-free verify_signed_k4_mus.py; solver output is not trusted directly.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib

import pysat
from pysat.solvers import Cadical195, Glucose42


DATA_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
DATA_URL = "https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6"
ORDER = 42
GRAPH_INDEX = 0
CORE_INDICES = (
    28, 36, 172, 179, 276, 411, 479, 486, 514, 515, 516, 527, 532, 547,
    548, 549, 555, 578, 581, 582, 589, 593, 664, 692, 738, 756, 758, 759,
    761, 763, 765, 906, 909, 928, 931, 946, 1052, 1184, 1199, 1271, 1316,
    1419, 1465, 1488, 1497, 1552, 1619, 1650, 1663, 1677, 1692, 1768,
    1772, 1887, 1900, 1996, 2170, 2175, 2190, 2192, 2211, 2215, 2216,
    2217, 2220, 2247, 2252, 2253, 2254, 2255, 2304, 2306, 2309, 2311,
)


def file_sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6(record: bytes) -> list[int]:
    """Return adjacency bitsets for a small graph6 record."""
    if not record or record.startswith(b">>"):
        raise ValueError("only headerless small graph6 records are accepted")
    order = record[0] - 63
    if order != ORDER:
        raise ValueError(f"expected order {ORDER}, found {order}")
    bits = (
        (byte - 63 >> shift) & 1
        for byte in record[1:]
        for shift in range(5, -1, -1)
    )
    adjacency = [0] * order
    for right in range(1, order):
        for left in range(right):
            if next(bits):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


def signed_k4_clauses(adjacency: list[int]):
    clauses: list[tuple[int, ...]] = []
    labels: list[tuple[str, tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(ORDER), 4):
        edge_count = sum(
            (adjacency[vertices[i]] >> vertices[j]) & 1
            for i in range(4)
            for j in range(i + 1, 4)
        )
        if edge_count == 6:
            clauses.append(tuple(-(vertex + 1) for vertex in vertices))
            labels.append(("red", vertices))
        elif edge_count == 0:
            clauses.append(tuple(vertex + 1 for vertex in vertices))
            labels.append(("blue", vertices))
    return clauses, labels


def model_bits(model: list[int]) -> str:
    values = {abs(literal): literal > 0 for literal in model}
    return "".join("1" if values[vertex] else "0" for vertex in range(1, ORDER + 1))


def generate(data_path: pathlib.Path) -> dict[str, object]:
    if file_sha256(data_path) != DATA_SHA256:
        raise ValueError("authoritative graph6 file SHA-256 mismatch")
    records = data_path.read_bytes().splitlines()
    if len(records) != 328:
        raise ValueError(f"expected 328 graph6 records, found {len(records)}")
    record = records[GRAPH_INDEX]
    adjacency = decode_graph6(record)
    clauses, labels = signed_k4_clauses(adjacency)
    core = [clauses[index] for index in CORE_INDICES]

    with Cadical195(bootstrap_with=core) as solver:
        if solver.solve():
            raise AssertionError("fixed core unexpectedly satisfiable")

    with Glucose42(bootstrap_with=core, with_proof=True) as solver:
        if solver.solve():
            raise AssertionError("proof solver unexpectedly found a model")
        proof = solver.get_proof()

    witnesses = []
    for removed in range(len(core)):
        reduced = core[:removed] + core[removed + 1 :]
        with Cadical195(bootstrap_with=reduced) as solver:
            if not solver.solve():
                raise AssertionError(f"core is not minimal at clause {removed}")
            witnesses.append({
                "removed_core_index": removed,
                "assignment": model_bits(solver.get_model()),
            })

    core_records = []
    for core_index, full_index in enumerate(CORE_INDICES):
        color, vertices = labels[full_index]
        core_records.append({
            "core_index": core_index,
            "full_clause_index": full_index,
            "color": color,
            "vertices_zero_based": list(vertices),
            "dimacs_clause": list(clauses[full_index]),
        })

    return {
        "schema_version": 1,
        "claim": (
            "These 74 signed K4 clauses form a subset-minimal unsatisfiable "
            "one-vertex extension obstruction for authoritative graph 0."
        ),
        "variable_convention": (
            "DIMACS variable v+1 is true iff the new edge to zero-based core "
            "vertex v is red."
        ),
        "source": {
            "url": DATA_URL,
            "sha256": DATA_SHA256,
            "record_count": len(records),
            "graph_index": GRAPH_INDEX,
            "graph6_record_sha256": hashlib.sha256(record).hexdigest(),
        },
        "full_system": {
            "variable_count": ORDER,
            "clause_count": len(clauses),
            "red_clause_count": sum(color == "red" for color, _ in labels),
            "blue_clause_count": sum(color == "blue" for color, _ in labels),
        },
        "core": {
            "clause_count": len(core_records),
            "red_clause_count": sum(record["color"] == "red" for record in core_records),
            "blue_clause_count": sum(record["color"] == "blue" for record in core_records),
            "covered_vertex_count": len({v for record in core_records for v in record["vertices_zero_based"]}),
            "subset_minimal": True,
            "clauses": core_records,
        },
        "drup_proof": proof,
        "deletion_witnesses": witnesses,
        "generation": {
            "python_sat_version": pysat.__version__,
            "unsat_backend": "Glucose 4.2 through PySAT",
            "minimality_backend": "CaDiCaL 1.9.5 through PySAT",
            "note": "All solver claims require acceptance by the independent verifier.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", type=pathlib.Path)
    args = parser.parse_args()
    print(json.dumps(generate(args.graph6), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
