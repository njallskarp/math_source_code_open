#!/usr/bin/env python3
"""Exact certificate for the QLP-42 q=41 third-order axis layer."""

from __future__ import annotations

import csv
from collections import defaultdict
from itertools import product
from math import comb
from pathlib import Path

Gaussian = tuple[int, int]

N = 21
FULL = (1 << N) - 1
MASK10 = (1 << 10) - 1
TAU = (1 << (4 - 1)) | (1 << (10 - 1))
ROOTS: tuple[Gaussian, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def scale(value: Gaussian, factor: Gaussian) -> Gaussian:
    return multiply(factor, value)


def norm(value: Gaussian) -> int:
    return value[0] ** 2 + value[1] ** 2


def div_pi(value: Gaussian) -> Gaussian:
    real, imag = value
    assert (real + imag) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def quotient_pi_squared_mod_pi(value: Gaussian) -> int:
    quotient = div_pi(div_pi(value))
    return (quotient[0] + quotient[1]) & 1


def div_one_plus_i(value: Gaussian) -> Gaussian:
    return div_pi(value)


def axis(value: Gaussian) -> int:
    assert value in ROOTS
    return int(value[0] == 0)


def sign(value: Gaussian) -> int:
    assert value in ROOTS
    return int(value in ((-1, 0), (0, -1)))


def local_states() -> tuple[dict[str, object], ...]:
    result = []
    for x, y in product(ROOTS, repeat=2):
        s = div_one_plus_i(subtract(x, y))
        h = div_one_plus_i(add(x, y))
        dot = x[0] * y[0] + x[1] * y[1]
        kind = "equal" if dot == 1 else "opposite" if dot == -1 else "quarter"
        result.append({"x": x, "y": y, "s": s, "h": h, "kind": kind})
    assert len(result) == 16
    return tuple(result)


def verify_local_and_cross_residues() -> tuple[int, int]:
    states = local_states()
    assert sum(row["kind"] == "quarter" for row in states) == 8
    for row in states:
        s, h, kind = row["s"], row["h"], row["kind"]
        assert isinstance(s, tuple) and isinstance(h, tuple)
        assert norm(s) + norm(h) == 2
        if kind == "quarter":
            assert s in ROOTS and h in ROOTS and axis(s) == 1 - axis(h)

    for h_axis in (0, 1):
        sign_pairs = {
            (sign(row["s"]), sign(row["h"]))
            for row in states
            if row["kind"] == "quarter" and axis(row["h"]) == h_axis
        }
        assert sign_pairs == set(product((0, 1), repeat=2))
    opposite_s = {row["s"] for row in states if row["kind"] == "opposite"}
    assert opposite_s == {(1, 1), (1, -1), (-1, 1), (-1, -1)}

    removed_checks = 0
    pi = (1, 1)
    center_checks = 0
    for filler, plus, minus in product(ROOTS, repeat=3):
        if axis(plus) != axis(minus):
            continue
        removed = add(
            multiply(filler, conjugate(plus)),
            multiply(minus, conjugate(filler)),
        )
        expected = 1 ^ sign(plus) ^ sign(minus) ^ axis(filler) ^ axis(plus)
        assert quotient_pi_squared_mod_pi(removed) == expected
        removed_checks += 1

        pi_center = add(
            multiply(scale(filler, pi), conjugate(plus)),
            multiply(minus, conjugate(scale(filler, pi))),
        )
        assert quotient_pi_squared_mod_pi(pi_center) == 1
        center_checks += 1
    assert removed_checks == center_checks == 32
    return removed_checks, center_checks


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def autocorrelation_signature(mask: int) -> int:
    return sum(
        (((mask & rotate(mask, shift)).bit_count() & 1) << (shift - 1))
        for shift in range(1, 11)
    )


def reflected_word(half_mask: int) -> int:
    result = 0
    for shift in range(1, 11):
        if (half_mask >> (shift - 1)) & 1:
            result |= (1 << shift) | (1 << (N - shift))
    return result


def group_b_words() -> dict[tuple[int, int], tuple[int, int]]:
    groups: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])
    seen = bytearray(1 << N)
    for mask in range(1 << N):
        if seen[mask]:
            continue
        orbit = []
        value = mask
        while value not in orbit:
            orbit.append(value)
            value = rotate(value, 1)
        for value in orbit:
            seen[value] = 1
        weight = mask.bit_count()
        invariant = autocorrelation_signature(mask)
        if weight & 1:
            invariant ^= MASK10
        groups[(weight, invariant)][0] += len(orbit)
        groups[(weight, invariant)][1] += 1
    result = {key: (value[0], value[1]) for key, value in groups.items()}
    assert sum(value[0] for value in result.values()) == 1 << N
    assert sum(value[1] for value in result.values()) == 99_880
    burnside = (2**21 + 2 * 2**7 + 6 * 2**3 + 12 * 2) // 21
    assert burnside == 99_880
    return result


