#!/usr/bin/env python3
"""Independent exact audit of the new h3599 conditioned/moment interfaces.

This checker reads the regenerated compact certificate but imports no producer,
emitter, solver, inherited OPB builder, or target checker.  It reconstructs
physical distributions from canonical state orbits and checks D3, T3, J1 and
the global deficiency row using a separate edge-set implementation.
"""

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import itertools as it
import json
import math
from pathlib import Path


N = 43
E = frozenset(range(2, 15))
PAIRS3 = tuple(it.combinations(range(3), 2))
PAIRS4 = tuple(it.combinations(range(4), 2))
CERTIFICATE_SHA256 = (
    "d957b35da176b786f85b8df85db37b1080ef1d04723a184be4a0cc8cae92f442"
)
SEPARATOR_SHA256 = (
    "307dd90f1f81cc849e2a2fdeddd584e4ac1ddade839cbfdb71bc8f21c63a8339"
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
    require(hashlib.sha256(payload).hexdigest() == CERTIFICATE_SHA256,
            "unexpected certificate hash")
    raw = json.loads(payload)
    require(
        set(raw) == {"format", "denominator", "cells", "active_selectors", "four_tables"}
        and raw["format"] == "class-state-orbits-v1",
        "certificate schema",
    )
    denominator = raw["denominator"]
    require(type(denominator) is int and denominator > 0, "positive denominator")
    cells = raw["cells"]
    require(
        all(isinstance(cell, list) and cell for cell in cells)
        and sorted(sum(cells, [])) == list(range(N)),
        "physical partition",
    )
    require(raw["active_selectors"] == [278], "root 278 selector")
    type_of = [None] * N
    for kind, cell in enumerate(cells):
        for vertex in cell:
            require(type(vertex) is int, "integer vertex")
            type_of[vertex] = kind
    sizes = tuple(map(len, cells))
    require(
        all(all((v in E) == (cell[0] in E) for v in cell) for cell in cells),
        "exceptional-class homogeneity",
    )
    expected = {
        types
        for types in it.combinations_with_replacement(range(len(cells)), 4)
        if all(types.count(kind) <= sizes[kind] for kind in set(types))
    }
    tables = {}
    positive_orbits = 0
    for record in raw["four_tables"]:
        require(set(record) == {"types", "orbits"}, "four-table schema")
        types = tuple(record["types"])
        require(types in expected and types not in tables, "unique feasible type multiset")
        stabilizer = [
            permutation
            for permutation in it.permutations(range(4))
            if all(types[permutation[position]] == types[position] for position in range(4))
        ]
        masses = [0] * 64
        covered = set()
        for key, value in record["orbits"].items():
            representative = int(key)
            require(
                str(representative) == key
                and 0 <= representative < 64
                and type(value) is int
                and 0 < value <= denominator,
                "positive orbit mass",
            )
            original = red_edges(representative)
            orbit = {
                edge_mask({
                    frozenset((left, right))
                    for left, right in PAIRS4
                    if frozenset((permutation[left], permutation[right])) in original
                })
                for permutation in stabilizer
            }
            require(representative == min(orbit), "canonical orbit representative")
            require(not covered.intersection(orbit), "disjoint state orbits")
            covered.update(orbit)
            for state in orbit:
                masses[state] = value
            positive_orbits += 1
        require(sum(masses) == denominator, "four-table normalization")
        tables[types] = tuple(masses)
    require(set(tables) == expected and len(tables) == 345, "complete four-table family")
    require(positive_orbits == 4149, "positive orbit census")
    return denominator, tuple(type_of), sizes, tables


def physical_decoder(tables):
    cache = {}

    def distribution(types):
        types = tuple(types)
        if types in cache:
            return cache[types]
        canonical_to_physical = tuple(
            sorted(range(4), key=lambda position: (types[position], position))
        )
        canonical_types = tuple(types[position] for position in canonical_to_physical)
        canonical = tables[canonical_types]
        physical = [0] * 64
        for state, mass in enumerate(canonical):
            edges = {
                frozenset((canonical_to_physical[left], canonical_to_physical[right]))
                for left, right in red_edges(state)
            }
            physical[edge_mask(edges)] = mass
        require(sum(physical) == sum(canonical), "physical state transport")
        cache[types] = tuple(physical)
        return cache[types]

    return distribution


def project_first_three(distribution):
    bits = (0, 1, 3)
    result = [0] * 8
    for state, mass in enumerate(distribution):
        result[sum(((state >> source) & 1) << target
                   for target, source in enumerate(bits))] += mass
    return tuple(result)


def low_marginals(denominator, sizes, distribution):
    triple = {}
    triple_projection_checks = 0
    kinds = range(len(sizes))
    for types in it.product(kinds, repeat=3):
        if any(types.count(kind) > sizes[kind] for kind in set(types)):
            continue
        candidates = []
        for extra in kinds:
            if types.count(extra) < sizes[extra]:
                candidates.append(project_first_three(distribution(types + (extra,))))
        require(candidates and all(value == candidates[0] for value in candidates),
                "inconsistent physical triple projection")
        triple[types] = candidates[0]
        triple_projection_checks += len(candidates)
    edge = {}
    edge_projection_checks = 0
    for types in it.product(kinds, repeat=2):
        if any(types.count(kind) > sizes[kind] for kind in set(types)):
            continue
        candidates = []
        for extra in kinds:
            if types.count(extra) < sizes[extra]:
                marginal = triple[types + (extra,)]
                candidates.append(sum(mass for state, mass in enumerate(marginal) if state & 1))
        require(candidates and all(value == candidates[0] for value in candidates),
                "inconsistent physical edge projection")
        edge[types] = candidates[0]
        edge_projection_checks += len(candidates)
    require(all(0 <= value <= denominator for value in edge.values()), "edge boxes")
    return triple, edge, triple_projection_checks, edge_projection_checks


def check_d3_t3(denominator, type_of, sizes, distribution, triple):
    d3_rows = 0
    t3_rows = 0
    t3_minimum = None
    degree_joint = {}
    all_four = {}
    for vertices in it.combinations(range(N), 3):
        types = tuple(type_of[v] for v in vertices)
        counts = [types.count(kind) for kind in range(len(sizes))]
        q = triple[types]
        for h_position, h in enumerate(vertices):
            degree = 20 if h in E else 21
            for state in range(8):
                local = sum(
                    (state >> bit) & 1
                    for bit, pair in enumerate(PAIRS3)
                    if h_position in pair
                )
                left = 0
                for kind, size in enumerate(sizes):
                    multiplicity = size - counts[kind]
                    if not multiplicity:
                        continue
                    key = (types, kind, h_position, state)
                    if key not in degree_joint:
                        masses = distribution(types + (kind,))
                        incident = PAIRS4.index(tuple(sorted((h_position, 3))))
                        degree_joint[key] = sum(
                            mass
                            for four_state, mass in enumerate(masses)
                            if (four_state >> incident) & 1
                            and all(
                                ((four_state >> source) & 1) == ((state >> target) & 1)
                                for target, source in enumerate((0, 1, 3))
                            )
                        )
                    left += multiplicity * degree_joint[key]
                require(left == (degree - local) * q[state], "D3 equality")
                d3_rows += 1
        for color in (0, 1):
            state = 7 if color else 0
            left = 0
            for kind, size in enumerate(sizes):
                multiplicity = size - counts[kind]
                if not multiplicity:
                    continue
                key = (types, kind, color)
                if key not in all_four:
                    masses = distribution(types + (kind,))
                    all_four[key] = masses[63 if color else 0]
                left += multiplicity * all_four[key]
            slack = 4 * q[state] - left
            require(slack >= 0, "T3 inequality")
            t3_minimum = slack if t3_minimum is None else min(t3_minimum, slack)
            t3_rows += 1
    require(d3_rows == 296184 and t3_rows == 24682, "complete D3/T3 row counts")
    return d3_rows, t3_rows, Fraction(t3_minimum, denominator)


def check_j1(denominator, type_of, distribution, triple, edge):
    red_four = {}
    rows = 0
    for h in range(N):
        others = tuple(v for v in range(N) if v != h)
        triangle_total = 93 if h in E else 100
        for a in others:
            left = 0
            for u, v in it.combinations(others, 2):
                if a in (u, v):
                    left += triple[(type_of[h], type_of[u], type_of[v])][7]
                else:
                    types = (type_of[h], type_of[a], type_of[u], type_of[v])
                    if types not in red_four:
                        red_four[types] = sum(
                            mass
                            for state, mass in enumerate(distribution(types))
                            if state & 39 == 39
                        )
                    left += red_four[types]
            right = triangle_total * edge[(type_of[h], type_of[a])]
            require(left == right, "J1 equality")
            rows += 1
    require(rows == 1806, "complete J1 count")
    return rows


def independent_separator_row():
    edge_names = {pair: index for index, pair in enumerate(it.combinations(range(N), 2), 1)}
    inherited = set()
    for c in range(9, 14):
        for k in range(7):
            sizes = (k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k)
            cells = []
            first = 2
            for size in sizes:
                cells.append(tuple(range(first, first + size)))
                first += size
            core = set(cells[0] + cells[4])
            outside = set(range(2, N)) - core
            inherited.update((u, v, h) for u, v in it.combinations(sorted(outside), 2)
                             for h in core)
    require(len(inherited) == 10612, "inherited wedge support")
    wedge_names = {key: 13634 + index for index, key in enumerate(sorted(inherited))}
    missing = [
        (u, v, h)
        for u, v in it.combinations(range(N), 2)
        for h in range(N)
        if h not in (u, v) and (u, v, h) not in inherited
    ]
    wedge_names.update({key: 98759 + index for index, key in enumerate(missing)})
    require(len(wedge_names) == 37023 and max(wedge_names.values()) == 125169,
            "complete wedge numbering")
    terms = {}
    for pair, index in edge_names.items():
        exceptional = sum(vertex in E for vertex in pair)
        if exceptional:
            terms[index] = -46 if exceptional == 2 else -25
    for key, index in wedge_names.items():
        if key[0] in E and key[1] in E:
            terms[index] = -2
    require(len(terms) == 3666, "separator term count")
    row = (" ".join(f"{coefficient:+d} x{index}"
                    for index, coefficient in sorted(terms.items()))
           + " >= -7972 ;\n").encode()
    require(hashlib.sha256(row).hexdigest() == SEPARATOR_SHA256, "separator hash")
    return row, edge_names, wedge_names


def check_global_moment(denominator, type_of, triple, edge, separator_path):
    reconstructed, edge_names, wedge_names = independent_separator_row()
    if separator_path is not None:
        supplied = separator_path.read_bytes()
        require(supplied == reconstructed, "supplied separator differs from reconstruction")
    first = 0
    direct_second = 0
    blue_expansion = 0
    row_left = 0
    for h in range(N):
        targets = tuple(u for u in sorted(E) if u != h)
        center_first = sum(edge[(type_of[h], type_of[u])] for u in targets)
        first += center_first
        direct_second += center_first
        blue_expansion += center_first
        for u, v in it.combinations(targets, 2):
            masses = triple[(type_of[u], type_of[v], type_of[h])]
            blue_wedge = masses[0] + masses[1]
            red_wedge = masses[6] + masses[7]
            x = edge[(type_of[h], type_of[u])]
            y = edge[(type_of[h], type_of[v])]
            require(red_wedge == blue_wedge + x + y - denominator,
                    "red/blue wedge identity")
            direct_second += 2 * red_wedge
            blue_expansion += 2 * (blue_wedge + x + y - denominator)
    require(first == 260 * denominator, "global first moment")
    require(direct_second == blue_expansion, "two square expansions agree")
    for pair, index in edge_names.items():
        exceptional = sum(vertex in E for vertex in pair)
        if exceptional:
            coefficient = -46 if exceptional == 2 else -25
            row_left += coefficient * edge[(type_of[pair[0]], type_of[pair[1]])]
    for (u, v, h), index in wedge_names.items():
        if u in E and v in E:
            masses = triple[(type_of[u], type_of[v], type_of[h])]
            row_left -= 2 * (masses[0] + masses[1])
    require(row_left + 7972 * denominator == 1576 * denominator - direct_second,
            "OPB row/scalar identity")
    gap = Fraction(direct_second - 1576 * denominator, denominator)
    require(gap > 71, "claimed strict separator gap")
    return Fraction(first, denominator), Fraction(direct_second, denominator), gap


def literal_controls():
    pairs = tuple(it.combinations(range(5), 2))
    d3_cases = j1_cases = cap_cases = square_cases = 0
    for graph in range(1024):
        red = {pair for bit, pair in enumerate(pairs) if (graph >> bit) & 1}
        degrees = [sum(vertex in pair for pair in red) for vertex in range(5)]
        for A in it.combinations(range(5), 3):
            observed = sum(
                (tuple(sorted(pair)) in red) << bit
                for bit, pair in enumerate(it.combinations(A, 2))
            )
            for h in A:
                external = sum(tuple(sorted((h, w))) in red for w in range(5) if w not in A)
                for state in range(8):
                    indicator = int(observed == state)
                    local = sum((state >> bit) & 1
                                for bit, pair in enumerate(it.combinations(A, 2)) if h in pair)
                    require(indicator * external == (degrees[h] - local) * indicator,
                            "literal D3 identity")
                    d3_cases += 1
        for h in range(5):
            others = tuple(v for v in range(5) if v != h)
            total = sum(all(tuple(sorted(pair)) in red
                            for pair in ((h, u), (h, v), (u, v)))
                        for u, v in it.combinations(others, 2))
            for a in others:
                conditioned = sum(all(tuple(sorted(pair)) in red
                                      for pair in ((h, u), (h, v), (u, v), (h, a)))
                                  for u, v in it.combinations(others, 2))
                require(conditioned == total * int(tuple(sorted((h, a))) in red),
                        "literal J1 identity")
                j1_cases += 1
        exceptional = {1, 2, 3}
        for h in range(5):
            targets = sorted(exceptional - {h})
            a = sum(tuple(sorted((h, u))) in red for u in targets)
            expanded = a
            for u, v in it.combinations(targets, 2):
                x = int(tuple(sorted((h, u))) in red)
                y = int(tuple(sorted((h, v))) in red)
                expanded += 2 * ((1-x) * (1-y) + x + y - 1)
            require(expanded == a * a, "literal square identity")
            square_cases += 1
    for color in (0, 1):
        for inner_graph in range(1024):
            same_edge = any(((inner_graph >> bit) & 1) == color for bit in range(10))
            opposite_clique = all(((inner_graph >> bit) & 1) != color for bit in range(10))
            require(same_edge or opposite_clique, "T3 five-neighbor dichotomy")
            cap_cases += 1
    deficiency_patterns = 0
    for left in range(N):
        for right in range(left, N):
            excess = [0] * N
            excess[left] += 1
            excess[right] += 1
            values = [6 + value for value in excess]
            require(sum(values) == 260, "deficiency total")
            require(sum(value * value for value in values) == (1576 if left == right else 1574),
                    "deficiency endpoint")
            deficiency_patterns += 1
    require((d3_cases, j1_cases, cap_cases, square_cases, deficiency_patterns)
            == (245760, 20480, 2048, 5120, 946), "literal control census")
    return d3_cases, j1_cases, cap_cases, square_cases, deficiency_patterns


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--separator", type=Path)
    args = parser.parse_args()
    denominator, type_of, sizes, tables = load_certificate(args.certificate)
    distribution = physical_decoder(tables)
    triple, edge, triple_checks, edge_checks = low_marginals(
        denominator, sizes, distribution
    )
    d3_rows, t3_rows, t3_minimum = check_d3_t3(
        denominator, type_of, sizes, distribution, triple
    )
    j1_rows = check_j1(denominator, type_of, distribution, triple, edge)
    first, second, gap = check_global_moment(
        denominator, type_of, triple, edge, args.separator
    )
    controls = literal_controls()
    result = {
        "certificate_sha256": CERTIFICATE_SHA256,
        "deficiency_first_moment": str(first),
        "deficiency_gap": str(gap),
        "deficiency_second_moment": str(second),
        "edge_projection_checks": edge_checks,
        "four_tables": len(tables),
        "j1_rows": j1_rows,
        "literal_cap_cases": controls[2],
        "literal_d3_cases": controls[0],
        "literal_deficiency_patterns": controls[4],
        "literal_j1_cases": controls[1],
        "literal_square_cases": controls[3],
        "separator_sha256": SEPARATOR_SHA256,
        "separator_terms": 3666,
        "status": "PASS",
        "t3_minimum_slack": str(t3_minimum),
        "t3_rows": t3_rows,
        "triple_projection_checks": triple_checks,
        "d3_rows": d3_rows,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
