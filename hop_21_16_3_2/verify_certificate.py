#!/usr/bin/env python3
"""Definition-level verification of a cyclic HOP(32,6,4) certificate.

This checker intentionally imports nothing from search_starters.py.  It uses
the 42 people (v,b), with v in {0,...,20} a couple and b in {0,1} a spouse
label.  An external perfect matching plus all spouse edges is one meal.  The
certificate stores the external matchings F1 and F3; the published odd-order
starter rule determines F2.  Cyclic development must partition every edge
between distinct couples exactly once.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

N = 20
INF = 20
ROOT = Path(__file__).resolve().parent
Person = tuple[int, int]
Edge = tuple[Person, Person]


def edge(a: Person, b: Person) -> Edge:
    if not (0 <= a[0] <= INF and 0 <= b[0] <= INF):
        raise ValueError("couple label outside 0,...,20")
    if a[1] not in (0, 1) or b[1] not in (0, 1):
        raise ValueError("spouse bit is not zero or one")
    if a[0] == b[0]:
        raise ValueError("external edge joins spouses in one couple")
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def parse_factor(raw: object) -> tuple[Edge, ...]:
    if not isinstance(raw, list):
        raise ValueError("factor is not a list")
    answer: list[Edge] = []
    for item in raw:
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("edge record is malformed")
        endpoints: list[Person] = []
        for endpoint in item:
            if not isinstance(endpoint, list) or len(endpoint) != 2:
                raise ValueError("endpoint record is malformed")
            endpoints.append((int(endpoint[0]), int(endpoint[1])))
        answer.append(edge(endpoints[0], endpoints[1]))
    if len(answer) != len(set(answer)):
        raise ValueError("factor repeats an external edge")
    return tuple(sorted(answer))


def rotate_person(person: Person, shift: int) -> Person:
    v, bit = person
    return (v if v == INF else (v + shift) % N, bit)


def rotate_factor(factor: tuple[Edge, ...], shift: int) -> tuple[Edge, ...]:
    return tuple(
        sorted(edge(rotate_person(a, shift), rotate_person(b, shift)) for a, b in factor)
    )


def make_f2(f1: tuple[Edge, ...]) -> tuple[Edge, ...]:
    f2 = set(rotate_factor(f1, N // 2))
    pink = edge((0, 0), (10, 0))
    blue = edge((0, 1), (10, 1))
    black_one = edge((0, 0), (10, 1))
    black_two = edge((0, 1), (10, 0))
    if pink not in f2 or blue not in f2:
        raise ValueError("half-turn does not contain the designated pink/blue 2-cycle")
    f2.remove(pink)
    f2.remove(blue)
    f2.add(black_one)
    f2.add(black_two)
    return tuple(sorted(f2))


def matching_and_person_cycle_lengths(factor: tuple[Edge, ...]) -> list[int]:
    incidence = Counter(person for e in factor for person in e)
    all_people = {(v, bit) for v in range(21) for bit in range(2)}
    if set(incidence) != all_people or set(incidence.values()) != {1}:
        raise ValueError("external edges are not a perfect matching of the 42 people")

    adjacency: dict[Person, list[Person]] = defaultdict(list)
    for a, b in factor:
        adjacency[a].append(b)
        adjacency[b].append(a)
    for v in range(21):
        a, b = (v, 0), (v, 1)
        adjacency[a].append(b)
        adjacency[b].append(a)
    if any(len(adjacency[p]) != 2 for p in all_people):
        raise AssertionError("meal union is not 2-regular")

    seen: set[Person] = set()
    lengths: list[int] = []
    for root in sorted(all_people):
        if root in seen:
            continue
        stack = [root]
        component: set[Person] = set()
        while stack:
            p = stack.pop()
            if p in component:
                continue
            component.add(p)
            seen.add(p)
            stack.extend(q for q in adjacency[p] if q not in component)
        lengths.append(len(component))
    return sorted(lengths, reverse=True)


def orbit(edge_value: Edge) -> frozenset[Edge]:
    return frozenset(rotate_factor((edge_value,), shift)[0] for shift in range(N))


def factor_bytes(factors: list[tuple[Edge, ...]]) -> bytes:
    serial = [
        [[list(a), list(b)] for a, b in factor]
        for factor in factors
    ]
    return json.dumps(serial, separators=(",", ":"), sort_keys=True).encode()


def main() -> None:
    raw_bytes = (ROOT / "certificate.json").read_bytes()
    data = json.loads(raw_bytes)
    if data.get("n") != 21 or data.get("type") != [16, 3, 2]:
        raise ValueError("certificate has the wrong declared parameters")
    f1 = parse_factor(data["F1"])
    f3 = parse_factor(data["F3"])
    f2 = make_f2(f1)

    designated = {
        edge((0, 0), (10, 0)),
        edge((0, 1), (10, 1)),
    }
    if not designated <= set(f1):
        raise ValueError("F1 lacks the required difference-10 pink/blue cycle")

    starters = [f1, f2, f3]
    for i, factor in enumerate(starters, start=1):
        lengths = matching_and_person_cycle_lengths(factor)
        if lengths != [32, 6, 4]:
            raise ValueError(f"F{i} has person-cycle lengths {lengths}")

    # This is a direct edge-level form of the Jerade--Sajna orbit conditions.
    # Ten translates of F1 and F2 plus twenty translates of F3 must be forty
    # pairwise edge-disjoint external perfect matchings.
    meals = [rotate_factor(f1, i) for i in range(10)]
    meals += [rotate_factor(f2, i) for i in range(10)]
    meals += [rotate_factor(f3, i) for i in range(20)]
    if len(meals) != 40 or len(set(meals)) != 40:
        raise ValueError("developed meals are not 40 distinct factors")
    if any(matching_and_person_cycle_lengths(f) != [32, 6, 4] for f in meals):
        raise ValueError("a developed meal has the wrong cycle type")

    counts = Counter(e for factor in meals for e in factor)
    expected = {
        edge((u, a), (v, b))
        for u in range(21)
        for v in range(u + 1, 21)
        for a in range(2)
        for b in range(2)
    }
    if set(counts) != expected or set(counts.values()) != {1}:
        missing = len(expected - set(counts))
        repeated = sum(c - 1 for c in counts.values() if c > 1)
        raise ValueError(f"development is not exact: missing={missing}, repeated={repeated}")

    f1_orbits = {orbit(e) for e in f1}
    f3_orbits = {orbit(e) for e in f3}
    if len(f1_orbits) != 21 or len(f3_orbits) != 21:
        raise ValueError("a stored starter repeats a cyclic edge orbit")

    cert_sha = hashlib.sha256(raw_bytes).hexdigest()
    schedule_sha = hashlib.sha256(factor_bytes(meals)).hexdigest()
    print("parameters=n:21 type:32,6,4")
    print("starter_external_edges=21,21,21")
    print("starter_person_cycle_lengths=32,6,4;32,6,4;32,6,4")
    print("developed_meals=40 external_edges=840 coverage_multiplicity=1")
    print(f"certificate_sha256={cert_sha}")
    print(f"developed_schedule_sha256={schedule_sha}")
    print("VERIFIED HOP(32,6,4)")


if __name__ == "__main__":
    main()
