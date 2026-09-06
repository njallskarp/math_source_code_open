#!/usr/bin/env python3
"""Derive the exact orbit certificate for the strict LP witness.

This script emits the 171-variable orbit LP and converts a rational SoPlex
solution into the compact certificate.  The certificate is checked directly
by verify_fractional.py and the independent C++ checker; the solver is not
part of the verification trust boundary.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter
from fractions import Fraction
from pathlib import Path

N = 43
TYPE_ORDER = ("u", "v", "p", "a", "b", "o", "h", "ca", "cb", "co")
TYPE_INDEX = {name: index for index, name in enumerate(TYPE_ORDER)}
VERTEX_TYPE = {0: "u", 1: "v", 2: "p", 14: "o", 28: "ca", 29: "cb"}
VERTEX_TYPE.update({vertex: "a" for vertex in range(3, 8)})
VERTEX_TYPE.update({vertex: "b" for vertex in range(8, 14)})
VERTEX_TYPE.update({vertex: "h" for vertex in range(15, 28)})
VERTEX_TYPE.update({vertex: "co" for vertex in range(30, 43)})
TYPE_SIZES = Counter(VERTEX_TYPE.values())

E = frozenset(range(2, 15))
H = frozenset(range(15, 28))
EA = frozenset(range(2, 8))
EB = frozenset(range(8, 14))
CS = frozenset((28, 29))
CO = frozenset(range(30, 43))

EDGE_PARAMETERS = {
    "pA": Fraction(5, 6),
    "pB": Fraction(23, 36),
    "pO": Fraction(0),
    "AA": Fraction(5, 6),
    "AB": Fraction(17, 90),
    "AO": Fraction(7, 10),
    "BB": Fraction(4, 5),
    "BO": Fraction(5, 12),
    "upA": Fraction(8, 15),
    "upB": Fraction(0),
    "upO": Fraction(67, 195),
    "aA": Fraction(5, 6),
    "aB": Fraction(4, 25),
    "aO": Fraction(901, 1950),
    "bA": Fraction(13, 60),
    "bB": Fraction(13, 15),
    "bO": Fraction(71, 156),
    "oA": Fraction(0),
    "oB": Fraction(0),
    "oO": Fraction(8, 13),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def red13(left: int, right: int) -> bool:
    return ((left - 15) - (right - 15)) % 13 in {1, 5, 8, 12}


def edge_value(left: int, right: int) -> Fraction:
    if left > right:
        left, right = right, left
    require(0 <= left < right < N, "invalid edge")
    if (left, right) == (0, 1):
        return Fraction(1)
    if left in (0, 1):
        if left == 0:
            return Fraction(int(right in H or right in EA or right == 28))
        return Fraction(int(right in H or right in EB or right == 29))
    if left in H and right in H:
        return Fraction(int(red13(left, right)))
    if (left in H) != (right in H):
        exterior = right if left in H else left
        return Fraction(6, 13) if exterior in E else Fraction(3, 5)
    if left in E and right in E:
        left_type, right_type = VERTEX_TYPE[left], VERTEX_TYPE[right]
        if "p" in (left_type, right_type):
            other = right_type if left_type == "p" else left_type
            return EDGE_PARAMETERS[{"a": "pA", "b": "pB", "o": "pO"}[other]]
        key = {
            ("a", "a"): "AA",
            ("a", "b"): "AB",
            ("a", "o"): "AO",
            ("b", "b"): "BB",
            ("b", "o"): "BO",
        }[tuple(sorted((left_type, right_type)))]
        return EDGE_PARAMETERS[key]
    if (left in E) != (right in E):
        exceptional = left if left in E else right
        central = right if left in E else left
        row = {"p": "up", "a": "a", "b": "b", "o": "o"}[
            VERTEX_TYPE[exceptional]
        ]
        column = {"ca": "A", "cb": "B", "co": "O"}[VERTEX_TYPE[central]]
        return EDGE_PARAMETERS[row + column]
    left_type, right_type = VERTEX_TYPE[left], VERTEX_TYPE[right]
    left_special = left_type in {"ca", "cb"}
    right_special = right_type in {"ca", "cb"}
    if left_special and right_special:
        return Fraction(1)
    if left_special != right_special:
        return Fraction(2, 5)
    return Fraction(8, 15)


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def signature(triple: tuple[int, int, int]) -> tuple[tuple[str, ...], tuple[Fraction, ...]]:
    types = tuple(sorted((VERTEX_TYPE[v] for v in triple), key=TYPE_INDEX.__getitem__))
    edges = tuple(sorted(edge_value(i, j) for i, j in itertools.combinations(triple, 2)))
    return types, edges


def signature_text(sig: tuple[tuple[str, ...], tuple[Fraction, ...]]) -> str:
    types, edges = sig
    return ",".join(types) + "|" + ",".join(fraction_text(value) for value in edges)


def orbit_table():
    groups: dict[
        tuple[tuple[str, ...], tuple[Fraction, ...]],
        tuple[int, Counter[str], Fraction, Fraction],
    ] = {}
    for triple in itertools.combinations(range(N), 3):
        sig = signature(triple)
        values = sig[1]
        lower = max(Fraction(0), sum(values, Fraction(0)) - 2)
        upper = min(values)
        if sig not in groups:
            groups[sig] = (0, Counter(), lower, upper)
        count, occurrences, old_lower, old_upper = groups[sig]
        require((lower, upper) == (old_lower, old_upper), "signature changes bounds")
        updated = occurrences.copy()
        updated.update(VERTEX_TYPE[v] for v in triple)
        groups[sig] = (count + 1, updated, lower, upper)

    result = []
    for sig in sorted(groups, key=signature_text):
        count, occurrences, lower, upper = groups[sig]
        incidence = []
        for name in TYPE_ORDER:
            require(occurrences[name] % TYPE_SIZES[name] == 0, "nonuniform orbit incidence")
            incidence.append(occurrences[name] // TYPE_SIZES[name])
        result.append((sig, count, tuple(incidence), lower, upper))
    return result


def parse_solution(path: Path, orbits) -> list[Fraction]:
    values = [Fraction(0) for _ in orbits]
    seen: set[int] = set()
    for line in path.read_text(encoding="ascii").splitlines():
        if not line.startswith("z"):
            continue
        name, value = line.split()
        index = int(name[1:])
        require(0 <= index < len(orbits), "solution variable index")
        require(index not in seen, "duplicate solution variable")
        seen.add(index)
        values[index] = Fraction(value)
    require(seen, "empty solution")
    targets = [93 if name in {"p", "a", "b", "o"} else 100 for name in TYPE_ORDER]
    for index, (value, orbit) in enumerate(zip(values, orbits, strict=True)):
        require(orbit[3] <= value <= orbit[4], f"orbit bound {index}")
    for i, target in enumerate(targets):
        observed = sum(
            Fraction(orbits[j][2][i]) * values[j] for j in range(len(orbits))
        )
        require(observed == target, f"triangle target {TYPE_ORDER[i]}: {observed}")
    return values


def certificate(orbits, values) -> bytes:
    lines = ["signature\ttriples\tlower\tupper\tz"]
    for orbit, value in zip(orbits, values, strict=True):
        sig, count, _, lower, upper = orbit
        lines.append(
            "\t".join(
                (
                    signature_text(sig),
                    str(count),
                    fraction_text(lower),
                    fraction_text(upper),
                    fraction_text(value),
                )
            )
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def lp_text(orbits) -> str:
    lines = ["Minimize", " obj: 0 z0", "Subject To"]
    for type_index, name in enumerate(TYPE_ORDER):
        terms = []
        for orbit_index, orbit in enumerate(orbits):
            coefficient = orbit[2][type_index]
            if coefficient:
                terms.append(f" + {coefficient} z{orbit_index}")
        target = 93 if name in {"p", "a", "b", "o"} else 100
        lines.append(f" type_{name}:" + "".join(terms) + f" = {target}")
    lines.append("Bounds")
    for orbit_index, orbit in enumerate(orbits):
        lines.append(
            f" {fraction_text(orbit[3])} <= z{orbit_index} <= {fraction_text(orbit[4])}"
        )
    lines.extend(("End", ""))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--lp", type=Path)
    parser.add_argument("--solution", type=Path)
    args = parser.parse_args()
    orbits = orbit_table()
    if args.lp is not None:
        args.lp.write_text(lp_text(orbits), encoding="ascii")
        print(f"PASS triangle_orbits={len(orbits)} lp={args.lp}")
        return
    require(args.output is not None and args.solution is not None, "give --output and --solution")
    values = parse_solution(args.solution, orbits)
    raw = certificate(orbits, values)
    args.output.write_bytes(raw)
    print(
        f"PASS triangle_orbits={len(orbits)} nonzero_z={sum(value != 0 for value in values)} "
        f"bytes={len(raw)}"
    )


if __name__ == "__main__":
    main()
