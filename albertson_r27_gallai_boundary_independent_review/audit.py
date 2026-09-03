#!/usr/bin/env python3
"""Independent audit of the Albertson r=27 two-clique boundary lemma.

The target verifier reduces matching pairs to five endpoint orbits.  This
checker instead enumerates every abstract Q-support/endpoint-partner type,
constructs the claimed coloring, and checks the 280 labelled rigid graphs.
It also regression-checks the same proof architecture for all admissible
two-clique parameters with 5 <= k <= 40; that finite sweep is evidence for,
not a proof of, the general statement recorded in the accompanying review.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
import platform


Q = tuple(f"q{i}" for i in range(8))
A = tuple(f"a{i}" for i in range(22))
B = tuple(f"b{i}" for i in range(23))
V = A + B + Q
A0, B0 = A[0], B[0]


def pair(x: str, y: str) -> frozenset[str]:
    assert x != y
    return frozenset((x, y))


def abstract_matching(
    low_side: tuple[str, ...], q_support: tuple[str, ...], endpoint_partner: str | None
) -> dict[str, str]:
    """Choose one representative matching of an abstract endpoint type."""
    assert len(set(q_support)) == len(q_support)
    assert endpoint_partner is None or endpoint_partner in q_support
    result: dict[str, str] = {}
    ordinary = iter(low_side[1:])
    for q in q_support:
        result[q] = low_side[0] if q == endpoint_partner else next(ordinary)
    assert len(set(result.values())) == len(q_support)
    return result


def coloring(
    match_a: dict[str, str], match_b: dict[str, str], bridge: bool
) -> list[tuple[str, ...]]:
    """Construct and definition-check the target's 26 color classes."""
    classes: dict[str, list[str]] = {q: [q] for q in Q}
    for q, a in match_a.items():
        classes[q].append(a)
    for q, b in match_b.items():
        classes[q].append(b)

    residual_a = [a for a in A if a not in match_a.values()]
    residual_b = [b for b in B if b not in match_b.values()]
    assert len(residual_a) == len(residual_b) == 18
    if bridge and A0 in residual_a and B0 in residual_b:
        bad = next(i for i, (a, b) in enumerate(zip(residual_a, residual_b)) if (a, b) == (A0, B0))
        other = 0 if bad != 0 else 1
        residual_b[bad], residual_b[other] = residual_b[other], residual_b[bad]

    result = [tuple(cls) for cls in classes.values()]
    result.extend((a, b) for a, b in zip(residual_a, residual_b))
    assert len(result) == 26
    flat = [vertex for cls in result for vertex in cls]
    assert len(flat) == len(V) and set(flat) == set(V)

    def is_known_nonedge(x: str, y: str) -> bool:
        if x in Q and y in A:
            x, y = y, x
        if x in Q and y in B:
            x, y = y, x
        if x in A and y in Q:
            return match_a.get(y) == x
        if x in B and y in Q:
            return match_b.get(y) == x
        if (x in A and y in B) or (x in B and y in A):
            return not (bridge and {x, y} == {A0, B0})
        return False

    for cls in result:
        for x, y in combinations(cls, 2):
            assert is_known_nonedge(x, y)
    return result


def audit_all_matching_types() -> tuple[int, int, int]:
    """Enumerate all Q-support and endpoint-partner signatures."""
    a_types = [
        (support, endpoint)
        for support in combinations(Q, 4)
        for endpoint in (None,) + support
    ]
    b_types = [
        (support, endpoint)
        for support in combinations(Q, 5)
        for endpoint in (None,) + support
    ]
    no_bridge = compatible_bridge = incompatible_bridge = 0
    for support_a, partner_a in a_types:
        match_a = abstract_matching(A, support_a, partner_a)
        for support_b, partner_b in b_types:
            match_b = abstract_matching(B, support_b, partner_b)
            coloring(match_a, match_b, bridge=False)
            no_bridge += 1
            incompatible = (
                partner_a is not None
                and partner_b is not None
                and partner_a == partner_b
            )
            if incompatible:
                incompatible_bridge += 1
            else:
                coloring(match_a, match_b, bridge=True)
                compatible_bridge += 1
    assert no_bridge == 117_600
    assert compatible_bridge == 107_800
    assert incompatible_bridge == 9_800
    return no_bridge, compatible_bridge, incompatible_bridge


def rigid_graph(
    support_a: frozenset[str], support_b: frozenset[str], qstar: str
) -> tuple[set[frozenset[str]], set[frozenset[str]]]:
    """Construct G and its complement directly from the forced row supports."""
    assert len(support_a) == 3 and len(support_b) == 4
    assert support_a.isdisjoint(support_b)
    assert support_a | support_b | {qstar} == set(Q)

    def is_g_edge(x: str, y: str) -> bool:
        if (x in A and y in A) or (x in B and y in B) or (x in Q and y in Q):
            return True
        if (x in A and y in B) or (x in B and y in A):
            return {x, y} == {A0, B0}
        if x in Q:
            x, y = y, x
        if x in A and y in Q:
            h_neighbors = support_a | ({qstar} if x == A0 else set())
            return y not in h_neighbors
        if x in B and y in Q:
            h_neighbors = support_b | ({qstar} if x == B0 else set())
            return y not in h_neighbors
        raise AssertionError((x, y))

    all_pairs = {pair(x, y) for x, y in combinations(V, 2)}
    g = {edge for edge in all_pairs if is_g_edge(*tuple(edge))}
    return g, all_pairs - g


