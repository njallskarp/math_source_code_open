#!/usr/bin/env python3
"""Solver-free literal verifier for the M=216 aggregate-edge limitation witness."""

from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
B = {18: 220, 19: 221, 20: 220, 21: 220, 22: 221, 23: 223, 24: 223}
EXTREMA = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


@lru_cache(None)
def upper(red, blue):
    if min(red, blue) == 1:
        return 1
    left, right = upper(red - 1, blue), upper(red, blue - 1)
    return left + right - int(left % 2 == right % 2 == 0)


def decode_core(order, mask):
    pairs = tuple(combinations(range(order), 2))
    require(type(mask) is int and 0 <= mask < 1 << len(pairs), "core mask range")
    adjacency = [set() for _ in range(order)]
    for bit, (left, right) in enumerate(pairs):
        if mask >> bit & 1:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return tuple(frozenset(row) for row in adjacency)


def clique(adjacency, vertices, red):
    return all((right in adjacency[left]) == red for left, right in combinations(vertices, 2))


def clique_number(adjacency, allowed, red):
    vertices = [vertex for vertex in range(len(adjacency)) if allowed >> vertex & 1]
    return max(
        size for size in range(len(vertices) + 1)
        if any(clique(adjacency, subset, red) for subset in combinations(vertices, size))
    )


def admissible_signatures(adjacency, degrees, M):
    order = len(adjacency)
    central = 43 - order
    full = (1 << order) - 1
    answer = {}
    for mask in range(1 << order):
        weight = sum(degrees[i] - 21 for i in range(order) if mask >> i & 1)
        if weight > M - 220:
            continue
        red_number = clique_number(adjacency, mask, True)
        blue_number = clique_number(adjacency, full ^ mask, False)
        if red_number >= 4 or blue_number >= 4:
            continue
        answer[mask] = min(central, upper(5 - red_number, 5 - blue_number) - 1)
    return answer


def root_data(adjacency):
    order = len(adjacency)
    for word in product(range(3), repeat=order):
        red = frozenset(i for i, value in enumerate(word) if value == 1)
        blue = frozenset(i for i, value in enumerate(word) if value == 2)
        if not red | blue or not clique(adjacency, red, True) or not clique(adjacency, blue, False):
            continue
        fixed = frozenset(
            i for i in range(order) if i not in red | blue
            and red <= adjacency[i] and not blue & adjacency[i]
        )
        yield red, blue, fixed, 5 - len(red), 5 - len(blue)


