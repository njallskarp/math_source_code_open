#!/usr/bin/env python3
"""Sparse exact MQ/SAT solver for the QLP-42 q=5/q=37 pi^3 layer."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field
from functools import cache

from generate_pi3_witnesses import (
    CASES,
    STATES,
    N,
    conjugate,
    multiply,
    read_supports,
    target,
)
from pycryptosat import Solver


def anf(truth: list[int]) -> list[int]:
    coefficients = truth.copy()
    bits = (len(truth) - 1).bit_length()
    assert len(truth) == 1 << bits
    for bit in range(bits):
        for mask in range(1 << bits):
            if (mask >> bit) & 1:
                coefficients[mask] ^= coefficients[mask ^ (1 << bit)]
    return [mask for mask, coefficient in enumerate(coefficients) if coefficient]


def state_index(bits: tuple[int, int, int], quarter: int) -> int:
    x0, x1, y1 = bits
    y0 = x0 ^ quarter
    return 4 * (2 * x1 + x0) + 2 * y1 + y0


@cache
def coordinate_anf(quarter: int, component: str, coordinate: int, predicate: str) -> tuple[int, ...]:
    truth = []
    for mask in range(8):
        bits = tuple((mask >> bit) & 1 for bit in range(3))
        value = STATES[state_index(bits, quarter)][component][coordinate]  # type: ignore[index]
        truth.append(int(value != 0) if predicate == "nonzero" else int(value < 0))
    return tuple(anf(truth))


@cache
def product_high_anf(
    left_quarter: int, right_quarter: int, component: str, residue: str
) -> tuple[int, ...]:
    truth = []
    for mask in range(64):
        left_bits = tuple((mask >> bit) & 1 for bit in range(3))
        right_bits = tuple((mask >> (bit + 3)) & 1 for bit in range(3))
        left = state_index(left_bits, left_quarter)
        right = state_index(right_bits, right_quarter)
        value = multiply(
            STATES[left][component],  # type: ignore[arg-type]
            conjugate(STATES[right][component]),  # type: ignore[arg-type]
        )
        transformed = value[0] + value[1] if residue == "plus" else value[1] - value[0]
        truth.append((transformed >> 1) & 1)
    result = tuple(anf(truth))
    assert max((mask.bit_count() for mask in result), default=0) <= 2
    return result


@dataclass
class Encoding:
    solver: Solver = field(default_factory=Solver)
    variables: int = 0
    clauses: int = 0
    xors: int = 0
    monomials: dict[tuple[int, ...], int] = field(default_factory=dict)

    def new(self) -> int:
        self.variables += 1
        return self.variables

    def clause(self, literals: list[int]) -> None:
        self.solver.add_clause(literals)
        self.clauses += 1

    def xor(self, variables: list[int], rhs: bool = False) -> None:
        self.solver.add_xor_clause(variables, rhs)
        self.xors += 1

    def conjunction(self, variables: list[int]) -> int:
        key = tuple(sorted(variables))
        if len(key) == 1:
            return key[0]
        if key not in self.monomials:
            output = self.new()
            for variable in key:
                self.clause([-output, variable])
            self.clause([output, *(-variable for variable in key)])
            self.monomials[key] = output
        return self.monomials[key]

    def define_anf(self, inputs: list[int], masks: tuple[int, ...]) -> int:
        output = self.new()
        terms = []
        constant = False
        for mask in masks:
            if mask == 0:
                constant = not constant
            else:
                terms.append(
                    self.conjunction(
                        [inputs[bit] for bit in range(len(inputs)) if (mask >> bit) & 1]
                    )
                )
        self.xor([output, *terms], constant)
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


def fix_word(encoding: Encoding, word: list[int], value: int) -> None:
    value %= 1 << len(word)
    for bit, variable in enumerate(word):
        encoding.clause([variable if (value >> bit) & 1 else -variable])


def encode_problem(
    q_value: int, orbit: int, case_id: int, threads: int = 1
) -> tuple[Encoding, list[list[list[int]]], tuple[int, int]]:
    q5, q37 = read_supports()
    support = (q5 if q_value == 5 else q37)[orbit]
    encoding = Encoding(solver=Solver(threads=threads))
    false = encoding.new()
    encoding.clause([-false])
    cells = [[[encoding.new() for _ in range(3)] for _ in range(N)] for _ in range(2)]

    opposite_words = []
    for family, support_mask in enumerate(support):
        for position, bits in enumerate(cells[family]):
            quarter = (support_mask >> position) & 1
            if quarter:
                opposite = false
            else:
                opposite = encoding.new()
                encoding.xor([bits[1], bits[2], opposite])
            opposite_words.append([opposite, false, false, false, false, false])
    fix_word(
        encoding,
        encoding.sum_words(opposite_words, 6, false),
        19 if q_value == 5 else 3,
    )

    p, q, x, y = CASES[case_id]
    sum_targets = (((p + q, q - p), (0, 0)), ((x + y - 1, y - x), (1, 0)))
    for family, support_mask in enumerate(support):
        for component_id, component in enumerate(("s", "h")):
            for coordinate in range(2):
                words = []
                for position, bits in enumerate(cells[family]):
                    quarter = (support_mask >> position) & 1
                    nonzero = encoding.define_anf(
                        bits, coordinate_anf(quarter, component, coordinate, "nonzero")
                    )
                    negative = encoding.define_anf(
                        bits, coordinate_anf(quarter, component, coordinate, "negative")
                    )
                    words.append([nonzero, negative, negative, negative, negative, negative])
                fix_word(
                    encoding,
                    encoding.sum_words(words, 6, false),
                    sum_targets[family][component_id][coordinate],
                )

    for component in ("s", "h"):
        for shift in range(1, 11):
            for residue in ("plus", "minus"):
                terms: set[int] = set()
                rhs = False
                low_count = 0
                for family, support_mask in enumerate(support):
                    for position in range(N):
                        other = (position + shift) % N
                        left_quarter = (support_mask >> position) & 1
                        right_quarter = (support_mask >> other) & 1
                        low_count += left_quarter & right_quarter
                        inputs = cells[family][position] + cells[family][other]
                        for mask in product_high_anf(
                            left_quarter, right_quarter, component, residue
                        ):
                            if mask == 0:
                                rhs = not rhs
                            else:
                                term = encoding.conjunction(
                                    [inputs[bit] for bit in range(6) if (mask >> bit) & 1]
                                )
                                if term in terms:
                                    terms.remove(term)
                                else:
                                    terms.add(term)
                wanted = target(component, shift)
                transformed = wanted[0] + wanted[1] if residue == "plus" else wanted[1] - wanted[0]
                assert low_count % 2 == transformed % 2
                rhs ^= bool(((transformed % 4) >> 1) ^ ((low_count // 2) & 1))
                if terms:
                    encoding.xor(sorted(terms), rhs)
                elif rhs:
                    encoding.clause([])
    return encoding, cells, support


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=(5, 37))
    parser.add_argument("orbit", type=int, choices=range(18))
    parser.add_argument("case", type=int, choices=range(6))
    parser.add_argument("--hint-a")
    parser.add_argument("--hint-b")
    parser.add_argument("--free-cells", type=int, default=24)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--time-limit", type=float)
    parser.add_argument("--threads", type=int, default=1)
    args = parser.parse_args()
    encoding, cells, support = encode_problem(args.q, args.orbit, args.case, args.threads)
    print(
        f"variables={encoding.variables};clauses={encoding.clauses};"
        f"xors={encoding.xors};monomials={len(encoding.monomials)}",
        flush=True,
    )
    hints = (args.hint_a, args.hint_b)
    if (args.hint_a is None) != (args.hint_b is None):
        parser.error("--hint-a and --hint-b must be supplied together")
    attempts = args.trials if args.hint_a is not None else 1
    generator = random.Random(100000 * args.q + 100 * args.orbit + args.case)
    satisfiable = None
    model = None
    for trial in range(attempts):
        assumptions = []
        if args.hint_a is not None:
            free = set(generator.sample(range(42), args.free_cells))
            for family, word in enumerate(hints):
                assert word is not None and len(word) == N
                for position, character in enumerate(word):
                    cell = family * N + position
                    if cell in free:
                        continue
                    state = int(character, 16)
                    x_phase, y_phase = divmod(state, 4)
                    values = (x_phase & 1, x_phase >> 1, y_phase >> 1)
                    for variable, value in zip(cells[family][position], values, strict=True):
                        assumptions.append(variable if value else -variable)
        satisfiable, model = encoding.solver.solve(
            assumptions=assumptions, time_limit=args.time_limit
        )
        print(f"trial={trial};status={satisfiable}", flush=True)
        if satisfiable:
            break
    print(f"satisfiable={satisfiable}")
    if satisfiable:
        words = []
        for family, support_mask in enumerate(support):
            word = []
            for position, bits in enumerate(cells[family]):
                values = tuple(int(model[variable]) for variable in bits)
                word.append(state_index(values, (support_mask >> position) & 1))
            words.append(word)
        encode = lambda word: "".join(format(state, "x") for state in word)
        print(
            f"{args.q}\t{args.orbit}\t{args.case}\t{support[0]:06x}\t{support[1]:06x}\t"
            f"{encode(words[0])}\t{encode(words[1])}"
        )


if __name__ == "__main__":
    main()
