"""Check the proposed strategy against full responses in actual expanded graphs."""

from collections import defaultdict, deque
from functools import lru_cache
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bits(mask):
    while mask:
        bit = mask & -mask
        mask -= bit
        yield bit.bit_length() - 1


def first_steps(adj, source):
    n = len(adj)
    d = [-1] * n
    d[source] = 0
    labels = [0] * n
    labels[source] = 1 << source
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                queue.append(v)
            if d[v] == d[u] + 1:
                labels[v] |= (1 << v) if u == source else labels[u]
    require(all(x >= 0 for x in d), "disconnected")
    return labels


def run(name, policy):
    n = 126
    qa = [set() for _ in range(n)]
    for a, b in policy["edges"]:
        qa[a].add(b)
        qa[b].add(a)
    erows = [first_steps(qa, p) for p in range(n)]
    for p in range(n):
        erows[p][p] = sum(1 << v for v in qa[p])
    fibres = []
    owner = []
    internal = []
    for v in range(n):
        if name == "singletons":
            m, kind = 1, "empty"
        elif name == "independent_pairs":
            m, kind = 2, "empty"
        elif name == "clique_triples":
            m, kind = 3, "clique"
        elif name == "paths_four":
            m, kind = 4, "path"
        elif name == "stars_four":
            m, kind = 4, "star_leaf_probe"
        elif name == "cubes_three":
            m, kind = 8, "cube"
        elif name == "mixed":
            m, kind = (
                1 + v % 5,
                ("empty", "clique", "disconnected", "path", "cycle")[v % 5],
            )
        else:
            raise ValueError("unknown scenario")
        fibre = list(range(len(owner), len(owner) + m))
        fibres.append(fibre)
        owner.extend([v] * m)
        es = []
        for a in range(m):
            for b in range(a + 1, m):
                yes = (
                    kind == "clique"
                    or kind == "path"
                    and b == a + 1
                    or kind == "star_leaf_probe"
                    and (a == 1 or a == 0 and b == 1)
                    or kind == "cycle"
                    and (b == a + 1 or a == 0 and b == m - 1)
                    or kind == "disconnected"
                    and a == 0
                    and b == 1
                    or kind == "cube"
                    and (a ^ b).bit_count() == 1
                )
                if yes:
                    es.append((fibre[a], fibre[b]))
        internal.extend(es)
    size = len(owner)
    adj = [set() for _ in range(size)]
    for a, b in internal:
        adj[a].add(b)
        adj[b].add(a)
    for p, q in policy["edges"]:
        for a in fibres[p]:
            for b in fibres[q]:
                adj[a].add(b)
                adj[b].add(a)
    fmask = [sum(1 << x for x in f) for f in fibres]
    reps = [f[0] for f in fibres]

    @lru_cache(None)
    def actual(p):
        return first_steps(adj, p)

    @lru_cache(None)
    def project(mask):
        return sum(1 << v for v in {owner[x] for x in bits(mask)})

    @lru_cache(None)
    def spread(mask):
        ans = mask
        for x in bits(mask):
            for y in adj[x]:
                ans |= 1 << y
        return ans

    def classes(territory, probes):
        rows = [actual(reps[p]) for p in probes]
        out = defaultdict(int)
        for x in bits(territory):
            out[tuple(row[x] for row in rows)] |= 1 << x
        return out

    finishing = set()
    finish_branches = 0

    def finish(territory, w):
        nonlocal finish_branches
        key = (territory, w)
        if key in finishing:
            return
        v = min(qa[w])
        parts = classes(territory, (w, v))
        require(
            all(post.bit_count() == 1 for post in parts.values()),
            "finishing pair failed",
        )
        finishing.add(key)
        finish_branches += len(parts)

    policy_rows = {(s, d): (p, q) for s, d, p, q in policy["nodes"]}
    pending = [((1 << size) - 1, (1 << n) - 1, policy["depth"])]
    seen = set()
    branches = 0
    singles = 0
    known_internal = 0
    known_virtual = 0
    worst = 0
    while pending:
        territory, virtual, rank = pending.pop()
        key = (territory, virtual, rank)
        if key in seen:
            continue
        seen.add(key)
        require((virtual, rank) in policy_rows, "missing virtual node")
        probes = policy_rows[(virtual, rank)]
        round_number = policy["depth"] + 1 - rank
        for signals, post in classes(territory, probes).items():
            branches += 1
            if post.bit_count() == 1:
                singles += 1
                worst = max(worst, round_number)
                continue
            known = {p for p, signal in zip(probes, signals) if signal & fmask[p]}
            if known:
                require(len(known) == 1, "inconsistent internal module identities")
                w = next(iter(known))
                require(post & ~fmask[w] == 0, "internal label misidentifies module")
                finish(spread(post), w)
                known_internal += 1
                worst = max(worst, round_number + 1)
                continue
            projected = tuple(project(s) for s in signals)
            vp = {
                x
                for x in bits(virtual)
                if tuple(erows[p][x] for p in probes) == projected
            }
            require(
                vp and {owner[x] for x in bits(post)} <= vp,
                "actual response not a virtual response",
            )
            if len(vp) == 1:
                finish(spread(post), next(iter(vp)))
                known_virtual += 1
                worst = max(worst, round_number + 1)
                continue
            require(rank > 1, "virtual rank exhausted")
            child = set(vp)
            for x in vp:
                child.update(qa[x])
            vm = sum(1 << x for x in child)
            next_actual = spread(post)
            require(
                {owner[x] for x in bits(next_actual)} <= child, "illegal simulated move"
            )
            pending.append((next_actual, vm, rank - 1))
    identities = 0
    internal_cases = 0
    for p in range(n):
        row = actual(reps[p])
        for x in range(size):
            if row[x] & fmask[p]:
                require(owner[x] == p, "external target returns internal label")
                internal_cases += 1
            else:
                require(
                    project(row[x]) == erows[p][owner[x]], "projection identity failed"
                )
                identities += 1
    require(worst <= policy["depth"] + 1, "round bound failed")
    return {
        "scenario": name,
        "vertices": size,
        "policy_states": len(seen),
        "response_branches": branches,
        "singleton_branches": singles,
        "module_identifications_internal": known_internal,
        "module_identifications_virtual": known_virtual,
        "finishing_states": len(finishing),
        "finishing_singletons": finish_branches,
        "projection_identities": identities,
        "internal_label_cases": internal_cases,
        "worst_rounds": worst,
    }


