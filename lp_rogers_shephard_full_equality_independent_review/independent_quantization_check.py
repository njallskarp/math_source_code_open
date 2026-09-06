#!/usr/bin/env python3
"""Exact adversarial checks for the full Firey equality quantization bridge.

The proof is measure-theoretic.  This standard-library checker independently
tests its finite-measure identities by rational arithmetic, including direct
convex-hull areas rather than relying only on the claimed Gini formula.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product


def gini_area(masses: tuple[F, ...], values: tuple[F, ...]) -> F:
    return sum(
        masses[i] * masses[j] * abs(values[j] - values[i])
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )


def cross(o: tuple[F, F], a: tuple[F, F], b: tuple[F, F]) -> F:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list[tuple[F, F]]) -> list[tuple[F, F]]:
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    lower: list[tuple[F, F]] = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[F, F]] = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def zonotope_area(vectors: list[tuple[F, F]]) -> tuple[F, int]:
    points = [
        (
            sum(bit * vector[0] for bit, vector in zip(bits, vectors)),
            sum(bit * vector[1] for bit, vector in zip(bits, vectors)),
        )
        for bits in product((0, 1), repeat=len(vectors))
    ]
    hull = convex_hull(points)
    twice_area = abs(
        sum(
            hull[i][0] * hull[(i + 1) % len(hull)][1]
            - hull[i][1] * hull[(i + 1) % len(hull)][0]
            for i in range(len(hull))
        )
    )
    return twice_area / 2, len(hull)


def check_case(
    name: str,
    slopes: tuple[F, ...],
    masses: tuple[F, ...],
    raw_levels: tuple[F, ...],
    horizontal: F,
    expected_endpoint_vertices: int,
) -> list[str]:
    assert len(slopes) == len(masses) == len(raw_levels)
    assert all(a < b for a, b in zip(slopes, slopes[1:]))
    assert all(mass > 0 for mass in masses)
    assert all(a <= b for a, b in zip(raw_levels, raw_levels[1:]))

    total_mass = sum(masses)
    original_gini = gini_area(masses, slopes)
    raw_gini = gini_area(masses, raw_levels)
    assert original_gini > 0 and raw_gini > 0
    scale = original_gini / raw_gini
    target = tuple(scale * level for level in raw_levels)
    assert gini_area(masses, target) == original_gini

    lipschitz = max(
        (target[i + 1] - target[i]) / (slopes[i + 1] - slopes[i])
        for i in range(len(slopes) - 1)
    )
    epsilon = 1 / (2 * (1 + lipschitz))
    probes = (-epsilon, -epsilon / 2, F(0), F(2, 5), F(1))
    constant_area = original_gini + horizontal * total_mass

    vertex_counts: list[int] = []
    for time in probes:
        transported = tuple(
            (1 - time) * slope + time * endpoint
            for slope, endpoint in zip(slopes, target)
        )
        assert all(a <= b for a, b in zip(transported, transported[1:]))
        assert gini_area(masses, transported) == original_gini
        vectors = [
            (mass * slope, mass)
            for mass, slope in zip(masses, transported)
        ]
        if horizontal:
            vectors.append((horizontal, F(0)))
        hull_area, vertex_count = zonotope_area(vectors)
        assert hull_area == constant_area
        vertex_counts.append(vertex_count)

    assert vertex_counts[-1] == expected_endpoint_vertices
    return [
        f"{name}_original_gini={original_gini}",
        f"{name}_raw_gini={raw_gini}",
        f"{name}_scale={scale}",
        f"{name}_lipschitz={lipschitz}",
        f"{name}_epsilon={epsilon}",
        f"{name}_constant_area={constant_area}",
        f"{name}_vertex_counts={','.join(map(str, vertex_counts))}",
    ]


def main() -> None:
    lines: list[str] = []
    lines.extend(
        check_case(
            "three_bins_no_horizontal",
            (F(-11), F(-2), F(7, 3), F(19)),
            (F(1, 101), F(7, 13), F(13, 17), F(101, 19)),
            (F(-5), F(-5), F(2), F(9)),
            F(0),
            6,
        )
    )
    lines.extend(
        check_case(
            "two_bins_with_horizontal",
            (F(-1000), F(-3), F(1, 7), F(500)),
            (F(1, 997), F(2, 3), F(5, 11), F(997, 13)),
            (F(-4), F(-4), F(17, 5), F(17, 5)),
            F(37, 23),
            6,
        )
    )
    lines.extend(
        check_case(
            "three_atomic_bins",
            (F(-5, 2), F(0), F(8, 3)),
            (F(3, 7), F(11, 5), F(2, 13)),
            (F(-13), F(1, 9), F(22)),
            F(0),
            6,
        )
    )
    digest = sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    for line in lines:
        print(line)
    print(f"result_sha256={digest}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
