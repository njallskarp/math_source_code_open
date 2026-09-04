#!/usr/bin/env python3
"""Independent exact checks for the Hamming rectangle cross-boundary result.

CPython 3.12+, standard library only.  The small-instance constructor does not
use the target's cyclic formula.  It searches star-count/outdegree profiles,
tests bipartite graphicality, constructs an orientation of K_{m,n}, and turns
the outgoing edges at every vertex into line parts of sizes s and s+1.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
from collections.abc import Iterable, Sequence
from functools import lru_cache


# A vertex option records (outdegree, number of stars, number of (s+1)-stars).
Option = tuple[int, int, int]
Profile = tuple[Option, ...]
Part = tuple[str, int, tuple[int, ...]]


def vertex_options(capacity: int, s: int) -> tuple[Option, ...]:
    options: list[Option] = []
    for stars in range(capacity // s + 1):
        for large in range(stars + 1):
            degree = stars * s + large
            if degree <= capacity:
                options.append((degree, stars, large))
    return tuple(sorted(options))


@lru_cache(maxsize=None)
def profile_index(
    vertex_count: int, capacity: int, s: int
) -> dict[tuple[int, int, int], tuple[Profile, ...]]:
    """Index canonical vertex profiles by (stars, large stars, outdegree)."""

    buckets: dict[tuple[int, int, int], list[Profile]] = {}
    for profile in itertools.combinations_with_replacement(
        vertex_options(capacity, s), vertex_count
    ):
        key = (
            sum(option[1] for option in profile),
            sum(option[2] for option in profile),
            sum(option[0] for option in profile),
        )
        buckets.setdefault(key, []).append(profile)
    return {key: tuple(values) for key, values in buckets.items()}


def gale_ryser(row_sums: Sequence[int], column_sums: Sequence[int]) -> bool:
    rows = sorted(row_sums, reverse=True)
    columns = sorted(column_sums, reverse=True)
    if sum(rows) != sum(columns):
        return False
    if rows and (rows[0] > len(columns) or rows[-1] < 0):
        return False
    if columns and (columns[0] > len(rows) or columns[-1] < 0):
        return False
    prefix = 0
    for k, degree in enumerate(rows, start=1):
        prefix += degree
        if prefix > sum(min(k, value) for value in columns):
            return False
    return True


def bipartite_matrix(
    row_sums: Sequence[int], column_sums: Sequence[int]
) -> list[list[int]] | None:
    """Construct a 0-1 matrix by bipartite Havel--Hakimi."""

    if not gale_ryser(row_sums, column_sums):
        return None
    row_order = sorted(range(len(row_sums)), key=lambda i: (-row_sums[i], i))
    remaining = list(column_sums)
    matrix = [[0] * len(column_sums) for _ in row_sums]
    for row in row_order:
        degree = row_sums[row]
        choices = sorted(
            range(len(remaining)), key=lambda j: (-remaining[j], j)
        )[:degree]
        if len(choices) != degree or any(remaining[j] == 0 for j in choices):
            return None
        for column in choices:
            matrix[row][column] = 1
            remaining[column] -= 1
    if any(remaining):
        return None
    return matrix


def chunks(values: Sequence[int], sizes: Iterable[int]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    start = 0
    for size in sizes:
        result.append(tuple(values[start : start + size]))
        start += size
    if start != len(values):
        raise AssertionError("star sizes do not consume the owned edges")
    return result


def build_partition(
    m: int, n: int, s: int, row_profile: Profile, column_profile: Profile
) -> tuple[Part, ...] | None:
    # Reordering symmetric vertices is harmless and makes the witness canonical.
    rows = tuple(sorted(row_profile, key=lambda option: (-option[0], option)))
    columns = tuple(
        sorted(column_profile, key=lambda option: (-(m - option[0]), option))
    )
    row_sums = [option[0] for option in rows]
    # A 1 assigns the cell to its row; a 0 assigns it to its column.
    row_owned_column_sums = [m - option[0] for option in columns]
    matrix = bipartite_matrix(row_sums, row_owned_column_sums)
    if matrix is None:
        return None

    parts: list[Part] = []
    for row, (_, stars, large) in enumerate(rows):
        owned = [column for column in range(n) if matrix[row][column] == 1]
        sizes = [s + 1] * large + [s] * (stars - large)
        parts.extend(("R", row, block) for block in chunks(owned, sizes))
    for column, (_, stars, large) in enumerate(columns):
        owned = [row for row in range(m) if matrix[row][column] == 0]
        sizes = [s + 1] * large + [s] * (stars - large)
        parts.extend(("C", column, block) for block in chunks(owned, sizes))
    return tuple(parts)


def validate_partition(m: int, n: int, s: int, parts: Sequence[Part]) -> None:
    seen: set[tuple[int, int]] = set()
    for axis, fixed, varying in parts:
        assert len(varying) in {s, s + 1}
        assert len(varying) == len(set(varying))
        if axis == "R":
            cells = {(fixed, column) for column in varying}
        elif axis == "C":
            cells = {(row, fixed) for row in varying}
        else:
            raise AssertionError("unknown line axis")
        assert seen.isdisjoint(cells)
        seen.update(cells)
    assert seen == set(itertools.product(range(m), range(n)))
    quotient, remainder = divmod(m * n, s)
    assert len(parts) == quotient
    assert sum(len(part[2]) == s + 1 for part in parts) == remainder


def independent_partition(m: int, n: int, s: int) -> tuple[Part, ...] | None:
    """Find a balanced optimal partition without the cyclic construction."""

    quotient, remainder = divmod(m * n, s)
    row_buckets = profile_index(m, n, s)
    column_buckets = profile_index(n, m, s)
    for (row_stars, row_large, row_degree), row_profiles in row_buckets.items():
        needed = (
            quotient - row_stars,
            remainder - row_large,
            m * n - row_degree,
        )
        for row_profile in row_profiles:
            for column_profile in column_buckets.get(needed, ()):
                parts = build_partition(m, n, s, row_profile, column_profile)
                if parts is not None:
                    validate_partition(m, n, s, parts)
                    return parts
    return None


def audit_independent_rectangles(max_s: int, max_side: int) -> tuple[int, str]:
    instances = 0
    digest = hashlib.sha256()
    for s in range(2, max_s + 1):
        for m in range(s, max_side + 1):
            for n in range(m, max_side + 1):
                parts = independent_partition(m, n, s)
                assert parts is not None
                digest.update(f"{s}:{m}:{n}:{parts}\n".encode())
                instances += 1
    return instances, digest.hexdigest()


def audit_corner_arithmetic(max_s: int) -> tuple[int, str]:
    """Audit the universal cyclic proof's inequalities and size refinement."""

    cases = 0
    digest = hashlib.sha256()
    for s in range(2, max_s + 1):
        for a in range(1, s):
            for b in range(1, s):
                q, t = divmod(a * b, s)
                length = b + q
                assert q <= a - 1
                assert b <= length < s + b
                marked = (s + a) * b
                assert marked == s * length + t
                excess_base, excess_remainder = divmod(t, length)
                column_sizes = [
                    s + excess_base + (index < excess_remainder)
                    for index in range(length)
                ]
                assert sum(column_sizes) == marked
                assert min(column_sizes) >= s
                part_count = s + a + length
                assert part_count == ((s + a) * (s + b)) // s
                # Exact target-construction profile: marked columns have two
                # consecutive sizes, with total excess t above size s.
                assert max(column_sizes) - min(column_sizes) <= 1
                assert sum(size - s for size in column_sizes) == t
                assert sum(size == s + excess_base + 1 for size in column_sizes) == (
                    excess_remainder
                )
                digest.update(
                    f"{s}:{a}:{b}:{q}:{t}:{length}:"
                    f"{excess_base}:{excess_remainder}\n".encode()
                )
                cases += 1
    return cases, digest.hexdigest()


