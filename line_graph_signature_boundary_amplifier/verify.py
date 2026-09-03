#!/usr/bin/env python3
"""Exact checks for the line-graph boundary-eigenvalue criterion.

No floating-point arithmetic and no third-party packages are used.
"""

from fractions import Fraction
import hashlib
import json


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matsub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def identity(n, scale=1):
    return [[scale if i == j else 0 for j in range(n)] for i in range(n)]


def determinant(a):
    """Bareiss fraction-free determinant over the integers."""
    n = len(a)
    if n == 0:
        return 1
    m = [list(map(int, row)) for row in a]
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if m[r][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        value = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * value - m[i][k] * m[k][j]) // previous
        previous = value
        for i in range(k + 1, n):
            m[i][k] = 0
    return sign * m[-1][-1]


def rank(a):
    m = [[Fraction(x) for x in row] for row in a]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if m[i][c]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        p = m[r][c]
        m[r] = [x / p for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


def inertia(a):
    """Exact symmetric congruence; returns (positive, zero, negative)."""
    n = len(a)
    m = [[Fraction(x) for x in row] for row in a]
    positive = negative = 0
    i = 0
    while i < n:
        pivot = next((j for j in range(i, n) if m[j][j]), None)
        if pivot is None:
            pair = next(
                ((r, c) for r in range(i, n) for c in range(r + 1, n) if m[r][c]),
                None,
            )
            if pair is None:
                break
            r, c = pair
            # Congruence operation: basis vector r <- r + c.
            for k in range(n):
                m[r][k] += m[c][k]
            for k in range(n):
                m[k][r] += m[k][c]
            continue
        if pivot != i:
            m[i], m[pivot] = m[pivot], m[i]
            for row in m:
                row[i], row[pivot] = row[pivot], row[i]
        d = m[i][i]
        positive += int(d > 0)
        negative += int(d < 0)
        old = [m[r][i] for r in range(i + 1, n)]
        for rr, r in enumerate(range(i + 1, n)):
            for cc, c in enumerate(range(i + 1, n)):
                m[r][c] -= old[rr] * old[cc] / d
        for r in range(i + 1, n):
            m[r][i] = m[i][r] = Fraction(0)
        i += 1
    return positive, n - positive - negative, negative


def incidence(vertices, edges):
    pos = {v: i for i, v in enumerate(vertices)}
    r = [[0 for _ in edges] for _ in vertices]
    for j, (u, v) in enumerate(edges):
        r[pos[u]][j] = 1
        r[pos[v]][j] = 1
    return r


def line_adjacency(edges):
    n = len(edges)
    a = [[0] * n for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        for j in range(i):
            x, y = edges[j]
            if u == x or u == y or v == x or v == y:
                a[i][j] = a[j][i] = 1
    return a


def principal_delete(a, j):
    return [[x for c, x in enumerate(row) if c != j] for r, row in enumerate(a) if r != j]


def signature(inert):
    return inert[0] - inert[2]


def main():
    # Paone's rooted C4--C5 module.  The root edge is listed first.
    vertices_m = list(range(10))
    edges_m = [
        (0, 1),
        (1, 2), (2, 3), (3, 4), (4, 1),
        (2, 5),
        (5, 6), (6, 7), (7, 8), (8, 9), (9, 5),
    ]
    vertices_j = list(range(1, 10))
    edges_j = edges_m[1:]

    rj = incidence(vertices_j, edges_j)
    rt_r = matmul(transpose(rj), rj)
    r_rt = matmul(rj, transpose(rj))
    b = line_adjacency(edges_j)
    q_minus_2 = matsub(r_rt, identity(len(vertices_j), 2))
    k = line_adjacency(edges_m)
    b_from_k = principal_delete(k, 0)

    assert matsub(rt_r, identity(len(edges_j), 2)) == b
    assert b_from_k == b
    assert rank(q_minus_2) == len(vertices_j) - 1
    assert rank(b) == len(edges_j) - 1

    in_b = inertia(b)
    in_k = inertia(k)
    det_b = determinant(b)
    det_k = determinant(k)
    assert in_b == (5, 1, 4)
    assert in_k == (6, 0, 5)
    assert det_b == 0
    assert det_k == -8
    assert in_k == (in_b[0] + 1, 0, in_b[2] + 1)

    c_j = len(edges_j) - len(vertices_j) + 1
    c_m = len(edges_m) - len(vertices_m) + 1
    assert c_j == c_m == 2
    assert signature(in_b) == signature(in_k) == 1

    result = {
        "B_det": det_b,
        "B_inertia": in_b,
        "B_nullity": len(b) - rank(b),
        "K_det": det_k,
        "K_inertia": in_k,
        "K_root_cofactor": determinant(b_from_k),
        "Q_minus_2_nullity": len(q_minus_2) - rank(q_minus_2),
        "cyclomatic_J": c_j,
        "cyclomatic_M": c_m,
        "incidence_identity": True,
        "signature_J": signature(in_b),
        "signature_M": signature(in_k),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()

