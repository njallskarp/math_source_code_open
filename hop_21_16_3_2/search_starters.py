#!/usr/bin/env python3
"""Search for odd-order cyclic HOP starters of contracted type [16,3,2].

Vertices 0,...,19 are cyclic and vertex 20 is infinity.  Each vertex is a
married couple with endpoints (v,0),(v,1).  A valid contracted HOP factor is
represented by a perfect matching of the 42 endpoints; adjoining the 21
spouse edges turns it into alternating cycles.

For n=21, the Jerade--Sajna three-starter construction is determined by F1
and F3.  F2 is the half-turn of F1, except that the pink/blue difference-10
2-cycle is replaced by the two black difference-10 edges.

This is exploratory search code.  A separately written definition-level
checker should be used for any retained certificate.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass

N = 20
INF = 20
VERTICES = tuple(range(21))
Endpoint = tuple[int, int]
Edge = tuple[Endpoint, Endpoint]
Orbit = tuple[object, ...]


def canon_edge(a: Endpoint, b: Endpoint) -> Edge:
    if a > b:
        a, b = b, a
    assert a[0] != b[0]
    return a, b


def orbit_key(edge: Edge) -> Orbit:
    (u, a), (v, b) = edge
    if u == INF or v == INF:
        if v == INF:
            u, v, a, b = v, u, b, a
        assert u == INF and v != INF
        return ("inf", a, b)
    d = (v - u) % N
    if d > N // 2:
        u, v, a, b = v, u, b, a
        d = N - d
    assert 1 <= d <= N // 2
    if d == N // 2 and a != b:
        return (d, 0, 1)
    return (d, a, b)


def all_regular_orbits() -> tuple[Orbit, ...]:
    out: list[Orbit] = []
    for d in range(1, N // 2):
        for a in range(2):
            for b in range(2):
                out.append((d, a, b))
    for a in range(2):
        for b in range(2):
            out.append(("inf", a, b))
    assert len(out) == 40
    return tuple(out)


REGULAR_ORBITS = all_regular_orbits()


def cycle_edges(cycle: list[tuple[int, int]]) -> list[Edge]:
    """Turn (vertex,outgoing-endpoint-bit) data into a valid HOP cycle."""
    edges: list[Edge] = []
    for i, (u, out_bit) in enumerate(cycle):
        v, next_out = cycle[(i + 1) % len(cycle)]
        edges.append(canon_edge((u, out_bit), (v, 1 - next_out)))
    return edges


def factor_cycle_lengths(edges: list[Edge]) -> list[int]:
    adj: dict[int, list[int]] = {v: [] for v in VERTICES}
    for (u, _), (v, _) in edges:
        adj[u].append(v)
        adj[v].append(u)
    if any(len(adj[v]) != 2 for v in VERTICES):
        return []
    seen: set[int] = set()
    lengths: list[int] = []
    for root in VERTICES:
        if root in seen:
            continue
        cur, prev, length = root, None, 0
        while cur not in seen:
            seen.add(cur)
            length += 1
            x, y = adj[cur]
            nxt = x if x != prev else y
            prev, cur = cur, nxt
        lengths.append(length)
    return sorted(lengths, reverse=True)


def endpoint_mask(edge: Edge) -> int:
    ans = 0
    for v, bit in edge:
        ans |= 1 << (2 * v + bit)
    return ans


def orbit_rows(key: Orbit) -> list[Edge]:
    rows: list[Edge] = []
    if key[0] == "inf":
        _, ibit, fbit = key
        for x in range(N):
            rows.append(canon_edge((INF, int(ibit)), (x, int(fbit))))
    else:
        d, a, b = map(int, key)
        assert 1 <= d < N // 2
        for x in range(N):
            rows.append(canon_edge((x, a), ((x + d) % N, b)))
    assert len(rows) == N and len(set(rows)) == N
    assert all(orbit_key(e) == key for e in rows)
    return rows


@dataclass(frozen=True)
class Row:
    orbit: int
    mask: int
    edge: Edge


class ExactCover:
    def __init__(self, keys: list[Orbit], rng: random.Random, node_limit: int):
        self.keys = keys
        self.rng = rng
        self.node_limit = node_limit
        self.nodes = 0
        self.solutions = 0
        self.rows: list[Row] = []
        self.by_endpoint: list[list[int]] = [[] for _ in range(42)]
        self.by_orbit: list[list[int]] = [[] for _ in keys]
        for j, key in enumerate(keys):
            local = orbit_rows(key)
            rng.shuffle(local)
            for edge in local:
                rid = len(self.rows)
                row = Row(j, endpoint_mask(edge), edge)
                self.rows.append(row)
                self.by_orbit[j].append(rid)
                for ep in range(42):
                    if row.mask >> ep & 1:
                        self.by_endpoint[ep].append(rid)

    def solve(self) -> list[Edge] | None:
        full_ep = (1 << 42) - 1
        full_orbit = (1 << len(self.keys)) - 1
        chosen: list[int] = []

        def active(rid: int, used_ep: int, used_orbit: int) -> bool:
            row = self.rows[rid]
            return not (used_orbit >> row.orbit & 1) and not (used_ep & row.mask)

        def partial_cycle_ok(extra: Edge) -> bool:
            # A closed component cannot later be changed.  Reject every cycle
            # except the required lengths, including excess 2- or 17-cycles.
            es = [self.rows[r].edge for r in chosen] + [extra]
            adj: dict[int, list[int]] = defaultdict(list)
            for (u, _), (v, _) in es:
                adj[u].append(v)
                adj[v].append(u)
            closed: list[int] = []
            seen: set[int] = set()
            for root in adj:
                if root in seen:
                    continue
                stack = [root]
                verts: set[int] = set()
                degree_sum = 0
                while stack:
                    x = stack.pop()
                    if x in verts:
                        continue
                    verts.add(x)
                    seen.add(x)
                    degree_sum += len(adj[x])
                    stack.extend(y for y in adj[x] if y not in verts)
                edge_count = degree_sum // 2
                if edge_count == len(verts) and all(len(adj[x]) == 2 for x in verts):
                    closed.append(edge_count)
            return (
                all(x in (2, 3, 16) for x in closed)
                and closed.count(2) <= 1
                and closed.count(3) <= 1
                and closed.count(16) <= 1
            )

        def rec(used_ep: int, used_orbit: int) -> list[Edge] | None:
            self.nodes += 1
            if self.nodes > self.node_limit:
                return None
            if used_ep == full_ep:
                assert used_orbit == full_orbit
                edges = [self.rows[r].edge for r in chosen]
                self.solutions += 1
                if factor_cycle_lengths(edges) == [16, 3, 2]:
                    return edges
                return None

            best: list[int] | None = None
            # Algorithm X: branch on the least-populated uncovered endpoint
            # or unused orbit constraint.
            for ep in range(42):
                if used_ep >> ep & 1:
                    continue
                opts = [r for r in self.by_endpoint[ep] if active(r, used_ep, used_orbit)]
                if not opts:
                    return None
                if best is None or len(opts) < len(best):
                    best = opts
            for j in range(len(self.keys)):
                if used_orbit >> j & 1:
                    continue
                opts = [r for r in self.by_orbit[j] if active(r, used_ep, used_orbit)]
                if not opts:
                    return None
                if best is None or len(opts) < len(best):
                    best = opts
            assert best is not None
            self.rng.shuffle(best)
            for rid in best:
                row = self.rows[rid]
                if not partial_cycle_ok(row.edge):
                    continue
                chosen.append(rid)
                ans = rec(used_ep | row.mask, used_orbit | (1 << row.orbit))
                if ans is not None:
                    return ans
                chosen.pop()
            return None

        return rec(0, 0)


def random_f1(rng: random.Random) -> list[Edge] | None:
    remaining = [v for v in VERTICES if v not in (0, 10)]
    rng.shuffle(remaining)
    middle = remaining[:3]
    long = remaining[3:]
    cycles = [
        [(0, 0), (10, 1)],
        [(v, rng.randrange(2)) for v in middle],
        [(v, rng.randrange(2)) for v in long],
    ]
    edges = [e for cyc in cycles for e in cycle_edges(cyc)]
    assert factor_cycle_lengths(edges) == [16, 3, 2]
    keys = [orbit_key(e) for e in edges]
    if Counter(keys)[(10, 0, 0)] != 1 or Counter(keys)[(10, 1, 1)] != 1:
        return None
    regular = [k for k in keys if k in REGULAR_ORBITS]
    if len(regular) != 19 or len(set(regular)) != 19:
        return None
    return edges


def encode_factor(edges: list[Edge]) -> list[list[list[int]]]:
    return [[[u, a], [v, b]] for ((u, a), (v, b)) in sorted(edges)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026090402)
    ap.add_argument("--trials", type=int, default=100_000)
    ap.add_argument("--nodes-per-f1", type=int, default=200_000)
    ap.add_argument("--progress", type=int, default=1000)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    start = time.monotonic()
    admissible = 0
    total_nodes = 0
    for trial in range(1, args.trials + 1):
        f1 = random_f1(rng)
        if f1 is None:
            continue
        admissible += 1
        used = {orbit_key(e) for e in f1 if orbit_key(e) in REGULAR_ORBITS}
        complement = [key for key in REGULAR_ORBITS if key not in used]
        assert len(complement) == 21
        solver = ExactCover(complement, rng, args.nodes_per_f1)
        f3 = solver.solve()
        total_nodes += solver.nodes
        if f3 is not None:
            out = {
                "n": 21,
                "type": [16, 3, 2],
                "search": {
                    "seed": args.seed,
                    "trial": trial,
                    "admissible_f1": admissible,
                    "exact_cover_nodes": total_nodes,
                },
                "F1": encode_factor(f1),
                "F3": encode_factor(f3),
            }
            print(json.dumps(out, sort_keys=True, separators=(",", ":")))
            print(f"FOUND elapsed_seconds={time.monotonic()-start:.3f}")
            return
        if args.progress and admissible % args.progress == 0:
            print(
                f"progress trials={trial} admissible_f1={admissible} "
                f"exact_cover_nodes={total_nodes} elapsed_seconds={time.monotonic()-start:.3f}",
                flush=True,
            )
    print(
        f"NOT_FOUND trials={args.trials} admissible_f1={admissible} "
        f"exact_cover_nodes={total_nodes} elapsed_seconds={time.monotonic()-start:.3f}"
    )
    raise SystemExit(1)


if __name__ == "__main__":
    main()
