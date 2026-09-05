#!/usr/bin/env python3
"""Independent exact audit of the all-large three-box line partition.

This checker was written from the theorem statement and proof identities.  It
uses a cell-to-owner map and normalized residue boxes, unlike the reviewed
artifact's ordered list-of-parts audit.  Finite checks corroborate, but do not
replace, the universal proof in README.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import product
import json
from math import prod
from typing import Hashable


Cell = tuple[int, ...]
Label = tuple[Hashable, ...]
Parts = dict[Label, set[Cell]]

SOURCE_ARTIFACT = "bafkreiaw6tpwigyze5zqmadeshbtf2vjtbabwagejmauvltlc4xg3xjzx4"
SOURCE_COMMIT = "f965d900f1db9d32c185e08eaa8f1167d2e418fc"
SOURCE_EXPECTED_SHA256 = (
    "416bc07c0e0a186a84decee3e83379c78aa213bca1371902bfaa19dadd30d114"
)


@dataclass
class RectangleCertificate:
    parts: Parts
    large_label_by_column: dict[int, Label]
    anchor_row: int
    core_columns: tuple[int, ...]


def _install(parts: Parts, label: Label, cells: set[Cell]) -> None:
    assert label not in parts
    assert cells
    parts[label] = cells


def _varying_axes(cells: set[Cell]) -> tuple[int, ...]:
    dimension = len(next(iter(cells)))
    return tuple(
        axis for axis in range(dimension) if len({cell[axis] for cell in cells}) > 1
    )


def validate_partition(parts: Parts, dimensions: tuple[int, ...], s: int) -> tuple[int, int]:
    """Check every cell and every part directly through an owner map."""

    assert s >= 2 and all(length >= s for length in dimensions)
    owners: dict[Cell, Label] = {}
    large_count = 0
    for label, cells in parts.items():
        assert len(cells) in (s, s + 1)
        large_count += len(cells) == s + 1
        assert len(_varying_axes(cells)) == 1
        for cell in cells:
            assert len(cell) == len(dimensions)
            assert all(0 <= coordinate < bound for coordinate, bound in zip(cell, dimensions))
            assert cell not in owners
            owners[cell] = label
    assert len(owners) == prod(dimensions)
    return len(parts), large_count


def rectangle_certificate(m: int, n: int, s: int, shift: int = 0) -> RectangleCertificate:
    """Construct the anchored rectangle certificate using labelled owners."""

    if s < 2 or m < s or n < s:
        raise ValueError("require m,n >= s >= 2")

    row_blocks, a = divmod(m, s)
    column_blocks, b = divmod(n, s)
    parts: Parts = {}

    if a == 0:
        for column in range(n):
            for block in range(row_blocks):
                label = ("row-axis", column, block)
                cells = {(row, column) for row in range(block * s, (block + 1) * s)}
                _install(parts, label, cells)
        return RectangleCertificate(parts, {}, 0, tuple(range(n)))

    if b == 0:
        for row in range(m):
            for block in range(column_blocks):
                label = ("column-axis", row, block)
                cells = {(row, column) for column in range(block * s, (block + 1) * s)}
                _install(parts, label, cells)
        return RectangleCertificate(parts, {}, 0, tuple(range(n)))

    core_row_start = (row_blocks - 1) * s
    core_column_start = (column_blocks - 1) * s
    core_rows = tuple(range(core_row_start, m))
    core_columns = tuple(range(core_column_start, n))

    # Remove exact strips before treating the (s+a)-by-(s+b) corner.
    for column in range(n):
        for block in range(row_blocks - 1):
            label = ("outer-row-axis", column, block)
            cells = {(row, column) for row in range(block * s, (block + 1) * s)}
            _install(parts, label, cells)
    for row in core_rows:
        for block in range(column_blocks - 1):
            label = ("outer-column-axis", row, block)
            cells = {(row, column) for column in range(block * s, (block + 1) * s)}
            _install(parts, label, cells)

    q, tau = divmod(a * b, s)
    sparse_count = a + q
    sparse_rows = core_rows[:sparse_count]
    full_rows = core_rows[sparse_count:]
    assert q <= a - 1 and len(full_rows) == s - q > 0

    width = len(core_columns)
    rotated_column = tuple(core_columns[(local + shift) % width] for local in range(width))
    marked: dict[int, set[Cell]] = {local: set() for local in range(width)}

    for sparse_index, row in enumerate(sparse_rows):
        marked_locals = {(sparse_index * b + offset) % width for offset in range(b)}
        assert len(marked_locals) == b
        row_cells = {
            (row, rotated_column[local])
            for local in range(width)
            if local not in marked_locals
        }
        _install(parts, ("corner-row", row), row_cells)
        for local in marked_locals:
            marked[local].add((row, rotated_column[local]))

    for row in full_rows:
        for local in range(width):
            marked[local].add((row, rotated_column[local]))

    large_label_by_column: dict[int, Label] = {}
    for local in range(width):
        column = rotated_column[local]
        label = ("corner-column", column)
        _install(parts, label, marked[local])
        if local < tau:
            large_label_by_column[column] = label

    return RectangleCertificate(parts, large_label_by_column, full_rows[0], core_columns)


def verify_rectangle(m: int, n: int, s: int, shift: int = 0) -> tuple[int, int, int]:
    certificate = rectangle_certificate(m, n, s, shift)
    part_count, large_count = validate_partition(certificate.parts, (m, n), s)
    quotient, remainder = divmod(m * n, s)
    assert part_count == quotient
    assert large_count == remainder == len(certificate.large_label_by_column)
    for column, label in certificate.large_label_by_column.items():
        assert (certificate.anchor_row, column) in certificate.parts[label]
    return part_count, m * n, large_count


def box_certificate(m: int, n: int, p: int, s: int) -> Parts:
    """Build the three-box partition and perform the carry swaps by label."""

    if s < 2 or min(m, n, p) < s:
        raise ValueError("require m,n,p >= s >= 2")

    vertical_blocks, residual_layers = divmod(p, s)
    _, pair_remainder = divmod(m * n, s)
    parts: Parts = {}
    first_vertical: dict[tuple[int, int], Label] = {}

    for row in range(m):
        for column in range(n):
            for block in range(vertical_blocks):
                label = ("vertical", row, column, block)
                cells = {
                    (row, column, layer)
                    for layer in range(block * s, (block + 1) * s)
                }
                _install(parts, label, cells)
                if block == 0:
                    first_vertical[(row, column)] = label

    donors: list[tuple[Label, Cell, int]] = []
    common_anchor: int | None = None
    common_core_columns: tuple[int, ...] | None = None
    for residual in range(residual_layers):
        rectangle = rectangle_certificate(m, n, s, residual * pair_remainder)
        if common_anchor is None:
            common_anchor = rectangle.anchor_row
            common_core_columns = rectangle.core_columns
        assert rectangle.anchor_row == common_anchor
        assert rectangle.core_columns == common_core_columns
        layer = vertical_blocks * s + residual

        embedded: dict[Label, Label] = {}
        for rectangle_label, base_cells in rectangle.parts.items():
            label = ("residual", residual) + rectangle_label
            embedded[rectangle_label] = label
            _install(parts, label, {(row, column, layer) for row, column in base_cells})

        if pair_remainder:
            assert common_core_columns is not None and common_anchor is not None
            width = len(common_core_columns)
            for local in range(pair_remainder):
                global_slot = residual * pair_remainder + local
                column = common_core_columns[global_slot % width]
                rectangle_label = rectangle.large_label_by_column[column]
                donors.append(
                    (
                        embedded[rectangle_label],
                        (common_anchor, column, layer),
                        column,
                    )
                )

    if not donors:
        return parts

    assert common_anchor is not None
    carry_count = (residual_layers * pair_remainder) // s
    assert carry_count <= s - 2
    for group in range(carry_count):
        carry_donors = donors[group * s : (group + 1) * s]
        assert len(carry_donors) == s
        assert len({column for _, _, column in carry_donors}) == s
        displaced_cells: set[Cell] = set()
        for donor_label, donor_cell, column in carry_donors:
            assert donor_cell in parts[donor_label]
            parts[donor_label].remove(donor_cell)

            recipient_label = first_vertical[(common_anchor, column)]
            displaced = (common_anchor, column, group)
            assert displaced in parts[recipient_label]
            assert donor_cell not in parts[recipient_label]
            parts[recipient_label].remove(displaced)
            parts[recipient_label].add(donor_cell)
            displaced_cells.add(displaced)
        _install(parts, ("carry-row", group), displaced_cells)
    return parts


def verify_box(m: int, n: int, p: int, s: int) -> tuple[int, int, int, int]:
    parts = box_certificate(m, n, p, s)
    part_count, large_count = validate_partition(parts, (m, n, p), s)
    quotient, remainder = divmod(m * n * p, s)
    carry_count = ((p % s) * ((m * n) % s)) // s
    assert part_count == quotient
    assert large_count == remainder
    return part_count, m * n * p, large_count, carry_count


def audit_residue_arithmetic(max_s: int = 64) -> dict[str, object]:
    """Audit every normalized residue state without enumerating its cells."""

    digest = sha256()
    states = positive_carry_states = 0
    maximum_carry = 0
    for s in range(2, max_s + 1):
        for a, b, c in product(range(s), repeat=3):
            m, n, p = s + a, s + b, s + c
            pair_quotient, tau = divmod(m * n, s)
            carry, remainder = divmod(c * tau, s)
            proposed_count = m * n + c * pair_quotient + carry
            quotient, volume_remainder = divmod(m * n * p, s)
            assert proposed_count == quotient
            assert remainder == volume_remainder
            assert carry <= s - 2
            if a and b:
                q = (a * b) // s
                assert q <= a - 1 and s - q > 0
            if carry:
                positive_carry_states += 1
                width = s + b
                assert width >= s
                for group in range(carry):
                    start = group * s
                    assert start + s - 1 - start < width
            maximum_carry = max(maximum_carry, carry)
            states += 1
            digest.update(
                f"{s}:{a}:{b}:{c}:{pair_quotient}:{tau}:{carry}:{remainder}\n".encode()
            )
    return {
        "max_s": max_s,
        "states": states,
        "positive_carry_states": positive_carry_states,
        "maximum_carry": maximum_carry,
        "sha256": digest.hexdigest(),
    }


def audit_cell_partitions(max_s: int = 9) -> dict[str, object]:
    digest = sha256()
    boxes = parts_checked = cells_checked = positive_carries = 0
    for s in range(2, max_s + 1):
        for a, b, c in product(range(s), repeat=3):
            result = verify_box(s + a, s + b, s + c, s)
            part_count, volume, large_count, carry = result
            boxes += 1
            parts_checked += part_count
            cells_checked += volume
            positive_carries += carry > 0
            digest.update(f"{s}:{a}:{b}:{c}:{result}\n".encode())
    return {
        "max_s": max_s,
        "boxes": boxes,
        "parts": parts_checked,
        "cells": cells_checked,
        "positive_carry_boxes": positive_carries,
        "sha256": digest.hexdigest(),
    }


def audit_quotient_extensions(max_s: int = 9) -> dict[str, object]:
    """Check nontrivial exact strips using a sparse adversarial residue grid."""

    digest = sha256()
    boxes = parts_checked = cells_checked = 0
    for s in range(2, max_s + 1):
        residues = sorted({0, 1, s // 2, s - 1})
        for a, b, c in product(residues, repeat=3):
            dimensions = (2 * s + a, 3 * s + b, 2 * s + c)
            result = verify_box(*dimensions, s)
            boxes += 1
            parts_checked += result[0]
            cells_checked += result[1]
            digest.update(f"{s}:{dimensions}:{result}\n".encode())
    return {
        "max_s": max_s,
        "boxes": boxes,
        "parts": parts_checked,
        "cells": cells_checked,
        "sha256": digest.hexdigest(),
    }


def audit_shell_bound(max_order: int = 8) -> dict[str, int]:
    """Definition-level bounded audit of the inherited class-size inequality."""

    parameter_rows = profiles = 0
    for n1 in range(2, max_order + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    caps = (n1 - 1, n2 - 1, n3 - 1, n4 - 1)
                    h = (sum(caps) + 1) // 2
                    if h < caps[0]:
                        continue
                    s = h - caps[0] + 1
                    assert h <= caps[0] + caps[1]
                    parameter_rows += 1
                    for first_shell in product(*(range(cap + 1) for cap in caps)):
                        A = sum(first_shell)
                        if A < h:
                            continue
                        twice_lower_bound = 2 + 2 * A + sum(
                            count * (h - count) for count in first_shell
                        )
                        assert twice_lower_bound >= 2 * n1 * s
                        profiles += 1
    return {"max_order": max_order, "parameter_rows": parameter_rows, "profiles": profiles}


def audit_hamming_family(max_k: int = 10_000) -> dict[str, int]:
    for k in range(3, max_k + 1):
        s = k * k - k
        quotient, remainder = divmod(k**6, s)
        assert quotient == k**4 + k**3 + k**2 + k + 1
        assert remainder == k
        n1 = k * k + 2 * k
        h = 2 * k * k + k - 2
        assert s == h - (n1 - 1) + 1
        assert k * k >= s
    base = verify_box(9, 9, 9, 6)
    assert base[:3] == (121, 729, 3)
    return {"max_k": max_k, "base_k": 3, "base_parts": base[0]}


def certificate() -> dict[str, object]:
    arithmetic = audit_residue_arithmetic()
    cells = audit_cell_partitions()
    extensions = audit_quotient_extensions()
    shell = audit_shell_bound()
    family = audit_hamming_family()
    assert arithmetic == {
        "max_s": 64,
        "states": 4_326_399,
        "positive_carry_states": 3_640_822,
        "maximum_carry": 62,
        "sha256": "30f86cdd4306c27f0484082d5baf1c2175b9af67bd40ea0995ad7a7c7b060c52",
    }
    assert cells == {
        "max_s": 9,
        "boxes": 2_024,
        "parts": 357_737,
        "cells": 2_911_328,
        "positive_carry_boxes": 810,
        "sha256": "50a83116d01e0155170fc21960db641a54df3e4cee06e4413467201a7f8a965c",
    }
    assert extensions == {
        "max_s": 9,
        "boxes": 419,
        "parts": 331_421,
        "cells": 2_410_928,
        "sha256": "4a0f605712bcc901fd95f68e6f7be779676cfca6a1a7ee3c8f1987c2bdfc56e0",
    }
    assert shell == {"max_order": 8, "parameter_rows": 203, "profiles": 77_511}
    assert family == {"max_k": 10_000, "base_k": 3, "base_parts": 121}
    return {
        "verdict": "ACCEPT",
        "verified_claim": "every m,n,p>=s>=2 has a balanced floor(m*n*p/s) coordinate-line partition",
        "source_artifact": SOURCE_ARTIFACT,
        "source_commit": SOURCE_COMMIT,
        "source_expected_output_sha256": SOURCE_EXPECTED_SHA256,
        "arithmetic_residue_audit": arithmetic,
        "cell_owner_audit": cells,
        "quotient_extension_audit": extensions,
        "bounded_shell_inequality_audit": shell,
        "hamming_first_carry_family_audit": family,
        "primary_scope": "rectangle existence is prior art; universal capacity choice and carry exchange remain candidate-new",
        "trust_boundary": "human proof is universal; exact finite audits are corroboration",
    }


def main() -> None:
    data = certificate()
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    print(json.dumps(data, sort_keys=True, indent=2))
    print(f"certificate_sha256={sha256(canonical.encode()).hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
