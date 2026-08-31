#!/usr/bin/env python3
"""Scaled exact CP-SAT model for the QLP-42 half-difference projection.

Every half-difference R=x-y is divisible by 1+i.  After writing R=(1+i)S,
the nine-point alphabet becomes the full ternary Gaussian grid

    S_j in {-1,0,1} + i*{-1,0,1}.

The combined norm is 43, so exactly 43 of the 84 scalar ternary coordinates
are nonzero.  This model uses that exact sparsity, removes the shift-zero
multiplication constraints, and fixes the independent cyclic rotations of
S_A and S_B by placing a least alphabet value at coordinate zero.
"""

from __future__ import annotations

from argparse import ArgumentParser

from ortools.sat.python import cp_model

HALF = 21
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)

# The representative shortest-shell combined autocorrelation, divided by the
# norm |1+i|^2=2 after the half-difference scaling.
TARGET = [0] * HALF
TARGET[0] = 43
TARGET[4] = TARGET[17] = -2
TARGET[10] = TARGET[11] = 2
TERNARY_PRODUCT = tuple(
    (left, right, left * right)
    for left in (-1, 0, 1)
    for right in (-1, 0, 1)
)

NEAR_A = "j1j-ij--ij1-1i1jji1j1--1--iii111jiiiij-jj-"
NEAR_B = "1j--iij1-iiiji-1i1jj11-i11-j-jji11-1ji--1-"
ROOT = {"1": (1, 0), "i": (0, 1), "-": (-1, 0), "j": (0, -1)}


