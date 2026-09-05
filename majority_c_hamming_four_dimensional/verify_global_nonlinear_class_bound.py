#!/usr/bin/env python3
"""Exact finite audit of the global nonlinear Hamming-class bound.

CPython 3.12+, standard library only.  This checker exhausts bounded Hamming
hosts and audits the first-carry arithmetic.  The universal proof is in
GLOBAL_NONLINEAR_CLASS_BOUND.md.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections.abc import Iterable, Sequence


Cell = tuple[int, ...]


def vertices(sides: Sequence[int]) -> tuple[Cell, ...]:
    return tuple(itertools.product(*(range(side) for side in sides)))


def adjacent(left: Cell, right: Cell) -> bool:
    return sum(a != b for a, b in zip(left, right, strict=True)) == 1


def neighbor_masks(cells: Sequence[Cell]) -> tuple[int, ...]:
    masks: list[int] = []
    for left in cells:
        mask = 0
        for index, right in enumerate(cells):
            if adjacent(left, right):
                mask |= 1 << index
        masks.append(mask)
    return tuple(masks)


def coordinate_line_masks(cells: Sequence[Cell]) -> tuple[int, ...]:
    dimension = len(cells[0])
    masks: list[int] = []
    for axis in range(dimension):
        groups: dict[tuple[int, ...], int] = {}
        for index, cell in enumerate(cells):
            key = cell[:axis] + cell[axis + 1 :]
            groups[key] = groups.get(key, 0) | (1 << index)
        masks.extend(groups.values())
    return tuple(masks)


def contained_in_line(mask: int, line_masks: Sequence[int]) -> bool:
    return any(mask & ~line_mask == 0 for line_mask in line_masks)


def induced_min_degree(mask: int, neighborhoods: Sequence[int]) -> int:
    return min(
        (neighborhoods[index] & mask).bit_count()
        for index in range(len(neighborhoods))
        if mask & (1 << index)
    )


def is_prism(cells: Iterable[Cell], h: int) -> bool:
    """Recognize X x {0,1} with |X|=h, up to coordinates and symbols."""

    selected = tuple(sorted(cells))
    if len(selected) != 2 * h or not selected:
        return False
    dimension = len(selected[0])
    for axis in range(dimension):
        groups: dict[tuple[int, ...], set[int]] = {}
        for cell in selected:
            key = cell[:axis] + cell[axis + 1 :]
            groups.setdefault(key, set()).add(cell[axis])
        if len(groups) != 2:
            continue
        (key_1, values_1), (key_2, values_2) = groups.items()
        if len(values_1) != h or values_1 != values_2:
            continue
        if sum(a != b for a, b in zip(key_1, key_2, strict=True)) == 1:
            return True
    return False


def selected_cells(mask: int, cells: Sequence[Cell]) -> tuple[Cell, ...]:
    return tuple(cell for index, cell in enumerate(cells) if mask & (1 << index))


def audit_small_hosts(
    max_dimension: int, max_side: int, max_host_cells: int
) -> dict[str, int | str]:
    hosts = subsets = nonlinear = claims = equality = 0
    equality_records: list[tuple[tuple[int, ...], int, tuple[Cell, ...]]] = []

    for dimension in range(2, max_dimension + 1):
        for sides in itertools.combinations_with_replacement(
            range(2, max_side + 1), dimension
        ):
            if math.prod(sides) > max_host_cells:
                continue
            hosts += 1
            cells = vertices(sides)
            neighborhoods = neighbor_masks(cells)
            lines = coordinate_line_masks(cells)
            for mask in range(1, 1 << len(cells)):
                subsets += 1
                if contained_in_line(mask, lines):
                    continue
                nonlinear += 1
                minimum_degree = induced_min_degree(mask, neighborhoods)
                size = mask.bit_count()
                for h in range(2, minimum_degree + 1):
                    claims += 1
                    if size < 2 * h:
                        raise AssertionError(
                            f"bound failure sides={sides} h={h} mask={mask}"
                        )
                    if size == 2 * h:
                        chosen = selected_cells(mask, cells)
                        if minimum_degree != h or not is_prism(chosen, h):
                            raise AssertionError(
                                f"rigidity failure sides={sides} h={h} cells={chosen}"
                            )
                        equality += 1
                        equality_records.append((sides, h, chosen))

    digest = hashlib.sha256(
        json.dumps(equality_records, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "hosts": hosts,
        "subsets": subsets,
        "nonlinear": nonlinear,
        "claims": claims,
        "equality": equality,
        "digest": digest,
    }


def audit_first_carry(max_s: int) -> dict[str, int | str]:
    patterns = below = equality = above = equality_illegal_tail = 0
    equality_records: list[tuple[int, int, int, int]] = []

    for s in range(3, max_s + 1):
        for r in range(1, s):
            for u in range(1, s):
                residue_product = r * u
                if residue_product >= s:
                    continue
                lower_p = max(2, (s + residue_product - 1) // residue_product)
                upper_p = min(s - 1, (2 * s - 1) // residue_product)
                for p in range(lower_p, upper_p + 1):
                    remainder = residue_product * p
                    if not s <= remainder < 2 * s:
                        raise AssertionError("first-carry range")

                    # A canonical large host; the identities are independent
                    # of the positive quotient coefficients.
                    m, n = 2 * s + r, 2 * s + u
                    line_count = p * (m * n // s)
                    volume = m * n * p
                    if volume != s * line_count + remainder:
                        raise AssertionError("Euclidean identity")
                    if volume // s != line_count + 1:
                        raise AssertionError("single carry")

                    patterns += 1
                    if remainder < 2 * s - 2:
                        below += 1
                    elif remainder == 2 * s - 2:
                        equality += 1
                        equality_records.append((s, r, u, p))
                        if r + u + p - 3 < s - 1:
                            equality_illegal_tail += 1
                    else:
                        above += 1

    if (5, 2, 2, 2) not in equality_records:
        raise AssertionError("missing (5,2,2,2) boundary case")
    digest = hashlib.sha256(
        json.dumps(equality_records, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "patterns": patterns,
        "below": below,
        "equality": equality,
        "above": above,
        "equality_illegal_tail": equality_illegal_tail,
        "digest": digest,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-dimension", type=int, default=4)
    parser.add_argument("--max-side", type=int, default=4)
    parser.add_argument("--max-host-cells", type=int, default=16)
    parser.add_argument("--max-s", type=int, default=500)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if (
        args.max_dimension < 2
        or args.max_side < 2
        or args.max_host_cells < 4
        or args.max_s < 5
    ):
        raise SystemExit("invalid positive audit bounds")

    hosts = audit_small_hosts(
        args.max_dimension, args.max_side, args.max_host_cells
    )
    carry = audit_first_carry(args.max_s)

    print(f"exhaustive Hamming hosts: {hosts['hosts']}")
    print(f"nonempty subsets checked: {hosts['subsets']}")
    print(f"nonlinear subsets checked: {hosts['nonlinear']}")
    print(f"legal nonlinear threshold claims: {hosts['claims']}")
    print(f"equality witnesses: {hosts['equality']}")
    print(f"equality witness SHA-256: {hosts['digest']}")
    print(f"first-carry patterns through s={args.max_s}: {carry['patterns']}")
    print(
        "first-carry remainder buckets below/equal/above 2s-2: "
        f"{carry['below']}/{carry['equality']}/{carry['above']}"
    )
    print(
        "equality patterns with illegal whole tail: "
        f"{carry['equality_illegal_tail']}"
    )
    print(f"equality-pattern SHA-256: {carry['digest']}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
