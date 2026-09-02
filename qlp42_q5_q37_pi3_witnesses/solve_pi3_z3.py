#!/usr/bin/env python3
"""Independent bit-vector witness search for the QLP-42 pi^3 frontier."""

from __future__ import annotations

import argparse
from itertools import product

import z3
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


def constant_array(index_bits: int, values: list[int], result_sort: z3.SortRef) -> z3.ArrayRef:
    result = z3.K(z3.BitVecSort(index_bits), z3.Const("zero", result_sort))
    zero = z3.IntVal(0) if result_sort == z3.IntSort() else z3.BitVecVal(0, result_sort.size())
    result = z3.K(z3.BitVecSort(index_bits), zero)
    for index, value in enumerate(values):
        item = z3.IntVal(value) if result_sort == z3.IntSort() else z3.BitVecVal(value, result_sort.size())
        result = z3.Store(result, z3.BitVecVal(index, index_bits), item)
    return result


COORDINATES = {
    (component, coordinate): constant_array(
        4,
        [state[component][coordinate] for state in STATES],  # type: ignore[index]
        z3.IntSort(),
    )
    for component in ("s", "h")
    for coordinate in range(2)
}
OPPOSITE_ARRAY = constant_array(4, list(OPPOSITE), z3.IntSort())
PRODUCTS = {}
for component in ("s", "h"):
    plus = []
    minus = []
    for left, right in product(range(16), repeat=2):
        value = multiply(STATES[left][component], conjugate(STATES[right][component]))  # type: ignore[arg-type]
        plus.append((value[0] + value[1]) % 4)
        minus.append((value[1] - value[0]) % 4)
    PRODUCTS[(component, "plus")] = constant_array(8, plus, z3.BitVecSort(2))
    PRODUCTS[(component, "minus")] = constant_array(8, minus, z3.BitVecSort(2))


def solve(q_value: int, orbit: int, case_id: int, timeout_ms: int) -> None:
    q5, q37 = read_supports()
    support = (q5 if q_value == 5 else q37)[orbit]
    solver = z3.Solver()
    solver.set(timeout=timeout_ms, random_seed=100000 * q_value + 100 * orbit + case_id)
    states = [[z3.BitVec(f"z_{family}_{position}", 4) for position in range(N)] for family in range(2)]
    for family, support_mask in enumerate(support):
        for position, state in enumerate(states[family]):
            allowed = QUARTER if (support_mask >> position) & 1 else NONQUARTER
            solver.add(z3.Or(*(state == index for index in allowed)))
    solver.add(
        z3.Sum(*(z3.Select(OPPOSITE_ARRAY, state) for family in states for state in family))
        == (19 if q_value == 5 else 3)
    )

    p, q, x, y = CASES[case_id]
    sum_targets = (((p + q, q - p), (0, 0)), ((x + y - 1, y - x), (1, 0)))
    for family in range(2):
        for component_id, component in enumerate(("s", "h")):
            for coordinate in range(2):
                solver.add(
                    z3.Sum(*(z3.Select(COORDINATES[(component, coordinate)], state) for state in states[family]))
                    == sum_targets[family][component_id][coordinate]
                )

    for component in ("s", "h"):
        for shift in range(1, 11):
            indices = [
                z3.Concat(states[family][position], states[family][(position + shift) % N])
                for family in range(2)
                for position in range(N)
            ]
            wanted = target(component, shift)
            plus_target = (wanted[0] + wanted[1]) % 4
            minus_target = (wanted[1] - wanted[0]) % 4
            solver.add(
                sum((z3.Select(PRODUCTS[(component, "plus")], index) for index in indices), z3.BitVecVal(0, 2))
                == z3.BitVecVal(plus_target, 2)
            )
            solver.add(
                sum((z3.Select(PRODUCTS[(component, "minus")], index) for index in indices), z3.BitVecVal(0, 2))
                == z3.BitVecVal(minus_target, 2)
            )

    status = solver.check()
    print(f"status={status}")
    if status == z3.sat:
        model = solver.model()
        words = [[model.eval(state).as_long() for state in family] for family in states]
        encode = lambda word: "".join(format(value, "x") for value in word)
        print(
            f"{q_value}\t{orbit}\t{case_id}\t{support[0]:06x}\t{support[1]:06x}\t"
            f"{encode(words[0])}\t{encode(words[1])}"
        )
    elif status == z3.unknown:
        print(f"reason={solver.reason_unknown()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=(5, 37))
    parser.add_argument("orbit", type=int, choices=range(18))
    parser.add_argument("case", type=int, choices=range(6))
    parser.add_argument("--timeout-ms", type=int, default=60000)
    args = parser.parse_args()
    solve(args.q, args.orbit, args.case, args.timeout_ms)


if __name__ == "__main__":
    main()
