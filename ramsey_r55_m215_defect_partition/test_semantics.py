#!/usr/bin/env python3
"""Nonvacuous graph relabeling controls for the canonical-anchor rule."""
from itertools import permutations
from partition import canonical_anchor_key


def require(value, message):
    if not value:
        raise ValueError(message)


def control(edges):
    n = 6
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    types = [(len(row), 0, 0) for row in adj]
    # The type-class selection is equivariant. These small graphs are transport
    # controls, not claimed to have order-43 deficiency labels.
    candidates = [v for v in range(n) if len(adj[v]) == max(map(len, adj))]
    require(len(candidates) > 1, "control needs multiple candidate anchors")
    key = canonical_anchor_key(adj, types, candidates)
    vectors = [canonical_anchor_key(adj, types, [v]) for v in candidates]
    tests = 0
    for perm in permutations(range(n)):
        transported = [set() for _ in range(n)]
        new_types = [None] * n
        for v in range(n):
            transported[perm[v]] = {perm[w] for w in adj[v]}
            new_types[perm[v]] = types[v]
        new_candidates = [perm[v] for v in candidates]
        require(canonical_anchor_key(transported, new_types, new_candidates) == key,
                "canonical key changed under graph relabeling")
        tests += 1
    # Compare every candidate pair, including ties, to the scalar key specified
    # in the formula theorem. The base-44 proof itself is in PROOF.md.
    def scalar(vector):
        out = 0
        for digit in vector:
            out = 44 * out + digit
        return out
    for a in vectors:
        for b in vectors:
            require((a <= b) == (scalar(a) <= scalar(b)), "scalar comparison disagrees")
    return tests, len(set(vectors))


if __name__ == "__main__":
    asymmetric = ((0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (4, 5), (1, 4))
    cycle = tuple((v, (v + 1) % 6) for v in range(6))
    first, distinct = control(asymmetric)
    second, tied = control(cycle)
    require(distinct > 1 and tied == 1, "missing distinct-key or tied-key control")
    try:
        canonical_anchor_key([], [], [])
    except ValueError:
        pass
    else:
        raise ValueError("empty candidate set accepted")
    print(f"PASS: {first + second} relabelings; distinct and tied minima; empty-anchor rejection")
