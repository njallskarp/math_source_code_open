#!/usr/bin/env python3
"""Exact type-orbit verifier for the all-width three-clique hub chain."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json

Type = tuple[int, int, int, int, int, int]
State = frozenset[Type]


def leq(left: Type, right: Type) -> bool:
    return all(x <= y for x, y in zip(left, right, strict=True))


def maximal(types: object) -> State:
    candidates = frozenset(types)
    return frozenset(
        x for x in candidates
        if not any(x != y and leq(x, y) for y in candidates)
    )


def type_box(n: int, m: int, ell: int) -> tuple[Type, ...]:
    return tuple(
        itertools.product((0, 1), range(n), (0, 1), range(m), (0, 1), range(ell))
    )


def base_box(n: int, ell: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.product((0, 1), range(n), (0, 1), (0, 1), range(ell)))


def base_of(type_: Type) -> tuple[int, ...]:
    return type_[:3] + type_[4:]


def insert_height(base: tuple[int, ...], height: int) -> Type:
    return base[:3] + (height,) + base[3:]


def kappa(type_: Type, n: int, m: int, ell: int) -> int:
    """The corrected cardinality statistic from the proof."""
    a, i, b, j, c, k = type_
    blocks_met = sum((a + i > 0, b + j > 0, c + k > 0))
    positive = (
        (a == b == 1)
        or (b == c == 1)
        or (a == 1 and i == n - 1)
        or (b == 1 and j == m - 1)
        or (c == 1 and k == ell - 1)
    )
    correction = 1 if positive else (-1 if blocks_met <= 1 else 0)
    return sum(type_) + correction


def full_blocks(n: int, m: int, ell: int) -> tuple[tuple[int, Type], ...]:
    return (
        (n, (1, n - 1, 0, 0, 0, 0)),
        (m, (0, 0, 1, m - 1, 0, 0)),
        (ell, (0, 0, 0, 0, 1, ell - 1)),
    )


def layer(s: int, n: int, m: int, ell: int) -> State:
    """B_s: the kappa-s layer, with the three full-block gap fillers."""
    result = {x for x in type_box(n, m, ell) if kappa(x, n, m, ell) == s}
    result.update(block for size, block in full_blocks(n, m, ell) if size == s + 1)
    return frozenset(result)


def initial(n: int, m: int, ell: int) -> State:
    """The edge types of the hubbed K_n--K_m--K_ell chain."""
    return frozenset(
        {
            (1, 1, 0, 0, 0, 0),
            (0, 2, 0, 0, 0, 0),
            (0, 0, 1, 1, 0, 0),
            (0, 0, 0, 2, 0, 0),
            (0, 0, 0, 0, 1, 1),
            (0, 0, 0, 0, 0, 2),
            (1, 0, 1, 0, 0, 0),
            (0, 0, 1, 0, 1, 0),
        }
    )


START_1: State = frozenset(
    {
        (0, 1, 0, 1, 0, 1),
        (0, 1, 0, 1, 1, 0),
        (0, 1, 1, 0, 0, 1),
        (1, 0, 0, 1, 0, 1),
        (1, 0, 0, 1, 1, 0),
    }
)


DEFICITS_3: tuple[Type, ...] = (
    (1, 0, 1, 0, 0, 0),
    (1, 0, 0, 1, 0, 0),
    (1, 0, 0, 0, 1, 0),
    (1, 0, 0, 0, 0, 1),
    (0, 1, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 0),
    (0, 1, 0, 0, 0, 1),
    (0, 0, 1, 0, 1, 0),
    (0, 0, 1, 0, 0, 1),
    (0, 0, 0, 1, 1, 0),
)


DEFICITS_4: tuple[Type, ...] = (
    (1, 1, 0, 0, 0, 0),
    (1, 0, 1, 0, 1, 0),
    (1, 0, 1, 0, 0, 1),
    (1, 0, 0, 1, 1, 0),
    (0, 2, 0, 0, 0, 0),
    (0, 1, 1, 0, 1, 0),
    (0, 1, 1, 0, 0, 1),
    (0, 1, 0, 1, 0, 0),
    (0, 0, 1, 1, 0, 0),
    (0, 0, 0, 2, 0, 0),
    (0, 0, 0, 1, 0, 1),
    (0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 0, 2),
)


def startup(n: int, m: int, ell: int) -> tuple[State, ...]:
    top = (1, n - 1, 1, m - 1, 1, ell - 1)
    start_2 = frozenset(
        {
            (0, 0, 1, m - 1, 1, ell - 1),
            (1, 0, 1, 0, 1, ell - 1),
            (1, n - 1, 0, 0, 1, ell - 1),
            (1, n - 1, 1, m - 1, 0, 0),
            (1, n - 1, 1, 0, 1, 0),
        }
    )
    start_3 = frozenset(
        tuple(x - d for x, d in zip(top, deficit, strict=True))
        for deficit in DEFICITS_3
    )
    start_4 = frozenset(
        tuple(x - d for x, d in zip(top, deficit, strict=True))
        for deficit in DEFICITS_4
    )
    return (initial(n, m, ell), START_1, start_2, start_3, start_4)


def predicted_orbit(n: int, m: int, ell: int) -> list[State]:
    total = n + m + ell
    return [*startup(n, m, ell), *(layer(s, n, m, ell) for s in range(total - 2, 1, -1))]


def delta_types(facets: State, n: int, m: int, ell: int) -> State:
    """Apply NF exactly in the S_(n-1) x S_(m-1) x S_(ell-1) quotient."""
    tops: list[Type] = []
    for base in base_box(n, ell):
        thresholds = [facet[3] for facet in facets if leq(base_of(facet), base)]
        height = min(thresholds) - 1 if thresholds else m - 1
        if height >= 0:
            tops.append(insert_height(base, height))
    return maximal(tops)


def verify_kappa_covers(n: int, m: int, ell: int) -> int:
    caps = (1, n - 1, 1, m - 1, 1, ell - 1)
    checks = 0
    for x in type_box(n, m, ell):
        for coordinate, cap in enumerate(caps):
            if x[coordinate] == cap:
                continue
            y = list(x)
            y[coordinate] += 1
            if kappa(tuple(y), n, m, ell) <= kappa(x, n, m, ell):
                raise AssertionError(f"kappa is not strict on cover {x} < {tuple(y)}")
            checks += 1
    return checks


def verify_rank_filling(n: int, m: int, ell: int) -> int:
    """Check the two interval assertions used by the all-parameter proof lemma."""
    total = n + m + ell
    box = type_box(n, m, ell)
    blocks = {block: size for size, block in full_blocks(n, m, ell)}

    def labels(x: Type) -> set[int]:
        answer = {kappa(x, n, m, ell)}
        if x in blocks:
            answer.add(blocks[x] - 1)
        return answer

    checks = 0
    for x in box:
        below = set().union(*(labels(y) for y in box if leq(y, x)))
        above = set().union(*(labels(y) for y in box if leq(x, y)))
        for s in range(3, min(kappa(x, n, m, ell), total - 2) + 1):
            if s not in below and not (x in blocks and s == blocks[x]):
                raise AssertionError(f"downward rank gap at {n,m,ell,x,s}")
            checks += 1
        for s in range(max(kappa(x, n, m, ell), 2), total - 2):
            if s not in above:
                raise AssertionError(f"upward rank gap at {n,m,ell,x,s}")
            checks += 1
    return checks


def state_record(state: State) -> list[list[int]]:
    return [list(type_) for type_ in sorted(state)]


def verify_case(n: int, m: int, ell: int) -> tuple[int, int, str]:
    orbit = predicted_orbit(n, m, ell)
    expected = n + m + ell + 2
    if len(orbit) != expected:
        raise AssertionError("wrong predicted orbit length")
    if len(set(orbit)) != expected:
        raise AssertionError(f"predicted states repeat early at {n,m,ell}")
    for index, state in enumerate(orbit):
        actual = delta_types(state, n, m, ell)
        target = orbit[(index + 1) % expected]
        if actual != target:
            raise AssertionError(
                f"transition mismatch at {n,m,ell}, index={index}: "
                f"missing={sorted(target-actual)[:3]}, extra={sorted(actual-target)[:3]}"
            )
    if not all(any(sum(type_) >= 3 for type_ in state) for state in orbit[1:]):
        raise AssertionError(f"dimension witness missing at {n,m,ell}")
    payload = json.dumps(
        [state_record(state) for state in orbit], separators=(",", ":")
    ).encode()
    return expected, sum(map(len, orbit)), hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-size", type=int, default=6)
    parser.add_argument("--rank-fill-max", type=int, default=5)
    args = parser.parse_args()
    if args.max_size < 3 or args.rank_fill_max < 3:
        raise SystemExit("bounds must be at least 3")

    cover_checks = 0
    rank_checks = 0
    transitions = 0
    facets = 0
    case_digests: list[str] = []
    cases = 0
    for n in range(3, args.max_size + 1):
        for m in range(3, args.max_size + 1):
            for ell in range(3, args.max_size + 1):
                cover_checks += verify_kappa_covers(n, m, ell)
                period, seen, digest = verify_case(n, m, ell)
                transitions += period
                facets += seen
                case_digests.append(digest)
                cases += 1
                if max(n, m, ell) <= args.rank_fill_max:
                    rank_checks += verify_rank_filling(n, m, ell)
    digest = hashlib.sha256("\n".join(case_digests).encode()).hexdigest()
    print(
        "VERIFIED all-width hubbed three-clique recurrence; "
        f"sizes=3..{args.max_size}; cases={cases}; transitions={transitions}; "
        f"facets_with_multiplicity={facets}; kappa_covers={cover_checks}; "
        f"rank_fill_checks={rank_checks}; NF(H_n,m,l)=n+m+l+2"
    )
    print(f"ORBIT_SHA256={digest}")


if __name__ == "__main__":
    main()
