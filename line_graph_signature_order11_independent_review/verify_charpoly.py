#!/usr/bin/env python3
"""Independent exact checker for streamed short-graph6 root graphs.

Unlike the reviewed implementation, this checker does not use congruence
elimination.  It computes the characteristic polynomial of Q(G)-2I by the
Faddeev-LeVerrier recurrence.  Because that matrix is real symmetric, all
roots are real, so Descartes sign variations of p(x) and p(-x) give its
positive and negative inertia indices exactly.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, deque


def decode_short_graph6(record: str) -> list[list[int]]:
    if record.startswith(">>graph6<<"):
        record = record[10:]
    if not record:
        raise ValueError("empty graph6 record")
    n = ord(record[0]) - 63
    needed = 1 + (n * (n - 1) // 2 + 5) // 6
    if not 0 <= n <= 62 or len(record) != needed:
        raise ValueError("not a short graph6 record")
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [[0] * n for _ in range(n)]
    cursor = 0
    for j in range(1, n):
        for i in range(j):
            adjacency[i][j] = adjacency[j][i] = bits[cursor]
            cursor += 1
    return adjacency


def assert_connected(adjacency: list[list[int]]) -> None:
    if not adjacency:
        raise AssertionError("empty graph is outside the review domain")
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor, edge in enumerate(adjacency[vertex]):
            if edge and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    if len(seen) != len(adjacency):
        raise AssertionError("generator emitted a disconnected graph")


def shifted_signless_laplacian(adjacency: list[list[int]]) -> list[list[int]]:
    matrix = [row.copy() for row in adjacency]
    for i, row in enumerate(adjacency):
        matrix[i][i] = sum(row) - 2
    return matrix


def multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    n = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def characteristic_polynomial(matrix: list[list[int]]) -> list[int]:
    """Return coefficients [1,c1,...,cn] of det(xI-A), exactly."""
    n = len(matrix)
    work = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n + 1):
        product = multiply(matrix, work)
        negative_trace = -sum(product[i][i] for i in range(n))
        quotient, remainder = divmod(negative_trace, k)
        if remainder:
            raise AssertionError("Faddeev-LeVerrier division was not exact")
        coefficients.append(quotient)
        for i in range(n):
            product[i][i] += quotient
        work = product
    return coefficients


def sign_variations(values: list[int]) -> int:
    signs = [1 if value > 0 else -1 for value in values if value]
    return sum(first != second for first, second in zip(signs, signs[1:]))


def symmetric_inertia_from_charpoly(coefficients: list[int]) -> tuple[int, int, int]:
    zero = 0
    while coefficients[-1 - zero] == 0:
        zero += 1
        if zero == len(coefficients) - 1:
            break
    reduced = coefficients[:-zero] if zero else coefficients
    degree = len(reduced) - 1
    positive = sign_variations(reduced)
    reflected = [
        coefficient * (-1 if (degree - index) % 2 else 1)
        for index, coefficient in enumerate(reduced)
    ]
    negative = sign_variations(reflected)
    if positive + zero + negative != len(coefficients) - 1:
        raise AssertionError("real-rooted inertia count has wrong dimension")
    return positive, zero, negative


def main() -> None:
    graphs = 0
    violations = 0
    sharp_violations = 0
    maximum_signature: int | None = None
    edge_counts: Counter[tuple[int, int]] = Counter()
    signature_counts: Counter[int] = Counter()
    for raw_record in sys.stdin:
        record = raw_record.strip()
        if not record:
            continue
        adjacency = decode_short_graph6(record)
        assert_connected(adjacency)
        n = len(adjacency)
        m = sum(map(sum, adjacency)) // 2
        if not n <= m <= 2 * n - 2:
            raise AssertionError("graph is outside the sparse finite-reduction range")
        inertia = symmetric_inertia_from_charpoly(
            characteristic_polynomial(shifted_signless_laplacian(adjacency))
        )
        signature = inertia[0] - inertia[2] - (m - n)
        cyclomatic = m - n + 1
        graphs += 1
        edge_counts[(n, m)] += 1
        signature_counts[signature] += 1
        maximum_signature = (
            signature if maximum_signature is None else max(maximum_signature, signature)
        )
        violations += signature > 1
        sharp_violations += 2 * signature > cyclomatic + 1
    result = {
        "algorithm": "Faddeev-LeVerrier+Descartes on Q(G)-2I",
        "counterexamples": violations,
        "edge_counts": {f"n={n},m={m}": count for (n, m), count in sorted(edge_counts.items())},
        "graphs": graphs,
        "maximum_signature": maximum_signature,
        "sharp_bound_violations": sharp_violations,
        "signature_counts": {str(key): value for key, value in sorted(signature_counts.items())},
        "status": "VERIFIED" if graphs and not violations and not sharp_violations else "FAILED",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    if result["status"] != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
