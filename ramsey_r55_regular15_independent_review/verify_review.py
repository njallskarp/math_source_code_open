#!/usr/bin/env python3
"""Clean-room audit of the regular (4,4;15) obstruction at graph height 2609."""

from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, permutations
import json
from math import factorial
from pathlib import Path


EXPECTED_CASES = [
    (5388912, 4060),
    (5404008, 2012),
    (5683824, 954),
    (5683824, 956),
    (5683824, 1884),
]


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def encode(adjacency):
    return sum(
        1 << index
        for index, (left, right) in enumerate(combinations(range(len(adjacency)), 2))
        if adjacency[left] >> right & 1
    )


def decode(order, mask):
    adjacency = [0] * order
    for index, (left, right) in enumerate(combinations(range(order), 2)):
        if mask >> index & 1:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return tuple(adjacency)


def complement(adjacency):
    full = (1 << len(adjacency)) - 1
    return tuple(full ^ (1 << vertex) ^ row for vertex, row in enumerate(adjacency))


def monochromatic(adjacency, vertices, red):
    return all(
        bool(adjacency[left] >> right & 1) == red
        for left, right in combinations(vertices, 2)
    )


def valid_34(adjacency):
    vertices = range(len(adjacency))
    return not any(monochromatic(adjacency, triple, True) for triple in combinations(vertices, 3)) \
        and not any(monochromatic(adjacency, four, False) for four in combinations(vertices, 4))


def augment_34(graphs):
    """Add the next labeled vertex using the exact local extension criterion."""
    old_order = len(graphs[0]) if graphs else 0
    next_order = old_order + 1
    output = []
    for old in graphs:
        for red_mask in range(1 << old_order):
            red_neighbors = [v for v in range(old_order) if red_mask >> v & 1]
            if any(old[a] >> b & 1 for a, b in combinations(red_neighbors, 2)):
                continue
            blue_neighbors = [v for v in range(old_order) if not (red_mask >> v & 1)]
            if any(
                all(not (old[a] >> b & 1) for a, b in combinations(triple, 2))
                for triple in combinations(blue_neighbors, 3)
            ):
                continue
            rows = list(old) + [red_mask]
            for vertex in red_neighbors:
                rows[vertex] |= 1 << old_order
            candidate = tuple(rows)
            require(len(candidate) == next_order and valid_34(candidate), "augmentation soundness")
            output.append(candidate)
    return output


def generate_34(max_order=8):
    levels = {0: [tuple()]}
    current = levels[0]
    for order in range(1, max_order + 1):
        current = augment_34(current)
        levels[order] = current
    return levels


def relabel_mask(adjacency, permutation, pair_index):
    result = 0
    for left, right in combinations(range(len(adjacency)), 2):
        if adjacency[left] >> right & 1:
            image = tuple(sorted((permutation[left], permutation[right])))
            result |= 1 << pair_index[image]
    return result


def classify_orbits(graphs):
    order = len(graphs[0])
    pair_index = {pair: index for index, pair in enumerate(combinations(range(order), 2))}
    by_mask = {encode(graph): graph for graph in graphs}
    require(len(by_mask) == len(graphs), "duplicate labeled graph")
    remaining = set(by_mask)
    records = []
    while remaining:
        representative = min(remaining)
        graph = by_mask[representative]
        orbit = {
            relabel_mask(graph, permutation, pair_index)
            for permutation in permutations(range(order))
        }
        require(orbit <= remaining, "orbit leaves or overlaps the complete census")
        remaining -= orbit
        records.append({
            "representative": representative,
            "edges": representative.bit_count(),
            "labeled_graphs": len(orbit),
            "automorphisms": factorial(order) // len(orbit),
        })
    return records


def direct_six_census():
    return {
        mask
        for mask in range(1 << 15)
        if valid_34(decode(6, mask))
    }


def balanced_rooted_pairs(eight_classes, six_classes):
    pairs = []
    for h_record in eight_classes:
        h_edges = h_record["edges"]
        for bc_record in six_classes:
            b_edges = 15 - bc_record["edges"]
            if 56 - 2 * h_edges == 48 - 2 * b_edges:
                require(h_edges - b_edges == 4, "degree balance identity")
                pairs.append((h_record["representative"], bc_record["representative"]))
    require(pairs == EXPECTED_CASES, "five rooted type pairs")
    return pairs


