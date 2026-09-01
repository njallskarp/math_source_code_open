#!/usr/bin/env python3
"""Independent high-precision reconstruction of the n=16 fixed-code point."""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp


HERE = Path(__file__).resolve().parent
N = 16


def signs(text: str) -> list[int]:
    return [1 if char == "+" else -1 for char in text]


def half_code(quarter: list[int]) -> list[int]:
    """Apply c_(n-j+1)=-c_j to the supplied first quarter."""
    return quarter + [-value for value in reversed(quarter)]


def stationarity(z: mp.matrix, code: list[int]) -> mp.matrix:
    phi = [mp.mpf(0)] + list(z[: N - 1]) + [mp.pi]
    y1, y2 = z[N - 1], z[N]
    result = []
    for j in range(1, N):
        a = code[j - 1] - code[j]
        left = (phi[j] - phi[j - 1]) / 2
        right = (phi[j + 1] - phi[j]) / 2
        result.append(
            (mp.cos(right) - mp.cos(left)) / 2
            + a * (y2 * mp.cos(phi[j]) - y1 * mp.sin(phi[j]))
        )
    result.append(
        sum(
            (code[j - 1] - code[j]) * mp.cos(phi[j])
            for j in range(1, N)
        )
        - (code[0] + code[N - 1])
    )
    result.append(
        sum(
            (code[j - 1] - code[j]) * mp.sin(phi[j])
            for j in range(1, N)
        )
    )
    return mp.matrix(result)


def jacobian(z: mp.matrix, code: list[int]) -> mp.matrix:
    """Differentiate stationarity directly; do not import verifier code."""
    phi = [mp.mpf(0)] + list(z[: N - 1]) + [mp.pi]
    y1, y2 = z[N - 1], z[N]
    matrix = mp.zeros(N + 1)
    for j in range(1, N):
        row = j - 1
        a = code[j - 1] - code[j]
        left = (phi[j] - phi[j - 1]) / 2
        right = (phi[j + 1] - phi[j]) / 2
        matrix[row, row] = (
            (mp.sin(left) + mp.sin(right)) / 4
            + a * (-y1 * mp.cos(phi[j]) - y2 * mp.sin(phi[j]))
        )
        if j > 1:
            matrix[row, row - 1] = -mp.sin(left) / 4
        if j < N - 1:
            matrix[row, row + 1] = -mp.sin(right) / 4
        matrix[row, N - 1] = matrix[N - 1, row] = -a * mp.sin(phi[j])
        matrix[row, N] = matrix[N, row] = a * mp.cos(phi[j])
    return matrix


def perimeter(z: mp.matrix) -> mp.mpf:
    phi = [mp.mpf(0)] + list(z[: N - 1]) + [mp.pi]
    return sum(2 * mp.sin((phi[j + 1] - phi[j]) / 2) for j in range(N))


def reconstruct() -> tuple[mp.matrix, mp.mpf, mp.mpf, int]:
    data = json.loads((HERE / "candidate.json").read_text())
    code = half_code(signs(data["quarter_code"]))
    mp.mp.dps = 160
    z = mp.matrix([j * mp.pi / N for j in range(1, N)] + [0, 0])
    for iteration in range(20):
        residual = stationarity(z, code)
        if max(abs(value) for value in residual) < mp.mpf("1e-145"):
            break
        z -= mp.lu_solve(jacobian(z, code), residual)
    else:
        raise RuntimeError("Newton iteration did not converge")

    residual_norm = max(abs(value) for value in stationarity(z, code))
    value = perimeter(z)
    expected = mp.mpf(data["published_perimeter"])
    if abs(value - expected) >= mp.mpf("1e-99"):
        raise AssertionError("reconstruction does not match the published perimeter")
    return z, value, residual_norm, iteration


if __name__ == "__main__":
    point, value, residual_norm, iterations = reconstruct()
    print(f"Newton iterations: {iterations}")
    print(f"residual infinity norm: {mp.nstr(residual_norm, 12)}")
    print(f"perimeter: {mp.nstr(value, 145)}")
    print("phi_2,...,phi_16:")
    for coordinate in point[: N - 1]:
        print(mp.nstr(coordinate, 145))
    print(f"lambda_1: {mp.nstr(point[N - 1], 145)}")
    print(f"lambda_2: {mp.nstr(point[N], 145)}")
