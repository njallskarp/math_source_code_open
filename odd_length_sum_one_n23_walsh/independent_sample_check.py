#!/usr/bin/env python3
"""Independent subset-XOR sample audit of the exhaustive n=23 Walsh census."""

from __future__ import annotations

import hashlib


N = 23
DIM = 11
FULL = (1 << N) - 1
NORMAL = (1 << DIM) - 1
STRIDE = 359
EXPECTED_SAMPLE_DIGEST = "08198a4e96b8ef223404c03ad1977b76b0d71dac0abed4e6a94606002436b88a"


def rotate(mask: int) -> int:
    return ((mask << 1) | (mask >> (N - 1))) & FULL


def d_columns(mask: int) -> tuple[int, ...]:
    columns = []
    for index in range(N):
        column = 0
        for shift in range(1, DIM + 1):
            plus = (index + shift) % N
            minus = (index - shift) % N
            column |= (((mask >> plus) ^ (mask >> minus)) & 1) << (shift - 1)
        columns.append(column)
    return tuple(columns)


def low_masks() -> tuple[int, ...]:
    result = []
    for bit in range(DIM):
        width = 1 << bit
        block = (1 << width) - 1
        mask = 0
        for start in range(0, 1 << DIM, 2 * width):
            mask |= block << start
        result.append(mask)
    return tuple(result)


LOW_MASKS = low_masks()


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


def image(columns: tuple[int, ...]) -> int:
    result = 1
    for column in columns:
        result |= translate(result, column)
    return result


def rank(columns: tuple[int, ...]) -> int:
    basis = [0] * DIM
    result = 0
    for column in columns:
        value = column
        while value:
            pivot = value.bit_length() - 1
            if basis[pivot]:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                result += 1
                break
    return result


def selected_orbits() -> list[tuple[int, int, int]]:
    seen = bytearray(1 << N)
    selected = []
    even_index = 0
    even_orbits = 0
    for mask in range(1 << N):
        if seen[mask]:
            continue
        value = mask
        orbit_size = 0
        while True:
            seen[value] = 1
            orbit_size += 1
            value = rotate(value)
            if value == mask:
                break
        if mask.bit_count() & 1:
            continue
        if even_index % STRIDE == 0:
            selected.append((even_index, mask, orbit_size))
        even_index += 1
        even_orbits += 1
    assert even_orbits == 182_362
    assert len(selected) == 508
    return selected


def main() -> None:
    parity = [0, 0]
    for syndrome in range(1 << DIM):
        parity[syndrome.bit_count() & 1] |= 1 << syndrome
    digest = hashlib.sha256()
    digest.update(b"orbit_index\taxis_word\torbit_size\trank\torigin\tnormal\trhs\tsupport\n")

    selected = selected_orbits()
    for orbit_index, mask, orbit_size in selected:
        columns = d_columns(mask)
        real = [column for index, column in enumerate(columns) if not ((mask >> index) & 1)]
        imaginary = [column for index, column in enumerate(columns) if (mask >> index) & 1]
        weight = mask.bit_count()
        support = xor_sumset(
            subset_xor_by_size(real)[(N - weight - 1) // 2],
            subset_xor_by_size(imaginary)[weight // 2],
        )
        matrix_rank = rank(columns)
        assert matrix_rank == (0 if mask == 0 else DIM)
        rhs = (weight // 2) & 1
        expected = image(columns) & parity[rhs]
        assert support == expected
        origin = (support & -support).bit_length() - 1
        digest.update(
            f"{orbit_index}\t{mask:06x}\t{orbit_size}\t{matrix_rank}\t"
            f"{origin:03x}\t{NORMAL:03x}\t{rhs}\t{support:0512x}\n".encode("ascii")
        )

    observed = digest.hexdigest()
    if EXPECTED_SAMPLE_DIGEST:
        assert observed == EXPECTED_SAMPLE_DIGEST
    print(f"sampled_rotation_orbits={len(selected)}")
    print(f"sampled_syndrome_memberships={len(selected) * (1 << DIM)}")
    print("sample_rank_dichotomy=verified")
    print("sample_exact_support_equation=verified")
    print(f"sample_stream_sha256={observed}")
    print("independent_sample_certificate=verified")


if __name__ == "__main__":
    main()
