#!/usr/bin/env python3
"""Exact SAT test for the six coefficientwise-even norm-32 residuals."""

from __future__ import annotations

from argparse import ArgumentParser
from time import monotonic

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from verify_half_compression import REPRESENTATIVES

N = 42
PROPER_FACTOR = [0] * 31
for exponent, coefficient in {
    0: -1,
    1: 1,
    2: -1,
    7: -1,
    8: 1,
    9: -1,
    21: 1,
    22: -1,
    23: 1,
    28: 1,
    29: -1,
    30: 1,
}.items():
    PROPER_FACTOR[exponent] = coefficient

# The three norm-32 vectors up to global sign in the real five-dimensional
# block, in coordinates Re(G_1),...,Re(G_5).
SHORTEST_PARAMETERS = (
    (0, 0, 0, 1, 1),
    (0, 1, 1, 0, 0),
    (1, 1, 0, -1, -1),
)

SYMBOL = {
    (False, False): "1",
    (False, True): "i",
    (True, True): "-",
    (True, False): "j",
}
ROOT = {"1": 1 + 0j, "i": 1j, "-": -1 + 0j, "j": -1j}


def convolve(left: list[complex | int], right: list[complex | int]) -> list[complex]:
    result = [0j] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def residual(parameters: tuple[int, ...], sign: int) -> list[int]:
    g = [0j] * 12
    for index, value in enumerate(parameters, start=1):
        g[index] = value
        g[12 - index] = -value
    values = [2 * sign * coefficient for coefficient in convolve(PROPER_FACTOR, g)]
    assert all(value.imag == 0 for value in values)
    result = [int(value.real) for value in values]
    assert sum(value * value for value in result) == 32
    return result


def paf(sequence: str) -> list[complex]:
    return [
        sum(
            ROOT[sequence[index]] * ROOT[sequence[(index + shift) % N]].conjugate()
            for index in range(N)
        )
        for shift in range(N)
    ]


def solve_target(
    parameters: tuple[int, ...],
    sign: int,
    solver_name: str,
    encoding: int,
    compression_case: int | None,
) -> bool:
    target_residual = residual(parameters, sign)
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
                encoding=encoding,
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
    add_equals(families["au"], 21)
    add_equals(families["av"], 21)
    add_equals(families["bu"], 20)
    add_equals(families["bv"], 21)

    if compression_case is None:
        # Use A's free phase to normalize A_0=1.  When a canonical half
        # compression is selected below, that same phase freedom was already
        # spent in the six-orbit reduction and must not be fixed again.
        cnf.append([-families["au"][0]])
        cnf.append([-families["av"][0]])
    else:
        p, q, x, y = REPRESENTATIVES[compression_case]
        even = list(range(0, N, 2))
        add_equals([families["au"][index] for index in even], (21 - p - q) // 2)
        add_equals([families["av"][index] for index in even], (21 - p + q) // 2)
        add_equals([families["bu"][index] for index in even], (21 - x - y) // 2)
        add_equals([families["bv"][index] for index in even], (21 - x + y) // 2)

    for shift in range(1, N // 2 + 1):
        real_xors: list[int] = []
        for family_name in ("au", "av", "bu", "bv"):
            family = families[family_name]
            real_xors.extend(
                xor(
                    family[index],
                    family[(index + shift) % N],
                    f"r_{shift}_{family_name}_{index}",
                )
                for index in range(N)
            )
        target_real = target_residual[shift] - 2
        add_equals(real_xors, 84 - target_real)

        if shift == N // 2:
            continue
        plus: list[int] = []
        minus: list[int] = []
        for prefix in ("a", "b"):
            u = families[prefix + "u"]
            v = families[prefix + "v"]
            plus.extend(
                xor(
                    u[index],
                    v[(index + shift) % N],
                    f"ip_{shift}_{prefix}_{index}",
                )
                for index in range(N)
            )
            minus.extend(
                xor(
                    v[index],
                    u[(index + shift) % N],
                    f"im_{shift}_{prefix}_{index}",
                )
                for index in range(N)
            )
        add_equals(plus + [-literal for literal in minus], 84)

    label = "_".join(map(str, parameters)) + ("_plus" if sign > 0 else "_minus")
    if compression_case is not None:
        label += f"_compression_{compression_case}"
    print(
        f"target={label}; variables={pool.top}; clauses={len(cnf.clauses)}",
        flush=True,
    )
    started = monotonic()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
        print(
            f"target={label}; status={'SAT' if satisfiable else 'UNSAT'}; "
            f"seconds={monotonic()-started:.3f}",
            flush=True,
        )
        if not satisfiable:
            return False
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
    combined = [left + right for left, right in zip(paf(a), paf(b))]
    assert sum(ROOT[symbol] for symbol in a) == 0
    assert sum(ROOT[symbol] for symbol in b) == 1 + 1j
    assert all(
        combined[shift] == target_residual[shift] - 2
        for shift in range(1, N)
    )
    print(f"A={a}\nB={b}")
    return True


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--encoding",
        choices=("cardnetwrk", "totalizer", "kmtotalizer", "seqcounter"),
        default="cardnetwrk",
    )
    parser.add_argument("--all", action="store_true")
    parser.add_argument(
        "--compression-case",
        type=int,
        choices=range(len(REPRESENTATIVES)),
        help="select one of the six symmetry-reduced modulo-two compressions",
    )
    args = parser.parse_args()
    encodings = {
        "cardnetwrk": EncType.cardnetwrk,
        "totalizer": EncType.totalizer,
        "kmtotalizer": EncType.kmtotalizer,
        "seqcounter": EncType.seqcounter,
    }
    satisfiable_targets = 0
    targets = (
        [(parameters, sign) for parameters in SHORTEST_PARAMETERS for sign in (1, -1)]
        if args.all
        else [(SHORTEST_PARAMETERS[0], 1)]
    )
    for parameters, sign in targets:
        satisfiable_targets += solve_target(
            parameters,
            sign,
            args.solver,
            encodings[args.encoding],
            args.compression_case,
        )
    print(
        f"satisfiable_targets={satisfiable_targets}; total_targets={len(targets)}"
    )


if __name__ == "__main__":
    main()
