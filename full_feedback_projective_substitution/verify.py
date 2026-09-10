#!/usr/bin/env python3
"""Exact definition-level audits of adjacent probes, products, and substitution.

Standard library only. The universal claims are proved in THEOREM.md.
"""
import hashlib
import json
from collections import deque
from functools import lru_cache
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise ValueError(message)


def plane(q):
    require(q in (2, 3, 5), "this generator is only used over the listed prime fields")
    vectors = [v for v in product(range(q), repeat=3)
               if any(v) and next(x for x in v if x) == 1]
    size = len(vectors)
    require(size == q*q + q + 1, "wrong projective normalization")
    adj = [set() for _ in range(2*size)]
    for i, point in enumerate(vectors):
        for j, line in enumerate(vectors):
            if sum(a*b for a, b in zip(point, line)) % q == 0:
                adj[i].add(size+j)
                adj[size+j].add(i)
    require(all(len(a) == q+1 for a in adj), "wrong incidence degree")
    for side in (range(size), range(size, 2*size)):
        for u, v in combinations(side, 2):
            require(len(adj[u] & adj[v]) == 1, "projective-plane axiom failed")
    return adj


def responses(adj):
    n = len(adj)
    distances = []
    for p in range(n):
        d = [None]*n
        d[p] = 0
        todo = deque([p])
        while todo:
            u = todo.popleft()
            for v in adj[u]:
                if d[v] is None:
                    d[v] = d[u]+1
                    todo.append(v)
        require(None not in d, "disconnected input")
        distances.append(d)
    return [[frozenset([p]) if p == x else
             frozenset(w for w in adj[p] if distances[w][x]+1 == distances[p][x])
             for x in range(n)] for p in range(n)]


def closed(adj, vertices):
    return frozenset(set(vertices).union(*(adj[v] for v in vertices)))


def classes(rows, probes, territory):
    result = {}
    for v in territory:
        signature = tuple(rows[p][v] for p in probes)
        result.setdefault(signature, set()).add(v)
    return result


def carrier(adj, core):
    common = set(range(len(adj)))
    for v in core:
        common &= adj[v]
    require(len(common) == 1, "nonsingleton core has no unique carrier")
    return next(iter(common))


def action(adj, core):
    if core is None:
        return (0, min(adj[0]))
    z = carrier(adj, core)
    a = min(core)
    return (a, min(adj[a]-{z}))


def update(adj, rows, q, core, probes, signature):
    territory = range(len(adj)) if core is None else closed(adj, core)
    posterior = frozenset(v for v in territory
                          if tuple(rows[p][v] for p in probes) == signature)
    require(posterior, "impossible projected response")
    if len(posterior) > 1:
        carrier(adj, posterior)
        require(len(posterior) <= (q if core is None else len(core)-1),
                "core failed to shrink")
    return posterior


def audit_cores(q):
    adj = plane(q)
    rows = responses(adj)
    initial_actions = initial_children = 0
    for a in range(len(adj)):
        for b in adj[a]:
            if a > b:
                continue
            initial_actions += 1
            for post in classes(rows, (a, b), range(len(adj))).values():
                if len(post) > 1:
                    require(len(post) <= q, "initial core too large")
                    carrier(adj, post)
                    initial_children += 1
    cores = obligations = children = 0
    for z in range(len(adj)):
        neighbors = sorted(adj[z])
        for size in range(2, len(neighbors)+1):
            for selected in combinations(neighbors, size):
                core = frozenset(selected)
                territory = closed(adj, core)
                cores += 1
                for a in core:
                    for b in adj[a]-{z}:
                        obligations += 1
                        for post in classes(rows, (a, b), territory).values():
                            if len(post) > 1:
                                require(len(post) < size, "nonshrinking response class")
                                carrier(adj, post)
                                children += 1
    return {"q": q, "vertices": len(adj), "initial_edges": initial_actions,
            "initial_unresolved_classes": initial_children, "cores": cores,
            "shrink_obligations": obligations, "unresolved_children": children}


def cartesian(factors):
    vertices = list(product(*(range(len(a)) for a in factors)))
    lookup = {v: i for i, v in enumerate(vertices)}
    adj = [set() for _ in vertices]
    for index, v in enumerate(vertices):
        for coordinate, factor in enumerate(factors):
            for w in factor[v[coordinate]]:
                neighbor = list(v)
                neighbor[coordinate] = w
                adj[index].add(lookup[tuple(neighbor)])
    return adj, vertices, lookup


def decode_coordinate(response, probe, coordinate, vertices):
    p = vertices[probe]
    result = {vertices[x][coordinate] for x in response
              if vertices[x][coordinate] != p[coordinate]}
    return frozenset(result or {p[coordinate]})


