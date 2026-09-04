#!/usr/bin/env python3
"""Exact audit of all one-vertex extensions of the 72 order-11 maximizers."""

from __future__ import annotations

import hashlib
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_CORE_SHA256 = "5f22202d2ea18eddf1b02e7ebe6cf1a855f80d8880d101335d546e3f328cd75b"


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    if not record:
        raise ValueError("empty graph6 record")
    order = ord(record[0]) - 63
    expected = 1 + (order * (order - 1) // 2 + 5) // 6
    if not 0 <= order <= 62 or len(record) != expected:
        raise ValueError(f"invalid short graph6 record: {record!r}")
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value <= 63:
            raise ValueError(f"invalid graph6 character in {record!r}")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, edges


def connected(order: int, edges: list[tuple[int, int]]) -> bool:
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            frontier.append(neighbor)
    return len(seen) == order


def shifted_signless_laplacian(order: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    matrix = [[0] * order for _ in range(order)]
    for left, right in edges:
        matrix[left][right] = matrix[right][left] = 1
        matrix[left][left] += 1
        matrix[right][right] += 1
    for index in range(order):
        matrix[index][index] -= 2
    return matrix


def symmetric_swap(matrix: list[list[Fraction]], left: int, right: int) -> None:
    if left == right:
        return
    matrix[left], matrix[right] = matrix[right], matrix[left]
    for row in matrix:
        row[left], row[right] = row[right], row[left]


def exact_inertia(integer_matrix: list[list[int]]) -> tuple[int, int, int]:
    """Rational symmetric congruence using 1-by-1 and zero-diagonal 2-by-2 pivots."""
    matrix = [[Fraction(value) for value in row] for row in integer_matrix]
    order = len(matrix)
    positive = zero = negative = 0
    pivot = 0
    while pivot < order:
        diagonal = next((i for i in range(pivot, order) if matrix[i][i]), None)
        if diagonal is not None:
            symmetric_swap(matrix, pivot, diagonal)
            value = matrix[pivot][pivot]
            if value > 0:
                positive += 1
            else:
                negative += 1
            for row in range(pivot + 1, order):
                for column in range(row, order):
                    matrix[row][column] -= matrix[row][pivot] * matrix[pivot][column] / value
                    matrix[column][row] = matrix[row][column]
            pivot += 1
            continue
        off_diagonal = next(
            (
                (row, column)
                for row in range(pivot, order)
                for column in range(row + 1, order)
                if matrix[row][column]
            ),
            None,
        )
        if off_diagonal is None:
            zero += order - pivot
            break
        row, column = off_diagonal
        symmetric_swap(matrix, pivot, row)
        if column == pivot:
            column = row
        symmetric_swap(matrix, pivot + 1, column)
        value = matrix[pivot][pivot + 1]
        assert matrix[pivot][pivot] == matrix[pivot + 1][pivot + 1] == 0 and value
        positive += 1
        negative += 1
        for row in range(pivot + 2, order):
            for column in range(row, order):
                matrix[row][column] -= (
                    matrix[row][pivot] * matrix[pivot + 1][column]
                    + matrix[row][pivot + 1] * matrix[pivot][column]
                ) / value
                matrix[column][row] = matrix[row][column]
        pivot += 2
    assert positive + zero + negative == order
    return positive, zero, negative


def line_graph_signature(order: int, edges: list[tuple[int, int]]) -> tuple[int, tuple[int, int, int]]:
    # The nonzero spectra of B B^T=Q(G) and B^T B=A(L(G))+2I agree.
    shifted_inertia = exact_inertia(shifted_signless_laplacian(order, edges))
    positive, at_two, _ = shifted_inertia
    signature = 2 * positive + at_two - len(edges)
    return signature, shifted_inertia


def main() -> None:
    path = ROOT / "maximizers_n11.g6"
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED_CORE_SHA256, digest
    records = raw.decode("ascii").splitlines()
    assert len(records) == len(set(records)) == 72
    histogram: Counter[int] = Counter()
    core_edge_histogram: Counter[int] = Counter()
    extensions = 0
    for core_number, record in enumerate(records):
        order, core_edges = decode_graph6(record)
        assert order == 11 and connected(order, core_edges)
        core_signature, _ = line_graph_signature(order, core_edges)
        assert core_signature == 1, (record, core_signature)
        core_edge_histogram[len(core_edges)] += 1
        for neighborhood_mask in range(1, 1 << order):
            edges = core_edges + [
                (vertex, order)
                for vertex in range(order)
                if neighborhood_mask >> vertex & 1
            ]
            signature, _ = line_graph_signature(order + 1, edges)
            if signature >= 2:
                raise AssertionError(
                    f"counterexample core={core_number} record={record} mask={neighborhood_mask} signature={signature}"
                )
            histogram[signature] += 1
            extensions += 1
    assert extensions == 72 * ((1 << 11) - 1) == 147_384
    assert max(histogram) == 1
    print(f"core_records=72 core_sha256={digest}")
    print("core_edge_histogram=" + ",".join(f"{key}:{core_edge_histogram[key]}" for key in sorted(core_edge_histogram)))
    print("extension_signature_histogram=" + ",".join(f"{key}:{histogram[key]}" for key in sorted(histogram)))
    print(f"extensions={extensions} maximum_extension_signature={max(histogram)} status=VERIFIED")


if __name__ == "__main__":
    main()
