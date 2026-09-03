#!/usr/bin/env python3
"""Check the sharp certificate for the genealogical four-incidence theorem.

The universal connectivity and cut theorems are proved in the accompanying
note.  This dependency-free program checks the exact resolution, provenance,
support-incidence, and Ramsey-coloring conventions on the compact witness.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import sys


def support(clause: frozenset[int]) -> frozenset[int]:
    return frozenset(abs(literal) for literal in clause)


def sign_of_pure_clause(clause: frozenset[int]) -> str:
    if len(clause) != 4:
        raise AssertionError("every leaf must have length four")
    if all(literal > 0 for literal in clause):
        return "positive"
    if all(literal < 0 for literal in clause):
        return "negative"
    raise AssertionError("every leaf must be pure by sign")


def connected(vertices: tuple[str, ...], edges: set[frozenset[str]]) -> bool:
    if not vertices:
        return False
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        current = stack.pop()
        for edge in edges:
            if current not in edge:
                continue
            for neighbor in edge:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return seen == set(vertices)


def verify(data: dict) -> dict[str, object]:
    clauses: dict[str, frozenset[int]] = {}
    colors: dict[str, str] = {}
    ancestry: dict[str, tuple[str, ...]] = {}
    child_sets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {}
    overlaps: dict[str, tuple[int, ...]] = {}

    for leaf in data["leaves"]:
        identifier = leaf["id"]
        if identifier in clauses:
            raise AssertionError("duplicate leaf identifier")
        clause = frozenset(leaf["clause"])
        if len(clause) != len(leaf["clause"]):
            raise AssertionError("duplicate literal in leaf")
        color = sign_of_pure_clause(clause)
        if color != leaf["color"]:
            raise AssertionError("serialized leaf color disagrees with literals")
        clauses[identifier] = clause
        colors[identifier] = color
        ancestry[identifier] = (identifier,)

    leaf_ids = tuple(ancestry)
    for left_index, left_id in enumerate(leaf_ids):
        for right_id in leaf_ids[left_index + 1 :]:
            if colors[left_id] != colors[right_id]:
                if len(support(clauses[left_id]) & support(clauses[right_id])) > 1:
                    raise AssertionError("opposite-color leaf supports intersect twice")

    for item in data["resolutions"]:
        identifier = item["id"]
        left_id, right_id = item["left"], item["right"]
        if identifier in clauses or left_id not in clauses or right_id not in clauses:
            raise AssertionError("resolution order or identifier is invalid")
        pivot = item["pivot"]
        left, right = clauses[left_id], clauses[right_id]
        if pivot not in left or -pivot not in right:
            raise AssertionError("declared complementary pivot is absent")
        clashes = {
            abs(literal)
            for literal in left
            if -literal in right
        }
        if clashes != {abs(pivot)}:
            raise AssertionError("parents do not resolve only on the declared pivot")
        left_tail = left - {pivot}
        right_tail = right - {-pivot}
        overlap = tuple(sorted(left_tail & right_tail, key=lambda x: (abs(x), x)))
        resolvent = left_tail | right_tail
        clauses[identifier] = resolvent
        ancestry[identifier] = ancestry[left_id] + ancestry[right_id]
        child_sets[identifier] = (ancestry[left_id], ancestry[right_id])
        overlaps[identifier] = overlap

    root = data["root"]
    expected = data["expected"]
    if tuple(sorted(clauses[root])) != tuple(expected["root_clause"]):
        raise AssertionError("wrong root clause")
    if len(ancestry[root]) != expected["leaf_occurrences"]:
        raise AssertionError("wrong unfolded leaf count")

    # Build the opposite-color intersection graph on leaf occurrences.  This
    # compact sharpness certificate uses distinct leaves; the written theorem
    # separately handles duplicated occurrences in an unfolded DAG ancestry.
    occurrence_ids = tuple(f"{leaf_id}@{index}" for index, leaf_id in enumerate(ancestry[root]))
    occurrence_leaf = dict(zip(occurrence_ids, ancestry[root]))
    bi_edges: set[frozenset[str]] = set()
    full_incidences: list[tuple[str, str, int, str]] = []
    for i, first in enumerate(occurrence_ids):
        leaf_first = occurrence_leaf[first]
        for second in occurrence_ids[i + 1 :]:
            leaf_second = occurrence_leaf[second]
            intersection = support(clauses[leaf_first]) & support(clauses[leaf_second])
            relation = "bichromatic" if colors[leaf_first] != colors[leaf_second] else "monochromatic"
            if relation == "bichromatic" and intersection:
                bi_edges.add(frozenset((first, second)))
            for variable in sorted(intersection):
                full_incidences.append((first, second, variable, relation))

    if len(bi_edges) != expected["bichromatic_intersection_edges"]:
        raise AssertionError("wrong bichromatic intersection edge count")
    if not connected(occurrence_ids, bi_edges):
        raise AssertionError("root bichromatic intersection graph is disconnected")

    # Connectivity must hold in every actual ancestry subtree.
    for node, node_leaves in ancestry.items():
        if len(node_leaves) == 1:
            continue
        positions = tuple(
            occurrence_ids[index]
            for index, leaf_id in enumerate(ancestry[root])
            if leaf_id in node_leaves
        )
        induced = {edge for edge in bi_edges if edge <= set(positions)}
        if not connected(positions, induced):
            raise AssertionError(f"bichromatic genealogy disconnected at {node}")

    four_cuts = 0
    for node, overlap_literals in overlaps.items():
        if len(overlap_literals) < 3:
            continue
        left_leaves, right_leaves = child_sets[node]
        pivot = next(item["pivot"] for item in data["resolutions"] if item["id"] == node)
        pivot_variable = abs(pivot)

        pivot_witness = False
        for left_leaf in left_leaves:
            for right_leaf in right_leaves:
                if colors[left_leaf] == colors[right_leaf]:
                    continue
                if pivot_variable in support(clauses[left_leaf]) & support(clauses[right_leaf]):
                    pivot_witness = True
        if not pivot_witness:
            raise AssertionError("no bichromatic leaf witness for pivot")

        overlap_labels: set[int] = set()
        for literal in overlap_literals:
            variable = abs(literal)
            witnessed = False
            for left_leaf in left_leaves:
                for right_leaf in right_leaves:
                    if colors[left_leaf] != colors[right_leaf]:
                        continue
                    if (literal > 0) != (colors[left_leaf] == "positive"):
                        continue
                    if variable in support(clauses[left_leaf]) & support(clauses[right_leaf]):
                        witnessed = True
            if not witnessed:
                raise AssertionError("no monochromatic leaf witness for overlap")
            overlap_labels.add(variable)
        if len(overlap_labels) < 3 or pivot_variable in overlap_labels:
            raise AssertionError("four-incidence labels are not distinct")
        four_cuts += 1

    maximum_overlap = max(map(len, overlaps.values()))
    if maximum_overlap != expected["maximum_nonpivot_overlap"]:
        raise AssertionError("wrong maximum overlap")
    if four_cuts != expected["four_incidence_cuts"]:
        raise AssertionError("wrong number of certified four-incidence cuts")

    # Reconstruct the complete K7 edge-coloring forced by the five supports.
    edge_colors: dict[frozenset[int], str] = {}
    for leaf_id in leaf_ids:
        color = "red" if colors[leaf_id] == "positive" else "blue"
        for u, v in itertools.combinations(support(clauses[leaf_id]), 2):
            edge = frozenset((u, v))
            previous = edge_colors.get(edge)
            if previous is not None and previous != color:
                raise AssertionError("leaf supports force conflicting edge colors")
            edge_colors[edge] = color
    vertices = sorted(set().union(*(support(clauses[leaf_id]) for leaf_id in leaf_ids)))
    if len(edge_colors) != len(vertices) * (len(vertices) - 1) // 2:
        raise AssertionError("sharpness witness does not color a complete graph")
    monochromatic_k5 = 0
    for subset in itertools.combinations(vertices, 5):
        colors_seen = {
            edge_colors[frozenset(edge)]
            for edge in itertools.combinations(subset, 2)
        }
        monochromatic_k5 += len(colors_seen) == 1
    if monochromatic_k5 != expected["monochromatic_k5_count"]:
        raise AssertionError("wrong monochromatic K5 count")

    return {
        "root_clause": tuple(sorted(clauses[root])),
        "leaf_occurrences": len(ancestry[root]),
        "bichromatic_edges": len(bi_edges),
        "full_support_incidences": len(full_incidences),
        "maximum_overlap": maximum_overlap,
        "four_incidence_cuts": four_cuts,
        "monochromatic_k5": monochromatic_k5,
    }


def main() -> None:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ramsey_r55_symbolic_extension/genealogical-four-incidence-cut-certificate.json"
    )
    raw = path.read_bytes()
    result = verify(json.loads(raw))
    digest = hashlib.sha256(raw).hexdigest()
    fields = "; ".join(f"{key}={value}" for key, value in result.items())
    print(f"verified: genealogical four-incidence cut; {fields}; certificate_sha256={digest}")


if __name__ == "__main__":
    main()
