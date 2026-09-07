#!/usr/bin/env python3
"""Independent exact audit of the h3665 incident-moment PSD certificate.

No target module is imported. Canonical four-vertex tables are transported to
numeric physical edge sets, all lower-marginal extensions are checked, and all
claimed moment entries are reconstructed. PSD is certified by exact positive
rank-one subtraction, not the submitted cell-contrast or Bareiss algorithms.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement, permutations
import json
import math
from pathlib import Path


N = 43
E = tuple(range(2, 15))
PAIRS4 = tuple(combinations(range(4), 2))
CERTIFICATE_SHA256 = "79c6c330bd4f1f786a23d9b0a7dd372fb5026effba4ff226f0e1b9a0115a1905"
MIXED_ROW_SHA256 = "4abab593b6942f7b25809d4c26c8c6a9dbe4bb6fbb1cd7ac65d42989807971e7"
EXPECTED_CELLS = (
    (0,),
    (1,),
    tuple(range(2, 8)),
    tuple(range(8, 14)),
    (14,),
    tuple(range(15, 27)),
    (27, 28),
    (29, 30),
    tuple(range(31, 43)),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for bit, (left, right) in enumerate(PAIRS4):
        if mask & (1 << bit):
            image = tuple(sorted((permutation[left], permutation[right])))
            result |= 1 << PAIRS4.index(image)
    return result


class PhysicalTables:
    def __init__(self, certificate: Path) -> None:
        payload = certificate.read_bytes()
        require(
            hashlib.sha256(payload).hexdigest() == CERTIFICATE_SHA256,
            "unexpected certificate hash",
        )
        raw = json.loads(payload)
        require(
            set(raw)
            == {"format", "denominator", "cells", "active_selectors", "four_tables"},
            "certificate schema",
        )
        require(raw["format"] == "class-state-orbits-v1", "certificate format")
        self.denominator = raw["denominator"]
        require(
            type(self.denominator) is int
            and self.denominator > 0
            and len(str(self.denominator)) == 214,
            "positive 214-digit denominator",
        )
        self.cells = tuple(tuple(cell) for cell in raw["cells"])
        require(self.cells == EXPECTED_CELLS, "stated physical cells")
        require(raw["active_selectors"] == [278], "sole active selector")
        self.vertex_class = {
            vertex: kind for kind, cell in enumerate(self.cells) for vertex in cell
        }

        sizes = tuple(map(len, self.cells))
        self.tables: dict[tuple[int, ...], tuple[int, ...]] = {}
        positive_orbits = 0
        for record in raw["four_tables"]:
            require(set(record) == {"types", "orbits"}, "four-table schema")
            types = tuple(record["types"])
            require(types == tuple(sorted(types)) and len(types) == 4, "canonical types")
            require(types not in self.tables, "duplicate table")
            require(
                all(0 <= kind < len(sizes) for kind in types)
                and all(types.count(kind) <= sizes[kind] for kind in set(types)),
                "feasible type multiset",
            )
            stabilizer = tuple(
                permutation
                for permutation in permutations(range(4))
                if all(
                    types[position] == types[permutation[position]]
                    for position in range(4)
                )
            )
            distribution: list[int | None] = [None] * 64
            for text, mass in record["orbits"].items():
                representative = int(text)
                require(
                    str(representative) == text
                    and 0 <= representative < 64
                    and type(mass) is int
                    and 0 < mass <= self.denominator,
                    "positive orbit mass",
                )
                orbit = {permute_mask(representative, p) for p in stabilizer}
                require(representative == min(orbit), "noncanonical orbit representative")
                require(
                    all(distribution[state] is None for state in orbit),
                    "overlapping state orbits",
                )
                for state in orbit:
                    distribution[state] = mass
                positive_orbits += 1
            completed = tuple(0 if mass is None else mass for mass in distribution)
            require(sum(completed) == self.denominator, "table normalization")
            self.tables[types] = completed

        expected = {
            types
            for types in combinations_with_replacement(range(len(sizes)), 4)
            if all(types.count(kind) <= sizes[kind] for kind in set(types))
        }
        require(set(self.tables) == expected, "complete feasible type support")
        require((len(self.tables), positive_orbits) == (345, 7774), "table/orbit census")
        self.positive_orbits = positive_orbits
        self._four_cache: dict[tuple[int, ...], tuple[int, ...]] = {}

    def physical_four(self, vertices: tuple[int, ...]) -> tuple[int, ...]:
        """Distribution in numeric-vertex edge order for one physical 4-set."""
        vertices = tuple(sorted(vertices))
        require(len(vertices) == 4 and len(set(vertices)) == 4, "physical four-set")
        if vertices in self._four_cache:
            return self._four_cache[vertices]
        ordered = tuple(sorted(vertices, key=lambda v: (self.vertex_class[v], v)))
        canonical = self.tables[tuple(self.vertex_class[v] for v in ordered)]
        physical_pairs = tuple(combinations(vertices, 2))
        transported = [0] * 64
        for physical_state in range(64):
            canonical_state = 0
            for bit, (left, right) in enumerate(PAIRS4):
                physical_edge = tuple(sorted((ordered[left], ordered[right])))
                source_bit = physical_pairs.index(physical_edge)
                canonical_state |= ((physical_state >> source_bit) & 1) << bit
            transported[physical_state] = canonical[canonical_state]
        result = tuple(transported)
        require(sum(result) == self.denominator, "transported normalization")
        self._four_cache[vertices] = result
        return result

    def three_distribution(
        self, triple: tuple[int, ...], filler: int
    ) -> tuple[int, ...]:
        triple = tuple(sorted(triple))
        require(len(triple) == 3 and filler not in triple, "triple extension")
        vertices = tuple(sorted(triple + (filler,)))
        distribution = self.physical_four(vertices)
        four_pairs = tuple(combinations(vertices, 2))
        positions = tuple(four_pairs.index(edge) for edge in combinations(triple, 2))
        projected = [0] * 8
        for state, mass in enumerate(distribution):
            small_state = sum(
                ((state >> source) & 1) << bit
                for bit, source in enumerate(positions)
            )
            projected[small_state] += mass
        return tuple(projected)


def all_lower_marginals(tables: PhysicalTables):
    triples: dict[tuple[int, ...], tuple[int, ...]] = {}
    triple_checks = 0
    for triple in combinations(range(N), 3):
        fillers = [vertex for vertex in range(N) if vertex not in triple]
        baseline = tables.three_distribution(triple, fillers[0])
        require(sum(baseline) == tables.denominator, "triple normalization")
        for filler in fillers[1:]:
            require(
                tables.three_distribution(triple, filler) == baseline,
                "inconsistent triple extension",
            )
            triple_checks += 1
        triples[triple] = baseline

    edges: dict[tuple[int, int], int] = {}
    edge_checks = 0
    for edge in combinations(range(N), 2):
        baseline = None
        for third in range(N):
            if third in edge:
                continue
            triple = tuple(sorted(edge + (third,)))
            bit = tuple(combinations(triple, 2)).index(edge)
            value = sum(
                mass
                for state, mass in enumerate(triples[triple])
                if state & (1 << bit)
            )
            if baseline is None:
                baseline = value
            else:
                require(value == baseline, "inconsistent edge extension")
                edge_checks += 1
        require(baseline is not None, "edge extension exists")
        edges[edge] = baseline

    require(triple_checks == math.comb(N, 3) * 39, "triple extension census")
    require(edge_checks == math.comb(N, 2) * 40, "edge extension census")
    return triples, edges, triple_checks, edge_checks


def red_product(tables, triples, edges, first, second) -> int:
    if first == second:
        return edges[first]
    vertices = tuple(sorted(set(first + second)))
    require(len(vertices) in (3, 4), "two-edge support")
    physical_pairs = tuple(combinations(vertices, 2))
    mask = (1 << physical_pairs.index(first)) | (1 << physical_pairs.index(second))
    distribution = (
        triples[vertices] if len(vertices) == 3 else tables.physical_four(vertices)
    )
    return sum(
        mass for state, mass in enumerate(distribution) if state & mask == mask
    )


def positive_outer_rank(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Certify A=sum c c^T/d with d>0 by exact residual subtraction."""
    order = len(matrix)
    require(order and all(len(row) == order for row in matrix), "square matrix")
    require(
        all(matrix[i][j] == matrix[j][i] for i in range(order) for j in range(order)),
        "symmetric matrix",
    )
    original = [[Fraction(value) for value in row] for row in matrix]
    residual = [row[:] for row in original]
    pieces: list[tuple[tuple[Fraction, ...], Fraction]] = []
    while True:
        require(all(residual[i][i] >= 0 for i in range(order)), "negative residual diagonal")
        pivot_index = next(
            (i for i in range(order) if residual[i][i] > 0), None
        )
        if pivot_index is None:
            require(
                all(residual[i][j] == 0 for i in range(order) for j in range(order)),
                "nonzero residual with zero diagonal",
            )
            break
        pivot = residual[pivot_index][pivot_index]
        column = tuple(residual[i][pivot_index] for i in range(order))
        for i in range(order):
            for j in range(i, order):
                residual[i][j] -= column[i] * column[j] / pivot
                residual[j][i] = residual[i][j]
        require(
            all(residual[pivot_index][j] == 0 for j in range(order)),
            "pivot row elimination",
        )
        pieces.append((column, pivot))

    require(
        all(
            original[i][j]
            == sum(column[i] * column[j] / pivot for column, pivot in pieces)
            for i in range(order)
            for j in range(order)
        ),
        "outer decomposition reconstruction",
    )
    return len(pieces)