def a_features() -> tuple[tuple[int, int, int], ...]:
    features = []
    for axes in range(1 << 10):
        a = reflected_word(axes)
        f = (FULL ^ 1) ^ a
        k_h = 0
        k_s = 0
        for shift in range(1, 11):
            c_a = (a & rotate(a, shift)).bit_count() & 1
            c_f = (f & rotate(f, shift)).bit_count() & 1
            a_shift = (axes >> (shift - 1)) & 1
            tau = (TAU >> (shift - 1)) & 1
            k_h |= (1 ^ a_shift ^ c_a) << (shift - 1)
            k_s |= (1 ^ (1 ^ a_shift) ^ c_f ^ tau) << (shift - 1)

        # The analytic parity identity used to prove wt(b)=0 mod 4.
        r = axes.bit_count()
        sum_c_a = sum(
            (a & rotate(a, shift)).bit_count() & 1 for shift in range(1, 11)
        ) & 1
        assert sum_c_a == (comb(2 * r, 2) & 1) == (r & 1)
        features.append((axes, k_h, k_s))
    return tuple(features)


def coordinate_sum_possible(pair_count: int, target: int) -> bool:
    for center_sign in (-1, 1):
        residual = target - center_sign
        if residual % 2:
            continue
        half = residual // 2
        if abs(half) <= pair_count and (half - pair_count) % 2 == 0:
            return True
    return False


def good_a_counts(
    features: tuple[tuple[int, int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    all_cases = []
    for p, q, _x, _y in CASES:
        target_real, target_imag = p + q, q - p
        per_signature = []
        for invariant in range(1 << 10):
            count = 0
            for axes, k_h, k_s in features:
                active_h = (~(k_h ^ invariant)) & MASK10
                if (active_h & axes).bit_count() & 1:
                    continue
                if (active_h & (~axes & MASK10)).bit_count() & 1:
                    continue

                active_s = (~(k_s ^ invariant)) & MASK10
                real_pairs = (active_s & axes).bit_count()
                imag_pairs = (active_s & (~axes & MASK10)).bit_count()
                if coordinate_sum_possible(real_pairs, target_real) and coordinate_sum_possible(
                    imag_pairs, target_imag
                ):
                    count += 1
            per_signature.append(count)
        all_cases.append(tuple(per_signature))
    return tuple(all_cases)


def classify(
    groups: dict[tuple[int, int], tuple[int, int]],
    good: tuple[tuple[int, ...], ...],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    case_rows = []
    weight_rows = []
    for case, (_p, _q, x, y) in enumerate(CASES):
        target_real, target_imag = x + y - 1, y - x
        by_weight: dict[int, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
        total_labeled = 0
        total_orbits = 0
        total_groups = 0
        for (weight, invariant), (labeled, orbits) in groups.items():
            if weight & 1 or weight > 20:
                continue
            if weight < abs(target_real) or 21 - weight < abs(target_imag):
                continue
            good_a = good[case][invariant]
            if not good_a:
                continue
            # H_A sum zero plus (1) forces weight divisible by four.
            assert weight % 4 == 0
            total_groups += 1
            total_labeled += good_a * labeled
            total_orbits += good_a * orbits
            row = by_weight[weight]
            row[0] += good_a * labeled
            row[1] += good_a * orbits
            row[2] += good_a
            row[3] += 1

        weights = sorted(by_weight)
        case_rows.append(
            {
                "case": str(case),
                "representative": str(CASES[case]).replace(" ", ""),
                "possible_b_imaginary_weights": ",".join(map(str, weights)),
                "labeled_axis_pairs": str(total_labeled),
                "b_rotation_orbits": str(total_orbits),
                "nonzero_weight_signature_groups": str(total_groups),
            }
        )
        for weight in weights:
            values = by_weight[weight]
            weight_rows.append(
                {
                    "case": str(case),
                    "b_imaginary_weight": str(weight),
                    "labeled_axis_pairs": str(values[0]),
                    "b_rotation_orbits": str(values[1]),
                    "compatible_a_signature_pairs": str(values[2]),
                    "nonzero_signatures": str(values[3]),
                }
            )
    return case_rows, weight_rows


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    removed_checks, center_checks = verify_local_and_cross_residues()
    groups = group_b_words()
    features = a_features()
    good = good_a_counts(features)
    case_rows, weight_rows = classify(groups, good)
    root = Path(__file__).resolve().parent
    assert case_rows == read_tsv(root / "case_table.tsv")
    assert weight_rows == read_tsv(root / "weight_table.tsv")

    print("local_states=16")
    print(f"removed_unit_cross_checks={removed_checks}")
    print(f"pi_center_cross_checks={center_checks}")
    print("a_reflected_axis_words=1024")
    print("b_axis_words=2097152")
    print(f"b_weight_signature_groups={len(groups)}")
    print("b_rotation_orbits=99880")
    print("third_order_labeled_axis_pairs=2147483648")
    print("third_order_b_rotation_orbits=102277120")
    for row in case_rows:
        print(
            f"case_{row['case']}={row['labeled_axis_pairs']},"
            f"{row['b_rotation_orbits']},"
            f"weights:{row['possible_b_imaginary_weights']}"
        )
    print("b_imaginary_weight_mod4=verified")
    print("tables=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
