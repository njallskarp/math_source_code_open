#!/usr/bin/env python3
"""Arb/Krawczyk certificate for the n=16 fixed-code stationary point."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, arb_mat, ctx


HERE = Path(__file__).resolve().parent
N = 16
DIMENSION = N + 1  # 15 free angles and two Lagrange multipliers


def signs(text: str) -> list[int]:
    if set(text) - {"+", "-"}:
        raise ValueError("a code may contain only '+' and '-'")
    return [1 if char == "+" else -1 for char in text]


def half_code(quarter: list[int]) -> list[int]:
    return quarter + [-value for value in reversed(quarter)]


def full_code(half: list[int]) -> list[int]:
    return half + [-value for value in half]


def negative_run_composition(code: list[int]) -> list[int]:
    runs = []
    for i, value in enumerate(code):
        if value == -1 and code[i - 1] == 1:
            length = 0
            while code[(i + length) % len(code)] == -1:
                length += 1
            runs.append(length)
    return runs


def stationarity(z: list[arb], code: list[int]) -> arb_mat:
    """Gradient of f+y_1 g_1+y_2 g_2 and the two constraints.

    We use f=-P/2, which is the normalization matching the displayed
    first-derivative formula in Mulansky--Potschka. Scaling f does not alter
    the maximizing angles.
    """
    phi = [arb(0)] + z[: N - 1] + [arb.pi()]
    y1, y2 = z[N - 1], z[N]
    result = []
    for j in range(1, N):
        a = code[j - 1] - code[j]
        left = (phi[j] - phi[j - 1]) / 2
        right = (phi[j + 1] - phi[j]) / 2
        result.append(
            (right.cos() - left.cos()) / 2
            + a * (y2 * phi[j].cos() - y1 * phi[j].sin())
        )
    result.append(
        sum(
            (code[j - 1] - code[j]) * phi[j].cos()
            for j in range(1, N)
        )
        - (code[0] + code[N - 1])
    )
    result.append(
        sum(
            (code[j - 1] - code[j]) * phi[j].sin()
            for j in range(1, N)
        )
    )
    return arb_mat([[value] for value in result])


def kkt_jacobian(z: list[arb], code: list[int]) -> arb_mat:
    """Definition-first Jacobian of stationarity, evaluated by Arb."""
    phi = [arb(0)] + z[: N - 1] + [arb.pi()]
    y1, y2 = z[N - 1], z[N]
    matrix = [[arb(0) for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    for j in range(1, N):
        row = j - 1
        a = code[j - 1] - code[j]
        left = (phi[j] - phi[j - 1]) / 2
        right = (phi[j + 1] - phi[j]) / 2
        matrix[row][row] = (
            (left.sin() + right.sin()) / 4
            + a * (-y1 * phi[j].cos() - y2 * phi[j].sin())
        )
        if j > 1:
            matrix[row][row - 1] = -left.sin() / 4
        if j < N - 1:
            matrix[row][row + 1] = -right.sin() / 4
        matrix[row][N - 1] = matrix[N - 1][row] = -a * phi[j].sin()
        matrix[row][N] = matrix[N][row] = a * phi[j].cos()
    return arb_mat(matrix)


def interval_ldl_pivots(matrix: arb_mat) -> list[arb]:
    """Interval LDL^T without pivoting; every returned pivot is enclosed."""
    size = matrix.nrows()
    lower = [[arb(0) for _ in range(size)] for _ in range(size)]
    pivots = []
    for i in range(size):
        lower[i][i] = arb(1)
    for k in range(size):
        pivot = matrix[k, k]
        for s in range(k):
            pivot -= lower[k][s] * lower[k][s] * pivots[s]
        if pivot.contains(0):
            raise AssertionError(f"LDL pivot {k + 1} contains zero")
        pivots.append(pivot)
        for i in range(k + 1, size):
            entry = matrix[i, k]
            for s in range(k):
                entry -= lower[i][s] * lower[k][s] * pivots[s]
            lower[i][k] = entry / pivot
    return pivots


def perimeter_box(z: list[arb]) -> arb:
    phi = [arb(0)] + z[: N - 1] + [arb.pi()]
    return sum(2 * ((phi[j + 1] - phi[j]) / 2).sin() for j in range(N))


def verify() -> dict[str, object]:
    data = json.loads((HERE / "candidate.json").read_text())
    ctx.prec = int(data["arb_precision_bits"])

    quarter = signs(data["quarter_code"])
    code = half_code(quarter)
    complete_code = full_code(code)
    assert code == signs(data["half_code"])
    assert complete_code == signs(data["full_code"])
    assert negative_run_composition(complete_code) == data["negative_run_composition"]

    center_strings = (
        data["phi_2_to_phi_16"] + [data["lambda_1"], data["lambda_2"]]
    )
    # mid() makes each center coordinate a fixed exact dyadic number.
    center = [arb(value).mid() for value in center_strings]
    radius = arb(data["box_radius"]).upper()
    displacement = [arb(0, radius) for _ in range(DIMENSION)]
    box = [center[i] + displacement[i] for i in range(DIMENSION)]

    # A is a fixed exact dyadic approximate inverse, as required by Krawczyk.
    approximate_inverse = kkt_jacobian(center, code).inv().mid()
    identity = arb_mat(
        [[int(i == j) for j in range(DIMENSION)] for i in range(DIMENSION)]
    )
    defect = identity - approximate_inverse * kkt_jacobian(box, code)
    center_column = arb_mat([[value] for value in center])
    displacement_column = arb_mat([[value] for value in displacement])
    krawczyk = (
        center_column
        - approximate_inverse * stationarity(center, code)
        + defect * displacement_column
    )
    inclusion = [
        box[i].contains_interior(krawczyk[i, 0]) for i in range(DIMENSION)
    ]
    if not all(inclusion):
        raise AssertionError("Krawczyk image is not strictly inside the box")

    row_bounds = []
    for i in range(DIMENSION):
        bound = arb(0)
        for j in range(DIMENSION):
            bound += abs(defect[i, j])
        row_bounds.append(bound)
    if not all(bound < 1 for bound in row_bounds):
        raise AssertionError("the interval Jacobian regularity bound failed")

    pivots = interval_ldl_pivots(kkt_jacobian(box, code))
    signs_of_pivots = ["+" if pivot > 0 else "-" for pivot in pivots]
    expected_signs = ["+"] * (N - 1) + ["-", "-"]
    if signs_of_pivots != expected_signs:
        raise AssertionError("unexpected KKT inertia")

    phi_box = [arb(0)] + box[: N - 1] + [arb.pi()]
    gaps = [phi_box[j + 1] - phi_box[j] for j in range(N)]
    if not all(gap > 0 for gap in gaps):
        raise AssertionError("an angle-ordering inequality may be active")

    perimeter = perimeter_box(box)
    if not perimeter.contains(arb(data["center_perimeter"])):
        raise AssertionError("high-precision center perimeter is outside the enclosure")
    if not data["center_perimeter"].startswith(data["published_perimeter"]):
        raise AssertionError("high-precision value does not extend the published digits")

    krawczyk_ratios = [
        (krawczyk[i, 0] - center[i]).abs_upper() / radius
        for i in range(DIMENSION)
    ]
    max_ratio = max(krawczyk_ratios, key=float)
    max_row_bound = max(row_bounds, key=lambda value: float(value.abs_upper()))
    min_gap = min(gaps, key=lambda value: float(value.lower()))
    return {
        "krawczyk_strict_inclusion": True,
        "box_radius": data["box_radius"],
        "max_krawczyk_radius_ratio": max_ratio.str(12),
        "jacobian_defect_infinity_norm_upper": max_row_bound.abs_upper().str(12),
        "ldl_pivot_signs": "".join(signs_of_pivots),
        "angle_gaps_strictly_positive": True,
        "minimum_angle_gap": min_gap.str(30),
        "perimeter_enclosure": perimeter.str(125),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
