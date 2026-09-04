#!/usr/bin/env python3
"""Independent exact review of the cyclomatic-three line-graph core claim.

This program does not import the target contribution's checkers.  It uses
NetworkX VF2 on MultiGraphs for the kernel quotient and constructs the
adjacency matrix of the line graph directly.  Inertia is then computed by
exact rational symmetric congruence.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import hashlib
import json

import networkx as nx


Matrix = list[list[int]]


def weak_compositions(total: int, parts: int):
    """Yield every ordered weak composition of total into parts entries."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first,) + tail


def slots(order: int) -> list[tuple[int, int]]:
    return [(v, v) for v in range(order)] + [
        (u, v) for u in range(order) for v in range(u + 1, order)
    ]


def graph_from_multiplicities(
    order: int, edge_slots: list[tuple[int, int]], multiplicities: tuple[int, ...]
) -> nx.MultiGraph:
    graph = nx.MultiGraph()
    graph.add_nodes_from(range(order))
    for (u, v), count in zip(edge_slots, multiplicities):
        for _ in range(count):
            graph.add_edge(u, v)
    return graph


def kernel_fingerprint(graph: nx.MultiGraph) -> tuple[int, ...]:
    """Canonical multiplicity-table fingerprint under every vertex permutation."""
    order = graph.number_of_nodes()
    encodings = []
    for permutation in permutations(range(order)):
        encodings.append(
            tuple(
                graph.number_of_edges(permutation[i], permutation[j])
                for i in range(order)
                for j in range(i, order)
            )
        )
    return (order,) + min(encodings)


def enumerate_kernels() -> list[nx.MultiGraph]:
    """Enumerate c=3 kernels, quotienting with NetworkX MultiGraph VF2."""
    representatives: list[nx.MultiGraph] = []
    for order in range(1, 5):
        edge_count = order + 2
        edge_slots = slots(order)
        for multiplicities in weak_compositions(edge_count, len(edge_slots)):
            graph = graph_from_multiplicities(order, edge_slots, multiplicities)
            if min(dict(graph.degree()).values()) < 3:
                continue
            if not nx.is_connected(graph):
                continue
            if any(nx.is_isomorphic(graph, old) for old in representatives):
                continue
            representatives.append(graph)
    representatives.sort(key=kernel_fingerprint)
    return representatives


def kernel_edges(graph: nx.MultiGraph) -> list[tuple[int, int]]:
    """Return distinguishable kernel-edge instances in a fixed slot order."""
    result = []
    for u, v in slots(graph.number_of_nodes()):
        result.extend([(u, v)] * graph.number_of_edges(u, v))
    return result


def representative_lengths(
    edges: list[tuple[int, int]], residues: tuple[int, ...]
) -> tuple[int, ...]:
    """Choose the smallest simple path representatives in each mod-4 class."""
    lengths = []
    direct_pairs: set[tuple[int, int]] = set()
    for (u, v), residue in zip(edges, residues):
        if u == v:
            lengths.append({0: 4, 1: 5, 2: 6, 3: 3}[residue])
        elif residue != 1:
            lengths.append({0: 4, 2: 2, 3: 3}[residue])
        else:
            pair = (u, v)
            if pair in direct_pairs:
                lengths.append(5)
            else:
                lengths.append(1)
                direct_pairs.add(pair)
    return tuple(lengths)


