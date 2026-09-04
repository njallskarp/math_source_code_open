#!/usr/bin/env python3
"""Independent exact audit of the D(a,3) Lagrange partition-chain theorem.

This checker imports no target code.  It constructs the cyclic {1,2} period
literally from each admissible run triple, evaluates every cyclic shift with
2x2 integer matrices, and compares the resulting exact Fraction scores with
the claimed partition fibres and order.  Prefix/suffix products make the
cyclic-shift calculation independent of the target's scalar-continuant
implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import comb, gcd

Matrix = tuple[int, int, int, int]
IDENTITY: Matrix = (1, 0, 0, 1)


def matmul(left: Matrix, right: Matrix) -> Matrix:
    a, b, c, d = left
    e, f, g, h = right
    return (
        a * e + b * g,
        a * f + b * h,
        c * e + d * g,
        c * f + d * h,
    )


def matpow(base: Matrix, exponent: int) -> Matrix:
    if exponent < 0:
        raise ValueError("matrix exponent must be nonnegative")
    result = IDENTITY
    while exponent:
        if exponent & 1:
            result = matmul(result, base)
        base = matmul(base, base)
        exponent >>= 1
    return result


def digit_matrix(digit: int) -> Matrix:
    if digit not in (1, 2):
        raise ValueError("continued-fraction digits must be 1 or 2")
    return (digit, 1, 1, 0)


D = digit_matrix(2)
E = matmul(digit_matrix(1), digit_matrix(1))


def block_matrix(run: int) -> Matrix:
    """Literal matrix for K_run, without a Fibonacci closed form."""
    if run < 0:
        raise ValueError("run length must be nonnegative")
    if run == 0:
        return E
    return matmul(matmul(D, matpow(E, run - 1)), D)


def fib(index: int) -> int:
    """Fibonacci number with F_0=0, F_1=1 and the standard negative extension."""
    if index < 0:
        value = fib(-index)
        return value if (-index) % 2 else -value
    previous, current = 0, 1
    for _ in range(index):
        previous, current = current, previous + current
    return previous


def coefficient_word(triple: tuple[int, int, int]) -> tuple[int, ...]:
    r, s, t = triple
    path = "R" * r + "U" + "R" * s + "U" + "R" * t + "U"
    digits = [2]  # Closing adjacency: the last U followed by the first R.
    for left, right in zip(path, path[1:]):
        if left == right:
            digits.extend((1, 1))
        else:
            digits.append(2)
    return tuple(digits)


def cyclic_data(digits: tuple[int, ...]) -> tuple[int, int, int, bool]:
    """Return trace, all-shift q minimum, 2-shift q minimum, and a 1-shift tie flag."""
    matrices = tuple(digit_matrix(digit) for digit in digits)
    prefix = [IDENTITY]
    for matrix in matrices:
        prefix.append(matmul(prefix[-1], matrix))
    suffix = [IDENTITY] * (len(matrices) + 1)
    for index in range(len(matrices) - 1, -1, -1):
        suffix[index] = matmul(matrices[index], suffix[index + 1])

    traces: set[int] = set()
    all_q: list[int] = []
    two_q: list[int] = []
    one_q: list[int] = []
    for index, digit in enumerate(digits):
        rotated = matmul(suffix[index], prefix[index])
        a, _b, q, d = rotated
        if a * d - rotated[1] * q != 1:
            raise AssertionError("cyclic period matrix must have determinant one")
        traces.add(a + d)
        all_q.append(q)
        (two_q if digit == 2 else one_q).append(q)
    if len(traces) != 1 or not two_q:
        raise AssertionError("cyclic trace mismatch or missing digit 2")
    q_all = min(all_q)
    q_two = min(two_q)
    if q_all != q_two:
        raise AssertionError("a digit-1 shift exceeds every digit-2 Lagrange shift")
    one_tie = bool(one_q) and min(one_q) == q_all
    return traces.pop(), q_all, q_two, one_tie


def admissible_triples(a: int) -> list[tuple[int, int, int]]:
    triples = []
    for r in range(a + 1):
        for s in range(a - r + 1):
            t = a - r - s
            if 3 * r >= a and 3 * (r + s) >= 2 * a:
                triples.append((r, s, t))
    return triples


def partitions(a: int) -> list[tuple[int, int, int]]:
    result = []
    for z in range(a // 3 + 1):
        for y in range(z, a + 1):
            x = a - y - z
            if x >= y:
                result.append((x, y, z))
    return sorted(result, key=lambda part: (part[2], -part[0]))


def block_trace_q(partition: tuple[int, int, int]) -> tuple[int, int]:
    product = IDENTITY
    for run in partition:
        product = matmul(product, block_matrix(run))
    return product[0] + product[3], product[2]


def check_closed_forms(partition: tuple[int, int, int]) -> None:
    x, y, z = partition
    trace, q = block_trace_q(partition)
    a_term = fib(2 * y + 1) * fib(2 * (x - z) - 2)
    if trace != 3 * q + 6 * a_term:
        raise AssertionError(f"trace-q identity failed for {partition}")
    if x > y:
        swapped_q = block_trace_q((y, x, z))[1]
        expected = -2 * fib(2 * (x - y)) * fib(2 * z + 3)
        if q - swapped_q != expected:
            raise AssertionError(f"first adjacent-swap identity failed for {partition}")
    if y > z:
        swapped_q = block_trace_q((x, z, y))[1]
        expected = -2 * fib(2 * (y - z)) * fib(2 * x - 1)
        if q - swapped_q != expected:
            raise AssertionError(f"second adjacent-swap identity failed for {partition}")


def check_endpoint(a: int) -> tuple[list[object], int, int, int, int]:
    triples = admissible_triples(a)
    if gcd(a, 3) == 1:
        expected_count = comb(a + 3, 3) // (a + 3)
        if len(triples) != expected_count:
            raise AssertionError(f"rational-Catalan count failed at a={a}")

    scores_by_partition: dict[tuple[int, int, int], set[Fraction]] = {}
    triples_by_partition: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {}
    one_shift_ties = 0
    sorted_cut_checks = 0
    for triple in triples:
        partition = tuple(sorted(triple, reverse=True))
        trace, q_all, q_two, one_tie = cyclic_data(coefficient_word(triple))
        score = Fraction(trace * trace - 4, q_all * q_all)
        scores_by_partition.setdefault(partition, set()).add(score)
        triples_by_partition.setdefault(partition, []).append(triple)
        one_shift_ties += int(one_tie)

        block_trace, sorted_q = block_trace_q(partition)
        if trace != block_trace or q_two != sorted_q:
            raise AssertionError(
                f"sorted block cut mismatch at a={a}, triple={triple}, partition={partition}"
            )
        sorted_cut_checks += 1

    expected_partitions = partitions(a)
    if sorted(scores_by_partition) != sorted(expected_partitions):
        raise AssertionError(f"partition coverage failed at a={a}")
    for partition, scores in scores_by_partition.items():
        if len(scores) != 1:
            raise AssertionError(f"partition fibre has unequal scores: {partition}")
        check_closed_forms(partition)

    score_by_partition = {
        partition: next(iter(scores)) for partition, scores in scores_by_partition.items()
    }
    obtained = sorted(score_by_partition, key=score_by_partition.get, reverse=True)
    if obtained != expected_partitions:
        raise AssertionError(f"partition-chain order failed at a={a}")
    if len(set(score_by_partition.values())) != len(expected_partitions):
        raise AssertionError(f"distinct partitions collide at a={a}")

    transition_checks = 0
    terminal_tie_repairs = 0
    for first, second in zip(expected_partitions, expected_partitions[1:]):
        t1, q1 = block_trace_q(first)
        t2, q2 = block_trace_q(second)
        a1 = fib(2 * first[1] + 1) * fib(2 * (first[0] - first[2]) - 2)
        a2 = fib(2 * second[1] + 1) * fib(2 * (second[0] - second[2]) - 2)
        if second[0] == second[1] == second[2]:
            # This case occurs exactly at the noncoprime endpoint a=3k, which
            # lies outside the target.  The target's odd-boundary q-drop has
            # a factor corresponding to h-z-1 and vanishes here.  The chain
            # nevertheless remains strict because q ties while trace drops.
            k = second[0]
            if first != (k + 1, k, k - 1):
                raise AssertionError("unexpected terminal partition transition")
            if not (
                q1 == q2
                and t1 - t2 == 12 * fib(2 * k + 1)
                and Fraction(t1 * t1 - 4, q1 * q1)
                > Fraction(t2 * t2 - 4, q2 * q2)
            ):
                raise AssertionError(f"noncoprime terminal repair failed: {first} -> {second}")
            terminal_tie_repairs += 1
        elif not (t1 > t2 and q1 > q2 and a1 * t2 > a2 * t1):
            raise AssertionError(f"transition inequalities failed: {first} -> {second}")
        transition_checks += 1

    rows: list[object] = []
    for partition in expected_partitions:
        score = score_by_partition[partition]
        rows.append(
            [
                a,
                list(partition),
                score.numerator,
                score.denominator,
                [list(triple) for triple in sorted(triples_by_partition[partition])],
            ]
        )
    return rows, sorted_cut_checks, transition_checks, one_shift_ties, terminal_tie_repairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=120)
    args = parser.parse_args()
    if args.max_a < 4:
        raise SystemExit("--max-a must be at least 4")

    for run in range(args.max_a + 1):
        matrix = block_matrix(run)
        expected = (
            fib(2 * run + 3),
            fib(2 * run + 1),
            fib(2 * run + 1),
            fib(2 * run - 1),
        )
        if matrix != expected:
            raise AssertionError(f"literal K_n/Fibonacci bridge failed at n={run}")

    all_rows: list[object] = []
    coprime_endpoints = coprime_triples = coprime_levels = 0
    extension_endpoints = extension_triples = extension_levels = 0
    sorted_cut_checks = transition_checks = one_shift_ties = terminal_tie_repairs = 0
    for a in range(4, args.max_a + 1):
        rows, cuts, transitions, ties, repairs = check_endpoint(a)
        all_rows.extend(rows)
        triple_count = len(admissible_triples(a))
        if gcd(a, 3) == 1:
            coprime_endpoints += 1
            coprime_triples += triple_count
            coprime_levels += len(rows)
        else:
            extension_endpoints += 1
            extension_triples += triple_count
            extension_levels += len(rows)
        sorted_cut_checks += cuts
        transition_checks += transitions
        one_shift_ties += ties
        terminal_tie_repairs += repairs

    payload = (json.dumps(all_rows, separators=(",", ":")) + "\n").encode()
    digest = hashlib.sha256(payload).hexdigest()
    print(
        "INDEPENDENT MATRIX AUDIT PASSED; "
        f"4<=a<={args.max_a}; coprime_endpoints={coprime_endpoints}; "
        f"coprime_paths={coprime_triples}; coprime_levels={coprime_levels}; "
        f"noncoprime_endpoints={extension_endpoints}; "
        f"noncoprime_paths={extension_triples}; noncoprime_levels={extension_levels}; "
        f"sorted_cut_checks={sorted_cut_checks}; transition_checks={transition_checks}; "
        f"noncoprime_terminal_q_ties={terminal_tie_repairs}; "
        f"digit1_max_ties={one_shift_ties}; audit_sha256={digest}"
    )


if __name__ == "__main__":
    main()
