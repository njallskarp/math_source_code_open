#!/usr/bin/env python3
"""Exact, solver-free verifier for the double-degree-19 transfer witnesses."""

from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
B = {18: 220, 19: 221, 20: 220, 21: 220, 22: 221, 23: 223, 24: 223}
EXPECTED = [
    ("0,2,1,36,4,0,0", 220, 5),
    ("0,2,2,36,3,0,0", 219, 6),
    ("0,2,3,36,2,0,0", 218, 6),
    ("0,2,4,36,1,0,0", 217, 5),
    ("0,2,5,36,0,0,0", 216, 3),
]


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


@lru_cache(None)
def upper(red, blue):
    """Elementary Ramsey upper bound with the even/even parity improvement."""
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


def clique(adjacency, mask, red):
    vertices = [vertex for vertex in range(len(adjacency)) if mask >> vertex & 1]
    return all((right in adjacency[left]) == red for left, right in combinations(vertices, 2))


def clique_number(adjacency, allowed, red):
    vertices = [vertex for vertex in range(len(adjacency)) if allowed >> vertex & 1]
    return max(
        (size for size in range(len(vertices) + 1)
         if any(clique(adjacency, sum(1 << vertex for vertex in subset), red)
                for subset in combinations(vertices, size))),
        default=0,
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


def verify_profile(record):
    counts_text = record["counts_18_to_24"]
    counts = tuple(map(int, counts_text.split(",")))
    M = record["M"]
    require(len(counts) == 7 and sum(counts) == 43, "profile order")
    require(sum(degree * count for degree, count in zip(range(18, 25), counts)) == 2 * (231 + M),
            "profile edge total")
    require(counts[1] == 2 and counts[3] == 36, "double-degree-19 family")
    degrees = tuple(degree for degree, count in zip(range(18, 25), counts)
                    if degree != 21 for _ in range(count))
    require(list(degrees) == record["exceptional_degrees"] and len(degrees) == 7,
            "exceptional degree list")
    require(sum(count * weight for count, weight in zip(counts, (21, 12, 3, 0, 3, 12, 21))) == 39,
            "paired excess 39")

    adjacency = decode_core(len(degrees), record["core_mask"])
    require(all(not clique(adjacency, sum(1 << vertex for vertex in subset), color)
                for subset in combinations(range(len(degrees)), 5) for color in (True, False)),
            "core has no monochromatic K5")
    epsilon = tuple(degree - 21 for degree in degrees)
    for vertex, degree in enumerate(degrees):
        weighted = sum(epsilon[neighbor] for neighbor in adjacency[vertex])
        require(weighted <= M - B[degree], "individual exceptional weighted inequality")
    central_weight = sum(epsilon[i] * (degrees[i] - len(adjacency[i])) for i in range(len(degrees)))
    require(central_weight <= 36 * (M - 220), "aggregate central weighted inequality")

    capacities = admissible_signatures(adjacency, degrees, M)
    require(len(capacities) == record["eligible_signatures"], "eligible signature count")
    cells = record["cells"]
    require(all(isinstance(pair, list) and len(pair) == 2 for pair in cells), "cell pair format")
    values = {}
    for mask, value in cells:
        require(type(mask) is type(value) is int and mask not in values and value > 0, "sparse cell format")
        require(mask in capacities and value <= capacities[mask], "signature capacity")
        values[mask] = value
    require(sum(values.values()) == 36, "central vertex total")
    for vertex, degree in enumerate(degrees):
        incidence = sum(value for mask, value in values.items() if mask >> vertex & 1)
        require(incidence == degree - len(adjacency[vertex]), "exceptional-to-central margin")

    full = (1 << len(degrees)) - 1
    union_count = 0
    for red_root in range(1 << len(degrees)):
        if not clique(adjacency, red_root, True):
            continue
        for blue_root in range(1 << len(degrees)):
            if red_root & blue_root or not (red_root | blue_root) or not clique(adjacency, blue_root, False):
                continue
            outside = full ^ (red_root | blue_root)
            red_vertices = [i for i in range(len(degrees)) if red_root >> i & 1]
            blue_vertices = [i for i in range(len(degrees)) if blue_root >> i & 1]
            exceptional_common = sum(
                all(i in adjacency[vertex] for i in red_vertices)
                and all(i not in adjacency[vertex] for i in blue_vertices)
                for vertex in range(len(degrees))
                if outside >> vertex & 1
            )
            central_common = sum(value for mask, value in values.items()
                                 if mask & red_root == red_root and not (mask & blue_root))
            bound = upper(5 - red_root.bit_count(), 5 - blue_root.bit_count()) - 1
            require(exceptional_common + central_common <= bound, "common-neighborhood union cut")
            union_count += 1
    require(union_count == record["union_cuts"], "complete union-root count")

    side_sizes = []
    for red_root in range(len(degrees)):
        for blue_root in range(len(degrees)):
            if red_root == blue_root:
                continue
            exceptional = sum(vertex not in (red_root, blue_root)
                              and vertex in adjacency[red_root]
                              and vertex not in adjacency[blue_root]
                              for vertex in range(len(degrees)))
            central = sum(value for mask, value in values.items()
                          if mask >> red_root & 1 and not (mask >> blue_root & 1))
            side_sizes.append(exceptional + central)
    histogram = {str(size): count for size, count in sorted(Counter(side_sizes).items())}
    require(histogram == record["side_size_histogram"], "ordered-side histogram")
    require(max(side_sizes) == record["maximum_exceptional_root_side"] == 14,
            "all exceptional-root one-way sides have order at most fourteen")
    return union_count, len(values), len(side_sizes)


def verify_document(document):
    require(document["format"] == "r55-exceptional-root-regular-side-transfer-v1", "format")
    require(document["scope"] ==
            "integer core/signature/union relaxation with every exceptional-root one-way side at most fourteen",
            "scope")
    require(document["profiles_requested"] == document["profiles_with_witness"] == 5, "five witnesses")
    records = document["records"]
    require([(row["counts_18_to_24"], row["M"], row["split_count"]) for row in records] == EXPECTED,
            "complete remaining double-degree-19 family")
    totals = Counter()
    for record in records:
        unions, cells, sides = verify_profile(record)
        totals.update(union_cuts=unions, positive_cells=cells, ordered_sides=sides,
                      anchored_splits=record["split_count"])
    require(totals == Counter(union_cuts=1522, positive_cells=105, ordered_sides=210, anchored_splits=25),
            "aggregate witness counts")
    return totals


def mutation_tests(document):
    mutants = [deepcopy(document) for _ in range(4)]
    mutants[0]["records"][0]["cells"][0][1] += 1
    mutants[1]["records"][1]["core_mask"] ^= 1
    mutants[2]["records"][2]["side_size_histogram"]["14"] += 1
    mutants[3]["records"].pop()
    for mutant in mutants:
        try:
            verify_document(mutant)
        except (KeyError, ValueError):
            continue
        raise ValueError("altered witness accepted")


def main():
    document = json.loads((HERE / "WITNESSES.json").read_text())
    totals = verify_document(document)
    mutation_tests(document)
    print("PASS five remaining double-degree-19 profiles, M=216..220 and 25 anchored splits")
    print("PASS literal exceptional cores: individual hard inequalities, central aggregate, and no core K5")
    print("PASS exact central cell margins and capacities; 105 positive cells")
    print("PASS all 1522 common-neighborhood union cuts")
    print("PASS all 210 ordered exceptional-root sides have order at most fourteen")
    print("PASS four altered witnesses rejected")
    print("LIMITATION the accepted order-15 regular-side obstruction cannot activate in this relaxation")
    print("SCOPE exact core/signature witnesses, not central-edge assignments or Ramsey(5,5;43) graphs")


if __name__ == "__main__":
    main()
