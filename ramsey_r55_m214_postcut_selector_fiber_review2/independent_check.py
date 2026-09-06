#!/usr/bin/env python3
"""Independent exact audit of Discovery Net h3531.

No module from the reviewed contribution or its producers is imported.  The
checker reconstructs the five probability tables, the 389-root coordinate
system, every inherited physical coordinate, the complete selector box test,
the P3/P4 moment layers, and the 83 anchor-interface equations.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path


F = Fraction
N = 43
E = frozenset(range(2, 15))
REMOVED = (48, 128, 129, 201, 202, 299, 300, 375, 376)
CAP = F(6, 13)
BASE_HASH = "9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609"
BASE_HEADER = b"* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64\n"
P4_PAIRS = tuple(combinations(range(4), 2))


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def edge_probability(types: tuple[int, int]) -> F:
    return (F(15, 29), F(6, 13), F(20, 39))[sum(types)]


def build_tables(parameters: dict[str, str]) -> tuple[tuple[F, ...], ...]:
    need(set(parameters) == {"u", "v", "t1", "t2"}, "parameter names")
    u, v, t1, t2 = (F(parameters[name]) for name in ("u", "v", "t1", "t2"))
    a, b, c = F(20, 39), F(6, 13), F(15, 29)
    two_red = {
        (1, 2): (19 * a - 30 * u) / 11,
        (1, 1): u,
        (1, 0): (19 * b - 12 * u) / 29,
        (0, 2): (20 * b - 29 * v) / 12,
        (0, 1): v,
        (0, 0): (20 * c - 13 * v) / 28,
    }
    triangle = {
        0: (100 - 78 * t2 - 377 * t1) / 406,
        1: t1,
        2: t2,
        3: (93 - 360 * t2 - 435 * t1) / 66,
    }
    result = []
    for exceptional_count in range(5):
        types = tuple(int(i < exceptional_count) for i in range(4))
        walsh: dict[int, F] = {0: F(1)}
        for bit, pair in enumerate(P4_PAIRS):
            walsh[1 << bit] = 1 - 2 * edge_probability((types[pair[0]], types[pair[1]]))
        for left, right in combinations(range(6), 2):
            common = set(P4_PAIRS[left]) & set(P4_PAIRS[right])
            if len(common) != 1:
                continue
            center = next(iter(common))
            leaves = (set(P4_PAIRS[left]) | set(P4_PAIRS[right])) - {center}
            joint = two_red[types[center], sum(types[x] for x in leaves)]
            p = edge_probability((types[P4_PAIRS[left][0]], types[P4_PAIRS[left][1]]))
            q = edge_probability((types[P4_PAIRS[right][0]], types[P4_PAIRS[right][1]]))
            walsh[(1 << left) | (1 << right)] = 1 - 2 * p - 2 * q + 4 * joint
        for vertices in combinations(range(4), 3):
            bits = tuple(P4_PAIRS.index(pair) for pair in combinations(vertices, 2))
            joints = 0
            for center in vertices:
                leaves = tuple(x for x in vertices if x != center)
                joints += two_red[types[center], sum(types[x] for x in leaves)]
            single_sum = sum(edge_probability((types[P4_PAIRS[x][0]], types[P4_PAIRS[x][1]]))
                             for x in bits)
            walsh[sum(1 << x for x in bits)] = 1 - 2 * single_sum + 4 * joints - 8 * triangle[sum(types[x] for x in vertices)]
        need(len(walsh) == 23, "Walsh support")
        atoms = tuple(sum(value * (-1 if (state & subset).bit_count() % 2 else 1)
                          for subset, value in walsh.items()) / 64 for state in range(64))
        need(min(atoms) > 0 and sum(atoms) == 1, "strict four-state probability")
        result.append(atoms)
    return tuple(result)


def project_four(distribution: tuple[int, ...], positions: tuple[int, ...]) -> tuple[int, ...]:
    selected = tuple(P4_PAIRS.index(pair) for pair in combinations(positions, 2))
    result = [0] * (1 << len(selected))
    for state, mass in enumerate(distribution):
        state_out = sum(((state >> source) & 1) << target for target, source in enumerate(selected))
        result[state_out] += mass
    return tuple(result)


def root_system():
    pattern_families = (("H", "A"), ("BB", "BO", "OO"), ("B", "O"),
                        ("BB", "BO", "OO"), ("HO", "AB"))
    roots = []
    for family, patterns in enumerate(pattern_families):
        for c in range(9, 14):
            for k in range(7):
                sizes = (k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k)
                cells, first = [], 2
                for size in sizes:
                    cells.append(tuple(range(first, first + size)))
                    first += size
                need(first == 43, "root partition")
                for pattern in patterns:
                    offset = 0 if family < 2 else 4
                    if any(pattern.count(label) > sizes[offset + j]
                           for j, label in enumerate("HABO")):
                        continue
                    core = tuple(sorted(cells[0] + cells[4]))
                    outside = tuple(v for v in range(2, N) if v not in core)
                    bits = {(0, 1): 1}
                    colors = ((1, 1), (1, 0), (0, 1), (0, 0))
                    for j, cell in enumerate(cells):
                        for vertex in cell:
                            bits[0, vertex], bits[1, vertex] = colors[j % 4]
                    roots.append(((family, c, k, pattern), core, outside, bits))
    need(len(roots) == 389, "389 roots")
    need(tuple(i for i, root in enumerate(roots) if root[0][1:3] == (13, 0)) == REMOVED,
         "nine root indices")
    missed, footprints = set(), set()
    for _, core, outside, _ in roots:
        for a, b in combinations(outside, 2):
            missed.update((a, b, h) for h in core)
            footprints.update((a, b, i, j) for i, j in combinations(core, 2))
    need((len(missed), len(footprints)) == (10612, 74513), "coordinate supports")
    return roots, tuple(sorted(missed)), tuple(sorted(footprints))


class ExactPoint:
    def __init__(self, tables: tuple[tuple[F, ...], ...], roots, missed, footprints):
        denominators = [value.denominator for row in tables for value in row]
        self.denominator = math.lcm(*denominators)
        self.tables = tuple(tuple(int(value * self.denominator) for value in row) for row in tables)
        self.roots = roots
        self.edge = {pair: i for i, pair in enumerate(combinations(range(N), 2), 1)}
        self.triangle = {triple: i for i, triple in enumerate(combinations(range(N), 3), 904)}
        self.missed = {key: i for i, key in enumerate(missed, 13634)}
        self.footprint = {key: i for i, key in enumerate(footprints, 24246)}
        self.values = [0] * 98759
        for pair, index in self.edge.items():
            self.values[index] = int(edge_probability(tuple(int(v in E) for v in pair)) * self.denominator)
        for triple, index in self.triangle.items():
            self.values[index] = self.triple_distribution(tuple(int(v in E) for v in triple))[7]
        for selector in range(389):
            self.values[13245 + selector] = 0
        for key, index in self.missed.items():
            self.values[index] = self.blue_wedge(key)
        for key, index in self.footprint.items():
            self.values[index] = self.footprint_mass(key)

    @lru_cache(maxsize=None)
    def four_distribution(self, types: tuple[int, int, int, int]) -> tuple[int, ...]:
        canonical_to_physical = tuple(sorted(range(4), key=lambda i: (-types[i], i)))
        base = self.tables[sum(types)]
        result = []
        for physical_state in range(64):
            canonical_state = 0
            for target, (a, b) in enumerate(P4_PAIRS):
                physical_pair = tuple(sorted((canonical_to_physical[a], canonical_to_physical[b])))
                source = P4_PAIRS.index(physical_pair)
                canonical_state |= ((physical_state >> source) & 1) << target
            result.append(base[canonical_state])
        return tuple(result)

    @lru_cache(maxsize=None)
    def triple_distribution(self, types: tuple[int, int, int]) -> tuple[int, ...]:
        return project_four(self.four_distribution(types + (0,)), (0, 1, 2))

    def blue_wedge(self, key: tuple[int, int, int]) -> int:
        a, b, center = key
        dist = self.triple_distribution(tuple(int(v in E) for v in (a, b, center)))
        return dist[0] + dist[1]

    def footprint_mass(self, key: tuple[int, int, int, int]) -> int:
        a, b, i, j = key
        dist = self.four_distribution(tuple(int(v in E) for v in key))
        red = 1 << P4_PAIRS.index((2, 3))
        blue = sum(1 << P4_PAIRS.index(pair) for pair in ((0, 2), (0, 3), (1, 2), (1, 3)))
        return sum(mass for state, mass in enumerate(dist) if state & red and not state & blue)


def check_certificate(source: Path, point: ExactPoint) -> dict:
    raw = json.loads((source / "certificate.json").read_text())
    need(raw["denominator"] == point.denominator == 2533440000, "certificate denominator")
    published = tuple(tuple(row["numerators"]) for row in raw["four_vertex_atoms"])
    need(published == point.tables, "independently reconstructed tables")
    minimum = min(min(row) for row in point.tables)
    need(F(minimum, point.denominator) == F(226211, 60320000), "minimum atom")
    return {"table_denominator": point.denominator,
            "table_sha256": sha256((source / "certificate.json").read_bytes()).hexdigest(),
            "minimum_four_mass": str(F(minimum, point.denominator))}


def check_base(opb: Path, point: ExactPoint) -> dict:
    digest = sha256()
    bytes_read = 0
    equality_count = 0
    selector_equalities = 0
    guard_roots = set()
    minimum = None
    upper = int(CAP * point.denominator)
    with opb.open("rb") as handle:
        header = next(handle)
        need(header == BASE_HEADER, "base header")
        digest.update(header)
        bytes_read += len(header)
        row_number = 0
        for row_number, raw_line in enumerate(handle, 1):
            digest.update(raw_line)
            bytes_read += len(raw_line)
            fields = raw_line.split()
            need(len(fields) >= 5 and len(fields) % 2 == 1 and fields[-1] == b";", "OPB syntax")
            relation = fields[-3]
            rhs = int(fields[-2])
            terms = {}
            physical_value = -rhs * point.denominator
            selectors = {}
            for offset in range(0, len(fields) - 3, 2):
                coefficient = int(fields[offset])
                token = fields[offset + 1]
                need(token.startswith(b"x"), "OPB variable")
                variable = int(token[1:])
                need(1 <= variable <= 98758 and variable not in terms, "OPB variable range/uniqueness")
                terms[variable] = coefficient
                if 13245 <= variable <= 13633:
                    selectors[variable] = coefficient
                else:
                    physical_value += coefficient * point.values[variable]
            if relation == b"=":
                equality_count += 1
                if selectors:
                    need(not any(v < 13245 or v > 13633 for v in terms), "mixed selector equality")
                    need(len(terms) == 389 and set(terms.values()) == {1} and rhs == 1,
                         "selector simplex equality")
                    selector_equalities += 1
                else:
                    need(physical_value == 0, f"physical equality row {row_number}")
                continue
            need(relation == b">=", "OPB relation")
            lower = physical_value + sum(coefficient * upper for coefficient in selectors.values()
                                         if coefficient < 0)
            need(lower >= 0, f"selector-box inequality row {row_number}")
            minimum = lower if minimum is None else min(minimum, lower)
            if terms.get(2) == 1 and len(terms) == 2 and rhs == 0:
                selector_terms = [(v, c) for v, c in terms.items() if 13245 <= v <= 13633]
                if len(selector_terms) == 1 and selector_terms[0][1] == -1:
                    guard_roots.add(selector_terms[0][0] - 13245)
    need((row_number, equality_count, selector_equalities) == (2983003, 87, 1), "base coverage")
    need(bytes_read == 511537255 and digest.hexdigest() == BASE_HASH, "base identity")
    need(guard_roots == set(range(389)), "sharp guard for every root")
    return {"base_rows": row_number, "base_equalities": equality_count,
            "base_sha256": digest.hexdigest(), "base_bytes": bytes_read,
            "base_box_minimum_slack": str(F(minimum, point.denominator)),
            "sharp_cap_guards": len(guard_roots)}


def check_global_moments(point: ExactPoint) -> dict:
    D = point.denominator
    red_codegree, blue_codegree = [], []
    blue_local = [0] * N
    all_wedges = {}
    triangle_atoms = 0
    for triple in combinations(range(N), 3):
        dist = point.triple_distribution(tuple(int(v in E) for v in triple))
        need(min(dist) >= 0 and sum(dist) == D, "triangle distribution")
        need(dist[7] == point.values[point.triangle[triple]], "triangle coordinate")
        for center in triple:
            leaves = tuple(v for v in triple if v != center)
            key = tuple(sorted(leaves)) + (center,)
            all_wedges[key] = point.blue_wedge(key)
            blue_local[center] += dist[0]
        triangle_atoms += 8
    for pair, edge_index in point.edge.items():
        red_total = sum(point.values[point.triangle[tuple(sorted(pair + (h,)))]]
                        for h in range(N) if h not in pair)
        red_codegree.append(13 * point.values[edge_index] - red_total)
        blue_total = 0
        for h in range(N):
            if h in pair:
                continue
            triple = tuple(sorted(pair + (h,)))
            blue_total += point.triple_distribution(tuple(int(v in E) for v in triple))[0]
        blue_codegree.append(13 * (D - point.values[edge_index]) - blue_total)
    need(min(red_codegree) >= 0 and min(blue_codegree) >= 0, "two-color codegrees")
    star_equalities = 0
    for center in range(N):
        degree = 20 if center in E else 21
        for a in range(N):
            if a == center:
                continue
            x = point.values[point.edge[tuple(sorted((a, center)))]]
            red_joint = blue_joint = 0
            for b in range(N):
                if b in (center, a):
                    continue
                key = tuple(sorted((a, b))) + (center,)
                m = all_wedges[key]
                blue_joint += m
                red_joint += m + x + point.values[point.edge[tuple(sorted((b, center)))]] - D
            need(red_joint == (degree - 1) * x, "red star equality")
            need(blue_joint == (41 - degree) * (D - x), "blue star equality")
            star_equalities += 1
    expected_blue = [F(1389, 13) if v in E else F(100) for v in range(N)]
    need([F(x, D) for x in blue_local] == expected_blue, "blue local totals")
    return {"triangle_atom_rows": triangle_atoms, "global_star_equalities": star_equalities,
            "red_codegree_minimum": str(F(min(red_codegree), D)),
            "blue_codegree_minimum": str(F(min(blue_codegree), D)),
            "blue_totals": ["1389/13", "100"]}


def check_root_suffix(point: ExactPoint) -> dict:
    D = point.denominator
    upper = int(CAP * D)
    coupled = facets = 0
    coupled_min = hull_min = None
    for _, core, outside, _ in point.roots:
        c = len(core)
        outside_pairs = math.comb(len(outside), 2)
        for i, j in combinations(core, 2):
            degree_sum = (20 if i in E else 21) + (20 if j in E else 21)
            K = 64 - c - degree_sum
            edge_value = point.values[point.edge[i, j]]
            Q = sum(point.values[point.footprint[a, b, i, j]] for a, b in combinations(outside, 2))
            A = sum(point.values[point.edge[tuple(sorted((h, w)))]]
                    for h in (i, j) for w in core if h != w)
            T = sum(point.values[point.triangle[tuple(sorted((i, j, w)))]] for w in outside)
            constant = 45 - c - degree_sum
            S = constant * D + A + T
            B = math.comb(K, 2)
            gap = B * edge_value + (outside_pairs - B) * (D - upper) - Q
            need(gap >= 0, "coupled column")
            cap = F(B * edge_value + (outside_pairs - B) * D - Q,
                    (outside_pairs - B) * D)
            coupled_min = cap if coupled_min is None else min(coupled_min, cap)
            coupled += 1
            for tangent in range(K):
                guard = tangent * constant - math.comb(tangent + 1, 2) + tangent * (c + 39)
                need(guard >= 0, "lower hull guard")
                intercept = Q - tangent * S + math.comb(tangent + 1, 2) * D + guard * (2 * D - edge_value)
                need(intercept - guard * upper >= 0, "lower hull facet")
                if guard:
                    candidate = F(intercept, guard * D)
                    hull_min = candidate if hull_min is None else min(hull_min, candidate)
                facets += 1
            guard = -(K - 1) * constant + 2 * outside_pairs
            need(guard > 0, "upper hull guard")
            intercept = (K - 1) * S - 2 * Q + guard * (2 * D - edge_value)
            need(intercept - guard * upper >= 0, "upper hull facet")
            candidate = F(intercept, guard * D)
            hull_min = candidate if hull_min is None else min(hull_min, candidate)
            facets += 1
    need((coupled, facets) == (21762, 264560), "root suffix coverage")
    return {"coupled_rows": coupled, "hull_rows": facets,
            "minimum_coupled_cap": str(coupled_min), "minimum_hull_cap": str(hull_min)}


def check_four_layer(point: ExactPoint) -> dict:
    D = point.denominator
    projections = 0
    for types in product((0, 1), repeat=4):
        dist = point.four_distribution(types)
        need(min(dist) >= 0 and sum(dist) == D, "four distribution")
        for positions in combinations(range(4), 3):
            expected = point.triple_distribution(tuple(types[i] for i in positions))
            need(project_four(dist, positions) == expected, "four-to-three marginal")
            projections += 8
    transports = 0
    for q, base in enumerate(point.tables):
        types = tuple(int(i < q) for i in range(4))
        for permutation in permutations(range(4)):
            permuted_types = tuple(types[i] for i in permutation)
            dist = point.four_distribution(permuted_types)
            for state, mass in enumerate(base):
                # permutation[new vertex] is its old vertex, so every new
                # edge bit pulls back from the corresponding old edge bit.
                target = 0
                for new_bit, pair in enumerate(P4_PAIRS):
                    old_pair = tuple(sorted((permutation[pair[0]], permutation[pair[1]])))
                    old_bit = P4_PAIRS.index(old_pair)
                    target |= ((state >> old_bit) & 1) << new_bit
                need(dist[target] == mass, "four-state physical transport")
                transports += 1
    for key, index in point.footprint.items():
        need(point.values[index] == point.footprint_mass(key), "footprint projection")
    census = [math.comb(13, q) * math.comb(30, 4-q) for q in range(5)]
    need(sum(census) == 123410 and transports == 5 * 24 * 64, "P4 coverage counts")
    return {"four_sets": sum(census), "type_projection_rows": projections,
            "physical_state_transports": transports, "footprint_equalities": len(point.footprint),
            "four_nonnegative_rows": 64 * sum(census),
            "triangle_marginal_equalities": 32 * sum(census), "four_set_census": census}


def parse_links(path: Path, point: ExactPoint) -> dict:
    anchor_edges = tuple(sorted(point.roots[0][3]))
    need(len(anchor_edges) == 83, "anchor domain")
    lines = path.read_text().splitlines()
    need(len(lines) == 83, "83 linkage rows")
    remaining = [r for r in range(389) if r not in REMOVED]
    violations = 0
    for pair, line in zip(anchor_edges, lines):
        fields = line.split()
        need(fields[-3:] == ["=", "0", ";"], "link syntax")
        terms = {int(fields[i + 1][1:]): int(fields[i]) for i in range(0, len(fields) - 3, 2)}
        expected = {point.edge[pair]: 1}
        expected.update({13245 + r: -1 for r, root in enumerate(point.roots) if root[3][pair]})
        need(terms == expected, "literal link coefficients")
        actual = F(point.values[point.edge[pair]], point.denominator)
        predicted = sum(F(1, 380) for r in remaining if point.roots[r][3][pair])
        violations += actual != predicted
    common_all = set(point.roots[0][3].items())
    for root in point.roots[1:]:
        common_all &= set(root[3].items())
    common_remaining = set(point.roots[remaining[0]][3].items())
    for r in remaining[1:]:
        common_remaining &= set(point.roots[r][3].items())
    need((len(common_all), len(common_remaining), violations) == (51, 53, 83), "anchor intersections")
    need(all(root[3][0, 2] == 1 for root in point.roots), "common separating unit")
    return {"anchor_rows": len(lines), "anchor_link_sha256": sha256(path.read_bytes()).hexdigest(),
            "uniform_link_violations": violations, "common_units_all": len(common_all),
            "common_units_after_cuts": len(common_remaining)}


def check_integer_separator(source: Path, point: ExactPoint) -> dict:
    certificate = json.loads((source / "anchor_cg.json").read_text())
    need(certificate["edge"] == [0, 2] and certificate["physical_variable"] == 2,
         "CG target edge")
    multiplier = F(certificate["each_guard_multiplier"])
    equality_multiplier = F(certificate["selector_equality_multiplier"])
    need(multiplier == equality_multiplier == F(1, 389), "CG multipliers")
    coefficients = Counter({2: 389 * multiplier})
    for r in range(389):
        coefficients[13245 + r] -= multiplier
        coefficients[13245 + r] += equality_multiplier
    need({k: v for k, v in coefficients.items() if v} == {2: F(1)}, "CG cancellation")
    need(math.ceil(F(1, 389)) == certificate["rounded_rhs"] == 1, "CG rounding")
    need(F(point.values[2], point.denominator) == CAP, "separating point value")
    need(2 * CAP < 1 and F(1, 3) <= CAP, "three-selector threshold")
    return {"selector_cap": str(CAP), "minimum_available_selectors": 3,
            "cg_pre_round_rhs": "1/389", "cg_rounded_rhs": 1,
            "family_separation_gap": str(1 - CAP)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--opb", type=Path, required=True)
    parser.add_argument("--links", type=Path, required=True)
    args = parser.parse_args()
    parameters = json.loads((args.source / "parameters.json").read_text())
    tables = build_tables(parameters)
    roots, missed, footprints = root_system()
    point = ExactPoint(tables, roots, missed, footprints)
    result = {
        "status": "INDEPENDENT_H3531_EXACT_SELECTOR_FIBER_PASS",
        **check_certificate(args.source, point),
        **check_base(args.opb, point),
        **check_global_moments(point),
        **check_root_suffix(point),
        **check_four_layer(point),
        **parse_links(args.links, point),
        **check_integer_separator(args.source, point),
        "roots": len(roots),
        "removed_roots": list(REMOVED),
        "retained_roots": 380,
        "inherited_not_reproved": [
            "Ramsey completeness of the 389-root normalization",
            "mathematical completeness of the predecessor P4 row families",
            "validity of the nine Boolean-root exclusions",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