def psd_self_tests() -> int:
    positive = (
        (((0,),), 0),
        (((1, 2), (2, 4)), 1),
        (((0, 0, 0), (0, 2, 1), (0, 1, 2)), 2),
        (((2, 1, 0), (1, 2, 1), (0, 1, 2)), 3),
    )
    for matrix, rank in positive:
        require(positive_outer_rank(matrix) == rank, "known PSD rank")
    rejected = 0
    for matrix in (
        ((1, 2), (2, 1)),
        ((0, 1), (1, 0)),
        ((-1,),),
        ((1, 0), (1, 1)),
    ):
        try:
            positive_outer_rank(matrix)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid PSD matrix accepted")
    require(rejected == 4, "PSD rejection controls")
    return len(positive) + rejected


def incident_matrices(tables, triples, edges):
    matrices = []
    physical_entries = 0
    for center in range(N):
        star = tuple(
            tuple(sorted((center, vertex)))
            for vertex in range(N)
            if vertex != center
        )
        means = [edges[edge] for edge in star]
        matrix = [[tables.denominator] + means]
        for i, first in enumerate(star):
            matrix.append(
                [means[i]]
                + [
                    red_product(tables, triples, edges, first, second)
                    for second in star
                ]
            )
        require(
            all(matrix[i][j] == matrix[j][i] for i in range(43) for j in range(43)),
            "physical incident symmetry",
        )
        matrices.append(tuple(map(tuple, matrix)))
        physical_entries += 43 * 43

    distinct = {}
    for matrix in matrices:
        if matrix not in distinct:
            distinct[matrix] = positive_outer_rank(matrix)
    ranks = [distinct[matrix] for matrix in matrices]
    require(len(distinct) == 9, "distinct incident matrices")
    require(ranks == [1, 1] + [39] * 41, "all incident ranks")
    require(physical_entries == 79507, "incident entry census")
    return ranks, len(distinct), physical_entries


