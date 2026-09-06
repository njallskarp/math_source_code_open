#!/usr/bin/env python3
"""Independent audit of the h3587 24-edge family and template coverage.

This checker imports data files, but no Python or C++ implementation, from the
reviewed public checkout.  The local model set is evaluated as a bit-parallel
truth table.  Global templates are reconstructed directly from the graph6
records and the pointed type-126 columns.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


TARGET = "ramsey_r55_type126_twenty_four_edge_kernel"
UPSTREAM = "ramsey_r55_dense_degree23_hub_classification"
INPUT_HASH = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
CERT_HASH = "f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02"
MANIFEST_HASH = "42e4692b75d87d3a34345238da60502d77c1b62b6ce20699473ff4e24f9c0a00"
MODEL_HASH = "272dc97a9946ae31e6e032511e0af7c621bd526fc351c3cc620db776151dfe54"
TEMPLATE_HASH = "150825996e25f472914c89da7fb467ad44e49345597f51455580082e368216f4"
G6 = (
    "Uv?IXZIhlRWjUXL[iphstCjRDY`slYrgyeF[??Bw",
    "Uv?IXZIhlRWjUXL[iphstfEi[dRug^MCw?}[??Bw",
)
PERM = tuple(range(16)) + (17, 16, 18, 20, 19, 21)
FREE = (
    (0, 16), (1, 17), (1, 18), (1, 19), (1, 20), (3, 17),
    (3, 19), (4, 16), (4, 17), (4, 19), (5, 16), (6, 16),
    (7, 17), (7, 18), (7, 19), (7, 20), (10, 16), (10, 19),
    (11, 20), (12, 18), (12, 19), (13, 20), (14, 18), (15, 16),
)
ADVERTISED_FORBIDDEN = {
    frozenset(x) for x in (
        (1,17),(1,19),(2,5),(2,6),(3,20),(3,23),(4,21),(5,19),
        (6,20),(6,23),(7,21),(7,24),(8,10),(8,12),(8,17),(9,13),
        (9,20),(10,18),(10,21),(11,12),(11,19),(11,22),(12,24),
        (13,16),(14,20),(15,18),(15,21),(16,19),(16,22),(17,18),
    )
}
ADVERTISED_MEETING = {
    frozenset(x) for x in (
        (2,8,9),(2,13,24),(3,4,5,14,15,16),(3,4,18),(3,5,22),
        (4,5,10,22),(14,15,23),(14,16,23),(18,22),(20,21),
    )
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def graph6(record: str) -> set[tuple[int, int]]:
    require(record and ord(record[0]) - 63 == 22, "graph6 order")
    bits = "".join(f"{ord(c)-63:06b}" for c in record[1:])
    bits = bits[: 22 * 21 // 2]
    result: set[tuple[int, int]] = set()
    pos = 0
    for v in range(22):
        for u in range(v):
            if bits[pos] == "1":
                result.add((u, v))
            pos += 1
    return result


def relabel(edges: set[tuple[int, int]], p: tuple[int, ...]) -> set[tuple[int, int]]:
    return {tuple(sorted((p[u], p[v]))) for u, v in edges}


def minimal_masks(rows: set[int]) -> set[int]:
    return {row for row in rows if not any(other != row and other & row == other for other in rows)}


def truth_column(variable: int, assignment_count: int) -> int:
    """Bit m is one iff bit `variable` is set in assignment m."""
    byte_count = assignment_count // 8
    if variable == 0:
        raw = bytes((0xAA,)) * byte_count
    elif variable == 1:
        raw = bytes((0xCC,)) * byte_count
    elif variable == 2:
        raw = bytes((0xF0,)) * byte_count
    else:
        block = 1 << (variable - 3)
        raw = (bytes(block) + bytes((0xFF,)) * block) * (byte_count // (2 * block))
    return int.from_bytes(raw, "little")


def local_audit(first: set[tuple[int, int]], second: set[tuple[int, int]]) -> dict:
    pairs22 = tuple(combinations(range(22), 2))
    moved = relabel(second, PERM)
    require(tuple(sorted(first ^ moved)) == FREE, "the 24 advertised disagreements")
    fixed = {e: int(e in first) for e in pairs22 if (e in first) == (e in moved)}
    variable = {e: i for i, e in enumerate(FREE)}

    red_rows: set[int] = set()
    red_five_rows: set[int] = set()
    blue_rows: set[int] = set()
    for q in combinations(range(22), 4):
        edges = tuple(combinations(q, 2))
        if all(fixed.get(e, 1) == 1 for e in edges):
            mask = sum(1 << variable[e] for e in edges if e in variable)
            require(mask != 0, "fixed red K4")
            red_rows.add(mask)
    for q in combinations(range(22), 5):
        edges = tuple(combinations(q, 2))
        if all(fixed.get(e, 1) == 1 for e in edges):
            mask = sum(1 << variable[e] for e in edges if e in variable)
            require(mask != 0, "fixed red K5")
            red_five_rows.add(mask)
        if all(fixed.get(e, 0) == 0 for e in edges):
            mask = sum(1 << variable[e] for e in edges if e in variable)
            require(mask != 0, "fixed blue K5")
            blue_rows.add(mask)
    red_min = minimal_masks(red_rows)
    blue_min = minimal_masks(blue_rows)
    require({frozenset(i + 1 for i in range(24) if row >> i & 1) for row in red_min}
            == ADVERTISED_FORBIDDEN, "derived red-K4 clauses")
    require({frozenset(i + 1 for i in range(24) if row >> i & 1) for row in blue_min}
            == ADVERTISED_MEETING, "derived blue-K5 clauses")

    assignments = 1 << 24
    universe = (1 << assignments) - 1
    columns = [truth_column(i, assignments) for i in range(24)]
    invalid = 0
    for row in red_rows:
        bad = universe
        for i in range(24):
            if row >> i & 1:
                bad &= columns[i]
        invalid |= bad
    for row in blue_rows:
        bad = universe
        for i in range(24):
            if row >> i & 1:
                bad &= universe ^ columns[i]
        invalid |= bad
    live = universe ^ invalid
    models: list[int] = []
    while live:
        bit = live & -live
        models.append(bit.bit_length() - 1)
        live ^= bit
    stream = "".join(f"{model}\n" for model in models).encode()
    require(len(models) == 995 and sha256(stream).hexdigest() == MODEL_HASH, "complete model stream")

    base_edges = {e for e, color in fixed.items() if color}
    histogram: Counter[int] = Counter()
    dense: list[int] = []
    for model in models:
        edges = base_edges | {e for e, i in variable.items() if model >> i & 1}
        degrees = Counter(v for e in edges for v in e)
        require([v for v in range(22) if degrees[v] == 5] == [21], "unique degree-five hub")
        s = {v for v in range(21) if tuple(sorted((v, 21))) in edges}
        require(s == set(range(16, 21)), "hub neighborhood S")
        s_degrees = sorted(sum(tuple(sorted((u, v))) in edges for v in s if v != u) for u in s)
        require(s_degrees == [2, 2, 2, 3, 3], "S induces K2,3")
        edge_count = len(edges)
        histogram[edge_count] += 1
        if edge_count == 109:
            dense.append(model)
    expected_histogram = {102: 3, 103: 44, 104: 190, 105: 343,
                          106: 284, 107: 109, 108: 20, 109: 2}
    require(dict(sorted(histogram.items())) == expected_histogram, "density polynomial")
    require(dense == [7166538, 9610677], "dense endpoints")
    require(len(base_edges) == 97, "fixed red-edge base")
    return {
        "dense_masks": dense,
        "density_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "fixed_red_edges": len(base_edges),
        # These are the distinct monochromatic-five clauses after adjoining a
        # universal red root: red K4s with the root, red K5s without it, and
        # blue K5s without it.
        "literal_clause_count": len(red_rows | red_five_rows) + len(blue_rows),
        "minimal_blue_five_clauses": len(blue_min),
        "minimal_red_four_clauses": len(red_min),
        "model_count": len(models),
        "model_sha256": sha256(stream).hexdigest(),
    }


def markings(edges: set[tuple[int, int]]) -> list[tuple[int, ...]]:
    s = [v for v in range(21) if tuple(sorted((v, 21))) in edges]
    require(s == list(range(16, 21)), "marked S")
    result = []
    for mark in permutations(s):
        desired = {tuple(sorted((mark[i], mark[j]))) for i in range(2) for j in range(2, 5)}
        actual = {e for e in edges if e[0] in s and e[1] in s}
        if desired == actual:
            result.append(mark)
    require(len(result) == 12, "12 literal K2,3 markings")
    return result


def matrix(edges: set[tuple[int, int]], mark: tuple[int, ...], columns: list[int],
           common: set[tuple[int, int]] | None = None) -> bytes:
    pairs43 = tuple(combinations(range(43), 2))
    colors: dict[tuple[int, int], int] = {}
    for e in combinations(range(22), 2):
        if common is None or e in common:
            colors[e] = int(e in edges)
    for v in range(43):
        if v != 22:
            colors[tuple(sorted((22, v)))] = int(v < 22)
    for v in range(23, 43):
        colors[(21, v)] = int(v < 40)
    squares = {x * x % 17 for x in range(1, 17)}
    for u, v in combinations(range(17), 2):
        colors[(u + 23, v + 23)] = int((u - v) % 17 in squares)
    for i, vertex in enumerate(mark):
        for t in range(17):
            colors[tuple(sorted((vertex, t + 23)))] = (columns[i] >> t) & 1
    return bytes(48 + colors.get(e, 2) for e in pairs43)


def literal_cnf(raw: bytes) -> tuple[int, str]:
    """Build the 40-vertex necessary kernel by scanning all 5-subsets."""
    pairs43 = tuple(combinations(range(43), 2))
    pair_index = {e: i for i, e in enumerate(pairs43)}
    variables = {e: i + 1 for i, (e, color) in enumerate((e, c) for e, c in zip(pairs43, raw)
                                                          if c == 50)}
    clauses: set[tuple[int, ...]] = set()
    for q in combinations(range(40), 5):
        free: list[int] = []
        fixed_blue = fixed_red = False
        for e in combinations(q, 2):
            color = raw[pair_index[e]]
            fixed_blue |= color == 48
            fixed_red |= color == 49
            if color == 50:
                free.append(variables[e])
        if not fixed_red:
            clauses.add(tuple(free))
        if not fixed_blue:
            clauses.add(tuple(-v for v in free))
    data = (f"p cnf {len(variables)} {len(clauses)}\n"
            + "".join(" ".join(map(str, clause)) + " 0\n" for clause in sorted(clauses))).encode()
    return len(clauses), sha256(data).hexdigest()


def global_audit(first: set[tuple[int, int]], second: set[tuple[int, int]],
                 certificate: dict, manifest_path: Path) -> dict:
    families = [f for f in certificate["families"] if f["type"] == 126]
    require(len(families) == 1 and len(families[0]["representatives"]) == 29,
            "29 pointed type-126 representatives")
    reps = families[0]["representatives"]
    require(all(len(r["columns"]) == 5 and sum(x.bit_count() for x in r["columns"]) == 37
                for r in reps), "equality-column shape")
    moved = relabel(second, PERM)
    common = {e for e in combinations(range(22), 2) if (e in first) == (e in moved)}
    target_marks = markings(first)
    targets: dict[tuple[int, int], bytes] = {}
    for j, rep in enumerate(reps):
        for k, mark in enumerate(target_marks):
            targets[j, k] = matrix(first, mark, rep["columns"], common)
    require(len(set(targets.values())) == 348, "348 distinct partial templates")
    require({raw.count(b"2") for raw in targets.values()} == {413}, "413 free physical pairs")
    active_positions = [i for i, e in enumerate(combinations(range(43), 2)) if e[1] < 40]
    require({sum(raw[i] == 50 for i in active_positions) for raw in targets.values()} == {296},
            "296 kernel variables")

    pairs43 = tuple(combinations(range(43), 2))
    pair_index = {e: i for i, e in enumerate(pairs43)}
    multiplicity = Counter()
    comparisons = 0
    for h, edges in enumerate((first, second)):
        p = tuple(range(43)) if h == 0 else PERM + tuple(range(22, 43))
        transport = [pair_index[tuple(sorted((p[u], p[v])))] for u, v in pairs43]
        for k, mark in enumerate(markings(edges)):
            target_k = target_marks.index(tuple(p[v] for v in mark))
            for j, rep in enumerate(reps):
                original = matrix(edges, mark, rep["columns"])
                target = targets[j, target_k]
                for i, to in enumerate(transport):
                    require(target[to] == 50 or target[to] == original[i], "fixed transport")
                    require(original[i] != 50 or target[to] == 50, "freedom preserved")
                    comparisons += 1
                multiplicity[j, target_k] += 1
    require(set(multiplicity.values()) == {2}, "two endpoint preimages per partial template")

    template_digest = sha256()
    for key, raw in targets.items():
        template_digest.update(f"{key[0]} {key[1]}\n".encode())
        template_digest.update(bytes(c - 48 for c in raw))
    require(template_digest.hexdigest() == TEMPLATE_HASH, "marked-template stream")
    manifest_raw = manifest_path.read_bytes()
    require(sha256(manifest_raw).hexdigest() == MANIFEST_HASH, "manifest identity")
    manifest = json.loads(manifest_raw)
    require(len(manifest) == 348, "manifest length")
    by_key = {tuple(row["key"]): row for row in manifest}
    require(set(by_key) == set(targets), "manifest keys")
    require(all(by_key[key]["matrix_sha256"] == sha256(raw).hexdigest()
                for key, raw in targets.items()), "all matrix hashes")
    require({row["variables"] for row in manifest} == {413}, "manifest variable counts")
    clause_range = [min(row["clauses"] for row in manifest), max(row["clauses"] for row in manifest)]
    require(clause_range == [22408, 22604], "manifest clause range")
    min_key = min(by_key, key=lambda key: (by_key[key]["clauses"], key))
    max_key = max(by_key, key=lambda key: (by_key[key]["clauses"], tuple(-x for x in key)))
    sample_keys = sorted({(0, 0), (14, 6), (28, 11), min_key, max_key})
    cnf_samples = {}
    for key in sample_keys:
        count, cnf_hash = literal_cnf(targets[key])
        require(count == by_key[key]["clauses"] and cnf_hash == by_key[key]["cnf_sha256"],
                "literal CNF sample")
        cnf_samples[f"{key[0]},{key[1]}"] = {"clauses": count, "sha256": cnf_hash}
    return {
        "active_kernel_variables": 296,
        "clause_range_imported_from_manifest": clause_range,
        "literal_cnf_samples": cnf_samples,
        "distinct_partial_templates": len(targets),
        "manifest_matrix_hashes_checked": len(targets),
        "manifest_sha256": sha256(manifest_raw).hexdigest(),
        "outside_variables": 117,
        "physical_edge_transports": comparisons,
        "preimages_per_template": 2,
        "template_sha256": template_digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_checkout", type=Path)
    args = parser.parse_args()
    root = args.source_checkout.resolve()
    target = root / TARGET
    upstream = root / UPSTREAM
    input_path = upstream / "inputs.json"
    cert_path = upstream / "certificate.json"
    require(digest(input_path) == INPUT_HASH, "pinned inputs.json")
    require(digest(cert_path) == CERT_HASH, "pinned certificate.json")
    inputs = json.loads(input_path.read_text())
    certificate = json.loads(cert_path.read_text())
    require(tuple(inputs["interfaces"][i] for i in (10, 11)) == G6, "literal interface records")
    first, second = map(graph6, G6)
    require(len(first) == len(second) == 109, "endpoint densities")
    result = {
        "global": global_audit(first, second, certificate, target / "MANIFEST.json"),
        "local": local_audit(first, second),
        "status": "INDEPENDENT_H3587_LOCAL_AND_TRANSPORT_AUDIT_PASSED",
        "trust_boundary": (
            "Imports pinned dense-hub inputs/certificate and manifest clause hashes; "
            "does not establish SAT unsatisfiability or catalogue completeness."
        ),
        "upstream_sha256": {"certificate.json": CERT_HASH, "inputs.json": INPUT_HASH},
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
