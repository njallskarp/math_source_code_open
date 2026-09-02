#!/usr/bin/env python3
"""Find full local-state witnesses for the QLP-42 q=5/q=37 pi^3 layer."""

from __future__ import annotations

import argparse
from csv import DictReader, DictWriter
from itertools import product
from pathlib import Path

from ortools.sat.python import cp_model

G = tuple[int, int]
N = 21
FULL = (1 << N) - 1
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def multiply(left: G, right: G) -> G:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: G) -> G:
    return value[0], -value[1]


def div_pi(value: G) -> G:
    real, imag = value
    assert (real + imag) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def local_states() -> tuple[dict[str, object], ...]:
    states = []
    for x, y in product(ROOTS, repeat=2):
        s = div_pi(subtract(x, y))
        h = div_pi(add(x, y))
        dot = x[0] * y[0] + x[1] * y[1]
        kind = "equal" if dot == 1 else "opposite" if dot == -1 else "quarter"
        states.append({"x": x, "y": y, "s": s, "h": h, "kind": kind})
    assert len(states) == len({(state["s"], state["h"]) for state in states}) == 16
    return tuple(states)


STATES = local_states()
QUARTER = tuple(index for index, state in enumerate(STATES) if state["kind"] == "quarter")
NONQUARTER = tuple(index for index, state in enumerate(STATES) if state["kind"] != "quarter")
OPPOSITE = tuple(int(state["kind"] == "opposite") for state in STATES)


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def canonical(mask: int) -> int:
    return min(rotate(mask, shift) for shift in range(N))


def read_supports() -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    path = Path(__file__).parent.parent / "qlp42_q5_q37_binary_frontier" / "frontier_orbits.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    q5 = sorted(
        (int(row["a_mask_hex"], 16), int(row["b_mask_hex"], 16))
        for row in rows
        if int(row["q_a"]) % 2 == 0
    )
    q37 = sorted(
        {
            (
                canonical(FULL ^ int(row["a_mask_hex"], 16)),
                canonical(FULL ^ int(row["b_mask_hex"], 16)),
            )
            for row in rows
            if int(row["q_a"]) % 2 == 1
        }
    )
    assert len(q5) == len(q37) == 18
    return q5, q37


def state_coordinate(component: str, coordinate: int) -> list[int]:
    return [state[component][coordinate] for state in STATES]  # type: ignore[index]


PRODUCT_RESIDUES: dict[str, tuple[list[int], list[int]]] = {}
for component in ("s", "h"):
    plus_values = []
    minus_values = []
    for left, right in product(range(16), repeat=2):
        value = multiply(STATES[left][component], conjugate(STATES[right][component]))  # type: ignore[arg-type]
        plus_values.append((value[0] + value[1]) % 4)
        minus_values.append((value[1] - value[0]) % 4)
    PRODUCT_RESIDUES[component] = plus_values, minus_values


def target(component: str, shift: int) -> G:
    if component == "h":
        return -2, 0
    if shift == 4:
        return -2, 0
    if shift == 10:
        return 2, 0
    return 0, 0


