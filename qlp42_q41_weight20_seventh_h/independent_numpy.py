#!/usr/bin/env python3
"""Independent vectorized audit of the q=41, wt(H_B axes)=20 H obstruction."""

from __future__ import annotations

from itertools import combinations
from math import comb

import numpy as np

N = 21
FULL = (1 << N) - 1
PAIR_MASKS = np.arange(1 << 10, dtype=np.uint16)
PAIR_SIGNS = 1 - 2 * ((PAIR_MASKS[:, None] >> np.arange(10)) & 1).astype(np.int16)


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def reflected_axes(a_half: int) -> int:
    result = 0
    for shift in range(1, 11):
        if (a_half >> (shift - 1)) & 1:
            result |= (1 << shift) | (1 << (N - shift))
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
        a_shift = (a_half >> (shift - 1)) & 1
        f_shift = 1 ^ a_shift
        c_a = (a & rotate(a, shift)).bit_count() & 1
        c_f = (f & rotate(f, shift)).bit_count() & 1
        e = (signature >> (shift - 1)) & 1
        tau = int(shift in (4, 10))
        theta_h |= (1 ^ a_shift ^ c_a ^ e) << (shift - 1)
        theta_s |= (1 ^ f_shift ^ c_f ^ e ^ tau) << (shift - 1)
    return theta_h, theta_s


def combination_masks(width: int, weight: int) -> np.ndarray:
    return np.fromiter(
        (sum(1 << index for index in chosen) for chosen in combinations(range(width), weight)),
        dtype=np.uint32,
        count=comb(width, weight),
    )


def paf(real: np.ndarray, imag: np.ndarray) -> np.ndarray:
    assert real.shape == imag.shape and real.shape[1] == N
    result = np.empty((real.shape[0], 10, 2), dtype=np.int16)
    for shift in range(1, 11):
        real_shift = np.roll(real, -shift, axis=1)
        imag_shift = np.roll(imag, -shift, axis=1)
        result[:, shift - 1, 0] = np.sum(
            real * real_shift + imag * imag_shift, axis=1, dtype=np.int16
        )
        result[:, shift - 1, 1] = np.sum(
            imag * real_shift - real * imag_shift, axis=1, dtype=np.int16
        )
    return result


