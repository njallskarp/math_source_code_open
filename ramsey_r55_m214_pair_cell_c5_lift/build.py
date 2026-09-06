#!/usr/bin/env python3
"""Build the exact missed-pair-cell and C5 edge-hull OPB lift."""

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
CELLS = "HABO"
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")
PATTERNS = {
    "E8": ("H", "A"),
    "E77": ("BB", "BO", "OO"),
    "C8": ("B", "O"),
    "C77": ("BB", "BO", "OO"),
    "C77partition": ("HO", "AB"),
}

# Height-3254 formula: height 3228 plus the c=9,10 projected pair rows.
PRIOR_VARIABLES = 13_633
PRIOR_CONSTRAINTS = 2_131_051
PRIOR_EQUALITIES = 87
PRIOR_LINES = 2_131_052
PRIOR_BYTES = 187_209_692
PRIOR_SHA256 = "298aed6afa61eff55c21a96dae8af49d24a8c67d13d5d611e342a127c417c997"
PRIOR_HEADER = b"* #variable= 13633 #constraint= 2131051 #equal= 87 intsize= 64\n"

CYCLIC_DIFFERENCES = frozenset((1, 5, 8, 12))
SHARP_MISSED = {
    3: frozenset((0, 1, 3)),
    4: frozenset((0, 1, 3, 4)),
    5: frozenset((0, 1, 2, 3, 8)),
}
NESTED_CORE = (0, 1, 2, 3, 4, 5, 8, 9, 6, 7, 10, 11, 12)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    require(0 <= i < j < N, "invalid physical edge")
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def root_keys():
    """Enumerate the complete height-3148 root cover in canonical order."""
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
    require(all(size >= 0 for size in sizes), "negative root-cell size")
    result = []
    cursor = 2
    for size in sizes:
        result.append(tuple(range(cursor, cursor + size)))
        cursor += size
    require(cursor == N, "root cells do not partition vertices 2,...,42")
    return tuple(result)


