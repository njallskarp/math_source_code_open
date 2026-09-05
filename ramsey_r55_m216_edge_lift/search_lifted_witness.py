#!/usr/bin/env python3
"""Discover the exact M=216 aggregate-edge limitation witness."""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_array, csr_array, vstack

import model


B = {18: 220, 19: 221, 20: 220, 21: 220, 22: 221, 23: 223, 24: 223}
DEGREES = (19, 19, 20, 20, 20, 20, 20)
M = 216


@lru_cache(None)
def upper(red, blue):
    if min(red, blue) == 1:
        return 1
    left, right = upper(red - 1, blue), upper(red, blue - 1)
    return left + right - int(left % 2 == right % 2 == 0)


def core_constraints(exclusions):
    epsilon = tuple(degree - 21 for degree in DEGREES)
    edges = tuple(combinations(range(len(DEGREES)), 2))
    rows, lower, upper_bounds = [], [], []
    for vertex, degree in enumerate(DEGREES):
        rows.append([
            epsilon[right] if left == vertex else epsilon[left] if right == vertex else 0
            for left, right in edges
        ])
        lower.append(-np.inf)
        upper_bounds.append(M - B[degree])
    central_constant = sum(weight * degree for weight, degree in zip(epsilon, DEGREES))
    rows.append([epsilon[left] + epsilon[right] for left, right in edges])
    lower.append(central_constant - 36 * (M - 220))
    upper_bounds.append(np.inf)
    for subset in combinations(range(len(DEGREES)), 5):
        chosen = set(subset)
        rows.append([int(left in chosen and right in chosen) for left, right in edges])
        lower.append(1)
        upper_bounds.append(9)
    for mask in exclusions:
        ones = mask.bit_count()
        rows.append([1 if mask >> index & 1 else -1 for index in range(len(edges))])
        lower.append(-np.inf)
        upper_bounds.append(ones - 1)
    return edges, LinearConstraint(np.asarray(rows, dtype=float), lower, upper_bounds)


def solve_core(exclusions, seed):
    edges, constraints = core_constraints(exclusions)
    objective = np.random.default_rng(seed).integers(-1000, 1001, size=len(edges)).astype(float)
    result = milp(
        objective, integrality=np.ones(len(edges)), bounds=Bounds(0, 1),
        constraints=constraints, options={"time_limit": 20},
    )
    if not result.success:
        return None
    values = tuple(int(round(value)) for value in result.x)
    if any(value not in (0, 1) for value in values):
        raise ValueError("nonbinary core proposal")
    return sum(value << index for index, value in enumerate(values))


def adjacency(mask):
    answer = [0] * len(DEGREES)
    for index, (left, right) in enumerate(combinations(range(len(DEGREES)), 2)):
        if mask >> index & 1:
            answer[left] |= 1 << right
            answer[right] |= 1 << left
    return tuple(answer)


def subset_tables(adjacency_rows):
    full = (1 << len(DEGREES)) - 1
    omega = [0] * (1 << len(DEGREES))
    alpha = [0] * (1 << len(DEGREES))
    red = [False] * (1 << len(DEGREES))
    blue = [False] * (1 << len(DEGREES))
    red[0] = blue[0] = True
    for mask in range(1, 1 << len(DEGREES)):
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        omega[mask] = max(omega[rest], 1 + omega[rest & adjacency_rows[vertex]])
        alpha[mask] = max(
            alpha[rest], 1 + alpha[rest & (full ^ adjacency_rows[vertex] ^ (1 << vertex))]
        )
        red[mask] = red[rest] and rest & ~adjacency_rows[vertex] == 0
        blue[mask] = blue[rest] and rest & adjacency_rows[vertex] == 0
    return omega, alpha, red, blue


def signature_data(adjacency_rows):
    full = (1 << len(DEGREES)) - 1
    omega, alpha, red, blue = subset_tables(adjacency_rows)
    signatures, capacities = [], []
    for mask in range(1 << len(DEGREES)):
        weight = sum(DEGREES[i] - 21 for i in range(len(DEGREES)) if mask >> i & 1)
        if weight > M - 220:
            continue
        red_number = omega[mask]
        blue_number = alpha[full ^ mask]
        if red_number >= 4 or blue_number >= 4:
            continue
        signatures.append(mask)
        capacities.append(min(36, upper(5 - red_number, 5 - blue_number) - 1))
    return tuple(signatures), tuple(capacities), red, blue


def union_rows(adjacency_rows, signatures, red, blue):
    full = (1 << len(DEGREES)) - 1
    index = {mask: column for column, mask in enumerate(signatures)}
    row_indices, columns, data, bounds = [], [], [], []
    row_number = 0
    for red_root, red_valid in enumerate(red):
        if not red_valid:
            continue
        for blue_root, blue_valid in enumerate(blue):
            if not blue_valid or red_root & blue_root or not red_root | blue_root:
                continue
            outside = full ^ (red_root | blue_root)
            fixed = sum(
                adjacency_rows[vertex] & red_root == red_root
                and not adjacency_rows[vertex] & blue_root
                for vertex in range(len(DEGREES)) if outside >> vertex & 1
            )
            bounds.append(
                upper(5 - red_root.bit_count(), 5 - blue_root.bit_count()) - 1 - fixed
            )
            subset = outside
            while True:
                mask = red_root | subset
                if mask in index:
                    row_indices.append(row_number)
                    columns.append(index[mask])
                    data.append(1)
                if subset == 0:
                    break
                subset = (subset - 1) & outside
            row_number += 1
    matrix = coo_array(
        (data, (row_indices, columns)), shape=(row_number, len(signatures)), dtype=float
    ).tocsr()
    return matrix, np.asarray(bounds, dtype=float), row_number