def build_model(
    q_value: int, support: tuple[int, int], case: tuple[int, int, int, int]
) -> tuple[cp_model.CpModel, list[list[cp_model.IntVar]]]:
    model = cp_model.CpModel()
    state_vars: list[list[cp_model.IntVar]] = []
    opposite_vars = []
    for family, support_mask in enumerate(support):
        family_vars = []
        for position in range(N):
            allowed = QUARTER if (support_mask >> position) & 1 else NONQUARTER
            state = model.new_int_var_from_domain(
                cp_model.Domain.from_values(allowed), f"z_{family}_{position}"
            )
            opposite = model.new_bool_var(f"o_{family}_{position}")
            model.add_allowed_assignments(
                [state, opposite], [(index, OPPOSITE[index]) for index in allowed]
            )
            family_vars.append(state)
            opposite_vars.append(opposite)
        state_vars.append(family_vars)
    model.add(sum(opposite_vars) == (19 if q_value == 5 else 3))

    p, q, x, y = case
    sum_targets = (
        ((p + q, q - p), (0, 0)),
        ((x + y - 1, y - x), (1, 0)),
    )
    for family in range(2):
        for component_index, component in enumerate(("s", "h")):
            for coordinate in range(2):
                values = []
                lookup = state_coordinate(component, coordinate)
                for position, state in enumerate(state_vars[family]):
                    value = model.new_int_var(-1, 1, f"sum_{family}_{component}_{coordinate}_{position}")
                    model.add_element(state, lookup, value)
                    values.append(value)
                model.add(sum(values) == sum_targets[family][component_index][coordinate])

    for component in ("s", "h"):
        for shift in range(1, 11):
            plus_terms = []
            minus_terms = []
            plus_lookup, minus_lookup = PRODUCT_RESIDUES[component]
            for family in range(2):
                for position in range(N):
                    pair_index = model.new_int_var(
                        0, 255, f"pair_{component}_{shift}_{family}_{position}"
                    )
                    model.add(
                        pair_index
                        == 16 * state_vars[family][position]
                        + state_vars[family][(position + shift) % N]
                    )
                    plus = model.new_int_var(0, 3, f"p_{component}_{shift}_{family}_{position}_plus")
                    minus = model.new_int_var(0, 3, f"p_{component}_{shift}_{family}_{position}_minus")
                    model.add_element(pair_index, plus_lookup, plus)
                    model.add_element(pair_index, minus_lookup, minus)
                    plus_terms.append(plus)
                    minus_terms.append(minus)
            wanted = target(component, shift)
            plus_sum = model.new_int_var(-200, 200, f"r_{component}_{shift}_plus")
            minus_sum = model.new_int_var(-200, 200, f"r_{component}_{shift}_minus")
            model.add(plus_sum == sum(plus_terms) - wanted[0] - wanted[1])
            model.add(minus_sum == sum(minus_terms) - wanted[1] + wanted[0])
            model.add_modulo_equality(0, plus_sum, 4)
            model.add_modulo_equality(0, minus_sum, 4)
    return model, state_vars


def encode(states: list[int]) -> str:
    return "".join(format(state, "x") for state in states)


def solve_one(
    q_value: int,
    orbit: int,
    support: tuple[int, int],
    case_id: int,
    workers: int,
    time_limit: float,
) -> dict[str, int | str]:
    model, state_vars = build_model(q_value, support, CASES[case_id])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 100000 * q_value + 100 * orbit + case_id
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.solve(model)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        raise RuntimeError(
            f"no witness found: q={q_value} orbit={orbit} case={case_id} "
            f"status={solver.status_name(status)} wall={solver.wall_time:.3f}"
        )
    words = [[solver.value(variable) for variable in family] for family in state_vars]
    return {
        "q": q_value,
        "orbit": orbit,
        "case": case_id,
        "a_mask_hex": f"{support[0]:06x}",
        "b_mask_hex": f"{support[1]:06x}",
        "states_a": encode(words[0]),
        "states_b": encode(words[1]),
        "solver_wall_seconds": f"{solver.wall_time:.6f}",
        "solver_branches": solver.num_branches,
        "solver_conflicts": solver.num_conflicts,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--q", type=int, choices=(5, 37))
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--case", type=int, choices=range(6))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    q5, q37 = read_supports()
    jobs = []
    for q_value, supports in ((5, q5), (37, q37)):
        if args.q is not None and q_value != args.q:
            continue
        for orbit, support in enumerate(supports):
            if args.orbit is not None and orbit != args.orbit:
                continue
            for case_id in range(6):
                if args.case is not None and case_id != args.case:
                    continue
                jobs.append((q_value, orbit, support, case_id))

    rows = []
    for job_id, job in enumerate(jobs, 1):
        row = solve_one(*job, args.workers, args.time_limit)
        rows.append(row)
        print(
            f"job={job_id}/{len(jobs)};q={row['q']};orbit={row['orbit']};"
            f"case={row['case']};wall={row['solver_wall_seconds']};"
            f"branches={row['solver_branches']};conflicts={row['solver_conflicts']}",
            flush=True,
        )

    if args.output is not None:
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            writer = DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