def expand(
    order: int, edges: list[tuple[int, int]], lengths: tuple[int, ...]
) -> list[tuple[int, int]]:
    """Expand kernel edges to internally disjoint paths in a simple root graph."""
    root_edges: list[tuple[int, int]] = []
    next_vertex = order
    for (u, v), length in zip(edges, lengths):
        internal = list(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        path = [u] + internal + [v]
        root_edges.extend(tuple(sorted(edge)) for edge in zip(path, path[1:]))

    assert all(u != v for u, v in root_edges)
    assert len(root_edges) == len(set(root_edges))
    degrees = Counter(vertex for edge in root_edges for vertex in edge)
    assert len(degrees) == next_vertex
    assert min(degrees.values()) >= 2
    assert len(root_edges) - next_vertex + 1 == 3
    return root_edges


def line_graph_adjacency(root_edges: list[tuple[int, int]]) -> Matrix:
    """Construct A(L(H)) directly from the edge-intersection definition."""
    size = len(root_edges)
    matrix = [[0] * size for _ in range(size)]
    for i, (a, b) in enumerate(root_edges):
        for j in range(i + 1, size):
            c, d = root_edges[j]
            if a == c or a == d or b == c or b == d:
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def inertia(matrix: Matrix) -> tuple[int, int, int]:
    """Exact inertia from symmetric Schur pivots over the rationals."""
    active = [[Fraction(entry) for entry in row] for row in matrix]
    positive = zero = negative = 0
    while active:
        size = len(active)
        diagonal = next((i for i in range(size) if active[i][i] != 0), None)
        if diagonal is not None:
            order = [diagonal] + [i for i in range(size) if i != diagonal]
            active = [[active[i][j] for j in order] for i in order]
            pivot = active[0][0]
            positive += pivot > 0
            negative += pivot < 0
            active = [
                [
                    active[i][j] - active[i][0] * active[0][j] / pivot
                    for j in range(1, size)
                ]
                for i in range(1, size)
            ]
            continue

        off_diagonal = next(
            (
                (i, j)
                for i in range(size)
                for j in range(i + 1, size)
                if active[i][j] != 0
            ),
            None,
        )
        if off_diagonal is None:
            zero += size
            break

        first, second = off_diagonal
        order = [first, second] + [
            i for i in range(size) if i not in (first, second)
        ]
        active = [[active[i][j] for j in order] for i in order]
        pivot = active[0][1]
        positive += 1
        negative += 1
        active = [
            [
                active[i][j]
                - (active[i][0] * active[1][j] + active[i][1] * active[0][j])
                / pivot
                for j in range(2, size)
            ]
            for i in range(2, size)
        ]
    return positive, zero, negative


EXPECTED_HISTOGRAM = {
    "s=-4,z=0": 44,
    "s=-3,z=0": 1155,
    "s=-3,z=1": 368,
    "s=-2,z=0": 4392,
    "s=-2,z=1": 3368,
    "s=-2,z=2": 1278,
    "s=-1,z=0": 5313,
    "s=-1,z=1": 4385,
    "s=-1,z=2": 1242,
    "s=-1,z=3": 343,
    "s=0,z=0": 1726,
    "s=0,z=1": 1764,
    "s=0,z=2": 596,
    "s=0,z=3": 102,
    "s=0,z=4": 44,
    "s=1,z=0": 268,
    "s=1,z=1": 160,
    "s=1,z=2": 132,
    "s=2,z=0": 8,
}


def equality_pattern(
    kernel: nx.MultiGraph,
    edges: list[tuple[int, int]],
    residues: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    loops = []
    parallel = []
    connectors = []
    for (u, v), residue in zip(edges, residues):
        if u == v:
            loops.append(residue)
        elif kernel.number_of_edges(u, v) == 2:
            parallel.append(residue)
        else:
            connectors.append(residue % 2)
    return tuple(sorted(loops)), tuple(sorted(parallel)), tuple(sorted(connectors))


def main() -> None:
    kernels = enumerate_kernels()
    assert len(kernels) == 15
    assert Counter(graph.number_of_nodes() for graph in kernels) == {
        1: 1,
        2: 4,
        3: 5,
        4: 5,
    }
    assert all(
        not nx.is_isomorphic(left, right)
        for i, left in enumerate(kernels)
        for right in kernels[i + 1 :]
    )

    histogram: Counter[tuple[int, int]] = Counter()
    per_kernel: dict[str, Counter[tuple[int, int]]] = {}
    equality_records = []
    state_hasher = hashlib.sha256()
    assignment_count = 0

    for kernel in kernels:
        fingerprint = kernel_fingerprint(kernel)
        fingerprint_text = ",".join(map(str, fingerprint))
        edges = kernel_edges(kernel)
        kernel_histogram: Counter[tuple[int, int]] = Counter()
        for residues in product(range(4), repeat=len(edges)):
            lengths = representative_lengths(edges, residues)
            root_edges = expand(kernel.number_of_nodes(), edges, lengths)
            exact_inertia = inertia(line_graph_adjacency(root_edges))
            signature = exact_inertia[0] - exact_inertia[2]
            nullity = exact_inertia[1]
            histogram[(signature, nullity)] += 1
            kernel_histogram[(signature, nullity)] += 1
            assignment_count += 1

            state = [fingerprint, residues, exact_inertia]
            state_hasher.update(
                (json.dumps(state, separators=(",", ":")) + "\n").encode()
            )
            if signature == 2:
                equality_records.append(
                    {
                        "kernel": kernel,
                        "kernel_fingerprint": fingerprint,
                        "edges": edges,
                        "residues": residues,
                        "lengths": lengths,
                        "inertia": exact_inertia,
                    }
                )
        per_kernel[fingerprint_text] = kernel_histogram

    encoded_histogram = {
        f"s={signature},z={nullity}": count
        for (signature, nullity), count in sorted(histogram.items())
    }
    assert assignment_count == 26688
    assert encoded_histogram == EXPECTED_HISTOGRAM
    assert len(equality_records) == 8
    assert {
        equality_pattern(record["kernel"], record["edges"], record["residues"])
        for record in equality_records
    } == {((1, 1), (1, 3), (1, 1))}
    assert {record["inertia"][1] for record in equality_records} == {0}
    assert len({record["kernel_fingerprint"] for record in equality_records}) == 1

    # Directly test the four-subdivision increment on every equality residue
    # assignment and on every one of its six kernel paths.
    subdivision_checks = 0
    for record in equality_records:
        base_inertia = record["inertia"]
        for edge_index in range(len(record["edges"])):
            longer = list(record["lengths"])
            longer[edge_index] += 4
            root_edges = expand(
                record["kernel"].number_of_nodes(),
                record["edges"],
                tuple(longer),
            )
            longer_inertia = inertia(line_graph_adjacency(root_edges))
            assert longer_inertia == (
                base_inertia[0] + 2,
                base_inertia[1],
                base_inertia[2] + 2,
            )
            subdivision_checks += 1

    encoded_per_kernel = {
        fingerprint: {
            f"s={signature},z={nullity}": count
            for (signature, nullity), count in sorted(kernel_histogram.items())
        }
        for fingerprint, kernel_histogram in sorted(per_kernel.items())
    }
    per_kernel_canonical = json.dumps(
        encoded_per_kernel, sort_keys=True, separators=(",", ":")
    )
    result = {
        "algorithm": (
            "NetworkX MultiGraph VF2 quotient; direct line-graph adjacency; "
            "Fraction symmetric congruence"
        ),
        "boundary_Q2_equality_cases": sum(
            count
            for (signature, nullity), count in histogram.items()
            if signature == 2 and nullity > 0
        ),
        "equality_assignments": len(equality_records),
        "equality_kernel_fingerprint": list(equality_records[0]["kernel_fingerprint"]),
        "equality_pattern": {
            "connector_parities": [1, 1],
            "parallel_path_residues": [1, 3],
            "terminal_loop_residues": [1, 1],
        },
        "histogram_signature_nullity": encoded_histogram,
        "kernel_count": len(kernels),
        "kernel_count_by_order": {
            str(order): count
            for order, count in sorted(
                Counter(graph.number_of_nodes() for graph in kernels).items()
            )
        },
        "labeled_residue_assignments": assignment_count,
        "maximum_signature": max(signature for signature, _ in histogram),
        "per_kernel_histogram_sha256": hashlib.sha256(
            per_kernel_canonical.encode()
        ).hexdigest(),
        "state_stream_sha256": state_hasher.hexdigest(),
        "subdivision_increment_checks": subdivision_checks,
        "status": "VERIFIED",
        "versions": {"networkx": nx.__version__},
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
