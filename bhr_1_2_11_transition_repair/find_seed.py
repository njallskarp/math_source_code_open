#!/usr/bin/env python3
"""CP-SAT generator for a BHR seed with selected simultaneous growth modes."""

from __future__ import annotations

import argparse
import json

from ortools.sat.python import cp_model

from verify import cyclic_length, changed_by_embedding, verify_growth, verify_realization

DEFAULT_COUNTS = (2, 18, 4)
SUPPORT = (1, 2, 11)
DEFAULT_GROWTH_MODES = (1, 2)


def solve(
    counts: tuple[int, int, int],
    seconds: float,
    growth_modes: tuple[int, ...] = DEFAULT_GROWTH_MODES,
) -> tuple[str, list[int] | None, dict[int, int] | None]:
    if not growth_modes or len(set(growth_modes)) != len(growth_modes):
        raise ValueError("growth modes must be nonempty and distinct")
    if any(mode not in SUPPORT for mode in growth_modes):
        raise ValueError(f"growth modes must belong to {SUPPORT}")
    n = sum(counts) + 1
    dummy = n
    model = cp_model.CpModel()
    arcs: dict[tuple[int, int], cp_model.IntVar] = {}
    edges: dict[tuple[int, int], cp_model.IntVar] = {}
    circuit = []

    for i in range(n):
        for j in range(i + 1, n):
            if cyclic_length(i, j, n) in SUPPORT:
                forward = model.new_bool_var(f"a_{i}_{j}")
                backward = model.new_bool_var(f"a_{j}_{i}")
                used = model.new_bool_var(f"e_{i}_{j}")
                arcs[i, j] = forward
                arcs[j, i] = backward
                edges[i, j] = used
                model.add(used == forward + backward)
                circuit.extend(((i, j, forward), (j, i, backward)))
        to_dummy = model.new_bool_var(f"a_{i}_D")
        from_dummy = model.new_bool_var(f"a_D_{i}")
        arcs[i, dummy] = to_dummy
        arcs[dummy, i] = from_dummy
        circuit.extend(((i, dummy, to_dummy), (dummy, i, from_dummy)))

    model.add_circuit(circuit)
    for length, target in zip(SUPPORT, counts):
        model.add(
            sum(
                edge
                for (i, j), edge in edges.items()
                if cyclic_length(i, j, n) == length
            )
            == target
        )

    growth_choices: dict[tuple[int, int], cp_model.IntVar] = {}
    for x in growth_modes:
        choices = []
        for m in range(x - 1, n - x):
            choice = model.new_bool_var(f"grow_{x}_{m}")
            growth_choices[x, m] = choice
            choices.append(choice)
            critical = set(range(m - x + 1, m + 1))
            changed = [
                (i, j, edge)
                for (i, j), edge in edges.items()
                if changed_by_embedding(i, j, x, m, n)
            ]
            for y in critical:
                model.add(
                    sum(edge for i, j, edge in changed if y in (i, j)) == 1
                ).only_enforce_if(choice)
            for i, j, edge in changed:
                if i not in critical and j not in critical:
                    model.add(edge == 0).only_enforce_if(choice)
        model.add_exactly_one(choices)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 1
    status = solver.solve(model)
    status_name = solver.status_name(status)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return status_name, None, None

    successor: dict[int, int] = {}
    for (i, j), arc in arcs.items():
        if solver.value(arc):
            successor[i] = j
    path = []
    at = successor[dummy]
    while at != dummy:
        path.append(at)
        at = successor[at]
    selected = {
        x: next(
            m
            for (xx, m), choice in growth_choices.items()
            if xx == x and solver.value(choice)
        )
        for x in growth_modes
    }
    verify_realization(path, counts)
    for x, m in selected.items():
        verify_growth(path, x, m)
    return status_name, path, selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument(
        "--counts",
        nargs=3,
        type=int,
        metavar=("A", "B", "C"),
        default=DEFAULT_COUNTS,
    )
    parser.add_argument(
        "--modes",
        nargs="+",
        type=int,
        choices=SUPPORT,
        default=DEFAULT_GROWTH_MODES,
        help="distinct growth modes required of the returned seed",
    )
    args = parser.parse_args()
    counts = tuple(args.counts)
    growth_modes = tuple(args.modes)
    status, path, selected = solve(counts, args.seconds, growth_modes)
    print(
        json.dumps(
            {
                "status": status,
                "counts": list(counts),
                "required_growth_modes": list(growth_modes),
                "selected_growth_cuts": selected,
                "path": path,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
