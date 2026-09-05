#!/usr/bin/env python3
"""Discover integral 20-order profiles for all 96 order-eight obstructions."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

from verify_certificate import agrees, order_vectors, parse_certificate


def solve_profile(
    tournament: int,
    dual: tuple[int, ...],
    orders: tuple[tuple[int, ...], ...],
) -> list[tuple[int, int]]:
    candidates = [
        index
        for index, order in enumerate(orders)
        if sum(agrees(tournament, order, edge) for edge in dual) == 13
    ]
    if len(candidates) != 832:
        raise ArithmeticError(f"expected 832 dual-tight orders, got {len(candidates)}")

    matrix = np.empty((29, len(candidates)), dtype=np.float64)
    matrix[0, :] = 1
    for edge in range(28):
        matrix[edge + 1, :] = [
            agrees(tournament, orders[index], edge) for index in candidates
        ]
    target = np.r_[20.0, np.full(28, 13.0)]
    result = milp(
        np.zeros(len(candidates)),
        integrality=np.ones(len(candidates)),
        bounds=Bounds(0, 20),
        constraints=LinearConstraint(csc_matrix(matrix), target, target),
    )
    if not result.success:
        raise RuntimeError(result.message)
    counts = np.rint(result.x).astype(int)
    if not np.array_equal(matrix @ counts, target):
        raise ArithmeticError("rounded MILP profile fails the exact integer equations")
    return [
        (candidates[column], int(count))
        for column, count in enumerate(counts)
        if count
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radial-certificate", type=Path, default=Path("certificate.txt"))
    parser.add_argument("--output", type=Path, default=Path("m6_profiles.txt"))
    args = parser.parse_args()

    records = parse_certificate(args.radial_certificate)
    orders = order_vectors()
    rows = [
        "CERTIFICATE stable_transitivity_m6_v1 n=8 classes=96 orders=20 margin=13",
        "# CLASS <source-index> tournament=<mask> profile=<order-index:multiplicity,...>",
    ]
    for number, (source_index, tournament, dual, _) in enumerate(records, 1):
        profile = solve_profile(tournament, dual, orders)
        profile_text = ",".join(f"{index}:{count}" for index, count in profile)
        rows.append(
            f"CLASS {source_index} tournament={tournament} profile={profile_text}"
        )
        print(f"generated {number}/96 class={source_index}", flush=True)
    args.output.write_text("\n".join(rows) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