def neighbor_matrix(tables, triples, edges):
    incident = {
        h: tuple(tuple(sorted((h, u))) for u in E if u != h)
        for h in range(N)
    }
    means = [sum(edges[edge] for edge in incident[h]) for h in range(N)]
    matrix = [[0] * 44 for _ in range(44)]
    matrix[0][0] = tables.denominator
    for h in range(N):
        matrix[0][h + 1] = matrix[h + 1][0] = means[h]
    for h in range(N):
        for k in range(N):
            matrix[h + 1][k + 1] = sum(
                red_product(tables, triples, edges, first, second)
                for first in incident[h]
                for second in incident[k]
            )
    factor = [1] + [7 if h in (29, 30) else 6 for h in range(N)]
    require(
        all(
            matrix[i][j] == tables.denominator * factor[i] * factor[j]
            for i in range(44)
            for j in range(44)
        ),
        "neighbor matrix factor",
    )
    return matrix, factor


def edge_sum_moments(tables, triples, edges, weighted_edges):
    mean = sum(weight * edges[edge] for edge, weight in weighted_edges)
    second = sum(
        first_weight
        * second_weight
        * red_product(tables, triples, edges, first, second)
        for first, first_weight in weighted_edges
        for second, second_weight in weighted_edges
    )
    return mean, second


