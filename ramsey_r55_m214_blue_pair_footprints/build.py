#!/usr/bin/env python3
"""Build the sharp blue-exterior-pair footprint certificate and OPB suffix."""

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

# Height-3228 all-c footprint formula, generated from its published source.
PRIOR_SHA256 = "e8ac0385c3654aa6106922bcb32d0e19832b6e8331a17d9aa55b44f7f3a8747a"
PRIOR_HEADER = b"* #variable= 13633 #constraint= 2056093 #equal= 87 intsize= 64\n"
PRIOR_BYTES = 174_004_384
PRIOR_LINES = 2_056_094
PRIOR_VARIABLES = 13_633
PRIOR_CONSTRAINTS = 2_056_093
PRIOR_EQUALITIES = 87

CYCLIC_DIFFERENCES = frozenset((1, 5, 8, 12))
NESTED_T = (0, 1, 2, 3, 4, 5, 8, 9)
NESTED_EXTRAS = (6, 7, 10, 11, 12)
MISSED_C5 = frozenset((0, 1, 2, 3, 8))
SUM_SHARP = {
    9: (frozenset((0, 4)), frozenset((5, 6))),
    10: (frozenset((0, 4, 5)), frozenset((2, 3))),
}
INDIVIDUAL_ONLY = {
    9: frozenset((6,)),
    10: frozenset((6, 7)),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


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
    """Emit the nonredundant c=9,10 blue-pair sum projections."""
    for root_index, key in enumerate(ROOT_KEYS):
        common = key[1]
        if common not in (9, 10):
            continue
        cells = root_cells(key)
        core = cells[0] + cells[4]
        exterior = tuple(vertex for vertex in range(2, N) if vertex not in core)
        require(len(core) == common and len(exterior) == 41 - common, "root sizes")
        selector = SELECTOR_FIRST + root_index
        bound = common - 5
        for left, right in itertools.combinations(exterior, 2):
            yield opb_row(
                [(1, edge_id(left, vertex)) for vertex in core]
                + [(1, edge_id(right, vertex)) for vertex in core]
                + [(bound, edge_id(left, right)), (-bound, selector)],
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


def is_transversal(footprint: frozenset[int], independent_fours: tuple[tuple[int, ...], ...]) -> bool:
    return all(footprint.intersection(four) for four in independent_fours)


def blue_pair_valid(
    left: frozenset[int], right: frozenset[int], independent_triples: tuple[tuple[int, ...], ...]
) -> bool:
    union = left | right
    return all(union.intersection(triple) for triple in independent_triples)


def sharpness_certificate() -> dict[str, object]:
    records = []
    all_vertices = tuple(range(13))
    require(
        not any(
            all(red13(left, right) for left, right in itertools.combinations(triple, 2))
            for triple in itertools.combinations(all_vertices, 3)
        ),
        "cyclic graph contains a red triangle",
    )
    require(independence_number(all_vertices) == 4, "cyclic graph alpha")
    require(independence_number(tuple(MISSED_C5)) == 2, "missed five-set alpha")
    for common in range(9, 14):
        core = NESTED_T + NESTED_EXTRAS[: common - 8]
        fours = tuple(independent_sets(core, 4))
        triples = tuple(independent_sets(core, 3))
        union_sharp = frozenset(core) - MISSED_C5
        require(len(union_sharp) == common - 5, "sharp union size")
        require(is_transversal(union_sharp, fours), "sharp union is not a footprint")
        require(blue_pair_valid(union_sharp, union_sharp, triples), "sharp pair invalid")
        record: dict[str, object] = {
            "c": common,
            "core": list(core),
            "independent_fours": len(fours),
            "independent_triples": len(triples),
            "missed_C5": sorted(MISSED_C5),
            "union_sharp": sorted(union_sharp),
        }
        if common in SUM_SHARP:
            left, right = SUM_SHARP[common]
            require(left.isdisjoint(right), "sum-sharp footprints overlap")
            require(len(left) + len(right) == common - 5, "sum-sharp total")
            require(is_transversal(left, fours) and is_transversal(right, fours), "sum-sharp unary")
            require(blue_pair_valid(left, right, triples), "sum-sharp blue pair")
            individual = INDIVIDUAL_ONLY[common]
            require(len(individual) == common - 8, "individual footprint size")
            require(is_transversal(individual, fours), "individual witness is not a footprint")
            require(2 * len(individual) < common - 5, "individual witness does not violate pair row")
            require(not blue_pair_valid(individual, individual, triples), "individual witness is pair-valid")
            record.update(
                {
                    "individual_only": sorted(individual),
                    "sum_sharp_left": sorted(left),
                    "sum_sharp_right": sorted(right),
                }
            )
        records.append(record)
    return {"records": records}


def certificate() -> tuple[bytes, dict[str, object]]:
    lines = ["index\tfamily\tc\tk\tpattern\tselector\tbound\tH\texterior\tpair_rows"]
    family_counts = Counter()
    common_counts = Counter()
    pair_rows = 0
    for root_index, key in enumerate(ROOT_KEYS):
        family, common, exceptional_common, pattern = key
        if common not in (9, 10):
            continue
        cells = root_cells(key)
        core = cells[0] + cells[4]
        exterior_count = 41 - common
        rows = exterior_count * (exterior_count - 1) // 2
        lines.append(
            "\t".join(
                (
                    str(root_index), family, str(common), str(exceptional_common), pattern,
                    str(SELECTOR_FIRST + root_index), str(common - 5),
                    ",".join(map(str, core)), str(exterior_count), str(rows),
                )
            )
        )
        family_counts[family] += 1
        common_counts[common] += 1
        pair_rows += rows
    raw = ("\n".join(lines) + "\n").encode("ascii")
    suffix_raw = ("".join(line + "\n" for line in suffix_lines())).encode("ascii")
    sharp_raw = json.dumps(sharpness_certificate(), sort_keys=True, separators=(",", ":")).encode("ascii")
    require(suffix_raw.count(b"\n") == pair_rows, "suffix row count")
    summary: dict[str, object] = {
        "active_roots": sum(common_counts.values()),
        "bounds_by_c": [4, 5],
        "certificate_bytes": len(raw),
        "certificate_lines": len(lines),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "common_counts": [common_counts[9], common_counts[10]],
        "family_counts": [family_counts[family] for family in FAMILIES],
        "roots": len(ROOT_KEYS),
        "sharp_sha256": hashlib.sha256(sharp_raw).hexdigest(),
        "suffix_bytes": len(suffix_raw),
        "suffix_rows": pair_rows,
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
