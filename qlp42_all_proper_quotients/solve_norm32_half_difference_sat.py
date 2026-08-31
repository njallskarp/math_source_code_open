#!/usr/bin/env python3
"""Exact SAT model for the length-21 QLP-42 half-difference projection.

This is a Boolean counterpart to ``solve_norm32_half_difference_ortools.py``.
Every alphabet choice is one-hot, every Gaussian correlation product is
channelled to one of the nine integers -4,...,4, and every required sum is
enforced by a deterministic finite-state summation automaton.  Consequently
the generated CNF has no nonlinear or floating-point semantics delegated to
the solver.
"""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from threading import Timer
from time import monotonic

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

HALF = 21
ALPHABET = (
    (0, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (2, 0),
    (-2, 0),
    (0, 2),
    (0, -2),
)
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
TARGET = [0] * HALF
TARGET[0] = 86
TARGET[4] = TARGET[17] = -4
TARGET[10] = TARGET[11] = 4


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


class Model:
    def __init__(self, case: int, symmetry_breaking: bool = True) -> None:
        self.case = case
        self.pool = IDPool()
        self.cnf = CNF()
        self.choice = {
            name: [
                [self.pool.id(f"{name}_{j}_{symbol}") for symbol in range(len(ALPHABET))]
                for j in range(HALF)
            ]
            for name in ("a", "b")
        }
        for rows in self.choice.values():
            for row in rows:
                self.add_exactly_one(row)

        # Binary shadows modulo (1+i): unit[name][j] is true exactly for the
        # four quarter-turn half-differences (the diagonal alphabet symbols).
        self.unit = {
            name: [self.pool.id(f"unit_{name}_{j}") for j in range(HALF)]
            for name in ("a", "b")
        }
        for name, rows in self.choice.items():
            for j, row in enumerate(rows):
                unit = self.unit[name][j]
                for literal in row[1:5]:
                    self.cnf.append([-literal, unit])
                self.cnf.append([-unit, *row[1:5]])

        # Independent cyclic rotation of either word preserves its sum and
        # PAF.  Thus each word may be rotated so that position zero contains
        # a least alphabet symbol in the fixed ordering above.
        if symmetry_breaking:
            for rows in self.choice.values():
                for row in rows[1:]:
                    for at_zero in range(len(ALPHABET)):
                        for later in range(at_zero):
                            self.cnf.append([-rows[0][at_zero], -row[later]])

        p, q, x, y = REPRESENTATIVES[case]
        for name, coordinate, target in (
            ("a", 0, 2 * p),
            ("a", 1, 2 * q),
            ("b", 0, 2 * x - 1),
            ("b", 1, 2 * y - 1),
        ):
            self.add_sum_automaton(
                self.choice[name],
                [value[coordinate] for value in ALPHABET],
                target,
                f"sum_{name}_{coordinate}",
            )

        energy_rows = self.choice["a"] + self.choice["b"]
        self.add_sum_automaton(
            energy_rows,
            [real * real + imag * imag for real, imag in ALPHABET],
            TARGET[0],
            "energy",
        )
        # The binary reduction modulo (1+i) proves that the total number of
        # quarter-turn differences is 1 modulo 4.  This is redundant with the
        # full correlation equations, but exposes a useful consequence to the
        # CDCL solver instead of asking it to rediscover the congruence.
        self.add_modulo_automaton(
            energy_rows,
            [0, 1, 1, 1, 1, 0, 0, 0, 0],
            modulus=4,
            target=1,
            label="quarter_count_mod4",
        )
        self.add_binary_shadow()

        for shift in range(1, HALF // 2 + 1):
            real_rows: list[list[int]] = []
            imaginary_rows: list[list[int]] = []
            for name in ("a", "b"):
                rows = self.choice[name]
                for j in range(HALF):
                    left = rows[j]
                    right = rows[(j + shift) % HALF]
                    real_values: list[int] = []
                    imaginary_values: list[int] = []
                    for ar, ai in ALPHABET:
                        for br, bi in ALPHABET:
                            real_values.append(ar * br + ai * bi)
                            imaginary_values.append(ai * br - ar * bi)
                    real_rows.append(
                        self.product_value_row(
                            left, right, real_values, f"corr_r_{shift}_{name}_{j}"
                        )
                    )
                    imaginary_rows.append(
                        self.product_value_row(
                            left, right, imaginary_values, f"corr_i_{shift}_{name}_{j}"
                        )
                    )
            self.add_sum_automaton(
                real_rows, list(range(-4, 5)), TARGET[shift], f"paf_r_{shift}"
            )
            self.add_sum_automaton(
                imaginary_rows, list(range(-4, 5)), 0, f"paf_i_{shift}"
            )

    def add_exactly_one(self, literals: list[int]) -> None:
        self.cnf.append(literals)
        for i, left in enumerate(literals):
            for right in literals[i + 1 :]:
                self.cnf.append([-left, -right])

    def add_and(self, left: int, right: int, label: str) -> int:
        result = self.pool.id(label)
        self.cnf.extend([[-result, left], [-result, right], [-left, -right, result]])
        return result

    def add_xor_equality(self, literals: list[int], parity: int, label: str) -> None:
        if not literals:
            if parity:
                self.cnf.append([])
            return
        current = literals[0]
        for i, literal in enumerate(literals[1:]):
            result = self.pool.id(f"{label}_xor_{i}")
            self.cnf.extend(
                [
                    [current, literal, -result],
                    [current, -literal, result],
                    [-current, literal, result],
                    [-current, -literal, -result],
                ]
            )
            current = result
        self.cnf.append([current if parity else -current])

    def add_binary_shadow(self) -> None:
        for shift in range(HALF // 2 + 1):
            products: list[int] = []
            for name in ("a", "b"):
                units = self.unit[name]
                if shift == 0:
                    products.extend(units)
                    continue
                products.extend(
                    self.add_and(
                        units[j],
                        units[(j + shift) % HALF],
                        f"binary_corr_{shift}_{name}_{j}",
                    )
                    for j in range(HALF)
                )
            self.add_xor_equality(
                products,
                parity=1 if shift == 0 else 0,
                label=f"binary_paf_{shift}",
            )

    def product_value_row(
        self,
        left: list[int],
        right: list[int],
        values: list[int],
        label: str,
    ) -> list[int]:
        outputs = [self.pool.id(f"{label}_{value}") for value in range(-4, 5)]
        self.add_exactly_one(outputs)
        width = len(ALPHABET)
        for a in range(width):
            for b in range(width):
                self.cnf.append([-left[a], -right[b], outputs[values[a * width + b] + 4]])
        return outputs

    def add_at_most_one_sequential(self, literals: list[int], label: str) -> None:
        if len(literals) < 2:
            return
        carries = [self.pool.id(f"{label}_carry_{i}") for i in range(len(literals) - 1)]
        self.cnf.append([-literals[0], carries[0]])
        for i in range(1, len(literals) - 1):
            self.cnf.extend(
                [
                    [-literals[i], carries[i]],
                    [-carries[i - 1], carries[i]],
                    [-literals[i], -carries[i - 1]],
                ]
            )
        self.cnf.append([-literals[-1], -carries[-1]])

    def add_sum_automaton(
        self,
        rows: list[list[int]],
        values: list[int],
        target: int,
        label: str,
    ) -> None:
        if any(len(row) != len(values) for row in rows):
            raise ValueError("each input row must have one literal per value")

        prefix = [{0}]
        for _ in rows:
            prefix.append({partial + value for partial in prefix[-1] for value in values})
        suffix = [{0} for _ in range(len(rows) + 1)]
        for i in range(len(rows) - 1, -1, -1):
            suffix[i] = {value + rest for value in values for rest in suffix[i + 1]}
        states = [
            sorted(partial for partial in prefix[i] if target - partial in suffix[i])
            for i in range(len(rows) + 1)
        ]
        if not states[0] or not states[-1]:
            self.cnf.append([])
            return

        variables = [
            {state: self.pool.id(f"{label}_state_{i}_{state}") for state in layer}
            for i, layer in enumerate(states)
        ]
        for i, layer in enumerate(states):
            literals = [variables[i][state] for state in layer]
            self.cnf.append(literals)
            self.add_at_most_one_sequential(literals, f"{label}_layer_{i}")
        self.cnf.append([variables[0][0]])
        self.cnf.append([variables[-1][target]])

        for i, row in enumerate(rows):
            for state in states[i]:
                state_literal = variables[i][state]
                for input_literal, value in zip(row, values, strict=True):
                    next_literal = variables[i + 1].get(state + value)
                    if next_literal is None:
                        self.cnf.append([-state_literal, -input_literal])
                    else:
                        self.cnf.append([-state_literal, -input_literal, next_literal])

    def add_modulo_automaton(
        self,
        rows: list[list[int]],
        values: list[int],
        modulus: int,
        target: int,
        label: str,
    ) -> None:
        states = [
            [self.pool.id(f"{label}_state_{i}_{residue}") for residue in range(modulus)]
            for i in range(len(rows) + 1)
        ]
        for i, layer in enumerate(states):
            self.add_exactly_one(layer)
            if i == 0:
                self.cnf.append([layer[0]])
        self.cnf.append([states[-1][target % modulus]])
        for i, row in enumerate(rows):
            for residue, state_literal in enumerate(states[i]):
                for input_literal, value in zip(row, values, strict=True):
                    self.cnf.append(
                        [
                            -state_literal,
                            -input_literal,
                            states[i + 1][(residue + value) % modulus],
                        ]
                    )

    def decode(self, model: list[int]) -> dict[str, list[tuple[int, int]]]:
        positive = {literal for literal in model if literal > 0}
        return {
            name: [
                ALPHABET[next(i for i, literal in enumerate(row) if literal in positive)]
                for row in rows
            ]
            for name, rows in self.choice.items()
        }


def verify(case: int, decoded: dict[str, list[tuple[int, int]]]) -> None:
    p, q, x, y = REPRESENTATIVES[case]
    assert sum(value[0] for value in decoded["a"]) == 2 * p
    assert sum(value[1] for value in decoded["a"]) == 2 * q
    assert sum(value[0] for value in decoded["b"]) == 2 * x - 1
    assert sum(value[1] for value in decoded["b"]) == 2 * y - 1
    paf_a = gaussian_paf(decoded["a"])
    paf_b = gaussian_paf(decoded["b"])
    assert all(
        paf_a[shift][0] + paf_b[shift][0] == TARGET[shift]
        and paf_a[shift][1] + paf_b[shift][1] == 0
        for shift in range(HALF)
    )


def run_case(case: int, solver_name: str, seconds: float, output: Path | None) -> str:
    started = monotonic()
    model = Model(case)
    build_seconds = monotonic() - started
    print(
        f"case={case}; representative={REPRESENTATIVES[case]}; variables={model.pool.top}; "
        f"clauses={len(model.cnf.clauses)}; build_seconds={build_seconds:.3f}",
        flush=True,
    )
    if output is not None:
        path = output.with_name(f"{output.stem}_case{case}{output.suffix or '.cnf'}")
        model.cnf.to_file(path)
        print(f"case={case}; cnf={path}", flush=True)

    with Solver(name=solver_name, bootstrap_with=model.cnf.clauses) as solver:
        timer = None
        if seconds > 0:
            timer = Timer(seconds, solver.interrupt)
            timer.start()
        solve_started = monotonic()
        try:
            satisfiable = solver.solve_limited(expect_interrupt=True)
        finally:
            if timer is not None:
                timer.cancel()
        elapsed = monotonic() - solve_started
        if satisfiable is None:
            print(f"case={case}; status=UNKNOWN; solve_seconds={elapsed:.3f}", flush=True)
            return "UNKNOWN"
        if not satisfiable:
            print(f"case={case}; status=UNSAT; solve_seconds={elapsed:.3f}", flush=True)
            return "UNSAT"
        decoded = model.decode(solver.get_model())

    verify(case, decoded)
    print(f"case={case}; status=SAT; solve_seconds={elapsed:.3f}; exact_verification=passed")
    print(f"R_A={decoded['a']}\nR_B={decoded['b']}")
    return "SAT"


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--case", type=int, choices=range(len(REPRESENTATIVES)))
    parser.add_argument("--solver", default="glucose4")
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--write-cnf", type=Path)
    args = parser.parse_args()
    cases = range(len(REPRESENTATIVES)) if args.case is None else (args.case,)
    statuses = [run_case(case, args.solver, args.seconds, args.write_cnf) for case in cases]
    print(
        "summary="
        + ",".join(
            f"case{case}:{status}" for case, status in zip(cases, statuses, strict=True)
        )
    )


if __name__ == "__main__":
    main()
