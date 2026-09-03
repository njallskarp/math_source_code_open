#!/usr/bin/env python3
"""Exact residue classification of minimum-degree-two c=3 root graphs.

The checker uses only Python's standard library.  All inertia calculations
use fractions.Fraction symmetric congruence; no floating point is used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import hashlib
import json


Matrix = list[list[int]]
Kernel = tuple[int, tuple[tuple[int, int, int], ...]]


def multiplicity_compositions(total: int, parts: int, prefix: tuple[int, ...] = ()):
    if parts == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from multiplicity_compositions(total - value, parts - 1, prefix + (value,))


def kernel_slots(order: int) -> list[tuple[int, int]]:
    return [(v, v) for v in range(order)] + [
        (u, v) for u in range(order) for v in range(u + 1, order)
    ]


def kernel_degrees(
    order: int, slots: list[tuple[int, int]], multiplicities: tuple[int, ...]
) -> list[int]:
    degree = [0] * order
    for (u, v), multiplicity in zip(slots, multiplicities):
        if u == v:
            degree[u] += 2 * multiplicity
        else:
            degree[u] += multiplicity
            degree[v] += multiplicity
    return degree


def kernel_connected(
    order: int, slots: list[tuple[int, int]], multiplicities: tuple[int, ...]
) -> bool:
    if order == 1:
        return True
    adjacency = [[] for _ in range(order)]
    for (u, v), multiplicity in zip(slots, multiplicities):
        if multiplicity and u != v:
            adjacency[u].append(v)
            adjacency[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == order


def canonical_kernel_key(
    order: int, slots: list[tuple[int, int]], multiplicities: tuple[int, ...]
) -> tuple[int, ...]:
    data = dict(zip(slots, multiplicities))
    best = None
    for permutation in permutations(range(order)):
        encoding = tuple(
            data[tuple(sorted((permutation[i], permutation[j])))]
            for i in range(order)
            for j in range(i, order)
        )
        if best is None or encoding < best:
            best = encoding
    assert best is not None
    return best


def enumerate_c3_kernels() -> list[Kernel]:
    """Enumerate looped multigraph kernels up to exact vertex permutation."""
    representatives: dict[tuple[int, tuple[int, ...]], Kernel] = {}
    c = 3
    for order in range(1, 2 * c - 1):
        edge_count = order + c - 1
        slots = kernel_slots(order)
        for multiplicities in multiplicity_compositions(edge_count, len(slots)):
            if min(kernel_degrees(order, slots, multiplicities)) < 3:
                continue
            if not kernel_connected(order, slots, multiplicities):
                continue
            key = (order, canonical_kernel_key(order, slots, multiplicities))
            data = tuple(
                (u, v, multiplicity)
                for (u, v), multiplicity in zip(slots, multiplicities)
                if multiplicity
            )
            representatives.setdefault(key, (order, data))
    return [representatives[key] for key in sorted(representatives)]


def kernel_edge_instances(kernel: Kernel) -> list[tuple[int, int]]:
    return [
        (u, v)
        for u, v, multiplicity in kernel[1]
        for _ in range(multiplicity)
    ]


def canonical_residue_lengths(
    edges: list[tuple[int, int]], residues: tuple[int, ...]
) -> tuple[int, ...]:
    """Choose simple representatives of all path-length classes modulo four.

    A loop path must have length at least three.  Among parallel nonloop
    paths, at most one may have length one; later residue-one paths use length
    five.  Every original simple subdivision reduces to one of these choices
    by deleting groups of four internal degree-two vertices.
    """
    lengths: list[int] = []
    direct_used: set[tuple[int, int]] = set()
    for edge, residue in zip(edges, residues):
        u, v = edge
        residue %= 4
        if u == v:
            lengths.append({0: 4, 1: 5, 2: 6, 3: 3}[residue])
        elif residue == 1:
            pair = tuple(sorted(edge))
            if pair in direct_used:
                lengths.append(5)
            else:
                lengths.append(1)
                direct_used.add(pair)
        else:
            lengths.append({0: 4, 2: 2, 3: 3}[residue])
    return tuple(lengths)


def expand_kernel(kernel: Kernel, lengths: tuple[int, ...]) -> Matrix:
    """Return a simple adjacency matrix obtained by replacing kernel edges."""
    order = kernel[0]
    edges = kernel_edge_instances(kernel)
    simple_edges: list[tuple[int, int]] = []
    next_vertex = order
    for (u, v), length in zip(edges, lengths):
        path = [u] + list(range(next_vertex, next_vertex + length - 1)) + [v]
        next_vertex += length - 1
        simple_edges.extend(zip(path, path[1:]))
    normalized = [tuple(sorted(edge)) for edge in simple_edges]
    assert all(u != v for u, v in normalized)
    assert len(normalized) == len(set(normalized))
    adjacency = [[0] * next_vertex for _ in range(next_vertex)]
    for u, v in normalized:
        adjacency[u][v] = adjacency[v][u] = 1
    assert min(map(sum, adjacency)) >= 2
    assert sum(map(sum, adjacency)) // 2 - next_vertex + 1 == 3
    return adjacency


def shifted_signless(adjacency: Matrix) -> Matrix:
    matrix = [row[:] for row in adjacency]
    for i, row in enumerate(adjacency):
        matrix[i][i] = sum(row) - 2
    return matrix


def inertia(matrix: Matrix) -> tuple[int, int, int]:
    """Exact symmetric congruence with one- and two-dimensional pivots."""
    active = [[Fraction(value) for value in row] for row in matrix]
    positive = zero = negative = 0
    while active:
        size = len(active)
        pivot = next((i for i in range(size) if active[i][i]), None)
        if pivot is not None:
            order = [pivot] + [i for i in range(size) if i != pivot]
            active = [[active[i][j] for j in order] for i in order]
            value = active[0][0]
            if value > 0:
                positive += 1
            else:
                negative += 1
            active = [
                [
                    active[i][j] - active[i][0] * active[0][j] / value
                    for j in range(1, size)
                ]
                for i in range(1, size)
            ]
            continue
        pair = next(
            (
                (i, j)
                for i in range(size)
                for j in range(i + 1, size)
                if active[i][j]
            ),
            None,
        )
        if pair is None:
            zero += size
            break
        first, second = pair
        order = [first, second] + [
            i for i in range(size) if i != first and i != second
        ]
        active = [[active[i][j] for j in order] for i in order]
        value = active[0][1]
        positive += 1
        negative += 1
        active = [
            [
                active[i][j]
                - (
                    active[i][0] * active[1][j]
                    + active[i][1] * active[0][j]
                )
                / value
                for j in range(2, size)
            ]
            for i in range(2, size)
        ]
    return positive, zero, negative


def multiply(left: Matrix, right: Matrix) -> Matrix:
    size = len(left)
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(size))
            for j in range(size)
        ]
        for i in range(size)
    ]


def characteristic_polynomial(matrix: Matrix) -> list[int]:
    """Faddeev-LeVerrier coefficients of det(xI-M), exactly."""
    size = len(matrix)
    work = [[int(i == j) for j in range(size)] for i in range(size)]
    coefficients = [1]
    for step in range(1, size + 1):
        product_matrix = multiply(matrix, work)
        numerator = -sum(product_matrix[i][i] for i in range(size))
        coefficient, remainder = divmod(numerator, step)
        assert remainder == 0
        coefficients.append(coefficient)
        for i in range(size):
            product_matrix[i][i] += coefficient
        work = product_matrix
    return coefficients


def sign_variations(values: list[int]) -> int:
    signs = [1 if value > 0 else -1 for value in values if value]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def inertia_from_charpoly(coefficients: list[int]) -> tuple[int, int, int]:
    zero = 0
    while zero < len(coefficients) - 1 and coefficients[-1 - zero] == 0:
        zero += 1
    reduced = coefficients[:-zero] if zero else coefficients
    degree = len(reduced) - 1
    positive = sign_variations(reduced)
    reflected = [
        coefficient * (-1 if (degree - index) % 2 else 1)
        for index, coefficient in enumerate(reduced)
    ]
    negative = sign_variations(reflected)
    assert positive + zero + negative == len(coefficients) - 1
    return positive, zero, negative


def kernel_description(kernel: Kernel) -> list[list[int]]:
    return [[u, v, multiplicity] for u, v, multiplicity in kernel[1]]


def main() -> None:
    kernels = enumerate_c3_kernels()
    assert len(kernels) == 15
    histogram: Counter[tuple[int, int]] = Counter()
    equality_records = []
    assignments = 0
    for kernel_index, kernel in enumerate(kernels):
        edges = kernel_edge_instances(kernel)
        for residues in product(range(1, 5), repeat=len(edges)):
            lengths = canonical_residue_lengths(edges, residues)
            adjacency = expand_kernel(kernel, lengths)
            exact_inertia = inertia(shifted_signless(adjacency))
            line_signature = exact_inertia[0] - exact_inertia[2] - 2
            nullity = exact_inertia[1]
            histogram[(line_signature, nullity)] += 1
            assignments += 1
            if line_signature == 2:
                independent = inertia_from_charpoly(
                    characteristic_polynomial(shifted_signless(adjacency))
                )
                assert independent == exact_inertia
                equality_records.append(
                    {
                        "kernel": kernel_index,
                        "lengths": list(lengths),
                        "nullity": nullity,
                        "residues": list(residues),
                    }
                )

    assert assignments == 26688
    assert max(signature for signature, _ in histogram) == 2
    assert len(equality_records) == 8
    assert all(record["kernel"] == 11 for record in equality_records)
    assert all(record["nullity"] == 0 for record in equality_records)

    equality_patterns = {
        (
            tuple(record["residues"][:2]),
            frozenset(record["residues"][2:4]),
            tuple(value % 2 for value in record["residues"][4:]),
        )
        for record in equality_records
    }
    assert equality_patterns == {((1, 1), frozenset({1, 3}), (1, 1))}

    result = {
        "algorithm": "Fraction congruence; charpoly-Descartes replay on equality cases",
        "boundary_simple_Q2_cases": sum(
            count
            for (signature, nullity), count in histogram.items()
            if signature == 2 and nullity == 1
        ),
        "equality_assignments": len(equality_records),
        "equality_kernel": kernel_description(kernels[11]),
        "equality_pattern": {
            "bridge_path_residues": "odd",
            "central_parallel_path_residues": [1, 3],
            "terminal_loop_path_residues": [1, 1],
        },
        "histogram_signature_nullity": {
            f"s={signature},z={nullity}": count
            for (signature, nullity), count in sorted(histogram.items())
        },
        "kernel_count": len(kernels),
        "labeled_residue_assignments": assignments,
        "maximum_signature": max(signature for signature, _ in histogram),
        "status": "VERIFIED",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
