#!/usr/bin/env python3
"""Exact verifier for the M=216 exceptional-root pointwise survivor."""

from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
B = {18: 220, 19: 221, 20: 220, 21: 220, 22: 221, 23: 223, 24: 223}
EXTREMA = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
TEMPLATE_EDGES = {
    (0, 1), (0, 2), (0, 3), (0, 6), (1, 4), (1, 5), (1, 6),
    (2, 3), (2, 4), (2, 5), (3, 6), (4, 5),
}


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
        answer[mask] = min(36, upper(5 - red_number, 5 - blue_number) - 1)
    return answer


def root_data(adjacency):
    order = len(adjacency)
    for word in product(range(3), repeat=order):
        red = frozenset(i for i, value in enumerate(word) if value == 1)
        blue = frozenset(i for i, value in enumerate(word) if value == 2)
        if not red | blue or not clique(adjacency, red, True) or not clique(adjacency, blue, False):
            continue
        fixed = frozenset(
            vertex for vertex in range(order) if vertex not in red | blue
            and red <= adjacency[vertex] and not blue & adjacency[vertex]
        )
        yield red, blue, fixed, 5 - len(red), 5 - len(blue)


def template_embeddings(core_edges):
    complement = set(combinations(range(7), 2)) - core_edges
    direct = reverse = 0
    for permutation in permutations(range(7)):
        image = {
            tuple(sorted((permutation[left], permutation[right])))
            for left, right in TEMPLATE_EDGES
        }
        direct += image == core_edges
        reverse += image == complement
    return direct, reverse


