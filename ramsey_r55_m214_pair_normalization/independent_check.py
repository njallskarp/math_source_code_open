#!/usr/bin/env python3
"""Definition-level orbit checker. Does not import the root producer."""

import csv
import hashlib
import io
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def margins(total, row_sum):
    # Independently enumerate all four-bin compositions, not the c,k formula.
    for a in range(total+1):
        for b in range(total-a+1):
            for c in range(total-a-b+1):
                d = total-a-b-c
                if a+b == row_sum and a+c == row_sum:
                    yield (a, b, c, d)


def projection_orbits():
    out = {}
    placements = Counter()
    for e in margins(13, 6):
        for central in margins(28, 14):
            codegree = e[0] + central[0]
            if not 9 <= codegree <= 13:
                continue
            e_word = "".join(ch*n for ch, n in zip("HABO", e))
            c_word = "".join(ch*n for ch, n in zip("HABO", central))
            candidates = {}
            candidates["E8"] = [
                (i,) for i in range(13) if e_word[i] in "HA"]
            candidates["E77"] = [
                vs for vs in itertools.combinations(range(13), 2)
                if all(e_word[v] in "BO" for v in vs)]
            candidates["C8"] = [
                (i,) for i in range(28) if c_word[i] in "BO"]
            candidates["C77"] = [
                vs for vs in itertools.combinations(range(28), 2)
                if all(c_word[v] in "BO" for v in vs)]
            candidates["C77partition"] = [
                (i, j) for i, j in itertools.combinations(range(28), 2)
                if {c_word[i], c_word[j]} in ({"H", "O"}, {"A", "B"})]
            for family, choices in candidates.items():
                word = e_word if family.startswith("E") else c_word
                for choice in choices:
                    pattern = "".join(word[i] for i in choice)
                    key = (family, codegree, e[0], pattern)
                    out[key] = (e, central)
                    placements[family] += 1
    return out, placements


def literal_root(key, e, central):
    family, codegree, k, pattern = key
    names = []
    for color, sizes in (("E", e), ("C", central)):
        for pair_cell, count in zip("HABO", sizes):
            names.extend([(color, pair_cell)] * count)
    vertex_name = dict(zip(range(2, 43), names))
    cells = [[w for w in range(2, 43) if vertex_name[w] == (color, cell)]
             for color in "EC" for cell in "HABO"]
    anomaly_color = family[0]
    anomalies = []
    for cell in "HABO":
        suitable = [w for w in range(2, 43)
                    if vertex_name[w] == (anomaly_color, cell)]
        anomalies += suitable[:pattern.count(cell)]
    require(len(anomalies) == len(pattern), "anomaly capacity")
    units = []
    for i, j in itertools.combinations(range(43), 2):
        if i == 0:
            red = 1 if j == 1 else int(vertex_name[j][1] in "HA")
            units.append([i, j, red])
        elif i == 1:
            units.append([i, j, int(vertex_name[j][1] in "HB")])
    buckets = []
    for color in "EC":
        for cell in "HABO":
            for is_anomaly in (False, True):
                group = [w for w in range(2, 43)
                         if vertex_name[w] == (color, cell)
                         and (w in anomalies) == is_anomaly]
                if group:
                    buckets.append(group)
    partition = None
    if family == "C77partition":
        partition = {"blue_pair": anomalies,
                     "one_red_to_pair": [w for w in [0, 1] + list(range(15, 43))
                                         if w not in anomalies]}
    return {
        "key": list(key), "E_cells": list(e), "C_cells": list(central),
        "anchors": [0, 1], "E": list(range(2, 15)), "cells": cells,
        "anomalies": anomalies, "edge_units": units,
        "a_equalities": [[w, 6 + ((2 if len(pattern) == 1 else 1)
                                  if w in anomalies else 0)]
                         for w in range(43)],
        "partition": partition, "ordering_buckets": buckets,
    }


def payload_digest(payload):
    raw = (json.dumps(payload, separators=(",", ":"), sort_keys=True)+"\n").encode()
    return hashlib.sha256(raw).hexdigest()


def check_table(text):
    expected, placements = projection_orbits()
    required_header = ["family", "c", "k", "pattern", "E_cells", "C_cells",
                       "anomalies", "root_sha256"]
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    require(reader.fieldnames == required_header, "table header")
    seen = set()
    counts = Counter()
    for row in reader:
        require(set(row) == set(required_header)
                and all(row[x] is not None for x in required_header), "row width")
        key = (row["family"], int(row["c"]), int(row["k"]), row["pattern"])
        require(key in expected and key not in seen, "missing/duplicate/invalid key")
        seen.add(key)
        e, central = expected[key]
        payload = literal_root(key, e, central)
        require(row["E_cells"] == ",".join(map(str, e)), "E bins")
        require(row["C_cells"] == ",".join(map(str, central)), "C bins")
        require(row["anomalies"] == ",".join(map(str, payload["anomalies"])),
                "anomaly labels")
        require(row["root_sha256"] == payload_digest(payload), "literal root digest")
        require(len(payload["edge_units"]) == 83, "anchor units")
        if payload["partition"] is not None:
            require(len(payload["partition"]["one_red_to_pair"]) == 28,
                    "partition scope")
        counts[key[0]] += 1
    require(seen == set(expected), "incomplete table")
    require(dict(counts) == {"E8": 60, "E77": 85, "C8": 70,
                            "C77": 104, "C77partition": 70}, "family totals")
    return counts, placements


def main():
    require(len(sys.argv) <= 2, "usage: independent_check.py [roots.tsv]")
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name("roots.tsv")
    raw = path.read_bytes()
    counts, placements = check_table(raw.decode("ascii"))
    print("PASS complete marked pair-incidence roots=389")
    print("family_counts=" + json.dumps(dict(counts), sort_keys=True))
    print("literal_anomaly_placements=" + json.dumps(dict(placements), sort_keys=True))
    print("PASS all 389 full root descriptors and 83 anchor units per root")
    print("roots_sha256=" + hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