def qualifying_pair(sides: Sequence[int], s: int) -> tuple[int, int, int] | None:
    if s < 2:
        return None
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        if sides[first] < s or sides[second] < s:
            continue
        tau = (sides[first] * sides[second]) % s
        if sides[remaining] * tau < s:
            return first, second, remaining
    return None


def audit_hamming_parameters(max_side: int) -> tuple[int, int, str]:
    near_triangle = 0
    certified = 0
    digest = hashlib.sha256()
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    orders = (n1, n2, n3, n4)
                    deficits = tuple(order - 1 for order in orders)
                    h = (sum(deficits) + 1) // 2
                    if h < deficits[0]:
                        continue
                    near_triangle += 1
                    s = h - deficits[0] + 1
                    sides = orders[1:]
                    pair = qualifying_pair(sides, s)
                    if pair is None:
                        continue
                    first, second, remaining = pair
                    rectangle_q, tau = divmod(sides[first] * sides[second], s)
                    assert sides[remaining] * tau < s
                    layer_count = sides[remaining] * rectangle_q
                    assert layer_count == math.prod(sides) // s
                    assert deficits[0] + s - 1 == h
                    digest.update(f"{orders}:{s}:{pair}:{layer_count}\n".encode())
                    certified += 1
    return near_triangle, certified, digest.hexdigest()


def audit_family(max_k: int) -> tuple[int, str]:
    digest = hashlib.sha256()
    checked = 0
    for k in range(2, max_k + 1):
        s = k * k
        orders = (s + 2 * k + 3, s + k, s + k, s + 2)
        deficits = tuple(order - 1 for order in orders)
        h = (sum(deficits) + 1) // 2
        assert h == 2 * s + 2 * k + 1
        assert h - deficits[0] + 1 == s
        assert (orders[1] * orders[2]) % s == 0
        assert math.prod(order % s for order in orders[1:]) == 2 * s
        exact = math.prod(orders[1:]) // s
        assert exact == (k + 1) ** 2 * (s + 2)
        digest.update(f"{k}:{orders}:{h}:{exact}\n".encode())
        checked += 1
    return checked, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-max-s", type=int, default=5)
    parser.add_argument("--small-max-side", type=int, default=8)
    parser.add_argument("--corner-max-s", type=int, default=200)
    parser.add_argument("--parameter-max-side", type=int, default=60)
    parser.add_argument("--family-max-k", type=int, default=10000)
    args = parser.parse_args()

    independent = audit_independent_rectangles(
        args.small_max_s, args.small_max_side
    )
    corners = audit_corner_arithmetic(args.corner_max_s)
    hamming = audit_hamming_parameters(args.parameter_max_side)
    family = audit_family(args.family_max_k)

    summary = (
        f"independent balanced rectangle partitions: {independent[0]}\n"
        f"independent witness digest: {independent[1]}\n"
        f"cyclic corner parameter triples: {corners[0]}\n"
        f"corner arithmetic digest: {corners[1]}\n"
        f"near-triangle quadruples: {hamming[0]}\n"
        f"pair-remainder exact quadruples: {hamming[1]}\n"
        f"Hamming parameter digest: {hamming[2]}\n"
        f"explicit family indices: {family[0]}\n"
        f"family digest: {family[1]}\n"
        "all independent checks passed"
    )
    print(summary)


if __name__ == "__main__":
    main()
