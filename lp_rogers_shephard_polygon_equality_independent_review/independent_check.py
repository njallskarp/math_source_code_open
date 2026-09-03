#!/usr/bin/env python3
"""Independent checks for the planar symmetric Firey polygon equality claim.

This is deliberately not a proof of the universal theorem.  It combines
exact rational checks of the generator-deletion shadow with a definition-level
floating-point reconstruction of Firey bodies from sampled support halfplanes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from fractions import Fraction
from typing import Callable, Iterable, Sequence


TARGET_REF = "bafkreia5tvsipltq7nhjsz6j5m5jxbfk4cxibvunlaq3bvjygtpr3veraa"
RationalPoint = tuple[Fraction, Fraction]
FloatPoint = tuple[float, float]


def det(u: Sequence[object], v: Sequence[object]):
    return u[0] * v[1] - u[1] * v[0]


def add(u: RationalPoint, v: RationalPoint) -> RationalPoint:
    return (u[0] + v[0], u[1] + v[1])


def scale_x(v: RationalPoint, factor: Fraction) -> RationalPoint:
    return (factor * v[0], v[1])


def cross(o: RationalPoint, a: RationalPoint, b: RationalPoint) -> Fraction:
    return det((a[0] - o[0], a[1] - o[1]), (b[0] - o[0], b[1] - o[1]))


def convex_hull(points: Iterable[RationalPoint]) -> list[RationalPoint]:
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower: list[RationalPoint] = []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[RationalPoint] = []
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def subset_sums(generators: Sequence[RationalPoint]) -> list[RationalPoint]:
    points: list[RationalPoint] = [(Fraction(0), Fraction(0))]
    for generator in generators:
        points += [add(point, generator) for point in points]
    return points


def polygon_area_exact(vertices: Sequence[RationalPoint]) -> Fraction:
    twice = sum(det(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices)))
    return abs(twice) / 2


def zonotope_area_formula(generators: Sequence[RationalPoint]) -> Fraction:
    return sum(det(generators[i], generators[j]) for i in range(len(generators)) for j in range(i + 1, len(generators)))


def deletion_parameters(generators: Sequence[RationalPoint]) -> tuple[Fraction, Fraction]:
    y_total = sum((v[1] for v in generators[1:]), Fraction(0))
    q_total = sum(
        (det(generators[i], generators[j]) for i in range(1, len(generators)) for j in range(i + 1, len(generators))),
        Fraction(0),
    )
    assert y_total > 0 and q_total > 0
    return q_total / y_total, y_total + q_total


def deform(generators: Sequence[RationalPoint], s: Fraction) -> list[RationalPoint]:
    lam, _ = deletion_parameters(generators)
    return [((1 + lam * s) * generators[0][0], Fraction(0))] + [
        scale_x(v, 1 - s) for v in generators[1:]
    ]


def support_polygon_area(support: Callable[[float, float], float], normals: int) -> float:
    step = 2.0 * math.pi / normals
    polar_points: list[FloatPoint] = []
    for i in range(normals):
        theta = i * step
        nx, ny = math.cos(theta), math.sin(theta)
        value = support(nx, ny)
        assert value > 0.0
        polar_points.append((nx / value, ny / value))

    # The sampled outer approximation is the polar of the convex hull of
    # n/h(n).  Taking this hull first removes redundant sampled halfplanes;
    # merely intersecting consecutive samples is incorrect near true corners.
    polar_points.sort()

    def float_cross(o: FloatPoint, a: FloatPoint, b: FloatPoint) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[FloatPoint] = []
    for point in polar_points:
        while len(lower) >= 2 and float_cross(lower[-2], lower[-1], point) <= 0.0:
            lower.pop()
        lower.append(point)
    upper: list[FloatPoint] = []
    for point in reversed(polar_points):
        while len(upper) >= 2 and float_cross(upper[-2], upper[-1], point) <= 0.0:
            upper.pop()
        upper.append(point)
    polar_hull = lower[:-1] + upper[:-1]

    vertices: list[FloatPoint] = []
    for i, (ux, uy) in enumerate(polar_hull):
        vx, vy = polar_hull[(i + 1) % len(polar_hull)]
        denominator = ux * vy - uy * vx
        vertices.append(((vy - uy) / denominator, (ux - vx) / denominator))

    twice_area = 0.0
    for i, vertex in enumerate(vertices):
        nxt = vertices[(i + 1) % len(vertices)]
        twice_area += vertex[0] * nxt[1] - vertex[1] * nxt[0]
    return abs(twice_area) / 2.0


def firey_area_from_base_support(
    base_support: Callable[[float, float], float], p: float, normals: int
) -> float:
    def support(nx: float, ny: float) -> float:
        forward = max(0.0, base_support(nx, ny))
        reflected = max(0.0, base_support(-nx, -ny))
        return (forward**p + reflected**p) ** (1.0 / p)

    return support_polygon_area(support, normals)


def adaptive_simpson(
    function: Callable[[float], float], left: float, right: float, tolerance: float = 2e-13
) -> float:
    def simpson(a: float, b: float, fa: float, fm: float, fb: float) -> float:
        return (b - a) * (fa + 4.0 * fm + fb) / 6.0

    middle = (left + right) / 2.0
    f_left, f_middle, f_right = function(left), function(middle), function(right)
    whole = simpson(left, right, f_left, f_middle, f_right)

    def recurse(
        a: float,
        b: float,
        fa: float,
        fm: float,
        fb: float,
        estimate: float,
        tol: float,
        depth: int,
    ) -> float:
        m = (a + b) / 2.0
        lm, rm = (a + m) / 2.0, (m + b) / 2.0
        flm, frm = function(lm), function(rm)
        left_estimate = simpson(a, m, fa, flm, fm)
        right_estimate = simpson(m, b, fm, frm, fb)
        correction = left_estimate + right_estimate - estimate
        if depth == 0 or abs(correction) <= 15.0 * tol:
            return left_estimate + right_estimate + correction / 15.0
        return recurse(a, m, fa, flm, fm, left_estimate, tol / 2.0, depth - 1) + recurse(
            m, b, fm, frm, fb, right_estimate, tol / 2.0, depth - 1
        )

    return recurse(left, right, f_left, f_middle, f_right, whole, tolerance, 30)


def c_q(q: float) -> float:
    return 2.0 * math.gamma(1.0 + 1.0 / q) ** 2 / math.gamma(1.0 + 2.0 / q)


def translated_rectangle_formula(a: float, p: float) -> float:
    side = 1.0 - a
    q = p / (p - 1.0)
    length = (side**p + a**p) ** (1.0 / p)
    alpha = (side / length) ** (p - 1.0)
    beta = (a / length) ** (p - 1.0)

    def integrand(y: float) -> float:
        return (1.0 - y**q) ** (-(q - 1.0) / q)

    arc = adaptive_simpson(integrand, 0.0, beta)
    return 1.0 + length * (alpha + beta) + a * arc + side * (c_q(q) - arc)


def translated_rectangle_support(a: float) -> Callable[[float, float], float]:
    side = 1.0 - a

    def support(nx: float, ny: float) -> float:
        return side * max(nx, 0.0) + a * max(-nx, 0.0) + max(ny, 0.0)

    return support


def zonotope_support(generators: Sequence[RationalPoint]) -> Callable[[float, float], float]:
    converted = [(float(v[0]), float(v[1])) for v in generators]

    def support(nx: float, ny: float) -> float:
        return sum(max(0.0, nx * x + ny * y) for x, y in converted)

    return support


def exact_shadow_audit(generators: Sequence[RationalPoint]) -> dict[str, object]:
    lam, expected_area = deletion_parameters(generators)
    left = -1 / lam
    probes = [left, (left + 0) / 2, Fraction(0), Fraction(1, 2), Fraction(1)]
    areas: list[str] = []
    for s in probes:
        moved = deform(generators, s)
        hull = convex_hull(subset_sums(moved))
        hull_area = polygon_area_exact(hull)
        formula_area = zonotope_area_formula(moved)
        assert hull_area == expected_area == formula_area
        areas.append(str(hull_area))

    side_counts = {}
    for label, s in (("left", left), ("zero", Fraction(0)), ("right", Fraction(1))):
        side_counts[label] = len(convex_hull(subset_sums(deform(generators, s))))
    expected_counts = {"left": 2 * (len(generators) - 1), "zero": 2 * len(generators), "right": 4}
    assert side_counts == expected_counts
    return {
        "generators": [[str(x), str(y)] for x, y in generators],
        "lambda": str(lam),
        "constant_area": str(expected_area),
        "probe_areas": areas,
        "side_counts": side_counts,
    }


def numerical_audit(normals: int) -> dict[str, object]:
    p_values = (1.2, 2.0, 5.0)
    a_values = (0.05, 0.37, 0.83)
    edge_checks = 0
    worst_edge_relative_error = 0.0
    smallest_edge_deficit = math.inf
    for p in p_values:
        q = p / (p - 1.0)
        sharp_constant = 2.0 + c_q(q)
        for a in a_values:
            reconstructed = firey_area_from_base_support(translated_rectangle_support(a), p, normals)
            formula = translated_rectangle_formula(a, p)
            relative_error = abs(reconstructed - formula) / formula
            worst_edge_relative_error = max(worst_edge_relative_error, relative_error)
            smallest_edge_deficit = min(smallest_edge_deficit, sharp_constant - reconstructed)
            edge_checks += 1
    assert worst_edge_relative_error < 2.0e-7
    assert smallest_edge_deficit > 1.0e-3

    generator_cases: tuple[tuple[RationalPoint, ...], ...] = (
        (
            (Fraction(1), Fraction(0)),
            (Fraction(2, 5), Fraction(3, 4)),
            (Fraction(0), Fraction(5, 4)),
        ),
        (
            (Fraction(1), Fraction(0)),
            (Fraction(3, 5), Fraction(1, 4)),
            (Fraction(1, 5), Fraction(5, 4)),
            (Fraction(0), Fraction(3, 2)),
        ),
    )
    convexity_checks = 0
    worst_negative_second_difference = 0.0
    worst_convexity_case: object = None
    largest_ratio_excess = -math.inf
    for generators in generator_cases:
        lam, exact_area = deletion_parameters(generators)
        left = -1.0 / float(lam)
        nodes = [left + (1.0 - left) * i / 8.0 for i in range(9)]
        for p in p_values:
            values: list[float] = []
            q = p / (p - 1.0)
            bound = (2.0 + c_q(q)) * float(exact_area)
            for node_index, node in enumerate(nodes):
                moved = deform(generators, Fraction(node))
                value = firey_area_from_base_support(zonotope_support(moved), p, normals)
                values.append(value)
                # The exact endpoint bodies are parallelogram equality cases,
                # while their sampled outer approximations lie slightly above
                # the true body.  Test the sharp bound only at strict interior
                # nodes, where this discretization artifact cannot mimic equality.
                if 0 < node_index < len(nodes) - 1:
                    largest_ratio_excess = max(
                        largest_ratio_excess,
                        value / float(exact_area) - (2.0 + c_q(q)),
                    )
            # Exclude the two second differences touching endpoint equality
            # bodies, where direction-grid alignment dominates the tiny slack.
            for i in range(2, len(values) - 2):
                second_difference = values[i - 1] - 2.0 * values[i] + values[i + 1]
                normalized = second_difference / bound
                if normalized < worst_negative_second_difference:
                    worst_negative_second_difference = normalized
                    worst_convexity_case = {
                        "generator_count": len(generators),
                        "p": p,
                        "index": i,
                        "nodes": nodes,
                        "values": values,
                    }
                convexity_checks += 1
    assert worst_negative_second_difference > -2.0e-7, (
        worst_negative_second_difference,
        worst_convexity_case,
    )
    assert largest_ratio_excess < -1.0e-4, largest_ratio_excess
    return {
        "normals_per_body": normals,
        "edge_formula_cases": edge_checks,
        "worst_edge_relative_error": f"{worst_edge_relative_error:.12e}",
        "smallest_sampled_edge_deficit": f"{smallest_edge_deficit:.12e}",
        "convexity_second_differences": convexity_checks,
        "worst_normalized_negative_second_difference": f"{worst_negative_second_difference:.12e}",
        "largest_sampled_ratio_excess": f"{largest_ratio_excess:.12e}",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--normals", type=int, default=32768)
    args = parser.parse_args()
    if args.normals < 4096 or args.normals % 8:
        parser.error("--normals must be a multiple of 8 and at least 4096")

    generator_cases: tuple[tuple[RationalPoint, ...], ...] = (
        (
            (Fraction(1), Fraction(0)),
            (Fraction(2, 5), Fraction(3, 4)),
            (Fraction(0), Fraction(5, 4)),
        ),
        (
            (Fraction(1), Fraction(0)),
            (Fraction(3, 5), Fraction(1, 4)),
            (Fraction(1, 5), Fraction(5, 4)),
            (Fraction(0), Fraction(3, 2)),
        ),
    )
    record = {
        "target_ref": TARGET_REF,
        "python": platform.python_version(),
        "exact_shadows": [exact_shadow_audit(case) for case in generator_cases],
        "numerical": numerical_audit(args.normals),
        "trust_boundary": "exact rational shadow checks; non-rigorous IEEE-754 support-halfplane sampling",
    }
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(record, indent=2, sort_keys=True))
    print(
        "worst_edge_relative_error="
        + str(record["numerical"]["worst_edge_relative_error"])
    )
    print(f"result_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
