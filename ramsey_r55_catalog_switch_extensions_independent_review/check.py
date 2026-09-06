"""Clean-room physical-clause and official DRAT-trim audit of all 328 cases.

The checker imports no code from the reviewed artifact.  It expects a run
regenerated from that artifact because the 1.4 GiB run directory is deliberately
not republished.
"""

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import csv
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess


CATALOG_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
CASES_SHA256 = "e3262023b7883a5706650d5bd79b4bb4a9e4da8f4c25b3618faf37a69c4733dd"
CASE_COLUMNS = [
    "parent",
    "cnf_clauses",
    "core_clauses",
    "core_bytes",
    "proof_bytes",
    "cnf_sha256",
    "core_sha256",
    "proof_sha256",
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6(record):
    require(record and all(63 <= ord(char) <= 126 for char in record), "graph6 alphabet")
    order = ord(record[0]) - 63
    require(0 <= order < 63, "graph6 short-order encoding")
    pairs = order * (order - 1) // 2
    require(len(record) == 1 + (pairs + 5) // 6, "graph6 length")
    payload = 0
    for char in record[1:]:
        payload = (payload << 6) | (ord(char) - 63)
    padding = 6 * (len(record) - 1) - pairs
    require(payload & ((1 << padding) - 1) == 0, "graph6 padding")
    adjacency = [[False] * order for _ in range(order)]
    width = 6 * (len(record) - 1)
    position = 0
    for vertex in range(1, order):
        for earlier in range(vertex):
            edge = bool(payload >> (width - position - 1) & 1)
            adjacency[earlier][vertex] = adjacency[vertex][earlier] = edge
            position += 1
    return adjacency


def contains_clique(neighbors, size):
    def visit(candidates, needed):
        if needed == 0:
            return True
        if candidates.bit_count() < needed:
            return False
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if visit(candidates & neighbors[vertex], needed - 1):
                return True
        return False

    return visit((1 << len(neighbors)) - 1, size)


def is_ramsey_55(graph):
    order = len(graph)
    universe = (1 << order) - 1
    red = [sum(1 << v for v in range(order) if graph[u][v]) for u in range(order)]
    blue = [universe ^ (1 << u) ^ red[u] for u in range(order)]
    return not contains_clique(red, 5) and not contains_clique(blue, 5)


def parse_core(path):
    with path.open() as stream:
        header = stream.readline().split()
        require(len(header) == 4 and header[:2] == ["p", "cnf"], "DIMACS header")
        variables, declared = map(int, header[2:])
        require(variables == 83 and declared > 0, "DIMACS dimensions")
        clauses = []
        for line in stream:
            fields = line.split()
            require(fields and fields[-1] == "0", "DIMACS terminator")
            literals = tuple(map(int, fields[:-1]))
            variables_used = [abs(literal) for literal in literals]
            require(literals and all(1 <= var <= variables for var in variables_used), "literal range")
            require(len(set(variables_used)) == len(variables_used), "duplicate or opposite literals")
            clauses.append(literals)
    require(len(clauses) == declared, "DIMACS clause count")
    return clauses


def physical_type(graph, clause):
    order = len(graph)
    falsifying = {abs(literal): int(literal < 0) for literal in clause}
    spins = {var: value for var, value in falsifying.items() if var < order}
    added = {var - order: value for var, value in falsifying.items() if var >= order}
    if added:
        require(len(added) == 4 and all(0 <= vertex < order for vertex in added), "added vertices")
        vertices = sorted(added)
        require(set(spins) == set(vertices) - {0}, "added-clause switch support")
        require(len(set(added.values())) == 1, "added-edge colors")
        colors = set(added.values())
        category = "added"
    else:
        require(len(spins) in (4, 5), "core-clause width")
        vertices = sorted(spins) if len(spins) == 5 else [0] + sorted(spins)
        require(len(vertices) == 5 and len(set(vertices)) == 5, "core vertices")
        colors = set()
        category = "core"
    spins[0] = 0
    colors.update(
        graph[u][v] ^ spins[u] ^ spins[v] for u, v in combinations(vertices, 2)
    )
    require(len(colors) == 1, "clause does not force one physical monochromatic K5")
    return f"{category}_color_{colors.pop()}"


def verify_case(task):
    index, record, row, run, drat_trim = task
    folder = run / f"parent{index:03d}"
    family = folder / "family.cnf"
    core = folder / "core.cnf"
    proof = folder / "trimmed.drat"
    require(row["parent"] == str(index), f"case-table parent {index}")
    for path, key in [
        (family, "cnf_sha256"),
        (core, "core_sha256"),
        (proof, "proof_sha256"),
    ]:
        require(path.is_file() and file_sha256(path) == row[key], f"case hash {index}/{path.name}")
    require(core.stat().st_size == int(row["core_bytes"]), f"core bytes {index}")
    require(proof.stat().st_size == int(row["proof_bytes"]), f"proof bytes {index}")
    with family.open() as stream:
        family_header = stream.readline().split()
    require(
        family_header[:3] == ["p", "cnf", "83"]
        and int(family_header[3]) == int(row["cnf_clauses"]),
        f"family dimensions {index}",
    )
    graph = decode_graph6(record)
    require(len(graph) == 42 and is_ramsey_55(graph), f"catalog parent is not Ramsey(5,5): {index}")
    clauses = parse_core(core)
    require(len(clauses) == int(row["core_clauses"]), f"core clauses {index}")
    physical = Counter(physical_type(graph, clause) for clause in clauses)
    checked = subprocess.run(
        [str(drat_trim), str(core), str(proof), "-f"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    transcript = checked.stdout + checked.stderr
    require(checked.returncode == 0 and "s VERIFIED" in transcript, f"DRAT-trim failed: {index}")
    return index, len(clauses), dict(physical)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    require(1 <= args.jobs <= 8, "worker count")
    require(args.run.is_dir(), "run directory")
    require(args.drat_trim.is_file(), "DRAT-trim executable")
    require(file_sha256(args.catalog) == CATALOG_SHA256, "catalog identity")
    require(file_sha256(args.cases) == CASES_SHA256, "case-table identity")
    records = args.catalog.read_text(encoding="ascii").splitlines()
    require(len(records) == 328 and len(set(records)) == 328, "catalog coverage")
    with args.cases.open(newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        require(reader.fieldnames == CASE_COLUMNS, "case-table columns")
        rows = list(reader)
    require(len(rows) == 328, "case-table coverage")
    tasks = [
        (index, record, rows[index], args.run.resolve(), args.drat_trim.resolve())
        for index, record in enumerate(records)
    ]
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(verify_case, tasks))
    require([result[0] for result in results] == list(range(328)), "ordered coverage")
    physical = Counter()
    for _, _, counts in results:
        physical.update(counts)
    output = {
        "status": "INDEPENDENT_FULL_CATALOG_SWITCH_REPLAY_PASS",
        "parents": len(results),
        "catalog_records_distinct": len(set(records)),
        "catalog_ramsey_55_parents": len(results),
        "normalized_variables_per_parent": 83,
        "official_drat_trim_proofs_verified": len(results),
        "full_formula_hashes_matched": len(results),
        "core_hashes_matched": len(results),
        "trimmed_proof_hashes_matched": len(results),
        "core_clauses_total": sum(result[1] for result in results),
        "core_clause_range": [min(result[1] for result in results), max(result[1] for result in results)],
        "physical_clauses": dict(sorted(physical.items())),
        "catalog_sha256": CATALOG_SHA256,
        "cases_tsv_sha256": CASES_SHA256,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
