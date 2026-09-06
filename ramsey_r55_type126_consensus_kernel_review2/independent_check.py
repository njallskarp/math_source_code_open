#!/usr/bin/env python3
"""Independent definition-level audit of Discovery Net h3505.

This checker imports no module from the reviewed package.  It reads the two
hash-pinned upstream data files and the reviewed compact certificates, then
reconstructs the local family, the 29 equality graphs, all 348 relaxed
physical templates, all 696 endpoint transports, and a stratified sample of
CNFs directly from the mathematical definitions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


UPSTREAM_HASHES = {
    "inputs.json": "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2",
    "certificate.json": "f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02",
}
PERMUTATION = (4, 6, 7, 5, 0, 3, 1, 2, 8, 12, 10, 15, 9, 13, 14, 11,
               17, 16, 19, 20, 18, 21)
FREE = ((0, 17), (0, 19), (1, 16), (1, 17), (3, 19), (6, 16),
        (8, 17), (8, 19), (11, 19), (13, 19), (14, 19), (15, 16))
CONFLICT = ((1, 2), (1, 7), (2, 5), (2, 8), (2, 9), (3, 5), (3, 6),
            (3, 8), (3, 9), (4, 7), (4, 11), (5, 10), (5, 11),
            (5, 12), (6, 12), (7, 8), (8, 10), (9, 11))
SAMPLE_KEYS = ((0, 0), (0, 11), (1, 5), (2, 7), (3, 9), (5, 3),
               (8, 8), (13, 4), (17, 10), (22, 1), (27, 6), (28, 11))
PAIR43 = tuple(combinations(range(43), 2))
INDEX43 = {e: i for i, e in enumerate(PAIR43)}
FIVE40 = tuple((q, tuple(combinations(q, 2))) for q in combinations(range(40), 5))


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path):
    return json.loads(path.read_text())


def decode_graph6(record: str) -> set[tuple[int, int]]:
    """Direct graph6 decoder for the short header used here."""
    demand(record and 63 <= ord(record[0]) < 126, "short graph6 header")
    n = ord(record[0]) - 63
    payload = []
    for char in record[1:]:
        value = ord(char) - 63
        demand(0 <= value < 64, "graph6 payload")
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need = n * (n - 1) // 2
    demand(len(payload) >= need and not any(payload[need:]), "graph6 padding")
    pairs = ((u, v) for v in range(n) for u in range(v))
    return {e for e, bit in zip(pairs, payload) if bit}


def has_clique(edges: set[tuple[int, int]], vertices: tuple[int, ...], size: int,
               red: bool) -> bool:
    for q in combinations(vertices, size):
        colors = ((tuple(sorted(e)) in edges) for e in combinations(q, 2))
        if all(colors) if red else not any(colors):
            return True
    return False


def moved(edges: set[tuple[int, int]], permutation: tuple[int, ...]) -> set[tuple[int, int]]:
    return {tuple(sorted((permutation[u], permutation[v]))) for u, v in edges}


def local_models(common: dict[tuple[int, int], int]) -> tuple[list[int], Counter[int]]:
    models, densities = [], Counter()
    forbidden_red = []
    forbidden_blue = []
    free_index = {e: i for i, e in enumerate(FREE)}
    for q in combinations(range(22), 4):
        values = [(common[e] if e in common else None) for e in combinations(q, 2)]
        if 0 not in values:
            forbidden_red.append(sum(1 << free_index[e] for e in combinations(q, 2)
                                     if e in free_index))
    for q in combinations(range(22), 5):
        values = [(common[e] if e in common else None) for e in combinations(q, 2)]
        if 1 not in values:
            forbidden_blue.append(sum(1 << free_index[e] for e in combinations(q, 2)
                                       if e in free_index))
    fixed_red = sum(common.values())
    for mask in range(1 << len(FREE)):
        red_ok = all(mask & required != required for required in forbidden_red)
        blue_ok = all((~mask) & ((1 << 12) - 1) & required != required
                      for required in forbidden_blue)
        if not (red_ok and blue_ok):
            continue
        models.append(mask)
        densities[fixed_red + mask.bit_count()] += 1
        degree = [0] * 22
        for e in combinations(range(22), 2):
            color = bool(mask >> free_index[e] & 1) if e in free_index else bool(common[e])
            if color:
                degree[e[0]] += 1
                degree[e[1]] += 1
        demand([v for v, d in enumerate(degree) if d == 5] == [21], "local unique hub")
    return models, densities


def markings(endpoint: set[tuple[int, int]]) -> tuple[tuple[int, ...], ...]:
    s = tuple(v for v in range(21) if (v, 21) in endpoint)
    demand(s == tuple(range(16, 21)), "literal hub neighbourhood")
    pattern = {(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)}
    result = []
    for order in permutations(s):
        induced = {ij for ij in combinations(range(5), 2)
                   if tuple(sorted((order[ij[0]], order[ij[1]]))) in endpoint}
        if induced == pattern:
            result.append(order)
    demand(len(result) == 12, "twelve K2,3 markings")
    return tuple(result)


def equality_graph(columns: list[int]) -> set[tuple[int, int]]:
    """Build J on r=0, S=1..5, T=6..22 from the displayed convention."""
    edges = {(0, s) for s in range(1, 6)}
    edges |= {(1 + i, 1 + j) for i in (0, 1) for j in (2, 3, 4)}
    squares = {x * x % 17 for x in range(1, 17)}
    edges |= {(6 + i, 6 + j) for i, j in combinations(range(17), 2)
              if (j - i) % 17 in squares}
    edges |= {(1 + s, 6 + t) for s in range(5) for t in range(17)
              if columns[s] >> t & 1}
    return edges


def template(endpoint: set[tuple[int, int]], common: dict[tuple[int, int], int],
             columns: list[int], mark: tuple[int, ...], relaxed: bool) -> list[int | None]:
    fixed: dict[tuple[int, int], int] = {}
    for e in combinations(range(22), 2):
        if not relaxed or e not in FREE:
            fixed[e] = int(e in endpoint) if not relaxed else common[e]
    for v in range(43):
        if v != 22:
            fixed[tuple(sorted((22, v)))] = int(v < 22)
    for v in range(23, 43):
        fixed[(21, v)] = int(v < 40)
    squares = {x * x % 17 for x in range(1, 17)}
    for u, v in combinations(range(23, 40), 2):
        fixed[(u, v)] = int((v - u) % 17 in squares)
    for s, physical in enumerate(mark):
        for t in range(17):
            fixed[(physical, 23 + t)] = (columns[s] >> t) & 1
    return [fixed.get(e) for e in PAIR43]


def formula(matrix: list[int | None]) -> bytes:
    free_pairs = (e for e in PAIR43 if matrix[INDEX43[e]] is None)
    variables = {e: i + 1 for i, e in enumerate(free_pairs)}
    clauses: set[tuple[int, ...]] = set()
    for _, pairs in FIVE40:
        states = [matrix[INDEX43[e]] for e in pairs]
        if 0 not in states:
            clauses.add(tuple(-variables[e] for e in pairs if e in variables))
        if 1 not in states:
            clauses.add(tuple(variables[e] for e in pairs if e in variables))
    return (f"p cnf {len(variables)} {len(clauses)}\n" +
            "".join(" ".join(map(str, clause)) + " 0\n" for clause in sorted(clauses))).encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="reviewed package directory")
    parser.add_argument("--upstream", type=Path, required=True,
                        help="reviewed upstream classification directory")
    args = parser.parse_args()

    blobs = {}
    for name, expected in UPSTREAM_HASHES.items():
        raw = (args.upstream / name).read_bytes()
        demand(sha256(raw).hexdigest() == expected, f"upstream hash {name}")
        blobs[name] = json.loads(raw)
    inputs, certificate = blobs["inputs.json"], blobs["certificate.json"]
    published_consensus = read_json(args.source / "CONSENSUS.json")
    demand(tuple(published_consensus["second_to_first"]) == PERMUTATION, "permutation transcription")
    demand(tuple(map(tuple, published_consensus["free_common_edges"])) == FREE, "free-edge transcription")

    first = decode_graph6(inputs["interfaces"][10])
    second = decode_graph6(inputs["interfaces"][12])
    second_moved = moved(second, PERMUTATION)
    demand(len(first) == len(second) == 109 and first ^ second_moved == set(FREE),
           "literal endpoints and twelve-edge consensus")
    common = {e: int(e in first) for e in combinations(range(22), 2) if e not in FREE}
    models, densities = local_models(common)
    model_bytes = "".join(f"{x}\n" for x in models).encode()
    demand(len(models) == 110, "110 local models")
    demand(densities == Counter({104: 2, 105: 15, 106: 37, 107: 38, 108: 16, 109: 2}),
           "local density polynomial")
    demand([m for m in models if 103 + m.bit_count() == 109] == [441, 3654], "dense endpoints")
    demand(sha256(model_bytes).hexdigest() ==
           "f886a266f5d70846d52afe5dc79443d38f6b1502cb82eac23d9785dd31ad872a",
           "local model hash")
    demand(all(bool(mask >> (i - 1) & 1) or bool(mask >> (j - 1) & 1)
               for mask in models for i, j in ((3, 4),)), "required meeting pair")
    demand(all(not ((mask >> (u - 1) & 1) and (mask >> (v - 1) & 1))
               for mask in models for u, v in CONFLICT), "conflict graph necessity")
    conflict_models = [mask for mask in range(1 << 12)
                       if mask & ((1 << 2) | (1 << 3))
                       and all(not (mask >> (u - 1) & 1 and mask >> (v - 1) & 1)
                               for u, v in CONFLICT)]
    demand(conflict_models == models, "conflict graph sufficiency")

    family = [f for f in certificate["families"] if f["type"] == 126]
    demand(len(family) == 1 and len(family[0]["representatives"]) == 29,
           "29 imported equality representatives")
    columns = [row["columns"] for row in family[0]["representatives"]]
    for j, row in enumerate(columns):
        graph = equality_graph(row)
        degree = Counter(v for e in graph for v in e)
        demand(len(graph) == 116, f"equality density {j}")
        demand([v for v in range(23) if degree[v] == 5] == [0], f"unique hub {j}")
        demand(not has_clique(graph, tuple(range(23)), 4, True), f"red K4 in equality graph {j}")
        demand(not has_clique(graph, tuple(range(23)), 5, False), f"blue K5 in equality graph {j}")

    target_marks = markings(first)
    manifest = read_json(args.source / "MANIFEST.json")
    manifest_by_key = {tuple(row["key"]): row for row in manifest}
    demand(set(manifest_by_key) == {(j, k) for j in range(29) for k in range(12)},
           "manifest key rectangle")
    matrices: dict[tuple[int, int], bytes] = {}
    marked = sha256()
    for j, row in enumerate(columns):
        for k, mark in enumerate(target_marks):
            values = template(first, common, row, mark, True)
            raw = bytes(50 if c is None else 48 + c for c in values)
            matrices[j, k] = raw
            demand(raw.count(b"2") == 401, f"physical freedom {(j, k)}")
            active_free = sum(c is None and e[1] < 40 for e, c in zip(PAIR43, values))
            demand(active_free == 284, f"kernel freedom {(j, k)}")
            demand(sha256(raw).hexdigest() == manifest_by_key[j, k]["matrix_sha256"],
                   f"matrix hash {(j, k)}")
            marked.update(f"{j} {k}\n".encode())
            marked.update(bytes(2 if c is None else c for c in values))
    demand(len(set(matrices.values())) == 348, "distinct relaxed templates")
    demand(marked.hexdigest() == "cc604bc250243288b5f4002c30f8b2315b885d6204f1064f28aa079681e2e528",
           "marked-template stream")

    transports = 0
    multiplicity = Counter()
    for h, endpoint in ((10, first), (12, second)):
        permutation = tuple(range(43)) if h == 10 else PERMUTATION + tuple(range(22, 43))
        edge_map = [INDEX43[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIR43]
        for k, mark in enumerate(markings(endpoint)):
            mapped_mark = tuple(permutation[v] for v in mark)
            target_k = target_marks.index(mapped_mark)
            for j, row in enumerate(columns):
                original = template(endpoint, common, row, mark, False)
                target = matrices[j, target_k]
                for index, target_index in enumerate(edge_map):
                    old, new = original[index], target[target_index] - 48
                    demand(new == 2 or new == old, "transported fixed color")
                    demand(old is not None or new == 2, "transported free edge")
                    transports += 1
                multiplicity[j, target_k] += 1
    demand(transports == 628_488 and set(multiplicity.values()) == {2}, "complete two-cohort transport")

    checked_formula = {}
    for key in SAMPLE_KEYS:
        data = formula([None if c == 50 else c - 48 for c in matrices[key]])
        row = manifest_by_key[key]
        demand(sha256(data).hexdigest() == row["cnf_sha256"], f"CNF hash {key}")
        header = data.splitlines()[0].decode()
        _, _, variable_count, clause_count = header.split()
        demand(int(variable_count) == row["variables"] == 401, f"CNF variables {key}")
        demand(int(clause_count) == row["clauses"], f"CNF clauses {key}")
        checked_formula[f"{key[0]}-{key[1]}"] = int(clause_count)

    result = {
        "status": "INDEPENDENT_H3505_DEFINITIONAL_CHECK_PASS",
        "upstream_hashes": UPSTREAM_HASHES,
        "local_assignments": 4096,
        "local_models": len(models),
        "local_model_sha256": sha256(model_bytes).hexdigest(),
        "density_histogram": dict(sorted(densities.items())),
        "dense_models": [441, 3654],
        "equality_representatives_checked": 29,
        "relaxed_matrices_checked": len(matrices),
        "matrix_hashes_matched": len(matrices),
        "endpoint_transports_checked": transports,
        "original_cases_covered": 696,
        "formula_sample": checked_formula,
        "formula_sample_size": len(checked_formula),
        "physical_free_edges": 401,
        "active_variables": 284,
        "inherited_not_reproved": ["completeness of the 29 equality representatives",
                                    "U(23)=122", "completeness of the 13-interface census"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
