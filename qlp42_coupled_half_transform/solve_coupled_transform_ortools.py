#!/usr/bin/env python3
"""Exact CP-SAT model for the coupled norm-32 QLP-42 transform.

Each length-21 coordinate is one of the 16 exact (S,H) states arising from an
ordered pair of fourth roots.  A single 256-row transition table channels a
pair of states to its simultaneous S- and H-autocorrelation contributions.
Thus every satisfying assignment reconstructs two length-42 fourth-root words
realizing the canonical norm-32 residual shell.
"""

from __future__ import annotations

from argparse import ArgumentParser

from ortools.sat.python import cp_model

HALF = 21
ROOTS = ((1, 0), (0, 1), (-1, 0), (0, -1))
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
TARGET_S = [0] * HALF
TARGET_S[0] = 43
TARGET_S[4] = TARGET_S[17] = -2
TARGET_S[10] = TARGET_S[11] = 2
TARGET_H = [41] + [-2] * (HALF - 1)


def div_one_plus_i(real: int, imaginary: int) -> tuple[int, int]:
    assert (real + imaginary) % 2 == 0
    assert (imaginary - real) % 2 == 0
    return (real + imaginary) // 2, (imaginary - real) // 2


def multiply_conjugate(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return (
        left[0] * right[0] + left[1] * right[1],
        left[1] * right[0] - left[0] * right[1],
    )


# State rows are (index, S_real, S_imag, H_real, H_imag, x_index, y_index).
STATE_ROWS = []
for x_index, x in enumerate(ROOTS):
    for y_index, y in enumerate(ROOTS):
        s = div_one_plus_i(x[0] - y[0], x[1] - y[1])
        h = div_one_plus_i(x[0] + y[0], x[1] + y[1])
        STATE_ROWS.append((len(STATE_ROWS), *s, *h, x_index, y_index))
assert len(STATE_ROWS) == 16

# Transition rows are (left_state, right_state, S_real, S_imag,
# H_real, H_imag).  They encode both correlations in one table.
TRANSITION_ROWS = []
for left in STATE_ROWS:
    for right in STATE_ROWS:
        product_s = multiply_conjugate((left[1], left[2]), (right[1], right[2]))
        product_h = multiply_conjugate((left[3], left[4]), (right[3], right[4]))
        TRANSITION_ROWS.append((left[0], right[0], *product_s, *product_h))


def gaussian_paf(sequence: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [
        tuple(
            sum(value[coordinate] for value in products)
            for coordinate in (0, 1)
        )
        for shift in range(len(sequence))
        for products in (
            [
                multiply_conjugate(sequence[j], sequence[(j + shift) % len(sequence)])
                for j in range(len(sequence))
            ],
        )
    ]


def add_lexicographic_leq(
    model: cp_model.CpModel,
    left: list[cp_model.IntVar],
    right: list[cp_model.IntVar],
    label: str,
) -> None:
    prefix_equal = model.new_bool_var(f"{label}_prefix_0")
    model.add(prefix_equal == 1)
    for index, (left_value, right_value) in enumerate(zip(left, right)):
        model.add(left_value <= right_value).only_enforce_if(prefix_equal)
        equal_here = model.new_bool_var(f"{label}_equal_{index}")
        model.add(left_value == right_value).only_enforce_if(equal_here)
        model.add(left_value != right_value).only_enforce_if(equal_here.negated())
        next_prefix = model.new_bool_var(f"{label}_prefix_{index + 1}")
        model.add_implication(next_prefix, prefix_equal)
        model.add_implication(next_prefix, equal_here)
        model.add_bool_or(
            (prefix_equal.negated(), equal_here.negated(), next_prefix)
        )
        prefix_equal = next_prefix


def solve_case(case: int, seconds: float, workers: int, log: bool) -> bool:
    p, q, x, y = REPRESENTATIVES[case]
    required_sums = {
        "a": ((p + q, q - p), (0, 0)),
        "b": ((x + y - 1, y - x), (1, 0)),
    }
    model = cp_model.CpModel()
    state = {
        name: [model.new_int_var(0, 15, f"{name}_state_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }
    s_real = {
        name: [model.new_int_var(-1, 1, f"{name}_sr_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }
    s_imag = {
        name: [model.new_int_var(-1, 1, f"{name}_si_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }
    h_real = {
        name: [model.new_int_var(-1, 1, f"{name}_hr_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }
    h_imag = {
        name: [model.new_int_var(-1, 1, f"{name}_hi_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }

    s_energy = []
    quarter_turn = []
    local_rows = [row[:5] for row in STATE_ROWS]
    for name in ("a", "b"):
        for j in range(HALF):
            model.add_allowed_assignments(
                [
                    state[name][j],
                    s_real[name][j],
                    s_imag[name][j],
                    h_real[name][j],
                    h_imag[name][j],
                ],
                local_rows,
            )
            energy = model.new_int_var(0, 2, f"{name}_s_energy_{j}")
            is_quarter = model.new_bool_var(f"{name}_quarter_{j}")
            model.add_allowed_assignments(
                [state[name][j], energy, is_quarter],
                tuple(
                    (
                        row[0],
                        row[1] * row[1] + row[2] * row[2],
                        int(row[1] * row[1] + row[2] * row[2] == 1),
                    )
                    for row in STATE_ROWS
                ),
            )
            s_energy.append(energy)
            quarter_turn.append(is_quarter)

        model.add(sum(s_real[name]) == required_sums[name][0][0])
        model.add(sum(s_imag[name]) == required_sums[name][0][1])
        model.add(sum(h_real[name]) == required_sums[name][1][0])
        model.add(sum(h_imag[name]) == required_sums[name][1][1])
        for rotation in range(1, HALF):
            add_lexicographic_leq(
                model,
                state[name],
                state[name][rotation:] + state[name][:rotation],
                f"{name}_rotation_{rotation}",
            )

    model.add(sum(s_energy) == TARGET_S[0])
    quarter_count = model.new_int_var(0, 42, "quarter_count")
    model.add(quarter_count == sum(quarter_turn))
    model.add_allowed_assignments(
        [quarter_count], tuple((value,) for value in range(1, 42, 4))
    )

    for shift in range(1, HALF // 2 + 1):
        s_real_terms = []
        s_imag_terms = []
        h_real_terms = []
        h_imag_terms = []
        for name in ("a", "b"):
            for j in range(HALF):
                k = (j + shift) % HALF
                sr = model.new_int_var(-2, 2, f"corr_sr_{shift}_{name}_{j}")
                si = model.new_int_var(-2, 2, f"corr_si_{shift}_{name}_{j}")
                hr = model.new_int_var(-2, 2, f"corr_hr_{shift}_{name}_{j}")
                hi = model.new_int_var(-2, 2, f"corr_hi_{shift}_{name}_{j}")
                model.add_allowed_assignments(
                    [state[name][j], state[name][k], sr, si, hr, hi],
                    TRANSITION_ROWS,
                )
                s_real_terms.append(sr)
                s_imag_terms.append(si)
                h_real_terms.append(hr)
                h_imag_terms.append(hi)
        model.add(sum(s_real_terms) == TARGET_S[shift])
        model.add(sum(s_imag_terms) == 0)
        model.add(sum(h_real_terms) == TARGET_H[shift])
        model.add(sum(h_imag_terms) == 0)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.log_search_progress = log
    status = solver.solve(model)
    print(
        f"case={case}; representative={REPRESENTATIVES[case]}; "
        f"status={solver.status_name(status)}; wall_time={solver.wall_time:.6f}; "
        f"conflicts={solver.num_conflicts}; branches={solver.num_branches}",
        flush=True,
    )
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return False

    decoded_s: dict[str, list[tuple[int, int]]] = {}
    decoded_h: dict[str, list[tuple[int, int]]] = {}
    original: dict[str, list[tuple[int, int]]] = {}
    for name in ("a", "b"):
        state_values = [solver.value(value) for value in state[name]]
        decoded_s[name] = [(STATE_ROWS[value][1], STATE_ROWS[value][2]) for value in state_values]
        decoded_h[name] = [(STATE_ROWS[value][3], STATE_ROWS[value][4]) for value in state_values]
        sequence = [(0, 0)] * 42
        for j, value in enumerate(state_values):
            x_root = ROOTS[STATE_ROWS[value][5]]
            y_root = ROOTS[STATE_ROWS[value][6]]
            sequence[22 * j % 42] = x_root
            sequence[(22 * j + 21) % 42] = y_root
        original[name] = sequence
        print(f"states_{name.upper()}={state_values}")

    paf_s_a = gaussian_paf(decoded_s["a"])
    paf_s_b = gaussian_paf(decoded_s["b"])
    paf_h_a = gaussian_paf(decoded_h["a"])
    paf_h_b = gaussian_paf(decoded_h["b"])
    assert all(
        paf_s_a[shift][0] + paf_s_b[shift][0] == TARGET_S[shift]
        and paf_s_a[shift][1] + paf_s_b[shift][1] == 0
        and paf_h_a[shift][0] + paf_h_b[shift][0] == TARGET_H[shift]
        and paf_h_a[shift][1] + paf_h_b[shift][1] == 0
        for shift in range(HALF)
    )
    combined = []
    paf_a = gaussian_paf(original["a"])
    paf_b = gaussian_paf(original["b"])
    for shift in range(42):
        combined.append(
            (
                paf_a[shift][0] + paf_b[shift][0],
                paf_a[shift][1] + paf_b[shift][1],
            )
        )
    assert combined[0] == (84, 0)
    assert all(value[1] == 0 for value in combined)
    assert {shift: value[0] for shift, value in enumerate(combined) if shift and value[0] != -2} == {
        4: -4,
        10: 0,
        11: -4,
        17: 0,
        25: 0,
        31: -4,
        32: 0,
        38: -4,
    }
    print(f"case={case}; exact_norm32_shell_witness=verified")
    return True


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--case", type=int, choices=range(6))
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()
    cases = range(6) if args.case is None else (args.case,)
    satisfiable = 0
    tested = 0
    for case in cases:
        satisfiable += solve_case(case, args.seconds, args.workers, args.log)
        tested += 1
    print(f"satisfiable_cases={satisfiable}; tested_cases={tested}")


if __name__ == "__main__":
    main()
