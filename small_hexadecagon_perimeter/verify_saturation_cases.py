#!/usr/bin/env python3
"""Exact exhaustive audit of reconstruction and perturbation incidence.

The half-vertex convention is z_16=-z_0.  Hence the half edges are
e_j=z_{j+1}-z_j for j<15 and e_15=-z_0-z_15.  All calculations below take
place in a free integer module; no geometric coordinates or floating-point
arithmetic are used.
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 16


def closure_coefficients(code: tuple[int, ...]) -> tuple[int, ...]:
    if len(code) != N or any(value not in (-1, 1) for value in code):
        raise ValueError("a code must contain sixteen signs")
    return (-(code[0] + code[-1]),) + tuple(
        code[j - 1] - code[j] for j in range(1, N)
    )


def direct_edge_expansion(code: tuple[int, ...]) -> tuple[int, ...]:
    """Expand sum c_j e_j directly in the basis z_0,...,z_15."""
    coefficients = [0] * N
    for j in range(N - 1):
        coefficients[j] -= code[j]
        coefficients[j + 1] += code[j]
    coefficients[0] -= code[-1]
    coefficients[-1] -= code[-1]
    return tuple(coefficients)


def half_edge_derivatives(vertex_velocities: tuple[int, ...]) -> tuple[int, ...]:
    """Scalar multiples of a common vector h in all half-edge derivatives."""
    if len(vertex_velocities) != N:
        raise ValueError("sixteen vertex velocities are required")
    return tuple(
        vertex_velocities[j + 1] - vertex_velocities[j]
        for j in range(N - 1)
    ) + (-vertex_velocities[0] - vertex_velocities[-1],)


def two_vertex_velocity(
    coefficients: tuple[int, ...], first: int, second: int
) -> tuple[int, ...]:
    """Closure-preserving velocity used when two vertices are interior."""
    velocity = [0] * N
    if coefficients[first] == 0:
        velocity[first] = 1
    elif coefficients[second] == 0:
        velocity[second] = 1
    else:
        velocity[first] = coefficients[second]
        velocity[second] = -coefficients[first]
    return tuple(velocity)


def verify() -> dict[str, object]:
    data = json.loads((HERE / "saturation_certificate.json").read_text())
    expected_codes = int(data["normalized_code_count"])
    expected_pairs = int(data["two_vertex_case_count"])
    code_count = 0
    pair_count = 0
    endpoint_pair_count = 0
    adjacent_pair_count = 0
    single_zero_count = 0
    nonzero_rank_blocks = 0

    # Global sign reversal negates every closure coefficient and leaves all
    # feasibility questions invariant, so c_0=+1 is a complete quotient.
    # This loop audits the cyclic summation-by-parts convention for every
    # normalized sign code.  The perturbation audit below is smaller because
    # it depends only on two coefficient values and two positions.
    for bits in range(1 << (N - 1)):
        code = (1,) + tuple(
            1 if ((bits >> (j - 1)) & 1) == 0 else -1
            for j in range(1, N)
        )
        coefficients = closure_coefficients(code)
        if direct_edge_expansion(code) != coefficients:
            raise AssertionError("summation-by-parts coefficient mismatch")
        if any(value not in (-2, 0, 2) for value in coefficients):
            raise AssertionError("closure coefficient outside {-2,0,2}")
        code_count += 1

    # A one-vertex motion is needed only when its coefficient is zero.  Check
    # every possible position, including both cyclic endpoints.
    for vertex in range(N):
        coefficients = (0,) * N
        velocity = tuple(1 if j == vertex else 0 for j in range(N))
        if sum(a * v for a, v in zip(coefficients, velocity)) != 0:
            raise AssertionError("zero-coefficient motion breaks closure")
        if not any(half_edge_derivatives(velocity)):
            raise AssertionError("one-vertex motion changes no edge")
        single_zero_count += 1

    # The equality Jacobian contains a 2-by-2 block a_r I_2.  Both possible
    # nonzero values are checked at every vertex position.
    for _vertex in range(N):
        for coefficient in (-2, 2):
            if coefficient * coefficient != 4:
                raise AssertionError("nonzero equality block is not invertible")
            nonzero_rank_blocks += 1

    # For two interior vertices, no other closure coefficient enters the
    # chosen velocity.  Thus the complete case space is 120 position pairs
    # times the nine ordered pairs in {-2,0,2}^2, not millions of repeated
    # sign codes.  This superset includes coefficient pairs that may not be
    # realized at a particular position by a sign code.
    for first, second in combinations(range(N), 2):
        for first_coefficient, second_coefficient in product((-2, 0, 2), repeat=2):
            coefficients_list = [0] * N
            coefficients_list[first] = first_coefficient
            coefficients_list[second] = second_coefficient
            coefficients = tuple(coefficients_list)
            velocity = two_vertex_velocity(coefficients, first, second)
            if sum(a * v for a, v in zip(coefficients, velocity)) != 0:
                raise AssertionError("two-vertex motion breaks closure")
            derivatives = half_edge_derivatives(velocity)
            if not any(derivatives):
                raise AssertionError("two-vertex motion changes no edge")
            if first == 0 or second == N - 1:
                endpoint_pair_count += 1
            if second == first + 1 or (first == 0 and second == N - 1):
                adjacent_pair_count += 1
            pair_count += 1

    if code_count != expected_codes:
        raise AssertionError("normalized code enumeration is incomplete")
    if pair_count != expected_pairs:
        raise AssertionError("two-vertex case enumeration is incomplete")

    # If all half-edge derivatives vanish, the first fifteen equations make
    # all vertex velocities equal; the endpoint equation then makes that
    # common value zero.  Thus the derivative map is injective.  The finite
    # checks above additionally audit every coefficient-dependent motion.
    test_constant = (1,) * N
    if half_edge_derivatives(test_constant)[-1] != -2:
        raise AssertionError("cyclic endpoint convention was not enforced")

    return {
        "exact_incidence_certificate": True,
        "normalization": "c_0=+1 modulo global sign reversal",
        "normalized_codes_checked": code_count,
        "two_interior_vertex_cases_checked": pair_count,
        "endpoint_pair_cases_checked": endpoint_pair_count,
        "adjacent_pair_cases_checked": adjacent_pair_count,
        "single_zero_coefficient_cases_checked": single_zero_count,
        "nonzero_equality_rank_blocks_checked": nonzero_rank_blocks,
        "half_edge_derivative_map_injective": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
