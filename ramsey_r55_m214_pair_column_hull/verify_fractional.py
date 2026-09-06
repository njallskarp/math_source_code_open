#!/usr/bin/env python3
"""Check the exact fractional point separated by the pair-column hull."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path

import build
import derive_fractional_certificate as witness


ROOT_INDEX = 48
ROOT_KEY = ("E8", 13, 0, "A")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_certificate(path: Path):
    lines = path.read_text(encoding="ascii").splitlines()
    require(lines and lines[0] == "signature\ttriples\tlower\tupper\tz", "certificate header")
    orbits = witness.orbit_table()
    require(len(lines) == len(orbits) + 1, "certificate row count")
    values = {}
    for index, (line, orbit) in enumerate(zip(lines[1:], orbits, strict=True)):
        fields = line.split("\t")
        require(len(fields) == 5, f"certificate fields {index}")
        sig, count, _, lower, upper = orbit
        require(fields[0] == witness.signature_text(sig), f"signature {index}")
        require(int(fields[1]) == count, f"triple count {index}")
        require(Fraction(fields[2]) == lower, f"lower bound {index}")
        require(Fraction(fields[3]) == upper, f"upper bound {index}")
        value = Fraction(fields[4])
        require(lower <= value <= upper, f"z bound {index}")
        require(sig not in values, f"duplicate signature {index}")
        values[sig] = value
    return values


def check_edge_certificate(path: Path) -> None:
    lines = path.read_text(encoding="ascii").splitlines()
    require(lines and lines[0] == "name\tvalue", "edge-certificate header")
    require(len(lines) == len(witness.EDGE_PARAMETERS) + 1, "edge-certificate rows")
    observed = {}
    for line in lines[1:]:
        name, value = line.split("\t")
        require(name not in observed, "duplicate edge parameter")
        observed[name] = Fraction(value)
    require(observed == witness.EDGE_PARAMETERS, "edge-certificate values")


def edge(left: int, right: int) -> Fraction:
    return witness.edge_value(left, right)


def triangle_value(triple: tuple[int, int, int], values) -> Fraction:
    return values[witness.signature(triple)]


def root_record(key: tuple[str, int, int, str]):
    family, _, _, pattern = key
    cells = build.root_cells(key)
    anomaly_offset = 0 if family.startswith("E") else 4
    anomalies = []
    for index, cell_name in enumerate(build.CELLS):
        anomalies.extend(cells[anomaly_offset + index][: pattern.count(cell_name)])
    excess = 2 if family in {"E8", "C8"} else 1
    units = [(0, 1, 1)]
    bits = ((1, 1), (1, 0), (0, 1), (0, 0))
    for index, cell in enumerate(cells):
        for vertex in cell:
            units.append((0, vertex, bits[index % 4][0]))
            units.append((1, vertex, bits[index % 4][1]))
    partition = None
    if family == "C77partition":
        p, q = anomalies
        partition = (
            p,
            q,
            tuple([0, 1] + [v for v in range(15, build.N) if v not in anomalies]),
        )
    return {
        "a_targets": tuple(6 + (excess if vertex in anomalies else 0) for vertex in range(build.N)),
        "partition": partition,
        "units": tuple(units),
    }


def maximum_zero_product(left: Fraction, right: Fraction) -> Fraction:
    return max(Fraction(0), 1 - left - right)


def check(edge_path: Path, triangle_path: Path) -> dict[str, object]:
    require(build.ROOT_KEYS[ROOT_INDEX] == ROOT_KEY, "selected root identity")
    check_edge_certificate(edge_path)
    z_values = parse_certificate(triangle_path)

    # Complete intrinsic LP: edge bounds, all degree/E-incidence equations,
    # all five-set rows, all triangle conjunction rows, and local triangle sums.
    edges = {
        (left, right): edge(left, right)
        for left, right in itertools.combinations(range(build.N), 2)
    }
    require(all(0 <= value <= 1 for value in edges.values()), "edge range")
    for vertex in range(build.N):
        degree = sum(edge(vertex, other) for other in range(build.N) if other != vertex)
        e_incidence = sum(
            edge(vertex, other) for other in build.EXCEPTIONAL if other != vertex
        )
        require(degree == (20 if vertex in build.EXCEPTIONAL else 21), f"degree {vertex}")
        require(e_incidence == (8 if vertex == 2 else 6), f"E incidence {vertex}")

    five_set_minimum = Fraction(10)
    five_set_maximum = Fraction(0)
    five_set_count = 0
    for vertices in itertools.combinations(range(build.N), 5):
        total = sum(edge(i, j) for i, j in itertools.combinations(vertices, 2))
        require(1 <= total <= 9, f"five-set row {vertices}")
        five_set_minimum = min(five_set_minimum, total)
        five_set_maximum = max(five_set_maximum, total)
        five_set_count += 1

    local_triangles = [Fraction(0) for _ in range(build.N)]
    triangle_count = 0
    for triple in itertools.combinations(range(build.N), 3):
        edge_values = [edge(i, j) for i, j in itertools.combinations(triple, 2)]
        value = triangle_value(triple, z_values)
        require(value >= sum(edge_values) - 2, f"triangle lower {triple}")
        require(all(value <= item for item in edge_values), f"triangle upper {triple}")
        for vertex in triple:
            local_triangles[vertex] += value
        triangle_count += 1
    for vertex, total in enumerate(local_triangles):
        require(total == (93 if vertex in build.EXCEPTIONAL else 100), f"local triangles {vertex}")

    # Every selector-gated root row from height 3160.
    selector_rows = 1
    for root_index, key in enumerate(build.ROOT_KEYS):
        selected = Fraction(int(root_index == ROOT_INDEX))
        record = root_record(key)
        for left, right, target in record["units"]:
            value = edge(left, right)
            require(
                value - selected >= 0 if target else -value - selected >= -1,
                f"guarded unit {root_index}",
            )
            selector_rows += 1
        for vertex, target in enumerate(record["a_targets"]):
            total = sum(
                edge(vertex, other)
                for other in build.EXCEPTIONAL
                if other != vertex
            )
            require(total - target * selected >= 0, f"a lower {root_index},{vertex}")
            require(-total - (13 - target) * selected >= -13, f"a upper {root_index},{vertex}")
            selector_rows += 2
        if record["partition"] is not None:
            p, q, vertices = record["partition"]
            require(-edge(p, q) - selected >= -1, f"partition edge {root_index}")
            selector_rows += 1
            for vertex in vertices:
                total = edge(vertex, p) + edge(vertex, q)
                require(total - selected >= 0, f"partition lower {root_index},{vertex}")
                require(-total - selected >= -2, f"partition upper {root_index},{vertex}")
                selector_rows += 2
    require(selector_rows == 69_732, "selector row count")

    # Height-3228 unary footprint rows and height-3254 c=9,10 pair rows.
    unary_rows = 0
    projected_pair_rows = 0
    for root_index, key in enumerate(build.ROOT_KEYS):
        common = key[1]
        core, exterior = build.root_data(key)
        selected = Fraction(int(root_index == ROOT_INDEX))
        for vertex in exterior:
            total = sum(edge(vertex, h) for h in core)
            require(total - (common - 8) * selected >= 0, f"unary footprint {root_index}")
            unary_rows += 1
        if common in (9, 10):
            for left, right in itertools.combinations(exterior, 2):
                total = sum(edge(left, h) + edge(right, h) for h in core)
                total += (common - 5) * edge(left, right)
                total -= (common - 5) * selected
                require(total >= 0, f"projected pair {root_index}")
                projected_pair_rows += 1
    require(unary_rows == 11_672 and projected_pair_rows == 74_958, "prior root rows")

    # Height-3274 exact m/q definitions and local pair-cell facets.
    missed = {
        key: maximum_zero_product(edge(key[0], key[2]), edge(key[1], key[2]))
        for key in build.MISSED_KEYS
    }
    for (left, right, vertex), value in missed.items():
        left_edge, right_edge = edge(left, vertex), edge(right, vertex)
        require(value + left_edge <= 1 and value + right_edge <= 1, "m upper")
        require(value + left_edge + right_edge >= 1, "m lower")

    red_inside_support: set[tuple[int, int, int, int]] = set()
    for key in build.ROOT_KEYS:
        core, exterior = build.root_data(key)
        for left, right in itertools.combinations(exterior, 2):
            red_inside_support.update(
                (left, right, i, j) for i, j in itertools.combinations(core, 2)
            )
    red_inside = {}
    for key in sorted(red_inside_support):
        left, right, i, j = key
        value = max(Fraction(0), missed[left, right, i] + missed[left, right, j] + edge(i, j) - 2)
        red_inside[key] = value
        require(value <= missed[left, right, i], "q upper i")
        require(value <= missed[left, right, j], "q upper j")
        require(value <= edge(i, j), "q upper edge")
        require(value >= missed[left, right, i] + missed[left, right, j] + edge(i, j) - 2, "q lower")
    require(len(red_inside) == 74_513, "q support")

    local_pair_rows = 0
    for root_index, key in enumerate(build.ROOT_KEYS):
        common = key[1]
        core, exterior = build.root_data(key)
        selected = Fraction(int(root_index == ROOT_INDEX))
        for left, right in itertools.combinations(exterior, 2):
            m = sum(missed[left, right, vertex] for vertex in core)
            q = sum(red_inside[left, right, i, j] for i, j in itertools.combinations(core, 2))
            pair = edge(left, right)
            require(-m + (common - 5) * pair - (common - 5) * selected >= -common, "pair m")
            require(q - m + (common - 2) * pair - (common - 2) * selected >= -common, "pair first")
            require(q - 3 * m + (3 * common - 10) * pair - (3 * common - 10) * selected >= -3 * common, "pair second")
            local_pair_rows += 3
    require(local_pair_rows == 508_986, "local pair row count")

    # Evaluate the new hull.  Exactly the 13 active lower rows fail.
    hull_violations = []
    hull_rows = 0
    for root_index, key in enumerate(build.ROOT_KEYS):
        common = key[1]
        core, exterior = build.root_data(key)
        selected = Fraction(int(root_index == ROOT_INDEX))
        pair_count = len(exterior) * (len(exterior) - 1) // 2
        for vertex in core:
            a = sum(edge(vertex, other) for other in core if other != vertex)
            m = sum(
                missed[left, right, vertex]
                for left, right in itertools.combinations(exterior, 2)
            )
            shift, lower, upper, tangents = build.hull_parameters(
                common, vertex in build.EXCEPTIONAL
            )
            for tangent in tangents:
                rhs_active = tangent * shift - tangent * (tangent + 1) // 2
                guard = rhs_active + tangent * (common - 1)
                slack = m - tangent * a - guard * selected + tangent * (common - 1)
                if slack < 0:
                    hull_violations.append((root_index, vertex, tangent, slack))
                hull_rows += 1
            slope_twice = lower + upper - 1
            rhs_active = lower * upper - slope_twice * shift
            guard = rhs_active + 2 * pair_count
            slack = -2 * m + slope_twice * a - guard * selected + 2 * pair_count
            if slack < 0:
                hull_violations.append((root_index, vertex, -1, slack))
            hull_rows += 1
    require(hull_rows == build.SUFFIX_ROWS, "hull row count")
    require(len(hull_violations) == 13, "hull violation count")
    require(
        all(root == ROOT_INDEX and tangent == 13 and slack == -72
            for root, _, tangent, slack in hull_violations),
        "unexpected hull violation",
    )

    active_core, active_exterior = build.root_data(ROOT_KEY)
    active_missed_totals = {
        sum(
            missed[left, right, vertex]
            for left, right in itertools.combinations(active_exterior, 2)
        )
        for vertex in active_core
    }
    require(active_missed_totals == {Fraction(6)}, "active missed totals")
    return {
        "active_columns": len(active_core),
        "active_missed_total": 6,
        "five_set_count": five_set_count,
        "five_set_max": str(five_set_maximum),
        "five_set_min": str(five_set_minimum),
        "hull_rows": hull_rows,
        "hull_violations": len(hull_violations),
        "local_pair_rows": local_pair_rows,
        "minimum_hull_slack": -72,
        "projected_pair_rows": projected_pair_rows,
        "q_variables": len(red_inside),
        "root": list(ROOT_KEY),
        "root_index": ROOT_INDEX,
        "selector_rows": selector_rows,
        "triangle_count": triangle_count,
        "triangle_orbits": len(z_values),
        "unary_rows": unary_rows,
    }


def main() -> None:
    require(len(sys.argv) in (1, 3), "usage: verify_fractional.py [edge_parameters.tsv triangle_orbits.tsv]")
    edge_path = Path(sys.argv[1]) if len(sys.argv) == 3 else Path("edge_parameters.tsv")
    triangle_path = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("triangle_orbits.tsv")
    result = check(edge_path, triangle_path)
    fields = " ".join(f"{key}={value}" for key, value in result.items())
    print("PASS " + fields)


if __name__ == "__main__":
    main()