def small_graph_interfaces():
    """All connected labeled quotients of orders 2--4; four module assignments."""
    quotients = instances = projections = internal_hits = finishing_actions = 0
    shapes = [(1, []), (2, []), (4, [(0, 1), (1, 2), (1, 3)]), (3, [(0, 1)])]
    for order in range(2, 5):
        possible = list(combinations(range(order), 2))
        for edge_mask in range(1 << len(possible)):
            qa = [set() for _ in range(order)]
            edges = []
            for i, (a, b) in enumerate(possible):
                if edge_mask >> i & 1:
                    qa[a].add(b)
                    qa[b].add(a)
                    edges.append((a, b))
            seen = {0}
            todo = [0]
            while todo:
                u = todo.pop()
                for v in qa[u] - seen:
                    seen.add(v)
                    todo.append(v)
            if len(seen) != order:
                continue
            quotients += 1
            erows = [first_steps(qa, p) for p in range(order)]
            for p in range(order):
                erows[p][p] = sum(1 << x for x in qa[p])
            for offset in range(len(shapes)):
                fibres = []
                owner = []
                internal = []
                for p in range(order):
                    m, es = shapes[(p + offset) % len(shapes)]
                    fibre = list(range(len(owner), len(owner) + m))
                    fibres.append(fibre)
                    owner.extend([p] * m)
                    internal.extend((fibre[a], fibre[b]) for a, b in es)
                adj = [set() for _ in owner]
                for a, b in internal:
                    adj[a].add(b)
                    adj[b].add(a)
                for p, q in edges:
                    for a in fibres[p]:
                        for b in fibres[q]:
                            adj[a].add(b)
                            adj[b].add(a)
                fm = [sum(1 << x for x in f) for f in fibres]
                rows = [first_steps(adj, a) for a in range(len(owner))]
                for a in range(len(owner)):
                    p = owner[a]
                    for x, signal in enumerate(rows[a]):
                        if signal & fm[p]:
                            require(owner[x] == p, "small graph internal-label failure")
                            internal_hits += 1
                        else:
                            projected = sum(
                                1 << v for v in {owner[y] for y in bits(signal)}
                            )
                            require(
                                projected == erows[p][owner[x]],
                                "small graph projection failure",
                            )
                            projections += 1
                for p in range(order):
                    territory = set(fibres[p])
                    for q in qa[p]:
                        territory.update(fibres[q])
                    for q in qa[p]:
                        for a in fibres[p]:
                            for b in fibres[q]:
                                require(
                                    len({(rows[a][x], rows[b][x]) for x in territory})
                                    == len(territory),
                                    "small graph finishing failure",
                                )
                                finishing_actions += 1
                instances += 1
    require(quotients == 43 and instances == 172, "incomplete small-graph census")
    return {
        "connected_labeled_quotients": quotients,
        "module_assignments": instances,
        "projection_identities": projections,
        "internal_label_cases": internal_hits,
        "finishing_actions": finishing_actions,
    }
