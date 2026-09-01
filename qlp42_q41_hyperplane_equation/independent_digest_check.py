#!/usr/bin/env python3
"""Independent orbit digest and sampled exact-support checker."""

from __future__ import annotations

from hashlib import sha256

N = 21
DIM = 10
FULL = (1 << N) - 1
NORMAL = (1 << DIM) - 1


def rotate(mask: int) -> int:
    return ((mask << 1) | (mask >> (N - 1))) & FULL


def orbit(mask: int) -> tuple[int, ...]:
    values = []
    value = mask
    while not values or value != mask:
        values.append(value)
        value = rotate(value)
    return tuple(values)


def d_rows(mask: int) -> tuple[int, ...]:
    rows = []
    for shift in range(1, DIM + 1):
        row = 0
        for index in range(N):
            bit = ((mask >> ((index + shift) % N)) ^
                   (mask >> ((index - shift) % N))) & 1
            row |= bit << index
        rows.append(row)
    return tuple(rows)


def d_columns(rows: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(((rows[shift] >> index) & 1) << shift for shift in range(DIM))
        for index in range(N)
    )


def basis(vectors: tuple[int, ...]) -> tuple[int, ...]:
    pivots: dict[int, int] = {}
    for original in vectors:
        value = original
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return tuple(pivots[pivot] for pivot in sorted(pivots, reverse=True))


def span(linear_basis: tuple[int, ...]) -> set[int]:
    values = {0}
    for vector in linear_basis:
        values |= {value ^ vector for value in tuple(values)}
    return values


def fixed_size_subset_xors(columns: list[int], choose: int) -> set[int]:
    layers = [set() for _ in range(choose + 1)]
    layers[0].add(0)
    used = 0
    for column in columns:
        used += 1
        for size in range(min(choose, used), 0, -1):
            layers[size].update(value ^ column for value in layers[size - 1])
    return layers[choose]


def direct_exact_support(mask: int, columns: tuple[int, ...]) -> set[int]:
    imaginary = [columns[j] for j in range(N) if (mask >> j) & 1]
    real = [columns[j] for j in range(N) if not ((mask >> j) & 1)]
    real_support = fixed_size_subset_xors(real, (len(real) - 1) // 2)
    imaginary_support = fixed_size_subset_xors(imaginary, len(imaginary) // 2)
    return {left ^ right for left in real_support for right in imaginary_support}


def main() -> None:
    digest = sha256()
    digest.update(b"axis_word\torbit_size\trank\torigin\tnormal\trhs\n")
    seen = bytearray(1 << N)
    representatives: list[int] = []
    first_by_rank: dict[int, int] = {}
    rhs_counts = [0, 0]

    for mask in range(1 << N):
        if seen[mask]:
            continue
        current_orbit = orbit(mask)
        for value in current_orbit:
            seen[value] = 1
        if mask.bit_count() & 1:
            continue

        rows = d_rows(mask)
        assert rows[0] ^ rows[1] ^ rows[2] ^ rows[3] ^ rows[4] ^ rows[5] ^ rows[6] ^ rows[7] ^ rows[8] ^ rows[9] == mask
        linear_basis = basis(d_columns(rows))
        image = span(linear_basis)
        rank = len(linear_basis)
        rhs = (mask.bit_count() // 2) & 1
        support = sorted(value for value in image if (value.bit_count() & 1) == rhs)
        assert len(support) == (1 if rank == 0 else 1 << (rank - 1))
        origin = support[0]
        line = f"{mask:06x}\t{len(current_orbit)}\t{rank}\t{origin:03x}\t{NORMAL:03x}\t{rhs}\n"
        digest.update(line.encode("ascii"))
        representatives.append(mask)
        first_by_rank.setdefault(rank, mask)
        rhs_counts[rhs] += 1

    assert len(representatives) == 49_940
    assert set(first_by_rank) == {0, 1, 3, 4, 6, 7, 9, 10}

    samples = set(representatives[:248]) | set(first_by_rank.values())
    for mask in representatives:
        if len(samples) == 256:
            break
        samples.add(mask)
    assert len(samples) == 256
    sampled_ranks = set()
    for mask in sorted(samples):
        rows = d_rows(mask)
        columns = d_columns(rows)
        image = span(basis(columns))
        rhs = (mask.bit_count() // 2) & 1
        expected = {value for value in image if (value.bit_count() & 1) == rhs}
        assert direct_exact_support(mask, columns) == expected
        sampled_ranks.add(len(basis(columns)))

    print(f"canonical_stream_sha256={digest.hexdigest()}")
    print(f"canonical_stream_records={len(representatives)}")
    print(f"rhs_zero_orbits={rhs_counts[0]}")
    print(f"rhs_one_orbits={rhs_counts[1]}")
    print(f"direct_subset_axis_words={len(samples)}")
    print("rank_coverage=" + ",".join(map(str, sorted(sampled_ranks))))
    print("independent_digest_and_support_check=verified")


if __name__ == "__main__":
    main()