def audit_product(orders):
    factors = [plane(q) for q in orders]
    factor_rows = [responses(adj) for adj in factors]
    adj, vertices, lookup = cartesian(factors)
    rows = responses(adj)
    identities = 0
    for p in range(len(adj)):
        for x in range(len(adj)):
            for j in range(len(factors)):
                require(decode_coordinate(rows[p][x], p, j, vertices)
                        == factor_rows[j][vertices[p][j]][vertices[x][j]],
                        "product response projection failed")
                identities += 1
    branches = 0

    @lru_cache(None)
    def visit(territory, phase, known, core, budget):
        nonlocal branches
        require(budget > 0 and phase < len(factors), "product strategy exceeded bound")
        active_pair = action(factors[phase], core)
        positions = []
        for active in active_pair:
            p = list(known) + [active] + [0]*(len(factors)-phase-1)
            positions.append(lookup[tuple(p)])
        require(positions[1] in adj[positions[0]], "product probes are not adjacent")
        worst = 1
        for signature, post in classes(rows, positions, territory).items():
            branches += 1
            if len(post) <= 1:
                continue
            decoded = [tuple(decode_coordinate(signature[k], positions[k], j, vertices)
                             for k in range(2)) for j in range(len(factors))]
            new_known = []
            for j in range(phase):
                possible = [x for x in factors[j][known[j]] | {known[j]}
                            if factor_rows[j][known[j]][x] == decoded[j][0]]
                require(len(possible) == 1, "previously located coordinate was lost")
                require(decoded[j][0] == decoded[j][1], "fixed-coordinate probes disagree")
                new_known.append(possible[0])
            active_core = update(factors[phase], factor_rows[phase], orders[phase],
                                 core, active_pair, decoded[phase])
            new_phase = phase
            if len(active_core) == 1:
                new_known.append(next(iter(active_core)))
                new_phase += 1
                active_core = None
            require(new_phase < len(factors), "all coordinates known but target ambiguous")
            for v in post:
                require(vertices[v][:new_phase] == tuple(new_known), "wrong tracked coordinate")
                if new_phase == phase:
                    require(vertices[v][phase] in active_core, "invalid active-coordinate history")
            depth = visit(closed(adj, post), new_phase, tuple(new_known), active_core, budget-1)
            worst = max(worst, 1+depth)
        return worst

    rounds = visit(frozenset(range(len(adj))), 0, (), None, sum(orders))
    return {"orders": orders, "vertices": len(adj), "projection_identities": identities,
            "policy_states": visit.cache_info().currsize, "response_branches": branches,
            "worst_rounds": rounds, "proved_round_bound": sum(orders)}


def substitute(base, sizes, kinds):
    modules, labels = [], []
    for v, size in enumerate(sizes):
        modules.append(tuple(range(len(labels), len(labels)+size)))
        labels.extend([v]*size)
    adj = [set() for _ in labels]
    for v, module in enumerate(modules):
        for a, b in combinations(module, 2):
            if kinds[v] == "clique" or (kinds[v] == "path" and b == a+1):
                adj[a].add(b)
                adj[b].add(a)
        for w in base[v]:
            for a in module:
                adj[a].update(modules[w])
    return adj, modules, labels


def audit_substitution(q, scenario):
    base = plane(q)
    n = len(base)
    if scenario == 0:
        sizes, kinds = [2]*n, ["empty"]*n
    elif scenario == 1:
        sizes, kinds = [3]*n, ["clique"]*n
    else:
        sizes = [1+(v+scenario)%3 for v in range(n)]
        kinds = [("empty", "path", "clique")[(v+2*scenario)%3] for v in range(n)]
    adj, modules, labels = substitute(base, sizes, kinds)
    rows, base_rows = responses(adj), responses(base)
    branches = 0

    @lru_cache(None)
    def visit(territory, core, finish, budget):
        nonlocal branches
        require(budget > 0, "substitution strategy exceeded bound")
        quotient_pair = (finish, min(base[finish])) if finish is not None else action(base, core)
        probes = tuple(modules[v][0] for v in quotient_pair)
        require(probes[1] in adj[probes[0]], "lifted probes are not adjacent")
        worst = 1
        for signature, post in classes(rows, probes, territory).items():
            branches += 1
            if len(post) <= 1:
                continue
            require(finish is None, "known-module finishing pair failed")
            require(not any(labels[v] in quotient_pair for v in post), "module guard failed")
            projected = tuple(frozenset(labels[v] for v in response) for response in signature)
            next_core = update(base, base_rows, q, core, quotient_pair, projected)
            require({labels[v] for v in post} <= next_core, "invalid projected history")
            next_finish = next(iter(next_core)) if len(next_core) == 1 else None
            if next_finish is not None:
                next_core = None
            depth = visit(closed(adj, post), next_core, next_finish, budget-1)
            worst = max(worst, 1+depth)
        return worst

    rounds = visit(frozenset(range(len(adj))), None, None, q+1)
    return {"q": q, "scenario": scenario, "vertices": len(adj),
            "policy_states": visit.cache_info().currsize, "response_branches": branches,
            "worst_rounds": rounds, "proved_round_bound": q+1}


def main():
    result = {"core_audits": [audit_cores(q) for q in (2, 3, 5)],
              "product_audit": audit_product([2, 2]),
              "substitution_audits": [audit_substitution(q, scenario)
                                      for q in (2, 3) for scenario in range(4)]}
    compact = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(json.dumps(result, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(compact.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
