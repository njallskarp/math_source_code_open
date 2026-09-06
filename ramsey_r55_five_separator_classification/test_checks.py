#!/usr/bin/env python3
"""Definition-level controls for both decoders and the new flow algorithm."""
import json
from itertools import combinations
from pathlib import Path
import audit
import verify


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def encode(matrix):
    n = len(matrix)
    bits = [int(matrix[v][w]) for w in range(n) for v in range(w)]
    bits += [0] * (-len(bits) % 6)
    return chr(63 + n) + "".join(chr(63 + sum(bits[j + k] * 2 ** (5 - k)
                                              for k in range(6)))
                                 for j in range(0, len(bits), 6))


def pair_separator(matrix, v, w):
    others = [x for x in range(len(matrix)) if x not in (v, w)]
    for size in range(len(others) + 1):
        for removed in combinations(others, size):
            reached = {v}
            # Repeated whole-matrix closure, independent of flow and DFS.
            while True:
                new = reached | {b for a in reached for b in range(len(matrix))
                                 if matrix[a][b] and b not in removed}
                if reached == new:
                    break
                reached = new
            if w not in reached:
                return size
    raise ValueError("nonadjacent pair had no separator")


def rejected(call):
    try:
        call()
    except (ValueError, TypeError, IndexError):
        return 1
    raise ValueError("bad input accepted")


def main():
    graphs = flow_pairs = 0
    for n in range(6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            matrix = [[False] * n for _ in range(n)]
            for i, (v, w) in enumerate(pairs):
                matrix[v][w] = matrix[w][v] = bool(mask & (1 << i))
            s = encode(matrix)
            demand(audit.unpack(s) == matrix, "packed decoder differs")
            demand(verify.decode(s) == [{w for w in range(n) if matrix[v][w]}
                                        for v in range(n)], "stream decoder differs")
            for v, w in pairs:
                if not matrix[v][w]:
                    demand(audit.paths(matrix, v, w, n) == pair_separator(matrix, v, w),
                           "flow differs from exhaustive terminal separation")
                    flow_pairs += 1
            graphs += 1
    failures = sum(rejected(lambda s=s, f=f: f(s))
                   for s in ("", "~", "U", "A", "B?x", "A@", "!", "A\n")
                   for f in (audit.unpack, verify.decode))
    matrix = [[False, True], [True, False]]
    failures += rejected(lambda: audit.paths(matrix, 0, 1, 2))
    failures += rejected(lambda: audit.paths(matrix, 0, 0, 2))
    data = json.loads(Path(__file__).with_name("inputs.json").read_text())
    for rep in data["representatives"]:
        mat = audit.reconstruct(data, rep)
        demand(encode(mat) == rep["graph6"], "independent representative reconstruction differs")
    print(json.dumps({"small_graphs": graphs, "flow_pair_comparisons": flow_pairs,
                      "rejected_inputs": failures, "representative_agreements": 13},
                     sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