def verify_document(document):
    require(document["format"] == "r55-double19-external-root-lift-v1", "format")
    require(document["generated_two_sided_rows"] == 3861 and document["search_trials"] == 54,
            "discovery metadata")
    record = document["record"]
    require(record["counts_18_to_24"] == "0,2,5,36,0,0,0", "selected profile")
    require(record["M"] == 216 and record["split_count"] == 3, "M and anchored split count")
    require(record["exceptional_degrees"] == [19, 19, 20, 20, 20, 20, 20], "exceptional degrees")
    degrees = tuple(record["exceptional_degrees"])
    edge_total = 231 + record["M"]
    require(sum(degrees) + 36 * 21 == 2 * edge_total, "global degree sum")
    require(3 * sum((degree - 21) ** 2 for degree in degrees) == 39, "paired excess 39")

    adjacency = decode_core(len(degrees), record["core_mask"])
    require(all(not clique(adjacency, subset, color)
                for subset in combinations(range(len(degrees)), 5) for color in (True, False)),
            "exceptional core has no monochromatic K5")
    epsilon = tuple(degree - 21 for degree in degrees)
    for vertex, degree in enumerate(degrees):
        weighted = sum(epsilon[neighbor] for neighbor in adjacency[vertex])
        require(weighted <= record["M"] - B[degree], "individual exceptional weighted inequality")
    central_weight = sum(epsilon[i] * (degrees[i] - len(adjacency[i])) for i in range(len(degrees)))
    require(central_weight <= 36 * (record["M"] - 220), "summed central weighted inequality")

    capacities = admissible_signatures(adjacency, degrees, record["M"])
    require(len(capacities) == record["eligible_signatures"] == 90, "eligible signatures")
    values = {}
    for pair in record["cells"]:
        require(isinstance(pair, list) and len(pair) == 2, "cell pair format")
        mask, value = pair
        require(type(mask) is type(value) is int and mask not in values and value > 0, "sparse cells")
        require(mask in capacities and value <= capacities[mask], "cell capacity")
        values[mask] = value
    require(sum(values.values()) == 36 and len(values) == 19, "central cell total")
    for vertex, degree in enumerate(degrees):
        incidence = sum(value for mask, value in values.items() if mask >> vertex & 1)
        require(incidence == degree - len(adjacency[vertex]), "exceptional margin")

    cells = tuple(sorted(values))
    variable_pairs = tuple(
        (left, right)
        for left, right in combinations_with_replacement(cells, 2)
        if left != right or values[left] >= 2
    )
    require(len(variable_pairs) == document["edge_variables"] == 184, "edge-variable count")
    variable_index = {pair: index for index, pair in enumerate(variable_pairs)}
    boxes = tuple(
        values[left] * values[right] if left != right
        else values[left] * (values[left] - 1) // 2
        for left, right in variable_pairs
    )
    edge_values = [0] * len(variable_pairs)
    seen_edges = set()
    for triple in document["aggregate_edges"]:
        require(isinstance(triple, list) and len(triple) == 3, "edge triple format")
        left, right, value = triple
        pair = (left, right)
        require(type(left) is type(right) is type(value) is int and value > 0, "sparse edge value")
        require(pair in variable_index and pair not in seen_edges, "known unique edge pair")
        index = variable_index[pair]
        require(value <= boxes[index], "edge box")
        edge_values[index] = value
        seen_edges.add(pair)
    require(len(seen_edges) == 138, "nonzero aggregate-edge count")

    labels = [None] * len(degrees)
    for mask in cells:
        labels.extend([mask] * values[mask])
    require(len(labels) == 43, "literal vertex count")
    central_vertices = frozenset(range(len(degrees), 43))
    all_vertices = frozenset(range(43))
    cell_vertices = {
        mask: frozenset(vertex for vertex in central_vertices if labels[vertex] == mask)
        for mask in cells
    }

    literal_entries = []
    literal_boxes = [0] * len(variable_pairs)
    for left, right in combinations(range(43), 2):
        if left >= len(degrees):
            pair = tuple(sorted((labels[left], labels[right])))
            index = variable_index[pair]
            literal_boxes[index] += 1
            literal_entries.append((left, right, index, None))
        else:
            red = right in adjacency[left] if right < len(degrees) else bool(labels[right] >> left & 1)
            literal_entries.append((left, right, None, red))
    require(tuple(literal_boxes) == boxes, "literal variable boxes")

    uniformity_checks = 0

    def form(left_set, right_set=None):
        nonlocal uniformity_checks
        coefficients = [None] * len(variable_pairs)
        fixed_red = 0
        possible = 0
        for left, right, index, fixed_color in literal_entries:
            weight = (int(left in left_set and right in left_set) if right_set is None
                      else int(left in left_set and right in right_set)
                      + int(right in left_set and left in right_set))
            possible += weight
            if index is None:
                fixed_red += weight * fixed_color
            elif coefficients[index] is None:
                coefficients[index] = weight
            else:
                require(coefficients[index] == weight, "nonuniform cell-pair coefficient")
                uniformity_checks += 1
        require(all(value is not None for value in coefficients), "missing literal variable class")
        red_total = fixed_red + sum(value * edge for value, edge in zip(coefficients, edge_values))
        return red_total, possible

    # Cellwise sums, not individual central-vertex degree sequences.
    for mask, vertices in cell_vertices.items():
        red_incidence, possible = form(vertices, all_vertices)
        require(red_incidence == 21 * len(vertices), "aggregate central degree")
        require(possible == 42 * len(vertices), "literal degree incidence capacity")

    local_profiles = []
    for vertex, degree in enumerate(degrees):
        red_neighborhood = adjacency[vertex] | frozenset(
            v for v in central_vertices if labels[v] >> vertex & 1
        )
        blue_neighborhood = all_vertices - {vertex} - red_neighborhood
        t_red, red_possible = form(red_neighborhood)
        red_inside_blue, blue_possible = form(blue_neighborhood)
        t_blue = blue_possible - red_inside_blue
        require(red_possible == degree * (degree - 1) // 2, "red-neighborhood size")
        require(blue_possible == (42 - degree) * (41 - degree) // 2, "blue-neighborhood size")
        require(t_red <= EXTREMA[degree] - 7, "hard red local cap")
        require(t_blue <= EXTREMA[42 - degree] - 7, "hard blue local cap")
        neighbor_degree_sum = sum(degrees[j] for j in adjacency[vertex])
        neighbor_degree_sum += 21 * (degree - len(adjacency[vertex]))
        identity = blue_possible - edge_total + neighbor_degree_sum
        require(t_red + t_blue == identity, "local edge identity")
        local_profiles.append((t_red, t_blue))

    roots = 0
    lifted_red = lifted_blue = fixed_lifts = density_rows = 0
    external_red = external_blue = 0
    smallest_lift_slack = None
    side_histogram = Counter()
    for red, blue, fixed_vertices, p, q in root_data(adjacency):
        roots += 1
        selected_cells = frozenset(
            mask for mask in cells
            if all(mask >> i & 1 for i in red) and all(not (mask >> i & 1) for i in blue)
        )
        selected_central = frozenset().union(*(cell_vertices[mask] for mask in selected_cells)) \
            if selected_cells else frozenset()
        side = fixed_vertices | selected_central
        require(len(side) <= upper(p, q) - 1, "root-union capacity")
        if len(red) == len(blue) == 1:
            side_histogram[len(side)] += 1

        for mask, vertices in cell_vertices.items():
            red_incidence, possible = form(vertices, side)
            if all(mask >> i & 1 for i in red):
                cap = upper(p - 1, q) - 1
                slack = cap * len(vertices) - red_incidence
                require(slack >= 0, "external-root red lifting")
                lifted_red += 1
                external_red += int(mask not in selected_cells)
                smallest_lift_slack = slack if smallest_lift_slack is None else min(smallest_lift_slack, slack)
            if all(not (mask >> i & 1) for i in blue):
                cap = upper(p, q - 1) - 1
                blue_incidence = possible - red_incidence
                slack = cap * len(vertices) - blue_incidence
                require(slack >= 0, "external-root blue lifting")
                lifted_blue += 1
                external_blue += int(mask not in selected_cells)
                smallest_lift_slack = slack if smallest_lift_slack is None else min(smallest_lift_slack, slack)

        for vertex in fixed_vertices:
            red_degree = len(adjacency[vertex] & fixed_vertices)
            red_degree += sum(values[mask] for mask in selected_cells if mask >> vertex & 1)
            blue_degree = len(side) - 1 - red_degree
            require(red_degree <= upper(p - 1, q) - 1, "fixed-root red lifting")
            require(blue_degree <= upper(p, q - 1) - 1, "fixed-root blue lifting")
            fixed_lifts += 2

        if p == q == 4 and len(side) in (15, 16):
            red_edges, possible = form(side)
            low, high = (50, 55) if len(side) == 15 else (58, 62)
            require(possible == len(side) * (len(side) - 1) // 2, "density side capacity")
            require(low <= red_edges <= high, "rooted density interval")
            density_rows += 1

    require(roots == record["union_cuts"] == 262, "complete root count")
    expected_histogram = {int(size): count for size, count in record["side_size_histogram"].items()}
    require(dict(sorted(side_histogram.items())) == expected_histogram, "ordered exceptional-root sides")
    require(max(side_histogram) == record["maximum_exceptional_root_side"] == 14, "maximum side fourteen")
    require(density_rows == 0, "order-15/16 density rows do not activate")

    fixed_edge_total = sum(right in adjacency[left] for left, right in combinations(range(len(degrees)), 2))
    fixed_edge_total += sum(values[mask] * mask.bit_count() for mask in cells)
    require(fixed_edge_total + sum(edge_values) == edge_total == 447, "global red edge total")

    return {
        "roots": roots,
        "lifted_red": lifted_red,
        "lifted_blue": lifted_blue,
        "external_red": external_red,
        "external_blue": external_blue,
        "fixed_lifts": fixed_lifts,
        "smallest_lift_slack": smallest_lift_slack,
        "uniformity_checks": uniformity_checks,
        "local_profiles": local_profiles,
    }


def mutation_tests(document):
    mutants = [deepcopy(document) for _ in range(4)]
    mutants[0]["aggregate_edges"][0][2] += 1
    mutants[1]["record"]["cells"][0][1] += 1
    mutants[2]["record"]["core_mask"] ^= 1
    mutants[3]["record"]["maximum_exceptional_root_side"] += 1
    for mutant in mutants:
        try:
            verify_document(mutant)
        except (KeyError, ValueError):
            continue
        raise ValueError("altered certificate accepted")


def main():
    document = json.loads((HERE / "EDGE_LIFT.json").read_text())
    summary = verify_document(document)
    mutation_tests(document)
    print("PASS M=216 profile 19^2 20^5 21^36; literal seven-vertex core and 19 signature cells")
    print("PASS 184 aggregate central-edge variables (138 nonzero), exact boxes, degrees, and 447 total edges")
    print("PASS hard exceptional local profiles: " + ", ".join(f"{red}/{blue}" for red, blue in summary["local_profiles"]))
    print(f"PASS all {summary['roots']} root-union capacities; exceptional ordered-side maximum 14")
    print(
        f"PASS {summary['lifted_red'] + summary['lifted_blue']} central-cell lifting inequalities "
        f"({summary['external_red'] + summary['external_blue']} genuinely external) and "
        f"{summary['fixed_lifts']} fixed-vertex inequalities; minimum slack {summary['smallest_lift_slack']}"
    )
    print(f"PASS literal cell-pair coefficient uniformity checked {summary['uniformity_checks']} times")
    print("PASS four altered certificates rejected")
    print("LIMITATION external-root lifting plus the rooted order-15/16 density result does not exclude M=216")
    print("SCOPE exact aggregate counts, not individual central edges, a 43-vertex graph, or profile feasibility")


if __name__ == "__main__":
    main()
