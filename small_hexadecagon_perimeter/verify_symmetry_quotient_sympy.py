#!/usr/bin/env python3
"""Independent SymPy audit of the n=16 code/reconstruction group action."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
N = 16
FULL = 32


def parse(text: str) -> tuple[int, ...]:
    if len(text) != N or any(char not in "+-" for char in text):
        raise ValueError("invalid representative")
    return tuple(1 if char == "+" else -1 for char in text)


def extend(half: tuple[int, ...]) -> tuple[int, ...]:
    return half + tuple(-entry for entry in half)


def full_edge(
    index: int, x: tuple[sp.Symbol, ...], y: tuple[sp.Symbol, ...]
) -> sp.Matrix:
    residue = index % FULL
    sign = 1 if residue < N else -1
    basis = residue if residue < N else residue - N
    return sp.Matrix([sign * x[basis], sign * y[basis]])


def verify() -> dict[str, object]:
    data = json.loads((HERE / "symmetry_quotient_certificate.json").read_text())
    exclusion = json.loads((HERE / data["code_exclusion_source"]).read_text())
    half = parse(data["representative_half_code"])
    code = extend(half)
    expected = set(exclusion["survivors"])

    x = sp.symbols("x0:16")
    y = sp.symbols("y0:16")
    a, b, c, d = sp.symbols("a b c d")
    orthogonal_placeholder = sp.Matrix([[a, b], [c, d]])
    original_residual = sum(
        (half[j] * full_edge(j, x, y) for j in range(N)),
        sp.zeros(2, 1),
    )

    orbit: set[str] = set()
    symbolic_residual_identities = 0
    symbolic_edge_identities = 0
    gap_permutations = 0
    deltas = sp.symbols("delta0:16")

    for reflected in (False, True):
        for shift in range(FULL):
            raw = tuple(
                code[(shift - j) % FULL] if reflected else code[(j + shift) % FULL]
                for j in range(FULL)
            )
            normalization = 1 if raw[0] == 1 else -1
            normalized_half = tuple(normalization * raw[j] for j in range(N))
            orbit.add("".join("+" if entry == 1 else "-" for entry in normalized_half))

            transformed_edges = []
            residual = sp.zeros(2, 1)
            source_indices = []
            for j in range(N):
                source = (shift - j) % FULL if reflected else (j + shift) % FULL
                source_indices.append(source % N)
                edge = orthogonal_placeholder * full_edge(source, x, y)
                if reflected:
                    edge = -edge
                selected = normalized_half[j] * edge
                transformed_edges.append(selected)
                residual += selected

            mu = normalization * (-1 if reflected else 1)
            if any(sp.expand(entry) != 0 for entry in residual - mu * orthogonal_placeholder * original_residual):
                raise AssertionError("symbolic closure equivariance failed")
            symbolic_residual_identities += 1

            expected_edges = [
                mu * orthogonal_placeholder * (half[j] * full_edge(j, x, y))
                for j in range(N)
            ]
            canonical_transformed = sorted(
                (tuple(sp.expand(entry) for entry in vector) for vector in transformed_edges),
                key=str,
            )
            canonical_expected = sorted(
                (tuple(sp.expand(entry) for entry in vector) for vector in expected_edges),
                key=str,
            )
            if canonical_transformed != canonical_expected:
                raise AssertionError("symbolic reconstruction-edge identity failed")
            symbolic_edge_identities += 1

            transformed_gap_sum = sum(deltas[source] for source in source_indices)
            if sp.expand(transformed_gap_sum - sum(deltas)) != 0:
                raise AssertionError("gap/perimeter permutation identity failed")
            gap_permutations += 1

    if orbit != expected or len(orbit) != data["normalized_survivor_count"]:
        raise AssertionError("independent symbolic orbit does not match survivors")

    # Signed shift on the sixteen-dimensional antiperiodic edge module.
    shift_matrix = sp.zeros(N)
    for j in range(N - 1):
        shift_matrix[j + 1, j] = 1
    shift_matrix[0, N - 1] = -1
    if shift_matrix**N != -sp.eye(N) or shift_matrix**FULL != sp.eye(N):
        raise AssertionError("antiperiodic shift relations failed")

    return {
        "sympy_symmetry_quotient": True,
        "coefficient_domain": "ZZ[a,b,c,d,x_0,...,x_15,y_0,...,y_15]",
        "normalized_orbit_size": len(orbit),
        "symbolic_closure_identities": symbolic_residual_identities,
        "symbolic_edge_multiset_identities": symbolic_edge_identities,
        "symbolic_gap_permutations": gap_permutations,
        "antiperiodic_shift_relations": "R^16=-I and R^32=I",
        "orthogonality_used_by_checker": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
