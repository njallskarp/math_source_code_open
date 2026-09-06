#!/usr/bin/env python3
"""Independent scope and replay audit for the interface-0 type-126 cohort."""

import argparse
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


TARGET_COMMIT = "ccc1580ba01738757795afa24f74e55af05f2aff"
TARGET_REF = "bafkreiagv3iecpt7t4azoq67xba7zzumqnhrpxvtfwrysdw3txn2g5xhei"
INPUT_HASHES = {
    "inputs.json": "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2",
    "certificate.json": "f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02",
}
EXPECTED_MANIFEST = "6d306dde34a449f0aa66a6b7054309f1396879f5d46e018751aaa9a0e0be28b0"
EXPECTED_MARKED_STREAM = "101b8d5bd81ddc273fa4f076a4d72bd3fcbd5d74b43890e3072aa208db702142"


class ReviewError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewError(message)


def load_json(path):
    return json.loads(path.read_text())


def decode_graph6(record):
    """Definition-level decoder, independent of the target's Python modules."""
    require(isinstance(record, str) and record, "empty graph6 record")
    require(all(63 <= ord(c) <= 126 for c in record), "invalid graph6 byte")
    n = ord(record[0]) - 63
    require(n < 63, "only short graph6 records are accepted")
    needed = n * (n - 1) // 2
    payload = "".join(format(ord(c) - 63, "06b") for c in record[1:])
    require(len(payload) == ((needed + 5) // 6) * 6, "graph6 payload length")
    require(set(payload[needed:]) <= {"0"}, "nonzero graph6 padding")
    edges = set()
    position = 0
    for v in range(n):
        for u in range(v):
            if payload[position] == "1":
                edges.add((u, v))
            position += 1
    return n, edges


def edge(u, v):
    return (u, v) if u < v else (v, u)


def is_clique(vertices, color, state):
    return all(state[edge(u, v)] == color for u, v in combinations(vertices, 2))


def reconstruct(edges, mark, columns):
    """Reconstruct all 903 physical pairs without importing target code."""
    pairs = list(combinations(range(43), 2))
    state = {pair: 2 for pair in pairs}

    def put(u, v, color):
        pair = edge(u, v)
        value = int(bool(color))
        require(state[pair] in (2, value), "conflicting physical pin")
        state[pair] = value

    for u, v in combinations(range(22), 2):
        put(u, v, (u, v) in edges)
    for v in range(43):
        if v != 22:
            put(22, v, v < 22)
    for v in range(23, 43):
        put(21, v, v < 40)
    residues = {1, 2, 4, 8, 9, 13, 15, 16}
    for u, v in combinations(range(23, 40), 2):
        put(u, v, (v - u) % 17 in residues)
    for row, physical_s in enumerate(mark):
        for t in range(17):
            put(physical_s, 23 + t, columns[row] >> t & 1)
    return state


def audit_local_graph(state, s):
    vertices = [22] + list(s) + list(range(23, 40))
    red_edges = sum(state[edge(u, v)] for u, v in combinations(vertices, 2))
    require(red_edges == 116, "local graph does not have density 116")
    degrees = {
        u: sum(state[edge(u, v)] for v in vertices if v != u)
        for u in vertices
    }
    require([u for u in vertices if degrees[u] == 5] == [22],
            "the distinguished hub is not the unique degree-five vertex")
    require(not any(is_clique(q, 1, state) for q in combinations(vertices, 4)),
            "red K4 in an asserted local representative")
    require(not any(is_clique(q, 0, state) for q in combinations(vertices, 5)),
            "blue K5 in an asserted local representative")


def parse_cnf(path, allowed_variables, expected_variables, expected_clauses):
    used = set()
    previous = None
    count = 0
    with path.open() as handle:
        header = handle.readline().split()
        require(header == ["p", "cnf", str(expected_variables), str(expected_clauses)],
                "DIMACS header mismatch: " + path.name)
        for line in handle:
            fields = [int(x) for x in line.split()]
            require(fields and fields[-1] == 0 and 0 not in fields[:-1],
                    "malformed DIMACS clause: " + path.name)
            clause = tuple(fields[:-1])
            require(1 <= len(clause) <= 10, "unexpected clause length")
            variables = {abs(x) for x in clause}
            require(variables <= allowed_variables, "outside variable used by kernel")
            require(previous is None or previous < clause, "clauses not strict canonical order")
            previous = clause
            used.update(variables)
            count += 1
    require(count == expected_clauses, "DIMACS clause count mismatch")
    require(used == allowed_variables, "kernel variable support is incomplete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path,
                        help="full public math_source_code_open checkout")
    parser.add_argument("replay_scratch", type=Path,
                        help="completed target reproduce.py scratch directory")
    args = parser.parse_args()

    root = args.checkout.resolve()
    scratch = args.replay_scratch.resolve()
    target = root / "ramsey_r55_type126_interface0_kernel"
    upstream = root / "ramsey_r55_dense_degree23_hub_classification"
    cohort = scratch / "cohort"

    for name, expected in INPUT_HASHES.items():
        raw = (upstream / name).read_bytes()
        require(sha256(raw).hexdigest() == expected, "upstream identity: " + name)
    inputs = load_json(upstream / "inputs.json")
    certificate = load_json(upstream / "certificate.json")

    n, h_edges = decode_graph6(inputs["interfaces"][0])
    require(n == 22 and len(h_edges) == 109, "interface order or density")
    degrees = [sum(edge(u, v) in h_edges for v in range(n) if v != u) for u in range(n)]
    require([u for u, degree in enumerate(degrees) if degree == 5] == [21],
            "interface does not have the stated unique hub")
    s = [u for u in range(21) if (u, 21) in h_edges]
    require(s == list(range(16, 21)), "unexpected common-neighborhood labels")
    s_edges = {edge(u, v) for u, v in combinations(s, 2) if edge(u, v) in h_edges}
    require(len(s_edges) == 6, "hub neighborhood is not K2,3")
    marks = []
    for mark in permutations(s):
        matches = all(
            (edge(mark[i], mark[j]) in s_edges) == (i < 2 <= j)
            for i, j in combinations(range(5), 2)
        )
        if matches:
            marks.append(mark)
    require(len(marks) == 12, "relative K2,3 marking count")

    families = [family for family in certificate["families"] if family["type"] == 126]
    require(len(families) == 1, "type-126 family multiplicity")
    representatives = families[0]["representatives"]
    require(len(representatives) == 29, "type-126 equality representative count")

    source_manifest_raw = (target / "MANIFEST.json").read_bytes()
    replay_manifest_raw = (cohort / "manifest.json").read_bytes()
    require(source_manifest_raw == replay_manifest_raw, "replayed manifest differs from source")
    require(sha256(source_manifest_raw).hexdigest() == EXPECTED_MANIFEST,
            "complete manifest digest")
    manifest = load_json(target / "MANIFEST.json")
    require(len(manifest) == 348, "manifest length")
    manifest_by_key = {tuple(row["key"]): row for row in manifest}
    require(len(manifest_by_key) == 348, "duplicate manifest key")

    pairs = list(combinations(range(43), 2))
    expected_free = (
        {edge(u, v) for u in range(16) for v in range(23, 40)}
        | {edge(u, v) for u in range(16) for v in range(40, 43)}
        | {edge(u, v) for u in s for v in range(40, 43)}
        | {edge(u, v) for u in range(23, 40) for v in range(40, 43)}
        | set(combinations(range(40, 43), 2))
    )
    require(len(expected_free) == 389, "free-pair partition arithmetic")

    marked_stream = sha256()
    matrices_seen = set()
    clause_min, clause_max = 10**9, 0
    for representative_index, representative in enumerate(representatives):
        columns = representative["columns"]
        require(len(columns) == 5 and all(isinstance(x, int) and 0 <= x < 2**17 for x in columns),
                "malformed equality columns")
        require(sum(x.bit_count() for x in columns) == 37, "equality cross-edge count")
        for marking_index, mark in enumerate(marks):
            key = (0, 126, representative_index, marking_index)
            state = reconstruct(h_edges, mark, columns)
            free = {pair for pair, color in state.items() if color == 2}
            require(free == expected_free, "physical free-edge scope")
            raw = bytes(48 + state[pair] for pair in pairs)
            require(raw not in matrices_seen, "duplicate marked physical template")
            matrices_seen.add(raw)
            marked_stream.update((" ".join(map(str, key)) + "\n").encode())
            marked_stream.update(bytes(value - 48 for value in raw))
            if marking_index == 0:
                audit_local_graph(state, s)

            generated_matrix = cohort / ("-".join(map(str, key)) + ".matrix")
            require(generated_matrix.read_bytes() == raw, "replay matrix mismatch")
            row = manifest_by_key[key]
            require(sha256(raw).hexdigest() == row["matrix_sha256"], "matrix digest mismatch")

            variable_ids = {
                pair: index + 1
                for index, pair in enumerate(pair for pair in pairs if pair in free)
            }
            active = {identifier for pair, identifier in variable_ids.items() if pair[1] < 40}
            require(len(variable_ids) == 389 and len(active) == 272,
                    "physical/kernel variable split")
            cnf = cohort / ("-".join(map(str, key)) + ".cnf")
            require(sha256(cnf.read_bytes()).hexdigest() == row["cnf_sha256"],
                    "formula digest mismatch")
            require(row["variables"] == 389, "formula variable count")
            parse_cnf(cnf, active, 389, row["clauses"])
            clause_min = min(clause_min, row["clauses"])
            clause_max = max(clause_max, row["clauses"])

    require(len(matrices_seen) == 348, "complete marked-template count")
    require(marked_stream.hexdigest() == EXPECTED_MARKED_STREAM, "marked-template stream digest")

    runs = load_json(cohort / "runs.json")
    require(len(runs) == 348, "proof run count")
    proof_index = sha256()
    proof_bytes = 0
    for run, row in zip(runs, manifest):
        key = tuple(run["key"])
        require(key == tuple(row["key"]), "proof run order")
        require(all(run[name] == row[name] for name in
                    ("variables", "clauses", "cnf_sha256", "matrix_sha256")),
                "run/manifest mismatch")
        stem = "-".join(map(str, key))
        proof = (cohort / (stem + ".drat")).read_bytes()
        require(proof and sha256(proof).hexdigest() == run["proof_sha256"],
                "proof trace identity")
        require("s UNSATISFIABLE" in (cohort / (stem + ".solver.log")).read_text(),
                "solver log lacks UNSAT")
        checker_log = (cohort / (stem + ".check.log")).read_text()
        require("s VERIFIED" in checker_log, "checker log lacks VERIFIED")
        require(run["solver_seconds"] >= 0 and run["checker_seconds"] >= 0,
                "negative timing")
        proof_bytes += len(proof)
        proof_index.update((stem + " " + run["proof_sha256"] + " " + str(len(proof)) + "\n").encode())

    result = load_json(cohort / "result.json")
    require(result == load_json(target / "EXPECTED.json"), "final result mismatch")
    require(result["status"] == "VERIFIED_COMPLETE_INTERFACE0_TYPE126_DENSITY116_EXCLUSION",
            "unexpected final status")

    output = {
        "status": "ACCEPTED_WITH_EXPLICIT_IMPORTS",
        "target_ref": TARGET_REF,
        "target_commit": TARGET_COMMIT,
        "cases": 348,
        "representatives": 29,
        "relative_markings": 12,
        "unique_physical_matrices": len(matrices_seen),
        "fixed_pairs_per_case": 514,
        "free_pairs_per_case": 389,
        "kernel_variables_per_case": 272,
        "clause_range": [clause_min, clause_max],
        "proofs_verified_from_logs": len(runs),
        "proof_bytes": proof_bytes,
        "manifest_sha256": sha256(source_manifest_raw).hexdigest(),
        "marked_template_sha256": marked_stream.hexdigest(),
        "proof_trace_index_sha256": proof_index.hexdigest(),
        "imported": [
            "completeness of the 29-representative equality catalogue",
            "Paley-17 uniqueness for the outside red neighborhood",
            "U(23)=122 only for deficiency wording",
            "soundness of drat-trim and ordinary compiler/hardware semantics",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
