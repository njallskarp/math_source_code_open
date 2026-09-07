#!/usr/bin/env python3
"""Independent physical-edge audit of the h3645 M214 moment certificate.

This checker imports no producer or target-checker module.  It decodes the
canonical four-vertex tables as exact distributions on physical edge sets,
checks every lower-marginal extension, reconstructs all 1,936 entries of the
44 by 44 neighbor moment matrix, and derives the 91-term square row directly
from unordered physical-edge pairs.
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
H = tuple(range(15, 27))
CENTER = 2
B = tuple(range(3, 15)) + (29,)
PAIRS4 = tuple(combinations(range(4), 2))
CERTIFICATE_SHA256 = "26c296d8bfd35eaa5211e39d458d3ce65436dd621cd4ba4fba57f1b0a89dacfe"
SQUARE_SHA256 = "11c964928bd4199c5101bf1bbb5e73380c4236f828ebc191f52b8923ce2e6572"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    out = 0
    for bit, (left, right) in enumerate(PAIRS4):
        if mask & (1 << bit):
            image = tuple(sorted((permutation[left], permutation[right])))
            out |= 1 << PAIRS4.index(image)
    return out


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
            "certificate fields",
        )
        require(raw["format"] == "class-state-orbits-v1", "certificate format")
        self.denominator = raw["denominator"]
        require(
            type(self.denominator) is int and self.denominator > 0,
            "positive integer denominator",
        )
        self.cells = raw["cells"]
        require(all(type(cell) is list and cell for cell in self.cells), "nonempty cells")
        require(
            sorted(vertex for cell in self.cells for vertex in cell) == list(range(N)),
            "physical vertex partition",
        )
        require(raw["active_selectors"] == [278], "active root")
        self.vertex_class = {
            vertex: kind
            for kind, cell in enumerate(self.cells)
            for vertex in cell
        }

        sizes = tuple(map(len, self.cells))
        self.tables: dict[tuple[int, ...], tuple[int, ...]] = {}
        positive_orbits = 0
        for record in raw["four_tables"]:
            require(set(record) == {"types", "orbits"}, "four-table fields")
            types = tuple(record["types"])
            require(types == tuple(sorted(types)) and len(types) == 4, "canonical types")
            require(types not in self.tables, "duplicate four-table")
            require(all(0 <= kind < len(sizes) for kind in types), "class range")
            require(
                all(types.count(kind) <= sizes[kind] for kind in set(types)),
                "class multiplicity",
            )
            stabilizer = tuple(
                permutation
                for permutation in permutations(range(4))
                if all(types[position] == types[permutation[position]] for position in range(4))
            )
            distribution: list[int | None] = [None] * 64
            for text, mass in record["orbits"].items():
                require(type(mass) is int and 0 < mass <= self.denominator, "orbit mass")
                representative = int(text)
                require(
                    str(representative) == text and 0 <= representative < 64,
                    "orbit representative",
                )
                orbit = {permute_mask(representative, p) for p in stabilizer}
                require(representative == min(orbit), "nonminimal orbit representative")
                require(
                    all(distribution[state] is None for state in orbit),
                    "overlapping orbits",
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
        require(set(self.tables) == expected, "incomplete four-table support")
        require((len(self.tables), positive_orbits) == (345, 4250), "table/orbit census")
        self.positive_orbits = positive_orbits
        self._physical_four_cache: dict[tuple[int, ...], tuple[int, ...]] = {}

    def physical_four(self, vertices: tuple[int, ...]) -> tuple[int, ...]:
        """Return the table in numeric-vertex edge order for one physical 4-set."""
        vertices = tuple(sorted(vertices))
        require(len(vertices) == 4 and len(set(vertices)) == 4, "physical four-set")
        if vertices in self._physical_four_cache:
            return self._physical_four_cache[vertices]
        ordered = tuple(sorted(vertices, key=lambda v: (self.vertex_class[v], v)))
        canonical = self.tables[tuple(self.vertex_class[v] for v in ordered)]
        physical_pairs = tuple(combinations(vertices, 2))
        transported = [0] * 64
        for physical_state in range(64):
            canonical_state = 0
            for bit, (left, right) in enumerate(PAIRS4):
                edge = tuple(sorted((ordered[left], ordered[right])))
                source_bit = physical_pairs.index(edge)
                canonical_state |= ((physical_state >> source_bit) & 1) << bit
            transported[physical_state] = canonical[canonical_state]
        result = tuple(transported)
        require(sum(result) == self.denominator, "transported normalization")
        self._physical_four_cache[vertices] = result
        return result

    def three_distribution(
        self, triple: tuple[int, ...], filler: int
    ) -> tuple[int, ...]:
        triple = tuple(sorted(triple))
        require(filler not in triple, "distinct filler")
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
    """Check every physical triple and edge against every possible extension."""
    triples: dict[tuple[int, ...], tuple[int, ...]] = {}
    triple_extension_checks = 0
    for triple in combinations(range(N), 3):
        fillers = [vertex for vertex in range(N) if vertex not in triple]
        baseline = tables.three_distribution(triple, fillers[0])
        require(sum(baseline) == tables.denominator, "triple normalization")
        for filler in fillers[1:]:
            require(
                tables.three_distribution(triple, filler) == baseline,
                "inconsistent triple marginal",
            )
            triple_extension_checks += 1
        triples[triple] = baseline

    edges: dict[tuple[int, int], int] = {}
    edge_extension_checks = 0
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
                require(value == baseline, "inconsistent edge marginal")
                edge_extension_checks += 1
        require(baseline is not None, "edge extension")
        edges[edge] = baseline

    require(
        triple_extension_checks == math.comb(N, 3) * 39,
        "triple extension census",
    )
    require(edge_extension_checks == math.comb(N, 2) * 40, "edge extension census")
    return triples, edges, triple_extension_checks, edge_extension_checks


def joint_red(tables: PhysicalTables, triples, first, second) -> int:
    if first == second:
        raise ValueError("joint_red expects distinct edges")
    vertices = tuple(sorted(set(first + second)))
    require(len(vertices) in (3, 4), "edge-pair support")
    pairs = tuple(combinations(vertices, 2))
    mask = (1 << pairs.index(first)) | (1 << pairs.index(second))
    distribution = triples[vertices] if len(vertices) == 3 else tables.physical_four(vertices)
    return sum(mass for state, mass in enumerate(distribution) if state & mask == mask)


def blue_wedge(triples, u: int, v: int, h: int) -> int:
    triple = tuple(sorted((u, v, h)))
    pairs = tuple(combinations(triple, 2))
    incident = (tuple(sorted((u, h))), tuple(sorted((v, h))))
    mask = (1 << pairs.index(incident[0])) | (1 << pairs.index(incident[1]))
    return sum(
        mass for state, mass in enumerate(triples[triple]) if state & mask == 0
    )


def moment_of_edge_sum(tables, triples, edges, edge_list):
    first = sum(edges[edge] for edge in edge_list)
    second = first + 2 * sum(
        joint_red(tables, triples, left, right)
        for left, right in combinations(edge_list, 2)
    )
    return first, second


def neighbor_matrix(tables, triples, edges):
    """Build every ordered entry from physical edge products."""
    denominator = tables.denominator
    incident = {
        h: tuple(tuple(sorted((h, u))) for u in E if u != h)
        for h in range(N)
    }
    means = [sum(edges[edge] for edge in incident[h]) for h in range(N)]

    matrix = [[0] * (N + 1) for _ in range(N + 1)]
    matrix[0][0] = denominator
    for h in range(N):
        matrix[0][h + 1] = matrix[h + 1][0] = means[h]
    for h in range(N):
        for k in range(N):
            total = 0
            for first in incident[h]:
                for second in incident[k]:
                    total += (
                        edges[first]
                        if first == second
                        else joint_red(tables, triples, first, second)
                    )
            matrix[h + 1][k + 1] = total

    factor = [1] + [7 if h in (29, 30) else 6 for h in range(N)]
    require(
        all(
            matrix[i][j] == denominator * factor[i] * factor[j]
            for i in range(N + 1)
            for j in range(N + 1)
        ),
        "matrix differs from exact rank-one factor",
    )
    require(
        all(matrix[i][j] == matrix[j][i] for i in range(N + 1) for j in range(N + 1)),
        "matrix symmetry",
    )
    trace = sum(matrix[i][i] for i in range(1, N + 1))
    require(trace == 1574 * denominator, "neighbor trace")
    covariance_max = max(
        abs(denominator * matrix[h + 1][k + 1] - means[h] * means[k])
        for h in range(N)
        for k in range(N)
    )
    require(covariance_max == 0, "neighbor covariance")
    return incident, means, matrix, factor, trace, covariance_max


def wedge_numbering():
    """Reconstruct the inherited/suffix wedge indices from the 389 root support."""
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


def star_square_row(wedge_names):
    """Expand (sum B x_2u - 6)^2 pair by pair using blue wedges."""
    edge_names = {edge: i for i, edge in enumerate(combinations(range(N), 2), 1)}
    star = tuple(tuple(sorted((CENTER, u))) for u in B)
    coefficients = Counter({edge_names[edge]: 1 - 12 for edge in star})
    constant = 36
    for first, second in combinations(star, 2):
        common = set(first) & set(second)
        require(common == {CENTER}, "star edge intersection")
        u, v = sorted((set(first) | set(second)) - {CENTER})
        coefficients[wedge_names[u, v, CENTER]] += 2
        coefficients[edge_names[first]] += 2
        coefficients[edge_names[second]] += 2
        constant -= 2
    coefficients = Counter({index: value for index, value in coefficients.items() if value})
    require(
        len(coefficients) == 91
        and Counter(coefficients.values()) == Counter({13: 13, 2: 78})
        and constant == -120,
        "star row support",
    )
    row = (
        " ".join(
            f"{coefficient:+d} x{index}"
            for index, coefficient in sorted(coefficients.items())
        )
        + " >= 120 ;\n"
    ).encode()
    require(hashlib.sha256(row).hexdigest() == SQUARE_SHA256, "reconstructed row hash")
    return star, coefficients, constant, row, edge_names


def evaluate_star_row(tables, triples, edges, coefficients, constant, edge_names, wedge_names):
    reverse_edges = {index: edge for edge, index in edge_names.items()}
    reverse_wedges = {index: key for key, index in wedge_names.items()}
    total = constant * tables.denominator
    for index, coefficient in coefficients.items():
        if index in reverse_edges:
            value = edges[reverse_edges[index]]
        else:
            require(index in reverse_wedges, "unknown row coordinate")
            value = blue_wedge(triples, *reverse_wedges[index])
        total += coefficient * value
    return total


def small_truth_table() -> int:
    """Test the pair rewrite for all specified five-vertex controls."""
    edges = tuple(combinations(range(5), 2))
    checked = 0
    for center in range(5):
        neighbors = tuple(v for v in range(5) if v != center)
        for subset_mask in range(16):
            subset = tuple(
                vertex
                for bit, vertex in enumerate(neighbors)
                if subset_mask & (1 << bit)
            )
            star = tuple(tuple(sorted((center, vertex))) for vertex in subset)
            for offset in range(-1, 6):
                for graph_mask in range(1 << len(edges)):
                    red = {
                        edge
                        for bit, edge in enumerate(edges)
                        if graph_mask & (1 << bit)
                    }
                    direct = (sum(edge in red for edge in star) - offset) ** 2
                    expanded = offset * offset
                    expanded += (1 - 2 * offset) * sum(edge in red for edge in star)
                    for first, second in combinations(star, 2):
                        u, v = sorted((set(first) | set(second)) - {center})
                        wedge = int(
                            tuple(sorted((u, center))) not in red
                            and tuple(sorted((v, center))) not in red
                        )
                        expanded += 2 * (
                            wedge + int(first in red) + int(second in red) - 1
                        )
                    require(expanded == direct, "five-vertex truth table")
                    checked += 1
    require(checked == 573440, "truth-table census")
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", required=True, type=Path)
    parser.add_argument("--square", required=True, type=Path)
    args = parser.parse_args()

    tables = PhysicalTables(args.certificate)
    triples, edges, triple_checks, edge_checks = all_lower_marginals(tables)
    incident, means, matrix, factor, trace, covariance_max = neighbor_matrix(
        tables, triples, edges
    )

    previous_cut = tuple((u, v) for u in E for v in H)
    previous_mean, previous_second = moment_of_edge_sum(
        tables, triples, edges, previous_cut
    )
    previous_square = (
        previous_second - 144 * previous_mean + 5184 * tables.denominator
    )
    require(previous_mean == 72 * tables.denominator, "previous cut mean")
    require(previous_square == 0, "previous cut square")

    wedge_names = wedge_numbering()
    star, coefficients, constant, row, edge_names = star_square_row(wedge_names)
    require(args.square.read_bytes() == row, "submitted square row differs")
    star_mean, star_second = moment_of_edge_sum(tables, triples, edges, star)
    star_square = star_second - 12 * star_mean + 36 * tables.denominator
    row_value = evaluate_star_row(
        tables,
        triples,
        edges,
        coefficients,
        constant,
        edge_names,
        wedge_names,
    )
    require(row_value == star_square, "row value versus physical moment")
    require(5 * star_square < -tables.denominator, "strict -1/5 separation")
    truth_cases = small_truth_table()

    result = {
        "active_selector": 278,
        "certificate_sha256": CERTIFICATE_SHA256,
        "edge_extension_checks": edge_checks,
        "four_tables": len(tables.tables),
        "matrix_order": len(matrix),
        "matrix_ordered_entries": len(matrix) ** 2,
        "matrix_rank": 1,
        "neighbor_factor": factor,
        "neighbor_means": [str(Fraction(value, tables.denominator)) for value in means],
        "neighbor_trace": str(Fraction(trace, tables.denominator)),
        "positive_orbits": tables.positive_orbits,
        "previous_cut_edges": len(previous_cut),
        "previous_cut_mean": str(Fraction(previous_mean, tables.denominator)),
        "previous_cut_square": str(Fraction(previous_square, tables.denominator)),
        "small_truth_table_cases": truth_cases,
        "star_edges": len(star),
        "star_mean": str(Fraction(star_mean, tables.denominator)),
        "star_second_moment": str(Fraction(star_second, tables.denominator)),
        "star_square": str(Fraction(star_square, tables.denominator)),
        "star_square_sha256": SQUARE_SHA256,
        "star_square_terms": len(coefficients),
        "status": "INDEPENDENT_NEIGHBOR_MOMENT_PSD_REVIEW_PASS",
        "triple_extension_checks": triple_checks,
        "zero_covariance": covariance_max == 0,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
