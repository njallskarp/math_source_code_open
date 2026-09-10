#!/usr/bin/env python3
"""Independent finite audit of graph contribution h4249; standard library only.

No imports or inputs from the author's implementation. Affine-coordinate
planes and integer-mask distance layers provide a different finite encoding.
The universal theorem is established by the written proof, not these cases.
"""
import hashlib
import json
from collections import Counter
from functools import cache
from itertools import combinations, product


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def mask_of(values):
    return sum(1 << x for x in set(values))


def closure(graph, mask):
    out = mask
    for v in bits(mask):
        out |= graph[v]
    return out


def plane(q):
    """Affine points (x,y), q slope points at infinity, vertical infinity.

    q=4 uses F_2[t]/(t^2+t+1), represented by two-bit integers.
    """
    check(q in (2, 3, 4, 5), "unsupported field")

    def add(a, b):
        return a ^ b if q == 4 else (a + b) % q

    def mul(a, b):
        if q != 4:
            return a * b % q
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & 4:
                a ^= 7
        return out

    check(all(len({mul(a, b) for b in range(q)}) == q
              for a in range(1, q)), "field multiplication")
    n = q*q + q + 1
    lines = []
    for slope in range(q):
        for intercept in range(q):
            lines.append(mask_of([q*x + add(mul(slope, x), intercept)
                                  for x in range(q)] + [q*q+slope]))
    for x in range(q):
        lines.append(mask_of([q*x+y for y in range(q)] + [q*q+q]))
    lines.append(mask_of(range(q*q, n)))
    graph = [0] * (2*n)
    for i, line in enumerate(lines):
        graph[n+i] = line
        for p in bits(line):
            graph[p] |= 1 << (n+i)
    check(len(lines) == n and all(m.bit_count() == q+1 for m in graph),
          "plane order or degree")
    for side in (range(n), range(n, 2*n)):
        check(all((graph[a] & graph[b]).bit_count() == 1
                  for a, b in combinations(side, 2)), "plane incidence axiom")
    return graph


def directions(graph):
    """All full responses, using Boolean wavefronts from each target.

    The previous distance layer intersected with N(probe) consists of all
    shortest first steps. A disconnected graph is an explicit error.
    """
    n = len(graph)
    full = (1 << n) - 1
    rows = [[0] * n for _ in graph]
    for target in range(n):
        layer = seen = 1 << target
        rows[target][target] = layer
        while seen != full:
            nxt = closure(graph, layer) & ~seen
            check(nxt != 0, "disconnected graph")
            for p in bits(nxt):
                rows[p][target] = graph[p] & layer
                check(rows[p][target] != 0, "empty response")
            seen |= nxt
            layer = nxt
    return rows


def partition(rows, pair, territory):
    out = {}
    a, b = pair
    for x in bits(territory):
        signature = (rows[a][x], rows[b][x])
        out[signature] = out.get(signature, 0) | (1 << x)
    return out


def carrier(graph, core):
    common = (1 << len(graph)) - 1
    for x in bits(core):
        common &= graph[x]
    check(common.bit_count() == 1, "core lacks unique carrier")
    return next(bits(common))


def action(graph, core):
    if core == 0:
        return 0, next(bits(graph[0]))
    z = carrier(graph, core)
    a = next(bits(core))
    return a, next(bits(graph[a] & ~(1 << z)))


def core_audit(q):
    graph = plane(q)
    rows = directions(graph)
    full = (1 << len(graph)) - 1
    edges = initial = cores = obligations = unresolved = 0
    for a in range(len(graph)):
        for b in bits(graph[a]):
            if a >= b:
                continue
            edges += 1
            parts = partition(rows, (a, b), full)
            check(Counter(p.bit_count() for p in parts.values())
                  == Counter({1: 2*(q+1), q: 2*q}), "initial exact histogram")
            for post in parts.values():
                if post.bit_count() > 1:
                    carrier(graph, post)
                    check(post.bit_count() == q, "wrong first core")
                    initial += 1
    for z, neighborhood in enumerate(graph):
        vertices = tuple(bits(neighborhood))
        for size in range(2, len(vertices)+1):
            for chosen in combinations(vertices, size):
                core = mask_of(chosen)
                cores += 1
                for a in chosen:
                    for b in bits(graph[a] & ~(1 << z)):
                        obligations += 1
                        parts = partition(rows, (a, b), closure(graph, core))
                        expected = Counter({1: q+2})
                        expected[size-1] += q+1
                        check(Counter(p.bit_count() for p in parts.values()) == expected,
                              "shrinking exact histogram")
                        for post in parts.values():
                            if post.bit_count() > 1:
                                carrier(graph, post)
                                check(post.bit_count() < size, "core did not shrink")
                                unresolved += 1
    return dict(q=q, vertices=len(graph), edges=edges, initial=initial,
                cores=cores, obligations=obligations, unresolved=unresolved)


def cartesian(factors):
    labels = list(product(*(range(len(g)) for g in factors)))
    lookup = {v: i for i, v in enumerate(labels)}
    graph = [0] * len(labels)
    for v, coords in enumerate(labels):
        for j, g in enumerate(factors):
            for w in bits(g[coords[j]]):
                other = coords[:j] + (w,) + coords[j+1:]
                graph[v] |= 1 << lookup[other]
    return graph, labels, lookup


