#!/usr/bin/env python3
"""Generate exact equal-margin certificates for the 96 order-eight obstructions.

SciPy/HiGHS is used only to discover sparse basic feasible solutions.  Every
floating-point result is rationally reconstructed and checked exactly before
it is written.  The standard-library verifier is the correctness boundary.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix

N = 8
PAIRS = tuple((i, j) for i in range(N) for j in range(i + 1, N))
TARGET = Fraction(13, 20)


def read_obstructions(path: Path) -> list[tuple[int, int]]:
    records: list[tuple[int, int]] = []
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        index_text, mask_text = line.split()
        records.append((int(index_text), int(mask_text)))
    if len(records) != 96 or len(set(records)) != 96:
        raise ValueError("expected 96 distinct obstruction records")
    return records


def order_data() -> tuple[list[tuple[int, ...]], np.ndarray]:
    orders = list(itertools.permutations(range(N)))
    vectors = np.empty((len(PAIRS), len(orders)), dtype=np.int8)
    for column, order in enumerate(orders):
        position = [0] * N
        for rank, vertex in enumerate(order):
            position[vertex] = rank
        for edge, (left, right) in enumerate(PAIRS):
            vectors[edge, column] = int(position[left] < position[right])
    return orders, vectors


def agrees_matrix(tournament: int, vectors: np.ndarray) -> np.ndarray:
    bits = np.array(
        [(tournament >> edge) & 1 for edge in range(len(PAIRS))],
        dtype=np.int8,
    )
    return np.where(bits[:, None], vectors, 1 - vectors).astype(float)


def exact_primal(
    solution: np.ndarray, agrees: np.ndarray
) -> list[tuple[int, Fraction]]:
    weights = [Fraction(float(value)).limit_denominator(100_000) for value in solution]
    sparse = [(index, weight) for index, weight in enumerate(weights) if weight]
    if any(weight < 0 for _, weight in sparse):
        raise ArithmeticError("negative reconstructed weight")
    if sum(weight for _, weight in sparse) != 1:
        raise ArithmeticError("reconstructed weights do not sum to one")
    for edge in range(len(PAIRS)):
        coverage = sum(
            weight for index, weight in sparse if int(agrees[edge, index]) == 1
        )
        if coverage != TARGET:
            raise ArithmeticError(
                f"edge {edge} has reconstructed coverage {coverage}, not {TARGET}"
            )
    return sparse


def solve_one(
    tournament: int, vectors: np.ndarray
) -> tuple[tuple[int, ...], list[tuple[int, Fraction]]]:
    agrees = agrees_matrix(tournament, vectors)
    order_count = agrees.shape[1]
    a_eq = np.hstack(
        [
            np.vstack([np.ones((1, order_count)), agrees]),
            np.r_[0.0, -np.ones(len(PAIRS))][:, None],
        ]
    )
    b_eq = np.r_[1.0, np.zeros(len(PAIRS))]
    objective = np.r_[np.zeros(order_count), -1.0]
    result = linprog(
        objective,
        A_eq=csc_matrix(a_eq),
        b_eq=b_eq,
        bounds=[(0, None)] * order_count + [(0, 1)],
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    value = Fraction(float(result.x[-1])).limit_denominator(100_000)
    if value != TARGET:
        raise ArithmeticError(f"unexpected optimum reconstruction {value}")

    dual = tuple(
        edge
        for edge, marginal in enumerate(result.eqlin.marginals[1:])
        if abs(float(marginal) - 1 / 20) < 1e-8
    )
    if len(dual) != 20:
        raise ArithmeticError(f"expected a 20-arc dual, got {len(dual)} arcs")
    maximum = max(
        sum(int(agrees[edge, order]) for edge in dual)
        for order in range(order_count)
    )
    if maximum != 13:
        raise ArithmeticError(f"dual maximum is {maximum}, not 13")

    return dual, exact_primal(result.x[:-1], agrees)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--obstructions", type=Path, default=Path("obstructions.txt"))
    parser.add_argument("--output", type=Path, default=Path("certificate.txt"))
    args = parser.parse_args()

    records = read_obstructions(args.obstructions)
    orders, vectors = order_data()
    rows = [
        "CERTIFICATE stable_transitivity_mu8_v1 n=8 classes=96 target=13/20",
        "# CLASS <source-index> tournament=<mask> dual=<edge-indices> primal=<order-index:num/den,...>",
    ]
    for number, (source_index, tournament) in enumerate(records, 1):
        dual, primal = solve_one(tournament, vectors)
        dual_text = ",".join(map(str, dual))
        primal_text = ",".join(
            f"{index}:{weight.numerator}/{weight.denominator}"
            for index, weight in primal
        )
        rows.append(
            f"CLASS {source_index} tournament={tournament} "
            f"dual={dual_text} primal={primal_text}"
        )
        print(f"generated {number}/96 class={source_index}", flush=True)
    args.output.write_text("\n".join(rows) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
