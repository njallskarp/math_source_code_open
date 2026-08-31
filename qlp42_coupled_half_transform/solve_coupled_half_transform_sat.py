#!/usr/bin/env python3
"""Exact SAT model for the coupled norm-32 QLP-42 shell transform.

Each of the 42 transformed coordinates chooses one of the 16 exact local
(S,H) states.  Gaussian sums and autocorrelations are enforced by Boolean
finite-state summation automata, so the generated CNF delegates no nonlinear
or floating-point semantics to the SAT solver.
"""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from threading import Timer
from time import monotonic

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver, SolverNames

G = tuple[int, int]
HALF = 21
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
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


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def sub(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def div_one_plus_i(value: G) -> G:
    assert (value[0] + value[1]) % 2 == 0
    assert (value[1] - value[0]) % 2 == 0
    return (value[0] + value[1]) // 2, (value[1] - value[0]) // 2


# State entries are (S,H,x,y).  Retaining x,y makes SAT-model decoding and
# independent verification of the reconstructed length-42 words immediate.
STATES = tuple(
    (div_one_plus_i(sub(x, y)), div_one_plus_i(add(x, y)), x, y)
    for x in ROOTS
    for y in ROOTS
)
assert len({(state[0], state[1]) for state in STATES}) == 16


def gaussian_paf(sequence: list[G]) -> list[G]:
    return [
        (
            sum(
                sequence[j][0] * sequence[(j + shift) % len(sequence)][0]
                + sequence[j][1] * sequence[(j + shift) % len(sequence)][1]
                for j in range(len(sequence))
            ),
            sum(
                sequence[j][1] * sequence[(j + shift) % len(sequence)][0]
                - sequence[j][0] * sequence[(j + shift) % len(sequence)][1]
                for j in range(len(sequence))
            ),
        )
        for shift in range(len(sequence))
    ]


class Model:
    def __init__(
        self,
        case: int,
        quarter_turns: int | None,
        symmetry_breaking: bool = True,
    ) -> None:
        self.case = case
        self.quarter_turns = quarter_turns
        self.pool = IDPool()
        self.cnf = CNF()
        self.choice = {
            name: [
                [self.pool.id(f"{name}_{j}_{state}") for state in range(len(STATES))]
                for j in range(HALF)
            ]
            for name in ("a", "b")
        }
        for rows in self.choice.values():
            for row in rows:
                self.add_exactly_one(row)

        # Independent cyclic rotation of each original word by an even CRT
        # shift rotates its coupled state word and preserves every constraint.
        if symmetry_breaking:
            if quarter_turns == 1:
                rotation_names = ("a",)
            elif quarter_turns == 41:
                rotation_names = ("b",)
            else:
                rotation_names = ("a", "b")
            for name in rotation_names:
                rows = self.choice[name]
                for row in rows[1:]:
                    for at_zero in range(len(STATES)):
                        for later in range(at_zero):
                            self.cnf.append([-rows[0][at_zero], -row[later]])

        p, q, x, y = REPRESENTATIVES[case]
        targets = {
            "a": ((p + q, q - p), (0, 0)),
            "b": ((x + y - 1, y - x), (1, 0)),
        }
        for name, (sum_s, sum_h) in targets.items():
            for component, target in ((0, sum_s), (1, sum_h)):
                for coordinate in range(2):
                    self.add_sum_automaton(
                        self.choice[name],
                        [state[component][coordinate] for state in STATES],
                        target[coordinate],
                        f"sum_{name}_{component}_{coordinate}",
                    )

        all_rows = self.choice["a"] + self.choice["b"]
        unit_values = [
            int(state[0][0] * state[0][0] + state[0][1] * state[0][1] == 1)
            for state in STATES
        ]
        self.add_modulo_automaton(
            all_rows,
            unit_values,
            modulus=4,
            target=1,
            label="quarter_turns_mod4",
        )
        # The fixed Gaussian sums orient the two binary shadows: reducing
        # sum(H_A)=0 and sum(H_B)=1 modulo 1+i forces an even number of
        # quarter-turn cells in A and an odd number in B.  These clauses are
        # logically redundant with the exact H-sum automata but propagate the
        # oriented mod-7 refinement directly in the Boolean layer.
        self.add_modulo_automaton(
            self.choice["a"],
            unit_values,
            modulus=2,
            target=0,
            label="quarter_turns_a_even",
        )
        self.add_modulo_automaton(
            self.choice["b"],
            unit_values,
            modulus=2,
            target=1,
            label="quarter_turns_b_odd",
        )
        if quarter_turns is not None:
            self.add_sum_automaton(
                all_rows,
                unit_values,
                quarter_turns,
                "quarter_turns_exact",
            )

        self.unit = {
            name: [self.pool.id(f"unit_{name}_{j}") for j in range(HALF)]
            for name in ("a", "b")
        }
        unit_indices = [index for index, value in enumerate(unit_values) if value]
        for name, rows in self.choice.items():
            for j, row in enumerate(rows):
                unit = self.unit[name][j]
                for index in unit_indices:
                    self.cnf.append([-row[index], unit])
                self.cnf.append([-unit, *(row[index] for index in unit_indices)])
        if symmetry_breaking:
            self.add_extreme_branch_constraints()
        self.add_binary_shadow()

        # The two center energies are redundant under the local state table,
        # but encoding both makes the complementary 43+41 split explicit.
        for component, target, label in ((0, 43, "s"), (1, 41, "h")):
            self.add_sum_automaton(
                all_rows,
                [
                    state[component][0] ** 2 + state[component][1] ** 2
                    for state in STATES
                ],
                target,
                f"energy_{label}",
            )

        for shift in range(1, HALF // 2 + 1):
            for component, target, label in (
                (0, TARGET_S[shift], "s"),
                (1, TARGET_H[shift], "h"),
            ):
                real_rows: list[list[int]] = []
                imaginary_rows: list[list[int]] = []
                real_values: list[int] = []
                imaginary_values: list[int] = []
                for left in STATES:
                    ar, ai = left[component]
                    for right in STATES:
                        br, bi = right[component]
                        real_values.append(ar * br + ai * bi)
                        imaginary_values.append(ai * br - ar * bi)
                for name in ("a", "b"):
                    rows = self.choice[name]
                    for j in range(HALF):
                        left = rows[j]
                        right = rows[(j + shift) % HALF]
                        real_rows.append(
                            self.product_value_row(
                                left,
                                right,
                                real_values,
                                f"corr_{label}_r_{shift}_{name}_{j}",
                            )
                        )
                        imaginary_rows.append(
                            self.product_value_row(
                                left,
                                right,
                                imaginary_values,
                                f"corr_{label}_i_{shift}_{name}_{j}",
                            )
                        )
                self.add_sum_automaton(
                    real_rows,
                    list(range(-2, 3)),
                    target,
                    f"paf_{label}_r_{shift}",
                )
                self.add_sum_automaton(
                    imaginary_rows,
                    list(range(-2, 3)),
                    0,
                    f"paf_{label}_i_{shift}",
                )

    def add_extreme_branch_constraints(self) -> None:
        """Encode the proved reflection lemmas at q=1 and q=41."""
        opposite_indices = tuple(
            index for index, state in enumerate(STATES) if state[1] == (0, 0)
        )
        if self.quarter_turns == 1:
            # Rotate the unique B-quarter cell to zero.  The fixed sums orient
            # its S entry to the imaginary axis and H entry to the real axis.
            oriented_quarter_indices = tuple(
                index
                for index, state in enumerate(STATES)
                if state[0][0] == 0
                and state[1][1] == 0
                and state[0][0] ** 2 + state[0][1] ** 2 == 1
            )
            assert len(oriented_quarter_indices) == 4
            self.cnf.append(
                [self.choice["b"][0][index] for index in oriented_quarter_indices]
            )
            opposite = [
                self.add_subset_indicator(
                    row, opposite_indices, f"q1_b_opposite_{j}"
                )
                for j, row in enumerate(self.choice["b"])
            ]
            for shift in range(1, HALF // 2 + 1):
                left = opposite[shift]
                right = opposite[-shift]
                self.cnf.extend(([-left, right], [left, -right]))
            minimum, maximum = {
                0: (4, 20),
                1: (4, 18),
                2: (4, 18),
                3: (4, 16),
                4: (4, 16),
                5: (2, 16),
            }[self.case]
            self.cnf.extend(
                CardEnc.atleast(
                    lits=opposite,
                    bound=minimum,
                    vpool=self.pool,
                    encoding=EncType.seqcounter,
                ).clauses
            )
            self.cnf.extend(
                CardEnc.atmost(
                    lits=opposite,
                    bound=maximum,
                    vpool=self.pool,
                    encoding=EncType.seqcounter,
                ).clauses
            )

        if self.quarter_turns == 41:
            # Rotate the unique A-opposite cell to zero.  Around that center,
            # the imaginary/real axes of the H units are reflected.
            self.cnf.append(
                [self.choice["a"][0][index] for index in opposite_indices]
            )
            imaginary_h_indices = tuple(
                index
                for index, state in enumerate(STATES)
                if state[1] in ((0, 1), (0, -1))
            )
            assert len(imaginary_h_indices) == 4
            imaginary_axis = [
                self.add_subset_indicator(
                    row, imaginary_h_indices, f"q41_a_h_imaginary_{j}"
                )
                for j, row in enumerate(self.choice["a"])
            ]
            for shift in range(1, HALF // 2 + 1):
                left = imaginary_axis[shift]
                right = imaginary_axis[-shift]
                self.cnf.extend(([-left, right], [left, -right]))

    def add_exactly_one(self, literals: list[int]) -> None:
        self.cnf.append(literals)
        for i, left in enumerate(literals):
            for right in literals[i + 1 :]:
                self.cnf.append([-left, -right])

    def add_subset_indicator(
        self, row: list[int], indices: tuple[int, ...], label: str
    ) -> int:
        result = self.pool.id(label)
        for index in indices:
            self.cnf.append([-row[index], result])
        self.cnf.append([-result, *(row[index] for index in indices)])
        return result

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

    def add_and(self, left: int, right: int, label: str) -> int:
        result = self.pool.id(label)
        self.cnf.extend([[-result, left], [-result, right], [-left, -right, result]])
        return result

    def add_xor_equality(self, literals: list[int], parity: int, label: str) -> None:
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
                else:
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
        outputs = [self.pool.id(f"{label}_{value}") for value in range(-2, 3)]
        self.add_exactly_one(outputs)
        width = len(STATES)
        for a in range(width):
            for b in range(width):
                self.cnf.append([-left[a], -right[b], outputs[values[a * width + b] + 2]])
        return outputs

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

    def decode(self, model: list[int]) -> dict[str, list[tuple[G, G, G, G]]]:
        positive = {literal for literal in model if literal > 0}
        return {
            name: [
                STATES[next(i for i, literal in enumerate(row) if literal in positive)]
                for row in rows
            ]
            for name, rows in self.choice.items()
        }


def verify(case: int, decoded: dict[str, list[tuple[G, G, G, G]]]) -> None:
    p, q, x, y = REPRESENTATIVES[case]
    expected_sums = {
        "a": ((p + q, q - p), (0, 0)),
        "b": ((x + y - 1, y - x), (1, 0)),
    }
    transformed: dict[str, tuple[list[G], list[G]]] = {}
    originals: dict[str, list[G]] = {}
    for name, states in decoded.items():
        s_word = [state[0] for state in states]
        h_word = [state[1] for state in states]
        transformed[name] = s_word, h_word
        assert tuple(map(sum, zip(*s_word, strict=True))) == expected_sums[name][0]
        assert tuple(map(sum, zip(*h_word, strict=True))) == expected_sums[name][1]
        original = [(0, 0)] * 42
        for j, state in enumerate(states):
            original[22 * j % 42] = state[2]
            original[(22 * j + 21) % 42] = state[3]
        originals[name] = original

    quarter_counts = {
        name: sum(
            state[0][0] * state[0][0] + state[0][1] * state[0][1] == 1
            for state in states
        )
        for name, states in decoded.items()
    }
    assert quarter_counts["a"] % 2 == 0
    assert quarter_counts["b"] % 2 == 1

    for component, target in ((0, TARGET_S), (1, TARGET_H)):
        paf_a = gaussian_paf(transformed["a"][component])
        paf_b = gaussian_paf(transformed["b"][component])
        assert all(
            paf_a[shift][0] + paf_b[shift][0] == target[shift]
            and paf_a[shift][1] + paf_b[shift][1] == 0
            for shift in range(HALF)
        )

    assert tuple(map(sum, zip(*originals["a"], strict=True))) == (0, 0)
    assert tuple(map(sum, zip(*originals["b"], strict=True))) == (1, 1)
    paf_a = gaussian_paf(originals["a"])
    paf_b = gaussian_paf(originals["b"])
    combined = [
        (paf_a[shift][0] + paf_b[shift][0], paf_a[shift][1] + paf_b[shift][1])
        for shift in range(42)
    ]
    target = [(-2, 0)] * 42
    target[0] = (84, 0)
    for shift in (4, 11, 31, 38):
        target[shift] = (-4, 0)
    for shift in (10, 17, 25, 32):
        target[shift] = (0, 0)
    assert combined == target


def run_case(
    case: int,
    quarter_turns: int | None,
    solver_name: str,
    seconds: float,
    output: Path | None,
) -> str:
    cadical_names = set(
        SolverNames.cadical103
        + SolverNames.cadical153
        + SolverNames.cadical195
        + SolverNames.cadical300
    )
    if seconds > 0 and solver_name.lower() in cadical_names:
        raise ValueError(
            "CaDiCaL does not support PySAT's interruptible limited solve; "
            "use --seconds 0 or an interruptible solver such as glucose4"
        )
    started = monotonic()
    model = Model(case, quarter_turns)
    build_seconds = monotonic() - started
    print(
        f"case={case}; quarter_turns={quarter_turns}; variables={model.pool.top}; "
        f"clauses={len(model.cnf.clauses)}; build_seconds={build_seconds:.3f}",
        flush=True,
    )
    if output is not None:
        suffix = "all" if quarter_turns is None else str(quarter_turns)
        path = output.with_name(f"{output.stem}_case{case}_q{suffix}.cnf")
        model.cnf.to_file(path)
        print(f"cnf={path}", flush=True)
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
            print(f"status=UNKNOWN; solve_seconds={elapsed:.3f}", flush=True)
            return "UNKNOWN"
        if not satisfiable:
            print(f"status=UNSAT; solve_seconds={elapsed:.3f}", flush=True)
            return "UNSAT"
        decoded = model.decode(solver.get_model())
    verify(case, decoded)
    print(f"status=SAT; solve_seconds={elapsed:.3f}; exact_verification=passed")
    for name, states in decoded.items():
        print(f"{name.upper()}_STATES={states}")
    return "SAT"


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--case", type=int, choices=range(len(REPRESENTATIVES)), required=True)
    parser.add_argument("--quarter-turns", type=int, choices=range(1, 42, 4))
    parser.add_argument("--solver", default="glucose4")
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--write-cnf", type=Path)
    args = parser.parse_args()
    status = run_case(
        args.case,
        args.quarter_turns,
        args.solver,
        args.seconds,
        args.write_cnf,
    )
    print(f"summary=case{args.case}:{status}")


if __name__ == "__main__":
    main()