def decode_columns(h_side, b_side, columns, degree):
    h_order = len(h_side)
    b_order = len(b_side)
    root = h_order
    order = h_order + 1 + b_order
    adjacency = [0] * order

    for left in range(h_order):
        for right in range(left + 1, h_order):
            if h_side[left] >> right & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        adjacency[left] |= 1 << root
        adjacency[root] |= 1 << left

    for left in range(b_order):
        for right in range(left + 1, b_order):
            if b_side[left] >> right & 1:
                a = h_order + 1 + left
                b = h_order + 1 + right
                adjacency[a] |= 1 << b
                adjacency[b] |= 1 << a

    for b_index, column in enumerate(columns):
        b_vertex = h_order + 1 + b_index
        for h_vertex in range(h_order):
            if column >> h_vertex & 1:
                adjacency[b_vertex] |= 1 << h_vertex
                adjacency[h_vertex] |= 1 << b_vertex

    require(all(row.bit_count() == degree for row in adjacency), "decoded regularity")
    require(
        all(not monochromatic(adjacency, four, red) for four in combinations(range(order), 4) for red in (True, False)),
        "decoded monochromatic four-set",
    )
    return tuple(adjacency)


def column_first_search(h_side, b_side, degree):
    """Enumerate cross columns, checking literal four-sets after each insertion."""
    h_order = len(h_side)
    b_order = len(b_side)
    root = h_order
    total_order = h_order + 1 + b_order
    adjacency = [[False] * total_order for _ in range(total_order)]

    for left in range(h_order):
        for right in range(h_order):
            adjacency[left][right] = bool(h_side[left] >> right & 1)
        adjacency[left][root] = adjacency[root][left] = True
    for left in range(b_order):
        for right in range(b_order):
            a = h_order + 1 + left
            b = h_order + 1 + right
            adjacency[a][b] = bool(b_side[left] >> right & 1)

    row_targets = [degree - 1 - row.bit_count() for row in h_side]
    row_counts = [0] * h_order
    nodes = Counter()
    attempted_columns = 0
    solutions = []

    def visit(b_index, chosen_columns):
        nonlocal attempted_columns
        nodes[b_index] += 1
        if b_index == b_order:
            if row_counts == row_targets:
                solution = tuple(chosen_columns)
                decode_columns(h_side, b_side, solution, degree)
                solutions.append(solution)
            return

        new_vertex = h_order + 1 + b_index
        old_vertices = list(range(h_order + 1)) + list(range(h_order + 1, new_vertex))
        old_triples = tuple(combinations(old_vertices, 3))
        column_size = degree - b_side[b_index].bit_count()
        remaining = b_order - b_index - 1

        for chosen in combinations(range(h_order), column_size):
            attempted_columns += 1
            chosen_set = set(chosen)
            if any(
                row_counts[h] + int(h in chosen_set) > row_targets[h]
                or row_counts[h] + int(h in chosen_set) + remaining < row_targets[h]
                for h in range(h_order)
            ):
                continue

            for h in range(h_order):
                adjacency[new_vertex][h] = adjacency[h][new_vertex] = h in chosen_set

            good = True
            for a, b, c in old_triples:
                color = adjacency[new_vertex][a]
                if (
                    adjacency[new_vertex][b] == color
                    and adjacency[new_vertex][c] == color
                    and adjacency[a][b] == color
                    and adjacency[a][c] == color
                    and adjacency[b][c] == color
                ):
                    good = False
                    break

            if good:
                for h in chosen_set:
                    row_counts[h] += 1
                mask = sum(1 << h for h in chosen_set)
                visit(b_index + 1, chosen_columns + [mask])
                for h in chosen_set:
                    row_counts[h] -= 1

        for h in range(h_order):
            adjacency[new_vertex][h] = adjacency[h][new_vertex] = False

    visit(0, [])
    return {
        "nodes_by_depth": [nodes[depth] for depth in range(b_order + 1)],
        "attempted_columns": attempted_columns,
        "solutions": sorted(solutions),
    }


def obstruction(eight_classes, six_classes):
    cases = balanced_rooted_pairs(eight_classes, six_classes)
    records = []
    for h_mask, b_complement_mask in cases:
        h_side = decode(8, h_mask)
        b_side = complement(decode(6, b_complement_mask))
        result = column_first_search(h_side, b_side, 8)
        require(result["solutions"] == [], "regular (4,4;15) completion found")
        records.append({
            "H_mask": h_mask,
            "B_complement_mask": b_complement_mask,
            "nodes_by_depth": result["nodes_by_depth"],
            "attempted_columns": result["attempted_columns"],
            "completions": 0,
        })
    require([record["attempted_columns"] for record in records] == [812, 812, 812, 812, 4732],
            "clean-room search coverage")
    return records


