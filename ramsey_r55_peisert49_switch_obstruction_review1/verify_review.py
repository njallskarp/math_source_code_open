#!/usr/bin/env python3
"""Independent expanded-embedding audit of the Peisert(49) switch obstruction.

The target certificate and target Python modules are deliberately not read.
Only the three published projective representatives in arcs.json are imported.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


TARGET_REF = "bafkreibqyof5gri5bpx3nfo5uggss3oikbnmsah2jlr5q4avqkykk7kcaa"
DEPENDENCY_REF = "bafkreicxhkf2dmw6olzioypy4qubctodu4u4aoyluxe5p6kq6fhpftvnoe"
TARGET_COMMIT = "e7eae57dd1196e2fb36120977c97e698da39650b"
ARCS_SHA256 = "6718119e0c67bb406f438f483732a0d5d04d3bc8af148e8d800499f7b656ec34"
TARGET_CERTIFICATE_SHA256 = "dad926f63de0e73cfd66a20f9cbed2ef2b065b5ce2cd998a04743df2c8733cce"
EXPECTED_HISTOGRAM = {
    3: 5760,
    4: 1728,
    5: 576,
    6: 5760,
    7: 4608,
    8: 576,
    9: 8640,
    10: 6048,
    11: 576,
}
MODULUS = 7
FIELD_SIZE = 49
FULL_MASK = (1 << FIELD_SIZE) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(vector):
    first = next((value for value in vector if value), None)
    require(first is not None, "zero projective vector")
    inverse = pow(first, MODULUS - 2, MODULUS)
    return tuple(value * inverse % MODULUS for value in vector)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right)) % MODULUS


def determinant(rows):
    first, second, third = rows
    return (
        first[0] * (second[1] * third[2] - second[2] * third[1])
        - first[1] * (second[0] * third[2] - second[2] * third[0])
        + first[2] * (second[0] * third[1] - second[1] * third[0])
    ) % MODULUS


def projective_plane():
    points = sorted(
        {normalize(vector) for vector in product(range(MODULUS), repeat=3) if any(vector)}
    )
    require(len(points) == MODULUS**2 + MODULUS + 1 == 57, "PG(2,7) cardinality")
    return points


def chart_forms(line):
    """Choose coordinate forms through a generic rank test."""
    vectors = [vector for vector in product(range(MODULUS), repeat=3) if any(vector)]
    for first in vectors:
        for second in vectors:
            if determinant((first, second, line)):
                return first, second
    raise ValueError("no affine chart basis")


def affine_chart(arc, line):
    first, second = chart_forms(line)
    image = []
    for point in arc:
        denominator = dot(line, point)
        require(denominator != 0, "chosen line at infinity meets the arc")
        inverse = pow(denominator, MODULUS - 2, MODULUS)
        image.append(
            (
                dot(first, point) * inverse % MODULUS,
                dot(second, point) * inverse % MODULUS,
            )
        )
    require(len(set(image)) == len(image) == 22, "affine chart is not injective")
    return image


def field_multiply(left, right):
    """Multiply x+y*t in F_7[t]/(t^2-3)."""
    x, y = left
    u, v = right
    return ((x * u + 3 * y * v) % MODULUS, (x * v + y * u) % MODULUS)


def field_power(value, exponent):
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = field_multiply(result, value)
        value = field_multiply(value, value)
        exponent >>= 1
    return result


def label(point):
    return point[0] + MODULUS * point[1]


def point(vertex):
    return vertex % MODULUS, vertex // MODULUS


def peisert_connection_set():
    generator = (1, 1)
    powers = []
    value = (1, 0)
    for exponent in range(FIELD_SIZE - 1):
        powers.append(value)
        value = field_multiply(value, generator)
    require(value == (1, 0) and len(set(powers)) == 48, "1+t is not primitive")
    return {label(value) for exponent, value in enumerate(powers) if exponent % 4 in (0, 1)}


def adjacency_rows(connection):
    rows = [0] * FIELD_SIZE
    for left in range(FIELD_SIZE):
        x, y = point(left)
        for right in range(FIELD_SIZE):
            if left == right:
                continue
            u, v = point(right)
            difference = ((x - u) % MODULUS, (y - v) % MODULUS)
            if label(difference) in connection:
                rows[left] |= 1 << right
    require(all(not (rows[i] >> i) & 1 for i in range(FIELD_SIZE)), "loop in graph")
    require(all(((rows[i] >> j) & 1) == ((rows[j] >> i) & 1)
                for i in range(FIELD_SIZE) for j in range(FIELD_SIZE)),
            "asymmetric Peisert adjacency")
    return rows


def slope(vector):
    x, y = vector
    require(x or y, "zero direction")
    return y * pow(x, MODULUS - 2, MODULUS) % MODULUS if x else MODULUS


def transform(points, matrix):
    a, b, c, d = matrix
    return [((a * x + b * y) % MODULUS, (c * x + d * y) % MODULUS)
            for x, y in points]


def direction_mask(matrix, adjacency):
    directions = [(1, value) for value in range(MODULUS)] + [(0, 1)]
    transformed = transform(directions, matrix)
    return sum(((adjacency[0] >> label(vector)) & 1) << index
               for index, vector in enumerate(transformed))


def monochromatic_four_records(adjacency):
    blue = [FULL_MASK & ~adjacency[vertex] & ~(1 << vertex)
            for vertex in range(FIELD_SIZE)]
    records = []
    color_counts = [0, 0]
    for quad in combinations(range(FIELD_SIZE), 4):
        color = (adjacency[quad[0]] >> quad[1]) & 1
        rows = adjacency if color else blue
        if not all((rows[left] >> right) & 1 for left, right in combinations(quad, 2)):
            continue
        quad_mask = sum(1 << vertex for vertex in quad)
        same = FULL_MASK
        opposite = FULL_MASK
        opposite_rows = blue if color else adjacency
        for vertex in quad:
            same &= rows[vertex]
            opposite &= opposite_rows[vertex]
        records.append((quad_mask, same & ~quad_mask, opposite & ~quad_mask))
        color_counts[color] += 1
    require(color_counts == [2156, 2156], "unexpected monochromatic K4 census")
    return records, color_counts


def count_admissible(anchor_mask, records):
    outside = FULL_MASK & ~anchor_mask
    forbidden = 0
    anchors = 0
    for quad_mask, same, opposite in records:
        if quad_mask & outside:
            continue
        require(not (same & anchor_mask), "22-point anchor contains a monochromatic K5")
        forbidden |= opposite
        anchors += 1
    forbidden &= outside
    return outside.bit_count() - forbidden.bit_count(), forbidden.bit_count(), anchors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path, help="checkout containing the target package")
    args = parser.parse_args()
    package = args.checkout.resolve() / "ramsey_r55_peisert49_switch_obstruction"

    arcs_raw = (package / "arcs.json").read_bytes()
    require(sha256(arcs_raw).hexdigest() == ARCS_SHA256, "arcs.json identity")
    raw_arcs = json.loads(arcs_raw)
    require(type(raw_arcs) is list and len(raw_arcs) == 3, "three arc representatives")

    plane = projective_plane()
    plane_set = set(plane)
    arcs = []
    profiles = []
    empty_lines = []
    saturation_checks = 0
    for raw_arc in raw_arcs:
        require(type(raw_arc) is list and len(raw_arc) == 22, "arc size")
        arc = [tuple(raw_point) for raw_point in raw_arc]
        require(len(arc) == len(set(arc)) == 22 and set(arc) <= plane_set,
                "literal projective representative")
        intersections = [sum(dot(line, arc_point) == 0 for arc_point in arc)
                         for line in plane]
        require(max(intersections) == 4, "representative is not a four-arc")
        profiles.append(tuple(intersections.count(size) for size in range(5)))
        empty_lines.append([line for line, size in zip(plane, intersections) if size == 0])
        for outside_point in plane_set - set(arc):
            require(any(size == 4 and dot(line, outside_point) == 0
                        for line, size in zip(plane, intersections)),
                    "representative extends to a 23-point four-arc")
            saturation_checks += 1
        arcs.append(arc)
    require(profiles == [(7, 1, 0, 21, 28), (6, 2, 3, 16, 30), (4, 4, 9, 6, 34)],
            "unexpected secant profiles")
    require([len(lines) for lines in empty_lines] == [7, 6, 4], "empty-line census")
    require(saturation_checks == 105, "projective saturation census")

    connection = peisert_connection_set()
    adjacency = adjacency_rows(connection)
    directions = [(1, value) for value in range(MODULUS)] + [(0, 1)]
    literal_red_slopes = {slope(vector) for vector in directions
                          if (adjacency[0] >> label(vector)) & 1}
    require(literal_red_slopes == {0, 1, 5, 7}, "quartic cosets disagree with slope colors")

    field = list(product(range(MODULUS), repeat=2))
    translation_checks = 0
    for shift in field:
        for left in field:
            for right in field:
                moved_left = ((left[0] + shift[0]) % MODULUS,
                              (left[1] + shift[1]) % MODULUS)
                moved_right = ((right[0] + shift[0]) % MODULUS,
                               (right[1] + shift[1]) % MODULUS)
                original = (adjacency[label(left)] >> label(right)) & 1
                moved = (adjacency[label(moved_left)] >> label(moved_right)) & 1
                require(original == moved, "translation changed a Peisert color")
                translation_checks += 1

    gl2 = [(a, b, c, d) for a, b, c, d in product(range(MODULUS), repeat=4)
           if (a * d - b * c) % MODULUS]
    require(len(gl2) == 2016, "GL(2,7) cardinality")
    mask_counts = Counter(direction_mask(matrix, adjacency) for matrix in gl2)
    require(len(mask_counts) == 28 and set(mask_counts.values()) == {72},
            "GL(2,7) direction-mask quotient")

    records, four_counts = monochromatic_four_records(adjacency)
    histogram = Counter()
    anchor_histogram = Counter()
    stream = sha256()
    expanded_cases = 0
    for arc_index, (arc, lines) in enumerate(zip(arcs, empty_lines)):
        for line_index, line in enumerate(lines):
            chart = affine_chart(arc, line)
            for matrix_index, matrix in enumerate(gl2):
                image = transform(chart, matrix)
                require(len(set(image)) == 22, "invertible image collision")
                anchor_mask = sum(1 << label(value) for value in image)
                admissible, forbidden, anchor_quads = count_admissible(anchor_mask, records)
                require(forbidden >= 7 and admissible <= 20,
                        "insufficient opposite-switch obstructions")
                histogram[admissible] += 1
                anchor_histogram[anchor_quads] += 1
                stream.update(
                    bytes((arc_index, line_index, matrix_index >> 8, matrix_index & 255,
                           admissible, forbidden, anchor_quads >> 8, anchor_quads & 255))
                )
                stream.update(anchor_mask.to_bytes(7, "little"))
                expanded_cases += 1
    require(expanded_cases == 17 * 2016 == 34272, "expanded embedding coverage")
    require(dict(sorted(histogram.items())) == EXPECTED_HISTOGRAM,
            "expanded attachment-capacity histogram")

    result = {
        "status": "ACCEPTED_WITH_HILL_LOVE_CLASSIFICATION_IMPORTED",
        "target_ref": TARGET_REF,
        "dependency_ref": DEPENDENCY_REF,
        "target_commit": TARGET_COMMIT,
        "target_certificate_sha256_replayed_separately": TARGET_CERTIFICATE_SHA256,
        "arcs_sha256": sha256(arcs_raw).hexdigest(),
        "projective_points_and_lines": len(plane),
        "representative_profiles": [list(profile) for profile in profiles],
        "empty_lines": [len(lines) for lines in empty_lines],
        "saturated_outside_projective_points": saturation_checks,
        "peisert_red_slopes": sorted(literal_red_slopes),
        "monochromatic_k4_blue_red": four_counts,
        "gl2_matrices_per_chart": len(gl2),
        "direction_masks": len(mask_counts),
        "matrices_per_direction_mask": sorted(set(mask_counts.values())).pop(),
        "expanded_affine_linear_cases": expanded_cases,
        "admissible_outside_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "maximum_individually_admissible_outside_points": max(histogram),
        "minimum_forbidden_outside_points": 27 - max(histogram),
        "anchor_monochromatic_k4_count_histogram": {
            str(key): value for key, value in sorted(anchor_histogram.items())
        },
        "translation_color_checks": translation_checks,
        "expanded_case_stream_sha256": stream.hexdigest(),
        "classification_recomputed": False,
        "target_certificate_consumed_by_independent_checker": False,
        "imported_theorem": (
            "Hill--Love (2003): exactly three projective equivalence classes "
            "of 22-point four-arcs in PG(2,7)."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
