#!/usr/bin/env python3
"""Independent expanded-orbit audit of the Paley(49) four-arc obstruction."""

import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


TARGET_REF = "bafkreigbtza7cclrgw7ylpkxy2bbgdgmy64fbas66uhni6o34tx4la3keq"
DEPENDENCY_REF = "bafkreicxhkf2dmw6olzioypy4qubctodu4u4aoyluxe5p6kq6fhpftvnoe"
TARGET_COMMIT = "3699fda9b6c67adb2b0f1266c735271033201e79"
CERTIFICATE_SHA256 = "ffa55fc61f4fb2733dbb492b32d7acf3f4aaa4a7da6392c72eb7a9811b33f594"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(vector):
    first = next((x for x in vector if x), None)
    require(first is not None, "zero projective vector")
    inverse = pow(first, 5, 7)
    return tuple(x * inverse % 7 for x in vector)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right)) % 7


def determinant(rows):
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) % 7


def projective_plane():
    points = sorted({normalize(v) for v in product(range(7), repeat=3) if any(v)})
    require(len(points) == 57, "PG(2,7) point count")
    return points


def chart_forms(line):
    """Choose affine coordinate forms by a generic rank test, not target conventions."""
    vectors = [v for v in product(range(7), repeat=3) if any(v)]
    for first in vectors:
        for second in vectors:
            if determinant((first, second, line)):
                return first, second
    raise ValueError("no chart basis")


def affine_chart(arc, line):
    first, second = chart_forms(line)
    image = []
    for point in arc:
        denominator = dot(line, point)
        require(denominator != 0, "chart line is not empty")
        inverse = pow(denominator, 5, 7)
        image.append((dot(first, point) * inverse % 7,
                      dot(second, point) * inverse % 7))
    require(len(set(image)) == 22, "chart is not injective")
    return image


def field_multiply(left, right):
    """Multiply pairs representing x+y*t in F7[t]/(t^2-3)."""
    x, y = left
    u, v = right
    return ((x * u + 3 * y * v) % 7, (x * v + y * u) % 7)


def field_subtract(left, right):
    return ((left[0] - right[0]) % 7, (left[1] - right[1]) % 7)


def field_power(value, exponent):
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = field_multiply(result, value)
        value = field_multiply(value, value)
        exponent >>= 1
    return result


def red(left, right):
    difference = field_subtract(left, right)
    return difference != (0, 0) and field_power(difference, 24) == (1, 0)


def transform(points, matrix):
    a, b, c, d = matrix
    return [((a * x + b * y) % 7, (c * x + d * y) % 7) for x, y in points]


def clique(rows, size, candidates=None, chosen=()):
    if size == 0:
        return chosen
    if candidates is None:
        candidates = (1 << len(rows)) - 1
    while candidates.bit_count() >= size:
        bit = candidates & -candidates
        candidates ^= bit
        vertex = bit.bit_length() - 1
        found = clique(rows, size - 1, candidates & rows[vertex], chosen + (vertex,))
        if found is not None:
            return found
    return None


def monochromatic_five(points):
    n = len(points)
    red_rows = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if red(points[i], points[j]):
                red_rows[i] |= 1 << j
                red_rows[j] |= 1 << i
    witness = clique(red_rows, 5)
    if witness is not None:
        return 1, witness
    mask = (1 << n) - 1
    blue_rows = [mask ^ red_rows[i] ^ (1 << i) for i in range(n)]
    witness = clique(blue_rows, 5)
    require(witness is not None, "expanded affine image has no monochromatic five-set")
    return 0, witness


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path, help="full public math_results checkout")
    args = parser.parse_args()
    package = args.checkout.resolve() / "ramsey_r55_paley49_arc_obstruction"
    certificate_raw = (package / "certificate.json").read_bytes()
    require(sha256(certificate_raw).hexdigest() == CERTIFICATE_SHA256,
            "certificate identity")
    certificate = json.loads(certificate_raw)
    require(set(certificate) == {"schema", "arcs", "cases"} and certificate["schema"] == 1,
            "certificate schema")

    plane = projective_plane()
    plane_set = set(plane)
    arcs = []
    profiles = []
    empty_lines = []
    for raw_arc in certificate["arcs"]:
        arc = [tuple(point) for point in raw_arc]
        require(len(arc) == len(set(arc)) == 22 and set(arc) <= plane_set,
                "literal 22-point projective set")
        intersections = [sum(dot(line, point) == 0 for point in arc) for line in plane]
        require(max(intersections) == 4, "representative is not a four-arc")
        profile = tuple(intersections.count(size) for size in range(5))
        profiles.append(profile)
        empty_lines.append([line for line, size in zip(plane, intersections) if size == 0])
        arcs.append(arc)
    require(len(arcs) == 3 and len(set(profiles)) == 3, "three inequivalent literal types")
    require([len(lines) for lines in empty_lines] == [7, 6, 4], "empty-line counts")

    gl2 = [
        (a, b, c, d)
        for a, b, c, d in product(range(7), repeat=4)
        if (a * d - b * c) % 7
    ]
    require(len(gl2) == 2016, "GL(2,7) cardinality")

    # Translation invariance is checked directly on every ordered field pair.
    field = list(product(range(7), repeat=2))
    translation_checks = 0
    for shift in field:
        for left in field:
            for right in field:
                moved_left = ((left[0] + shift[0]) % 7, (left[1] + shift[1]) % 7)
                moved_right = ((right[0] + shift[0]) % 7, (right[1] + shift[1]) % 7)
                require(red(left, right) == red(moved_left, moved_right),
                        "translation changed a Paley color")
                translation_checks += 1

    witnesses = sha256()
    colors = [0, 0]
    expanded_cases = 0
    for arc_index, (arc, lines) in enumerate(zip(arcs, empty_lines)):
        for line_index, line in enumerate(lines):
            base = affine_chart(arc, line)
            for matrix_index, matrix in enumerate(gl2):
                image = transform(base, matrix)
                require(len(set(image)) == 22, "invertible image collision")
                color, witness = monochromatic_five(image)
                require(all(red(image[i], image[j]) == bool(color)
                            for position, i in enumerate(witness)
                            for j in witness[position + 1:]),
                        "reported witness is not physical")
                colors[color] += 1
                witnesses.update(bytes((arc_index, line_index, matrix_index >> 8,
                                         matrix_index & 255, color, *witness)))
                expanded_cases += 1
    require(expanded_cases == 17 * 2016 == 34272, "expanded orbit coverage")

    result = {
        "status": "ACCEPTED_WITH_HILL_LOVE_CLASSIFICATION_IMPORTED",
        "target_ref": TARGET_REF,
        "dependency_ref": DEPENDENCY_REF,
        "target_commit": TARGET_COMMIT,
        "projective_points_and_lines": 57,
        "representative_profiles": [list(profile) for profile in profiles],
        "empty_lines": [len(lines) for lines in empty_lines],
        "gl2_matrices_per_chart": len(gl2),
        "expanded_affine_linear_cases": expanded_cases,
        "blue_red_witnesses": colors,
        "translation_color_checks": translation_checks,
        "witness_stream_sha256": witnesses.hexdigest(),
        "certificate_sha256": sha256(certificate_raw).hexdigest(),
        "classification_recomputed": False,
        "imported_theorem": (
            "Hill--Love (2003): exactly three projective equivalence classes "
            "of 22-point four-arcs in PG(2,7)."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