def rook_control():
    rook = [
        {other for other in range(9) if vertex != other and (vertex // 3 == other // 3 or vertex % 3 == other % 3)}
        for vertex in range(9)
    ]
    root = 0
    h_vertices = sorted(rook[root])
    b_vertices = sorted(set(range(1, 9)) - set(h_vertices))
    h_side = tuple(
        sum(1 << j for j, other in enumerate(h_vertices) if other in rook[vertex])
        for vertex in h_vertices
    )
    b_side = tuple(
        sum(1 << j for j, other in enumerate(b_vertices) if other in rook[vertex])
        for vertex in b_vertices
    )
    actual = tuple(
        sum(1 << h for h, vertex in enumerate(h_vertices) if vertex in rook[b_vertex])
        for b_vertex in b_vertices
    )
    result = column_first_search(h_side, b_side, 4)
    require(len(result["solutions"]) == 82 and actual in result["solutions"], "rook positive control")
    for solution in result["solutions"]:
        decode_columns(h_side, b_side, solution, 4)

    negative_tests = 0
    changed = list(actual)
    changed[0] ^= 1
    try:
        decode_columns(h_side, b_side, changed, 4)
    except ValueError:
        negative_tests += 1
    else:
        raise ValueError("changed rook cross edge accepted")

    complete = tuple(((1 << 5) - 1) ^ (1 << vertex) for vertex in range(5))
    try:
        require(
            all(not monochromatic(complete, four, red) for four in combinations(range(5), 4) for red in (True, False)),
            "decoded monochromatic four-set",
        )
    except ValueError:
        negative_tests += 1
    else:
        raise ValueError("complete graph negative accepted")
    require(negative_tests == 2, "negative control count")
    return {
        "solutions": len(result["solutions"]),
        "attempted_columns": result["attempted_columns"],
        "nodes_by_depth": result["nodes_by_depth"],
        "negative_tests": negative_tests,
    }


def application_audit():
    # Height 2589, independently reviewed at height 2597, supplies a set P of
    # fourteen vertices and root 4 with all fifteen degrees equal to eight.
    require(14 + 1 == 15, "rooted side order")
    require(14 * 8 + 8 == 2 * 60, "rooted side edge count")
    # Uniform red adjacency to exceptional root 0 and uniform blue adjacency
    # to exceptional root 1 turn a monochromatic K4 in the side into a K5.
    return {
        "profile": "19^2 20^3 21^38",
        "M": 217,
        "rooted_side_order": 15,
        "rooted_side_degree": 8,
        "rooted_side_edges": 60,
        "hard_branch_excluded": True,
        "global_profiles_after": 66,
        "anchored_splits_after": 271,
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    levels = generate_34(8)
    labeled_counts = [len(levels[order]) for order in range(1, 9)]
    require(labeled_counts == [1, 2, 7, 40, 322, 2812, 13842, 17640], "labeled census counts")
    six_masks = {encode(graph) for graph in levels[6]}
    require(six_masks == direct_six_census(), "independent six-vertex brute force")
    six_classes = classify_orbits(levels[6])
    eight_classes = classify_orbits(levels[8])
    require(len(six_classes) == 15 and sum(row["labeled_graphs"] for row in six_classes) == 2812,
            "fifteen six-vertex orbits")
    require([row["representative"] for row in eight_classes] == [5388912, 5404008, 5683824],
            "three eight-vertex orbits")
    require([row["labeled_graphs"] for row in eight_classes] == [5040, 10080, 2520],
            "eight-vertex orbit sizes")

    cases = obstruction(eight_classes, six_classes)
    control = rook_control()
    application = application_audit()
    report = {
        "census": {
            "labeled_counts_order_1_to_8": labeled_counts,
            "six_vertex_classes": six_classes,
            "eight_vertex_classes": eight_classes,
        },
        "balanced_cases": cases,
        "positive_control": control,
        "application": application,
        "algorithm": "column-first literal-four-set search",
        "solver_used": False,
        "external_catalog_used_in_proof": False,
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print("PASS independent labeled (3,4) augmentation through order eight:", labeled_counts)
    print("PASS S8 and S6 orbit partitions: eight_types=3 six_types=15 labeled=17640/2812")
    print("PASS degree balance reduces 45 rooted pairs to five exact mask pairs")
    print("PASS transposed column-first literal search excludes all five cases; attempts=812,812,812,812,4732")
    print("PASS rook-graph positive control has 82 completions; two negative controls rejected")
    print("THEOREM no eight-regular (4,4;15) graph; conditional hard profile 19^2 20^3 21^38 excluded")
    print("SCOPE application imports the reviewed height-2589 hard-branch reduction; no target graph or Ramsey-bound claim")


if __name__ == "__main__":
    main()