def degree(edges: set[frozenset[str]], vertex: str) -> int:
    return sum(vertex in edge for edge in edges)


def is_connected(edges: set[frozenset[str]]) -> bool:
    reached = {V[0]}
    frontier = [V[0]]
    while frontier:
        x = frontier.pop()
        for edge in edges:
            if x not in edge:
                continue
            y = next(iter(edge - {x}))
            if y not in reached:
                reached.add(y)
                frontier.append(y)
    return reached == set(V)


def audit_rigid_certificates() -> tuple[int, str]:
    records: list[dict[str, object]] = []
    for qstar in Q:
        remainder = tuple(q for q in Q if q != qstar)
        for chosen in combinations(remainder, 3):
            support_a = frozenset(chosen)
            support_b = frozenset(set(remainder) - support_a)
            g, h = rigid_graph(support_a, support_b, qstar)
            assert len(g) == 713 and len(h) == 665
            assert all(degree(g, low) == 26 for low in A + B)
            high_degrees = tuple(sorted(degree(g, q) for q in Q))
            assert high_degrees == (29, 29, 29, 29, 30, 30, 30, 50)
            assert is_connected(h)

            branches = set(A) | set(support_b) | {qstar}
            missing = {
                pair(x, y)
                for x, y in combinations(sorted(branches), 2)
                if pair(x, y) not in g
            }
            assert len(branches) == 27
            assert missing == {pair(A0, qstar)}
            internal_a = min(support_a)
            path = (A0, B0, internal_a, qstar)
            assert set(path[1:-1]).isdisjoint(branches)
            assert all(pair(x, y) in g for x, y in zip(path, path[1:]))
            records.append(
                {
                    "qstar": qstar,
                    "support_a": sorted(support_a),
                    "support_b": sorted(support_b),
                    "path": path,
                    "high_degrees": high_degrees,
                }
            )

    assert len(records) == 280
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return len(records), sha256(canonical.encode("ascii")).hexdigest()


def audit_general_parameters() -> tuple[int, str]:
    """Finite regression sweep for the general two-clique formulation."""
    records: list[tuple[int, int, int, int, int]] = []
    for k in range(5, 41):
        for a in range(2, k - 1):
            for b in range(2, k - 1):
                h = 2 * k - 1 - a - b
                x, y = k - b, k - a
                if h < 1 or x < 2 or y < 2:
                    continue
                if a - 1 < x or b - 1 < y:
                    continue

                # Forced support sizes (x-1), (y-1), and one q* partition Q.
                assert (x - 1) + (y - 1) + 1 == h
                support_a = set(range(x - 1))
                support_b = set(range(x - 1, h - 1))
                qstar = h - 1
                assert len(support_b) == y - 1
                assert support_a.isdisjoint(support_b)
                assert support_a | support_b | {qstar} == set(range(h))

                # Degree and coloring arithmetic for low vertices.
                assert (a - 1) + (h - (x - 1)) == k - 1
                assert (a - 1) + 1 + (h - x) == k - 1
                assert (b - 1) + (h - (y - 1)) == k - 1
                assert (b - 1) + 1 + (h - y) == k - 1
                residual = a - x
                assert residual == b - y and h + residual == k - 1

                # Branch set A union S_B union {q*} has k vertices; S_A is
                # nonempty and supplies the internal Q vertex for the missing edge.
                assert a + len(support_b) + 1 == k
                assert support_a
                assert a <= k - 2 and b <= k - 2
                records.append((k, a, b, h, residual))

    assert records
    canonical = json.dumps(records, separators=(",", ":"))
    return len(records), sha256(canonical.encode("ascii")).hexdigest()


def main() -> None:
    no_bridge, compatible, incompatible = audit_all_matching_types()
    rigid_count, rigid_digest = audit_rigid_certificates()
    general_count, general_digest = audit_general_parameters()
    print("PASS independent Albertson two-clique matching audit")
    print(f"python={platform.python_version()}")
    print(f"abstract no-bridge matching pairs checked={no_bridge}")
    print(f"compatible bridged matching pairs checked={compatible}")
    print(f"incompatible bridged matching pairs classified={incompatible}")
    print(f"labelled rigid TK27 graphs checked={rigid_count}")
    print(f"rigid_graph_manifest_sha256={rigid_digest}")
    print(f"general parameter tuples checked (5<=k<=40)={general_count}")
    print(f"general_parameter_manifest_sha256={general_digest}")


if __name__ == "__main__":
    main()
