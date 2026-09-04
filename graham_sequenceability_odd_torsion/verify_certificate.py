#!/usr/bin/env python3
"""Definition-level checker for the odd-torsion false-terminal family.

Only Python integers, Fraction, tuples, and JSON decoding are used.  The
search that found the five moves is not imported or trusted.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "certificate.json"


def unit(n: int, i: int) -> tuple[int, ...]:
    return tuple(int(j == i) for j in range(n))


def targets(n: int) -> tuple[tuple[int, ...], ...]:
    ans = [unit(n, i) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            ans.append(tuple(int(t == i) - int(t == j) for t in range(n)))
    return tuple(ans)


def rref_q(rows: list[tuple[int, ...]]) -> tuple[tuple[tuple[Fraction, ...], ...], tuple[int, ...]]:
    if not rows:
        return (), ()
    a = [list(map(Fraction, row)) for row in rows]
    rank = 0
    pivots: list[int] = []
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        value = a[rank][column]
        a[rank] = [x / value for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][column]:
                value = a[i][column]
                a[i] = [a[i][j] - value * a[rank][j] for j in range(len(a[i]))]
        pivots.append(column)
        rank += 1
        if rank == len(a):
            break
    return tuple(tuple(row) for row in a[:rank]), tuple(pivots)


def rref_mod(
    rows: list[tuple[int, ...]], prime: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    if not rows:
        return (), ()
    a = [[x % prime for x in row] for row in rows]
    rank = 0
    pivots: list[int] = []
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][column], -1, prime)
        a[rank] = [(x * inverse) % prime for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][column]:
                value = a[i][column]
                a[i] = [
                    (a[i][j] - value * a[rank][j]) % prime
                    for j in range(len(a[i]))
                ]
        pivots.append(column)
        rank += 1
        if rank == len(a):
            break
    return tuple(tuple(row) for row in a[:rank]), tuple(pivots)


def reduce_q(
    vector: tuple[int, ...],
    reduced: tuple[tuple[Fraction, ...], ...],
    pivots: tuple[int, ...],
) -> tuple[Fraction, ...]:
    answer = list(map(Fraction, vector))
    for row, column in zip(reduced, pivots, strict=True):
        value = answer[column]
        if value:
            answer = [answer[j] - value * row[j] for j in range(len(answer))]
    return tuple(answer)


def reduce_mod(
    vector: tuple[int, ...],
    reduced: tuple[tuple[int, ...], ...],
    pivots: tuple[int, ...],
    prime: int,
) -> tuple[int, ...]:
    answer = [x % prime for x in vector]
    for row, column in zip(reduced, pivots, strict=True):
        value = answer[column]
        if value:
            answer = [
                (answer[j] - value * row[j]) % prime
                for j in range(len(answer))
            ]
    return tuple(answer)


def reconstruct_rows(k: int, moves: list[tuple[int, int]]) -> tuple[list[tuple[int, ...]], tuple[int, ...]]:
    order = list(range(k))
    rows: list[tuple[int, ...]] = []
    for left, right in moves:
        assert 0 <= left < right < k
        row = tuple(int(label in order[left : right + 1]) for label in range(k))
        assert row not in rows
        rows.append(row)
        if left >= 1:
            order[left - 1], order[left] = order[left], order[left - 1]
        else:
            assert right + 1 < k
            order[right], order[right + 1] = order[right + 1], order[right]
    return rows, tuple(order)


def linear_combination(
    coefficients: tuple[int, ...], rows: list[tuple[int, ...]]
) -> tuple[int, ...]:
    return tuple(
        sum(coefficient * row[j] for coefficient, row in zip(coefficients, rows, strict=True))
        for j in range(len(rows[0]))
    )


def quotient_labels(
    relation_rows: list[tuple[int, ...]], prime: int
) -> tuple[tuple[tuple[int, ...], ...], int]:
    reduced, pivots = rref_mod(relation_rows, prime)
    n = len(relation_rows[0])
    labels = tuple(reduce_mod(unit(n, i), reduced, pivots, prime) for i in range(n))
    return labels, n - len(pivots)


def check_distinct_nonzero(labels: tuple[tuple[int, ...], ...]) -> None:
    zero = (0,) * len(labels[0])
    assert all(label != zero for label in labels)
    assert len(set(labels)) == len(labels)


def quotient_sum(labels: tuple[tuple[int, ...], ...], prime: int) -> tuple[int, ...]:
    return tuple(sum(label[j] for label in labels) % prime for j in range(len(labels[0])))


def main() -> None:
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    prime = data["field_prime"]
    moves = [tuple(move) for move in data["moves"]]
    stored_rows = [tuple(row) for row in data["rows_on_six_labels"]]

    rows6, order6 = reconstruct_rows(6, moves)
    assert rows6 == stored_rows
    assert order6 == (1, 3, 0, 2, 4, 5)

    # The first four nodes are not rational zero/equality terminals.
    target6 = targets(6)
    for depth in range(1, 5):
        reduced, pivots = rref_q(rows6[:depth])
        assert all(any(reduce_q(t, reduced, pivots)) for t in target6)

    # Both displayed identities are exact over Z and put e_1,e_4 in the
    # rational row span, but only after multiplying by three.
    for identity in data["terminal_identities"]:
        coefficients = tuple(identity["coefficients"])
        index = identity["target_index_zero_based"]
        multiple = identity["target_multiple"]
        expected = tuple(multiple * x for x in unit(6, index))
        assert linear_combination(coefficients, rows6) == expected

    reduced_q, pivots_q = rref_q(rows6)
    rational_terminals = tuple(
        i for i, t in enumerate(target6) if not any(reduce_q(t, reduced_q, pivots_q))
    )
    assert rational_terminals

    # Over F_3 no zero/equality target lies in the row space.  Thus the
    # universal quotient assignment a_i=[e_i] has distinct nonzero labels.
    reduced3, pivots3 = rref_mod(rows6, prime)
    assert len(pivots3) == 4
    assert all(any(reduce_mod(t, reduced3, pivots3, prime)) for t in target6)
    labels6, dimension6 = quotient_labels(rows6, prime)
    check_distinct_nonzero(labels6)
    assert dimension6 == 2
    assert all(
        quotient_sum(tuple(labels6[j] for j, bit in enumerate(row) if bit), prime)
        == (0,) * 6
        for row in rows6
    )

    # Audit the parameter family.  Extending the rows by zero columns makes
    # the same five moves legal in general mode for every k>=6.  Adding the
    # all-ones relation makes a zero-sum quotient; with at least two added
    # coordinates (k>=8), its labels remain distinct and nonzero.
    family_records = []
    for k in range(6, 65):
        rows, order = reconstruct_rows(k, moves)
        assert rows == [row + (0,) * (k - 6) for row in rows6]
        assert moves[0] != (0, k - 1)
        assert order[:6] == order6 and order[6:] == tuple(range(6, k))
        labels, dimension = quotient_labels(rows, prime)
        check_distinct_nonzero(labels)
        assert dimension == k - 4
        family_records.append(["general", k, dimension, hashlib.sha256(repr(labels).encode()).hexdigest()])

        if k >= 8:
            assert max(right - left for left, right in moves) <= k // 2
            zero_rows = rows + [(1,) * k]
            zero_labels, zero_dimension = quotient_labels(zero_rows, prime)
            check_distinct_nonzero(zero_labels)
            assert quotient_sum(zero_labels, prime) == (0,) * k
            assert zero_dimension == k - 5
            family_records.append(
                ["zero_sum", k, zero_dimension, hashlib.sha256(repr(zero_labels).encode()).hexdigest()]
            )

    family_digest = hashlib.sha256(
        json.dumps(family_records, separators=(",", ":")).encode()
    ).hexdigest()
    cert_digest = hashlib.sha256(raw).hexdigest()
    explicit_labels = tuple(
        tuple(label[j] for j in range(6) if j not in pivots3) for label in labels6
    )

    print("path_moves=" + ",".join(f"[{left},{right}]" for left, right in moves))
    print("rows=" + ";".join("".join(map(str, row)) for row in rows6))
    print("proper_prefixes_nonterminal=4 final_rational_terminal=true")
    print("integer_identity=-r1+r3+r4+r5=3e1")
    print(f"mod3_quotient_dimension={dimension6} labels={explicit_labels}")
    print("general_family=k>=6 zero_sum_family=k>=8")
    print(f"certificate_sha256={cert_digest}")
    print(f"family_audit_sha256={family_digest}")
    print("VERIFIED odd-torsion false-terminal family")


if __name__ == "__main__":
    main()
