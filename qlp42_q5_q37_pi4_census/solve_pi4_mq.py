#!/usr/bin/env python3
"""Exact sparse MQ/SAT encoding of the QLP-42 Gaussian pi^4 layer.

This strengthens the complete pi^3 cell encoding in the adjacent published
directory.  Since pi^4 = -4, a Gaussian residual is divisible by pi^4 exactly
when its real and imaginary coordinates are both zero modulo 4.
"""

from __future__ import annotations

import argparse
import random
import sys
from functools import cache
from pathlib import Path

PI3_DIRECTORY = Path(__file__).resolve().parent.parent / "qlp42_q5_q37_pi3_witnesses"
sys.path.insert(0, str(PI3_DIRECTORY))

from generate_pi3_witnesses import N, STATES, conjugate, multiply, target  # noqa: E402
from solve_pi3_mq import (  # noqa: E402
    Encoding,
    anf,
    encode_problem as encode_pi3_problem,
    fix_word,
    state_index,
)


@cache
def product_coordinate_anf(
    left_quarter: int,
    right_quarter: int,
    component: str,
    coordinate: int,
    bit: int,
) -> tuple[int, ...]:
    """Return the ANF of one product-coordinate bit modulo 4.

    Product coordinates lie in {-2,-1,0,1,2}.  Reducing modulo 4 and taking
    literal little-endian bits handles all five possibilities without a
    signed-arithmetic shortcut.
    """

    if bit not in (0, 1):
        raise ValueError(f"unsupported bit: {bit}")
    truth = []
    for mask in range(64):
        left_bits = tuple((mask >> bit) & 1 for bit in range(3))
        right_bits = tuple((mask >> (bit + 3)) & 1 for bit in range(3))
        left = state_index(left_bits, left_quarter)
        right = state_index(right_bits, right_quarter)
        value = multiply(
            STATES[left][component],  # type: ignore[arg-type]
            conjugate(STATES[right][component]),  # type: ignore[arg-type]
        )[coordinate]
        assert value in (-2, -1, 0, 1, 2)
        truth.append(((value % 4) >> bit) & 1)
    return tuple(anf(truth))


def encode_problem(
    q_value: int, orbit: int, case_id: int, threads: int = 1
) -> tuple[Encoding, list[list[list[int]]], tuple[int, int]]:
    """Encode a full exact-sum cell together with every pi^4 correlation test."""

    encoding, cells, support = encode_pi3_problem(q_value, orbit, case_id, threads)
    false = encoding.new()
    encoding.clause([-false])

    for component in ("s", "h"):
        for shift in range(1, 11):
            wanted = target(component, shift)
            for coordinate in range(2):
                words: list[list[int]] = []
                for family, support_mask in enumerate(support):
                    for position in range(N):
                        other = (position + shift) % N
                        left_quarter = (support_mask >> position) & 1
                        right_quarter = (support_mask >> other) & 1
                        inputs = cells[family][position] + cells[family][other]
                        words.append(
                            [
                                encoding.define_anf(
                                    inputs,
                                    product_coordinate_anf(
                                        left_quarter,
                                        right_quarter,
                                        component,
                                        coordinate,
                                        bit,
                                    ),
                                )
                                for bit in range(2)
                            ]
                        )
                fix_word(encoding, encoding.sum_words(words, 2, false), wanted[coordinate])
    return encoding, cells, support


def assumptions_from_words(
    cells: list[list[list[int]]], words: tuple[str, str], free: set[int]
) -> list[int]:
    assumptions = []
    for family, word in enumerate(words):
        if len(word) != N:
            raise ValueError(f"word {family} has length {len(word)}, expected {N}")
        for position, character in enumerate(word):
            cell = family * N + position
            if cell in free:
                continue
            state = int(character, 16)
            x_phase, y_phase = divmod(state, 4)
            values = (x_phase & 1, x_phase >> 1, y_phase >> 1)
            for variable, value in zip(cells[family][position], values, strict=True):
                assumptions.append(variable if value else -variable)
    return assumptions


def decode_model(
    cells: list[list[list[int]]], support: tuple[int, int], model: list[bool | None]
) -> tuple[str, str]:
    result = []
    for family, support_mask in enumerate(support):
        states = []
        for position, bits in enumerate(cells[family]):
            values = tuple(int(bool(model[variable])) for variable in bits)
            states.append(state_index(values, (support_mask >> position) & 1))
        result.append("".join(format(state, "x") for state in states))
    return result[0], result[1]


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
    if (args.hint_a is None) != (args.hint_b is None):
        parser.error("--hint-a and --hint-b must be supplied together")
    if not 0 <= args.free_cells <= 42:
        parser.error("--free-cells must lie in 0,...,42")

    encoding, cells, support = encode_problem(args.q, args.orbit, args.case, args.threads)
    print(
        f"variables={encoding.variables};clauses={encoding.clauses};"
        f"xors={encoding.xors};monomials={len(encoding.monomials)}",
        flush=True,
    )
    attempts = args.trials if args.hint_a is not None else 1
    generator = random.Random(100000 * args.q + 100 * args.orbit + args.case)
    satisfiable = None
    model = None
    for trial in range(attempts):
        assumptions = []
        if args.hint_a is not None and args.hint_b is not None:
            free = set(generator.sample(range(42), args.free_cells))
            assumptions = assumptions_from_words(cells, (args.hint_a, args.hint_b), free)
        satisfiable, model = encoding.solver.solve(
            assumptions=assumptions, time_limit=args.time_limit
        )
        print(f"trial={trial};status={satisfiable}", flush=True)
        if satisfiable:
            break
    print(f"satisfiable={satisfiable}")
    if satisfiable:
        assert model is not None
        states_a, states_b = decode_model(cells, support, model)
        print(
            f"{args.q}\t{args.orbit}\t{args.case}\t{support[0]:06x}\t"
            f"{support[1]:06x}\t{states_a}\t{states_b}"
        )


if __name__ == "__main__":
    main()
