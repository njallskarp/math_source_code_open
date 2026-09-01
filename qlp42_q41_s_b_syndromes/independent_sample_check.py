#!/usr/bin/env python3
"""Independent fixed-cardinality subset-XOR audit of the C++ sample stream."""

from __future__ import annotations

import hashlib

N = 21
DIM = 10
FULL = (1 << N) - 1
TARGETS = ((4, -5), (4, -3), (0, -5), (4, -1), (4, 1), (0, -3))
EXPECTED_SHA256 = "12124e91beecd8b4607b9bd54d080318b7b41c1212532fa3cbb8d6633b8bc2f2"


def low_block_mask(width: int) -> int:
    result = 0
    block = (1 << width) - 1
    for start in range(0, 1 << DIM, 2 * width):
        result |= block << start
    return result


LOW_MASKS = tuple(low_block_mask(1 << bit) for bit in range(DIM))


def xor_permute(bits: int, shift: int) -> int:
    """Map the bit at syndrome y to syndrome y xor shift."""
    for bit in range(DIM):
        if (shift >> bit) & 1:
            width = 1 << bit
            low = LOW_MASKS[bit]
            bits = ((bits & low) << width) | ((bits >> width) & low)
    return bits


def subset_xor_by_size(columns: list[int]) -> list[int]:
    """Return 1,024-bit support vectors for every subset cardinality."""
    supports = [0] * (len(columns) + 1)
    supports[0] = 1
    used = 0
    for column in columns:
        used += 1
        for size in range(used, 0, -1):
            supports[size] |= xor_permute(supports[size - 1], column)
    return supports


def xor_sumset(left: int, right: int) -> int:
    if left.bit_count() > right.bit_count():
        left, right = right, left
    result = 0
    while left:
        low = left & -left
        value = low.bit_length() - 1
        result |= xor_permute(right, value)
        left ^= low
    return result


def rotate(mask: int) -> int:
    return ((mask << 1) | (mask >> (N - 1))) & FULL


def d_columns(axis: int) -> list[int]:
    columns = []
    for j in range(N):
        column = 0
        for shift in range(1, DIM + 1):
            plus = (j + shift) % N
            minus = (j - shift) % N
            coefficient = ((axis >> plus) ^ (axis >> minus)) & 1
            column |= coefficient << (shift - 1)
        columns.append(column)
    return columns


def binary_rank(values: list[int]) -> int:
    values = values[:]
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


def image_support(columns: list[int]) -> int:
    support = 1
    for column in columns:
        support |= xor_permute(support, column)
    return support


def main() -> None:
    lines = ["axis_word\torbit_size\tweight\trank\tcase\tsupport"]
    seen = bytearray(1 << N)
    processed_orbits = 0
    processed_words = 0
    sampled_orbits = 0
    sampled_ranks: set[int] = set()

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
        weight = mask.bit_count()
        if weight % 4:
            continue

        columns = d_columns(mask)
        rank = binary_rank(columns)
        if processed_orbits % 49 == 0 or rank not in sampled_ranks:
            image = image_support(columns)
            real_columns = [columns[j] for j in range(N) if (mask >> j) & 1]
            imag_columns = [columns[j] for j in range(N) if not ((mask >> j) & 1)]
            real_supports = subset_xor_by_size(real_columns)
            imag_supports = subset_xor_by_size(imag_columns)
            case_supports = []

            for case, (target_real, target_imag) in enumerate(TARGETS):
                nr = (weight - target_real) // 2
                ni = (N - weight - target_imag) // 2
                if nr < 0 or nr > weight or ni < 0 or ni > N - weight:
                    support = 0
                else:
                    support = xor_sumset(real_supports[nr], imag_supports[ni])
                assert support & ~image == 0
                assert all((syndrome.bit_count() & 1) == 0 for syndrome in range(1 << DIM)
                           if (support >> syndrome) & 1)
                case_supports.append(support)
                lines.append(
                    f"{mask:06x}\t{len(orbit)}\t{weight}\t{rank}\t{case}\t{support:0256x}"
                )
            assert case_supports[3] == case_supports[4]
            sampled_orbits += 1
            sampled_ranks.add(rank)

        processed_orbits += 1
        processed_words += len(orbit)

    stream = ("\n".join(lines) + "\n").encode()
    digest = hashlib.sha256(stream).hexdigest()
    assert processed_orbits == 24_946
    assert processed_words == 523_776
    assert sampled_orbits == 516
    assert len(lines) == 3_097
    assert digest == EXPECTED_SHA256
    print(f"sampled_orbits={sampled_orbits}")
    print(f"sampled_cases={sampled_orbits * len(TARGETS)}")
    print(f"sampled_ranks={','.join(map(str, sorted(sampled_ranks)))}")
    print("direct_subset_xor_matches_primary_sample_stream=verified")
    print("even_parity_containment=verified")
    print("case_3_case_4_support_identity=verified")
    print(f"sample_stream_sha256={digest}")


if __name__ == "__main__":
    main()