def solve_cells(adjacency_rows, seed):
    signatures, capacities, red, blue = signature_data(adjacency_rows)
    targets = [36] + [degree - adjacency_rows[i].bit_count() for i, degree in enumerate(DEGREES)]
    equalities = csr_array(np.asarray(
        [[1] * len(signatures)]
        + [[int(mask >> i & 1) for mask in signatures] for i in range(len(DEGREES))],
        dtype=float,
    ))
    unions, union_bounds, root_count = union_rows(adjacency_rows, signatures, red, blue)
    matrix = vstack((equalities, unions), format="csr")
    lower = np.concatenate((np.asarray(targets, dtype=float), np.full(root_count, -np.inf)))
    upper_bounds = np.concatenate((np.asarray(targets, dtype=float), union_bounds))
    objective = np.random.default_rng(seed).integers(-1000, 1001, size=len(signatures)).astype(float)
    result = milp(
        objective, integrality=np.ones(len(signatures)),
        bounds=Bounds(0, np.asarray(capacities, dtype=float)),
        constraints=LinearConstraint(matrix, lower, upper_bounds), options={"time_limit": 30},
    )
    if not result.success:
        return None
    cell_values = tuple(int(round(value)) for value in result.x)
    if list(equalities @ np.asarray(cell_values)) != targets:
        raise ValueError("cell margins")
    sides = []
    for red_root in range(len(DEGREES)):
        for blue_root in range(len(DEGREES)):
            if red_root == blue_root:
                continue
            fixed = sum(
                vertex not in (red_root, blue_root)
                and adjacency_rows[red_root] >> vertex & 1
                and not adjacency_rows[blue_root] >> vertex & 1
                for vertex in range(len(DEGREES))
            )
            central = sum(
                value for mask, value in zip(signatures, cell_values)
                if mask >> red_root & 1 and not mask >> blue_root & 1
            )
            sides.append(fixed + central)
    return {
        "cells": [[mask, value] for mask, value in zip(signatures, cell_values) if value],
        "eligible_signatures": len(signatures),
        "union_cuts": root_count,
        "maximum_exceptional_root_side": max(sides),
        "side_size_histogram": dict(sorted(Counter(sides).items())),
    }


def lift(record, time_limit):
    pairs, boxes, rows = model.build(record, stage=2)
    matrix = np.asarray([row for _, row, _, _ in rows], dtype=float)
    lower = np.asarray([lo for _, _, lo, _ in rows], dtype=float)
    upper = np.asarray([hi for _, _, _, hi in rows], dtype=float)
    result = milp(
        np.zeros(len(pairs)),
        integrality=np.ones(len(pairs)),
        bounds=Bounds(np.zeros(len(pairs)), np.asarray(boxes, dtype=float)),
        constraints=LinearConstraint(matrix, lower, upper),
        options={"time_limit": time_limit, "mip_rel_gap": 0.0},
    )
    if not result.success:
        return None
    values = tuple(int(round(value)) for value in result.x)
    if any(not lo <= sum(a * z for a, z in zip(row, values)) <= hi
           for _, row, lo, hi in rows):
        raise ValueError("rounded edge lift rejected")
    return pairs, values, len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--core-attempts", type=int, default=50)
    parser.add_argument("--cell-attempts", type=int, default=50)
    parser.add_argument("--edge-time-limit", type=float, default=10)
    args = parser.parse_args()

    excluded = []
    seen = set()
    trials = 0
    for core_attempt in range(args.core_attempts):
        seed = 9100009 + M * 100003 + core_attempt * 7919
        core = solve_core(excluded, seed)
        if core is None:
            break
        excluded.append(core)
        adjacency_rows = adjacency(core)
        for cell_attempt in range(args.cell_attempts):
            candidate = solve_cells(adjacency_rows, seed + 104729 * (cell_attempt + 1))
            if candidate is None:
                break
            cell_key = tuple(tuple(pair) for pair in candidate["cells"])
            if cell_key in seen:
                continue
            seen.add(cell_key)
            trials += 1
            record = {
                "counts_18_to_24": "0,2,5,36,0,0,0",
                "M": M,
                "split_count": 3,
                "exceptional_degrees": list(DEGREES),
                "core_mask": core,
                **candidate,
            }
            result = lift(record, args.edge_time_limit)
            print(
                f"trial={trials} core={core} cells={len(record['cells'])} "
                f"side={record['maximum_exceptional_root_side']} lifted={result is not None}",
                flush=True,
            )
            if result is None:
                continue
            pairs, values, row_count = result
            document = {
                "format": "r55-double19-external-root-lift-v1",
                "record": record,
                "aggregate_edges": [
                    [left, right, value]
                    for (left, right), value in zip(pairs, values) if value
                ],
                "edge_variables": len(pairs),
                "generated_two_sided_rows": row_count,
                "search_trials": trials,
            }
            args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
            print(f"FOUND M={M} after {trials} distinct cell vectors", flush=True)
            return
    raise SystemExit(f"NO WITNESS after {trials} distinct cell vectors and {len(excluded)} cores")


if __name__ == "__main__":
    main()
