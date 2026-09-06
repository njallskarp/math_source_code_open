#!/usr/bin/env python3
"""Generate one selector-gated OPB containing all 389 complete pair roots."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path


N = 43
ANCHORS = (0, 1)
EXCEPTIONAL = frozenset(range(2, 15))
CENTRAL = frozenset(range(N)) - EXCEPTIONAL
CELLS = "HABO"
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")
PATTERNS = {
    "E8": ("H", "A"),
    "E77": ("BB", "BO", "OO"),
    "C8": ("B", "O"),
    "C77": ("BB", "BO", "OO"),
    "C77partition": ("HO", "AB"),
}
EDGE_COUNT = N * (N - 1) // 2
TRIANGLE_COUNT = N * (N - 1) * (N - 2) // 6
BASE_VARIABLE_COUNT = EDGE_COUNT + TRIANGLE_COUNT
FIVE_SET_COUNT = N * (N - 1) * (N - 2) * (N - 3) * (N - 4) // 120
BASE_EQUALITY_COUNT = 2 * N
BASE_CONSTRAINT_COUNT = 2 * FIVE_SET_COUNT + 4 * TRIANGLE_COUNT + 3 * N


class CanonicalWriter:
    def __init__(self, raw):
        self.raw = raw
        self.sha256 = hashlib.sha256()
        self.bytes_written = 0
        self.lines_written = 0

    def line(self, value: str) -> None:
        data = (value + "\n").encode("ascii")
        self.raw.write(data)
        self.sha256.update(data)
        self.bytes_written += len(data)
        self.lines_written += 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    require(0 <= i < j < N, f"invalid edge ({i},{j})")
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def triangle_ids() -> dict[tuple[int, int, int], int]:
    return {
        triple: EDGE_COUNT + rank
        for rank, triple in enumerate(itertools.combinations(range(N), 3), 1)
    }


def row(terms: list[tuple[int, int]], relation: str, rhs: int) -> str:
    require(terms and relation in {">=", "="}, "invalid row")
    return " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in terms) + f" {relation} {rhs} ;"


def root_keys():
    for family in FAMILIES:
        for common in range(9, 14):
            for exceptional_common in range(7):
                e_sizes = (exceptional_common, 6 - exceptional_common,
                           6 - exceptional_common, 1 + exceptional_common)
                c_sizes = (common - exceptional_common, 14 - common + exceptional_common,
                           14 - common + exceptional_common, common - exceptional_common)
                sizes = e_sizes if family.startswith("E") else c_sizes
                for pattern in PATTERNS[family]:
                    if all(pattern.count(cell) <= sizes[index]
                           for index, cell in enumerate(CELLS)):
                        yield family, common, exceptional_common, pattern


def root_record(key: tuple[str, int, int, str]) -> dict[str, object]:
    family, common, exceptional_common, pattern = key
    e_sizes = (exceptional_common, 6 - exceptional_common,
               6 - exceptional_common, 1 + exceptional_common)
    c_sizes = (common - exceptional_common, 14 - common + exceptional_common,
               14 - common + exceptional_common, common - exceptional_common)
    cells: list[list[int]] = []
    cursor = 2
    for size in e_sizes + c_sizes:
        cells.append(list(range(cursor, cursor + size)))
        cursor += size
    require(cursor == N, "root cells do not partition the vertices")

    anomaly_offset = 0 if family.startswith("E") else 4
    anomalies: list[int] = []
    for index, cell_name in enumerate(CELLS):
        anomalies.extend(cells[anomaly_offset + index][:pattern.count(cell_name)])
    excess = 2 if family in {"E8", "C8"} else 1

    units = [(0, 1, 1)]
    bits = ((1, 1), (1, 0), (0, 1), (0, 0))
    for index, cell in enumerate(cells):
        for vertex in cell:
            units.append((0, vertex, bits[index % 4][0]))
            units.append((1, vertex, bits[index % 4][1]))
    units.sort()
    require(len(units) == 83, "anchor-unit count")

    partition = None
    if family == "C77partition":
        p, q = anomalies
        partition = (p, q, tuple([0, 1] + [vertex for vertex in range(15, N)
                                            if vertex not in anomalies]))
        require(len(partition[2]) == 28, "partition row count")
    return {
        "a_targets": tuple(6 + (excess if vertex in anomalies else 0)
                           for vertex in range(N)),
        "anomalies": tuple(anomalies),
        "partition": partition,
        "units": tuple(units),
    }


ROOT_KEYS = tuple(root_keys())
ROOT_COUNT = len(ROOT_KEYS)
PARTITION_ROOT_COUNT = sum(key[0] == "C77partition" for key in ROOT_KEYS)
SELECTOR_FIRST = BASE_VARIABLE_COUNT + 1
VARIABLE_COUNT = BASE_VARIABLE_COUNT + ROOT_COUNT
ROOT_COMMON_ROWS = 83 + 2 * N
ROOT_PARTITION_ROWS = 1 + 2 * 28
SELECTOR_ROWS = ROOT_COUNT * ROOT_COMMON_ROWS + PARTITION_ROOT_COUNT * ROOT_PARTITION_ROWS + 1
CONSTRAINT_COUNT = BASE_CONSTRAINT_COUNT + SELECTOR_ROWS
EQUALITY_COUNT = BASE_EQUALITY_COUNT + 1


def emit_guarded_unit(writer: CanonicalWriter, edge: int, value: int, selector: int) -> None:
    if value == 1:
        writer.line(row([(1, edge), (-1, selector)], ">=", 0))
    else:
        writer.line(row([(-1, edge), (-1, selector)], ">=", -1))


def emit_guarded_sum_equality(writer: CanonicalWriter, variables: list[int], target: int,
                              selector: int, maximum: int) -> None:
    writer.line(row([(1, variable) for variable in variables] + [(-target, selector)], ">=", 0))
    writer.line(row([(-1, variable) for variable in variables] +
                    [(-(maximum - target), selector)], ">=", -maximum))


def generate(raw) -> dict[str, int | str]:
    triangles = triangle_ids()
    writer = CanonicalWriter(raw)
    writer.line(f"* #variable= {VARIABLE_COUNT} #constraint= {CONSTRAINT_COUNT} "
                f"#equal= {EQUALITY_COUNT} intsize= 64")
    emitted = 0

    for vertices in itertools.combinations(range(N), 5):
        edges = [edge_id(i, j) for i, j in itertools.combinations(vertices, 2)]
        writer.line(row([(1, edge) for edge in edges], ">=", 1))
        writer.line(row([(-1, edge) for edge in edges], ">=", -9))
        emitted += 2

    for triangle, z_variable in triangles.items():
        edges = [edge_id(i, j) for i, j in itertools.combinations(triangle, 2)]
        for edge in edges:
            writer.line(row([(-1, z_variable), (1, edge)], ">=", 0))
        writer.line(row([(1, z_variable)] + [(-1, edge) for edge in edges], ">=", -2))
        emitted += 4

    for vertex in range(N):
        incident = [edge_id(vertex, other) for other in range(N) if other != vertex]
        writer.line(row([(1, edge) for edge in incident], "=",
                        20 if vertex in EXCEPTIONAL else 21))
        emitted += 1

    for vertex in range(N):
        others = [other for other in range(N) if other != vertex]
        local = [triangles[tuple(sorted((vertex, i, j)))]
                 for i, j in itertools.combinations(others, 2)]
        writer.line(row([(1, variable) for variable in local], "=",
                        93 if vertex in EXCEPTIONAL else 100))
        emitted += 1

    for vertex in range(N):
        exceptional_neighbors = [edge_id(vertex, other) for other in EXCEPTIONAL
                                 if other != vertex]
        writer.line(row([(1, edge) for edge in exceptional_neighbors], ">=", 6))
        emitted += 1

    selectors = list(range(SELECTOR_FIRST, VARIABLE_COUNT + 1))
    writer.line(row([(1, selector) for selector in selectors], "=", 1))
    emitted += 1

    family_counts = {family: 0 for family in FAMILIES}
    for root_index, key in enumerate(ROOT_KEYS):
        selector = SELECTOR_FIRST + root_index
        record = root_record(key)
        family_counts[key[0]] += 1
        for i, j, value in record["units"]:
            emit_guarded_unit(writer, edge_id(i, j), value, selector)
            emitted += 1
        for vertex, target in enumerate(record["a_targets"]):
            variables = [edge_id(vertex, other) for other in EXCEPTIONAL if other != vertex]
            emit_guarded_sum_equality(writer, variables, target, selector, 13)
            emitted += 2
        partition = record["partition"]
        if partition is not None:
            p, q, vertices = partition
            emit_guarded_unit(writer, edge_id(p, q), 0, selector)
            emitted += 1
            for vertex in vertices:
                emit_guarded_sum_equality(writer,
                                          [edge_id(vertex, p), edge_id(vertex, q)],
                                          1, selector, 2)
                emitted += 2

    require(emitted == CONSTRAINT_COUNT, f"constraint count {emitted}")
    require(writer.lines_written == CONSTRAINT_COUNT + 1, "line count")
    require(tuple(family_counts.values()) == (60, 85, 70, 104, 70), "family census")
    root_key_bytes = "".join("\t".join(map(str, key)) + "\n" for key in ROOT_KEYS).encode("ascii")
    return {
        "bytes": writer.bytes_written,
        "constraints": emitted,
        "equalities": EQUALITY_COUNT,
        "family_counts": list(family_counts.values()),
        "lines": writer.lines_written,
        "partition_roots": PARTITION_ROOT_COUNT,
        "roots": ROOT_COUNT,
        "root_keys_sha256": hashlib.sha256(root_key_bytes).hexdigest(),
        "selector_rows": SELECTOR_ROWS,
        "sha256": writer.sha256.hexdigest(),
        "variables": VARIABLE_COUNT,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True,
                        help="OPB destination (generated state; do not commit)")
    args = parser.parse_args()
    destination = args.output.resolve()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    try:
        with temporary.open("wb") as raw:
            summary = generate(raw)
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
