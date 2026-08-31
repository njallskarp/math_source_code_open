#!/usr/bin/env python3
"""Exact CNF search for all proper quotient constraints at QLP length 42.

Imposing quotient orders 6, 14, and 21 also imposes their coarsenings, hence
every nontrivial proper divisor of 42.  A SAT result is only a quotient-level
certificate, not a quaternary Legendre pair.
"""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from time import monotonic

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

N = 42
DIVISORS = (6, 14, 21)
SYMBOL = {
    (False, False): "1",
    (False, True): "i",
    (True, True): "-",
    (True, False): "j",
}
BITS = {symbol: bits for bits, symbol in SYMBOL.items()}
ROOT = {"1": 1 + 0j, "i": 1j, "-": -1 + 0j, "j": -1j}

# Best heuristic state from the independent C++ search (score 240).  These
# literals are preferences only and do not constrain the exact model.
NEAR_A = "1iji1jj-jj1i1-ijjj1ij1i1iii1i-j-i--j-i1-j-"
NEAR_B = "jji1---ij1i-ii1jjj---1j1ij1-iijji1i1i-11ji"


def quotient(sequence: str, divisor: int) -> list[complex]:
    return [
        sum(ROOT[sequence[index]] for index in range(residue, N, divisor))
        for residue in range(divisor)
    ]


def paf(sequence: list[complex]) -> list[complex]:
    length = len(sequence)
    return [
        sum(
            sequence[index] * sequence[(index + shift) % length].conjugate()
            for index in range(length)
        )
        for shift in range(length)
    ]


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--cnf", type=Path)
    args = parser.parse_args()

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
                encoding=EncType.cardnetwrk,
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

    # These four exact bit counts are equivalent to sum(A)=0, sum(B)=1+i.
    add_equals(families["au"], 21)
    add_equals(families["av"], 21)
    add_equals(families["bu"], 20)
    add_equals(families["bv"], 21)

    # Independent phase symmetry of A fixes A[0]=1.
    cnf.append([-families["au"][0]])
    cnf.append([-families["av"][0]])

    for divisor in DIVISORS:
        class_length = N // divisor
        term_count = 2 * N * class_length
        for shift in range(divisor // 2 + 1):
            pairs = [
                (left, right)
                for left in range(N)
                for right in range(N)
                if (right - left) % divisor == shift
            ]
            target = 86 - 2 * class_length if shift == 0 else -2 * class_length

            real_xors: list[int] = []
            for family_name in ("au", "av", "bu", "bv"):
                family = families[family_name]
                real_xors.extend(
                    xor(
                        family[left],
                        family[right],
                        f"r_{divisor}_{shift}_{family_name}_{left}_{right}",
                    )
                    for left, right in pairs
                )
            add_equals(real_xors, term_count - target)

            if shift == 0 or 2 * shift == divisor:
                continue
            plus: list[int] = []
            minus: list[int] = []
            for prefix in ("a", "b"):
                u = families[prefix + "u"]
                v = families[prefix + "v"]
                plus.extend(
                    xor(
                        u[left],
                        v[right],
                        f"ip_{divisor}_{shift}_{prefix}_{left}_{right}",
                    )
                    for left, right in pairs
                )
                minus.extend(
                    xor(
                        v[left],
                        u[right],
                        f"im_{divisor}_{shift}_{prefix}_{left}_{right}",
                    )
                    for left, right in pairs
                )
            add_equals(plus + [-literal for literal in minus], term_count)

    if args.cnf:
        cnf.to_file(args.cnf)
    print(f"variables={pool.top}; clauses={len(cnf.clauses)}; solver={args.solver}")

    started = monotonic()
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        preferred: list[int] = []
        for prefix, sequence in (("a", NEAR_A), ("b", NEAR_B)):
            for index, symbol in enumerate(sequence):
                for coordinate, value in zip(("u", "v"), BITS[symbol]):
                    literal = families[prefix + coordinate][index]
                    preferred.append(literal if value else -literal)
        solver.set_phases(preferred)
        satisfiable = solver.solve()
        print(f"status={'SAT' if satisfiable else 'UNSAT'}; seconds={monotonic()-started:.3f}")
        if not satisfiable:
            return
        positive = {literal for literal in solver.get_model() if literal > 0}

    def decode(prefix: str) -> str:
        return "".join(
            SYMBOL[
                (
                    families[prefix + "u"][index] in positive,
                    families[prefix + "v"][index] in positive,
                )
            ]
            for index in range(N)
        )

    a = decode("a")
    b = decode("b")
    print(f"A={a}")
    print(f"B={b}")
    assert sum(ROOT[symbol] for symbol in a) == 0
    assert sum(ROOT[symbol] for symbol in b) == 1 + 1j
    for divisor in (2, 3, 6, 7, 14, 21):
        qa = quotient(a, divisor)
        qb = quotient(b, divisor)
        combined = [left + right for left, right in zip(paf(qa), paf(qb))]
        class_length = N // divisor
        expected = [86 - 2 * class_length] + [-2 * class_length] * (divisor - 1)
        assert combined == expected, (divisor, combined, expected)
        print(f"d={divisor} combined={combined}")


if __name__ == "__main__":
    main()
