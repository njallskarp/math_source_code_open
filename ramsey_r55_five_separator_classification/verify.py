#!/usr/bin/env python3
"""Literal forbidden sets and every deletion of at most five vertices.

No upstream program is imported. The thirteen-class census itself remains
an explicit theorem dependency, not re-established by checking its records.
"""
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from urllib.request import urlopen


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, separators=(",", ":")) + "\n"
    return hashlib.sha256(raw.encode()).hexdigest()


def decode(s):
    require(isinstance(s, str) and bool(s), "empty graph6")
    require(all(63 <= ord(c) <= 126 for c in s), "bad graph6 character")
    n = ord(s[0]) - 63
    require(n <= 62, "only short graph6 is supported")
    needed = n * (n - 1) // 2
    require(len(s) == 1 + (needed + 5) // 6, "bad graph6 length")
    bits = [(ord(c) - 63) >> b & 1 for c in s[1:] for b in range(5, -1, -1)]
    require(not any(bits[needed:]), "nonzero graph6 padding")
    adj = [set() for _ in range(n)]
    for bit, (v, w) in zip(bits, ((v, w) for w in range(n) for v in range(w))):
        if bit:
            adj[v].add(w)
            adj[w].add(v)
    return adj


def connected(adj, removed):
    remaining = set(range(len(adj))) - set(removed)
    if not remaining:
        return True
    seen = {min(remaining)}
    todo = list(seen)
    while todo:
        new = (adj[todo.pop()] & remaining) - seen
        seen.update(new)
        todo.extend(new)
    return seen == remaining


def all_cuts(adj, maximum):
    return [list(s) for k in range(maximum + 1)
            for s in combinations(range(len(adj)), k) if not connected(adj, s)]


def budget_table():
    capacity = {1: 3, 2: 8, 3: 17}
    partitions = []

    def visit(prefix, lower, left):
        if len(prefix) >= 2:
            partitions.append(tuple(prefix))
        for part in range(lower, min(3, left) + 1):
            visit(prefix + [part], part, left - part)

    visit([], 1, 4)
    viable = [p for p in partitions if sum(capacity[x] for x in p) >= 17]
    require(viable == [(1, 3)], "component independence budget changed")
    return [[s, 22 - s - b, b] for s in range(6) for b in range(1, 4)
            if 1 <= 22 - s - b <= 17]


def check_import(data):
    url = ("https://raw.githubusercontent.com/njallskarp/math_source_code_open/"
           + data["upstream"]["commit"]
           + "/ramsey_r55_degree_five_classification/certificate.json")
    with urlopen(url, timeout=30) as response:
        raw = response.read()
    require(hashlib.sha256(raw).hexdigest() ==
            data["upstream"]["certificate_sha256"], "upstream hash mismatch")
    old = json.loads(raw)
    require(data["cores"] == old["catalogue_records"], "core import mismatch")
    require(data["types"] == {str(r["type"]): r["s_edges"] for r in old["cases"]},
            "type import mismatch")
    wanted = [{k: r[k] for k in ("core", "type", "columns", "graph6")}
              for r in old["representatives"]]
    require(data["representatives"] == wanted, "representative import mismatch")


def check(data):
    require(len(data["representatives"]) == 13, "expected thirteen imported classes")
    records = []
    for i, rep in enumerate(data["representatives"]):
        adj = decode(rep["graph6"])
        require(len(adj) == 22, "wrong order")
        edges = [[v, w] for v, w in combinations(range(22), 2) if w in adj[v]]
        require(len(edges) == 109, "wrong density")
        for k, red in ((4, True), (5, False)):
            require(not any(all((w in adj[v]) == red for v, w in combinations(s, 2))
                            for s in combinations(range(22), k)), "forbidden set")
        degrees = [len(x) for x in adj]
        require(degrees[21] == 5 and min(degrees[:21]) >= 9, "degree gap failed")
        cuts = all_cuts(adj, 5)
        require(cuts == [sorted(adj[21])], "unexpected separator")
        records.append({"id": i, "edge_sha256": digest(edges),
                        "degree_sequence": sorted(degrees), "cuts": cuts})
    return {"component_cases_s_a_b": sorted(budget_table()), "graphs": records,
            "classes": 13, "connectivity": 5, "five_cuts_per_graph": 1,
            "outside_edges_per_interface": 630}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-import", action="store_true")
    args = parser.parse_args()
    data = json.loads(Path(__file__).with_name("inputs.json").read_text())
    if args.verify_import:
        check_import(data)
    print(json.dumps(check(data), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
