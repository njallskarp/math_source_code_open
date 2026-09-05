#!/usr/bin/env python3
"""Independent finite checks for the girth-sensitive cubic-density review.

This does not prove the universal minimal-counterexample lemma.  It checks the
integer optimization independently and exhausts the finite tree/apex models
that underlie the equality-rigidity step through seven component vertices.
"""

from collections import deque
from fractions import Fraction
import hashlib
from itertools import combinations, product


G_MAX = 64
A_MAX = 1024
TREE_ORDER_MAX = 7


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def prufer_tree(sequence: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Decode a Pruefer word to a sorted labeled-tree edge tuple."""
    n = len(sequence) + 2
    degree = [1] * n
    for vertex in sequence:
        degree[vertex] += 1

    edges: list[tuple[int, int]] = []
    for vertex in sequence:
        leaf = next(i for i, value in enumerate(degree) if value == 1)
        edges.append(tuple(sorted((leaf, vertex))))
        degree[leaf] -= 1
        degree[vertex] -= 1

    remaining = [i for i, value in enumerate(degree) if value == 1]
    require(len(remaining) == 2, "Pruefer decoder did not leave two vertices")
    edges.append(tuple(remaining))
    return tuple(sorted(edges))


def distance_matrix(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)

    distances: list[list[int]] = []
    for root in range(n):
        row = [-1] * n
        row[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if row[v] == -1:
                    row[v] = row[u] + 1
                    queue.append(v)
        require(all(value >= 0 for value in row), "decoded tree is disconnected")
        distances.append(row)
    return distances


def audit_tree_apex_models() -> tuple[int, int, str]:
    """Check the local girth/equality step on every small labeled tree.

    An added apex is adjacent to a subset W of at least two tree vertices.  Its
    shortest new cycle has length 2 plus the minimum tree-distance in W.
    Equality |C| = girth-1 must force C to be a path and W to be its endpoints.
    """
    digest = hashlib.sha256()
    models = 0
    equality_models = 0

    for n in range(2, TREE_ORDER_MAX + 1):
        for sequence in product(range(n), repeat=n - 2):
            edges = prufer_tree(sequence)
            distances = distance_matrix(n, edges)
            tree_degrees = [0] * n
            for u, v in edges:
                tree_degrees[u] += 1
                tree_degrees[v] += 1
            endpoints = {i for i, value in enumerate(tree_degrees) if value == 1}

            for mask in range(1 << n):
                if mask.bit_count() < 2:
                    continue
                neighbors = [i for i in range(n) if mask & (1 << i)]
                closest = min(distances[u][v] for u, v in combinations(neighbors, 2))
                local_girth = closest + 2
                require(n >= local_girth - 1, "component-radius inequality failed")

                equality = n == local_girth - 1
                if equality:
                    require(
                        sorted(tree_degrees) == [1, 1] + [2] * (n - 2),
                        "equality component is not a path",
                    )
                    require(set(neighbors) == endpoints, "equality apex misses path endpoints")
                    equality_models += 1

                digest.update(
                    f"{n}|{','.join(map(str, sequence))}|{mask}|{local_girth}|{int(equality)}\n".encode()
                )
                models += 1

    return models, equality_models, digest.hexdigest()


def audit_integer_profiles() -> tuple[int, int, str]:
    """Independently maximize b over component counts and excess values."""
    digest = hashlib.sha256()
    profiles = 0
    refined_rows = 0

    for g in range(3, G_MAX + 1):
        component_floor = g - 1
        rational_bound = Fraction(4 * (g - 1), 5 * g - 3)

        for a in range(1, A_MAX + 1):
            q_max = a // component_floor

            # Maximize over all possible component counts, rather than insert
            # q=floor(a/(g-1)) at the outset.
            possible_b = [
                (a + 2 * q) // 4
                for q in range(q_max + 1)
            ]
            b_max = max(possible_b)
            published_rhs = a + 2 * q_max
            require(b_max == published_rhs // 4, "component maximization mismatch")
            require(
                4 * b_max <= published_rhs < 4 * (b_max + 1),
                "integer bound mismatch",
            )
            require(
                Fraction(a, a + b_max) >= rational_bound,
                "rational density consequence failed",
            )

            # Cyclomatic excess beta=e(H)-a+q strengthens the intermediate
            # cut bound by exactly 2 beta.  Check the whole bounded parameter
            # box, including impossible profiles; only the monotone arithmetic
            # implication is asserted here.
            for q in range(q_max + 1):
                for beta in range(5):
                    refined_rhs = a + 2 * q - 2 * beta
                    require(refined_rhs <= published_rhs, "cyclomatic refinement failed")
                    refined_rows += 1

            digest.update(f"{g}|{a}|{q_max}|{published_rhs}|{b_max}\n".encode())
            profiles += 1

    require(Fraction(4 * (3 - 1), 5 * 3 - 3) == Fraction(2, 3), "g=3 mismatch")
    require(Fraction(4 * (5 - 1), 5 * 5 - 3) == Fraction(8, 11), "g=5 mismatch")
    require(Fraction(4 * (6 - 1), 5 * 6 - 3) == Fraction(20, 27), "g=6 mismatch")
    return profiles, refined_rows, digest.hexdigest()


def audit_equality_divisibility() -> tuple[int, str]:
    """Check the exact arithmetic conditions forced by rational equality."""
    digest = hashlib.sha256()
    cases = 0
    for g in range(3, 101):
        for q in range(1, 501):
            a = q * (g - 1)
            numerator = q * (g + 1)
            if numerator % 4:
                continue
            b = numerator // 4
            require(
                4 * b == a + 2 * (a // (g - 1)),
                "exact equality bound mismatch",
            )
            require(
                Fraction(a, a + b) == Fraction(4 * (g - 1), 5 * g - 3),
                "equality density mismatch",
            )
            digest.update(f"{g}|{q}|{a}|{b}\n".encode())
            cases += 1
    return cases, digest.hexdigest()


def main() -> None:
    profiles, refined_rows, profile_hash = audit_integer_profiles()
    models, equality_models, tree_hash = audit_tree_apex_models()
    equality_cases, equality_hash = audit_equality_divisibility()

    print(f"integer profiles checked: {profiles}")
    print(f"cyclomatic-refinement rows checked: {refined_rows}")
    print(f"integer-profile sha256: {profile_hash}")
    print(f"tree/apex models checked: {models}")
    print(f"tree/apex equality models: {equality_models}")
    print(f"tree/apex stream sha256: {tree_hash}")
    print(f"equality divisibility cases checked: {equality_cases}")
    print(f"equality-divisibility sha256: {equality_hash}")
    print("all independent checks passed")


if __name__ == "__main__":
    main()
