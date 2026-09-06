#!/usr/bin/env python3
"""Independent exact audit of the h3581 star and conditioned-degree claims.

The checker reads only the published compact certificate.  It deliberately
uses edge sets and physical four-tuples instead of importing the producer's
decoder, emitters, inherited OPB builders, or checker.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools as it
import json
import math
from pathlib import Path


N = 43
EXCEPTIONAL = frozenset(range(2, 15))
PAIRS4 = tuple(it.combinations(range(4), 2))
EXPECTED_CERTIFICATE_SHA256 = (
    "a457fd08c54515ae68ff2526ef79d4f74adaf21074babaea53927d3917a49b1c"
)
EXPECTED_SEPARATOR_SHA256 = (
    "d59e2f376c97232300532c004409f29a518868694cf7888175f731b0e10f4070"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def red_edges(mask):
    return {
        frozenset(pair)
        for bit, pair in enumerate(PAIRS4)
        if (mask >> bit) & 1
    }


def edge_mask(edges):
    return sum(
        1 << bit
        for bit, pair in enumerate(PAIRS4)
        if frozenset(pair) in edges
    )


def load_certificate(path):
    payload = path.read_bytes()
    require(
        hashlib.sha256(payload).hexdigest() == EXPECTED_CERTIFICATE_SHA256,
        "unexpected certificate hash",
    )
    raw = json.loads(payload)
    require(
        set(raw)
        == {"format", "denominator", "cells", "active_selectors", "four_tables"}
        and raw["format"] == "class-state-orbits-v1",
        "certificate schema",
    )
    denominator = raw["denominator"]
    require(type(denominator) is int and denominator > 0, "positive denominator")
    cells = raw["cells"]
    flat = sum(cells, [])
    require(
        all(isinstance(cell, list) and cell for cell in cells)
        and len(flat) == N
        and sorted(flat) == list(range(N)),
        "physical vertex partition",
    )
    require(raw["active_selectors"] == [278], "selected root 278")
    type_of = [None] * N
    for kind, cell in enumerate(cells):
        for vertex in cell:
            require(type(vertex) is int, "integer vertex label")
            type_of[vertex] = kind

    sizes = tuple(map(len, cells))
    expected_types = {
        types
        for types in it.combinations_with_replacement(range(len(cells)), 4)
        if all(types.count(kind) <= sizes[kind] for kind in set(types))
    }
    tables = {}
    for record in raw["four_tables"]:
        require(set(record) == {"types", "orbits"}, "four-table schema")
        types = tuple(record["types"])
        require(
            types in expected_types and types not in tables,
            "unique feasible canonical type multiset",
        )
        masses = [0] * 64
        covered = set()
        stabilizer = [
            permutation
            for permutation in it.permutations(range(4))
            if all(types[permutation[position]] == types[position] for position in range(4))
        ]
        for key, value in record["orbits"].items():
            representative = int(key)
            require(
                str(representative) == key
                and 0 <= representative < 64
                and type(value) is int
                and value > 0,
                "positive canonical orbit mass",
            )
            original_edges = red_edges(representative)
            orbit = set()
            for permutation in stabilizer:
                transformed = {
                    frozenset((left, right))
                    for left, right in PAIRS4
                    if frozenset((permutation[left], permutation[right])) in original_edges
                }
                orbit.add(edge_mask(transformed))
            require(representative == min(orbit), "noncanonical orbit representative")
            require(not (covered & orbit), "overlapping state orbits")
            covered.update(orbit)
            for state in orbit:
                masses[state] = value
        require(sum(masses) == denominator, "four-table normalization")
        tables[types] = tuple(masses)
    require(set(tables) == expected_types and len(tables) == 345, "complete table family")
    return denominator, tuple(type_of), tables


def physical_decoder(type_of, tables):
    cache = {}

    def distribution(vertices):
        type_sequence = tuple(type_of[vertex] for vertex in vertices)
        if type_sequence in cache:
            return cache[type_sequence]
        canonical_to_physical = tuple(
            sorted(range(4), key=lambda position: (type_sequence[position], position))
        )
        canonical_types = tuple(type_sequence[position] for position in canonical_to_physical)
        canonical = tables[canonical_types]
        physical = [0] * 64
        for canonical_state, mass in enumerate(canonical):
            physical_edges = {
                frozenset((canonical_to_physical[left], canonical_to_physical[right]))
                for left, right in map(tuple, red_edges(canonical_state))
            }
            physical[edge_mask(physical_edges)] = mass
        require(sum(physical) == sum(canonical), "physical state transport")
        cache[type_sequence] = tuple(physical)
        return cache[type_sequence]

    return distribution


def edge_marginals(denominator, tables):
    candidates = defaultdict(set)
    for types, masses in tables.items():
        for bit, (left, right) in enumerate(PAIRS4):
            pair_types = tuple(sorted((types[left], types[right])))
            candidates[pair_types].add(
                sum(mass for state, mass in enumerate(masses) if (state >> bit) & 1)
            )
    require(
        all(len(values) == 1 for values in candidates.values()),
        "inconsistent edge projections across four-tables",
    )
    result = {key: next(iter(values)) for key, values in candidates.items()}
    require(all(0 <= value <= denominator for value in result.values()), "edge boxes")
    return result


def check_star_family(denominator, type_of, tables, edge_moment):
    minimum = None
    tight = [0, 0]
    per_center = [0] * N
    row_count = 0
    for four_set in it.combinations(range(N), 4):
        masses = tables[tuple(sorted(type_of[vertex] for vertex in four_set))]
        all_blue = masses[0]
        all_red = masses[63]
        outside = (vertex for vertex in range(N) if vertex not in four_set)
        for center in outside:
            red_sum = sum(
                edge_moment[tuple(sorted((type_of[center], type_of[vertex])))]
                for vertex in four_set
            )
            gaps = (red_sum - all_blue, 4 * denominator - red_sum - all_red)
            require(min(gaps) >= 0, f"star row failure {(center, four_set)}")
            minimum = min(gaps) if minimum is None else min(minimum, *gaps)
            tight[0] += gaps[0] == 0
            tight[1] += gaps[1] == 0
            per_center[center] += 2
            row_count += 2
    require(row_count == 2 * N * math.comb(N - 1, 4), "complete star count")
    require(per_center == [223860] * N, "complete center multiplicities")
    return {
        "star_rows": row_count,
        "star_minimum_slack": str(Fraction(minimum, denominator)),
        "star_tight_blue": tight[0],
        "star_tight_red": tight[1],
    }


def restriction_and_joint(distribution, omitted_position, center_position):
    kept = tuple(position for position in range(4) if position != omitted_position)
    kept_pairs = tuple(it.combinations(kept, 2))
    bit_for_pair = {pair: bit for bit, pair in enumerate(PAIRS4)}
    outside_edge = tuple(sorted((omitted_position, center_position)))
    marginal = [0] * 8
    joint = [0] * 8
    for state, mass in enumerate(distribution):
        triple_state = sum(
            ((state >> bit_for_pair[pair]) & 1) << bit
            for bit, pair in enumerate(kept_pairs)
        )
        marginal[triple_state] += mass
        if (state >> bit_for_pair[outside_edge]) & 1:
            joint[triple_state] += mass
    return tuple(marginal), tuple(joint)


def combination_rank_table():
    return {four_set: rank for rank, four_set in enumerate(it.combinations(range(N), 4))}


def witness_row(type_of, distribution, ranks):
    triple = (14, 27, 29)
    center = 27
    prescribed_degree = 21
    base_vertex = 0
    coefficients = Counter()
    values = {}
    for outside in range(N):
        if outside in triple:
            continue
        four_set = tuple(sorted(triple + (outside,)))
        position = {vertex: index for index, vertex in enumerate(four_set)}
        pairs = tuple(it.combinations(range(4), 2))
        bit_for_pair = {pair: bit for bit, pair in enumerate(pairs)}
        triple_bits = [
            bit_for_pair[tuple(sorted((position[left], position[right])))]
            for left, right in it.combinations(triple, 2)
        ]
        incident_bit = bit_for_pair[
            tuple(sorted((position[center], position[outside])))
        ]
        masses = distribution(four_set)
        base_index = 125170 + 64 * ranks[four_set]
        for state, mass in enumerate(masses):
            if any((state >> bit) & 1 for bit in triple_bits):
                continue
            coefficient = (state >> incident_bit) & 1
            if outside == base_vertex:
                coefficient -= prescribed_degree
            if coefficient:
                index = base_index + state
                coefficients[index] += coefficient
                values[index] = mass
    coefficients = {index: value for index, value in coefficients.items() if value}
    text = " ".join(f"{value:+d} x{index}" for index, value in sorted(coefficients.items()))
    text += " = 0 ;\n"
    row_hash = hashlib.sha256(text.encode()).hexdigest()
    require(len(coefficients) == 164, "separator support size")
    require(row_hash == EXPECTED_SEPARATOR_SHA256, "separator row hash")
    return coefficients, values, row_hash


def check_conditioned_degrees(denominator, type_of, distribution):
    cached = {}

    def for_four_set(four_set, omitted, center):
        key = (tuple(type_of[v] for v in four_set), omitted, center)
        if key not in cached:
            cached[key] = restriction_and_joint(distribution(four_set), omitted, center)
        return cached[key]

    rows = 0
    violated = 0
    shared_marginal_coordinates = 0
    witness = None
    for triple in it.combinations(range(N), 3):
        outside_vertices = tuple(vertex for vertex in range(N) if vertex not in triple)
        reference_marginal = None
        joint_sums = {center: [0] * 8 for center in triple}
        for outside in outside_vertices:
            four_set = tuple(sorted(triple + (outside,)))
            omitted_position = four_set.index(outside)
            for center in triple:
                marginal, joint = for_four_set(
                    four_set, omitted_position, four_set.index(center)
                )
                if reference_marginal is None:
                    reference_marginal = marginal
                require(marginal == reference_marginal, "shared triple marginal")
                for state in range(8):
                    joint_sums[center][state] += joint[state]
            shared_marginal_coordinates += 8
        triple_pairs = tuple(it.combinations(range(3), 2))
        for center in triple:
            center_position = triple.index(center)
            prescribed_degree = 20 if center in EXCEPTIONAL else 21
            for state in range(8):
                local_degree = sum(
                    (state >> bit) & 1
                    for bit, pair in enumerate(triple_pairs)
                    if center_position in pair
                )
                left = joint_sums[center][state]
                right = (prescribed_degree - local_degree) * reference_marginal[state]
                gap = left - right
                rows += 1
                violated += gap != 0
                if (triple, center, state) == ((14, 27, 29), 27, 0):
                    witness = (left, reference_marginal[state], gap)
    require(rows == 3 * 8 * math.comb(N, 3), "complete conditioned-degree count")
    require(
        shared_marginal_coordinates == 8 * (N - 3) * math.comb(N, 3),
        "complete shared-marginal comparison count",
    )
    require(witness is not None, "missing named witness")
    left, mass, gap = witness
    ranks = combination_rank_table()
    coefficients, values, row_hash = witness_row(type_of, distribution, ranks)
    require(sum(coefficients[i] * values[i] for i in coefficients) == gap, "row value")
    return {
        "conditioned_degree_rows": rows,
        "violated_conditioned_degree_rows": violated,
        "shared_triple_marginal_coordinates": shared_marginal_coordinates,
        "witness_triple_mass": str(Fraction(mass, denominator)),
        "witness_lhs": str(Fraction(left, denominator)),
        "witness_rhs": "21/2",
        "witness_gap": str(Fraction(gap, denominator)),
        "separator_terms": len(coefficients),
        "separator_sha256": row_hash,
    }


def truth_table_controls():
    pairs = tuple(it.combinations(range(5), 2))
    bit_for_pair = {pair: bit for bit, pair in enumerate(pairs)}
    star_cases = 0
    excluded_cases = 0
    degree_cases = 0
    for graph in range(1 << len(pairs)):
        degrees = [
            sum((graph >> bit) & 1 for bit, pair in enumerate(pairs) if vertex in pair)
            for vertex in range(5)
        ]
        for center in range(5):
            inner = tuple(vertex for vertex in range(5) if vertex != center)
            red_sum = sum(
                (graph >> bit_for_pair[tuple(sorted((center, vertex)))]) & 1
                for vertex in inner
            )
            all_blue = int(
                all(
                    not ((graph >> bit_for_pair[pair]) & 1)
                    for pair in it.combinations(inner, 2)
                )
            )
            all_red = int(
                all(
                    (graph >> bit_for_pair[pair]) & 1
                    for pair in it.combinations(inner, 2)
                )
            )
            gaps = (red_sum - all_blue, 4 - red_sum - all_red)
            require(
                (gaps[0] < 0) == (graph == 0)
                and (gaps[1] < 0) == (graph == (1 << len(pairs)) - 1),
                "five-vertex star implication",
            )
            excluded_cases += (gaps[0] < 0) + (gaps[1] < 0)
            star_cases += 2
        for triple in it.combinations(range(5), 3):
            observed = sum(
                ((graph >> bit_for_pair[pair]) & 1) << bit
                for bit, pair in enumerate(it.combinations(triple, 2))
            )
            for center in triple:
                outside_degree = sum(
                    (graph >> bit_for_pair[tuple(sorted((center, vertex)))]) & 1
                    for vertex in range(5)
                    if vertex not in triple
                )
                center_position = triple.index(center)
                for state in range(8):
                    indicator = int(state == observed)
                    local_degree = sum(
                        (state >> bit) & 1
                        for bit, pair in enumerate(it.combinations(range(3), 2))
                        if center_position in pair
                    )
                    require(
                        indicator * outside_degree
                        == (degrees[center] - local_degree) * indicator,
                        "conditioned degree identity",
                    )
                    degree_cases += 1
    return {
        "five_vertex_star_cases": star_cases,
        "excluded_monochromatic_cases": excluded_cases,
        "five_vertex_conditioned_degree_cases": degree_cases,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    denominator, type_of, tables = load_certificate(args.certificate)
    distribution = physical_decoder(type_of, tables)
    result = {
        "status": "INDEPENDENT_EXACT_STAR_AND_D3_PASS",
        "certificate_sha256": EXPECTED_CERTIFICATE_SHA256,
        "denominator": str(denominator),
        "canonical_four_tables": len(tables),
        **truth_table_controls(),
        **check_star_family(
            denominator, type_of, tables, edge_marginals(denominator, tables)
        ),
        **check_conditioned_degrees(denominator, type_of, distribution),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
