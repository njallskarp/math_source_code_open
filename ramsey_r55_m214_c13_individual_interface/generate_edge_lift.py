#!/usr/bin/env python3
"""Generate the exact outside-edge lift MILP for a fixed k=0 footprint selection."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path


N = 13
OUTSIDE = 28
FULL = (1 << N) - 1
A = tuple(range(0, 7))
B = tuple(range(7, 14))
O = tuple(range(14, 28))
DIFF = frozenset((1, 5, 8, 12))


def core_edge(i: int, j: int) -> bool:
    return i != j and (i - j) % N in DIFF


def edge_name(x: int, y: int) -> str:
    if x > y:
        x, y = y, x
    return f"e_{x:02d}_{y:02d}"


def independent_triples() -> tuple[int, ...]:
    return tuple(
        sum(1 << i for i in triple)
        for triple in itertools.combinations(range(N), 3)
        if all(not core_edge(i, j) for i, j in itertools.combinations(triple, 2))
    )


def generate(source: Path, destination: Path) -> dict[str, int | str]:
    data = json.loads(source.read_text(encoding="ascii"))
    expected = {"core_e", "footprints", "outside_e", "outside_red_edges", "pivot"}
    if not isinstance(data, dict) or set(data) != expected:
        raise ValueError("certificate fields")
    rows = tuple(int(text, 16) for text in data["footprints"])
    marked = frozenset(data["outside_e"])
    if data["core_e"] != [] or data["pivot"] != "D0" or len(rows) != OUTSIDE:
        raise ValueError("requires the canonical k=0,D0 selection")
    if marked != frozenset((*range(0, 6), *range(7, 13), 14)):
        raise ValueError("canonical outside marks")
    triples = independent_triples()
    core_edges = tuple(
        (1 << i) | (1 << j)
        for i, j in itertools.combinations(range(N), 2)
        if core_edge(i, j)
    )
    pairs = tuple(itertools.combinations(range(OUTSIDE), 2))

    def blue_forbidden(x: int, y: int) -> bool:
        missing = FULL ^ (rows[x] | rows[y])
        return any(missing & triple == triple for triple in triples)

    def red_forbidden(x: int, y: int) -> bool:
        same_cell = x < y < 7 or 7 <= x < y < 14
        common = rows[x] & rows[y]
        return same_cell and any(common & edge == edge for edge in core_edges)

    forced = tuple(pair for pair in pairs if blue_forbidden(*pair))
    forbidden = tuple(pair for pair in pairs if red_forbidden(*pair))
    if set(forced) & set(forbidden):
        raise AssertionError("no-color pair")

    temporary = destination.with_name(destination.name + ".partial")
    digest = hashlib.sha256()
    line_count = constraint_count = byte_count = 0
    with temporary.open("wb") as raw:
        def write(text: str) -> None:
            nonlocal line_count, byte_count
            encoded = text.encode("ascii")
            raw.write(encoded)
            digest.update(encoded)
            line_count += encoded.count(b"\n")
            byte_count += len(encoded)

        def equation(name: str, variables: list[str], target: int) -> None:
            nonlocal constraint_count
            if not variables:
                raise ValueError(name)
            write(f" {name}: " + " + ".join(variables) + f" = {target}\n")
            constraint_count += 1

        write("Minimize\n obj: + 0 e_00_01\nSubject To\n")
        for x in range(OUTSIDE):
            degree = 21 - int(x in marked) - int(x in A or x in B) - rows[x].bit_count()
            equation(
                f"degree_{x:02d}",
                [edge_name(x, y) for y in range(OUTSIDE) if y != x],
                degree,
            )
            e_degree = 6 + 2 * int(x == 0)
            equation(
                f"E_degree_{x:02d}",
                [edge_name(x, y) for y in sorted(marked) if y != x],
                e_degree,
            )
        a_pairs = tuple(itertools.combinations(A, 2))
        b_pairs = tuple(itertools.combinations(B, 2))
        o_pairs = tuple(itertools.combinations(O, 2))
        ao_pairs = tuple((x, y) for x in A for y in O)
        bo_pairs = tuple((x, y) for x in B for y in O)
        equation("anchor_red_A", [edge_name(*pair) for pair in a_pairs], 61 - sum(rows[x].bit_count() for x in A))
        equation("anchor_red_B", [edge_name(*pair) for pair in b_pairs], 61 - sum(rows[x].bit_count() for x in B))
        equation("anchor_blue_u", [edge_name(*pair) for pair in (*b_pairs, *o_pairs, *bo_pairs)], 110)
        equation("anchor_blue_v", [edge_name(*pair) for pair in (*a_pairs, *o_pairs, *ao_pairs)], 110)
        for x, y in forced:
            equation(f"force_{x:02d}_{y:02d}", [edge_name(x, y)], 1)
        for x, y in forbidden:
            equation(f"forbid_{x:02d}_{y:02d}", [edge_name(x, y)], 0)
        write("Binary\n")
        for x, y in pairs:
            write(" " + edge_name(x, y) + "\n")
        write("End\n")
        raw.flush()
        os.fsync(raw.fileno())
    os.replace(temporary, destination)
    return {
        "binary_variables": len(pairs),
        "bytes": byte_count,
        "constraints": constraint_count,
        "forbidden_red": len(forbidden),
        "forced_red": len(forced),
        "lines": line_count,
        "sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(generate(args.certificate, args.output), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
