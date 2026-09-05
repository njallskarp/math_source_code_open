#!/usr/bin/env python3
"""Discover exact lower-bound profiles in the nonzero scale-six residues."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

from verify_certificate import agrees, order_vectors, parse_certificate


def solve_profile(
    dilation: int,
    tournament: int,
    dual: tuple[int, ...],
    orders: tuple[tuple[int, ...], ...],
) -> tuple[int, int, list[tuple[int, int]]]:
    stabilizer = (7 * dilation + 5) // 6
    profile_size = dilation + 2 * stabilizer
    margin = dilation + stabilizer
    allowed_deficit = 13 * profile_size - 20 * margin
    candidates = []
    for index, order in enumerate(orders):
        deficit = 13 - sum(agrees(tournament, order, edge) for edge in dual)
        if deficit <= allowed_deficit:
            candidates.append(index)

    matrix = np.empty((29, len(candidates)), dtype=np.float64)
    matrix[0, :] = 1
    for edge in range(28):
        matrix[edge + 1, :] = [
            agrees(tournament, orders[index], edge) for index in candidates
        ]
    target = np.r_[float(profile_size), np.full(28, float(margin))]
    constraints = LinearConstraint(csc_matrix(matrix), target, target)
    result = milp(
        np.zeros(len(candidates)),
        integrality=np.ones(len(candidates)),
        bounds=Bounds(0, 1),
        constraints=constraints,
    )
    if not result.success:
        raise RuntimeError(
            f"no square-free profile: d={dilation} status={result.status} "
            f"message={result.message} "
            f"candidates={len(candidates)} deficit={allowed_deficit}"
        )
    counts = np.rint(result.x).astype(int)
    if not np.array_equal(matrix @ counts, target):
        raise ArithmeticError("rounded MILP profile fails the exact integer equations")
    profile = [
        (candidates[column], int(count))
        for column, count in enumerate(counts)
        if count
    ]
    return allowed_deficit, len(candidates), profile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radial-certificate", type=Path, default=Path("certificate.txt"))
    parser.add_argument("--output", type=Path, default=Path("residue_profiles.txt"))
    parser.add_argument("--residues", default="2,3,4,5")
    parser.add_argument("--class-start", type=int, default=0)
    parser.add_argument("--class-stop", type=int)
    parser.add_argument("--class-limit", type=int)
    args = parser.parse_args()

    residues = tuple(int(value) for value in args.residues.split(","))
    if not residues or any(value < 1 or value > 5 for value in residues):
        raise ValueError("residues must lie in 1,...,5")
    records = parse_certificate(args.radial_certificate)
    if args.class_start < 0 or (
        args.class_stop is not None and args.class_stop < args.class_start
    ):
        raise ValueError("invalid class range")
    records = records[args.class_start : args.class_stop]
    if args.class_limit is not None:
        records = records[: args.class_limit]
    orders = order_vectors()
    rows = [
        "CERTIFICATE stable_transitivity_residue_profiles_v1 n=8",
        "# CLASS <source-index> tournament=<mask> dilation=<d> "
        "stabilizer=<a> deficit=<delta> candidates=<count> "
        "profile=<order-index:multiplicity,...>",
    ]
    for record_number, (source_index, tournament, dual, _) in enumerate(records, 1):
        for dilation in residues:
            deficit, candidate_count, profile = solve_profile(
                dilation, tournament, dual, orders
            )
            stabilizer = (7 * dilation + 5) // 6
            profile_text = ",".join(f"{index}:{count}" for index, count in profile)
            rows.append(
                f"CLASS {source_index} tournament={tournament} dilation={dilation} "
                f"stabilizer={stabilizer} deficit={deficit} "
                f"candidates={candidate_count} profile={profile_text}"
            )
            print(
                f"generated class={record_number}/{len(records)} source={source_index} "
                f"d={dilation} terms={len(profile)} candidates={candidate_count} "
                f"deficit={deficit}",
                flush=True,
            )
    args.output.write_text("\n".join(rows) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
