#!/usr/bin/env python3
"""Separate literal-graph/disjoint-edge check; imports no primary checker."""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    # Each triangle type is a literal graph in an 8-vertex E/X/T universe.
    groups = {'E': [0, 1, 2], 'X': [3, 4, 5], 'T': [6, 7]}
    corrections = {'EEE': 3, 'EEX': 1, 'EXX': 0, 'XXX': 0, 'EET': 2, 'EXT': 0, 'XXT': -1}
    rows = []
    for word, correction in corrections.items():
        used = dict.fromkeys(groups, 0)
        vertices = []
        for letter in word:
            vertices.append(groups[letter][used[letter]])
            used[letter] += 1
        adj = [[0] * 8 for _ in range(8)]
        for i, j in combinations(vertices, 2):
            adj[i][j] = adj[j][i] = 1
        local = [sum(adj[i][j] * adj[v][i] * adj[v][j] for i, j in combinations(range(8), 2))
                 for v in range(8)]
        s_e = sum(local[v] for v in groups['E'])
        s_x = sum(local[v] for v in groups['X'])
        d = sum(adj[i][j] * sum(adj[i][v] * adj[j][v] for v in range(8))
                for i, j in combinations(groups['X'], 2))
        require(d == s_x - s_e + correction, 'literal triangle identity')
        rows.append((word, s_e, s_x, d))

    # A different predicate: ignore alpha and remove exactly the literal stars.
    universe = list(combinations(range(6), 2))
    nonstars = 0
    min_disjoint = 10
    for indices in combinations(range(15), 5):
        edges = [set(universe[i]) for i in indices]
        if any(all(v in edge for edge in edges) for v in range(6)):
            continue
        disjoint = sum(not (left & right) for left, right in combinations(edges, 2))
        require(disjoint >= 2, 'at least two disjoint pairs')
        min_disjoint = min(min_disjoint, disjoint)
        nonstars += 1
    require((nonstars, min_disjoint) == (2997, 2), 'nonstar census')
    require(10 + 2 * (10 - min_disjoint) == 26, 'square identity')

    # Direct expansion of the stated signed sum, using no certificate values.
    base = 28 * 100 - 13 * 93
    lower = base + 3 * 10 + 28 * 2 + 2 * (2 * 3) - 2 * 60
    edges_j = 28 * (21 - 6 - 1) // 2
    require(lower - 8 * edges_j == 1, 'strict averaging margin')
    print('PASS literal triangle rows=' + repr(rows))
    print('PASS nonstars=2997 minimum_disjoint_edge_pairs=2')
    print('PASS exact averaging margin=1; external U14 upper bound=60')


if __name__ == '__main__':
    main()
