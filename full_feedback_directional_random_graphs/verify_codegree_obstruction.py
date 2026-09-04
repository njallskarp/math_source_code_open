#!/usr/bin/env python3
"""Exact audit of the degree--codegree full-feedback criterion.

Only the Python standard library and exact integer/set operations are used.
The universal theorem is proved in CODEGREE_OBSTRUCTION.md; this program
audits its definitions and constants on finite instances.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, combinations_with_replacement


Graph = list[set[int]]


def edge_pairs(n: int) -> list[tuple[int, int]]:
    return list(combinations(range(n), 2))


def graph_from_mask(n: int, mask: int) -> Graph:
    adjacency = [set() for _ in range(n)]
    for bit, (x, y) in enumerate(edge_pairs(n)):
        if (mask >> bit) & 1:
            adjacency[x].add(y)
            adjacency[y].add(x)
    return adjacency


def distances(adjacency: Graph, start: int) -> list[int | None]:
    distance: list[int | None] = [None] * len(adjacency)
    distance[start] = 0
    queue = [start]
    for x in queue:
        assert distance[x] is not None
        for y in adjacency[x]:
            if distance[y] is None:
                distance[y] = distance[x] + 1
                queue.append(y)
    return distance


def response(adjacency: Graph, probe: int, robber: int) -> tuple[int, ...] | None:
    if probe == robber:
        return (probe,)
    distance = distances(adjacency, robber)
    if distance[probe] is None:
        return None
    return tuple(
        sorted(x for x in adjacency[probe] if distance[x] == distance[probe] - 1)
    )


def probe_resolves(adjacency: Graph, probe: int) -> bool:
    profiles = [response(adjacency, probe, robber) for robber in range(len(adjacency))]
    return None not in profiles and len(profiles) == len(set(profiles))


def local_criterion(adjacency: Graph, v: int) -> bool:
    n = len(adjacency)
    outside = set(range(n)) - adjacency[v] - {v}
    if any(len(adjacency[v] & adjacency[x]) < 2 for x in outside):
        return False
    for x, y in combinations(outside, 2):
        symmetric_difference = len(adjacency[x] ^ adjacency[y])
        if symmetric_difference < n - len(adjacency[v]):
            return False
    return True


def global_criterion(adjacency: Graph) -> bool:
    n = len(adjacency)
    delta = min(map(len, adjacency))
    codegrees = {
        (x, y): len(adjacency[x] & adjacency[y])
        for x, y in combinations(range(n), 2)
    }
    if any(
        codegrees[x, y] < 2
        for x, y in combinations(range(n), 2)
        if y not in adjacency[x]
    ):
        return False
    maximum_codegree = max(codegrees.values(), default=0)
    return 3 * delta - 2 * maximum_codegree >= n


def petersen_complement() -> Graph:
    petersen_edges: set[tuple[int, int]] = set()
    for i in range(5):
        petersen_edges.add(tuple(sorted((i, (i + 1) % 5))))
        petersen_edges.add((i, i + 5))
        petersen_edges.add(tuple(sorted((i + 5, ((i + 2) % 5) + 5))))
    adjacency = [set() for _ in range(10)]
    for x, y in combinations(range(10), 2):
        if (x, y) not in petersen_edges:
            adjacency[x].add(y)
            adjacency[y].add(x)
    return adjacency


def c5_independent_blowup(m: int) -> Graph:
    n = 5 * m
    adjacency = [set() for _ in range(n)]
    for fiber in range(5):
        next_fiber = (fiber + 1) % 5
        for a in range(fiber * m, (fiber + 1) * m):
            for b in range(next_fiber * m, (next_fiber + 1) * m):
                adjacency[a].add(b)
                adjacency[b].add(a)
    return adjacency


def simultaneous_pair_resolves(adjacency: Graph, a: int, b: int) -> bool:
    profiles = [
        (response(adjacency, a, robber), response(adjacency, b, robber))
        for robber in range(len(adjacency))
    ]
    return len(profiles) == len(set(profiles))


def second_round_resolves_territory(adjacency: Graph, territory: set[int], a: int, b: int) -> bool:
    profiles = {
        (response(adjacency, a, robber), response(adjacency, b, robber))
        for robber in territory
    }
    return len(profiles) == len(territory)


def main() -> None:
    digest_rows: list[str] = []
    graphs_examined = 0
    local_instances = 0
    global_graphs = 0

    for n in range(2, 7):
        graph_count = 1 << len(edge_pairs(n))
        local_n = 0
        global_n = 0
        for mask in range(graph_count):
            adjacency = graph_from_mask(n, mask)
            graphs_examined += 1
            for v in range(n):
                if local_criterion(adjacency, v):
                    assert probe_resolves(adjacency, v)
                    local_instances += 1
                    local_n += 1
            if global_criterion(adjacency):
                assert all(probe_resolves(adjacency, v) for v in range(n))
                global_graphs += 1
                global_n += 1
        row = f"n={n} graphs={graph_count} local_instances={local_n} global_graphs={global_n}"
        print(row)
        digest_rows.append(row)

    complement = petersen_complement()
    degrees = sorted({len(neighbours) for neighbours in complement})
    adjacent_codegrees = sorted(
        {
            len(complement[x] & complement[y])
            for x, y in combinations(range(10), 2)
            if y in complement[x]
        }
    )
    nonadjacent_codegrees = sorted(
        {
            len(complement[x] & complement[y])
            for x, y in combinations(range(10), 2)
            if y not in complement[x]
        }
    )
    assert degrees == [6]
    assert adjacent_codegrees == [3]
    assert nonadjacent_codegrees == [4]
    assert global_criterion(complement)
    assert all(probe_resolves(complement, v) for v in range(10))
    boundary_row = "petersen_complement=(n,d,lambda,mu)=(10,6,3,4) boundary=10"
    print(boundary_row)
    digest_rows.append(boundary_row)

    blowup_checks = 0
    for m in range(3, 13):
        adjacency = c5_independent_blowup(m)
        assert all(
            not simultaneous_pair_resolves(adjacency, a, b)
            for a, b in combinations_with_replacement(range(5 * m), 2)
        )
        territory = set(range(2 * m, 5 * m))
        assert second_round_resolves_territory(adjacency, territory, 2 * m, 3 * m)
        blowup_checks += 1
    blowup_row = "c5_independent_blowups=m=3..12 no_one_round_pair explicit_second_round_ok"
    print(blowup_row)
    digest_rows.append(blowup_row)

    digest = sha256("\n".join(digest_rows).encode()).hexdigest()
    print(f"graphs_examined={graphs_examined}")
    print(f"local_criterion_instances={local_instances}")
    print(f"global_criterion_graphs={global_graphs}")
    print(f"blowup_family_checks={blowup_checks}")
    print(f"audit_sha256={digest}")


if __name__ == "__main__":
    main()