def expand(base, scenario):
    modules, labels = [], []
    for v in range(len(base)):
        size = 1 if scenario == "singleton" else (
            2 if scenario == "independent2" else 1 + v % 4)
        modules.append(tuple(range(len(labels), len(labels)+size)))
        labels.extend([v] * size)
    graph = [0] * len(labels)
    for v, module in enumerate(modules):
        external = mask_of(x for w in bits(base[v]) for x in modules[w])
        for x in module:
            graph[x] = external
        if scenario == "mixed":
            # Includes singleton, independent, clique, path, and an edge
            # plus isolated vertices, varied independently of module size.
            kind = (v // 4) % 4
            for i, j in combinations(range(len(module)), 2):
                edge = kind == 1 or (kind == 2 and j == i+1) or (
                    kind == 3 and i == 0 and j == 1)
                if edge:
                    graph[module[i]] |= 1 << module[j]
                    graph[module[j]] |= 1 << module[i]
    return graph, modules, labels


def run_policy(orders, scenario):
    """Every response history in the *expanded product*, through final capture.

    The action depends only on the cop's memory (phase, core, known
    coordinates); territory is used to audit all adversarial responses.
    """
    factors = [plane(q) for q in orders]
    factor_rows = [directions(g) for g in factors]
    base, coordinates, index = cartesian(factors)
    graph, modules, module_of = expand(base, scenario)
    rows = directions(graph)
    bound = sum(orders) + (scenario != "singleton")
    branches = finishes = tracked = projections = 0

    def project(response):
        return mask_of(module_of[x] for x in bits(response))

    def decode(response, probe, j):
        p = coordinates[probe][j]
        values = {coordinates[v][j] for v in bits(response)
                  if coordinates[v][j] != p}
        return mask_of(values) if values else 1 << p

    @cache
    def visit(territory, phase, core, known, remaining):
        nonlocal branches, finishes, tracked, projections
        check(remaining > 0, "round bound exceeded")
        if phase == len(orders):
            w = index[known]
            pair = (w, next(bits(base[w])))
            finishes += 1
        else:
            active = action(factors[phase], core)
            pair = tuple(index[known + (a,) + (0,)*(len(orders)-phase-1)]
                         for a in active)
        probes = tuple(modules[v][0] for v in pair)
        check(graph[probes[0]] & (1 << probes[1]), "nonadjacent probes")
        worst = 1
        for signature, post in partition(rows, probes, territory).items():
            branches += 1
            if post.bit_count() == 1:
                continue
            check(phase < len(orders), "finishing round failed")
            check(all(module_of[x] not in pair for x in bits(post)), "guard failed")
            projected = tuple(project(r) for r in signature)
            # Verify quotient/factor response identities on EVERY surviving
            # actual target before using the decoded values for cop memory.
            decoded = [tuple(decode(projected[k], pair[k], j) for k in (0, 1))
                       for j in range(len(orders))]
            for x in bits(post):
                coords = coordinates[module_of[x]]
                for j in range(len(orders)):
                    for k in (0, 1):
                        check(decoded[j][k] == factor_rows[j][coordinates[pair[k]][j]][coords[j]],
                              "incorrect response projection")
                        projections += 1
            new_known = []
            for j, old in enumerate(known):
                possible = closure(factors[j], 1 << old)
                match = mask_of(x for x in bits(possible)
                                if factor_rows[j][old][x] == decoded[j][0])
                check(match.bit_count() == 1 and decoded[j][0] == decoded[j][1],
                      "tracked coordinate became ambiguous")
                new_known.append(next(bits(match)))
                tracked += 1
            domain = closure(factors[phase], core) if core else (
                (1 << len(factors[phase])) - 1)
            next_core = partition(factor_rows[phase], active, domain).get(decoded[phase], 0)
            check(next_core != 0, "impossible decoded history")
            if next_core.bit_count() > 1:
                carrier(factors[phase], next_core)
                limit = core.bit_count()-1 if core else orders[phase]
                check(next_core.bit_count() <= limit, "factor core bound failed")
                next_phase = phase
            else:
                new_known.append(next(bits(next_core)))
                next_phase = phase+1
                next_core = 0
            for x in bits(post):
                coords = coordinates[module_of[x]]
                check(coords[:next_phase] == tuple(new_known), "wrong known coordinates")
                if next_core:
                    check(next_core & (1 << coords[phase]), "target lost from core")
            worst = max(worst, 1 + visit(closure(graph, post), next_phase,
                                        next_core, tuple(new_known), remaining-1))
        return worst

    worst = visit((1 << len(graph))-1, 0, 0, (), bound)
    return dict(orders=orders, scenario=scenario, vertices=len(graph),
                states=visit.cache_info().currsize, branches=branches,
                finishing_states=finishes, tracked_updates=tracked,
                surviving_target_projection_checks=projections,
                worst_rounds=worst, bound=bound)


def main():
    result = {
        "cores": [core_audit(q) for q in (2, 3, 4, 5)],
        "policies": [run_policy(orders, scenario)
                     for orders in ([2], [3], [4], [2, 2], [2, 3])
                     for scenario in ("singleton", "independent2", "mixed")],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(json.dumps(result, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("PASS: complete expanded-product policy audit")


if __name__ == "__main__":
    main()
