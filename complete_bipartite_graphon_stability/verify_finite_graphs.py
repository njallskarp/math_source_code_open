#!/usr/bin/env python3
"""Exact finite-step checks for the quantitative K_(s,t) inequality.

This program validates normalization and finite specializations.  Exhaustive
finite checks do not prove the graphon theorem in README.md.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import platform
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class OrientedMoments:
    density: Fraction
    p: Fraction
    degree_variance: Fraction
    common_mean: Fraction
    common_variance: Fraction
    nonlinear_bound: Fraction
    linear_bound: Fraction


def neighbor_masks(n: int, edge_mask: int) -> tuple[int, ...]:
    """Decode the canonical lexicographic edge bit ordering."""
    neighbors = [0] * n
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (edge_mask >> bit) & 1:
                neighbors[i] |= 1 << j
                neighbors[j] |= 1 << i
            bit += 1
    return tuple(neighbors)


def oriented_moments(
    neighbors: tuple[int, ...], s: int, t: int
) -> OrientedMoments:
    """Compute every term of the s-oriented bound using exact fractions."""
    if s < 2 or t < 2:
        raise ValueError("s and t must both be at least two")
    n = len(neighbors)
    if n == 0:
        raise ValueError("the host graph must have at least one vertex")

    degrees = tuple(mask.bit_count() for mask in neighbors)
    p = Fraction(sum(degrees), n * n)
    normalized_degrees = tuple(Fraction(degree, n) for degree in degrees)
    degree_variance = sum((degree - p) ** 2 for degree in normalized_degrees) / n

    all_vertices = (1 << n) - 1
    common_values: list[Fraction] = []
    for vertices in itertools.product(range(n), repeat=s):
        common = all_vertices
        for vertex in vertices:
            common &= neighbors[vertex]
        common_values.append(Fraction(common.bit_count(), n))

    tuple_count = n**s
    common_mean = sum(common_values) / tuple_count
    degree_moment = sum(degree**s for degree in normalized_degrees) / n
    if common_mean != degree_moment:
        raise AssertionError("Fubini/common-neighborhood normalization mismatch")

    common_variance = (
        sum((value - common_mean) ** 2 for value in common_values) / tuple_count
    )
    density = sum(value**t for value in common_values) / tuple_count

    a_s = p**s + (s - 1) * p ** (s - 2) * degree_variance
    nonlinear_bound = (
        a_s**t + (t - 1) * common_mean ** (t - 2) * common_variance
    )
    linear_bound = (
        p ** (s * t)
        + t * (s - 1) * p ** (s * t - 2) * degree_variance
        + (t - 1) * common_mean ** (t - 2) * common_variance
    )
    return OrientedMoments(
        density=density,
        p=p,
        degree_variance=degree_variance,
        common_mean=common_mean,
        common_variance=common_variance,
        nonlinear_bound=nonlinear_bound,
        linear_bound=linear_bound,
    )


def brute_hom_density(
    neighbors: tuple[int, ...], s: int, t: int
) -> Fraction:
    """Definition-level enumeration of all maps K_(s,t) -> G."""
    n = len(neighbors)
    homomorphisms = 0
    for image in itertools.product(range(n), repeat=s + t):
        left = image[:s]
        right = image[s:]
        if all((neighbors[x] >> y) & 1 for x in left for y in right):
            homomorphisms += 1
    return Fraction(homomorphisms, n ** (s + t))


def check_cut_reduction_components(
    neighbors: tuple[int, ...], s: int
) -> None:
    """Check the exact finite counterparts of the all-K_(s,t) cut reduction."""
    if s < 2:
        raise ValueError("s must be at least two")
    n = len(neighbors)
    degrees = tuple(Fraction(mask.bit_count(), n) for mask in neighbors)
    p = sum(degrees) / n
    degree_variance = sum((degree - p) ** 2 for degree in degrees) / n
    all_vertices = (1 << n) - 1

    def common_density(vertices: tuple[int, ...]) -> Fraction:
        common = all_vertices
        for vertex in vertices:
            common &= neighbors[vertex]
        return Fraction(common.bit_count(), n)

    tuples = tuple(itertools.product(range(n), repeat=s))
    q_values = tuple(common_density(vertices) for vertices in tuples)
    mu_s = sum(q_values) / len(q_values)
    v_s = sum((value - mu_s) ** 2 for value in q_values) / len(q_values)

    taylor_coefficient = Fraction(s * (s - 1), 2)
    if mu_s - p**s > taylor_coefficient * degree_variance:
        raise AssertionError("degree-moment Taylor bound failed")

    h_values: list[Fraction] = []
    for x in range(n):
        for z in range(n):
            remaining = itertools.product(range(n), repeat=s - 2)
            conditional_h = (
                sum(common_density((x, z, *tail)) for tail in remaining)
                / n ** (s - 2)
                - mu_s
            )
            weighted_codegree = sum(
                Fraction(
                    ((neighbors[x] >> y) & 1) * ((neighbors[z] >> y) & 1),
                    n,
                )
                * degrees[y] ** (s - 2)
                for y in range(n)
            )
            if conditional_h != weighted_codegree - mu_s:
                raise AssertionError("conditional Fubini identity failed")
            h_values.append(conditional_h)

            codegree = common_density((x, z))
            weighted_error = weighted_codegree - p ** (s - 2) * codegree
            if weighted_error**2 > (s - 2) ** 2 * degree_variance:
                raise AssertionError("weighted-codegree Lipschitz bound failed")

    h_norm_squared = sum(value**2 for value in h_values) / (n * n)
    if h_norm_squared > v_s:
        raise AssertionError("conditional-expectation contraction failed")


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def run_exhaustion(max_n: int, max_part: int) -> tuple[int, int, str]:
    if max_n < 1:
        raise ValueError("max_n must be positive")
    if max_part < 2:
        raise ValueError("max_part must be at least two")

    graph_count = 0
    inequality_count = 0
    digest = hashlib.sha256()

    for n in range(1, max_n + 1):
        edge_count = n * (n - 1) // 2
        for edge_mask in range(1 << edge_count):
            neighbors = neighbor_masks(n, edge_mask)
            graph_count += 1
            moments: dict[tuple[int, int], OrientedMoments] = {}

            for s in range(2, max_part + 1):
                check_cut_reduction_components(neighbors, s)
                for t in range(2, max_part + 1):
                    current = oriented_moments(neighbors, s, t)
                    moments[s, t] = current
                    reverse = moments.get((t, s))
                    if current.density < current.nonlinear_bound:
                        raise AssertionError(
                            f"nonlinear bound failed at n={n}, mask={edge_mask}, "
                            f"s={s}, t={t}"
                        )
                    if current.nonlinear_bound < current.linear_bound:
                        raise AssertionError(
                            f"linearization failed at n={n}, mask={edge_mask}, "
                            f"s={s}, t={t}"
                        )
                    if reverse is not None and current.density != reverse.density:
                        raise AssertionError("K_(s,t) orientation symmetry failed")

                    if n <= 4 and s <= 3 and t <= 3:
                        brute = brute_hom_density(neighbors, s, t)
                        if current.density != brute:
                            raise AssertionError(
                                f"homomorphism normalization failed at n={n}, "
                                f"mask={edge_mask}, s={s}, t={t}"
                            )

                    record = ":".join(
                        (
                            str(n),
                            str(edge_mask),
                            str(s),
                            str(t),
                            fraction_text(current.density),
                            fraction_text(current.nonlinear_bound),
                            fraction_text(current.linear_bound),
                        )
                    )
                    digest.update(record.encode("ascii"))
                    digest.update(b"\n")
                    inequality_count += 1

    return graph_count, inequality_count, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--max-part", type=int, default=4)
    args = parser.parse_args()

    graph_count, inequality_count, digest = run_exhaustion(
        args.max_n, args.max_part
    )
    print(f"python={platform.python_version()}")
    print(f"max_n={args.max_n}")
    print(f"max_part={args.max_part}")
    print(f"labelled_graphs={graph_count}")
    print(f"oriented_inequalities={inequality_count}")
    print(f"record_sha256={digest}")
    print("status=PASS")


if __name__ == "__main__":
    main()
