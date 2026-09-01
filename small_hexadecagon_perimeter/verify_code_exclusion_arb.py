#!/usr/bin/env python3
"""Independent 512-bit Arb certificate for the n=16 code exclusion."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


HERE = Path(__file__).resolve().parent
N = 16


def code_from_bits(bits: int) -> tuple[int, ...]:
    return (1,) + tuple(
        1 if ((bits >> (j - 1)) & 1) == 0 else -1 for j in range(1, N)
    )


def code_string(code: tuple[int, ...]) -> str:
    return "".join("+" if value == 1 else "-" for value in code)


def dihedral_orbit(representative: tuple[int, ...]) -> set[tuple[int, ...]]:
    full = representative + tuple(-value for value in representative)
    orbit: set[tuple[int, ...]] = set()
    for shift in range(2 * N):
        rotated = full[shift:] + full[:shift]
        reflected = tuple(rotated[(-j) % (2 * N)] for j in range(2 * N))
        for transformed in (rotated, reflected):
            half = transformed[:N]
            if half[0] < 0:
                half = tuple(-value for value in half)
            orbit.add(half)
    return orbit


def verify() -> dict[str, object]:
    data = json.loads((HERE / "code_exclusion_certificate.json").read_text())
    ctx.prec = int(data["arb_precision_bits"])
    radius_squared = arb(data["squared_gap_radius_upper"])
    radius = radius_squared.sqrt()
    pi = arb.pi()
    roots = [
        ((j * pi / N).cos(), (j * pi / N).sin()) for j in range(N + 1)
    ]
    edges = [
        (roots[j + 1][0] - roots[j][0], roots[j + 1][1] - roots[j][1])
        for j in range(N)
    ]
    dirichlet_constant = 1 / (4 * (pi / 32).sin() ** 2)
    remainder = dirichlet_constant * radius_squared
    universal_margin_claim = arb(data["universal_screen_margin_lower"])
    spectral_margin_claim = arb(data["spectral_screen_margin_lower"])

    green = [
        [arb(min(j, k) * (N - max(j, k))) / N for k in range(1, N)]
        for j in range(1, N)
    ]

    def residual(code: tuple[int, ...]) -> arb:
        real = arb(0)
        imag = arb(0)
        for coefficient, edge in zip(code, edges):
            real += coefficient * edge[0]
            imag += coefficient * edge[1]
        return (real * real + imag * imag).sqrt()

    def gram_entry(left: list[arb], right: list[arb]) -> arb:
        value = arb(0)
        for j in range(N - 1):
            for k in range(N - 1):
                value += left[j] * green[j][k] * right[k]
        return value

    universal_survivors: list[tuple[int, ...]] = []
    for bits in range(1 << (N - 1)):
        code = code_from_bits(bits)
        switches = sum(code[j - 1] != code[j] for j in range(1, N))
        sigma_bound = 2 * (dirichlet_constant * switches).sqrt()
        margin = residual(code) - radius * sigma_bound - remainder
        if margin > 0:
            if not margin > universal_margin_claim:
                raise AssertionError("universal-screen margin is too small")
        else:
            universal_survivors.append(code)

    if len(universal_survivors) != int(data["universal_screen_survivor_count"]):
        raise AssertionError("unexpected Arb universal-screen survivor count")

    final_survivors: list[tuple[int, ...]] = []
    for code in universal_survivors:
        coefficients = [code[j - 1] - code[j] for j in range(1, N)]
        real = [-coefficients[j - 1] * roots[j][1] for j in range(1, N)]
        imag = [coefficients[j - 1] * roots[j][0] for j in range(1, N)]
        gram_00 = gram_entry(real, real)
        gram_11 = gram_entry(imag, imag)
        gram_01 = gram_entry(real, imag)
        eigenvalue = (
            gram_00
            + gram_11
            + ((gram_00 - gram_11) ** 2 + 4 * gram_01**2).sqrt()
        ) / 2
        sigma = eigenvalue.sqrt()
        margin = residual(code) - radius * sigma - remainder
        if margin > 0:
            if not margin > spectral_margin_claim:
                raise AssertionError("Arb spectral margin is too small")
        else:
            final_survivors.append(code)

    representative = tuple(
        1 if symbol == "+" else -1 for symbol in data["representative_half_code"]
    )
    orbit = dihedral_orbit(representative)
    if set(final_survivors) != orbit:
        raise AssertionError("Arb survivors are not exactly the dihedral orbit")

    return {
        "arb_certificate": True,
        "precision_bits": ctx.prec,
        "normalized_codes_checked": 1 << (N - 1),
        "universal_screen_survivors": len(universal_survivors),
        "spectral_screen_survivors": len(final_survivors),
        "survivors": sorted(code_string(code) for code in final_survivors),
        "dihedral_orbit_size": len(orbit),
        "universal_screen_margin_lower": data["universal_screen_margin_lower"],
        "spectral_screen_margin_lower": data["spectral_screen_margin_lower"],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
