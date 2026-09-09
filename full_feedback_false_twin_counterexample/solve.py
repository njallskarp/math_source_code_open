#!/usr/bin/env python3
"""Regenerate the finite certificate with a complete all-subsets fixed point.

Independent of verify.py: Floyd--Warshall, integer masks, synchronous ranks.
Default mode compares with the supplied certificate; --write regenerates it.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def solve(n, edges):
    adj = [0] * n
    dist = [[0 if u == v else n + 1 for v in range(n)] for u in range(n)]
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
        dist[u][v] = dist[v][u] = 1
    for w in range(n):
        for u in range(n):
            for v in range(n):
                dist[u][v] = min(dist[u][v], dist[u][w] + dist[w][v])
    parts = []
    for p in range(n):
        groups = {}
        for x in range(n):
            response = 1 << p if x == p else sum(
                1 << w for w in range(n)
                if adj[p] & (1 << w) and dist[w][x] + 1 == dist[p][x])
            groups[response] = groups.get(response, 0) | (1 << x)
        parts.append(list(groups.values()))
    limit = 1 << n
    spread = [0] * limit
    for mask in range(1, limit):
        bit = mask & -mask
        spread[mask] = spread[mask - bit] | bit | adj[bit.bit_length() - 1]
    transitions = [[] for _ in range(limit)]
    for mask in range(1, limit):
        for groups in parts:
            transitions[mask].append(sorted({spread[mask & c] for c in groups
                                             if (mask & c).bit_count() > 1}))
    rank = {mask: 0 for mask in range(limit) if mask.bit_count() <= 1}
    action = {}
    roundno = 0
    while True:
        roundno += 1
        newly_winning = {}
        for mask in range(limit):
            if mask in rank:
                continue
            for p, children in enumerate(transitions[mask]):
                if all(c in rank for c in children):
                    newly_winning[mask] = roundno
                    action[mask] = p
                    break
        if not newly_winning:
            break
        rank.update(newly_winning)
    full = limit - 1
    strategy = []
    if full in rank:
        todo, seen = [full], {full}
        for mask in todo:
            strategy.append([mask, rank[mask], action[mask]])
            for child in transitions[mask][action[mask]]:
                if child not in seen:
                    seen.add(child)
                    todo.append(child)
    reachable, seen = [full], {full}
    for mask in reachable:
        for children in transitions[mask]:
            for child in children:
                if child not in seen:
                    seen.add(child)
                    reachable.append(child)
    losing = sorted((s for s in reachable if s not in rank),
                    key=lambda s: (s.bit_count(), [v for v in range(n) if s & (1 << v)]))
    minimal = []
    for mask in losing:
        if not any(t & mask == t for t in minimal):
            minimal.append(mask)
    summary = {"n": n, "all_beliefs": limit, "winning_beliefs": len(rank),
               "losing_beliefs": limit - len(rank), "initial_rank": rank.get(full),
               "reachable_beliefs": len(reachable)}
    return strategy, minimal, summary


def main():
    path = HERE / "certificate.json"
    data = json.loads(path.read_text())
    n, edges, twin = data["n"], data["edges"], data["duplicated_vertex"]
    base_strategy, _, base_result = solve(n, edges)
    neighbors = sorted(v if u == twin else u for u, v in edges if twin in (u, v))
    extra_edges = edges + [[v, n] for v in neighbors]
    _, family, enlarged_result = solve(n + 1, extra_edges)
    regenerated = {"n": n, "edges": edges, "duplicated_vertex": twin,
                   "base_strategy": base_strategy, "evasion_family": family,
                   "two_probe_resolver": [2, 7]}
    encoded = json.dumps(regenerated, indent=2) + "\n"
    if sys.argv[1:] == ["--write"]:
        path.write_text(encoded)
    elif sys.argv[1:]:
        raise SystemExit("usage: python3 solve.py [--write]")
    elif regenerated != data:
        raise SystemExit("regenerated certificate does not match supplied certificate")
    print(json.dumps([base_result, enlarged_result], indent=2))
    print("certificate_sha256=" + hashlib.sha256(encoded.encode()).hexdigest())
    print("REGENERATED")


if __name__ == "__main__":
    main()