def root_data(key: tuple[str, int, int, str]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    cells = root_cells(key)
    core = cells[0] + cells[4]
    core_set = frozenset(core)
    exterior = tuple(vertex for vertex in PHYSICAL if vertex not in core_set)
    require(len(core) == key[1] and len(exterior) == 41 - key[1], "root orders")
    return core, exterior


def supports() -> tuple[tuple[tuple[int, int, int], ...], tuple[tuple[int, int, int, int], ...]]:
    missed: set[tuple[int, int, int]] = set()
    red_inside: set[tuple[int, int, int, int]] = set()
    for key in ROOT_KEYS:
        core, exterior = root_data(key)
        for left, right in itertools.combinations(exterior, 2):
            missed.update((left, right, vertex) for vertex in core)
            red_inside.update((left, right, i, j) for i, j in itertools.combinations(core, 2))
    return tuple(sorted(missed)), tuple(sorted(red_inside))


MISSED_KEYS, RED_INSIDE_KEYS = supports()
MISSED_FIRST = PRIOR_VARIABLES + 1
RED_INSIDE_FIRST = MISSED_FIRST + len(MISSED_KEYS)
MISSED_IDS = {key: MISSED_FIRST + index for index, key in enumerate(MISSED_KEYS)}
RED_INSIDE_IDS = {
    key: RED_INSIDE_FIRST + index for index, key in enumerate(RED_INSIDE_KEYS)
}
VARIABLES = PRIOR_VARIABLES + len(MISSED_KEYS) + len(RED_INSIDE_KEYS)


def opb_row(terms: list[tuple[int, int]], rhs: int) -> str:
    require(terms, "empty OPB row")
    return " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in terms) + f" >= {rhs} ;"


def definition_lines():
    """Define m=(not x_zi) AND (not x_z'i), then q=m_i AND m_j AND x_ij."""
    for left, right, vertex in MISSED_KEYS:
        missed = MISSED_IDS[left, right, vertex]
        left_edge = edge_id(left, vertex)
        right_edge = edge_id(right, vertex)
        yield opb_row([(-1, missed), (-1, left_edge)], -1)
        yield opb_row([(-1, missed), (-1, right_edge)], -1)
        yield opb_row([(1, missed), (1, left_edge), (1, right_edge)], 1)
    for left, right, i, j in RED_INSIDE_KEYS:
        red_inside = RED_INSIDE_IDS[left, right, i, j]
        missed_i = MISSED_IDS[left, right, i]
        missed_j = MISSED_IDS[left, right, j]
        core_edge = edge_id(i, j)
        yield opb_row([(-1, red_inside), (1, missed_i)], 0)
        yield opb_row([(-1, red_inside), (1, missed_j)], 0)
        yield opb_row([(-1, red_inside), (1, core_edge)], 0)
        yield opb_row(
            [(1, red_inside), (-1, missed_i), (-1, missed_j), (-1, core_edge)],
            -2,
        )


def root_lines():
    """Emit the exact missed-cell bound and its two lower edge-hull facets."""
    selector_first = 13_245
    for root_index, key in enumerate(ROOT_KEYS):
        common = key[1]
        core, exterior = root_data(key)
        selector = selector_first + root_index
        for left, right in itertools.combinations(exterior, 2):
            pair_edge = edge_id(left, right)
            missed_terms = [MISSED_IDS[left, right, vertex] for vertex in core]
            inside_terms = [
                RED_INSIDE_IDS[left, right, i, j]
                for i, j in itertools.combinations(core, 2)
            ]

            # Active root and blue pair: m <= 5.
            guard = common - 5
            yield opb_row(
                [(-1, variable) for variable in missed_terms]
                + [(guard, pair_edge), (-guard, selector)],
                -common,
            )

            # Lower hull: e >= m-2.
            guard = common - 2
            yield opb_row(
                [(1, variable) for variable in inside_terms]
                + [(-1, variable) for variable in missed_terms]
                + [(guard, pair_edge), (-guard, selector)],
                -common,
            )

            # The C5 facet: e >= 3m-10.
            guard = 3 * common - 10
            yield opb_row(
                [(1, variable) for variable in inside_terms]
                + [(-3, variable) for variable in missed_terms]
                + [(guard, pair_edge), (-guard, selector)],
                -3 * common,
            )


DEFINITION_ROWS = 3 * len(MISSED_KEYS) + 4 * len(RED_INSIDE_KEYS)
ROOT_PAIR_COUNTS = Counter()
for root_key in ROOT_KEYS:
    _, root_exterior = root_data(root_key)
    ROOT_PAIR_COUNTS[root_key[1]] += len(root_exterior) * (len(root_exterior) - 1) // 2
ROOT_PAIRS = sum(ROOT_PAIR_COUNTS.values())
ROOT_ROWS = 3 * ROOT_PAIRS
SUFFIX_ROWS = DEFINITION_ROWS + ROOT_ROWS
CONSTRAINTS = PRIOR_CONSTRAINTS + SUFFIX_ROWS
HEADER = (
    f"* #variable= {VARIABLES} #constraint= {CONSTRAINTS} "
    f"#equal= {PRIOR_EQUALITIES} intsize= 64\n"
).encode("ascii")


def red13(i: int, j: int) -> bool:
    return (i - j) % 13 in CYCLIC_DIFFERENCES


def independent(vertices: frozenset[int]) -> bool:
    return all(not red13(i, j) for i, j in itertools.combinations(vertices, 2))


def independence_number(vertices: frozenset[int]) -> int:
    for order in range(len(vertices), -1, -1):
        if any(independent(frozenset(part)) for part in itertools.combinations(vertices, order)):
            return order
    raise AssertionError("unreachable")


def sharpness_certificate() -> dict[str, object]:
    records = []
    for missed_order, missed in SHARP_MISSED.items():
        red_edges = sum(red13(i, j) for i, j in itertools.combinations(sorted(missed), 2))
        require(independence_number(missed) == 2, "sharp missed-set independence")
        require(red_edges == {3: 1, 4: 2, 5: 5}[missed_order], "sharp edge count")
        records.append(
            {
                "e": red_edges,
                "m": missed_order,
                "missed": sorted(missed),
                "first_facet_slack": red_edges - missed_order + 2,
                "second_facet_slack": red_edges - 3 * missed_order + 10,
            }
        )
    for common in range(9, 14):
        core = frozenset(NESTED_CORE[:common])
        require(independence_number(core) == 4, "sharp core independence")
        require(
            not any(
                red13(i, j) and red13(i, k) and red13(j, k)
                for i, j, k in itertools.combinations(sorted(core), 3)
            ),
            "sharp core triangle",
        )
        require(all(missed <= core for missed in SHARP_MISSED.values()), "sharp missed containment")
    return {"records": records, "nested_core": list(NESTED_CORE)}


def key_hash(keys: tuple[tuple[int, ...], ...]) -> str:
    raw = "".join(",".join(map(str, key)) + "\n" for key in keys).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def root_certificate() -> bytes:
    lines = ["index\tfamily\tc\tk\tpattern\tselector\tH\texterior\tpairs\trows"]
    for root_index, key in enumerate(ROOT_KEYS):
        core, exterior = root_data(key)
        pairs = len(exterior) * (len(exterior) - 1) // 2
        lines.append(
            "\t".join(
                (
                    str(root_index),
                    key[0],
                    str(key[1]),
                    str(key[2]),
                    key[3],
                    str(13_245 + root_index),
                    ",".join(map(str, core)),
                    str(len(exterior)),
                    str(pairs),
                    str(3 * pairs),
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


def formula_chunks(prior_path: Path, suffix_path: Path):
    with prior_path.open("rb") as prior:
        old_header = prior.readline()
        require(old_header == PRIOR_HEADER, "prior header")
        yield HEADER
        while True:
            chunk = prior.read(1 << 20)
            if not chunk:
                break
            yield chunk
    with suffix_path.open("rb") as suffix:
        while True:
            chunk = suffix.read(1 << 20)
            if not chunk:
                break
            yield chunk


def file_identity(path: Path) -> tuple[int, int, str]:
    digest = hashlib.sha256()
    byte_count = 0
    line_count = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
            byte_count += len(chunk)
            line_count += chunk.count(b"\n")
    return byte_count, line_count, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--suffix", type=Path, required=True)
    parser.add_argument("--prior-opb", type=Path)
    parser.add_argument("--output-opb", type=Path)
    args = parser.parse_args()
    require((args.prior_opb is None) == (args.output_opb is None), "full-formula arguments")

    certificate_raw = root_certificate()
    certificate_stats = write_atomic(args.certificate, (certificate_raw,))
    suffix_stats = write_atomic(
        args.suffix,
        (line + "\n" for line in itertools.chain(definition_lines(), root_lines())),
    )
    require(certificate_stats[1] == len(ROOT_KEYS) + 1, "certificate line count")
    require(suffix_stats[1] == SUFFIX_ROWS, "suffix line count")

    sharp_raw = json.dumps(
        sharpness_certificate(), sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    result: dict[str, object] = {
        "definition_rows": DEFINITION_ROWS,
        "final_constraints": CONSTRAINTS,
        "final_variables": VARIABLES,
        "missed_keys": len(MISSED_KEYS),
        "missed_keys_sha256": key_hash(MISSED_KEYS),
        "red_inside_keys": len(RED_INSIDE_KEYS),
        "red_inside_keys_sha256": key_hash(RED_INSIDE_KEYS),
        "root_certificate_bytes": certificate_stats[0],
        "root_certificate_sha256": certificate_stats[2],
        "root_pair_counts": [ROOT_PAIR_COUNTS[c] for c in range(9, 14)],
        "root_pairs": ROOT_PAIRS,
        "root_rows": ROOT_ROWS,
        "roots": len(ROOT_KEYS),
        "sharpness_sha256": hashlib.sha256(sharp_raw).hexdigest(),
        "suffix_bytes": suffix_stats[0],
        "suffix_rows": suffix_stats[1],
        "suffix_sha256": suffix_stats[2],
    }

    if args.prior_opb is not None and args.output_opb is not None:
        prior_identity = file_identity(args.prior_opb)
        require(prior_identity == (PRIOR_BYTES, PRIOR_LINES, PRIOR_SHA256), "prior identity")
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
            "variables": VARIABLES,
        }

    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
