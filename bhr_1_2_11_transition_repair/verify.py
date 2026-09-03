#!/usr/bin/env python3
"""Definition-level checker for the BHR {1,2,11}, c=4 orthant repair."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform

try:
    from .construct import boundary_one_path, boundary_two_path, interior_path
except ImportError:  # Direct script execution from this directory.
    from construct import boundary_one_path, boundary_two_path, interior_path

SUPPORT = (1, 2, 11)


class VerificationError(ValueError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise VerificationError(str(message))


def cyclic_length(u: int, v: int, n: int) -> int:
    d = abs(u - v)
    return min(d, n - d)


def changed_by_embedding(u: int, v: int, x: int, m: int, n: int) -> bool:
    old = cyclic_length(u, v, n)
    uu = u if u <= m else u + x
    vv = v if v <= m else v + x
    # Growability is defined by a strict increase, not merely a difference.
    # Gap insertion cannot decrease cyclic length, but retaining the strict
    # predicate here makes that definition an explicit checker obligation.
    return cyclic_length(uu, vv, n + x) > old


def changed_edges(path: list[int], x: int, m: int) -> list[tuple[int, int]]:
    n = len(path)
    return [
        (u, v)
        for u, v in zip(path, path[1:])
        if changed_by_embedding(u, v, x, m, n)
    ]


def verify_growth(path: list[int], x: int, m: int) -> None:
    n = len(path)
    require(x - 1 <= m <= n - 1 - x, ("growth range", n, x, m))
    critical = set(range(m - x + 1, m + 1))
    incidence: Counter[int] = Counter()
    for u, v in changed_edges(path, x, m):
        require(u in critical or v in critical, ("outside changed edge", x, m, u, v))
        if u in critical:
            incidence[u] += 1
        if v in critical:
            incidence[v] += 1
    require(
        all(incidence[y] == 1 for y in critical),
        ("wrong growth incidence", x, m, dict(incidence)),
    )


def growth_cuts(path: list[int], x: int) -> list[int]:
    cuts = []
    for m in range(x - 1, len(path) - x):
        try:
            verify_growth(path, x, m)
        except VerificationError:
            continue
        cuts.append(m)
    return cuts


def grow_once(path: list[int], x: int, m: int) -> list[int]:
    """Apply the insertion construction, without assuming cross-preservation."""
    verify_growth(path, x, m)
    n = len(path)
    critical = set(range(m - x + 1, m + 1))
    embedded = {y: y if y <= m else y + x for y in range(n)}
    out = [embedded[path[0]]]
    for u, v in zip(path, path[1:]):
        if changed_by_embedding(u, v, x, m, n):
            inside = [y for y in (u, v) if y in critical]
            require(len(inside) == 1, ("ambiguous insertion", x, m, u, v))
            out.append(inside[0] + x)
        out.append(embedded[v])
    return out


def verify_realization(path: list[int], counts: tuple[int, int, int]) -> None:
    n = sum(counts) + 1
    require(sorted(path) == list(range(n)), ("not a permutation", counts))
    actual = Counter(
        cyclic_length(u, v, n) for u, v in zip(path, path[1:])
    )
    require(actual == Counter(dict(zip(SUPPORT, counts))), (counts, actual))


def verify_certificate(path: Path, grid: int) -> dict[str, object]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data["schema"] == "bhr-growable-orthant-repair-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT, "wrong support")

    boundary = data["boundary_seed"]
    g = boundary["path"]
    require(tuple(boundary["counts"]) == (1, 16, 4), "wrong boundary counts")
    verify_realization(g, (1, 16, 4))
    verify_growth(g, 1, 0)
    verify_growth(g, 2, 1)

    # The precise regression that invalidated independent cross-growth.
    require(growth_cuts(grow_once(g, 1, 0), 2) == [], "1 then 2 unexpectedly survived")
    require(growth_cuts(grow_once(g, 2, 1), 1) == [], "2 then 1 unexpectedly survived")

    records: list[object] = []
    a_path = g
    b_path = g
    for k in range(grid + 1):
        verify_realization(a_path, (1 + k, 16, 4))
        verify_growth(a_path, 1, 0)
        require(a_path == boundary_one_path(k), ("boundary-one formula", k))
        verify_realization(b_path, (1, 16 + 2 * k, 4))
        verify_growth(b_path, 2, 1)
        require(b_path == boundary_two_path(k), ("boundary-two formula", k))
        records.append(["a", k, a_path])
        records.append(["b", k, b_path])
        a_path = grow_once(a_path, 1, 0)
        b_path = grow_once(b_path, 2, 1)

    interior = data["interior_seed"]
    p00 = interior["path"]
    require(tuple(interior["counts"]) == (2, 18, 4), "wrong interior counts")
    require(p00 == interior_path(0, 0), "interior seed/formula mismatch")
    verify_realization(p00, (2, 18, 4))
    verify_growth(p00, 1, 18)
    verify_growth(p00, 2, 19)

    family: dict[tuple[int, int], list[int]] = {}
    for p in range(grid + 2):
        row = p00
        for _ in range(p):
            row = grow_once(row, 1, 18)
        for q in range(grid + 2):
            if q:
                row = grow_once(row, 2, 19 + p)
            family[p, q] = row
            verify_realization(row, (2 + p, 18 + 2 * q, 4))
            verify_growth(row, 1, 18)
            verify_growth(row, 2, 19 + p)
            require(row == interior_path(p, q), ("interior formula", p, q))

    for p in range(grid + 1):
        for q in range(grid + 1):
            current = family[p, q]
            require(
                grow_once(current, 1, 18) == family[p + 1, q],
                ("noncommuting 1-transition", p, q),
            )
            require(
                grow_once(current, 2, 19 + p) == family[p, q + 1],
                ("noncommuting 2-transition", p, q),
            )
            records.append(["p", p, q, current])

    record_bytes = json.dumps(records, separators=(",", ":")).encode()
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "python": platform.python_version(),
        "grid": grid,
        "boundary_paths_checked": 2 * (grid + 1),
        "interior_paths_checked": (grid + 2) ** 2,
        "commuting_squares_checked": (grid + 1) ** 2,
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=24)
    args = parser.parse_args()
    summary = verify_certificate(args.certificate, args.grid)
    for key, value in summary.items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
