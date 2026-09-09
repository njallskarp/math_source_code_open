#!/usr/bin/env python3
"""Check finite strategy certificates directly; Python standard library only."""
import copy
import hashlib
import json
from collections import deque
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def graph(n, edges):
    require(type(n) is int and n >= 2, "invalid order")
    adj = [set() for _ in range(n)]
    for u, v in edges:
        require(type(u) is int and type(v) is int and 0 <= u < v < n,
                "edges must have ordered, distinct endpoints")
        require(v not in adj[u], "duplicate edge")
        adj[u].add(v)
        adj[v].add(u)
    seen = {0}
    todo = [0]
    for u in todo:
        for v in adj[u] - seen:
            seen.add(v)
            todo.append(v)
    require(len(seen) == n, "disconnected graph")
    return adj


def add_twins(adj, vertex, count):
    result = [s.copy() for s in adj] + [adj[vertex].copy() for _ in range(count)]
    for v in adj[vertex]:
        result[v].update(range(len(adj), len(result)))
    return result


def responses(adj):
    n = len(adj)
    distances = []
    for start in range(n):
        d = [None] * n
        d[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if d[v] is None:
                    d[v] = d[u] + 1
                    queue.append(v)
        require(None not in d, "disconnected response input")
        distances.append(d)
    result = []
    for probe in range(n):
        result.append([
            frozenset([probe]) if x == probe else
            frozenset(v for v in adj[probe]
                      if distances[v][x] + 1 == distances[probe][x])
            for x in range(n)
        ])
    return result


def partition(row):
    classes = {}
    for x, response in enumerate(row):
        classes.setdefault(response, set()).add(x)
    return list(classes.values())


def decode(mask, n):
    require(type(mask) is int and 0 < mask < 1 << n, "invalid territory mask")
    return {v for v in range(n) if mask & (1 << v)}


def encode(s):
    return sum(1 << v for v in s)


def closed(adj, s):
    return s.union(*(adj[v] for v in s))


def check_strategy(adj, records):
    n = len(adj)
    table = {}
    for record in records:
        mask, rank, probe = record
        require(mask not in table, "duplicate strategy state")
        decode(mask, n)
        require(type(rank) is int and rank >= 1, "invalid rank")
        require(type(probe) is int and 0 <= probe < n, "invalid probe")
        table[mask] = (rank, probe)
    require((1 << n) - 1 in table, "missing initial state")
    parts = [partition(row) for row in responses(adj)]
    branches = 0
    for mask, (rank, probe) in table.items():
        territory = decode(mask, n)
        for c in parts[probe]:
            posterior = territory & c
            if len(posterior) <= 1:
                continue
            child = encode(closed(adj, posterior))
            require(child in table, "missing strategy child")
            require(table[child][0] < rank, "strategy rank did not decrease")
            branches += 1
    return {"states": len(table), "unresolved_branches": branches,
            "round_bound": table[(1 << n) - 1][0]}


def check_evasion(adj, masks):
    require(len(masks) > 0 and len(masks) == len(set(masks)), "invalid evasion family")
    family = [decode(mask, len(adj)) for mask in masks]
    require(all(len(s) >= 2 for s in family), "singleton evasion state")
    parts = [partition(row) for row in responses(adj)]
    # The initial territory is all vertices, so it contains every family member.
    obligations = 0
    for territory in family:
        for probe in range(len(adj)):
            good = False
            for c in parts[probe]:
                posterior = territory & c
                if len(posterior) >= 2:
                    child = closed(adj, posterior)
                    if any(t <= child for t in family):
                        good = True
                        break
            require(good, "evasion family is not closed under probe " + str(probe))
            obligations += 1
    return {"states": len(family), "response_obligations": obligations}


def check_pair(adj, probes):
    require(len(probes) == 2 and len(set(probes)) == 2, "invalid resolving pair")
    require(all(type(p) is int and 0 <= p < len(adj) for p in probes), "invalid probe")
    rows = responses(adj)
    signatures = {tuple(rows[p][x] for p in probes) for x in range(len(adj))}
    require(len(signatures) == len(adj), "pair does not resolve every location")


def check_coarsening(old, new, old_twins):
    old_rows, new_rows = responses(old), responses(new)
    representative = min(old_twins)
    for p in range(len(new)):
        virtual = p if p < len(old) else representative
        for x, y in combinations(range(len(old)), 2):
            if old_rows[virtual][x] == old_rows[virtual][y]:
                require(new_rows[p][x] == new_rows[p][y], "old response class was split")


def check_certificate(data):
    base = graph(data["n"], data["edges"])
    require(len(base) == 12 and all(len(a) == 3 for a in base), "base must be cubic of order 12")
    vertex = data["duplicated_vertex"]
    require(vertex == 5 and base[vertex] == {0, 2, 4}, "wrong designated vertex")
    enlarged = add_twins(base, vertex, 1)
    upper = check_strategy(base, data["base_strategy"])
    lower = check_evasion(enlarged, data["evasion_family"])
    check_pair(enlarged, data["two_probe_resolver"])
    require(set(data["two_probe_resolver"]) == {2, 7}, "wrong displayed resolving pair")
    # Boundary audits of the universal replication argument, not an infinite proof.
    family_orders = []
    for multiplicity in range(2, 9):
        expanded = add_twins(base, vertex, multiplicity - 1)
        check_pair(expanded, data["two_probe_resolver"])
        check_coarsening(enlarged, expanded, {5, 12})
        family_orders.append(len(expanded))
    return {"base_one_probe": upper, "extension_one_probe_evasion": lower,
            "extension_two_probe_rounds": 1, "replication_audit_orders": family_orders}


def small_coarsening_audit():
    count = 0
    for n in range(2, 5):
        possible = list(combinations(range(n), 2))
        for bits in range(1 << len(possible)):
            edges = [e for i, e in enumerate(possible) if bits & (1 << i)]
            try:
                base = graph(n, edges)
            except InvalidCertificate:
                continue
            for v in range(n):
                old = add_twins(base, v, 1)
                new = add_twins(base, v, 2)
                check_coarsening(old, new, {v, n})
                count += 1
    return count


def main():
    data = json.loads((HERE / "certificate.json").read_text())
    result = check_certificate(data)
    result["small_replication_instances"] = small_coarsening_audit()
    mutations = []
    bad = copy.deepcopy(data)
    bad["base_strategy"][0][1] = 1
    mutations.append(bad)
    bad = copy.deepcopy(data)
    bad["evasion_family"] = [3]
    mutations.append(bad)
    bad = copy.deepcopy(data)
    bad["two_probe_resolver"] = [0, 1]
    mutations.append(bad)
    for bad in mutations:
        try:
            check_certificate(bad)
        except InvalidCertificate:
            continue
        raise InvalidCertificate("corrupted certificate accepted")
    result["rejected_corruptions"] = len(mutations)
    compact = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(json.dumps(result, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(compact.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
