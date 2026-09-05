#!/usr/bin/env python3
"""Search a pointwise binary root lift of an aggregate witness."""

from argparse import ArgumentParser
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_array


@lru_cache(None)
def upper(red, blue):
    if min(red, blue) == 1:
        return 1
    left, right = upper(red - 1, blue), upper(red, blue - 1)
    return left + right - int(left % 2 == right % 2 == 0)


def decode_core(order, mask):
    adjacency = [set() for _ in range(order)]
    for bit, (left, right) in enumerate(combinations(range(order), 2)):
        if mask >> bit & 1:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return tuple(frozenset(row) for row in adjacency)


def roots(adjacency):
    order = len(adjacency)
    for word in product(range(3), repeat=order):
        red = frozenset(i for i, value in enumerate(word) if value == 1)
        blue = frozenset(i for i, value in enumerate(word) if value == 2)
        if not red | blue:
            continue
        if any(right not in adjacency[left] for left, right in combinations(red, 2)):
            continue
        if any(right in adjacency[left] for left, right in combinations(blue, 2)):
            continue
        fixed = frozenset(
            i for i in range(order) if i not in red | blue
            and red <= adjacency[i] and not blue & adjacency[i]
        )
        yield red, blue, fixed, 5 - len(red), 5 - len(blue)


def build(document):
    record = document["record"]
    adjacency = decode_core(7, record["core_mask"])
    labels = []
    for mask, value in record["cells"]:
        labels.extend([mask] * value)
    pairs = tuple(combinations(range(36), 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    target_edges = {(a, b): value for a, b, value in document["aggregate_edges"]}
    row_indices, columns, data, lower, upper_bounds, names = [], [], [], [], [], []

    def add(name, entries, lo, hi):
        row = len(lower)
        for column, coefficient in entries:
            if coefficient:
                row_indices.append(row); columns.append(column); data.append(coefficient)
        lower.append(lo); upper_bounds.append(hi); names.append(name)

    cells = sorted(dict(record["cells"]))
    for cell_index, left_cell in enumerate(cells):
        for right_cell in cells[cell_index:]:
            left_vertices = [i for i, label in enumerate(labels) if label == left_cell]
            right_vertices = [i for i, label in enumerate(labels) if label == right_cell]
            literal = combinations(left_vertices, 2) if left_cell == right_cell else product(left_vertices, right_vertices)
            entries = [(pair_index[tuple(sorted(pair))], 1) for pair in literal]
            if entries:
                target = target_edges.get((left_cell, right_cell), 0)
                add(("quota", left_cell, right_cell), entries, target, target)
    for vertex, label in enumerate(labels):
        entries = [(index, 1) for index, pair in enumerate(pairs) if vertex in pair]
        target = 21 - label.bit_count()
        add(("degree", vertex), entries, target, target)

    lifted = {"red": 0, "blue": 0}
    for root_index, (red, blue, fixed, p, q) in enumerate(roots(adjacency)):
        selected = frozenset(
            vertex for vertex, label in enumerate(labels)
            if all(label >> i & 1 for i in red) and all(not (label >> i & 1) for i in blue)
        )
        for vertex, label in enumerate(labels):
            entries = [
                (pair_index[tuple(sorted((vertex, other)))], 1)
                for other in selected if other != vertex
            ]
            if all(label >> i & 1 for i in red):
                fixed_red = sum(label >> i & 1 for i in fixed)
                add(("root-red", root_index, vertex), entries, -np.inf,
                    upper(p - 1, q) - 1 - fixed_red)
                lifted["red"] += 1
            if all(not (label >> i & 1) for i in blue):
                fixed_blue = sum(not (label >> i & 1) for i in fixed)
                possible = len(selected) - int(vertex in selected)
                add(("root-blue", root_index, vertex), entries,
                    possible + fixed_blue - (upper(p, q - 1) - 1), np.inf)
                lifted["blue"] += 1
    matrix = coo_array(
        (data, (row_indices, columns)), shape=(len(lower), len(pairs)), dtype=float
    ).tocsr()
    return labels, pairs, matrix, np.asarray(lower), np.asarray(upper_bounds), names, lifted


def solve(document, time_limit):
    labels, pairs, matrix, lower, upper_bounds, names, lifted = build(document)
    result = milp(
        np.zeros(len(pairs)), integrality=np.ones(len(pairs)), bounds=Bounds(0, 1),
        constraints=LinearConstraint(matrix, lower, upper_bounds),
        options={"time_limit": time_limit, "mip_rel_gap": 0.0},
    )
    if not result.success:
        return None
    values = tuple(int(round(value)) for value in result.x)
    totals = matrix @ np.asarray(values)
    for name, total, lo, hi in zip(names, totals, lower, upper_bounds):
        if not lo <= total <= hi:
            raise ValueError((name, total, lo, hi))
    return labels, pairs, values, matrix.shape[0], lifted


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    args = parser.parse_args()
    document = json.loads(args.input.read_text())
    result = solve(document, args.time_limit)
    if result is None:
        print("No binary pointwise lift found")
        raise SystemExit(2)
    labels, pairs, values, row_count, lifted = result
    output = {
        **document,
        "format": "r55-m216-height2715-cut-pointwise-survivor-v1",
        "central_labels": labels,
        "central_red_edges": [[left, right] for (left, right), value in zip(pairs, values) if value],
        "binary_variables": len(pairs),
        "pointwise_rows": row_count,
        "pointwise_lifted_counts": lifted,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"PASS {sum(values)} central red edges and {sum(lifted.values())} pointwise lifting bounds")


if __name__ == "__main__":
    main()