def verify_document(document):
    require(document["format"] == "r55-m216-height2715-cut-pointwise-survivor-v1", "format")
    record = document["record"]
    require(record["counts_18_to_24"] == "0,2,5,36,0,0,0", "profile counts")
    require(record["M"] == 216 and record["split_count"] == 3, "M and split count")
    degrees = tuple(record["exceptional_degrees"])
    require(degrees == (19, 19, 20, 20, 20, 20, 20), "exceptional degrees")
    adjacency = decode_core(7, record["core_mask"])
    require(record["core_mask"] == 901619, "recorded core")
    require(all(not clique(adjacency, subset, color)
                for subset in combinations(range(7), 5) for color in (True, False)),
            "core has no monochromatic K5")
    core_edges = {
        pair for pair in combinations(range(7), 2) if pair[1] in adjacency[pair[0]]
    }
    direct_templates, reverse_templates = template_embeddings(core_edges)
    require((direct_templates, reverse_templates) == (0, 0), "no exceptional-core template embedding")
    require(document["template_embeddings"] == [] and document["template_violations"] == 0,
            "template metadata")

    epsilon = tuple(degree - 21 for degree in degrees)
    for vertex, degree in enumerate(degrees):
        require(sum(epsilon[nbr] for nbr in adjacency[vertex]) <= 216 - B[degree],
                "individual exceptional weighted inequality")
    central_weight = sum(epsilon[i] * (degrees[i] - len(adjacency[i])) for i in range(7))
    require(central_weight <= 36 * (216 - 220), "central weighted inequality")

    capacities = admissible_signatures(adjacency, degrees, 216)
    require(len(capacities) == record["eligible_signatures"] == 90, "eligible signatures")
    cells = {}
    for mask, value in record["cells"]:
        require(type(mask) is type(value) is int and mask not in cells and value > 0, "cell format")
        require(mask in capacities and value <= capacities[mask], "cell capacity")
        cells[mask] = value
    require(len(cells) == 18 and sum(cells.values()) == 36, "positive cells")
    for vertex, degree in enumerate(degrees):
        require(sum(value for mask, value in cells.items() if mask >> vertex & 1)
                == degree - len(adjacency[vertex]), "exceptional margin")

    labels = tuple(mask for mask in sorted(cells) for _ in range(cells[mask]))
    require(labels == tuple(document["central_labels"]), "canonical central labels")
    central_pairs = tuple(combinations(range(36), 2))
    red_central = set()
    for pair in document["central_red_edges"]:
        require(isinstance(pair, list) and len(pair) == 2, "central edge format")
        left, right = pair
        require(type(left) is type(right) is int and 0 <= left < right < 36, "central edge range")
        require((left, right) not in red_central, "unique central edge")
        red_central.add((left, right))
    require(len(central_pairs) == document["binary_variables"] == 630, "binary variable count")
    require(len(red_central) == 321, "central red edge count")

    cell_pairs = tuple(
        (left, right) for left, right in combinations_with_replacement(sorted(cells), 2)
        if left != right or cells[left] >= 2
    )
    require(len(cell_pairs) == document["edge_variables"] == 165, "aggregate variable count")
    expected_aggregate = {(left, right): 0 for left, right in cell_pairs}
    for left, right, value in document["aggregate_edges"]:
        require((left, right) in expected_aggregate and value > 0, "aggregate edge format")
        require(expected_aggregate[(left, right)] == 0, "unique aggregate edge")
        expected_aggregate[(left, right)] = value
    actual_aggregate = Counter(
        tuple(sorted((labels[left], labels[right]))) for left, right in red_central
    )
    require(all(actual_aggregate[pair] == value for pair, value in expected_aggregate.items()),
            "literal edges match every aggregate quota")

    red_graph = [set() for _ in range(43)]
    for left, right in core_edges:
        red_graph[left].add(right); red_graph[right].add(left)
    for central, mask in enumerate(labels, 7):
        for exceptional in range(7):
            if mask >> exceptional & 1:
                red_graph[exceptional].add(central); red_graph[central].add(exceptional)
    for left, right in red_central:
        left += 7; right += 7
        red_graph[left].add(right); red_graph[right].add(left)
    expected_degrees = degrees + (21,) * 36
    require(tuple(map(len, red_graph)) == expected_degrees, "all 43 exact degrees")
    require(sum(map(len, red_graph)) // 2 == 447, "global red edge total")

    exceptional_profiles = []
    for vertex, degree in enumerate(degrees):
        red_neighbors = red_graph[vertex]
        blue_neighbors = set(range(43)) - {vertex} - red_neighbors
        t_red = sum(right in red_graph[left] for left, right in combinations(red_neighbors, 2))
        t_blue = sum(right not in red_graph[left] for left, right in combinations(blue_neighbors, 2))
        require(t_red <= EXTREMA[degree] - 7 and t_blue <= EXTREMA[42 - degree] - 7,
                "hard exceptional local caps")
        exceptional_profiles.append((t_red, t_blue))

    root_count = red_lifts = blue_lifts = external_lifts = fixed_lifts = density_rows = 0
    side_histogram = Counter()
    minimum_slack = None
    for red, blue, fixed, p, q in root_data(adjacency):
        root_count += 1
        selected = {
            central for central, mask in enumerate(labels, 7)
            if all(mask >> i & 1 for i in red) and all(not (mask >> i & 1) for i in blue)
        }
        side = set(fixed) | selected
        require(len(side) <= upper(p, q) - 1, "root-union capacity")
        if len(red) == len(blue) == 1:
            side_histogram[len(side)] += 1
        for central, mask in enumerate(labels, 7):
            if all(mask >> i & 1 for i in red):
                slack = upper(p - 1, q) - 1 - len(red_graph[central] & side)
                require(slack >= 0, "pointwise red external-root bound")
                red_lifts += 1
                external_lifts += central not in side
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
            if all(not (mask >> i & 1) for i in blue):
                blue_degree = len(side - {central} - red_graph[central])
                slack = upper(p, q - 1) - 1 - blue_degree
                require(slack >= 0, "pointwise blue external-root bound")
                blue_lifts += 1
                external_lifts += central not in side
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        for vertex in fixed:
            require(len(red_graph[vertex] & side) <= upper(p - 1, q) - 1,
                    "fixed red external-root bound")
            require(len(side - {vertex} - red_graph[vertex]) <= upper(p, q - 1) - 1,
                    "fixed blue external-root bound")
            fixed_lifts += 2
        if p == q == 4 and len(side) in (15, 16):
            red_edges = sum(right in red_graph[left] for left, right in combinations(side, 2))
            low, high = (50, 55) if len(side) == 15 else (58, 62)
            require(low <= red_edges <= high, "rooted density interval")
            density_rows += 1
    require(root_count == record["union_cuts"] == 263, "complete root count")
    require(red_lifts == document["pointwise_lifted_counts"]["red"] == 3015, "red lift count")
    require(blue_lifts == document["pointwise_lifted_counts"]["blue"] == 4284, "blue lift count")
    require(document["pointwise_rows"] == 7500, "pointwise row metadata")
    expected_histogram = {int(size): count for size, count in record["side_size_histogram"].items()}
    require(dict(sorted(side_histogram.items())) == expected_histogram, "ordered side histogram")
    require(max(side_histogram) == record["maximum_exceptional_root_side"] == 15, "maximum side")

    central_cap_violations = 0
    for vertex in range(7, 43):
        red_neighbors = red_graph[vertex]
        blue_neighbors = set(range(43)) - {vertex} - red_neighbors
        t_red = sum(right in red_graph[left] for left, right in combinations(red_neighbors, 2))
        t_blue = sum(right not in red_graph[left] for left, right in combinations(blue_neighbors, 2))
        central_cap_violations += t_red > 100 or t_blue > 100
    require(central_cap_violations == 32, "explicit central-cap limitation")

    monochromatic = [0, 0]
    for subset in combinations(range(43), 5):
        colors = [right in red_graph[left] for left, right in combinations(subset, 2)]
        monochromatic[0] += all(colors)
        monochromatic[1] += not any(colors)
    require(monochromatic == [317, 346], "explicit K5 limitation")

    return {
        "exceptional_profiles": exceptional_profiles,
        "root_count": root_count,
        "red_lifts": red_lifts,
        "blue_lifts": blue_lifts,
        "external_lifts": external_lifts,
        "fixed_lifts": fixed_lifts,
        "density_rows": density_rows,
        "minimum_slack": minimum_slack,
        "central_cap_violations": central_cap_violations,
        "monochromatic": monochromatic,
    }


def mutation_tests(document):
    mutants = [deepcopy(document) for _ in range(4)]
    mutants[0]["central_red_edges"].pop()
    mutants[1]["record"]["core_mask"] ^= 1
    mutants[2]["central_labels"][0] ^= 1
    mutants[3]["aggregate_edges"][0][2] += 1
    for mutant in mutants:
        try:
            verify_document(mutant)
        except (KeyError, ValueError):
            continue
        raise ValueError("altered survivor accepted")


def main():
    document = json.loads((HERE / "POINTWISE_SURVIVOR.json").read_text())
    result = verify_document(document)
    mutation_tests(document)
    print("PASS M=216 core 901619 has no direct or color-reversed height-2715 exceptional template")
    print("PASS 36 named central vertices, 321 red central edges, all 43 exact degrees, and 447 total edges")
    print("PASS all 165 cell-pair quotas and 263 exceptional root-union capacities")
    print("PASS hard exceptional local profiles: " + ", ".join(f"{a}/{b}" for a, b in result["exceptional_profiles"]))
    print(
        f"PASS {result['red_lifts'] + result['blue_lifts']} pointwise central lifting inequalities "
        f"({result['external_lifts']} genuinely external), {result['fixed_lifts']} fixed inequalities, "
        f"and {result['density_rows']} density rows; minimum slack {result['minimum_slack']}"
    )
    print("PASS four altered survivors rejected")
    print("LIMITATION exceptional-core height-2715 cut plus pointwise exceptional-root lifting does not exclude M=216")
    print(
        f"SCOPE not a Ramsey graph: {result['central_cap_violations']} central hard-cap violations and "
        f"{result['monochromatic'][0]}/{result['monochromatic'][1]} red/blue K5s"
    )


if __name__ == "__main__":
    main()
