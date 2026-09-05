#!/usr/bin/env python3
"""Exact audits for the local extremal-deletion cut family."""

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SURVIVOR = HERE / "HEIGHT2731_SURVIVOR.json"
SURVIVOR_SHA256 = "9fad7f23af43c461187bd4fae2f4ef740c94afb5a5cfef1a7f3c7737170a6051"
U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
EXPECTED_EXACT_SEVEN = (
    (20, 1, 19, 1), (20, 2, 18, 8),
    (21, 2, 19, 8), (21, 3, 18, 15),
    (22, 2, 20, 7), (22, 3, 19, 15), (22, 4, 18, 22),
    (23, 1, 22, 1), (23, 2, 21, 8), (23, 3, 20, 15),
    (23, 4, 19, 23), (23, 5, 18, 30),
    (24, 1, 23, 3), (24, 2, 22, 11), (24, 3, 21, 18),
    (24, 4, 20, 25), (24, 5, 19, 33), (24, 6, 18, 40),
)


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def exhaustive_edge_partition(max_order=6):
    graph_count = subset_count = 0
    for order in range(max_order + 1):
        pairs = tuple(combinations(range(order), 2))
        for graph_mask in range(1 << len(pairs)):
            graph_count += 1
            total = graph_mask.bit_count()
            for subset_mask in range(1 << order):
                subset_count += 1
                incident = remaining = 0
                for bit, (left, right) in enumerate(pairs):
                    if not graph_mask >> bit & 1:
                        continue
                    touches = bool(subset_mask >> left & 1 or subset_mask >> right & 1)
                    incident += touches
                    remaining += not touches
                require(incident + remaining == total, "edge partition identity")
    return graph_count, subset_count


def exact_seven_table():
    rows = []
    for order in range(18, 25):
        total = U[order] - 7
        for removed in range(1, order - 17):
            remaining = order - removed
            required = total - U[remaining]
            if required > 0:
                rows.append((order, removed, remaining, required))
    require(tuple(rows) == EXPECTED_EXACT_SEVEN, "exact-seven table")
    return rows


def scalar_cap_counterexamples():
    examples = ((20, 1), (21, 2), (22, 2), (23, 1), (24, 1))
    for order, removed_size in examples:
        total = U[order] - 7
        remaining = tuple(range(removed_size, order))
        edges = set(tuple(edge) for edge in list(combinations(remaining, 2))[:total])
        require(len(edges) == total, "fixture edge supply")
        removed = set(range(removed_size))
        incident = sum(left in removed or right in removed for left, right in edges)
        required = total - U[order - removed_size]
        require(total <= U[order] - 7 and incident < required, "strict scalar fixture")
    return len(examples)


def graph_from_document(document):
    record = document["record"]
    red = [set() for _ in range(43)]
    for bit, (left, right) in enumerate(combinations(range(7), 2)):
        if record["core_mask"] >> bit & 1:
            red[left].add(right)
            red[right].add(left)
    for central, mask in enumerate(document["central_labels"], 7):
        for exceptional in range(7):
            if mask >> exceptional & 1:
                red[central].add(exceptional)
                red[exceptional].add(central)
    for left, right in document["central_red_edges"]:
        left += 7
        right += 7
        red[left].add(right)
        red[right].add(left)
    return tuple(frozenset(row) for row in red)


def local_graph(red, root, color):
    universe = set(range(43)) - {root}
    vertices = red[root] if color else universe - red[root]
    adjacency = {}
    for vertex in vertices:
        adjacency[vertex] = (
            red[vertex] & vertices if color
            else vertices - {vertex} - red[vertex]
        )
    return tuple(sorted(vertices)), adjacency


def count_edges(vertices, adjacency):
    return sum(right in adjacency[left] for left, right in combinations(vertices, 2))


def audit_height2731():
    raw = SURVIVOR.read_bytes()
    require(sha256(raw).hexdigest() == SURVIVOR_SHA256, "height-2731 source hash")
    red = graph_from_document(json.loads(raw))
    require(tuple(map(len, red)) == (19, 19, 20, 20, 20, 20, 20) + (21,) * 36,
            "height-2731 degree sequence")
    tested = scalar_good_tested = violations = scalar_good_violations = 0
    minimum_slack = scalar_good_minimum = None
    scalar_good_sides = 0
    for root in range(43):
        for color in (True, False):
            vertices, adjacency = local_graph(red, root, color)
            order = len(vertices)
            total = count_edges(vertices, adjacency)
            scalar_good = total <= U[order] - 7
            scalar_good_sides += scalar_good
            for removed_size in range(1, order - 17):
                remaining_order = order - removed_size
                required = total - U[remaining_order]
                if required <= 0:
                    continue
                for removed_tuple in combinations(vertices, removed_size):
                    tested += 1
                    scalar_good_tested += scalar_good
                    removed = set(removed_tuple)
                    incident = sum(
                        right in adjacency[left] and (left in removed or right in removed)
                        for left, right in combinations(vertices, 2)
                    )
                    slack = incident - required
                    minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
                    if scalar_good:
                        scalar_good_minimum = (
                            slack if scalar_good_minimum is None else min(scalar_good_minimum, slack)
                        )
                    violations += slack < 0
                    scalar_good_violations += scalar_good and slack < 0
    result = (tested, scalar_good_tested, violations, scalar_good_violations,
              minimum_slack, scalar_good_minimum, scalar_good_sides)
    require(result == (247094, 197142, 0, 0, 0, 4, 54), "height-2731 cut audit")
    return result


def main():
    graphs, subsets = exhaustive_edge_partition()
    rows = exact_seven_table()
    fixtures = scalar_cap_counterexamples()
    tested, scalar_tested, _, _, slack, scalar_slack, sides = audit_height2731()
    print(f"PASS deletion identity on {graphs} labeled graphs and {subsets} graph/subset pairs")
    print(f"PASS {len(rows)} positive exact-deficiency-seven rows for local orders 18..24")
    print(f"PASS {fixtures} scalar-cap fixtures violate a deletion cut")
    print(f"PASS height-2731 witness satisfies {tested} known-range cuts; minimum slack {slack}")
    print(f"PASS {sides} scalar-good root-colors satisfy {scalar_tested} cuts; minimum slack {scalar_slack}")
    print("SCOPE transferable valid inequalities; they do not exclude the height-2731 survivor")


if __name__ == "__main__":
    main()
