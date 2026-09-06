#!/usr/bin/env python3
"""Build the all-codegree common-core footprint certificate and OPB suffix."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path


N = 43
CELLS = "HABO"
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")
PATTERNS = {
    "E8": ("H", "A"),
    "E77": ("BB", "BO", "OO"),
    "C8": ("B", "O"),
    "C77": ("BB", "BO", "OO"),
    "C77partition": ("HO", "AB"),
}
SELECTOR_FIRST = 13_245

# The independently accepted height-3160 integrated formula to which this
# suffix applies.  Height 3192 is compatible but is deliberately not a premise.
PRIOR_SHA256 = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
PRIOR_HEADER = b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n"
PRIOR_BYTES = 172_788_992
PRIOR_LINES = 2_044_422
PRIOR_VARIABLES = 13_633
PRIOR_CONSTRAINTS = 2_044_421
PRIOR_EQUALITIES = 87

# Cyclic (3,5;13) graph: ij is red iff i-j is in this set modulo 13.
CYCLIC_DIFFERENCES = frozenset((1, 5, 8, 12))
SHARP_T = (0, 1, 2, 3, 4, 5, 8, 9)
SHARP_EXTRAS = (6, 7, 10, 11, 12)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def root_keys():
    """Enumerate the 389 height-3148 roots in their canonical order."""
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
    """Return EH,EA,EB,EO,CH,CA,CB,CO labeled cells for a root."""
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
        cells.append(tuple(range(cursor, cursor + size)))
        cursor += size
    require(cursor == N, "root cells do not partition vertices 2,...,42")
    return tuple(cells)


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    require(0 <= i < j < N, "invalid edge")
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def opb_row(terms: list[tuple[int, int]], rhs: int) -> str:
    require(terms, "empty OPB row")
    return " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in terms) + f" >= {rhs} ;"


def suffix_lines():
    """Emit one guarded footprint lower bound for each root/exterior vertex."""
    for root_index, key in enumerate(ROOT_KEYS):
        common = key[1]
        cells = root_cells(key)
        core = cells[0] + cells[4]
        require(len(core) == common, "common-core size")
        exterior = tuple(vertex for vertex in range(2, N) if vertex not in core)
        require(len(exterior) == 41 - common, "exterior size")
        selector = SELECTOR_FIRST + root_index
        bound = common - 8
        for vertex in exterior:
            yield opb_row(
                [(1, edge_id(vertex, core_vertex)) for core_vertex in core]
                + [(-bound, selector)],
                0,
            )


def red13(i: int, j: int) -> bool:
    return (i - j) % 13 in CYCLIC_DIFFERENCES


def independent_sets(vertices: tuple[int, ...], size: int):
    for subset in itertools.combinations(vertices, size):
        if all(not red13(left, right) for left, right in itertools.combinations(subset, 2)):
            yield subset


def independence_number(vertices: tuple[int, ...]) -> int:
    for size in range(len(vertices), 0, -1):
        if next(independent_sets(vertices, size), None) is not None:
            return size
    return 0


def sharpness_certificate() -> dict[str, object]:
    all_vertices = tuple(range(13))
    require(
        not any(
            all(red13(left, right) for left, right in itertools.combinations(triple, 2))
            for triple in itertools.combinations(all_vertices, 3)
        ),
        "cyclic graph contains a red triangle",
    )
    require(independence_number(all_vertices) == 4, "cyclic graph alpha is not four")
    require(independence_number(SHARP_T) == 3, "sharp eight-set alpha is not three")

    records = []
    for common in range(9, 14):
        footprint = SHARP_EXTRAS[: common - 8]
        core = SHARP_T + footprint
        independent_fours = tuple(independent_sets(core, 4))
        require(len(core) == common, "sharp core size")
        require(independence_number(core) == 4, "sharp core alpha")
        require(
            all(set(four).intersection(footprint) for four in independent_fours),
            "sharp footprint misses an independent four-set",
        )
        records.append(
            {
                "c": common,
                "core": list(core),
                "footprint": list(footprint),
                "independent_fours": len(independent_fours),
            }
        )
    return {
        "cyclic_edges": sum(red13(i, j) for i in all_vertices for j in range(i + 1, 13)),
        "cyclic_independence": independence_number(all_vertices),
        "records": records,
        "T": list(SHARP_T),
        "T_independence": independence_number(SHARP_T),
    }


def certificate() -> tuple[bytes, dict[str, object]]:
    lines = ["index\tfamily\tc\tk\tpattern\tselector\tbound\tH\texterior_rows"]
    family_counts = Counter()
    common_counts = Counter()
    for root_index, key in enumerate(ROOT_KEYS):
        family, common, exceptional_common, pattern = key
        cells = root_cells(key)
        core = cells[0] + cells[4]
        exterior_rows = 41 - common
        lines.append(
            "\t".join(
                (
                    str(root_index),
                    family,
                    str(common),
                    str(exceptional_common),
                    pattern,
                    str(SELECTOR_FIRST + root_index),
                    str(common - 8),
                    ",".join(map(str, core)),
                    str(exterior_rows),
                )
            )
        )
        family_counts[family] += 1
        common_counts[common] += 1
    raw = ("\n".join(lines) + "\n").encode("ascii")
    suffix_raw = ("".join(line + "\n" for line in suffix_lines())).encode("ascii")
    sharp = sharpness_certificate()
    sharp_raw = json.dumps(sharp, sort_keys=True, separators=(",", ":")).encode("ascii")
    summary: dict[str, object] = {
        "bounds_by_c": [common - 8 for common in range(9, 14)],
        "certificate_bytes": len(raw),
        "certificate_lines": len(lines),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "common_counts": [common_counts[common] for common in range(9, 14)],
        "family_counts": [family_counts[family] for family in FAMILIES],
        "roots": len(ROOT_KEYS),
        "sharp_independent_four_counts": [
            record["independent_fours"] for record in sharp["records"]
        ],
        "sharp_sha256": hashlib.sha256(sharp_raw).hexdigest(),
        "suffix_bytes": len(suffix_raw),
        "suffix_rows": suffix_raw.count(b"\n"),
        "suffix_sha256": hashlib.sha256(suffix_raw).hexdigest(),
    }
    return raw, summary


def atomic_write(path: Path, raw: bytes) -> None:
    destination = path.resolve()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    try:
        with temporary.open("wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise


def strengthen(prior_path: Path, output_path: Path, suffix_raw: bytes) -> dict[str, int | str]:
    suffix_rows = suffix_raw.count(b"\n")
    new_constraints = PRIOR_CONSTRAINTS + suffix_rows
    new_header = (
        f"* #variable= {PRIOR_VARIABLES} #constraint= {new_constraints} "
        f"#equal= {PRIOR_EQUALITIES} intsize= 64\n"
    ).encode("ascii")
    destination = output_path.resolve()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    prior_hash = hashlib.sha256()
    output_hash = hashlib.sha256()
    prior_bytes = 0
    try:
        with prior_path.resolve().open("rb") as source, temporary.open("wb") as target:
            header = source.readline()
            require(header == PRIOR_HEADER, "unexpected prior header")
            prior_hash.update(header)
            prior_bytes += len(header)
            target.write(new_header)
            output_hash.update(new_header)
            while True:
                block = source.read(1 << 20)
                if not block:
                    break
                prior_hash.update(block)
                prior_bytes += len(block)
                target.write(block)
                output_hash.update(block)
            require(prior_bytes == PRIOR_BYTES, "unexpected prior byte count")
            require(prior_hash.hexdigest() == PRIOR_SHA256, "unexpected prior SHA-256")
            target.write(suffix_raw)
            output_hash.update(suffix_raw)
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    return {
        "formula_bytes": len(new_header) + PRIOR_BYTES - len(PRIOR_HEADER) + len(suffix_raw),
        "formula_constraints": new_constraints,
        "formula_equalities": PRIOR_EQUALITIES,
        "formula_lines": PRIOR_LINES + suffix_rows,
        "formula_sha256": output_hash.hexdigest(),
        "formula_variables": PRIOR_VARIABLES,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--suffix", type=Path)
    parser.add_argument("--prior-opb", type=Path)
    parser.add_argument("--output-opb", type=Path)
    args = parser.parse_args()
    require((args.prior_opb is None) == (args.output_opb is None), "give both OPB paths")

    certificate_raw, summary = certificate()
    suffix_raw = ("".join(line + "\n" for line in suffix_lines())).encode("ascii")
    if args.certificate is not None:
        atomic_write(args.certificate, certificate_raw)
    if args.suffix is not None:
        atomic_write(args.suffix, suffix_raw)
    if args.prior_opb is not None:
        summary.update(strengthen(args.prior_opb, args.output_opb, suffix_raw))
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
