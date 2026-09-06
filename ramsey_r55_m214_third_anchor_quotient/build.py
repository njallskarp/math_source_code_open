#!/usr/bin/env python3
"""Build and certify the all-root third-anchor incidence quotient."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
from collections import Counter, defaultdict
from fractions import Fraction
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
BASE_SHA256 = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
BASE_HEADER = b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n"
BASE_BYTES = 172_788_992
BASE_LINES = 2_044_422
BASE_VARIABLES = 13_633
BASE_CONSTRAINTS = 2_044_421
BASE_EQUALITIES = 87
SELECTOR_FIRST = 13_245


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


def root_layout(key: tuple[str, int, int, str]) -> dict[str, object]:
    family, common, exceptional_common, pattern = key
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
    cells: list[list[int]] = []
    cursor = 2
    for size in e_sizes + c_sizes:
        cells.append(list(range(cursor, cursor + size)))
        cursor += size
    require(cursor == N, "cell partition")

    anomaly_offset = 0 if family.startswith("E") else 4
    anomalies: list[int] = []
    for index, name in enumerate(CELLS):
        anomalies.extend(cells[anomaly_offset + index][: pattern.count(name)])
    anomaly_set = frozenset(anomalies)

    buckets: list[dict[str, object]] = []
    for color, offset in (("E", 0), ("C", 4)):
        for cell_index, cell_name in enumerate(CELLS):
            for anomalous in (False, True):
                vertices = [
                    vertex
                    for vertex in cells[offset + cell_index]
                    if (vertex in anomaly_set) == anomalous
                ]
                if vertices:
                    buckets.append(
                        {
                            "name": f"{color}{cell_name}{'a' if anomalous else 'o'}",
                            "color": color,
                            "cell": cell_name,
                            "anomalous": anomalous,
                            "vertices": vertices,
                        }
                    )

    pools = [
        bucket
        for bucket in buckets
        if bucket["color"] == "C"
        and bucket["cell"] == "H"
        and not bucket["anomalous"]
    ]
    require(len(pools) == 1, "unique ordinary central-H pool")
    pool = pools[0]
    pool_size = len(pool["vertices"])
    require(pool_size >= 2, "third-anchor pool has fewer than two vertices")
    third_anchor = min(pool["vertices"])
    pool["vertices"] = [vertex for vertex in pool["vertices"] if vertex != third_anchor]

    partition_pair = frozenset(anomalies) if family == "C77partition" else frozenset()
    if partition_pair:
        require(len(partition_pair) == 2, "partition anomaly pair")
    require(sum(len(bucket["vertices"]) for bucket in buckets) == 40, "residual vertices")
    require(all(bucket["vertices"] for bucket in buckets), "empty refined bucket")
    return {
        "key": key,
        "common": common,
        "third_anchor": third_anchor,
        "pool_size": pool_size,
        "buckets": buckets,
        "partition_pair": partition_pair,
    }


def cell_options(
    buckets: list[dict[str, object]], partition_pair: frozenset[int]
) -> dict[tuple[int, int], tuple[int, int]]:
    """Return (red total, red partition anomalies) -> (orbits, labelings)."""
    states: dict[tuple[int, int], tuple[int, int]] = {(0, 0): (1, 1)}
    for bucket in buckets:
        vertices = bucket["vertices"]
        size = len(vertices)
        marked = sum(vertex in partition_pair for vertex in vertices)
        require(marked in (0, size), "partition mark splits a refined bucket")
        if marked:
            require(size == 1, "partition anomaly bucket is not singleton")
        following: defaultdict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])
        for (total, partition_red), (orbits, labelings) in states.items():
            for chosen in range(size + 1):
                key = (total + chosen, partition_red + (chosen if marked else 0))
                following[key][0] += orbits
                following[key][1] += labelings * math.comb(size, chosen)
        states = {key: tuple(value) for key, value in following.items()}
    return states


def color_options(
    layout: dict[str, object], color: str, target: int
) -> dict[tuple[tuple[int, int, int, int], int], tuple[int, int]]:
    tables = []
    for cell in CELLS:
        cell_buckets = [
            bucket
            for bucket in layout["buckets"]
            if bucket["color"] == color and bucket["cell"] == cell
        ]
        tables.append(cell_options(cell_buckets, layout["partition_pair"]))

    result: defaultdict[
        tuple[tuple[int, int, int, int], int], list[int]
    ] = defaultdict(lambda: [0, 0])
    for selections in itertools.product(*(table.items() for table in tables)):
        totals = tuple(selection[0][0] for selection in selections)
        if sum(totals) != target:
            continue
        partition_red = sum(selection[0][1] for selection in selections)
        orbit_factor = math.prod(selection[1][0] for selection in selections)
        labeling_factor = math.prod(selection[1][1] for selection in selections)
        result[(totals, partition_red)][0] += orbit_factor
        result[(totals, partition_red)][1] += labeling_factor
    return {key: tuple(value) for key, value in result.items()}


def count_rows(layout: dict[str, object]) -> tuple[int, int]:
    common = layout["common"]
    e_options = color_options(layout, "E", 6)
    c_options = color_options(layout, "C", 13)
    orbit_rows = 0
    labeled_rows = 0
    for (e_totals, e_partition), (e_orbits, e_labelings) in e_options.items():
        for (c_totals, c_partition), (c_orbits, c_labelings) in c_options.items():
            red_h = e_totals[0] + c_totals[0]
            red_a = e_totals[1] + c_totals[1]
            red_b = e_totals[2] + c_totals[2]
            if not common - 9 <= red_h <= 4:
                continue
            if red_h + red_a > 12 or red_h + red_b > 12:
                continue
            if layout["partition_pair"] and e_partition + c_partition != 1:
                continue
            orbit_rows += e_orbits * c_orbits
            labeled_rows += e_labelings * c_labelings
    require(orbit_rows > 0 and labeled_rows >= orbit_rows, "empty or invalid row quotient")
    return orbit_rows, labeled_rows


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    require(0 <= i < j < N, "invalid edge")
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def opb_row(terms: list[tuple[int, int]], rhs: int) -> str:
    require(terms, "empty OPB row")
    return " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in terms) + f" >= {rhs} ;"


def suffix_lines():
    for root_index, key in enumerate(ROOT_KEYS):
        layout = root_layout(key)
        selector = SELECTOR_FIRST + root_index
        third_anchor = layout["third_anchor"]
        common = layout["common"]

        for bucket in layout["buckets"]:
            vertices = bucket["vertices"]
            for left, right in zip(vertices, vertices[1:]):
                yield opb_row(
                    [
                        (1, edge_id(third_anchor, left)),
                        (-1, edge_id(third_anchor, right)),
                        (-1, selector),
                    ],
                    -1,
                )

        by_cell = {
            cell: [
                vertex
                for bucket in layout["buckets"]
                if bucket["cell"] == cell
                for vertex in bucket["vertices"]
            ]
            for cell in CELLS
        }
        red_h = by_cell["H"]
        red_a = by_cell["A"]
        red_b = by_cell["B"]
        require(len(red_h) == common - 1, "H size after third anchor")
        require(len(red_a) == len(red_b) == 20 - common, "off-diagonal sizes")

        if common > 9:
            yield opb_row(
                [(1, edge_id(third_anchor, vertex)) for vertex in red_h]
                + [(-(common - 9), selector)],
                0,
            )
        yield opb_row(
            [(-1, edge_id(third_anchor, vertex)) for vertex in red_h]
            + [(-(common - 5), selector)],
            -(common - 1),
        )
        yield opb_row(
            [(-1, edge_id(third_anchor, vertex)) for vertex in red_h + red_a]
            + [(-7, selector)],
            -19,
        )
        yield opb_row(
            [(-1, edge_id(third_anchor, vertex)) for vertex in red_h + red_b]
            + [(-7, selector)],
            -19,
        )


def suffix_summary() -> tuple[dict[str, int | str], bytes]:
    raw = "".join(line + "\n" for line in suffix_lines()).encode("ascii")
    return {
        "suffix_bytes": len(raw),
        "suffix_rows": raw.count(b"\n"),
        "suffix_sha256": hashlib.sha256(raw).hexdigest(),
    }, raw


def certificate() -> tuple[bytes, dict[str, object]]:
    lines = [
        "family\tc\tk\tpattern\tthird_anchor\tpool_size\tbuckets_after_anchor"
        "\tordering_rows\torbit_rows\tlabeled_rows"
    ]
    family_roots = Counter()
    family_orbits = Counter()
    family_labelings = Counter()
    ratios: list[tuple[Fraction, tuple[str, int, int, str], int, int]] = []
    total_ordering = 0
    for key in ROOT_KEYS:
        layout = root_layout(key)
        orbit_rows, labeled_rows = count_rows(layout)
        ordering_rows = sum(len(bucket["vertices"]) - 1 for bucket in layout["buckets"])
        total_ordering += ordering_rows
        bucket_text = ",".join(
            f"{bucket['name']}:{len(bucket['vertices'])}" for bucket in layout["buckets"]
        )
        lines.append(
            "\t".join(
                map(
                    str,
                    (
                        *key,
                        layout["third_anchor"],
                        layout["pool_size"],
                        bucket_text,
                        ordering_rows,
                        orbit_rows,
                        labeled_rows,
                    ),
                )
            )
        )
        family_roots[key[0]] += 1
        family_orbits[key[0]] += orbit_rows
        family_labelings[key[0]] += labeled_rows
        ratios.append((Fraction(labeled_rows, orbit_rows), key, labeled_rows, orbit_rows))

    raw = ("\n".join(lines) + "\n").encode("ascii")
    minimum_ratio, minimum_key, minimum_labeled, minimum_orbits = min(ratios)
    suffix, _ = suffix_summary()
    summary: dict[str, object] = {
        "certificate_bytes": len(raw),
        "certificate_lines": len(lines),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "family_labeled_rows": [family_labelings[family] for family in FAMILIES],
        "family_orbit_rows": [family_orbits[family] for family in FAMILIES],
        "family_roots": [family_roots[family] for family in FAMILIES],
        "labeled_rows": sum(family_labelings.values()),
        "minimum_compression_denominator": minimum_orbits,
        "minimum_compression_floor": minimum_ratio.numerator // minimum_ratio.denominator,
        "minimum_compression_key": list(minimum_key),
        "minimum_compression_numerator": minimum_labeled,
        "orbit_rows": sum(family_orbits.values()),
        "ordering_rows": total_ordering,
        "pool_max": max(root_layout(key)["pool_size"] for key in ROOT_KEYS),
        "pool_min": min(root_layout(key)["pool_size"] for key in ROOT_KEYS),
        "roots": len(ROOT_KEYS),
        **suffix,
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


def strengthen(base_path: Path, output_path: Path, suffix_raw: bytes) -> dict[str, int | str]:
    suffix_rows = suffix_raw.count(b"\n")
    new_constraints = BASE_CONSTRAINTS + suffix_rows
    new_header = (
        f"* #variable= {BASE_VARIABLES} #constraint= {new_constraints} "
        f"#equal= {BASE_EQUALITIES} intsize= 64\n"
    ).encode("ascii")
    destination = output_path.resolve()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    base_hash = hashlib.sha256()
    output_hash = hashlib.sha256()
    base_bytes = 0
    try:
        with base_path.resolve().open("rb") as source, temporary.open("wb") as target:
            header = source.readline()
            require(header == BASE_HEADER, "unexpected base header")
            base_hash.update(header)
            base_bytes += len(header)
            target.write(new_header)
            output_hash.update(new_header)
            while True:
                block = source.read(1 << 20)
                if not block:
                    break
                base_hash.update(block)
                base_bytes += len(block)
                target.write(block)
                output_hash.update(block)
            require(base_bytes == BASE_BYTES, "unexpected base byte count")
            require(base_hash.hexdigest() == BASE_SHA256, "unexpected base SHA-256")
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
        "formula_bytes": len(new_header) + BASE_BYTES - len(BASE_HEADER) + len(suffix_raw),
        "formula_constraints": new_constraints,
        "formula_equalities": BASE_EQUALITIES,
        "formula_lines": BASE_LINES + suffix_rows,
        "formula_sha256": output_hash.hexdigest(),
        "formula_variables": BASE_VARIABLES,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--suffix", type=Path)
    parser.add_argument("--base-opb", type=Path)
    parser.add_argument("--output-opb", type=Path)
    args = parser.parse_args()
    require((args.base_opb is None) == (args.output_opb is None), "give both OPB paths")

    certificate_raw, summary = certificate()
    suffix, suffix_raw = suffix_summary()
    require(all(summary[key] == value for key, value in suffix.items()), "suffix disagreement")
    if args.certificate is not None:
        atomic_write(args.certificate, certificate_raw)
    if args.suffix is not None:
        atomic_write(args.suffix, suffix_raw)
    if args.base_opb is not None:
        summary.update(strengthen(args.base_opb, args.output_opb, suffix_raw))
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
