#!/usr/bin/env python3
"""Independent exact audit of the M=214 pair-cover/root/OPB interface.

This imports no researcher module and invokes no solver.  Synthetic graphs below
test relabeling only; they are not Ramsey graphs or existence witnesses.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
import math
import tarfile
from collections import Counter
from pathlib import Path


N = 43
E = frozenset(range(2, 15))
C = frozenset(range(N)) - E
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")
FAMILY_COUNTS = (60, 85, 70, 104, 70)
EDGE_COUNT = math.comb(N, 2)
TRIPLES = tuple(itertools.combinations(range(N), 3))
FIVE_SET_COUNT = math.comb(N, 5)
BASE_VARIABLES = EDGE_COUNT + len(TRIPLES)
SELECTOR_FIRST = BASE_VARIABLES + 1
SELECTOR_LAST = SELECTOR_FIRST + 388
SELECTORS = frozenset(range(SELECTOR_FIRST, SELECTOR_LAST + 1))
BASE_ROWS = 1_974_689
FORMULA_ROWS = 2_044_421
FORMULA_BYTES = 172_788_992
FORMULA_SHA = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
BASE_SHA = "5f160c74a405726503649581080e3127d6a21c25b8fb59f6ffe72740dce600c4"
TAIL_SHA = "43da325c040c3cec73a0bdf6041f6e70f89b4a89fafb4d7d4b472279f970767a"
ROOTS_SHA = "f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e"
ARCHIVE_SHA = "9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6"
LEVEL60_SHA = "752aa8b1509075bc39cb1151936b250c681fbdf0a9fdda20d8d5bbb6e6356c62"
EXPECTED_SOURCE_HASHES = {
    "ramsey_r55_m214_reanchoring_cover/certificate.json":
        "68a39af932506b81fc5a102d0e14a50e00efaf97c38130d96e8899153964b4d1",
    "ramsey_r55_m214_exact_pair_nine/certificate.json":
        "015e1cec9107cafc6239605284acdecb1d56a93d9d0e0e7849af5122dca18149",
    "ramsey_r55_m214_pair_normalization/roots.tsv": ROOTS_SHA,
    "ramsey_r55_m214_pair_normalization/pair_roots.py":
        "8fdccc44cab88d462cc122c055a9c54cffbefc957a73b6eeff84aa57a9e2256e",
    "ramsey_r55_m214_integrated_pair_roots/generate_opb.py":
        "e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08",
    "ramsey_r55_m214_integrated_pair_roots/formula_manifest.json":
        "4e37a2b804ada9e8bb192af477d056ba5e10146647e004896651cc01d52f6578",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    need(0 <= i < j < N, "invalid edge")
    return i * (2 * N - i - 1) // 2 + j - i


def has_clique(adjacency: list[int], size: int, complement: bool = False) -> bool:
    for vertices in itertools.combinations(range(len(adjacency)), size):
        values = ((adjacency[i] >> j) & 1
                  for i, j in itertools.combinations(vertices, 2))
        if all((not value) if complement else value for value in values):
            return True
    return False


def graph6(line: bytes) -> list[int]:
    data = line.strip()
    need(data and data[0] != 126, "only short graph6 records are expected")
    order = data[0] - 63
    need(0 <= order <= 62, "graph6 order")
    bits = []
    for byte in data[1:]:
        value = byte - 63
        need(0 <= value < 64, "graph6 alphabet")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need(len(bits) >= math.comb(order, 2), "short graph6 payload")
    adjacency = [0] * order
    cursor = 0
    for j in range(1, order):
        for i in range(j):
            if bits[cursor]:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
            cursor += 1
    return adjacency


def catalog_check(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    need(sha256(raw) == ARCHIVE_SHA, "official archive identity")
    expected = {22: 2, 23: 16, 58: 47, 59: 4, 60: 1}
    observed = {}
    total = 0
    with tarfile.open(path, "r:gz") as archive:
        for level, count in expected.items():
            name = f"r45extreme/r4514.{level}.g6"
            member = archive.extractfile(name)
            need(member is not None, "missing order-14 archive member")
            member_raw = member.read()
            lines = member_raw.splitlines(keepends=True)
            need(len(lines) == count, "order-14 level census")
            if level == 60:
                need(sha256(member_raw) == LEVEL60_SHA, "level-60 member identity")
            for line in lines:
                adjacency = graph6(line)
                need(len(adjacency) == 14, "catalog graph order")
                edges = sum(mask.bit_count() for mask in adjacency) // 2
                need(edges == level, "catalog graph edge level")
                need(not has_clique(adjacency, 4), "catalog red K4")
                need(not has_clique(adjacency, 5, True), "catalog independent five-set")
            observed[level] = len(lines)
            total += len(lines)
    need(total == 70, "order-14 extreme census")
    return {"archive_sha256": sha256(raw), "level_counts": observed,
            "ramsey_graphs_checked": total, "level60_sha256": LEVEL60_SHA}


def adjacency_from_mask(order: int, mask: int) -> list[int]:
    adjacency = [0] * order
    for bit, (i, j) in enumerate(itertools.combinations(range(order), 2)):
        if mask >> bit & 1:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    return adjacency


def finite_lemmas() -> dict[str, object]:
    admissible_two = 0
    admissible_five = 0
    maximum_degree_square = 0
    minimum_disjoint = 99
    for mask in range(1 << 15):
        edges = mask.bit_count()
        if edges not in (2, 5):
            continue
        adjacency = adjacency_from_mask(6, mask)
        if has_clique(adjacency, 5, True):
            continue
        if edges == 2:
            admissible_two += 1
        else:
            admissible_five += 1
            degrees = [row.bit_count() for row in adjacency]
            maximum_degree_square = max(maximum_degree_square,
                                        sum(value * value for value in degrees))
            edge_list = [(i, j) for i, j in itertools.combinations(range(6), 2)
                         if adjacency[i] >> j & 1]
            disjoint = sum(not ({*left} & {*right})
                           for left, right in itertools.combinations(edge_list, 2))
            minimum_disjoint = min(minimum_disjoint, disjoint)
    need((admissible_two, admissible_five) == (45, 2997), "six-vertex census")
    need((maximum_degree_square, minimum_disjoint) == (26, 2),
         "five-edge degree-square lemma")

    seven_checked = 0
    pairs7 = tuple(itertools.combinations(range(7), 2))
    for count in range(3):
        for chosen in itertools.combinations(range(len(pairs7)), count):
            mask = sum(1 << bit for bit in chosen)
            need(has_clique(adjacency_from_mask(7, mask), 5, True),
                 "seven vertices with at most two edges")
            seven_checked += 1
    need(seven_checked == 232, "seven-vertex census")

    groups = {"E": (0, 1, 2), "X": (3, 4, 5), "T": (6, 7)}
    correction = {"EEE": 3, "EEX": 1, "EXX": 0, "XXX": 0,
                  "EET": 2, "EXT": 0, "XXT": -1}
    rows = []
    for word, claimed in correction.items():
        used = Counter()
        vertices = []
        for letter in word:
            vertices.append(groups[letter][used[letter]])
            used[letter] += 1
        adjacency = [0] * 8
        for i, j in itertools.combinations(vertices, 2):
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
        local = [sum(bool((adjacency[v] >> i) & 1 and
                          (adjacency[v] >> j) & 1 and
                          (adjacency[i] >> j) & 1)
                     for i, j in itertools.combinations(range(8), 2))
                 for v in range(8)]
        s_e = sum(local[v] for v in groups["E"])
        s_x = sum(local[v] for v in groups["X"])
        d_value = sum(bool((adjacency[i] >> j) & 1) *
                      sum(bool((adjacency[i] >> v) & 1 and
                               (adjacency[j] >> v) & 1) for v in range(8))
                      for i, j in itertools.combinations(groups["X"], 2))
        need(d_value == s_x - s_e + claimed, "signed triangle coefficient")
        rows.append([word, claimed])

    base = 28 * 100 - 13 * 93
    lower = base + 3 * 10 + 56 + 2 * 6 - 2 * 60
    j_edges = 28 * 14 // 2
    need((base, lower, j_edges, lower - 8 * j_edges) == (1591, 1569, 196, 1),
         "strict partner averaging")
    return {"admissible_two_edge_graphs": admissible_two,
            "admissible_five_edge_graphs": admissible_five,
            "maximum_degree_square": maximum_degree_square,
            "minimum_disjoint_edge_pairs": minimum_disjoint,
            "seven_vertex_graphs_checked": seven_checked,
            "signed_triangle_coefficients": rows,
            "partition_D_lower_bound": lower, "partition_J_edges": j_edges,
            "strict_margin": 1}


def cover_arithmetic() -> dict[str, object]:
    splits = []
    for excess_e in range(3):
        excess_c = 2 - excess_e
        if excess_e % 2 == 0:
            for location, amount in (("E", excess_e), ("C", excess_c)):
                if amount == 2:
                    splits.extend([(location + "8", (2,)),
                                   (location + "77", (1, 1))])
    need([name for name, _ in splits] == ["C8", "C77", "E8", "E77"],
         "intrinsic excess classification")
    reanchor_minima = {"E8_red_to_anomaly": 12,
                       "E77_common_blue": 4,
                       "C8_exact_common_blue": 16}
    pre_upgrade = {
        "first_four_exact_partner_sum": 200 - 6 * 13,
        "first_four_partner_lower_bound": (200 - 6 * 13 + 14) // 15,
        "partition_exact_partner_sum": 200 - 7 * 13,
        "partition_partner_lower_bound": (200 - 7 * 13 + 13) // 14,
        "partition_anomaly_if_all_exact_at_most_8": 200 - 6 * 13 - 14 * 8,
    }
    need(tuple(pre_upgrade.values()) == (122, 9, 109, 8, 10),
         "pre-upgrade partner arithmetic")
    return {"excess_profiles": [name for name, _ in splits],
            "reanchor_minima": reanchor_minima,
            "pre_upgrade": pre_upgrade}


def margins(total: int, row_sum: int):
    for h in range(total + 1):
        for a in range(total - h + 1):
            for b in range(total - h - a + 1):
                o = total - h - a - b
                if h + a == row_sum and h + b == row_sum:
                    yield h, a, b, o


def projection_orbits() -> tuple[dict[tuple[str, int, int, str], tuple], Counter]:
    roots = {}
    placements = Counter()
    for e_sizes in margins(13, 6):
        for c_sizes in margins(28, 14):
            common = e_sizes[0] + c_sizes[0]
            if not 9 <= common <= 13:
                continue
            e_word = "".join(name * size for name, size in zip("HABO", e_sizes))
            c_word = "".join(name * size for name, size in zip("HABO", c_sizes))
            choices = {
                "E8": [(i,) for i in range(13) if e_word[i] in "HA"],
                "E77": [pair for pair in itertools.combinations(range(13), 2)
                         if all(e_word[i] in "BO" for i in pair)],
                "C8": [(i,) for i in range(28) if c_word[i] in "BO"],
                "C77": [pair for pair in itertools.combinations(range(28), 2)
                         if all(c_word[i] in "BO" for i in pair)],
                "C77partition": [pair for pair in itertools.combinations(range(28), 2)
                                   if {c_word[pair[0]], c_word[pair[1]]}
                                   in ({"H", "O"}, {"A", "B"})],
            }
            for family, alternatives in choices.items():
                word = e_word if family.startswith("E") else c_word
                for choice in alternatives:
                    pattern = "".join(word[i] for i in choice)
                    roots[(family, common, e_sizes[0], pattern)] = (e_sizes, c_sizes)
                    placements[family] += 1
    need(Counter(key[0] for key in roots) ==
         dict(zip(FAMILIES, FAMILY_COUNTS)), "root-family census")
    need(placements == {"E8": 210, "E77": 735, "C8": 490,
                        "C77": 3185, "C77partition": 3920},
         "literal placement census")
    return roots, placements


def literal_root(key: tuple[str, int, int, str], sizes: tuple) -> dict[str, object]:
    family, _, _, pattern = key
    e_sizes, c_sizes = sizes
    cells = []
    cursor = 2
    for size in e_sizes + c_sizes:
        cells.append(list(range(cursor, cursor + size)))
        cursor += size
    need(cursor == N, "root cells partition")
    offset = 0 if family.startswith("E") else 4
    anomalies = []
    for index, name in enumerate("HABO"):
        anomalies.extend(cells[offset + index][:pattern.count(name)])
    bits = ((1, 1), (1, 0), (0, 1), (0, 0))
    units = [[0, 1, 1]]
    for index, cell in enumerate(cells):
        for vertex in cell:
            units.extend([[0, vertex, bits[index % 4][0]],
                          [1, vertex, bits[index % 4][1]]])
    units.sort()
    excess = 2 if family in ("E8", "C8") else 1
    buckets = []
    for cell in cells:
        for status in (False, True):
            bucket = [v for v in cell if (v in anomalies) == status]
            if bucket:
                buckets.append(bucket)
    partition = None
    if family == "C77partition":
        partition = {"blue_pair": anomalies,
                     "one_red_to_pair": [0, 1] +
                     [v for v in range(15, N) if v not in anomalies]}
    return {"key": list(key), "E_cells": list(e_sizes), "C_cells": list(c_sizes),
            "anchors": [0, 1], "E": list(range(2, 15)), "cells": cells,
            "anomalies": anomalies, "edge_units": units,
            "a_equalities": [[v, 6 + (excess if v in anomalies else 0)]
                             for v in range(N)],
            "partition": partition, "ordering_buckets": buckets}


def canonical_digest(value: object) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return sha256(raw)


def roots_check(path: Path):
    raw = path.read_bytes()
    need(sha256(raw) == ROOTS_SHA, "roots.tsv identity")
    expected, placements = projection_orbits()
    reader = csv.DictReader(io.StringIO(raw.decode("ascii")), delimiter="\t")
    header = ["family", "c", "k", "pattern", "E_cells", "C_cells",
              "anomalies", "root_sha256"]
    need(reader.fieldnames == header, "roots.tsv header")
    records = []
    seen = set()
    for row in reader:
        key = (row["family"], int(row["c"]), int(row["k"]), row["pattern"])
        need(key in expected and key not in seen, "invalid or duplicate root")
        record = literal_root(key, expected[key])
        need(row["E_cells"] == ",".join(map(str, record["E_cells"])), "E cells")
        need(row["C_cells"] == ",".join(map(str, record["C_cells"])), "C cells")
        need(row["anomalies"] == ",".join(map(str, record["anomalies"])),
             "anomaly labels")
        need(row["root_sha256"] == canonical_digest(record), "root descriptor digest")
        need(len(record["edge_units"]) == 83 and len(record["a_equalities"]) == 43,
             "complete root interface")
        seen.add(key)
        records.append(record)
    need(seen == set(expected) and len(records) == 389, "complete root set")
    return records, placements


def transport_controls(records: list[dict[str, object]]) -> int:
    checked = 0
    scramble = {v: (17 * v + 7) % N for v in range(N)}
    for record in records:
        key = record["key"]
        graph = [[0] * N for _ in range(N)]
        for i, j in itertools.combinations(range(N), 2):
            bit = int((i * i + 3 * i * j + 7 * j * j + key[1] + key[2]) % 11 < 5)
            graph[i][j] = graph[j][i] = bit
        for i, j, bit in record["edge_units"]:
            graph[i][j] = graph[j][i] = bit
        if record["partition"]:
            p, q = record["anomalies"]
            graph[p][q] = graph[q][p] = 0
            for w in record["partition"]["one_red_to_pair"]:
                if w not in (0, 1):
                    bit = (w + key[1]) % 2
                    graph[w][p] = graph[p][w] = bit
                    graph[w][q] = graph[q][w] = 1 - bit
        moved = [[0] * N for _ in range(N)]
        for i, j in itertools.combinations(range(N), 2):
            moved[scramble[i]][scramble[j]] = graph[i][j]
            moved[scramble[j]][scramble[i]] = graph[i][j]
        old_e = {scramble[v] for v in record["E"]}
        old_anomalies = {scramble[v] for v in record["anomalies"]}
        u, v = scramble[0], scramble[1]
        bit_index = {(1, 1): 0, (1, 0): 1, (0, 1): 2, (0, 0): 3}
        old_cells = [[] for _ in range(8)]
        for w in range(N):
            if w not in (u, v):
                old_cells[(0 if w in old_e else 4) +
                          bit_index[moved[u][w], moved[v][w]]].append(w)
        need([len(cell) for cell in old_cells] ==
             record["E_cells"] + record["C_cells"], "transported cell margins")
        old_buckets = []
        for cell in old_cells:
            for status in (False, True):
                bucket = [w for w in cell if (w in old_anomalies) == status]
                if bucket:
                    old_buckets.append(bucket)
        need(list(map(len, old_buckets)) == list(map(len, record["ordering_buckets"])),
             "transported refined buckets")
        permutation = {u: 0, v: 1}
        for old_bucket, new_bucket in zip(old_buckets, record["ordering_buckets"]):
            signature = lambda w: tuple(sum(moved[w][z] for z in bucket)
                                        for bucket in old_buckets)
            for old, new in zip(sorted(old_bucket, key=lambda w: (signature(w), w)),
                                new_bucket):
                permutation[old] = new
        need(set(permutation) == set(range(N)) and
             set(permutation.values()) == set(range(N)), "transport bijection")
        normalized = [[0] * N for _ in range(N)]
        for i, j in itertools.combinations(range(N), 2):
            normalized[permutation[i]][permutation[j]] = moved[i][j]
            normalized[permutation[j]][permutation[i]] = moved[i][j]
        need(all(moved[i][j] == normalized[permutation[i]][permutation[j]]
                 for i, j in itertools.combinations(range(N), 2)), "physical edge transport")
        need(all(normalized[i][j] == bit for i, j, bit in record["edge_units"]),
             "transported anchor units")
        for old in range(N):
            new = permutation[old]
            need(sum(moved[old][z] for z in old_e) ==
                 sum(normalized[new][z] for z in E), "transported E-incidence")
        if record["partition"]:
            p, q = record["anomalies"]
            need(normalized[p][q] == 0 and all(
                normalized[w][p] + normalized[w][q] == 1
                for w in record["partition"]["one_red_to_pair"]),
                "transported partition equations")
        for bucket in record["ordering_buckets"]:
            signatures = [tuple(sum(normalized[w][z] for z in other)
                                for other in record["ordering_buckets"])
                          for w in bucket]
            need(signatures == sorted(signatures), "sorted residual signatures")
        checked += 1
    return checked


def parse_opb(raw: bytes) -> tuple[dict[int, int], bytes, int]:
    need(raw.endswith(b"\n"), "OPB row newline")
    parts = raw.split()
    need(len(parts) >= 5 and len(parts) % 2 == 1 and parts[-1] == b";",
         "OPB row grammar")
    relation = parts[-3]
    need(relation in (b">=", b"="), "OPB relation")
    rhs = int(parts[-2])
    terms = {}
    for index in range(0, len(parts) - 3, 2):
        coefficient = int(parts[index])
        token = parts[index + 1]
        need(token.startswith(b"x") and token[1:].isdigit(), "OPB variable grammar")
        variable = int(token[1:])
        need(1 <= variable <= SELECTOR_LAST and variable not in terms,
             "OPB variable range or duplicate")
        need(coefficient != 0 and abs(coefficient) < 2**63, "OPB coefficient")
        terms[variable] = coefficient
    need(abs(rhs) < 2**63, "OPB rhs")
    return terms, relation, rhs


def expect(row, terms: dict[int, int], relation: bytes, rhs: int, message: str) -> None:
    actual_terms, actual_relation, actual_rhs = row
    need(actual_terms == terms and actual_relation == relation and actual_rhs == rhs, message)


def guarded_unit(variable: int, value: int, selector: int):
    if value:
        return {variable: 1, selector: -1}, b">=", 0
    return {variable: -1, selector: -1}, b">=", -1


def guarded_equality(variables, target: int, selector: int, maximum: int):
    return [({**{variable: 1 for variable in variables}, selector: -target}, b">=", 0),
            ({**{variable: -1 for variable in variables},
              selector: -(maximum - target)}, b">=", -maximum)]


def inactive_tautology(row) -> bool:
    terms, _, rhs = row
    selectors = set(terms) & SELECTORS
    need(len(selectors) == 1, "unique selector guard")
    selector = next(iter(selectors))
    physical = {variable: coefficient for variable, coefficient in terms.items()
                if variable != selector}
    return sum(min(0, coefficient) for coefficient in physical.values()) >= rhs


def formula_check(path: Path, records: list[dict[str, object]]) -> dict[str, object]:
    full_hash = hashlib.sha256()
    base_hash = hashlib.sha256()
    tail_hash = hashlib.sha256()
    byte_count = 0
    line_count = 0
    guards = 0
    partition_equalities = 0
    with path.open("rb") as stream:
        def read(section: str):
            nonlocal byte_count, line_count
            raw = stream.readline()
            need(raw, "early OPB EOF")
            full_hash.update(raw)
            if section == "base":
                base_hash.update(raw)
            elif section == "tail":
                tail_hash.update(raw)
            byte_count += len(raw)
            line_count += 1
            return raw

        header = read("header")
        need(header == b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n",
             "OPB header")
        for vertices in itertools.combinations(range(N), 5):
            variables = [edge_id(i, j) for i, j in itertools.combinations(vertices, 2)]
            expect(parse_opb(read("base")), {v: 1 for v in variables}, b">=", 1,
                   "red five-set row")
            expect(parse_opb(read("base")), {v: -1 for v in variables}, b">=", -9,
                   "blue five-set row")
        triangle_ids = {triple: EDGE_COUNT + index
                        for index, triple in enumerate(TRIPLES, 1)}
        for triple in TRIPLES:
            z = triangle_ids[triple]
            sides = [edge_id(i, j) for i, j in itertools.combinations(triple, 2)]
            for side in sides:
                expect(parse_opb(read("base")), {z: -1, side: 1}, b">=", 0,
                       "triangle upper row")
            expect(parse_opb(read("base")), {z: 1, **{side: -1 for side in sides}},
                   b">=", -2, "triangle lower row")
        for vertex in range(N):
            variables = [edge_id(vertex, other) for other in range(N) if other != vertex]
            expect(parse_opb(read("base")), {v: 1 for v in variables}, b"=",
                   20 if vertex in E else 21, "degree star")
        for vertex in range(N):
            variables = [triangle_ids[tuple(sorted((vertex, i, j)))]
                         for i, j in itertools.combinations(
                             [w for w in range(N) if w != vertex], 2)]
            expect(parse_opb(read("base")), {v: 1 for v in variables}, b"=",
                   93 if vertex in E else 100, "local triangle star")
        for vertex in range(N):
            variables = [edge_id(vertex, other) for other in E if other != vertex]
            expect(parse_opb(read("base")), {v: 1 for v in variables}, b">=", 6,
                   "E-incidence lower bound")
        need(line_count == BASE_ROWS + 1, "base formula row boundary")
        expect(parse_opb(read("tail")), {v: 1 for v in SELECTORS}, b"=", 1,
               "selector one-hot")
        for root_index, record in enumerate(records):
            selector = SELECTOR_FIRST + root_index
            expected_rows = []
            for i, j, value in record["edge_units"]:
                expected_rows.append(guarded_unit(edge_id(i, j), value, selector))
            for vertex, target in record["a_equalities"]:
                variables = [edge_id(vertex, other) for other in E if other != vertex]
                expected_rows.extend(guarded_equality(variables, target, selector, 13))
            if record["partition"]:
                p, q = record["partition"]["blue_pair"]
                expected_rows.append(guarded_unit(edge_id(p, q), 0, selector))
                for vertex in record["partition"]["one_red_to_pair"]:
                    expected_rows.extend(guarded_equality(
                        [edge_id(vertex, p), edge_id(vertex, q)], 1, selector, 2))
                    partition_equalities += 1
            for expected_row in expected_rows:
                row = parse_opb(read("tail"))
                need(inactive_tautology(row), "inactive selector guard restricts graph")
                expect(row, *expected_row, "guarded root condition")
                guards += 1
        need(stream.read(1) == b"", "extra OPB content")
    need((line_count, byte_count) == (FORMULA_ROWS + 1, FORMULA_BYTES),
         "formula dimensions")
    need((guards, partition_equalities) == (69_731, 1_960), "selector census")
    need(full_hash.hexdigest() == FORMULA_SHA, "formula hash")
    need(base_hash.hexdigest() == BASE_SHA and tail_hash.hexdigest() == TAIL_SHA,
         "formula section hashes")
    return {"variables": SELECTOR_LAST, "constraints": FORMULA_ROWS,
            "equalities": 87, "five_sets_both_colors": FIVE_SET_COUNT,
            "triangle_conjunctions": len(TRIPLES), "physical_star_rows": 129,
            "roots": len(records), "inactive_guards_checked": guards,
            "partition_equalities": partition_equalities,
            "formula_sha256": full_hash.hexdigest(),
            "base_body_sha256": base_hash.hexdigest(),
            "selector_suffix_sha256": tail_hash.hexdigest()}


def source_identity(source: Path) -> dict[str, str]:
    observed = {}
    for relative, expected in EXPECTED_SOURCE_HASHES.items():
        value = sha256((source / relative).read_bytes())
        need(value == expected, "pinned source identity: " + relative)
        observed[relative] = value
    return observed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True,
                        help="checkout containing the five reviewed source packages")
    parser.add_argument("--formula", type=Path, required=True,
                        help="freshly generated complete integrated OPB")
    parser.add_argument("--catalog", type=Path, required=True,
                        help="fresh official r45extreme.tar.gz archive")
    args = parser.parse_args()
    identities = source_identity(args.source)
    roots_path = args.source / "ramsey_r55_m214_pair_normalization/roots.tsv"
    records, placements = roots_check(roots_path)
    result = {
        "status": "INDEPENDENT_EXACT_M214_PAIR_ROOT_COVER_ACCEPTED",
        "scope": "cover/root/formula equivalence; no SAT or branch exclusion",
        "source_hashes": identities,
        "cover_arithmetic": cover_arithmetic(),
        "finite_lemmas": finite_lemmas(),
        "catalog": catalog_check(args.catalog),
        "root_certificate": {
            "roots": len(records),
            "family_counts": dict(Counter(record["key"][0] for record in records)),
            "literal_anomaly_placements": dict(placements),
            "roots_sha256": ROOTS_SHA,
            "synthetic_full_edge_transports": transport_controls(records),
        },
        "formula": formula_check(args.formula, records),
        "trust_boundary": [
            "McKay public page completeness assertion for the order-14 extrema archive",
            "classical R(3,5)=14",
            "upstream intrinsic M=214 branch derivation",
            "CPython exact semantics, SHA-256 implementation, hardware",
        ],
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
