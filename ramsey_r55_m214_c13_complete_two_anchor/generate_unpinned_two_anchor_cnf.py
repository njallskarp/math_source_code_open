#!/usr/bin/env python3
"""Generate the complete unpinned c=13 two-anchor relaxation.

The formula fixes only the standard E_left_8 anchor u=13 and names a central
red partner v=14.  It quantifies every partner E-marking and every labeling of
the common-red core.  It imposes all exact global degrees and E-incidences,
both anchors' red/blue local edge totals, and all Ramsey constraints induced
inside their four color neighborhoods.  Five-sets outside all four local
neighborhoods are deliberately outside this two-anchor relaxation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from collections.abc import Callable, Sequence
from pathlib import Path


N = 43
E = tuple(range(13))
U = 13
V = 14
U_RED = tuple(range(6)) + tuple(range(14, 29))
U_BLUE = tuple(range(6, 13)) + tuple(range(29, 43))
GRAPH_VARIABLES = N * (N - 1) // 2
V_OTHER_PAIRS = tuple(itertools.combinations((i for i in range(N) if i != V), 2))
RED_TRIANGLE_VARIABLES = {
    pair: GRAPH_VARIABLES + rank
    for rank, pair in enumerate(V_OTHER_PAIRS, 1)
}
BLUE_TRIANGLE_VARIABLES = {
    pair: GRAPH_VARIABLES + len(V_OTHER_PAIRS) + rank
    for rank, pair in enumerate(V_OTHER_PAIRS, 1)
}
BASE_VARIABLES = GRAPH_VARIABLES + 2 * len(V_OTHER_PAIRS)


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    if not 0 <= i < j < N:
        raise ValueError((i, j))
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


class Encoder:
    def __init__(self, emit: Callable[[Sequence[int]], None] | None) -> None:
        self.emit = emit
        self.variables = BASE_VARIABLES
        self.clauses = 0
        self.local_clauses = 0
        self.conjunction_clauses = 0
        self.unit_clauses = 0
        self.exact_sums = 0
        self.totalizer_variables = 0
        self.totalizer_clauses = 0
        self.merges = 0

    def clause(self, literals: Sequence[int], category: str = "local") -> None:
        if not literals or any(literal == 0 for literal in literals):
            raise ValueError(tuple(literals))
        self.clauses += 1
        if category == "local":
            self.local_clauses += 1
        elif category == "conjunction":
            self.conjunction_clauses += 1
        elif category == "unit":
            self.unit_clauses += 1
        elif category == "totalizer":
            self.totalizer_clauses += 1
        else:
            raise ValueError(category)
        if self.emit is not None:
            self.emit(literals)

    def new_variables(self, count: int) -> tuple[int, ...]:
        if count <= 0:
            raise ValueError(count)
        first = self.variables + 1
        self.variables += count
        self.totalizer_variables += count
        return tuple(range(first, self.variables + 1))

    def totalizer(self, inputs: Sequence[int], limit: int) -> tuple[int, ...]:
        if len(inputs) == 1:
            return (inputs[0],)
        middle = len(inputs) // 2
        left = self.totalizer(inputs[:middle], limit)
        right = self.totalizer(inputs[middle:], limit)
        output = self.new_variables(min(len(inputs), limit))
        self.merges += 1
        for i in range(len(left) + 1):
            for j in range(len(right) + 1):
                if not 1 <= i + j <= len(output):
                    continue
                clause: list[int] = []
                if i:
                    clause.append(-left[i - 1])
                if j:
                    clause.append(-right[j - 1])
                clause.append(output[i + j - 1])
                self.clause(clause, "totalizer")
        for i in range(len(left) + 1):
            for j in range(len(right) + 1):
                threshold = i + j + 1
                if threshold > len(output):
                    continue
                clause = []
                if i < len(left):
                    clause.append(left[i])
                if j < len(right):
                    clause.append(right[j])
                clause.append(-output[threshold - 1])
                self.clause(clause, "totalizer")
        return output

    def exact_sum(self, inputs: Sequence[int], target: int) -> None:
        if not inputs or not 0 < target < len(inputs):
            raise ValueError((len(inputs), target))
        root = self.totalizer(tuple(inputs), target + 1)
        self.clause((root[target - 1],), "totalizer")
        self.clause((-root[target],), "totalizer")
        self.exact_sums += 1


def emit_formula(encoder: Encoder) -> None:
    # Safe E_left_8 anchor normalization; in particular uv is red.
    for vertex in U_RED:
        encoder.clause((edge_id(U, vertex),), "unit")
    for vertex in U_BLUE:
        encoder.clause((-edge_id(U, vertex),), "unit")

    # The complete cell's red degrees and E-incidences.
    for vertex in range(N):
        incident = tuple(edge_id(vertex, other) for other in range(N) if other != vertex)
        encoder.exact_sum(incident, 20 if vertex in E else 21)
    for vertex in range(N):
        e_incident = tuple(edge_id(vertex, other) for other in E if other != vertex)
        encoder.exact_sum(e_incident, 8 if vertex == 5 else 6)

    # All E-markings of v occur in this one exact sum.  Since N_R(u) is fixed,
    # these are precisely the possible common-red neighbors of u and v.
    common_inputs = tuple(edge_id(V, vertex) for vertex in U_RED if vertex != V)
    if len(common_inputs) != 20:
        raise AssertionError(len(common_inputs))
    encoder.exact_sum(common_inputs, 13)

    # Exact red/blue triangle indicators at the variable partner v.
    for pair in V_OTHER_PAIRS:
        i, j = pair
        edges = (edge_id(V, i), edge_id(V, j), edge_id(i, j))
        red_triangle = RED_TRIANGLE_VARIABLES[pair]
        blue_triangle = BLUE_TRIANGLE_VARIABLES[pair]
        for edge in edges:
            encoder.clause((-red_triangle, edge), "conjunction")
            encoder.clause((-blue_triangle, -edge), "conjunction")
        encoder.clause((red_triangle,) + tuple(-edge for edge in edges), "conjunction")
        encoder.clause((blue_triangle,) + edges, "conjunction")
    encoder.exact_sum(tuple(RED_TRIANGLE_VARIABLES.values()), 100)
    encoder.exact_sum(tuple(BLUE_TRIANGLE_VARIABLES.values()), 100)

    # The fixed anchor has the same doubly exact local totals, expressed
    # directly in its two fixed neighborhoods.
    encoder.exact_sum(
        tuple(edge_id(i, j) for i, j in itertools.combinations(U_RED, 2)),
        100,
    )
    encoder.exact_sum(
        tuple(edge_id(i, j) for i, j in itertools.combinations(U_BLUE, 2)),
        110,
    )

    # Complete Ramsey constraints induced inside u's fixed red/blue
    # neighborhoods.
    for vertices in itertools.combinations(U_RED, 4):
        encoder.clause(tuple(-edge_id(i, j) for i, j in itertools.combinations(vertices, 2)))
    for vertices in itertools.combinations(U_RED, 5):
        encoder.clause(tuple(edge_id(i, j) for i, j in itertools.combinations(vertices, 2)))
    for vertices in itertools.combinations(U_BLUE, 5):
        encoder.clause(tuple(-edge_id(i, j) for i, j in itertools.combinations(vertices, 2)))
    for vertices in itertools.combinations(U_BLUE, 4):
        encoder.clause(tuple(edge_id(i, j) for i, j in itertools.combinations(vertices, 2)))

    # The corresponding four conditional families for v.  These range over
    # all other vertices, so no partner neighborhood or E-marking is pinned.
    others = tuple(vertex for vertex in range(N) if vertex != V)
    for vertices in itertools.combinations(others, 4):
        spokes = tuple(edge_id(V, vertex) for vertex in vertices)
        interior = tuple(edge_id(i, j) for i, j in itertools.combinations(vertices, 2))
        encoder.clause(tuple(-edge for edge in spokes + interior))
        encoder.clause(spokes + interior)
    for vertices in itertools.combinations(others, 5):
        spokes = tuple(edge_id(V, vertex) for vertex in vertices)
        interior = tuple(edge_id(i, j) for i, j in itertools.combinations(vertices, 2))
        encoder.clause(tuple(-edge for edge in spokes) + interior)
        encoder.clause(spokes + tuple(-edge for edge in interior))


def count_formula() -> Encoder:
    encoder = Encoder(None)
    emit_formula(encoder)
    return encoder


def build(destination: Path) -> dict[str, int | str]:
    count = count_formula()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    digest = hashlib.sha256()
    bytes_written = 0
    lines_written = 0
    try:
        with temporary.open("wb") as raw:
            def write(data: bytes) -> None:
                nonlocal bytes_written, lines_written
                raw.write(data)
                digest.update(data)
                bytes_written += len(data)
                lines_written += data.count(b"\n")

            write(f"p cnf {count.variables} {count.clauses}\n".encode("ascii"))

            def emit(literals: Sequence[int]) -> None:
                write((" ".join(map(str, literals)) + " 0\n").encode("ascii"))

            output = Encoder(emit)
            emit_formula(output)
            if {**vars(output), "emit": None} != {**vars(count), "emit": None}:
                raise AssertionError("count/write divergence")
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    return {
        "base_variables": BASE_VARIABLES,
        "blue_triangle_variables": len(BLUE_TRIANGLE_VARIABLES),
        "bytes": bytes_written,
        "clauses": count.clauses,
        "conjunction_clauses": count.conjunction_clauses,
        "exact_sums": count.exact_sums,
        "graph_variables": GRAPH_VARIABLES,
        "lines": lines_written,
        "local_clauses": count.local_clauses,
        "merges": count.merges,
        "red_triangle_variables": len(RED_TRIANGLE_VARIABLES),
        "sha256": digest.hexdigest(),
        "totalizer_clauses": count.totalizer_clauses,
        "totalizer_variables": count.totalizer_variables,
        "unit_clauses": count.unit_clauses,
        "variables": count.variables,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output.resolve()), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
