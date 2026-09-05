#!/usr/bin/env python3
"""Generate the all-marking aggregate footprint MILP for M=214,c=13."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path


CORE_ORDER = 13
DIFFERENCES = frozenset((1, 5, 8, 12))
CELLS = ("A", "B", "O")
CELL_SIZES = {"A": 7, "B": 7, "O": 14}
ANCHOR_RED = {"A": 1, "B": 1, "O": 0}


def core_edge(i: int, j: int) -> bool:
    return i != j and ((i - j) % CORE_ORDER) in DIFFERENCES


def independent_fours() -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in subset)
        for subset in itertools.combinations(range(CORE_ORDER), 4)
        if all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2))
    )


def transversals() -> tuple[int, ...]:
    fours = independent_fours()
    result = tuple(mask for mask in range(1 << CORE_ORDER) if all(mask & four for four in fours))
    if len(fours) != 39 or len(result) != 3459:
        raise AssertionError((len(fours), len(result)))
    return result


def row_name(cell: str, marked: int, mask: int) -> str:
    return f"n_{cell}_{marked}_{mask:04x}"


def signed_term(coefficient: int, variable: str) -> str:
    sign = "+" if coefficient >= 0 else "-"
    magnitude = abs(coefficient)
    return f" {sign} {variable}" if magnitude == 1 else f" {sign} {magnitude} {variable}"


class LPWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.temporary = path.with_name(path.name + ".partial")
        self.raw = self.temporary.open("wb")
        self.digest = hashlib.sha256()
        self.bytes = 0
        self.lines = 0
        self.constraints = 0

    def write(self, text: str) -> None:
        data = text.encode("ascii")
        self.raw.write(data)
        self.digest.update(data)
        self.bytes += len(data)
        self.lines += data.count(b"\n")

    def constraint(self, name: str, terms: list[tuple[int, str]], relation: str, rhs: int) -> None:
        kept = [(coefficient, variable) for coefficient, variable in terms if coefficient]
        if not kept:
            raise ValueError(name)
        self.write(f" {name}:")
        for index, (coefficient, variable) in enumerate(kept):
            if index and index % 8 == 0:
                self.write("\n  ")
            self.write(signed_term(coefficient, variable))
        self.write(f" {relation} {rhs}\n")
        self.constraints += 1

    def finish(self) -> str:
        self.raw.flush()
        os.fsync(self.raw.fileno())
        self.raw.close()
        os.replace(self.temporary, self.path)
        return self.digest.hexdigest()


def generate(destination: Path) -> dict[str, int | str]:
    masks = transversals()
    rows = tuple(
        (cell, marked, mask, row_name(cell, marked, mask))
        for cell in CELLS
        for marked in (0, 1)
        for mask in masks
    )
    writer = LPWriter(destination)
    try:
        writer.write("\\ all-marking M=214,c=13 aggregate footprint relaxation\n")
        writer.write("Minimize\n obj: + k\nSubject To\n")

        for cell in CELLS:
            marked_terms = [(1, name) for c, marked, _, name in rows if c == cell and marked == 1]
            unmarked_terms = [(1, name) for c, marked, _, name in rows if c == cell and marked == 0]
            if cell in ("A", "B"):
                writer.constraint(f"count_{cell}_marked", marked_terms + [(1, "k")], "=", 6)
                writer.constraint(f"count_{cell}_unmarked", unmarked_terms + [(-1, "k")], "=", 1)
            else:
                writer.constraint("count_O_marked", marked_terms + [(-1, "k")], "=", 1)
                writer.constraint("count_O_unmarked", unmarked_terms + [(1, "k")], "=", 13)

        writer.constraint(
            "core_mark_count",
            [(1, "k")] + [(-1, f"e_{index}") for index in range(CORE_ORDER)],
            "=",
            0,
        )
        writer.constraint(
            "pivot_location",
            [(1, "p_A")] + [(1, f"p_{index}") for index in range(CORE_ORDER)],
            "=",
            1,
        )
        for index in range(CORE_ORDER):
            writer.constraint(f"pivot_mark_{index}", [(1, f"p_{index}"), (-1, f"e_{index}")], "<=", 0)
        writer.constraint("outside_pivot_exists", [(1, "p_A"), (1, "k")], "<=", 6)

        for index in range(CORE_ORDER):
            terms = [
                (1, name)
                for _, _, mask, name in rows
                if mask >> index & 1
            ]
            terms.append((1, f"e_{index}"))
            writer.constraint(f"column_total_{index}", terms, "=", 15)

        for index in range(CORE_ORDER):
            terms = [
                (1, name)
                for _, marked, mask, name in rows
                if marked and mask >> index & 1
            ]
            terms.extend((1, f"e_{neighbor}") for neighbor in range(CORE_ORDER) if core_edge(index, neighbor))
            terms.append((-2, f"p_{index}"))
            writer.constraint(f"column_marked_{index}", terms, "=", 6)

        for cell in ("A", "B"):
            incidence_terms = [
                (-mask.bit_count(), name)
                for c, _, mask, name in rows
                if c == cell
            ]
            writer.constraint(f"incidence_{cell}", [(1, f"i_{cell}")] + incidence_terms, "=", 0)
            writer.constraint(f"anchor_red_{cell}", [(1, f"m_{cell}"), (1, f"i_{cell}")], "=", 61)

        writer.constraint("anchor_blue_u", [(1, "m_B"), (1, "m_O"), (1, "m_BO")], "=", 110)
        writer.constraint("anchor_blue_v", [(1, "m_A"), (1, "m_O"), (1, "m_AO")], "=", 110)

        # Every induced subgraph is both K5-free and independent-5-free.  The
        # complementary Turan bounds are 3..18 on 7 vertices, 18..73 on 14,
        # and 84..294 on 28.  The red-neighborhood K4 condition sharpens the
        # 7-vertex upper bounds to 16 below.
        writer.constraint("AB_turan_lower", [(1, "m_A"), (1, "m_B"), (1, "m_AB")], ">=", 18)
        writer.constraint("AB_turan_upper", [(1, "m_A"), (1, "m_B"), (1, "m_AB")], "<=", 73)
        all_d_edges = [
            (1, variable)
            for variable in ("m_A", "m_B", "m_O", "m_AB", "m_AO", "m_BO")
        ]
        writer.constraint("D_turan_lower", all_d_edges, ">=", 84)
        writer.constraint("D_turan_upper", all_d_edges, "<=", 294)

        for cell in CELLS:
            degree_terms = []
            for c, marked, mask, name in rows:
                if c == cell:
                    required = 21 - marked - ANCHOR_RED[cell] - mask.bit_count()
                    degree_terms.append((-required, name))
            writer.constraint(f"degree_sum_{cell}", [(1, f"d_{cell}")] + degree_terms, "=", 0)
            if cell == "A":
                edge_terms = [(1, "d_A"), (-2, "m_A"), (-1, "m_AB"), (-1, "m_AO")]
            elif cell == "B":
                edge_terms = [(1, "d_B"), (-2, "m_B"), (-1, "m_AB"), (-1, "m_BO")]
            else:
                edge_terms = [(1, "d_O"), (-2, "m_O"), (-1, "m_AO"), (-1, "m_BO")]
            writer.constraint(f"cell_degree_{cell}", edge_terms, "=", 0)

        writer.write("Bounds\n")
        writer.write(" 0 <= k <= 6\n")
        bounds = {
            "i_A": (0, 91),
            "i_B": (0, 91),
            "d_A": (0, 189),
            "d_B": (0, 189),
            "d_O": (0, 378),
            # A and B lie in red neighborhoods, so their induced red graphs
            # are K4-free.  Turan's theorem gives ex(7,K4)=16.
            "m_A": (3, 16),
            "m_B": (3, 16),
            "m_O": (18, 73),
            "m_AB": (0, 49),
            "m_AO": (0, 98),
            "m_BO": (0, 98),
        }
        for variable, (lower, upper) in bounds.items():
            writer.write(f" {lower} <= {variable} <= {upper}\n")
        for cell, _, _, name in rows:
            writer.write(f" 0 <= {name} <= {CELL_SIZES[cell]}\n")

        writer.write("Binary\n")
        for index in range(CORE_ORDER):
            writer.write(f" e_{index}\n")
        for index in range(CORE_ORDER):
            writer.write(f" p_{index}\n")
        writer.write(" p_A\n")

        writer.write("General\n k\n")
        for variable in bounds:
            writer.write(f" {variable}\n")
        for _, _, _, name in rows:
            writer.write(f" {name}\n")
        writer.write("End\n")
        digest = writer.finish()
    except BaseException:
        if not writer.raw.closed:
            writer.raw.close()
        if writer.temporary.exists():
            writer.temporary.unlink()
        raise

    return {
        "binary_variables": 27,
        "bytes": writer.bytes,
        "constraints": writer.constraints,
        "integer_variables": 1 + 11 + len(rows),
        "lines": writer.lines,
        "row_variables": len(rows),
        "sha256": digest,
        "transversal_masks": len(masks),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(generate(args.output.resolve()), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
