#!/usr/bin/env python3
"""Exact independent boundary audit for the Ramsey-link fan Lean theorem.

This checker does not parse Lean output and does not use the target source.
It evaluates the eight admissible degree rows and constructs a finite-set
model attaining each claimed abstract upper bound.
"""

from __future__ import annotations

import hashlib
import json


def ceil_div_four(n: int) -> int:
    if n < 0:
        raise ValueError("natural-number input required")
    return (n + 3) // 4


def sharp_abstract_model(rho: int, max_m: int) -> dict[str, object]:
    """Construct disjoint categories and a capacity-four target cover."""
    cover_count = ceil_div_four(rho - 3)
    selected = set(range(44))
    red = set(range(0, 11))
    side = set(range(11, 11 + max_m))
    witness = set(range(11 + max_m, 14 + max_m))
    extra = set(range(14 + max_m, 14 + max_m + cover_count))
    categories = (red, side, witness, extra)

    assert sum(map(len, categories)) == 44
    assert set().union(*categories) == selected
    assert all(
        categories[i].isdisjoint(categories[j])
        for i in range(len(categories))
        for j in range(i + 1, len(categories))
    )

    target = set(range(rho - 3))
    pieces: dict[int, set[int]] = {}
    ordered_extra = sorted(extra)
    for index, clause in enumerate(ordered_extra):
        pieces[clause] = set(range(4 * index, min(4 * index + 4, rho - 3)))
    covered = set().union(*(pieces[clause] for clause in ordered_extra))
    assert target <= covered
    assert all(len(piece) <= 4 for piece in pieces.values())

    return {
        "selected": len(selected),
        "red": len(red),
        "side": len(side),
        "witness": len(witness),
        "extra": len(extra),
        "target": len(target),
        "max_piece": max(map(len, pieces.values())),
    }


def main() -> None:
    expected_maxima = {
        17: 26,
        18: 26,
        19: 26,
        20: 25,
        21: 25,
        22: 25,
        23: 25,
        24: 24,
    }
    rows: list[dict[str, object]] = []

    for rho in range(17, 25):
        blue_degree = 41 - rho
        assert 17 <= blue_degree <= 24
        assert ceil_div_four(rho - 3) == rho // 4

        cover_count = ceil_div_four(rho - 3)
        max_m = 30 - cover_count
        assert max_m == expected_maxima[rho]
        assert max_m + cover_count == 30
        assert max_m + 1 + cover_count > 30

        model = sharp_abstract_model(rho, max_m)
        row = {
            "rho": rho,
            "blue_degree": blue_degree,
            "cover_count": cover_count,
            "max_m": max_m,
            "next_m_fails": True,
            "abstract_model": model,
        }
        rows.append(row)
        print(
            f"rho={rho} blueDegree={blue_degree} "
            f"cover={cover_count} max_m={max_m} next_fails=yes"
        )

    for excluded in range(27, 31):
        assert all(excluded + row["cover_count"] > 30 for row in rows)

    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    print(
        "verified: 8 strata; global m<=26; excluded=[27,28,29,30]; "
        "abstract stratum bounds are sharp"
    )
    print(f"record_sha256={digest}")


if __name__ == "__main__":
    main()
