"""Solver-free possible-clique recursion and explicit threshold-grid clauses."""
from itertools import combinations


def require(ok, message):
    if not ok:
        raise ValueError(message)


def clique_rows(rows, free):
    """Generate possible monochromatic cliques by adjacency intersections."""
    result = set()
    for color in '01':
        adj = [sum(1 << v for v in range(43) if v != u and rows[u][v] in (color, '.'))
               for u in range(43)]

        def visit(chosen, candidates):
            if len(chosen) == 5:
                ids = [free[tuple(sorted(p))] for p in combinations(chosen, 2)
                       if tuple(sorted(p)) in free]
                sign = -1 if color == '1' else 1
                result.add(tuple(sorted(sign * v for v in ids)))
                return
            while candidates:
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length() - 1
                visit(chosen + [v], candidates & adj[v])

        visit([], (1 << 43) - 1)
    return result


def sequential(lits, threshold, top):
    """Independent explicit threshold-grid reconstruction of the counter."""
    n = len(lits)
    if threshold >= n:
        return [], top, {}
    if threshold == n - 1:
        return [[-x for x in lits]], top, {}
    if threshold == 0:
        return [[-x] for x in lits], top, {}
    require(0 < threshold < n - 1, 'counter threshold')
    nodes = {}
    clauses = []

    def node(k, j):
        nonlocal top
        if (k, j) not in nodes:
            top += 1
            nodes[k, j] = top
        return nodes[k, j]

    for j in range(n - threshold):
        clauses.append([-lits[j], node(0, j)])
        for k in range(threshold):
            a = node(k, j)
            if j + 1 < n - threshold:
                clauses.append([-a, node(k, j + 1)])
            if k + 1 < threshold:
                clauses.append([-lits[j + k + 1], -a, node(k + 1, j)])
            else:
                clauses.append([-lits[j + threshold], -a])
    return clauses, top, nodes
