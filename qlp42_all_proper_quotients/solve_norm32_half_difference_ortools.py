#!/usr/bin/env python3
"""Exact CP-SAT model for the length-21 half-difference projection.

For a length-42 fourth-root sequence X, use the CRT coordinates

    x_j = X_(22*j mod 42), y_j = X_(22*j+21 mod 42), R_j = x_j-y_j.

The half-difference identity reduces the norm-32 residual target to a pair of
length-21 sequences R_A,R_B over a nine-point Gaussian alphabet.  This model
tests each of the six canonical order-two compression cases.
"""

from __future__ import annotations

from argparse import ArgumentParser

from ortools.sat.python import cp_model

HALF = 21
ALPHABET = (
    (0, 0),
    (2, 0),
    (-2, 0),
    (0, 2),
    (0, -2),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
)
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)

# A deterministic full-sequence heuristic came within squared real residual
# 32 of the shell.  Multiplying its A sequence by -1 and shifting both words
# left once puts its order-two compression nearest to canonical case 3.  Its
# exact half-differences are useful CP-SAT hints only; they satisfy neither the
# target sums nor all target correlations and are not evidence of feasibility.
NEAR_A = "j1j-ij--ij1-1i1jji1j1--1--iii111jiiiij-jj-"
NEAR_B = "1j--iij1-iiiji-1i1jj11-i11-j-jji11-1ji--1-"
ROOT = {"1": (1, 0), "i": (0, 1), "-": (-1, 0), "j": (0, -1)}


def near_case_three_hint() -> dict[str, list[tuple[int, int]]]:
    a = [(-ROOT[symbol][0], -ROOT[symbol][1]) for symbol in NEAR_A]
    b = [ROOT[symbol] for symbol in NEAR_B]
    a = a[1:] + a[:1]
    b = b[1:] + b[:1]
    return {
        name: [
            (
                sequence[22 * j % 42][0] - sequence[(22 * j + 21) % 42][0],
                sequence[22 * j % 42][1] - sequence[(22 * j + 21) % 42][1],
            )
            for j in range(HALF)
        ]
        for name, sequence in (("a", a), ("b", b))
    }

# Combined target c_s=PAF(A,s)+PAF(B,s) for the canonical norm-32 residual.
COMBINED = [-2] * 42
COMBINED[0] = 84
for shift in (4, 11, 31, 38):
    COMBINED[shift] = -4
for shift in (10, 17, 25, 32):
    COMBINED[shift] = 0

# C_s = PAF(R_A,s)+PAF(R_B,s)
#     = (-1)^s (c_s-c_(s+21)), including s=0 without a sign change.
TARGET = [
    ((-1) ** shift) * (COMBINED[shift] - COMBINED[shift + HALF])
    for shift in range(HALF)
]
assert TARGET[0] == 86
assert {index: value for index, value in enumerate(TARGET) if index and value} == {
    4: -4,
    10: 4,
    11: 4,
    17: -4,
}


def gaussian_paf(sequence: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [
        (
            sum(
                sequence[index][0] * sequence[(index + shift) % HALF][0]
                + sequence[index][1] * sequence[(index + shift) % HALF][1]
                for index in range(HALF)
            ),
            sum(
                sequence[index][1] * sequence[(index + shift) % HALF][0]
                - sequence[index][0] * sequence[(index + shift) % HALF][1]
                for index in range(HALF)
            ),
        )
        for shift in range(HALF)
    ]


def solve_case(case: int, seconds: float, workers: int, log: bool) -> bool:
    p, q, x, y = REPRESENTATIVES[case]
    model = cp_model.CpModel()
    real = {
        name: [model.new_int_var(-2, 2, f"{name}_r_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }
    imag = {
        name: [model.new_int_var(-2, 2, f"{name}_i_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }
    for name in ("a", "b"):
        for j in range(HALF):
            model.add_allowed_assignments([real[name][j], imag[name][j]], ALPHABET)

    model.add(sum(real["a"]) == 2 * p)
    model.add(sum(imag["a"]) == 2 * q)
    model.add(sum(real["b"]) == 2 * x - 1)
    model.add(sum(imag["b"]) == 2 * y - 1)

    if case == 3:
        for name, sequence in near_case_three_hint().items():
            for j, (real_value, imaginary_value) in enumerate(sequence):
                model.add_hint(real[name][j], real_value)
                model.add_hint(imag[name][j], imaginary_value)

    for shift in range(HALF // 2 + 1):
        real_terms = []
        imaginary_terms = []
        for name in ("a", "b"):
            for j in range(HALF):
                k = (j + shift) % HALF
                rr = model.new_int_var(-4, 4, f"rr_{shift}_{name}_{j}")
                ii = model.new_int_var(-4, 4, f"ii_{shift}_{name}_{j}")
                ir = model.new_int_var(-4, 4, f"ir_{shift}_{name}_{j}")
                ri = model.new_int_var(-4, 4, f"ri_{shift}_{name}_{j}")
                model.add_multiplication_equality(rr, [real[name][j], real[name][k]])
                model.add_multiplication_equality(ii, [imag[name][j], imag[name][k]])
                model.add_multiplication_equality(ir, [imag[name][j], real[name][k]])
                model.add_multiplication_equality(ri, [real[name][j], imag[name][k]])
                real_terms.extend((rr, ii))
                imaginary_terms.extend((ir, -ri))
        model.add(sum(real_terms) == TARGET[shift])
        model.add(sum(imaginary_terms) == 0)

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

    decoded = {}
    for name in ("a", "b"):
        decoded[name] = [
            (solver.value(real[name][j]), solver.value(imag[name][j]))
            for j in range(HALF)
        ]
        print(f"R_{name.upper()}={decoded[name]}")

    paf_a = gaussian_paf(decoded["a"])
    paf_b = gaussian_paf(decoded["b"])
    assert all(
        paf_a[shift][0] + paf_b[shift][0] == TARGET[shift]
        and paf_a[shift][1] + paf_b[shift][1] == 0
        for shift in range(HALF)
    )
    assert sum(z[0] for z in decoded["a"]) == 2 * p
    assert sum(z[1] for z in decoded["a"]) == 2 * q
    assert sum(z[0] for z in decoded["b"]) == 2 * x - 1
    assert sum(z[1] for z in decoded["b"]) == 2 * y - 1
    print(f"case={case}; exact_verification=passed")
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
    for case in cases:
        satisfiable += solve_case(case, args.seconds, args.workers, args.log)
    print(f"satisfiable_cases={satisfiable}; tested_cases={len(tuple(cases))}")


if __name__ == "__main__":
    main()
