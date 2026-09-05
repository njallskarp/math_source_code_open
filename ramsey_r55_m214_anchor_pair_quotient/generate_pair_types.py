#!/usr/bin/env python3
"""Generate the 60 canonical high-codegree anchor-pair types.

The labels agree with the complete M=214 E_left_8 formulation:

* E = 0,...,12 is the degree-20 class;
* 5 is the unique vertex with eight red neighbours in E;
* 13 is the fixed central anchor;
* 0,...,5 and 14,...,28 are red neighbours of 13;
* 6,...,12 and 29,...,42 are blue neighbours of 13.

For every type, vertex 14 is the selected high-codegree central red
neighbour.  The emitted literals fix its 41 incidences not already fixed by
the anchor normalization.  Generated roots are deliberately not retained.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


N = 43
ANCHOR = 13
PARTNER = 14
EXCEPTION = 5
E_RED_ORDINARY = tuple(range(5))
E_BLUE = tuple(range(6, 13))
C_RED_OTHER = tuple(range(15, 29))
C_BLUE = tuple(range(29, 43))


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    if not 0 <= i < j < N:
        raise ValueError((i, j))
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def canonical_neighbours(c: int, s: int, k: int) -> frozenset[int]:
    if not 9 <= c <= 13 or s not in (0, 1) or not 0 <= k <= 5:
        raise ValueError((c, s, k))
    p = s + k
    e_blue_count = 6 - p
    c_red_count = c - p
    c_blue_count = 14 - c + p
    if not 0 <= e_blue_count <= 7:
        raise AssertionError("invalid E-blue count")
    if not 0 <= c_red_count <= 14 or not 0 <= c_blue_count <= 14:
        raise AssertionError("invalid central count")
    return frozenset(
        (ANCHOR,)
        + E_RED_ORDINARY[:k]
        + ((EXCEPTION,) if s else ())
        + E_BLUE[:e_blue_count]
        + C_RED_OTHER[:c_red_count]
        + C_BLUE[:c_blue_count]
    )


def row(c: int, s: int, k: int) -> dict[str, int | str]:
    p = s + k
    neighbours = canonical_neighbours(c, s, k)
    if len(neighbours) != 21 or ANCHOR not in neighbours or PARTNER in neighbours:
        raise AssertionError("partner degree construction failed")
    common = p + (c - p)
    if common != c:
        raise AssertionError("codegree construction failed")
    literals = tuple(
        edge_id(PARTNER, vertex) if vertex in neighbours else -edge_id(PARTNER, vertex)
        for vertex in range(N)
        if vertex not in (ANCHOR, PARTNER)
    )
    if len(literals) != 41 or len({abs(x) for x in literals}) != 41:
        raise AssertionError("unit construction failed")
    orbit_size = (
        binomial(5, k)
        * binomial(7, 6 - p)
        * binomial(14, c - p)
        * binomial(14, 14 - c + p)
    )
    return {
        "c": c,
        "s": s,
        "k": k,
        "p": p,
        "e_both_red": p,
        "e_anchor_only": 6 - p,
        "e_partner_only": 6 - p,
        "e_both_blue": 1 + p,
        "c_both_red": c - p,
        "c_anchor_only": 14 - c + p,
        "c_partner_only": 14 - c + p,
        "c_both_blue": c - p,
        "orbit_size": orbit_size,
        "unit_sha256": hashlib.sha256(
            (" ".join(map(str, literals)) + "\n").encode("ascii")
        ).hexdigest(),
    }


def binomial(n: int, k: int) -> int:
    if not 0 <= k <= n:
        return 0
    answer = 1
    for i in range(1, k + 1):
        answer = answer * (n - k + i) // i
    return answer


def build(output: Path) -> dict[str, int | str]:
    fieldnames = [
        "c", "s", "k", "p",
        "e_both_red", "e_anchor_only", "e_partner_only", "e_both_blue",
        "c_both_red", "c_anchor_only", "c_partner_only", "c_both_blue",
        "orbit_size", "unit_sha256",
    ]
    rows = [row(c, s, k) for c in range(9, 14) for s in range(2) for k in range(6)]
    if len(rows) != 60 or len({(x["c"], x["s"], x["k"]) for x in rows}) != 60:
        raise AssertionError("type census failed")
    with output.open("w", encoding="ascii", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames, dialect="unix")
        writer.writeheader()
        writer.writerows(rows)
    data = output.read_bytes()
    return {
        "bytes": len(data),
        "rows": len(rows),
        "sha256": hashlib.sha256(data).hexdigest(),
        "types_per_codegree": 12,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
