#!/usr/bin/env python3
"""Check an exact pairwise-compatible aggregate M=214,c=13 selection."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


CORE_ORDER = 13
OUTSIDE_ORDER = 28
FULL = (1 << CORE_ORDER) - 1
U, V = 0, 1
CORE = tuple(range(2, 15))
D = tuple(range(15, 43))
A = tuple(range(0, 7))
B = tuple(range(7, 14))
O = tuple(range(14, 28))
CORE_DIFFERENCES = frozenset((1, 5, 8, 12))


def core_edge(i: int, j: int) -> bool:
    return i != j and ((i - j) % CORE_ORDER) in CORE_DIFFERENCES


def independent_masks(size: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << i for i in subset)
        for subset in itertools.combinations(range(CORE_ORDER), size)
        if all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2))
    )


def parse(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_bytes()
    data = json.loads(raw)
    expected = {"core_e", "footprints", "m_o", "outside_e", "pivot"}
    if not isinstance(data, dict) or set(data) != expected:
        raise ValueError("certificate fields")
    return data, hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data, certificate_hash = parse(args.certificate)

    if data["core_e"] != []:
        raise AssertionError("certificate is the k=0 branch")
    outside_e_list = data["outside_e"]
    expected_outside_e = [*range(0, 6), *range(7, 13), 14]
    if outside_e_list != expected_outside_e:
        raise AssertionError("canonical outside marks")
    outside_e = frozenset(outside_e_list)
    if data["pivot"] != "D0" or 0 not in outside_e:
        raise AssertionError("outside pivot")

    footprint_text = data["footprints"]
    if not isinstance(footprint_text, list) or len(footprint_text) != OUTSIDE_ORDER:
        raise ValueError("footprints")
    footprints: list[int] = []
    for text in footprint_text:
        if not isinstance(text, str) or len(text) != 4 or text != text.lower():
            raise ValueError("footprint encoding")
        mask = int(text, 16)
        if not 0 <= mask <= FULL:
            raise ValueError("footprint range")
        footprints.append(mask)
    m_o = data["m_o"]
    if not isinstance(m_o, int):
        raise ValueError("m_o")

    core_edges = tuple(
        (1 << i) | (1 << j)
        for i, j in itertools.combinations(range(CORE_ORDER), 2)
        if core_edge(i, j)
    )
    triples = independent_masks(3)
    fours = independent_masks(4)
    transversals = tuple(mask for mask in range(1 << CORE_ORDER) if all(mask & four for four in fours))
    if (len(core_edges), len(triples), len(fours), len(transversals)) != (26, 78, 39, 3459):
        raise AssertionError("core census")
    transversal_set = frozenset(transversals)
    if any(mask not in transversal_set for mask in footprints):
        raise AssertionError("nontransversal footprint")

    column_sums = [sum(mask >> i & 1 for mask in footprints) for i in range(CORE_ORDER)]
    marked_columns = [
        sum(footprints[x] >> i & 1 for x in outside_e)
        for i in range(CORE_ORDER)
    ]
    if column_sums != [15] * CORE_ORDER:
        raise AssertionError(("column sums", column_sums))
    if marked_columns != [6] * CORE_ORDER:
        raise AssertionError(("marked columns", marked_columns))
    if tuple(sum(x in outside_e for x in cell) for cell in (A, B, O)) != (6, 6, 1):
        raise AssertionError("cell marks")

    def blue_forbidden(x: int, y: int) -> bool:
        missing = FULL ^ (footprints[x] | footprints[y])
        return any(missing & triple == triple for triple in triples)

    def red_forbidden(x: int, y: int) -> bool:
        common = footprints[x] & footprints[y]
        return any(common & edge == edge for edge in core_edges)

    categories = {
        "A": tuple(itertools.combinations(A, 2)),
        "B": tuple(itertools.combinations(B, 2)),
        "O": tuple(itertools.combinations(O, 2)),
        "AB": tuple((x, y) for x in A for y in B),
        "AO": tuple((x, y) for x in A for y in O),
        "BO": tuple((x, y) for x in B for y in O),
    }
    incidence_a = sum(footprints[x].bit_count() for x in A)
    incidence_b = sum(footprints[x].bit_count() for x in B)
    incidence_o = sum(footprints[x].bit_count() for x in O)
    if incidence_a + incidence_b + incidence_o != 195:
        raise AssertionError("total footprint incidence")
    targets = {
        "A": 61 - incidence_a,
        "B": 61 - incidence_b,
        "O": m_o,
        "AB": m_o - 37,
        "AO": 49 + incidence_a - m_o,
        "BO": 49 + incidence_b - m_o,
    }

    red_edges: set[tuple[int, int]] = set()
    forced_counts: dict[str, int] = {}
    red_forbidden_counts: dict[str, int] = {}
    for name, pairs in categories.items():
        forced = tuple(pair for pair in pairs if blue_forbidden(*pair))
        allowed = tuple(
            pair for pair in pairs
            if name not in ("A", "B") or not red_forbidden(*pair)
        )
        forced_counts[name] = len(forced)
        red_forbidden_counts[name] = len(pairs) - len(allowed)
        if not set(forced).issubset(allowed):
            raise AssertionError(("no-color pair", name))
        target = targets[name]
        optional = tuple(pair for pair in allowed if pair not in frozenset(forced))
        if not len(forced) <= target <= len(allowed):
            raise AssertionError(("edge capacity", name, len(forced), target, len(allowed)))
        chosen = forced + optional[: target - len(forced)]
        red_edges.update(chosen)

    expected_targets = {"A": 11, "B": 13, "O": 47, "AB": 10, "AO": 52, "BO": 50}
    expected_forced = {"A": 0, "B": 0, "O": 5, "AB": 10, "AO": 17, "BO": 21}
    if targets != expected_targets or forced_counts != expected_forced:
        raise AssertionError((targets, forced_counts))
    if red_forbidden_counts["A"] != 10 or red_forbidden_counts["B"] != 8:
        raise AssertionError("same-cell red-forbidden census")
    if len(red_edges) != 183:
        raise AssertionError("outside red-edge total")

    # Check every aggregate equation from the height-2869 relaxation.
    m_a, m_b = targets["A"], targets["B"]
    if not (m_a + incidence_a == 61 and m_b + incidence_b == 61):
        raise AssertionError("anchor red equations")
    if not (m_b + m_o + targets["BO"] == 110
            and m_a + m_o + targets["AO"] == 110):
        raise AssertionError("anchor blue equations")
    degree_sums = {
        cell_name: sum(
            (1 if x in A or x in B else 0)
            + footprints[x].bit_count()
            + sum((min(x, y), max(x, y)) in red_edges for y in range(OUTSIDE_ORDER) if y != x)
            for x in cell
        )
        for cell_name, cell in (("A", A), ("B", B), ("O", O))
    }
    expected_degree_sums = {
        name: sum(21 - int(x in outside_e) for x in cell)
        for name, cell in (("A", A), ("B", B), ("O", O))
    }
    if degree_sums != expected_degree_sums:
        raise AssertionError(("degree sums", degree_sums, expected_degree_sums))
    if not (3 <= m_a <= 16 and 3 <= m_b <= 16 and 18 <= m_o <= 73):
        raise AssertionError("cell edge intervals")
    if not 18 <= m_a + m_b + targets["AB"] <= 73:
        raise AssertionError("A union B interval")

    def red(i: int, j: int) -> bool:
        if i > j:
            i, j = j, i
        if (i, j) == (U, V):
            return True
        if i in (U, V) and j in CORE:
            return True
        if i in CORE and j in CORE:
            return core_edge(i - CORE[0], j - CORE[0])
        if i == U and j in D:
            return j - D[0] in A
        if i == V and j in D:
            return j - D[0] in B
        if i in CORE and j in D:
            return bool(footprints[j - D[0]] >> (i - CORE[0]) & 1)
        if i in D and j in D:
            return (i - D[0], j - D[0]) in red_edges
        raise AssertionError((i, j))

    monochromatic = {0: 0, 1: 0, 2: 0}
    for five in itertools.combinations(range(43), 5):
        outside_count = sum(vertex in D for vertex in five)
        if outside_count > 2:
            continue
        colors = tuple(red(i, j) for i, j in itertools.combinations(five, 2))
        if all(colors) or not any(colors):
            monochromatic[outside_count] += 1
    if any(monochromatic.values()):
        raise AssertionError(("local monochromatic K5", monochromatic))

    result = {
        "certificate_sha256": certificate_hash,
        "columns": column_sums,
        "core_edges": len(core_edges),
        "edge_targets": targets,
        "forced_red": forced_counts,
        "independent_fours": len(fours),
        "independent_triples": len(triples),
        "incidences": {"A": incidence_a, "B": incidence_b, "O": incidence_o},
        "marked_columns": marked_columns,
        "monochromatic_K5_with_at_most_two_outside": sum(monochromatic.values()),
        "outside_red_edges": len(red_edges),
        "red_forbidden": {"A": red_forbidden_counts["A"], "B": red_forbidden_counts["B"]},
        "status": "VERIFIED PAIRWISE-COMPATIBLE AGGREGATE SELECTION",
        "transversals": len(transversals),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
