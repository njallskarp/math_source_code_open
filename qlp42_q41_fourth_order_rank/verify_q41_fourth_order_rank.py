#!/usr/bin/env python3
"""Exact certificate for the QLP-42 q=41 fourth-order lift."""

from __future__ import annotations

import csv
from collections import defaultdict
from itertools import product
from pathlib import Path
from random import Random

Gaussian = tuple[int, int]

N = 21
FULL = (1 << N) - 1
MASK10 = (1 << 10) - 1
PI = (1, 1)
PI2 = (0, 2)
PI3 = (-2, 2)
ROOTS: tuple[Gaussian, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
TARGET_H = (-2, 0)


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


def scale(value: Gaussian, coefficient: int) -> Gaussian:
    return value[0] * coefficient, value[1] * coefficient


def div_pi(value: Gaussian) -> Gaussian:
    real, imag = value
    assert (real + imag) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def pi_valuation_bit(value: Gaussian, power: int) -> int:
    for _ in range(power):
        value = div_pi(value)
    return (value[0] + value[1]) & 1


def congruent_mod_pi_power(left: Gaussian, right: Gaussian, power: int) -> bool:
    value = subtract(left, right)
    try:
        for _ in range(power):
            value = div_pi(value)
    except AssertionError:
        return False
    return True


def unit(axis: int, sign: int) -> Gaussian:
    value = (1, 0) if axis == 0 else (0, 1)
    return scale(value, -1 if sign else 1)


def rotate(mask: int, shift: int, length: int = N) -> int:
    full = (1 << length) - 1
    shift %= length
    return ((mask << shift) | (mask >> (length - shift))) & full


def paf(word: list[Gaussian], shift: int) -> Gaussian:
    result = (0, 0)
    length = len(word)
    for index, value in enumerate(word):
        result = add(result, multiply(value, conjugate(word[(index + shift) % length])))
    return result


def target_s(shift: int) -> Gaussian:
    if shift == 4:
        return -2, 0
    if shift == 10:
        return 2, 0
    return 0, 0


def reflected_axes(half_mask: int) -> int:
    result = 0
    for shift in range(1, 11):
        if (half_mask >> (shift - 1)) & 1:
            result |= (1 << shift) | (1 << (N - shift))
    return result


def autocorrelation_signature(mask: int) -> int:
    parity = mask.bit_count() & 1
    return sum(
        ((parity ^ ((mask & rotate(mask, shift)).bit_count() & 1)) << (shift - 1))
        for shift in range(1, 11)
    )


def d_columns(mask: int) -> tuple[int, ...]:
    columns = []
    for index in range(N):
        column = 0
        for shift in range(1, 11):
            bit = ((mask >> ((index + shift) % N)) ^ (mask >> ((index - shift) % N))) & 1
            column |= bit << (shift - 1)
        columns.append(column)
    return tuple(columns)


def rref(vectors: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    rows = [value for value in vectors if value]
    pivot_row = 0
    for column in range(10):
        pivot = next((row for row in range(pivot_row, len(rows)) if (rows[row] >> column) & 1), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for row in range(len(rows)):
            if row != pivot_row and ((rows[row] >> column) & 1):
                rows[row] ^= rows[pivot_row]
        pivot_row += 1
    return tuple(rows[:pivot_row])


def orthogonal_mask(vectors: tuple[int, ...] | list[int]) -> int:
    basis = rref(vectors)
    result = 0
    for candidate in range(1 << 10):
        if all(((candidate & value).bit_count() & 1) == 0 for value in basis):
            result |= 1 << candidate
    return result


BAD_DOT = tuple(
    sum(1 << witness for witness in range(1 << 10) if (value & witness).bit_count() & 1)
    for value in range(1 << 10)
)


def in_sum_space(value: int, left_orthogonal: int, right_orthogonal: int) -> bool:
    return (left_orthogonal & right_orthogonal & BAD_DOT[value]) == 0


def verify_unit_formula() -> int:
    for axis, sign in product((0, 1), repeat=2):
        expected = add(
            add((1, 0), scale(PI, axis)),
            add(scale(PI2, sign ^ axis), scale(PI3, sign ^ axis ^ (sign & axis))),
        )
        assert congruent_mod_pi_power(unit(axis, sign), expected, 4)

    checks = 0
    length = 5
    for phases in product(range(4), repeat=length):
        axes = tuple(phase & 1 for phase in phases)
        signs = tuple(phase >> 1 for phase in phases)
        word = [unit(axis, sign) for axis, sign in zip(axes, signs)]
        for shift in range(1, 1 + length // 2):
            c_beta = sum(axes[j] & axes[(j + shift) % length] for j in range(length)) & 1
            e_beta = (sum(axes) ^ c_beta) & 1
            d_beta = sum(
                (signs[j] ^ signs[(j + shift) % length])
                & (axes[j] ^ axes[(j + shift) % length])
                for j in range(length)
            ) & 1
            # The linear-axis term occurs an even number of times.  Its
            # exact half-count contributes one further pi^3 coefficient,
            # turning the raw third coefficient into E_beta + D_beta.
            third = e_beta ^ d_beta
            expected = add((1, 0), add(scale(PI2, e_beta), scale(PI3, third)))
            assert congruent_mod_pi_power(paf(word, shift), expected, 4)
            checks += 1
    assert checks == 2048
    return checks


def verify_local_sign_independence() -> int:
    pairs: dict[int, set[tuple[int, int]]] = defaultdict(set)
    quarter_count = 0
    for x, y in product(ROOTS, repeat=2):
        s = div_pi(subtract(x, y))
        h = div_pi(add(x, y))
        if s not in ROOTS or h not in ROOTS:
            continue
        quarter_count += 1
        h_axis = int(h[0] == 0)
        s_axis = int(s[0] == 0)
        assert s_axis == 1 - h_axis
        s_sign = int(s in ((-1, 0), (0, -1)))
        h_sign = int(h in ((-1, 0), (0, -1)))
        pairs[h_axis].add((s_sign, h_sign))
    assert quarter_count == 8
    assert pairs[0] == pairs[1] == set(product((0, 1), repeat=2))
    return quarter_count


def theta_masks(a_half: int, e_signature: int) -> tuple[int, int]:
    a = reflected_axes(a_half)
    f = (FULL ^ 1) ^ a
    theta_h = 0
    theta_s = 0
    for shift in range(1, 11):
        a_shift = (a_half >> (shift - 1)) & 1
        f_shift = 1 ^ a_shift
        c_a = (a & rotate(a, shift)).bit_count() & 1
        c_f = (f & rotate(f, shift)).bit_count() & 1
        e = (e_signature >> (shift - 1)) & 1
        tau = int(shift in (4, 10))
        theta_h |= (1 ^ a_shift ^ c_a ^ e) << (shift - 1)
        theta_s |= (1 ^ f_shift ^ c_f ^ e ^ tau) << (shift - 1)
    return theta_h, theta_s


def a_word(a_half: int, theta: int, component: str, center_phase: int = 0) -> list[Gaussian]:
    a = reflected_axes(a_half)
    axes = a if component == "H" else (FULL ^ 1) ^ a
    word = [(0, 0)] * N
    if component == "S":
        word[0] = multiply(PI, ROOTS[center_phase])
    for shift in range(1, 11):
        axis = (axes >> shift) & 1
        word[shift] = unit(axis, 0)
        word[N - shift] = unit(axis, (theta >> (shift - 1)) & 1)
    return word


def b_word(mask: int, component: str) -> list[Gaussian]:
    axes = mask if component == "H" else FULL ^ mask
    return [unit((axes >> index) & 1, 0) for index in range(N)]


def b_residue(e_bit: int, parity: int, component: str) -> Gaussian:
    del parity, component
    return add((1, 0), add(scale(PI2, e_bit), scale(PI3, e_bit)))


def vector_from_deltas(base: list[Gaussian], variants: list[list[Gaussian]]) -> tuple[int, ...]:
    columns = []
    for variant in variants:
        column = 0
        for shift in range(1, 11):
            delta = subtract(paf(variant, shift), paf(base, shift))
            column |= pi_valuation_bit(delta, 3) << (shift - 1)
        columns.append(column)
    return tuple(columns)


def coupled_base_vector(
    a_values: list[Gaussian], e_signature: int, parity: int, component: str
) -> int:
    result = 0
    for shift in range(1, 11):
        target = TARGET_H if component == "H" else target_s(shift)
        combined = subtract(
            add(a_values[shift - 1], b_residue((e_signature >> (shift - 1)) & 1, parity, component)),
            target,
        )
        result |= pi_valuation_bit(combined, 3) << (shift - 1)
    return result


def a_systems() -> tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
]:
    systems = []
    affine_data = []
    for a_half in range(1 << 10):
        theta_h0, theta_s0 = theta_masks(a_half, 0)
        h_base_word = a_word(a_half, theta_h0, "H")
        h_base_pafs = [paf(h_base_word, shift) for shift in range(1, 11)]
        h_pair_variants = []
        for pair in range(10):
            variant = h_base_word.copy()
            shift = pair + 1
            variant[shift] = scale(variant[shift], -1)
            variant[N - shift] = scale(variant[N - shift], -1)
            h_pair_variants.append(variant)
        h_columns = vector_from_deltas(h_base_word, h_pair_variants)
        h_orthogonal = orthogonal_mask(h_columns)

        h_e_columns = []
        for pair in range(10):
            theta, _ = theta_masks(a_half, 1 << pair)
            word = a_word(a_half, theta, "H")
            values = [paf(word, shift) for shift in range(1, 11)]
            h_e_columns.append(
                coupled_base_vector(values, 1 << pair, 0, "H")
                ^ coupled_base_vector(h_base_pafs, 0, 0, "H")
            )
        h_base00 = coupled_base_vector(h_base_pafs, 0, 0, "H")

        s_bases = []
        s_e_columns_by_center = []
        s_orthogonal = None
        for center in range(4):
            s_base_word = a_word(a_half, theta_s0, "S", center)
            s_base_pafs = [paf(s_base_word, shift) for shift in range(1, 11)]
            s_pair_variants = []
            for pair in range(10):
                variant = s_base_word.copy()
                shift = pair + 1
                variant[shift] = scale(variant[shift], -1)
                variant[N - shift] = scale(variant[N - shift], -1)
                s_pair_variants.append(variant)
            columns = vector_from_deltas(s_base_word, s_pair_variants)
            current_orthogonal = orthogonal_mask(columns)
            if s_orthogonal is None:
                s_orthogonal = current_orthogonal
            else:
                assert s_orthogonal == current_orthogonal

            s_base00 = coupled_base_vector(s_base_pafs, 0, 0, "S")
            s_bases.append(s_base00)
            e_columns = []
            for pair in range(10):
                _, theta = theta_masks(a_half, 1 << pair)
                word = a_word(a_half, theta, "S", center)
                values = [paf(word, shift) for shift in range(1, 11)]
                e_columns.append(
                    coupled_base_vector(values, 1 << pair, 0, "S") ^ s_base00
                )
            s_e_columns_by_center.append(tuple(e_columns))
        assert s_orthogonal is not None
        assert len(set(s_e_columns_by_center)) == 1
        systems.append((h_orthogonal, s_orthogonal))
        affine_data.append(
            (
                (h_base00, *h_e_columns),
                (tuple(s_bases), *s_e_columns_by_center[0]),
            )
        )
    return tuple(systems), tuple(affine_data)


def affine_value(base: int, columns: tuple[int, ...], mask: int, parity: int) -> int:
    del parity
    value = base
    while mask:
        least = mask & -mask
        value ^= columns[least.bit_length() - 1]
        mask ^= least
    return value


def enumerate_b_orbits() -> tuple[
    dict[tuple[int, int, int, int], tuple[int, int]], dict[tuple[int, int], int], dict[int, list[int]]
]:
    groups: dict[tuple[int, int, int, int], list[int]] = defaultdict(lambda: [0, 0])
    representatives: dict[tuple[int, int], int] = {}
    rank_counts: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    seen = bytearray(1 << N)
    orbit_count = 0
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
        orbit_count += 1
        parity = mask.bit_count() & 1
        signature = autocorrelation_signature(mask)
        representatives.setdefault((signature, parity), mask)
        columns = d_columns(mask)
        rank = len(rref(columns))
        v_orthogonal = orthogonal_mask(columns)
        key = (rank, signature, parity, v_orthogonal)
        groups[key][0] += len(orbit)
        groups[key][1] += 1
        rank_counts[rank][0] += len(orbit)
        rank_counts[rank][1] += 1
    assert orbit_count == 99_880
    assert sum(value[0] for value in groups.values()) == 1 << N
    assert len(representatives) == 1 << 11
    burnside = (2**21 + 2 * 2**7 + 6 * 2**3 + 12 * 2) // 21
    assert burnside == orbit_count
    return (
        {key: (value[0], value[1]) for key, value in groups.items()},
        representatives,
        rank_counts,
    )


def verify_affine_predictions(
    systems: tuple[tuple[int, int], ...],
    affine_data: tuple[tuple[tuple[int, ...], tuple[tuple[int, ...], ...]], ...],
    representatives: dict[tuple[int, int], int],
) -> int:
    rng = Random(0x5141_0004)
    checks = 0
    keys = sorted(representatives)
    for _ in range(200):
        signature, parity = keys[rng.randrange(len(keys))]
        b_mask = representatives[(signature, parity)]
        a_half = rng.randrange(1 << 10)
        theta_h, theta_s = theta_masks(a_half, signature)
        h_a = a_word(a_half, theta_h, "H")
        h_b = b_word(b_mask, "H")
        h_direct = 0
        for shift in range(1, 11):
            residual = subtract(add(paf(h_a, shift), paf(h_b, shift)), TARGET_H)
            h_direct |= pi_valuation_bit(residual, 3) << (shift - 1)
        h_data, s_data = affine_data[a_half]
        h_predicted = affine_value(h_data[0], h_data[1:], signature, parity)
        assert h_direct == h_predicted

        center = rng.randrange(4)
        s_a = a_word(a_half, theta_s, "S", center)
        s_b = b_word(b_mask, "S")
        s_direct = 0
        for shift in range(1, 11):
            residual = subtract(add(paf(s_a, shift), paf(s_b, shift)), target_s(shift))
            s_direct |= pi_valuation_bit(residual, 3) << (shift - 1)
        s_bases = s_data[0]
        s_columns = s_data[1:]
        assert isinstance(s_bases, tuple)
        s_predicted = affine_value(s_bases[center], s_columns, signature, parity)
        assert s_direct == s_predicted

        if checks < 20:
            expected_columns = d_columns(b_mask)
            for component in ("H", "S"):
                base_word = b_word(b_mask, component)
                variants = []
                for index in range(N):
                    variant = base_word.copy()
                    variant[index] = scale(variant[index], -1)
                    variants.append(variant)
                assert vector_from_deltas(base_word, variants) == expected_columns
        checks += 1
    return checks


def classify(
    groups: dict[tuple[int, int, int, int], tuple[int, int]],
    systems: tuple[tuple[int, int], ...],
    affine_data: tuple[tuple[tuple[int, ...], tuple[tuple[int, ...], ...]], ...],
    rank_counts: dict[int, list[int]],
) -> list[dict[str, str]]:
    survivors: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    parity_survivors: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    for (rank, signature, parity, b_orthogonal), (labeled_b, orbit_b) in groups.items():
        if rank == 10:
            good_a = 1 << 10
        else:
            good_a = 0
            for a_half in range(1 << 10):
                h_orthogonal, s_orthogonal = systems[a_half]
                h_data, s_data = affine_data[a_half]
                h_value = affine_value(h_data[0], h_data[1:], signature, parity)
                if not in_sum_space(h_value, h_orthogonal, b_orthogonal):
                    continue
                s_bases = s_data[0]
                s_columns = s_data[1:]
                assert isinstance(s_bases, tuple)
                if any(
                    in_sum_space(
                        affine_value(base, s_columns, signature, parity),
                        s_orthogonal,
                        b_orthogonal,
                    )
                    for base in s_bases
                ):
                    good_a += 1
        survivors[rank][0] += good_a * labeled_b
        survivors[rank][1] += good_a * orbit_b
        parity_survivors[parity][0] += good_a * labeled_b
        parity_survivors[parity][1] += good_a * orbit_b

    assert parity_survivors[0] == parity_survivors[1]
    rows = []
    for rank in sorted(rank_counts):
        b_labeled, b_orbits = rank_counts[rank]
        rows.append(
            {
                "rank": str(rank),
                "b_axis_words": str(b_labeled),
                "b_rotation_orbits": str(b_orbits),
                "possible_labeled_axis_pairs": str(b_labeled * (1 << 10)),
                "possible_axis_orbits": str(b_orbits * (1 << 10)),
                "surviving_labeled_axis_pairs": str(survivors[rank][0]),
                "surviving_axis_orbits": str(survivors[rank][1]),
            }
        )
    assert sum(int(row["surviving_labeled_axis_pairs"]) for row in rows) == 1_717_504_656
    assert sum(int(row["surviving_axis_orbits"]) for row in rows) == 81_785_936
    return rows


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    formula_checks = verify_unit_formula()
    local_checks = verify_local_sign_independence()
    systems, affine_data = a_systems()
    groups, representatives, rank_counts = enumerate_b_orbits()
    affine_checks = verify_affine_predictions(systems, affine_data, representatives)
    rows = classify(groups, systems, affine_data, rank_counts)
    root = Path(__file__).resolve().parent
    assert rows == read_tsv(root / "rank_table.tsv")

    possible_labeled = (1 << 10) * (1 << N)
    possible_orbits = (1 << 10) * 99_880
    surviving_labeled = sum(int(row["surviving_labeled_axis_pairs"]) for row in rows)
    surviving_orbits = sum(int(row["surviving_axis_orbits"]) for row in rows)
    print(f"local_quarter_states={local_checks}")
    print("unit_pi4_expansions=4")
    print(f"length5_paf_formula_checks={formula_checks}")
    print("a_reflected_axis_words=1024")
    print("b_axis_words=2097152")
    print("b_rotation_orbits=99880")
    print(f"affine_direct_checks={affine_checks}")
    for row in rows:
        print(
            "rank_{rank}={b_axis_words},{b_rotation_orbits},"
            "{surviving_labeled_axis_pairs},{surviving_axis_orbits}".format(**row)
        )
    print(f"possible_labeled_axis_pairs={possible_labeled}")
    print(f"surviving_labeled_axis_pairs={surviving_labeled}")
    print(f"eliminated_labeled_axis_pairs={possible_labeled - surviving_labeled}")
    print(f"possible_b_rotation_axis_orbits={possible_orbits}")
    print(f"surviving_b_rotation_axis_orbits={surviving_orbits}")
    print(f"eliminated_b_rotation_axis_orbits={possible_orbits - surviving_orbits}")
    print("b_parity_survivors=symmetric")
    print("rank_table=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