def near_case_three_hint() -> dict[str, list[tuple[int, int]]]:
    a = [(-ROOT[symbol][0], -ROOT[symbol][1]) for symbol in NEAR_A]
    b = [ROOT[symbol] for symbol in NEAR_B]
    a = a[1:] + a[:1]
    b = b[1:] + b[:1]
    result: dict[str, list[tuple[int, int]]] = {}
    for name, sequence in (("a", a), ("b", b)):
        scaled = []
        for j in range(HALF):
            even = sequence[22 * j % 42]
            odd = sequence[(22 * j + 21) % 42]
            real = even[0] - odd[0]
            imaginary = even[1] - odd[1]
            assert (real + imaginary) % 2 == 0
            assert (imaginary - real) % 2 == 0
            scaled.append(
                ((real + imaginary) // 2, (imaginary - real) // 2)
            )
        result[name] = scaled
    return result


def gaussian_paf(sequence: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [
        (
            sum(
                sequence[j][0] * sequence[(j + shift) % HALF][0]
                + sequence[j][1] * sequence[(j + shift) % HALF][1]
                for j in range(HALF)
            ),
            sum(
                sequence[j][1] * sequence[(j + shift) % HALF][0]
                - sequence[j][0] * sequence[(j + shift) % HALF][1]
                for j in range(HALF)
            ),
        )
        for shift in range(HALF)
    ]


def add_lexicographic_leq(
    model: cp_model.CpModel,
    left: list[cp_model.IntVar],
    right: list[cp_model.IntVar],
    label: str,
) -> None:
    """Add left <=lex right using reified prefix equalities."""
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


def solve_case(
    case: int,
    seconds: float,
    workers: int,
    log: bool,
    quarter_turns: int | None,
) -> bool:
    p, q, x, y = REPRESENTATIVES[case]
    required_sum = {
        "a": (p + q, q - p),
        "b": (x + y - 1, y - x),
    }
    model = cp_model.CpModel()
    real = {
        name: [model.new_int_var(-1, 1, f"{name}_r_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }
    imag = {
        name: [model.new_int_var(-1, 1, f"{name}_i_{j}") for j in range(HALF)]
        for name in ("a", "b")
    }

    scalar_support = []
    unit_cell = {"a": [], "b": []}
    for name in ("a", "b"):
        model.add(sum(real[name]) == required_sum[name][0])
        model.add(sum(imag[name]) == required_sum[name][1])

        codes = []
        for j in range(HALF):
            code = model.new_int_var(0, 8, f"{name}_code_{j}")
            model.add(code == 3 * (real[name][j] + 1) + imag[name][j] + 1)
            codes.append(code)
            coordinate_support = []
            for coordinate, label in (
                (real[name][j], "r"),
                (imag[name][j], "i"),
            ):
                support = model.new_bool_var(f"{name}_{label}_nz_{j}")
                model.add_allowed_assignments(
                    [coordinate, support], ((-1, 1), (0, 0), (1, 1))
                )
                scalar_support.append(support)
                coordinate_support.append(support)
            unit = model.new_bool_var(f"{name}_unit_{j}")
            model.add_allowed_assignments(
                [coordinate_support[0], coordinate_support[1], unit],
                ((0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 0)),
            )
            unit_cell[name].append(unit)

        # PAF and the Gaussian sum are independently invariant under a cyclic
        # rotation of either sequence.  Keep the lexicographically least
        # rotation; this removes a factor of up to 21 for each sequence.
        for rotation in range(1, HALF):
            add_lexicographic_leq(
                model,
                codes,
                codes[rotation:] + codes[:rotation],
                f"{name}_rotation_{rotation}",
            )

    model.add(sum(scalar_support) == TARGET[0])

    # Reducing the Gaussian norm equation modulo 1+i leaves two binary
    # cyclic autocorrelations whose sum is the delta sequence.  Pairing the
    # ten nonzero shifts s and 21-s shows that the total number q of unit
    # cells satisfies q == 1 (mod 4).  The fixed Gaussian sums also force the
    # A and B unit counts to be even and odd respectively.
    q_a = model.new_int_var(0, HALF, "quarter_turns_a")
    q_b = model.new_int_var(0, HALF, "quarter_turns_b")
    model.add(q_a == sum(unit_cell["a"]))
    model.add(q_b == sum(unit_cell["b"]))
    model.add_allowed_assignments([q_a], tuple((value,) for value in range(0, 22, 2)))
    model.add_allowed_assignments([q_b], tuple((value,) for value in range(1, 22, 2)))
    model.add_allowed_assignments(
        [q_a, q_b],
        tuple(
            (left, right)
            for left in range(0, 22, 2)
            for right in range(1, 22, 2)
            if (left + right) % 4 == 1
        ),
    )
    if quarter_turns is not None:
        model.add(q_a + q_b == quarter_turns)

    if case == 3:
        for name, sequence in near_case_three_hint().items():
            for j, (real_value, imaginary_value) in enumerate(sequence):
                model.add_hint(real[name][j], real_value)
                model.add_hint(imag[name][j], imaginary_value)

    # Hermitian symmetry makes shifts 11,...,20 redundant once 1,...,10 are
    # imposed.  The shift-zero equation is the support equality above.
    for shift in range(1, HALF // 2 + 1):
        real_terms = []
        imaginary_terms = []
        for name in ("a", "b"):
            for j in range(HALF):
                k = (j + shift) % HALF
                rr = model.new_int_var(-1, 1, f"rr_{shift}_{name}_{j}")
                ii = model.new_int_var(-1, 1, f"ii_{shift}_{name}_{j}")
                ir = model.new_int_var(-1, 1, f"ir_{shift}_{name}_{j}")
                ri = model.new_int_var(-1, 1, f"ri_{shift}_{name}_{j}")
                model.add_allowed_assignments(
                    [real[name][j], real[name][k], rr], TERNARY_PRODUCT
                )
                model.add_allowed_assignments(
                    [imag[name][j], imag[name][k], ii], TERNARY_PRODUCT
                )
                model.add_allowed_assignments(
                    [imag[name][j], real[name][k], ir], TERNARY_PRODUCT
                )
                model.add_allowed_assignments(
                    [real[name][j], imag[name][k], ri], TERNARY_PRODUCT
                )
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
        f"quarter_turns={quarter_turns}; "
        f"status={solver.status_name(status)}; wall_time={solver.wall_time:.6f}; "
        f"conflicts={solver.num_conflicts}; branches={solver.num_branches}",
        flush=True,
    )
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return False

    decoded: dict[str, list[tuple[int, int]]] = {}
    for name in ("a", "b"):
        decoded[name] = [
            (solver.value(real[name][j]), solver.value(imag[name][j]))
            for j in range(HALF)
        ]
        print(f"S_{name.upper()}={decoded[name]}")

    paf_a = gaussian_paf(decoded["a"])
    paf_b = gaussian_paf(decoded["b"])
    assert all(
        paf_a[shift][0] + paf_b[shift][0] == TARGET[shift]
        and paf_a[shift][1] + paf_b[shift][1] == 0
        for shift in range(HALF)
    )
    assert all(
        sum(value[coordinate] for value in decoded[name])
        == required_sum[name][coordinate]
        for name in ("a", "b")
        for coordinate in (0, 1)
    )
    assert sum(
        int(coordinate != 0)
        for name in ("a", "b")
        for value in decoded[name]
        for coordinate in value
    ) == 43
    print(f"case={case}; exact_verification=passed")
    return True


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--case", type=int, choices=range(6))
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--quarter-turns", type=int, choices=range(1, 42, 4))
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()
    cases = range(6) if args.case is None else (args.case,)
    satisfiable = 0
    tested = 0
    for case in cases:
        satisfiable += solve_case(
            case, args.seconds, args.workers, args.log, args.quarter_turns
        )
        tested += 1
    print(f"satisfiable_cases={satisfiable}; tested_cases={tested}")


if __name__ == "__main__":
    main()
