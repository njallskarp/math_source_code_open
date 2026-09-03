#!/usr/bin/env python3
"""Definition-level finite audit of the interior canonical Lucas b=5 slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import math


DEFAULT_MAX_K = 30
EXPECTED_DEFAULT_DIGEST = "5a4dc7d8534fa8fa03b1a37ce14a7486b878029e64c761df0acd872d237a090e"
Polynomial = list[int]


def trim(poly: Polynomial) -> Polynomial:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def add(*polys: Polynomial) -> Polynomial:
    result = [0] * max((len(poly) for poly in polys), default=0)
    for poly in polys:
        for index, coefficient in enumerate(poly):
            result[index] += coefficient
    return trim(result)


def scale(poly: Polynomial, coefficient: int) -> Polynomial:
    return trim([coefficient * value for value in poly])


def shift(poly: Polynomial, amount: int = 1) -> Polynomial:
    return ([0] * amount + poly) if poly else []


def mul(left: Polynomial, right: Polynomial) -> Polynomial:
    if not left or not right:
        return []
    result = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return trim(result)


def lucas_table(limit: int) -> list[Polynomial]:
    # At (e1,e2)=(1+q,q), F_(n+1)=(1+q)F_n+qF_(n-1).
    values: list[Polynomial] = [[], [1]]
    while len(values) <= limit:
        values.append(add(values[-1], shift(values[-1]), shift(values[-2])))
    return values


def lucas_binomials(values: list[Polynomial], limit: int) -> list[list[Polynomial]]:
    # Sagan--Savage recurrence, retaining only lower indices 0,...,5.
    choose: list[list[Polynomial]] = []
    for n in range(limit + 1):
        row = [[] for _ in range(6)]
        row[0] = [1]
        if 1 <= n <= 5:
            row[n] = [1]
        if n:
            previous = choose[-1]
            for r in range(1, min(5, n - 1) + 1):
                row[r] = add(
                    mul(values[r + 1], previous[r]),
                    shift(mul(values[n - r - 1], previous[r - 1])),
                )
        choose.append(row)
    return choose


def coefficient(poly: Polynomial, index: int) -> int:
    return poly[index] if 0 <= index < len(poly) else 0


def ballot(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    return math.comb(n, r) - (math.comb(n, r - 1) if r else 0)


def normalized_difference(choose: list[list[Polynomial]], a: int, k: int) -> Polynomial:
    first = choose[a * k + 5][5]
    second = choose[5 * k + a][a]
    sign = (-1) ** (a + 1)
    return add(scale(first, sign), scale(second, -sign))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=DEFAULT_MAX_K)
    args = parser.parse_args()
    if args.max_k < 3:
        parser.error("need --max-k >= 3")

    maximum_n = 5 * args.max_k + 4
    lucas = lucas_table(maximum_n + 1)
    choose = lucas_binomials(lucas, maximum_n)
    record: list[dict[str, object]] = []

    for a in (2, 3, 4):
        first_k = (5 + a - 1) // a
        for k in range(first_k, args.max_k + 1):
            degree = 5 * a * k
            delta = normalized_difference(choose, a, k)
            assert len(delta) <= degree + 1
            delta += [0] * (degree + 1 - len(delta))
            assert delta == list(reversed(delta)), ("symmetry", a, k)
            monomial = [coefficient(delta, r) for r in range(degree // 2 + 1)]
            schur = [value - (monomial[r - 1] if r else 0) for r, value in enumerate(monomial)]
            assert schur[: a + 1] == [0] * (a + 1), ("zero boundary", a, k)
            assert min(schur[a + 1 :]) > 0, ("strict support", a, k)
            assert schur[a + 1] == 1, ("leading coefficient", a, k)

            if a == 2:
                for r in range(4, degree // 2 + 1):
                    assert schur[r] >= ballot(degree - 8, r - 4)
            elif a == 3:
                for r in range(5, degree // 2 + 1):
                    assert schur[r] >= ballot(degree - 10, r - 5)
            else:
                for r in range(5, degree // 2 + 1):
                    assert schur[r] >= ballot(degree - 10, r - 5)

            payload = ",".join(str(value) for value in schur).encode()
            record.append(
                {
                    "a": a,
                    "coefficient_count": len(schur),
                    "k": k,
                    "schur_sha256": hashlib.sha256(payload).hexdigest(),
                }
            )

    digest = hashlib.sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if args.max_k == DEFAULT_MAX_K and not EXPECTED_DEFAULT_DIGEST.startswith("__"):
        assert digest == EXPECTED_DEFAULT_DIGEST
    print("definition-level interior b=5 slice audit passed")
    print(f"a=2,3,4 through k={args.max_k}; instances={len(record)}")
    print(f"record_sha256={digest}")


if __name__ == "__main__":
    main()