def pi_residues(values: np.ndarray, power: int) -> np.ndarray:
    current = values.astype(np.int32, copy=True)
    result = np.zeros(values.shape[:-1], dtype=np.uint8)
    for place in range(power):
        digit = (current[..., 0] + current[..., 1]) & 1
        result |= digit.astype(np.uint8) << place
        old_real = current[..., 0] - digit
        old_imag = current[..., 1]
        assert np.all(((old_real + old_imag) & 1) == 0)
        current = np.stack(
            ((old_real + old_imag) // 2, (old_imag - old_real) // 2), axis=-1
        )
    return result


def row_set(rows: np.ndarray) -> set[bytes]:
    return {row.tobytes() for row in np.ascontiguousarray(rows)}


def membership(rows: np.ndarray, support: set[bytes]) -> np.ndarray:
    return np.fromiter(
        (row.tobytes() in support for row in np.ascontiguousarray(rows)),
        dtype=np.bool_,
        count=rows.shape[0],
    )


def b_h_supports() -> tuple[dict[int, set[bytes]], int]:
    masks = combination_masks(20, 10)
    assert masks.size == 184_756
    signs = 1 - 2 * ((masks[:, None] >> np.arange(20)) & 1).astype(np.int16)
    real = np.zeros((masks.size, N), dtype=np.int16)
    imag = np.zeros_like(real)
    real[:, 0] = 1
    imag[:, 1:] = signs
    values = paf(real, imag)
    supports = {power: row_set(pi_residues(values, power)) for power in range(4, 8)}
    exact_count = np.unique(values.reshape(values.shape[0], -1), axis=0).shape[0]
    return supports, int(exact_count)


def b_s_fourth_support() -> set[bytes]:
    masks = combination_masks(20, 8)
    assert masks.size == 125_970
    signs = 1 - 2 * ((masks[:, None] >> np.arange(20)) & 1).astype(np.int16)
    real = np.zeros((masks.size, N), dtype=np.int16)
    imag = np.zeros_like(real)
    imag[:, 0] = -1
    real[:, 1:] = signs
    return row_set(pi_residues(paf(real, imag), 4))


def a_words(a_half: int, theta: int, component: str, center: tuple[int, int] | None = None):
    axes = reflected_axes(a_half)
    if component == "S":
        axes = (FULL ^ 1) ^ axes
    real = np.zeros((1 << 10, N), dtype=np.int16)
    imag = np.zeros_like(real)
    if center is not None:
        real[:, 0], imag[:, 0] = center
    for pair in range(10):
        shift = pair + 1
        left = PAIR_SIGNS[:, pair]
        xor = (theta >> pair) & 1
        right = left if xor == 0 else -left
        if (axes >> shift) & 1:
            imag[:, shift] = left
            imag[:, N - shift] = right
        else:
            real[:, shift] = left
            real[:, N - shift] = right
    return real, imag


def required_h(values: np.ndarray) -> np.ndarray:
    required = -values.astype(np.int16, copy=True)
    required[..., 0] -= 2
    return required


def required_s(values: np.ndarray) -> np.ndarray:
    required = -values.astype(np.int16, copy=True)
    required[:, 3, 0] -= 2
    required[:, 9, 0] += 2
    return required


def main() -> None:
    b_supports, b_exact_count = b_h_supports()
    s_b4 = b_s_fourth_support()
    b_mask = FULL ^ 1
    signature = autocorrelation_signature(b_mask)

    assignment_counts = {power: 0 for power in range(4, 8)}
    axis_masks = {power: 0 for power in range(4, 8)}
    s4_mask = 0
    a_exact_sum_assignments = 0
    for a_half in range(1 << 10):
        theta_h, theta_s = theta_masks(a_half, signature)
        real, imag = a_words(a_half, theta_h, "H")
        keep = (np.sum(real, axis=1) == 0) & (np.sum(imag, axis=1) == 0)
        a_exact_sum_assignments += int(np.count_nonzero(keep))
        h_values = paf(real[keep], imag[keep])
        needed = required_h(h_values)
        for power in range(4, 8):
            hits = membership(pi_residues(needed, power), b_supports[power])
            assignment_counts[power] += int(np.count_nonzero(hits))
            if np.any(hits):
                axis_masks[power] |= 1 << a_half

        s_survives = False
        for center in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            s_real, s_imag = a_words(a_half, theta_s, "S", center)
            keep_s = (np.sum(s_real, axis=1) == 5) & (np.sum(s_imag, axis=1) == -1)
            if not np.any(keep_s):
                continue
            s_needed = required_s(paf(s_real[keep_s], s_imag[keep_s]))
            if np.any(membership(pi_residues(s_needed, 4), s_b4)):
                s_survives = True
                break
        if s_survives:
            s4_mask |= 1 << a_half

    sixth_axes = [index for index in range(1 << 10) if (axis_masks[6] >> index) & 1]
    all_sums_fourth = (axis_masks[4] & s4_mask).bit_count()
    all_sums_fifth_h = (axis_masks[5] & s4_mask).bit_count()

    assert [len(b_supports[p]) for p in range(4, 8)] == [512, 72_688, 92_128, 92_854]
    assert b_exact_count == 92_854
    assert len(s_b4) == 511
    assert a_exact_sum_assignments == 127_704
    assert [assignment_counts[p] for p in range(4, 8)] == [127_704, 16_272, 720, 0]
    assert [axis_masks[p].bit_count() for p in range(4, 8)] == [512, 418, 4, 0]
    assert sixth_axes == [0, 356, 667, 1023]
    assert all_sums_fourth == 388
    assert all_sums_fifth_h == 317

    print("implementation=independent_numpy_vectorized_direct_paf")
    print("b_exact_sum_assignments=184756")
    for power in range(4, 8):
        print(f"b_order_{power}_fingerprints={len(b_supports[power])}")
    print(f"b_exact_paf_vectors={b_exact_count}")
    print("s_b_exact_sum_assignments=125970")
    print(f"s_b_fourth_fingerprints={len(s_b4)}")
    print(f"a_exact_sum_assignments={a_exact_sum_assignments}")
    for power in range(4, 8):
        print(f"order_{power}_h_compatible_assignments={assignment_counts[power]}")
        print(f"order_{power}_h_surviving_a_axes={axis_masks[power].bit_count()}")
    print("sixth_order_a_axes=" + ",".join(map(str, sixth_axes)))
    print(f"case_3_all_sums_fourth_order_a_axes={all_sums_fourth}")
    print(f"case_3_all_sums_plus_fifth_h_a_axes={all_sums_fifth_h}")
    print("seventh_order_weight20_exclusion=verified")


if __name__ == "__main__":
    main()
