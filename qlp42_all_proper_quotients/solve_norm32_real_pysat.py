#!/usr/bin/env python3
"""Exact SAT model for the real Gray-component relaxation at norm 32."""

from __future__ import annotations

from argparse import ArgumentParser
from time import monotonic

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

N = 42
TARGET_RESIDUAL = [0] * N
for shift in (4, 11, 31, 38):
    TARGET_RESIDUAL[shift] = -2
for shift in (10, 17, 25, 32):
    TARGET_RESIDUAL[shift] = 2

# Closest deterministic heuristic state found in 20 restarts of 1,000,000
# moves each: squared real-equation residual 32.
HEURISTIC_A = "j1j-ij--ij1-1i1jji1j1--1--iii111jiiiij-jj-"
HEURISTIC_B = "1j--iij1-iiiji-1i1jj11-i11-j-jji11-1ji--1-"
BITS = {"1": (0, 0), "i": (0, 1), "-": (1, 1), "j": (1, 0)}


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--encoding",
        choices=("cardnetwrk", "totalizer", "kmtotalizer", "seqcounter"),
        default="kmtotalizer",
    )
    args = parser.parse_args()
    encodings = {
        "cardnetwrk": EncType.cardnetwrk,
        "totalizer": EncType.totalizer,
        "kmtotalizer": EncType.kmtotalizer,
        "seqcounter": EncType.seqcounter,
    }

    pool = IDPool()
    cnf = CNF()

    def variable(family: str, index: int) -> int:
        return pool.id(f"{family}_{index}")

    def add_equals(literals: list[int], bound: int) -> None:
        cnf.extend(
            CardEnc.equals(
                lits=literals,
                bound=bound,
                vpool=pool,
                encoding=encodings[args.encoding],
            ).clauses
        )

    def xor(left: int, right: int, name: str) -> int:
        result = pool.id(name)
        cnf.extend(
            [
                [left, right, -result],
                [left, -right, result],
                [-left, right, result],
                [-left, -right, -result],
            ]
        )
        return result

    families = {
        name: [variable(name, index) for index in range(N)]
        for name in ("au", "av", "bu", "bv")
    }
    for name, weight in (("au", 21), ("av", 21), ("bu", 20), ("bv", 21)):
        add_equals(families[name], weight)

    # Each binary autocorrelation is independently rotation invariant.  Every
    # component has at least one zero, so rotate it to put a zero at index 0.
    for family in families.values():
        cnf.append([-family[0]])

    for shift in range(1, N // 2 + 1):
        differences: list[int] = []
        for family_name, family in families.items():
            differences.extend(
                xor(
                    family[index],
                    family[(index + shift) % N],
                    f"d_{shift}_{family_name}_{index}",
                )
                for index in range(N)
            )
        # Re(PAF(A,s)+PAF(B,s)) = 84 - sum(differences).
        add_equals(differences, 86 - TARGET_RESIDUAL[shift])

    print(f"variables={pool.top}; clauses={len(cnf.clauses)}", flush=True)
    started = monotonic()
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        phases: list[int] = []
        for prefix, sequence in (("a", HEURISTIC_A), ("b", HEURISTIC_B)):
            for index, symbol in enumerate(sequence):
                for suffix, value in zip(("u", "v"), BITS[symbol]):
                    literal = families[prefix + suffix][index]
                    phases.append(literal if value else -literal)
        solver.set_phases(phases)
        satisfiable = solver.solve()
        print(
            f"status={'SAT' if satisfiable else 'UNSAT'}; "
            f"seconds={monotonic() - started:.6f}",
            flush=True,
        )
        if not satisfiable:
            return
        positive = {literal for literal in solver.get_model() if literal > 0}

    decoded: dict[str, list[int]] = {}
    for name, family in families.items():
        bits = [int(literal in positive) for literal in family]
        decoded[name] = bits
        print(f"{name}={''.join(map(str, bits))}")

    for shift in range(1, N):
        correlations = 0
        for bits in decoded.values():
            signs = [1 - 2 * bit for bit in bits]
            correlations += sum(
                signs[index] * signs[(index + shift) % N]
                for index in range(N)
            )
        assert correlations == 2 * (TARGET_RESIDUAL[shift] - 2)
    print("exact real autocorrelation verification passed")


if __name__ == "__main__":
    main()
