#!/usr/bin/env python3
"""Build the all-root missed-pair column-hull OPB strengthening."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path


N = 43
PHYSICAL = tuple(range(2, N))
EXCEPTIONAL = frozenset(range(2, 15))
CELLS = "HABO"
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")
PATTERNS = {
    "E8": ("H", "A"),
    "E77": ("BB", "BO", "OO"),
    "C8": ("B", "O"),
    "C77": ("BB", "BO", "OO"),
    "C77partition": ("HO", "AB"),
}

# Height-3274 exact pair-cell lift.
PRIOR_VARIABLES = 98_758
PRIOR_CONSTRAINTS = 2_969_925
PRIOR_EQUALITIES = 87
PRIOR_LINES = 2_969_926
PRIOR_BYTES = 451_842_281
PRIOR_SHA256 = "c0afe63fb47a3941481154addcbf383be134eeee0861afbd8451eb5eba19050c"
PRIOR_HEADER = b"* #variable= 98758 #constraint= 2969925 #equal= 87 intsize= 64\n"

SELECTOR_FIRST = 13_245
MISSED_FIRST = 13_634


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    require(0 <= i < j < N, "invalid physical edge")
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def root_keys():
    for family in FAMILIES:
        for common in range(9, 14):
            for exceptional_common in range(7):
                e_sizes = (
                    exceptional_common,
                    6 - exceptional_common,
                    6 - exceptional_common,
                    1 + exceptional_common,
                )
                c_sizes = (
                    common - exceptional_common,
                    14 - common + exceptional_common,
                    14 - common + exceptional_common,
                    common - exceptional_common,
                )
                sizes = e_sizes if family.startswith("E") else c_sizes
                for pattern in PATTERNS[family]:
                    if all(
                        pattern.count(cell) <= sizes[index]
                        for index, cell in enumerate(CELLS)
                    ):
                        yield family, common, exceptional_common, pattern


ROOT_KEYS = tuple(root_keys())


def root_cells(key: tuple[str, int, int, str]) -> tuple[tuple[int, ...], ...]:
    _, common, exceptional_common, _ = key
    sizes = (
        exceptional_common,
        6 - exceptional_common,
        6 - exceptional_common,
        1 + exceptional_common,
        common - exceptional_common,
        14 - common + exceptional_common,
        14 - common + exceptional_common,
        common - exceptional_common,
    )
    cells = []
    cursor = 2
    for size in sizes:
        require(size >= 0, "negative root-cell size")
        cells.append(tuple(range(cursor, cursor + size)))
        cursor += size
    require(cursor == N, "root cells do not partition the physical vertices")
    return tuple(cells)


def root_data(key: tuple[str, int, int, str]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    cells = root_cells(key)
    core = cells[0] + cells[4]
    core_set = frozenset(core)
    exterior = tuple(vertex for vertex in PHYSICAL if vertex not in core_set)
    require(len(core) == key[1] and len(exterior) == 41 - key[1], "root orders")
    return core, exterior


def missed_support() -> tuple[tuple[int, int, int], ...]:
    support: set[tuple[int, int, int]] = set()
    for key in ROOT_KEYS:
        core, exterior = root_data(key)
        for left, right in itertools.combinations(exterior, 2):
            support.update((left, right, vertex) for vertex in core)
    return tuple(sorted(support))


MISSED_KEYS = missed_support()
MISSED_IDS = {key: MISSED_FIRST + index for index, key in enumerate(MISSED_KEYS)}


def opb_row(terms: list[tuple[int, int]], rhs: int) -> str:
    require(terms, "empty OPB row")
    return " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in terms) + f" >= {rhs} ;"


def hull_parameters(common: int, exceptional: bool) -> tuple[int, int, int, tuple[int, ...]]:
    degree = 20 if exceptional else 21
    exterior_order = 41 - common
    shift = exterior_order - degree + 2
    degree_lower = common - 9
    degree_upper = 4
    missed_lower = shift + degree_lower
    missed_upper = shift + degree_upper
    tangents = tuple(range(missed_lower, missed_upper))
    if not tangents:
        tangents = (missed_lower,)
    require(missed_lower == (14 if exceptional else 13), "unexpected missed lower bound")
    require(missed_lower <= missed_upper, "empty core-degree interval")
    return shift, missed_lower, missed_upper, tangents


def root_lines():
    for root_index, key in enumerate(ROOT_KEYS):
        common = key[1]
        core, exterior = root_data(key)
        selector = SELECTOR_FIRST + root_index
        pair_count = len(exterior) * (len(exterior) - 1) // 2
        for vertex in core:
            internal_edges = [edge_id(vertex, other) for other in core if other != vertex]
            missed = [
                MISSED_IDS[left, right, vertex]
                for left, right in itertools.combinations(exterior, 2)
            ]
            require(len(internal_edges) == common - 1 and len(missed) == pair_count, "row support")
            shift, lower, upper, tangents = hull_parameters(
                common, vertex in EXCEPTIONAL
            )

            # Lower convex-envelope facets of M = binom(shift+a,2).
            for tangent in tangents:
                rhs_active = tangent * shift - tangent * (tangent + 1) // 2
                guard = rhs_active + tangent * (common - 1)
                yield opb_row(
                    [(1, variable) for variable in missed]
                    + [(-tangent, variable) for variable in internal_edges]
                    + [(-guard, selector)],
                    -tangent * (common - 1),
                )

            # Upper chord through the two endpoint values.
            slope_twice = lower + upper - 1
            rhs_active = lower * upper - slope_twice * shift
            guard = rhs_active + 2 * pair_count
            yield opb_row(
                [(-2, variable) for variable in missed]
                + [(slope_twice, variable) for variable in internal_edges]
                + [(-guard, selector)],
                -2 * pair_count,
            )


ROWS_BY_C = {
    common: common * (len(hull_parameters(common, False)[3]) + 1)
    for common in range(9, 14)
}
ROOT_COUNTS = Counter(key[1] for key in ROOT_KEYS)
SUFFIX_ROWS = sum(ROOT_COUNTS[common] * ROWS_BY_C[common] for common in range(9, 14))
CONSTRAINTS = PRIOR_CONSTRAINTS + SUFFIX_ROWS
HEADER = (
    f"* #variable= {PRIOR_VARIABLES} #constraint= {CONSTRAINTS} "
    f"#equal= {PRIOR_EQUALITIES} intsize= 64\n"
).encode("ascii")


def key_hash(keys: tuple[tuple[int, ...], ...]) -> str:
    raw = "".join(",".join(map(str, key)) + "\n" for key in keys).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def root_certificate() -> bytes:
    lines = [
        "index\tfamily\tc\tk\tpattern\tselector\tH\texterior\tE_columns"
        "\tC_columns\trows"
    ]
    for root_index, key in enumerate(ROOT_KEYS):
        core, exterior = root_data(key)
        exceptional_columns = sum(vertex in EXCEPTIONAL for vertex in core)
        row_count = sum(
            len(hull_parameters(key[1], vertex in EXCEPTIONAL)[3]) + 1
            for vertex in core
        )
        require(exceptional_columns == key[2], "exceptional-core count")
        lines.append(
            "\t".join(
                (
                    str(root_index),
                    key[0],
                    str(key[1]),
                    str(key[2]),
                    key[3],
                    str(SELECTOR_FIRST + root_index),
                    ",".join(map(str, core)),
                    str(len(exterior)),
                    str(exceptional_columns),
                    str(key[1] - exceptional_columns),
                    str(row_count),
                )
            )
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def write_atomic(path: Path, chunks) -> tuple[int, int, str]:
    destination = path.resolve()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    digest = hashlib.sha256()
    byte_count = 0
    line_count = 0
    try:
        with temporary.open("wb") as handle:
            for chunk in chunks:
                raw = chunk if isinstance(chunk, bytes) else chunk.encode("ascii")
                handle.write(raw)
                digest.update(raw)
                byte_count += len(raw)
                line_count += raw.count(b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    return byte_count, line_count, digest.hexdigest()


def file_identity(path: Path) -> tuple[int, int, str]:
    digest = hashlib.sha256()
    byte_count = 0
    line_count = 0
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
            byte_count += len(block)
            line_count += block.count(b"\n")
    return byte_count, line_count, digest.hexdigest()


def formula_chunks(prior_path: Path, suffix_path: Path):
    with prior_path.open("rb") as prior:
        require(prior.readline() == PRIOR_HEADER, "prior header")
        yield HEADER
        while block := prior.read(1 << 20):
            yield block
    with suffix_path.open("rb") as suffix:
        while block := suffix.read(1 << 20):
            yield block


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--suffix", type=Path, required=True)
    parser.add_argument("--prior-opb", type=Path)
    parser.add_argument("--output-opb", type=Path)
    args = parser.parse_args()
    require((args.prior_opb is None) == (args.output_opb is None), "full formula arguments")

    certificate_stats = write_atomic(args.certificate, (root_certificate(),))
    suffix_stats = write_atomic(args.suffix, (line + "\n" for line in root_lines()))
    require(certificate_stats[1] == len(ROOT_KEYS) + 1, "certificate line count")
    require(suffix_stats[1] == SUFFIX_ROWS, "suffix line count")
    result: dict[str, object] = {
        "certificate_bytes": certificate_stats[0],
        "certificate_sha256": certificate_stats[2],
        "constraints": CONSTRAINTS,
        "missed_keys": len(MISSED_KEYS),
        "missed_keys_sha256": key_hash(MISSED_KEYS),
        "root_counts_by_c": [ROOT_COUNTS[common] for common in range(9, 14)],
        "rows_by_root_c": [ROWS_BY_C[common] for common in range(9, 14)],
        "roots": len(ROOT_KEYS),
        "suffix_bytes": suffix_stats[0],
        "suffix_rows": suffix_stats[1],
        "suffix_sha256": suffix_stats[2],
        "variables": PRIOR_VARIABLES,
    }
    if args.prior_opb is not None and args.output_opb is not None:
        require(
            file_identity(args.prior_opb) == (PRIOR_BYTES, PRIOR_LINES, PRIOR_SHA256),
            "prior identity",
        )
        formula_stats = write_atomic(
            args.output_opb, formula_chunks(args.prior_opb, args.suffix)
        )
        require(formula_stats[1] == CONSTRAINTS + 1, "formula line count")
        result["formula"] = {
            "bytes": formula_stats[0],
            "constraints": CONSTRAINTS,
            "equalities": PRIOR_EQUALITIES,
            "lines": formula_stats[1],
            "sha256": formula_stats[2],
            "variables": PRIOR_VARIABLES,
        }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