def subset_rank(vertices: tuple[int, ...], n: int) -> int:
    require(tuple(sorted(set(vertices))) == vertices, "canonical subset")
    rank = 0
    previous = -1
    size = len(vertices)
    for position, vertex in enumerate(vertices):
        rank += sum(
            math.comb(n - candidate - 1, size - position - 1)
            for candidate in range(previous + 1, vertex)
        )
        previous = vertex
    return rank


def wedge_numbering():
    inherited = set()
    root_count = 0
    families = (
        ("H", "A"),
        ("BB", "BO", "OO"),
        ("B", "O"),
        ("BB", "BO", "OO"),
        ("HO", "AB"),
    )
    for family, patterns in enumerate(families):
        for c in range(9, 14):
            for k in range(7):
                sizes = (k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k)
                cells = []
                first = 2
                for size in sizes:
                    cells.append(tuple(range(first, first + size)))
                    first += size
                for pattern in patterns:
                    offset = 0 if family < 2 else 4
                    if any(
                        pattern.count(label) > sizes[offset + j]
                        for j, label in enumerate("HABO")
                    ):
                        continue
                    root_count += 1
                    core = set(cells[0] + cells[4])
                    outside = tuple(v for v in range(2, N) if v not in core)
                    inherited.update(
                        (u, v, h)
                        for u, v in combinations(outside, 2)
                        for h in core
                    )
    require((root_count, len(inherited)) == (389, 10612), "root/wedge support")
    names = {key: 13634 + i for i, key in enumerate(sorted(inherited))}
    all_keys = tuple(
        (u, v, h)
        for u, v in combinations(range(N), 2)
        for h in range(N)
        if h not in (u, v)
    )
    missing = [key for key in all_keys if key not in names]
    names.update({key: 98759 + i for i, key in enumerate(sorted(missing))})
    require(len(names) == 37023 and max(names.values()) == 125169, "wedge numbering")
    return names


def blue_wedge(triples, u: int, v: int, center: int) -> int:
    triple = tuple(sorted((u, v, center)))
    physical_pairs = tuple(combinations(triple, 2))
    incident = (
        tuple(sorted((u, center))),
        tuple(sorted((v, center))),
    )
    mask = (1 << physical_pairs.index(incident[0])) | (
        1 << physical_pairs.index(incident[1])
    )
    return sum(
        mass for state, mass in enumerate(triples[triple]) if state & mask == 0
    )


def reconstruct_mixed_row(tables, triples, edges, path: Path):
    edge_names = {edge: i for i, edge in enumerate(combinations(range(N), 2), 1)}
    wedge_names = wedge_numbering()
    weights = {tuple(sorted((29, u))): 2 for u in E}
    weights[(2, 8)] = 1
    coefficients = Counter()
    values = {}
    constant = 196
    for edge, weight in weights.items():
        coefficients[edge_names[edge]] += weight * weight - 28 * weight
        values[edge_names[edge]] = edges[edge]
    for (first, first_weight), (second, second_weight) in combinations(
        weights.items(), 2
    ):
        coefficient = 2 * first_weight * second_weight
        common = set(first) & set(second)
        if common:
            center = next(iter(common))
            u, v = sorted((set(first) | set(second)) - {center})
            coefficients[wedge_names[u, v, center]] += coefficient
            coefficients[edge_names[first]] += coefficient
            coefficients[edge_names[second]] += coefficient
            values[wedge_names[u, v, center]] = blue_wedge(triples, u, v, center)
            constant -= coefficient
        else:
            vertices = tuple(sorted(first + second))
            physical_pairs = tuple(combinations(vertices, 2))
            required = (1 << physical_pairs.index(first)) | (
                1 << physical_pairs.index(second)
            )
            start = 125170 + 64 * subset_rank(vertices, N)
            distribution = tables.physical_four(vertices)
            for state, mass in enumerate(distribution):
                if state & required == required:
                    coefficients[start + state] += coefficient
                    values[start + state] = mass

    coefficients = Counter(
        {index: coefficient for index, coefficient in coefficients.items() if coefficient}
    )
    require(constant == -436 and len(coefficients) == 270, "mixed row support")
    require(
        Counter(coefficients.values())
        == Counter({44: 11, 48: 2, -19: 1, 8: 78, 4: 178}),
        "mixed row coefficient histogram",
    )
    row = (
        " ".join(
            f"{coefficient:+d} x{index}"
            for index, coefficient in sorted(coefficients.items())
        )
        + " >= 436 ;\n"
    ).encode()
    require(hashlib.sha256(row).hexdigest() == MIXED_ROW_SHA256, "mixed row hash")
    require(path.read_bytes() == row, "submitted mixed row differs")
    value = constant * tables.denominator + sum(
        coefficient * values[index] for index, coefficient in coefficients.items()
    )
    return weights, coefficients, value


