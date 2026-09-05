"""Solver-free verification of the eight-clause third-anchor obstruction."""
from __future__ import annotations

import base64
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LOCAL_UPPER = {20: 100, 21: 107, 22: 114}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def decode_graph6(encoded):
    raw = base64.b64decode(encoded, validate=True)
    require(bool(raw), "empty graph6")
    order = raw[0] - 63
    require(0 <= order <= 62, "small graph6 order")
    bit_count = order * (order - 1) // 2
    require(len(raw) == 1 + (bit_count + 5) // 6, "graph6 length")
    bits = []
    for value in raw[1:]:
        require(63 <= value <= 126, "graph6 alphabet")
        bits.extend(((value - 63) >> bit) & 1 for bit in range(5, -1, -1))
    require(not any(bits[bit_count:]), "graph6 padding")
    edges = set()
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.add((left, right))
            cursor += 1
    return order, edges


def construct(data):
    require(data["format"] == "r55-d22-two-anchor-width2-gap-v1", "base format")
    require(data["anchors"] == [0, 3], "base anchors")
    order, red_core = decode_graph6(data["red_core_parent_graph6_base64"])
    require(order == 22 and len(red_core) == 114, "red parent core")
    for raw_edge in data["red_core_delete_edges"]:
        deleted = tuple(raw_edge)
        require(deleted in red_core, "red deletion")
        red_core.remove(deleted)
    order, blue_core = decode_graph6(data["blue_core_graph6_base64"])
    require(order == 20 and len(blue_core) == 100, "blue core")
    rows = data["cross_rows"]
    require(
        len(rows) == 22 and all(len(row) == 20 and set(row) <= {"0", "1"} for row in rows),
        "cross rows",
    )
    red = {(0, vertex) for vertex in range(1, 23)}
    red.update((a + 1, b + 1) for a, b in red_core)
    red.update(
        (a + 23, b + 23)
        for a, b in combinations(range(20), 2)
        if (a, b) not in blue_core
    )
    red.update(
        (a + 1, b + 23)
        for a, row in enumerate(rows)
        for b, bit in enumerate(row)
        if bit == "1"
    )
    return red


def color(red, pair):
    return pair in red


def check_local(red, root):
    rows = []
    for root_color in (True, False):
        vertices = [
            vertex for vertex in range(43)
            if vertex != root and color(red, edge(root, vertex)) == root_color
        ]
        same_edges = sum(color(red, pair) == root_color for pair in combinations(vertices, 2))
        for size, forbidden_color in ((4, root_color), (5, not root_color)):
            require(
                not any(
                    all(color(red, pair) == forbidden_color for pair in combinations(subset, 2))
                    for subset in combinations(vertices, size)
                ),
                f"base local property root={root},color={int(root_color)}",
            )
        rows.append([
            root,
            "R" if root_color else "B",
            len(vertices),
            same_edges,
            LOCAL_UPPER[len(vertices)] - same_edges,
        ])
    return rows


def derive_clause(red, diagonal, root, record):
    root_color = record["anchor_color"] == "R"
    forbidden_color = record["forbidden_color"] == "R"
    subset = tuple(record["subset"])
    require(len(subset) == len(set(subset)), "distinct subset")
    require(root not in subset and all(0 <= vertex < 43 for vertex in subset), "subset labels")
    expected_size = 4 if root_color == forbidden_color else 5
    require(len(subset) == expected_size, "local forbidden-set size")
    conditions = [(edge(root, vertex), root_color) for vertex in subset]
    conditions.extend((pair, forbidden_color) for pair in combinations(subset, 2))
    derived = set()
    for pair, required_color in conditions:
        if pair in diagonal:
            derived.add((pair[0], pair[1], "B" if required_color else "R"))
        else:
            require(color(red, pair) == required_color, "advertised fixed local literal")
    require(derived, "nonempty local clause")
    stored = {(left, right, label) for left, right, label in record["clause"]}
    require(all(edge(left, right) == (left, right) for left, right, _label in stored), "canonical clause edges")
    require(all(label in ("R", "B") for _left, _right, label in stored), "clause colors")
    require(stored == derived, "derived local clause")
    return tuple(sorted(stored))


def clause_holds(clause, assignment):
    return any(assignment[(left, right)] == (label == "R") for left, right, label in clause)


def audit(red, certificate):
    require(certificate["format"] == "r55-d22-third-anchor-unit-core-v1", "certificate format")
    require(certificate["fixed_anchors"] == [0, 3], "fixed anchors")
    require(certificate["third_anchor"] == 1, "third anchor")
    require(all(0 <= left < right < 43 for left, right in red), "simple canonical base")
    adjacency = [[False] * 43 for _ in range(43)]
    for left, right in red:
        adjacency[left][right] = adjacency[right][left] = True
    degrees = [sum(row) for row in adjacency]
    require(len(red) == 452, "base red edge count")
    require(Counter(degrees) == Counter({20: 8, 21: 26, 22: 9}), "base degree profile")
    local = check_local(red, 0) + check_local(red, 3)
    require(
        local == [[0, "R", 22, 108, 6], [0, "B", 20, 100, 0],
                  [3, "R", 21, 99, 8], [3, "B", 21, 98, 9]],
        "base local profiles",
    )

    outside = [vertex for vertex in range(43) if vertex not in (0, 3)]
    signature = {
        vertex: (int(adjacency[0][vertex]), int(adjacency[3][vertex]))
        for vertex in outside
    }
    cells = Counter(signature.values())
    require([cells[key] for key in ((1, 1), (1, 0), (0, 1), (0, 0))] == [10, 11, 10, 10], "cells")
    diagonal = {
        pair for pair in combinations(outside, 2)
        if all(signature[pair[0]][index] != signature[pair[1]][index] for index in range(2))
    }
    require(len(diagonal) == 210, "diagonal size")

    variables = [tuple(pair) for pair in certificate["variables"]]
    require(len(variables) == len(set(variables)) == 7, "seven variables")
    require(set(variables) <= diagonal, "variables are doubly unseen")
    clauses = [derive_clause(red, diagonal, 1, record) for record in certificate["constraints"]]
    require(len(clauses) == len(set(clauses)) == 8, "eight distinct clauses")
    require(set(edge(left, right) for clause in clauses for left, right, _label in clause) == set(variables), "variable support")

    satisfying = []
    deletion_counts = []
    deletion_examples = []
    for bits in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, bits))
        truth = [clause_holds(clause, assignment) for clause in clauses]
        if all(truth):
            satisfying.append(bits)
        for omitted in range(len(clauses)):
            if all(value for index, value in enumerate(truth) if index != omitted):
                if len(deletion_examples) <= omitted:
                    deletion_examples.extend([None] * (omitted + 1 - len(deletion_examples)))
                if deletion_examples[omitted] is None:
                    deletion_examples[omitted] = "".join("1" if bit else "0" for bit in bits)
    for omitted in range(len(clauses)):
        count = 0
        for bits in product((False, True), repeat=len(variables)):
            assignment = dict(zip(variables, bits))
            if all(clause_holds(clause, assignment) for index, clause in enumerate(clauses) if index != omitted):
                count += 1
        deletion_counts.append(count)
    require(not satisfying, "core is unsatisfiable")
    require(all(count > 0 for count in deletion_counts), "core is deletion-minimal")

    edge_text = "".join(f"{left} {right}\n" for left, right in sorted(red))
    fixed_text = "".join(
        f"{left} {right} {'R' if pair in red else 'B'}\n"
        for pair in combinations(range(43), 2)
        if pair not in diagonal
        for left, right in (pair,)
    )
    clause_text = "".join(
        " ".join(f"{left}-{right}-{label}" for left, right, label in clause) + "\n"
        for clause in clauses
    )
    return {
        "base_degree_profile": sorted(Counter(degrees).items()),
        "base_edge_sha256": sha256(edge_text.encode()).hexdigest(),
        "base_edges": len(red),
        "base_local_profiles": local,
        "cell_sizes": [cells[key] for key in ((1, 1), (1, 0), (0, 1), (0, 0))],
        "clause_sha256": sha256(clause_text.encode()).hexdigest(),
        "core_clauses": len(clauses),
        "core_variables": len(variables),
        "deletion_examples": deletion_examples,
        "deletion_satisfying_counts": deletion_counts,
        "diagonal_edges": len(diagonal),
        "fixed_incidence_sha256": sha256(fixed_text.encode()).hexdigest(),
        "satisfying_assignments": len(satisfying),
        "third_anchor": 1,
    }


def main():
    data = json.loads((HERE / "BASE_WITNESS.json").read_text())
    certificate = json.loads((HERE / "CERTIFICATE.json").read_text())
    print(json.dumps(audit(construct(data), certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
