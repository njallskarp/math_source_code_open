#!/usr/bin/env python3
"""Dependency-free exact certificate for the n=16 symmetry quotient.

The checker works in the free signed-edge module.  It acts simultaneously on
the full antiperiodic code and on the labeled difference-body edges, so it
checks closure and reconstruction equivariance rather than only comparing
sign strings.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 16
FULL = 2 * N


def parse_code(text: str) -> tuple[int, ...]:
    if len(text) != N or any(char not in "+-" for char in text):
        raise ValueError("a half-code must contain exactly sixteen signs")
    return tuple(1 if char == "+" else -1 for char in text)


def code_string(code: tuple[int, ...]) -> str:
    return "".join("+" if value == 1 else "-" for value in code)


def antiperiodic_extension(half: tuple[int, ...]) -> tuple[int, ...]:
    if len(half) != N or any(value not in (-1, 1) for value in half):
        raise ValueError("invalid half-code")
    return half + tuple(-value for value in half)


def code_action(
    full_code: tuple[int, ...], shift: int, reflected: bool
) -> tuple[int, ...]:
    """Return T_j=C_(j+s) or T_j=C_(s-j), with indices modulo 32."""
    if len(full_code) != FULL:
        raise ValueError("the full code must have length thirty-two")
    if reflected:
        return tuple(full_code[(shift - j) % FULL] for j in range(FULL))
    return tuple(full_code[(j + shift) % FULL] for j in range(FULL))


def normalized_half(full_code: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    multiplier = 1 if full_code[0] == 1 else -1
    normalized = tuple(multiplier * full_code[j] for j in range(N))
    if normalized[0] != 1:
        raise AssertionError("normalization failed")
    return normalized, multiplier


def signed_half_edge(index: int) -> tuple[int, int]:
    """Represent E_index as sign*E_basis for E_(j+16)=-E_j."""
    residue = index % FULL
    if residue < N:
        return residue, 1
    return residue - N, -1


def transformed_selected_edges(
    representative: tuple[int, ...], shift: int, reflected: bool
) -> tuple[tuple[int, int], ...]:
    """Return selected edges after stripping the common orthogonal map.

    An orientation-reversing relabeling has E'_j=-A E_(s-j); the extra minus
    is part of each returned coefficient.  Pairs are (source basis, sign).
    """
    full_code = antiperiodic_extension(representative)
    transformed = code_action(full_code, shift, reflected)
    half, normalization = normalized_half(transformed)
    result = []
    for j in range(N):
        source = (shift - j) % FULL if reflected else (j + shift) % FULL
        basis, edge_sign = signed_half_edge(source)
        orientation_sign = -1 if reflected else 1
        result.append(
            (basis, half[j] * orientation_sign * edge_sign)
        )
    return tuple(result)


def expected_selected_edges(
    representative: tuple[int, ...], polygon_factor: int
) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted((j, polygon_factor * representative[j]) for j in range(N))
    )


def verify() -> dict[str, object]:
    certificate = json.loads((HERE / "symmetry_quotient_certificate.json").read_text())
    exclusion = json.loads(
        (HERE / certificate["code_exclusion_source"]).read_text()
    )
    representative = parse_code(certificate["representative_half_code"])
    full_code = antiperiodic_extension(representative)
    if len(full_code) != certificate["full_code_length"]:
        raise AssertionError("unexpected full-code length")
    if any(full_code[j + N] != -full_code[j] for j in range(N)):
        raise AssertionError("the full code is not antiperiodic")

    expected_survivors = set(exclusion["survivors"])
    witnesses: dict[str, list[dict[str, object]]] = defaultdict(list)
    cyclic_survivors: set[str] = set()
    endpoint_actions_checked = 0

    for reflected in (False, True):
        for shift in range(FULL):
            transformed = code_action(full_code, shift, reflected)
            half, normalization = normalized_half(transformed)
            if antiperiodic_extension(half) != tuple(
                normalization * value for value in transformed
            ):
                raise AssertionError("normalization broke antiperiodicity")

            key = code_string(half)
            polygon_factor = normalization * (-1 if reflected else 1)
            selected = tuple(
                sorted(transformed_selected_edges(representative, shift, reflected))
            )
            if selected != expected_selected_edges(representative, polygon_factor):
                raise AssertionError("reconstruction edge multiset is not equivariant")

            # The sum of selected edges is the closure residual in the free
            # signed-edge module, so entrywise equality also proves
            # G'=(polygon_factor) A G for the common orthogonal map A.
            coefficients = [0] * N
            for basis, sign in selected:
                coefficients[basis] += sign
            expected_coefficients = [
                polygon_factor * representative[j] for j in range(N)
            ]
            if coefficients != expected_coefficients:
                raise AssertionError("closure residual is not equivariant")

            gap_sources = tuple(
                ((shift - j) if reflected else (j + shift)) % N
                for j in range(N)
            )
            if sorted(gap_sources) != list(range(N)):
                raise AssertionError("gap action is not a permutation")

            witnesses[key].append(
                {
                    "shift": shift,
                    "reflected": reflected,
                    "normalization_sign": normalization,
                    "polygon_factor_after_isometry": polygon_factor,
                }
            )
            if not reflected:
                cyclic_survivors.add(key)
            if shift in (0, N - 1, N, FULL - 1):
                endpoint_actions_checked += 1

    action_count = sum(len(value) for value in witnesses.values())
    if action_count != certificate["full_dihedral_action_count"]:
        raise AssertionError("the full dihedral action list is incomplete")
    if len(witnesses) != certificate["normalized_survivor_count"]:
        raise AssertionError("unexpected normalized orbit size")
    if set(witnesses) != expected_survivors:
        raise AssertionError("the quotient orbit does not equal the certified survivors")
    if cyclic_survivors != expected_survivors:
        raise AssertionError("reflections add a new normalized code")
    if any(
        len(entries) != certificate["witnesses_per_normalized_survivor"]
        for entries in witnesses.values()
    ):
        raise AssertionError("unexpected orbit multiplicity")

    # For this representative the formal reflection is already a shift and a
    # global sign: C_(s-j)=-C_(j+15-s).  This explains structurally why the
    # normalized dihedral orbit is only the sixteen-element cyclic orbit.
    offset = int(certificate["reflection_shift_offset"])
    for shift in range(FULL):
        for j in range(FULL):
            if full_code[(shift - j) % FULL] != -full_code[(j + offset - shift) % FULL]:
                raise AssertionError("reflection-to-shift identity failed")

    canonical_witnesses = []
    for code in sorted(witnesses):
        choices = [
            witness
            for witness in witnesses[code]
            if not witness["reflected"] and witness["shift"] < N
        ]
        if len(choices) != 1:
            raise AssertionError("a unique canonical cyclic witness was not found")
        canonical_witnesses.append({"code": code, **choices[0]})

    return {
        "exact_symmetry_quotient": True,
        "model": "free signed-edge module with E_(j+16)=-E_j",
        "normalized_survivor_count": len(witnesses),
        "full_dihedral_actions_checked": action_count,
        "cyclic_orbit_already_complete": cyclic_survivors == expected_survivors,
        "witnesses_per_survivor": sorted({len(value) for value in witnesses.values()}),
        "reflection_identity": "C_(s-j)=-C_(j+15-s)",
        "endpoint_actions_checked": endpoint_actions_checked,
        "closure_equivariance": "G_prime=mu*A*G",
        "reconstruction_equivariance": "Edges(P_prime)=mu*A*Edges(P)",
        "canonical_cyclic_witnesses": canonical_witnesses,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