def mixed_truth_table() -> int:
    weights = {tuple(sorted((29, u))): 2 for u in E}
    weights[(2, 8)] = 1
    support = tuple(weights)
    cases = 0
    for assignment in range(1 << len(support)):
        red = {
            edge
            for bit, edge in enumerate(support)
            if assignment & (1 << bit)
        }
        direct = (
            sum(weight * int(edge in red) for edge, weight in weights.items()) - 14
        ) ** 2
        expanded = 196 + sum(
            (weight * weight - 28 * weight) * int(edge in red)
            for edge, weight in weights.items()
        )
        for (first, first_weight), (second, second_weight) in combinations(
            weights.items(), 2
        ):
            coefficient = 2 * first_weight * second_weight
            if set(first) & set(second):
                center = next(iter(set(first) & set(second)))
                u, v = sorted((set(first) | set(second)) - {center})
                wedge = int(
                    tuple(sorted((u, center))) not in red
                    and tuple(sorted((v, center))) not in red
                )
                expanded += coefficient * (
                    wedge + int(first in red) + int(second in red) - 1
                )
            else:
                expanded += coefficient * int(first in red and second in red)
        require(expanded == direct and direct >= 0, "mixed Boolean identity")
        cases += 1
    require(cases == 16384, "mixed truth-table census")
    return cases


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", required=True, type=Path)
    parser.add_argument("--mixed-row", required=True, type=Path)
    args = parser.parse_args()

    psd_cases = psd_self_tests()
    tables = PhysicalTables(args.certificate)
    triples, edges, triple_checks, edge_checks = all_lower_marginals(tables)
    incident_ranks, distinct_incident, incident_entries = incident_matrices(
        tables, triples, edges
    )
    neighbor, factor = neighbor_matrix(tables, triples, edges)
    require(positive_outer_rank(tuple(map(tuple, neighbor))) == 1, "neighbor PSD rank")

    old_star = [(tuple(sorted((2, u))), 1) for u in tuple(range(3, 15)) + (29,)]
    old_mean, old_second = edge_sum_moments(tables, triples, edges, old_star)
    old_square = old_second - 12 * old_mean + 36 * tables.denominator
    require(old_square >= 0, "former star square repaired")

    weights, coefficients, row_value = reconstruct_mixed_row(
        tables, triples, edges, args.mixed_row
    )
    mixed_mean, mixed_second = edge_sum_moments(
        tables, triples, edges, tuple(weights.items())
    )
    mixed_square = mixed_second - 28 * mixed_mean + 196 * tables.denominator
    require(row_value == mixed_square, "row value equals direct mixed moment")
    require(30 * mixed_square < -tables.denominator, "strict -1/30 separation")
    truth_cases = mixed_truth_table()

    result = {
        "active_selector": 278,
        "certificate_sha256": CERTIFICATE_SHA256,
        "distinct_incident_matrices": distinct_incident,
        "edge_extension_checks": edge_checks,
        "four_tables": len(tables.tables),
        "incident_matrix_order": 43,
        "incident_ordered_entries": incident_entries,
        "incident_ranks": incident_ranks,
        "mixed_mean": str(Fraction(mixed_mean, tables.denominator)),
        "mixed_row_sha256": MIXED_ROW_SHA256,
        "mixed_row_terms": len(coefficients),
        "mixed_second_moment": str(Fraction(mixed_second, tables.denominator)),
        "mixed_square": str(Fraction(mixed_square, tables.denominator)),
        "mixed_truth_table_cases": truth_cases,
        "neighbor_factor": factor,
        "neighbor_matrix_order": 44,
        "neighbor_rank": 1,
        "old_star_mean": str(Fraction(old_mean, tables.denominator)),
        "old_star_second_moment": str(Fraction(old_second, tables.denominator)),
        "old_star_square": str(Fraction(old_square, tables.denominator)),
        "positive_orbits": tables.positive_orbits,
        "psd_algorithm_controls": psd_cases,
        "status": "INDEPENDENT_INCIDENT_MOMENT_PSD_REVIEW_PASS",
        "triple_extension_checks": triple_checks,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
