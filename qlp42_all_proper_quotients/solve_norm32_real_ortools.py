#!/usr/bin/env python3
"""CP-SAT search for the real Gray-component relaxation at norm 32."""

from __future__ import annotations

from argparse import ArgumentParser

from ortools.sat.python import cp_model

N = 42
TARGET_RESIDUAL = [0] * N
for shift in (4, 11, 31, 38):
    TARGET_RESIDUAL[shift] = -2
for shift in (10, 17, 25, 32):
    TARGET_RESIDUAL[shift] = 2

HEURISTIC_A = "j1j-ij--ij1-1i1jji1j1--1--iii111jiiiij-jj-"
HEURISTIC_B = "1j--iij1-iiiji-1i1jj11-i11-j-jji11-1ji--1-"
BITS = {"1": (0, 0), "i": (0, 1), "-": (1, 1), "j": (1, 0)}


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()

    model = cp_model.CpModel()
    families = {
        name: [model.new_bool_var(f"{name}_{index}") for index in range(N)]
        for name in ("au", "av", "bu", "bv")
    }
    model.add(sum(families["au"]) == 21)
    model.add(sum(families["av"]) == 21)
    model.add(sum(families["bu"]) == 20)
    model.add(sum(families["bv"]) == 21)

    for family in families.values():
        model.add(family[0] == 0)

    for shift in range(1, N // 2 + 1):
        differences = []
        for name, family in families.items():
            for index in range(N):
                different = model.new_bool_var(f"d_{shift}_{name}_{index}")
                model.add_bool_xor(
                    [family[index], family[(index + shift) % N], different.Not()]
                )
                differences.append(different)
        model.add(sum(differences) == 86 - TARGET_RESIDUAL[shift])

    for prefix, sequence in (("a", HEURISTIC_A), ("b", HEURISTIC_B)):
        for index, symbol in enumerate(sequence):
            for suffix, value in zip(("u", "v"), BITS[symbol]):
                model.add_hint(families[prefix + suffix][index], value)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.log_search_progress = args.log
    status = solver.solve(model)
    print(f"status={solver.status_name(status)}")
    print(f"wall_time={solver.wall_time:.6f}")
    print(f"conflicts={solver.num_conflicts}; branches={solver.num_branches}")
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return

    decoded: dict[str, list[int]] = {}
    for name, family in families.items():
        bits = [solver.value(bit) for bit in family]
        decoded[name] = bits
        print(f"{name}={''.join(map(str, bits))}")

    for shift in range(1, N):
        correlations = 0
        for bits in decoded.values():
            signs = [1 - 2 * bit for bit in bits]
            correlations += sum(
                signs[index] * signs[(index + shift) % N]
                for index in range(N)
            )
        assert correlations == 2 * (TARGET_RESIDUAL[shift] - 2)
    print("exact real autocorrelation verification passed")


if __name__ == "__main__":
    main()
