#!/usr/bin/env python3
"""Emit and certify the 20-variable rational edge-parameter LP."""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction
from pathlib import Path


N = 43
NAMES = (
    "pA", "pB", "pO", "AA", "AB", "AO", "BB", "BO",
    "upA", "upB", "upO", "aA", "aB", "aO", "bA", "bB", "bO",
    "oA", "oB", "oO",
)
INDEX = {name: index for index, name in enumerate(NAMES)}
E = frozenset(range(2, 15))
H = frozenset(range(15, 28))
EA = frozenset(range(2, 8))
EB = frozenset(range(8, 14))
CS = frozenset((28, 29))
CO = frozenset(range(30, 43))
VERTEX_TYPE = {2: "p", 14: "o", 28: "ca", 29: "cb"}
VERTEX_TYPE.update({vertex: "a" for vertex in range(3, 8)})
VERTEX_TYPE.update({vertex: "b" for vertex in range(8, 14)})
VERTEX_TYPE.update({vertex: "h" for vertex in range(15, 28)})
VERTEX_TYPE.update({vertex: "co" for vertex in range(30, 43)})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def frac(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def expression(constant: Fraction = Fraction(0), **terms: int):
    coefficients = [0] * len(NAMES)
    for name, coefficient in terms.items():
        coefficients[INDEX[name]] = coefficient
    return constant, tuple(coefficients)


def red13(left: int, right: int) -> bool:
    return ((left - 15) - (right - 15)) % 13 in {1, 5, 8, 12}


def edge_expression(left: int, right: int):
    if left > right:
        left, right = right, left
    if (left, right) == (0, 1):
        return expression(Fraction(1))
    if left in (0, 1):
        if left == 0:
            return expression(Fraction(int(right in H or right in EA or right == 28)))
        return expression(Fraction(int(right in H or right in EB or right == 29)))
    if left in H and right in H:
        return expression(Fraction(int(red13(left, right))))
    if (left in H) != (right in H):
        exterior = right if left in H else left
        return expression(Fraction(6, 13) if exterior in E else Fraction(3, 5))
    if left in E and right in E:
        lt, rt = VERTEX_TYPE[left], VERTEX_TYPE[right]
        if "p" in (lt, rt):
            other = rt if lt == "p" else lt
            return expression(**{{"a": "pA", "b": "pB", "o": "pO"}[other]: 1})
        name = {
            ("a", "a"): "AA", ("a", "b"): "AB", ("a", "o"): "AO",
            ("b", "b"): "BB", ("b", "o"): "BO",
        }[tuple(sorted((lt, rt)))]
        return expression(**{name: 1})
    if (left in E) != (right in E):
        exceptional = left if left in E else right
        central = right if left in E else left
        row = {"p": "up", "a": "a", "b": "b", "o": "o"}[VERTEX_TYPE[exceptional]]
        column = {"ca": "A", "cb": "B", "co": "O"}[VERTEX_TYPE[central]]
        return expression(**{row + column: 1})
    lt, rt = VERTEX_TYPE[left], VERTEX_TYPE[right]
    ls, rs = lt in {"ca", "cb"}, rt in {"ca", "cb"}
    if ls and rs:
        return expression(Fraction(1))
    if ls != rs:
        return expression(Fraction(2, 5))
    return expression(Fraction(8, 15))


def add(left, right):
    return (
        left[0] + right[0],
        tuple(a + b for a, b in zip(left[1], right[1], strict=True)),
    )


def equations():
    rows = []
    def row(target: Fraction | int, **terms: int) -> None:
        rows.append((expression(**terms)[1], Fraction(target)))
    row(8, pA=5, pB=6, pO=1)
    row(6, pA=1, AA=4, AB=6, AO=1)
    row(6, pB=1, BB=5, AB=5, BO=1)
    row(6, pO=1, AO=5, BO=6)
    row(5, upA=1, upB=1, upO=13)
    row(7, aA=1, aB=1, aO=13)
    row(7, bA=1, bB=1, bO=13)
    row(8, oA=1, oB=1, oO=13)
    row(6, upA=1, aA=5, bA=6, oA=1)
    row(6, upB=1, aB=5, bB=6, oB=1)
    row(6, upO=1, aO=5, bO=6, oO=1)
    row(Fraction(86, 5), pA=5, AA=10, upA=1, aA=5)
    row(Fraction(86, 5), BB=15, bB=6)
    return rows


def five_set_expressions():
    unique = set()
    for vertices in itertools.combinations(range(N), 5):
        total = expression()
        for left, right in itertools.combinations(vertices, 2):
            total = add(total, edge_expression(left, right))
        unique.add(total)
    return tuple(sorted(unique))


def linear_text(coefficients, variables="z") -> str:
    terms = []
    for index, coefficient in enumerate(coefficients):
        if coefficient:
            terms.append(f" {coefficient:+d} {variables}{index}")
    return "".join(terms) or " 0"


def lp_text() -> str:
    lines = ["Minimize", " obj: 0 z0", "Subject To"]
    for index, (coefficients, target) in enumerate(equations()):
        lines.append(f" eq{index}:" + linear_text(coefficients) + f" = {frac(target)}")
    five_sets = five_set_expressions()
    for index, (constant, coefficients) in enumerate(five_sets):
        if not any(coefficients):
            require(1 <= constant <= 9, "constant five-set row")
            continue
        lines.append(f" red{index}:" + linear_text(coefficients) + f" >= {frac(1 - constant)}")
        lines.append(f" blue{index}:" + linear_text(coefficients) + f" <= {frac(9 - constant)}")
    lines.append("Bounds")
    lines.extend(f" 0 <= z{index} <= 1" for index in range(len(NAMES)))
    lines.extend(("End", ""))
    return "\n".join(lines)


def parse_solution(path: Path):
    values = [Fraction(0) for _ in NAMES]
    seen = set()
    for line in path.read_text(encoding="ascii").splitlines():
        if not line.startswith("z"):
            continue
        name, value = line.split()
        index = int(name[1:])
        require(0 <= index < len(NAMES) and index not in seen, "solution variable")
        seen.add(index)
        values[index] = Fraction(value)
    require(seen, "empty solution")
    require(all(0 <= value <= 1 for value in values), "solution bounds")
    for coefficients, target in equations():
        require(sum(Fraction(c) * v for c, v in zip(coefficients, values, strict=True)) == target,
                "solution equation")
    for constant, coefficients in five_set_expressions():
        total = constant + sum(Fraction(c) * v for c, v in zip(coefficients, values, strict=True))
        require(1 <= total <= 9, "solution five-set")
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lp", type=Path)
    parser.add_argument("--solution", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.lp is not None:
        args.lp.write_text(lp_text(), encoding="ascii")
        print(f"PASS variables={len(NAMES)} equations={len(equations())} five_set_rows={len(five_set_expressions())}")
        return
    require(args.solution is not None and args.output is not None, "give --lp or --solution and --output")
    values = parse_solution(args.solution)
    raw = "name\tvalue\n" + "".join(
        f"{name}\t{frac(value)}\n" for name, value in zip(NAMES, values, strict=True)
    )
    args.output.write_text(raw, encoding="ascii")
    print(f"PASS variables={len(NAMES)} bytes={len(raw.encode('ascii'))}")


if __name__ == "__main__":
    main()
