#!/usr/bin/env python3
"""Independent direct-Gaussian audit of the q=41 all-sums sample stream."""

from __future__ import annotations

import hashlib
from pathlib import Path

Gaussian = tuple[int, int]
N = 21
DIM = 10
FULL = (1 << N) - 1
MASK10 = (1 << DIM) - 1
HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample_axis_survivors.tsv"
EXPECTED_DIGEST = "995c6c17c07e81575f0fcd51db8dc786ec7d9172c93b03903a30550e7af48290"
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
S_A_TARGETS = tuple((p + q, q - p) for p, q, _x, _y in CASES)
S_B_TARGETS = tuple((x + y - 1, y - x) for _p, _q, x, y in CASES)


def add(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] + y[0], x[1] + y[1]


def sub(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] - y[0], x[1] - y[1]


def mul(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def conj(x: Gaussian) -> Gaussian:
    return x[0], -x[1]


def neg(x: Gaussian) -> Gaussian:
    return -x[0], -x[1]


def div_pi(x: Gaussian) -> Gaussian:
    assert (x[0] + x[1]) % 2 == 0
    return (x[0] + x[1]) // 2, (x[1] - x[0]) // 2


def pi3_bit(x: Gaussian) -> int:
    for _ in range(3):
        x = div_pi(x)
    return (x[0] + x[1]) & 1


def scale(x: Gaussian, coefficient: int) -> Gaussian:
    return coefficient * x[0], coefficient * x[1]


def unit(axis: int, sign: int = 0) -> Gaussian:
    value = (1, 0) if axis == 0 else (0, 1)
    return neg(value) if sign else value


def rotate(mask: int, shift: int = 1) -> int:
    shift %= N
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def paf(word: list[Gaussian], shift: int) -> Gaussian:
    total = (0, 0)
    for j, value in enumerate(word):
        total = add(total, mul(value, conj(word[(j + shift) % N])))
    return total


def word_sum(word: list[Gaussian]) -> Gaussian:
    total = (0, 0)
    for value in word:
        total = add(total, value)
    return total


def reflected_axes(a_half: int) -> int:
    result = 0
    for shift in range(1, 11):
        bit = (a_half >> (shift - 1)) & 1
        result |= bit << shift
        result |= bit << (N - shift)
    return result


def autocorrelation_signature(mask: int) -> int:
    parity = mask.bit_count() & 1
    return sum(
        (parity ^ ((mask & rotate(mask, shift)).bit_count() & 1)) << (shift - 1)
        for shift in range(1, 11)
    )


def theta_masks(a_half: int, signature: int) -> tuple[int, int]:
    a = reflected_axes(a_half)
    f = (FULL ^ 1) ^ a
    theta_h = 0
    theta_s = 0
    for shift in range(1, 11):
        a_bit = (a_half >> (shift - 1)) & 1
        c_a = (a & rotate(a, shift)).bit_count() & 1
        c_f = (f & rotate(f, shift)).bit_count() & 1
        e = (signature >> (shift - 1)) & 1
        theta_h |= (1 ^ a_bit ^ c_a ^ e) << (shift - 1)
        theta_s |= (a_bit ^ c_f ^ e ^ int(shift in (4, 10))) << (shift - 1)
    return theta_h, theta_s


def a_word(a_half: int, theta: int, component: str, center: int = 0) -> list[Gaussian]:
    axes_h = reflected_axes(a_half)
    axes = axes_h if component == "H" else (FULL ^ 1) ^ axes_h
    word = [(0, 0)] * N
    if component == "S":
        roots = ((1, 0), (0, 1), (-1, 0), (0, -1))
        word[0] = mul((1, 1), roots[center])
    for shift in range(1, 11):
        axis = (axes >> shift) & 1
        word[shift] = unit(axis)
        word[N - shift] = unit(axis, (theta >> (shift - 1)) & 1)
    return word


def b_word(mask: int, component: str) -> list[Gaussian]:
    axes = mask if component == "H" else FULL ^ mask
    return [unit((axes >> j) & 1) for j in range(N)]


def target_s(shift: int) -> Gaussian:
    return (-2, 0) if shift == 4 else (2, 0) if shift == 10 else (0, 0)


def residual_syndrome(a: list[Gaussian], b_pafs: list[Gaussian], component: str) -> int:
    result = 0
    for shift in range(1, 11):
        target = (-2, 0) if component == "H" else target_s(shift)
        residual = sub(add(paf(a, shift), b_pafs[shift - 1]), target)
        result |= pi3_bit(residual) << (shift - 1)
    return result


def d_columns(mask: int) -> tuple[int, ...]:
    columns = []
    for j in range(N):
        column = 0
        for shift in range(1, 11):
            plus = (j + shift) % N
            minus = (j - shift) % N
            column |= (((mask >> plus) ^ (mask >> minus)) & 1) << (shift - 1)
        columns.append(column)
    return tuple(columns)


def binary_rank(values: tuple[int, ...]) -> int:
    values = list(values)
    rank = 0
    for bit in range(DIM - 1, -1, -1):
        pivot = next((row for row in range(rank, len(values)) if (values[row] >> bit) & 1), None)
        if pivot is None:
            continue
        values[rank], values[pivot] = values[pivot], values[rank]
        for row in range(len(values)):
            if row != rank and ((values[row] >> bit) & 1):
                values[row] ^= values[rank]
        rank += 1
    return rank


def make_low_masks() -> tuple[int, ...]:
    masks = []
    for bit in range(DIM):
        width = 1 << bit
        block = (1 << width) - 1
        mask = 0
        for start in range(0, 1 << DIM, 2 * width):
            mask |= block << start
        masks.append(mask)
    return tuple(masks)


LOW_MASKS = make_low_masks()


def translate(bits: int, shift: int) -> int:
    for bit, low_mask in enumerate(LOW_MASKS):
        if (shift >> bit) & 1:
            width = 1 << bit
            bits = ((bits & low_mask) << width) | ((bits >> width) & low_mask)
    return bits


def subset_xor_by_size(columns: list[int]) -> list[int]:
    supports = [0] * (len(columns) + 1)
    supports[0] = 1
    for used, column in enumerate(columns, 1):
        for size in range(used, 0, -1):
            supports[size] |= translate(supports[size - 1], column)
    return supports


def xor_sumset(left: int, right: int) -> int:
    if left.bit_count() > right.bit_count():
        left, right = right, left
    result = 0
    while left:
        least = left & -left
        result |= translate(right, least.bit_length() - 1)
        left ^= least
    return result


def exact_support(columns: tuple[int, ...], axis_mask: int, real_on_one: bool,
                  target: tuple[int, int]) -> int:
    if real_on_one:
        real = [columns[j] for j in range(N) if (axis_mask >> j) & 1]
        imag = [columns[j] for j in range(N) if not ((axis_mask >> j) & 1)]
    else:
        real = [columns[j] for j in range(N) if not ((axis_mask >> j) & 1)]
        imag = [columns[j] for j in range(N) if (axis_mask >> j) & 1]
    nr = (len(real) - target[0]) // 2
    ni = (len(imag) - target[1]) // 2
    if nr < 0 or nr > len(real) or ni < 0 or ni > len(imag):
        return 0
    return xor_sumset(subset_xor_by_size(real)[nr], subset_xor_by_size(imag)[ni])


def attainable(pair_count: int, target: int) -> bool:
    return abs(target) <= pair_count and (target - pair_count) % 2 == 0


def h_a_possible(a_half: int, theta_h: int) -> bool:
    active = (~theta_h) & MASK10
    return ((active & a_half).bit_count() % 2 == 0 and
            (active & (~a_half & MASK10)).bit_count() % 2 == 0)


def s_a_possible(a_half: int, theta_s: int, target: Gaussian) -> bool:
    active = (~theta_s) & MASK10
    real_pairs = (active & a_half).bit_count()
    imag_pairs = (active & (~a_half & MASK10)).bit_count()
    for center in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        rr = (target[0] - center[0]) // 2
        ri = (target[1] - center[1]) // 2
        if attainable(real_pairs, rr) and attainable(imag_pairs, ri):
            return True
    return False


def brute_a_sum_checks(a_half: int, signature: int) -> None:
    theta_h, theta_s = theta_masks(a_half, signature)
    h_base = a_word(a_half, theta_h, "H")
    h_sums = set()
    s_sums = set()
    for flips in range(1 << 10):
        h = h_base.copy()
        for pair in range(10):
            if (flips >> pair) & 1:
                shift = pair + 1
                h[shift] = neg(h[shift])
                h[N - shift] = neg(h[N - shift])
        h_sums.add(word_sum(h))
        for center in range(4):
            s = a_word(a_half, theta_s, "S", center)
            for pair in range(10):
                if (flips >> pair) & 1:
                    shift = pair + 1
                    s[shift] = neg(s[shift])
                    s[N - shift] = neg(s[N - shift])
            s_sums.add(word_sum(s))
    assert ((0, 0) in h_sums) == h_a_possible(a_half, theta_h)
    for target in set(S_A_TARGETS):
        assert (target in s_sums) == s_a_possible(a_half, theta_s, target)


def selected_masks() -> set[int]:
    seen = bytearray(1 << N)
    eligible = []
    for mask in range(1 << N):
        if seen[mask]:
            continue
        orbit = []
        value = mask
        while True:
            orbit.append(value)
            seen[value] = 1
            value = rotate(value)
            if value == mask:
                break
        if mask.bit_count() % 4 == 0:
            eligible.append((mask, len(orbit), binary_rank(d_columns(mask))))
    assert len(eligible) == 24_946
    result = set()
    seen_ranks = set()
    for index, (mask, _orbit_size, rank) in enumerate(eligible):
        if index % 199 == 0 or rank not in seen_ranks:
            result.add(mask)
            seen_ranks.add(rank)
    assert len(result) == 132
    assert seen_ranks == {0, 3, 4, 6, 7, 9, 10}
    return result


def parse_sample():
    raw = SAMPLE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_DIGEST
    lines = raw.decode("ascii").splitlines()
    assert lines[0] == (
        "axis_word\torbit_size\tweight\trank\tsignature\tcase_0_a_mask\t"
        "case_1_a_mask\tcase_2_a_mask\tcase_3_a_mask\tcase_4_a_mask\tcase_5_a_mask"
    )
    records = []
    for line in lines[1:]:
        fields = line.split("\t")
        assert len(fields) == 11
        records.append(
            (int(fields[0], 16), int(fields[1]), int(fields[2]), int(fields[3]),
             int(fields[4], 16), tuple(int(value, 16) for value in fields[5:]))
        )
    assert len(records) == 132
    assert {record[0] for record in records} == selected_masks()
    assert records == sorted(records, key=lambda record: (record[4], record[0]))
    return records


def main() -> None:
    records = parse_sample()
    audited_pairs = set()
    for mask, orbit_size, weight, rank, signature, expected_masks in records:
        assert weight == mask.bit_count()
        assert signature == autocorrelation_signature(mask)
        orbit = {rotate(mask, shift) for shift in range(N)}
        assert mask == min(orbit) and orbit_size == len(orbit)
        columns = d_columns(mask)
        assert binary_rank(columns) == rank
        h_support = exact_support(columns, mask, False, (1, 0))
        s_supports = tuple(
            exact_support(columns, mask, True, target) for target in S_B_TARGETS
        )
        assert s_supports[3] == s_supports[4]
        h_b_pafs = [paf(b_word(mask, "H"), shift) for shift in range(1, 11)]
        s_b_pafs = [paf(b_word(mask, "S"), shift) for shift in range(1, 11)]
        actual_masks = [0] * 6
        for a_half in range(1 << 10):
            theta_h, theta_s = theta_masks(a_half, signature)
            h_a = a_word(a_half, theta_h, "H")
            s_a = a_word(a_half, theta_s, "S", 0)
            h_value = residual_syndrome(h_a, h_b_pafs, "H")
            s_value = residual_syndrome(s_a, s_b_pafs, "S")
            if not h_a_possible(a_half, theta_h) or not ((h_support >> h_value) & 1):
                continue
            for case in range(6):
                if s_a_possible(a_half, theta_s, S_A_TARGETS[case]) and (
                    (s_supports[case] >> s_value) & 1
                ):
                    actual_masks[case] |= 1 << a_half
            if len(audited_pairs) < 32 and a_half in (0, mask & MASK10, 341, 682, 1023):
                audited_pairs.add((mask, a_half))
                for component, base, b_pafs in (
                    ("H", h_a, h_b_pafs), ("S", s_a, s_b_pafs)
                ):
                    base_value = residual_syndrome(base, b_pafs, component)
                    for pair in range(10):
                        variant = base.copy()
                        shift = pair + 1
                        variant[shift] = neg(variant[shift])
                        variant[N - shift] = neg(variant[N - shift])
                        assert residual_syndrome(variant, b_pafs, component) == base_value
                for center in range(1, 4):
                    centered = a_word(a_half, theta_s, "S", center)
                    assert residual_syndrome(centered, s_b_pafs, "S") == s_value
                brute_a_sum_checks(a_half, signature)
        assert tuple(actual_masks) == expected_masks
        assert actual_masks[3] == actual_masks[4]

    assert len(audited_pairs) == 32
    print("sampled_b_rotation_orbits=132")
    print("sampled_axis_pairs=135168")
    print("direct_zero_direction_pair_audits=640")
    print("direct_center_residual_audits=96")
    print("brute_a_sum_domain_audits=32")
    print("direct_fixed_cardinality_b_supports=924")
    print("all_six_survivor_masks_match=verified")
    print("case_3_case_4_identity=verified")
    print(f"sample_axis_survivor_stream_sha256={EXPECTED_DIGEST}")


if __name__ == "__main__":
    main()
