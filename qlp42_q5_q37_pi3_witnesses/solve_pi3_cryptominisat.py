#!/usr/bin/env python3
"""CNF/XOR witness search for the QLP-42 q=5/q=37 pi^3 frontier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field

from generate_pi3_witnesses import (
    CASES,
    NONQUARTER,
    OPPOSITE,
    QUARTER,
    STATES,
    N,
    conjugate,
    multiply,
    read_supports,
    target,
)
from pycryptosat import Solver


@dataclass
class Encoding:
    solver: Solver = field(default_factory=Solver)
    variables: int = 0
    clauses: int = 0
    xors: int = 0

    def new(self) -> int:
        self.variables += 1
        return self.variables

    def clause(self, literals: list[int]) -> None:
        self.solver.add_clause(literals)
        self.clauses += 1

    def xor(self, variables: list[int], rhs: bool = False) -> None:
        self.solver.add_xor_clause(variables, rhs)
        self.xors += 1

    def exactly_one(self, variables: list[int]) -> None:
        self.clause(variables)
        for left in range(len(variables)):
            for right in range(left + 1, len(variables)):
                self.clause([-variables[left], -variables[right]])

    def and_gate(self, left: int, right: int) -> int:
        output = self.new()
        self.clause([-output, left])
        self.clause([-output, right])
        self.clause([output, -left, -right])
        return output

    def full_adder(self, left: int, right: int, carry_in: int) -> tuple[int, int]:
        total = self.new()
        carry_out = self.new()
        self.xor([left, right, carry_in, total])
        self.clause([-left, -right, carry_out])
        self.clause([-left, -carry_in, carry_out])
        self.clause([-right, -carry_in, carry_out])
        self.clause([left, right, -carry_out])
        self.clause([left, carry_in, -carry_out])
        self.clause([right, carry_in, -carry_out])
        return total, carry_out

    def add_words(self, left: list[int], right: list[int], false: int) -> list[int]:
        assert len(left) == len(right)
        result = []
        carry = false
        for left_bit, right_bit in zip(left, right, strict=True):
            total, carry = self.full_adder(left_bit, right_bit, carry)
            result.append(total)
        return result

    def sum_words(self, words: list[list[int]], bits: int, false: int) -> list[int]:
        result = [false] * bits
        for word in words:
            result = self.add_words(result, word, false)
        return result

    def select_bit(self, state_variables: dict[int, int], values: list[int]) -> int:
        selected = [variable for state, variable in state_variables.items() if values[state]]
        output = self.new()
        if selected:
            self.xor([output, *selected])
        else:
            self.clause([-output])
        return output


def fix_word(encoding: Encoding, word: list[int], value: int) -> None:
    value %= 1 << len(word)
    for bit, variable in enumerate(word):
        encoding.clause([variable if (value >> bit) & 1 else -variable])


def encode_problem(q_value: int, orbit: int, case_id: int) -> tuple[Encoding, list[list[dict[int, int]]], tuple[int, int]]:
    q5, q37 = read_supports()
    support = (q5 if q_value == 5 else q37)[orbit]
    encoding = Encoding()
    false = encoding.new()
    encoding.clause([-false])

    cells: list[list[dict[int, int]]] = []
    for family, support_mask in enumerate(support):
        family_cells = []
        for position in range(N):
            allowed = QUARTER if (support_mask >> position) & 1 else NONQUARTER
            state_variables = {state: encoding.new() for state in allowed}
            encoding.exactly_one(list(state_variables.values()))
            family_cells.append(state_variables)
        cells.append(family_cells)

    opposite_words = []
    for family in cells:
        for state_variables in family:
            bit = encoding.select_bit(state_variables, list(OPPOSITE))
            opposite_words.append([bit, false, false, false, false, false])
    fix_word(
        encoding,
        encoding.sum_words(opposite_words, 6, false),
        19 if q_value == 5 else 3,
    )

    p, q, x, y = CASES[case_id]
    sum_targets = (((p + q, q - p), (0, 0)), ((x + y - 1, y - x), (1, 0)))
    for family in range(2):
        for component_id, component in enumerate(("s", "h")):
            for coordinate in range(2):
                words = []
                values = [state[component][coordinate] for state in STATES]  # type: ignore[index]
                for state_variables in cells[family]:
                    nonzero = encoding.select_bit(
                        state_variables, [int(value != 0) for value in values]
                    )
                    negative = encoding.select_bit(
                        state_variables, [int(value < 0) for value in values]
                    )
                    words.append([nonzero, negative, negative, negative, negative, negative])
                fix_word(
                    encoding,
                    encoding.sum_words(words, 6, false),
                    sum_targets[family][component_id][coordinate],
                )

    for component in ("s", "h"):
        for shift in range(1, 11):
            residue_words = {"plus": [], "minus": []}
            for family in range(2):
                for position in range(N):
                    left = cells[family][position]
                    right = cells[family][(position + shift) % N]
                    output = {
                        "plus": [encoding.new(), encoding.new()],
                        "minus": [encoding.new(), encoding.new()],
                    }
                    for left_state, left_variable in left.items():
                        for right_state, right_variable in right.items():
                            value = multiply(
                                STATES[left_state][component],  # type: ignore[arg-type]
                                conjugate(STATES[right_state][component]),  # type: ignore[arg-type]
                            )
                            residues = {
                                "plus": (value[0] + value[1]) % 4,
                                "minus": (value[1] - value[0]) % 4,
                            }
                            for name in ("plus", "minus"):
                                for bit in range(2):
                                    literal = output[name][bit]
                                    if not ((residues[name] >> bit) & 1):
                                        literal = -literal
                                    encoding.clause([-left_variable, -right_variable, literal])
                    for name in ("plus", "minus"):
                        residue_words[name].append(output[name])
            wanted = target(component, shift)
            wanted_residues = {
                "plus": (wanted[0] + wanted[1]) % 4,
                "minus": (wanted[1] - wanted[0]) % 4,
            }
            for name in ("plus", "minus"):
                fix_word(
                    encoding,
                    encoding.sum_words(residue_words[name], 2, false),
                    wanted_residues[name],
                )
    return encoding, cells, support


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=(5, 37))
    parser.add_argument("orbit", type=int, choices=range(18))
    parser.add_argument("case", type=int, choices=range(6))
    args = parser.parse_args()
    encoding, cells, support = encode_problem(args.q, args.orbit, args.case)
    print(
        f"variables={encoding.variables};clauses={encoding.clauses};xors={encoding.xors}",
        flush=True,
    )
    satisfiable, model = encoding.solver.solve()
    print(f"satisfiable={int(satisfiable)}")
    if satisfiable:
        words = []
        for family in cells:
            word = []
            for state_variables in family:
                selected = [state for state, variable in state_variables.items() if model[variable]]
                assert len(selected) == 1
                word.append(selected[0])
            words.append(word)
        encode = lambda word: "".join(format(state, "x") for state in word)
        print(
            f"{args.q}\t{args.orbit}\t{args.case}\t{support[0]:06x}\t{support[1]:06x}\t"
            f"{encode(words[0])}\t{encode(words[1])}"
        )


if __name__ == "__main__":
    main()
