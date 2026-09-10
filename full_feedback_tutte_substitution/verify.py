"""Verify the weakened-feedback policy and actual substitution interfaces."""

import json
from collections import Counter, defaultdict, deque
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORDER = 126
LCF = (17, 27, -13, -59, -35, 35, -11, 13, -53, 53, -27, 21, 57, 11, -21, -57, 59, -17)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph():
    edges = {tuple(sorted((v, (v + 1) % ORDER))) for v in range(ORDER)}
    edges.update(
        tuple(sorted((v, (v + LCF[v % len(LCF)]) % ORDER))) for v in range(ORDER)
    )
    adjacency = [set() for _ in range(ORDER)]
    for u, v in edges:
        require(u != v, "loop")
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(
        len(edges) == 189 and all(len(a) == 3 for a in adjacency),
        "wrong size or degree",
    )
    return adjacency, sorted(edges)


def distances(adjacency, source, omitted_edge=None):
    row = {source: 0}
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for w in adjacency[v]:
            if omitted_edge is not None and tuple(sorted((v, w))) == omitted_edge:
                continue
            if w not in row:
                row[w] = row[v] + 1
                queue.append(w)
    return row


def modified_responses(adjacency, distance):
    # Only this virtual game replaces the self response by the open neighborhood.
    # The expanded-graph audit uses the genuine self response {p}.
    return [
        [
            frozenset(adjacency[p])
            if p == x
            else frozenset(
                w for w in adjacency[p] if distance[w][x] + 1 == distance[p][x]
            )
            for x in range(ORDER)
        ]
        for p in range(ORDER)
    ]


def verify_policy(data, adjacency, distance, responses):
    require(
        set(data) == {"depth", "nodes"} and data["depth"] == 4,
        "wrong policy format or depth",
    )
    policy = {}
    for row in data["nodes"]:
        require(
            isinstance(row, list)
            and len(row) == 4
            and all(type(x) is int for x in row),
            "bad policy row",
        )
        mask, rank, p, q = row
        require(0 < mask < (1 << ORDER) and 1 <= rank <= 4, "bad territory/rank")
        require(
            0 <= p < ORDER and 0 <= q < ORDER and distance[p][q] == 2,
            "probes must be at distance two",
        )
        require((mask, rank) not in policy, "duplicate row")
        policy[(mask, rank)] = (p, q)
    root = ((1 << ORDER) - 1, data["depth"])
    pending = [root]
    seen = set()
    ranks = Counter()
    unresolved = singletons = 0
    while pending:
        key = pending.pop()
        if key in seen:
            continue
        seen.add(key)
        require(key in policy, "missing reachable row")
        mask, rank = key
        p, q = policy[key]
        ranks[rank] += 1
        classes = defaultdict(set)
        for x in range(ORDER):
            if (mask >> x) & 1:
                classes[(responses[p][x], responses[q][x])].add(x)
        for posterior in classes.values():
            if len(posterior) == 1:
                singletons += 1
                continue
            require(rank > 1, "unresolved terminal response")
            territory = set(posterior)
            for x in posterior:
                territory.update(adjacency[x])
            child = (sum(1 << x for x in territory), rank - 1)
            require(child in policy, "missing exact response child")
            pending.append(child)
            unresolved += 1
    require(seen == set(policy), "unreachable certificate row")
    return {
        "depth": data["depth"],
        "policy_nodes": len(policy),
        "nodes_by_rank": dict(sorted(ranks.items())),
        "unresolved_branches": unresolved,
        "singleton_branches": singletons,
        "initial_probes": list(policy[root]),
    }


def check_distance_two_partitions(adjacency, distance, modified):
    # Independently test the geometric lemma on every distance-two action.
    ordinary = [row[:] for row in modified]
    for p in range(ORDER):
        ordinary[p][p] = frozenset([p])

    def partition(p, q, table):
        groups = defaultdict(set)
        for x in range(ORDER):
            groups[(table[p][x], table[q][x])].add(x)
        return frozenset(frozenset(c) for c in groups.values())

    actions = 0
    for p in range(ORDER):
        for q in range(p + 1, ORDER):
            if distance[p][q] == 2:
                require(
                    partition(p, q, ordinary) == partition(p, q, modified),
                    "distance-two partition lemma failed",
                )
                actions += 1
    require(actions == 378, "incomplete distance-two action census")
    return actions


def reject_mutations(data, adjacency, distance, responses):
    mutations = []
    missing = json.loads(json.dumps(data))
    missing["nodes"].pop(0)
    mutations.append(missing)
    wrong_rank = json.loads(json.dumps(data))
    for row in wrong_rank["nodes"]:
        if row[1] == 4:
            row[1] = 1
    mutations.append(wrong_rank)
    wrong_probe = json.loads(json.dumps(data))
    wrong_probe["nodes"][0][3] = wrong_probe["nodes"][0][2]
    mutations.append(wrong_probe)
    for mutation in mutations:
        try:
            verify_policy(mutation, adjacency, distance, responses)
        except ValueError:
            pass
        else:
            raise ValueError("corrupted policy accepted")
    return len(mutations)


def main():
    import audit_expansion

    adjacency, edges = graph()
    distance = [distances(adjacency, v) for v in range(ORDER)]
    require(all(len(row) == ORDER for row in distance), "disconnected graph")
    require(
        all(
            Counter(row.values())
            == Counter({0: 1, 1: 3, 2: 6, 3: 12, 4: 24, 5: 48, 6: 32})
            for row in distance
        ),
        "unexpected distance layers",
    )
    require(
        all((distance[0][u] - distance[0][v]) % 2 for u, v in edges), "not bipartite"
    )
    require(
        min(distances(adjacency, u, (u, v))[v] + 1 for u, v in edges) == 12,
        "wrong girth",
    )
    responses = modified_responses(adjacency, distance)
    policy_bytes = (ROOT / "policy.json").read_bytes()
    data = json.loads(policy_bytes)
    enriched = dict(data, edges=edges)
    result = {
        "graph": {
            "order": ORDER,
            "size": len(edges),
            "degree": 3,
            "girth": 12,
            "diameter": 6,
            "bipartite": True,
        },
        "modified_policy": verify_policy(data, adjacency, distance, responses),
        "distance_two_partition_actions": check_distance_two_partitions(
            adjacency, distance, responses
        ),
        "rejected_policy_mutations": reject_mutations(
            data, adjacency, distance, responses
        ),
        "actual_substitutions": [
            audit_expansion.run(name, enriched)
            for name in (
                "singletons",
                "independent_pairs",
                "clique_triples",
                "paths_four",
                "stars_four",
                "cubes_three",
                "mixed",
            )
        ],
        "small_graph_interfaces": audit_expansion.small_graph_interfaces(),
        "policy_sha256": sha256(policy_bytes).hexdigest(),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("result_sha256=" + sha256(canonical).hexdigest())
    print(
        "VERIFIED: quotient policy and actual substitution interfaces"
    )


if __name__ == "__main__":
    main()
