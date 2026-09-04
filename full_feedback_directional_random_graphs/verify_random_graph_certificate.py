#!/usr/bin/env python3
"""Exact audit for the two-hop full-feedback random-graph certificate.

Only the Python standard library is used.  All probability calculations use
fractions; graph enumeration is exhaustive and deterministic.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb, factorial


def edge_pairs(n: int) -> list[tuple[int, int]]:
    return list(combinations(range(n), 2))


def graph_from_mask(n: int, mask: int) -> list[set[int]]:
    adjacency = [set() for _ in range(n)]
    for bit, (a, b) in enumerate(edge_pairs(n)):
        if (mask >> bit) & 1:
            adjacency[a].add(b)
            adjacency[b].add(a)
    return adjacency


def two_hop_resolving(adjacency: list[set[int]], v: int = 0) -> bool:
    neighbourhood = adjacency[v]
    outside = set(range(len(adjacency))) - neighbourhood - {v}
    codes = [frozenset(neighbourhood & adjacency[x]) for x in outside]
    return all(len(code) >= 2 for code in codes) and len(set(codes)) == len(codes)


def distances(adjacency: list[set[int]], start: int) -> list[int | None]:
    result: list[int | None] = [None] * len(adjacency)
    result[start] = 0
    queue = [start]
    for x in queue:
        assert result[x] is not None
        for y in adjacency[x]:
            if result[y] is None:
                result[y] = result[x] + 1
                queue.append(y)
    return result


def full_feedback_profiles(adjacency: list[set[int]], v: int = 0) -> list[tuple[int, ...]]:
    profiles: list[tuple[int, ...]] = []
    for robber in range(len(adjacency)):
        if robber == v:
            profiles.append((v,))
            continue
        distance = distances(adjacency, robber)
        if distance[v] is None:
            raise AssertionError("certificate graph must be connected")
        profiles.append(
            tuple(sorted(x for x in adjacency[v] if distance[x] == distance[v] - 1))
        )
    return profiles


def elementary_symmetric(weights: list[Fraction], degree: int) -> Fraction:
    coefficients = [Fraction(0) for _ in range(degree + 1)]
    coefficients[0] = Fraction(1)
    for weight in weights:
        for j in range(degree, 0, -1):
            coefficients[j] += weight * coefficients[j - 1]
    return coefficients[degree]


def certificate_probability_formula(n: int, p: Fraction) -> Fraction:
    q = 1 - p
    total = Fraction(0)
    N = n - 1
    for d in range(N + 1):
        m = N - d
        weights: list[Fraction] = []
        for k in range(2, d + 1):
            weights.extend([p**k * q ** (d - k)] * comb(d, k))
        conditional = factorial(m) * elementary_symmetric(weights, m)
        total += comb(N, d) * p**d * q ** (N - d) * conditional
    return total


def half_probability_closed_form(n: int) -> Fraction:
    N = n - 1
    total = Fraction(0)
    for d in range(N + 1):
        m = N - d
        allowed = 2**d - d - 1
        falling = 1
        for j in range(m):
            falling *= allowed - j
        if falling < 0:
            # This cannot occur before a zero factor; retaining zero is the
            # combinatorial falling-factorial convention for m > allowed.
            falling = 0
        conditional = Fraction(falling, 2 ** (d * m))
        total += Fraction(comb(N, d), 2**N) * conditional
    return total


def certificate_probability_enumeration(n: int, p: Fraction) -> Fraction:
    pairs = edge_pairs(n)
    q = 1 - p
    total = Fraction(0)
    for mask in range(1 << len(pairs)):
        adjacency = graph_from_mask(n, mask)
        if two_hop_resolving(adjacency):
            edges = mask.bit_count()
            total += p**edges * q ** (len(pairs) - edges)
    return total


def collision_union_bound(n: int, p: Fraction) -> Fraction:
    q = 1 - p
    N = n - 1
    small = Fraction(0)
    if N:
        small = N * q * (1 - p * p) ** (n - 2)
        if n >= 3:
            small += N * q * (n - 2) * p * p * (1 - p * p) ** (n - 3)
    collision = Fraction(0)
    if n >= 3:
        collision = comb(N, 2) * q * q * (1 - 2 * p * p * q) ** (n - 3)
    return small + collision


def main() -> None:
    digest_rows: list[str] = []
    graph_total = 0
    certificate_total = 0
    profile_checks = 0

    for n in range(2, 7):
        pair_count = comb(n, 2)
        count = 0
        for mask in range(1 << pair_count):
            adjacency = graph_from_mask(n, mask)
            graph_total += 1
            if two_hop_resolving(adjacency):
                count += 1
                certificate_total += 1
                profiles = full_feedback_profiles(adjacency)
                assert len(profiles) == len(set(profiles))
                profile_checks += 1
        probability = Fraction(count, 1 << pair_count)
        formula = certificate_probability_formula(n, Fraction(1, 2))
        closed = half_probability_closed_form(n)
        assert probability == formula == closed
        assert 1 - probability <= collision_union_bound(n, Fraction(1, 2))
        row = f"n={n} graphs={1 << pair_count} certificates={count} probability={probability}"
        print(row)
        digest_rows.append(row)

    weighted_checks = 0
    for n in range(2, 6):
        for p in (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3)):
            direct = certificate_probability_enumeration(n, p)
            formula = certificate_probability_formula(n, p)
            assert direct == formula
            assert 1 - direct <= collision_union_bound(n, p)
            weighted_checks += 1
            digest_rows.append(f"weighted n={n} p={p} probability={direct}")

    digest = sha256("\n".join(digest_rows).encode()).hexdigest()
    print(f"profile_implication_checks={profile_checks}")
    print(f"weighted_formula_checks={weighted_checks}")
    print(f"graphs_examined={graph_total}")
    print(f"certificate_graphs={certificate_total}")
    print(f"audit_sha256={digest}")


if __name__ == "__main__":
    main()
