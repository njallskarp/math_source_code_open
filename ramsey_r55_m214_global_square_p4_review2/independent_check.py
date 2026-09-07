#!/usr/bin/env python3
"""Definition-level review of the M214 negative cut-square certificate.

This checker imports no module from the contribution under review. It decodes
canonical four-vertex tables as distributions on physical edge sets, verifies
all lower-marginal transports, recomputes the cut and deficiency moments, and
reconstructs the OPB cut-square row from unordered physical edge pairs.
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
PAIRS4 = tuple(combinations(range(4), 2))
CERTIFICATE_SHA256 = "3b16d19909a4a77c783a38ed264bead685f384c9a426dc3710b896a53309d815"
SQUARE_SHA256 = "f417545ff00195cf4da0a6ae22f2af7bb9984fc131c4a5bd7671e3cdfc5d0043"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def subset_rank(vertices: tuple[int, ...], n: int) -> int:
    """Zero-based lexicographic rank among equal-size subsets of range(n)."""
    require(tuple(sorted(set(vertices))) == vertices, "noncanonical subset")
    rank = 0
    previous = -1
    k = len(vertices)
    for i, vertex in enumerate(vertices):
        rank += sum(
            math.comb(n - candidate - 1, k - i - 1)
            for candidate in range(previous + 1, vertex)
        )
        previous = vertex
    return rank


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    out = 0
    for bit, (u, v) in enumerate(PAIRS4):
        if mask & (1 << bit):
            image = tuple(sorted((permutation[u], permutation[v])))
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
        require(type(self.denominator) is int and self.denominator > 0, "denominator")
        self.cells = raw["cells"]
        require(all(type(cell) is list and cell for cell in self.cells), "nonempty cells")
        require(
            sorted(v for cell in self.cells for v in cell) == list(range(N)),
            "physical vertex partition",
        )
        self.vertex_class = {v: c for c, cell in enumerate(self.cells) for v in cell}
        require(raw["active_selectors"] == [278], "active root")

        sizes = tuple(map(len, self.cells))
        self.tables: dict[tuple[int, ...], tuple[int, ...]] = {}
        positive_orbits = 0
        for record in raw["four_tables"]:
            require(set(record) == {"types", "orbits"}, "four-table fields")
            types = tuple(record["types"])
            require(types == tuple(sorted(types)) and len(types) == 4, "canonical types")
            require(types not in self.tables, "duplicate four-table")
            require(all(0 <= c < len(sizes) for c in types), "class range")
            require(
                all(types.count(c) <= sizes[c] for c in set(types)),
                "class multiplicity",
            )
            stabilizer = tuple(
                p
                for p in permutations(range(4))
                if all(types[i] == types[p[i]] for i in range(4))
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
            if all(types.count(c) <= sizes[c] for c in set(types))
        }
        require(set(self.tables) == expected, "incomplete four-table support")
        require((len(self.tables), positive_orbits) == (345, 4165), "table/orbit census")
        self.positive_orbits = positive_orbits
        self._physical_four_cache: dict[tuple[int, ...], tuple[int, ...]] = {}

    def physical_four(self, vertices: tuple[int, ...]) -> tuple[int, ...]:
        """Distribution in the numeric-vertex edge order of one physical 4-set."""
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
            for bit, (u_pos, v_pos) in enumerate(PAIRS4):
                edge = tuple(sorted((ordered[u_pos], ordered[v_pos])))
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
    """Verify that every physical triple/edge is independent of its extension."""
    triples: dict[tuple[int, ...], tuple[int, ...]] = {}
    triple_extension_checks = 0
    for triple in combinations(range(N), 3):
        fillers = [v for v in range(N) if v not in triple]
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
        "triple check census",
    )
    require(edge_extension_checks == math.comb(N, 2) * 40, "edge check census")
    return triples, edges, triple_extension_checks, edge_extension_checks


def joint_red(tables: PhysicalTables, triples, first, second) -> int:
    vertices = tuple(sorted(set(first + second)))
    require(len(vertices) in (3, 4), "distinct edge pair")
    pairs = tuple(combinations(vertices, 2))
    mask = (1 << pairs.index(first)) | (1 << pairs.index(second))
    distribution = triples[vertices] if len(vertices) == 3 else tables.physical_four(vertices)
    return sum(
        mass for state, mass in enumerate(distribution) if state & mask == mask
    )


def blue_wedge(triples, u: int, v: int, h: int) -> int:
    triple = tuple(sorted((u, v, h)))
    pairs = tuple(combinations(triple, 2))
    incident = (tuple(sorted((u, h))), tuple(sorted((v, h))))
    mask = (1 << pairs.index(incident[0])) | (1 << pairs.index(incident[1]))
    return sum(
        mass for state, mass in enumerate(triples[triple]) if state & mask == 0
    )


def physical_moments(tables: PhysicalTables, triples, edges):
    denominator = tables.denominator
    cut = tuple((u, v) for u in E for v in H)
    cut_mean = sum(edges[edge] for edge in cut)
    cut_second = cut_mean
    shared = disjoint = 0
    for first, second in combinations(cut, 2):
        cut_second += 2 * joint_red(tables, triples, first, second)
        if set(first) & set(second):
            shared += 1
        else:
            disjoint += 1
    cut_square = cut_second - 144 * cut_mean + 5184 * denominator
    require((len(cut), shared, disjoint) == (156, 1794, 10296), "cut pair census")
    require(cut_mean == 72 * denominator, "cut mean")
    require(cut_square < -353 * denominator, "strict cut-square violation")

    deficiency_first = deficiency_second = 0
    for h in range(N):
        incident = tuple(tuple(sorted((h, u))) for u in E if u != h)
        local_first = sum(edges[edge] for edge in incident)
        local_second = local_first + 2 * sum(
            joint_red(tables, triples, first, second)
            for first, second in combinations(incident, 2)
        )
        deficiency_first += local_first
        deficiency_second += local_second
    require(deficiency_first == 260 * denominator, "deficiency first moment")
    require(
        deficiency_second == 1576 * denominator,
        "tight deficiency second moment",
    )
    return cut, cut_mean, cut_second, cut_square, shared, disjoint


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


def cut_square_row(cut, wedge_names):
    """Literal pair expansion, with shared products rewritten as blue wedges."""
    edge_names = {edge: i for i, edge in enumerate(combinations(range(N), 2), 1)}
    coefficients = Counter({edge_names[edge]: -143 for edge in cut})
    atom_coordinates = {}
    shared = disjoint = 0
    constant = 5184
    for first, second in combinations(cut, 2):
        common = set(first) & set(second)
        if common:
            h = next(iter(common))
            u, v = sorted((set(first) | set(second)) - {h})
            coefficients[wedge_names[u, v, h]] += 2
            coefficients[edge_names[first]] += 2
            coefficients[edge_names[second]] += 2
            constant -= 2
            shared += 1
        else:
            vertices = tuple(sorted(first + second))
            pairs = tuple(combinations(vertices, 2))
            mask = (1 << pairs.index(first)) | (1 << pairs.index(second))
            base = 125170 + 64 * subset_rank(vertices, N)
            for state in range(64):
                if state & mask == mask:
                    coordinate = base + state
                    coefficients[coordinate] += 2
                    atom_coordinates[coordinate] = (vertices, state)
            disjoint += 1
    coefficients = Counter({i: c for i, c in coefficients.items() if c})
    require(
        (shared, disjoint, constant, len(coefficients))
        == (1794, 10296, 1596, 146094),
        "row support",
    )
    require(
        Counter(coefficients.values()) == Counter({-97: 156, 2: 125346, 4: 20592}),
        "coefficient histogram",
    )
    row = (
        " ".join(
            f"{coefficient:+d} x{index}"
            for index, coefficient in sorted(coefficients.items())
        )
        + " >= -1596 ;\n"
    ).encode()
    require(hashlib.sha256(row).hexdigest() == SQUARE_SHA256, "reconstructed row hash")
    return coefficients, atom_coordinates, constant, row, edge_names


def evaluate_row(
    tables,
    triples,
    edges,
    coefficients,
    atom_coordinates,
    constant,
    edge_names,
    wedge_names,
):
    reverse_edges = {index: edge for edge, index in edge_names.items()}
    reverse_wedges = {index: key for key, index in wedge_names.items()}
    total = constant * tables.denominator
    for index, coefficient in coefficients.items():
        if index in reverse_edges:
            value = edges[reverse_edges[index]]
        elif index in reverse_wedges:
            value = blue_wedge(triples, *reverse_wedges[index])
        else:
            vertices, state = atom_coordinates[index]
            value = tables.physical_four(vertices)[state]
        total += coefficient * value
    return total


def small_truth_table() -> int:
    """Check the same literal-pair rewrite on every graph over five vertices."""
    n = 5
    physical_edges = tuple(combinations(range(n), 2))
    edge_names = {edge: i for i, edge in enumerate(physical_edges, 1)}
    wedge_names = {
        (u, v, h): 11 + i
        for i, (u, v, h) in enumerate(
            (u, v, h)
            for u, v in physical_edges
            for h in range(n)
            if h not in (u, v)
        )
    }
    four_sets = tuple(combinations(range(n), 4))
    checked = 0
    for left in combinations(range(n), 2):
        right = tuple(v for v in range(n) if v not in left)
        cut = tuple(tuple(sorted((u, v))) for u in left for v in right)
        coefficients = Counter({edge_names[edge]: 1 - 6 for edge in cut})
        constant = 9
        for first, second in combinations(cut, 2):
            common = set(first) & set(second)
            if common:
                h = next(iter(common))
                u, v = sorted((set(first) | set(second)) - {h})
                coefficients[wedge_names[u, v, h]] += 2
                coefficients[edge_names[first]] += 2
                coefficients[edge_names[second]] += 2
                constant -= 2
            else:
                vertices = tuple(sorted(first + second))
                pairs = tuple(combinations(vertices, 2))
                required = (1 << pairs.index(first)) | (1 << pairs.index(second))
                base = 100 + 64 * four_sets.index(vertices)
                for state in range(64):
                    if state & required == required:
                        coefficients[base + state] += 2
        for graph in range(1 << len(physical_edges)):
            red = {
                edge
                for bit, edge in enumerate(physical_edges)
                if graph & (1 << bit)
            }
            values = {edge_names[edge]: int(edge in red) for edge in physical_edges}
            values.update(
                {
                    index: int(
                        tuple(sorted((u, h))) not in red
                        and tuple(sorted((v, h))) not in red
                    )
                    for (u, v, h), index in wedge_names.items()
                }
            )
            for j, vertices in enumerate(four_sets):
                state = sum(
                    int(edge in red) << bit
                    for bit, edge in enumerate(combinations(vertices, 2))
                )
                values[100 + 64 * j + state] = 1
            lhs = constant + sum(
                coefficient * values.get(index, 0)
                for index, coefficient in coefficients.items()
            )
            x = sum(edge in red for edge in cut)
            require(lhs == (x - 3) ** 2, "five-vertex truth table")
            checked += 1
    require(checked == 10240, "truth-table census")
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", required=True, type=Path)
    parser.add_argument("--square", required=True, type=Path)
    args = parser.parse_args()

    tables = PhysicalTables(args.certificate)
    triples, edges, triple_checks, edge_checks = all_lower_marginals(tables)
    cut, mean, second, square, shared, disjoint = physical_moments(
        tables, triples, edges
    )
    wedge_names = wedge_numbering()
    coefficients, atoms, constant, row, edge_names = cut_square_row(cut, wedge_names)
    require(args.square.read_bytes() == row, "submitted square row differs")
    row_value = evaluate_row(
        tables,
        triples,
        edges,
        coefficients,
        atoms,
        constant,
        edge_names,
        wedge_names,
    )
    require(row_value == square, "row value versus physical moment")
    truth_cases = small_truth_table()

    result = {
        "active_selector": 278,
        "certificate_sha256": CERTIFICATE_SHA256,
        "cut_edges": len(cut),
        "cut_mean": str(Fraction(mean, tables.denominator)),
        "cut_second_moment": str(Fraction(second, tables.denominator)),
        "cut_square_value": str(Fraction(square, tables.denominator)),
        "deficiency_first_moment": "260",
        "deficiency_second_moment": "1576",
        "disjoint_cut_pairs": disjoint,
        "edge_extension_checks": edge_checks,
        "four_tables": len(tables.tables),
        "matrix_determinant": str(Fraction(square, tables.denominator)),
        "positive_orbits": tables.positive_orbits,
        "row_coefficient_histogram": {"-97": 156, "2": 125346, "4": 20592},
        "row_terms": len(coefficients),
        "shared_cut_pairs": shared,
        "small_truth_table_cases": truth_cases,
        "square_sha256": SQUARE_SHA256,
        "status": "INDEPENDENT_M214_GLOBAL_SQUARE_REVIEW_PASS",
        "triple_extension_checks": triple_checks,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
