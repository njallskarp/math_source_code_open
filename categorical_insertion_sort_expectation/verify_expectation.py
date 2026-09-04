#!/usr/bin/env python3
"""Exact definition-level audit of the categorical insertion-sort formulas."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import factorial


def inversion_count(word: tuple[int, ...]) -> int:
    return sum(
        word[i] > word[j]
        for i in range(len(word))
        for j in range(i + 1, len(word))
    )


def insertion_sort_swaps(word: tuple[int, ...]) -> int:
    data = list(word)
    swaps = 0
    for i in range(1, len(data)):
        j = i
        while j and data[j - 1] > data[j]:
            data[j - 1], data[j] = data[j], data[j - 1]
            swaps += 1
            j -= 1
    assert all(data[i] <= data[i + 1] for i in range(len(data) - 1))
    return swaps


def positive_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - parts + 2):
        for tail in positive_compositions(total - first, parts - 1):
            yield (first,) + tail


def multiset_words(counts: tuple[int, ...]):
    remaining = list(counts)
    word: list[int] = []
    n = sum(counts)

    def visit():
        if len(word) == n:
            yield tuple(word)
            return
        for letter, count in enumerate(remaining):
            if count:
                remaining[letter] -= 1
                word.append(letter)
                yield from visit()
                word.pop()
                remaining[letter] += 1

    yield from visit()


def fixed_mean(counts: tuple[int, ...]) -> Fraction:
    return Fraction(
        sum(counts[a] * counts[b] for a in range(len(counts)) for b in range(a + 1, len(counts))),
        2,
    )


def iid_mean(n: int, probabilities: tuple[Fraction, ...]) -> Fraction:
    collision_probability = sum(p * p for p in probabilities)
    return Fraction(n * (n - 1), 4) * (1 - collision_probability)


def weak_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first,) + tail


def audit_fixed_counts(max_n: int = 8) -> dict[str, int]:
    vectors = 0
    words_checked = 0
    palindromic_distributions = 0
    for n in range(1, max_n + 1):
        for m in range(1, n + 1):
            for counts in positive_compositions(n, m):
                vectors += 1
                distribution: Counter[int] = Counter()
                swap_sum = 0
                word_count = 0
                for word in multiset_words(counts):
                    inversions = inversion_count(word)
                    assert insertion_sort_swaps(word) == inversions
                    distribution[inversions] += 1
                    swap_sum += inversions
                    word_count += 1
                expected_word_count = factorial(n)
                for count in counts:
                    expected_word_count //= factorial(count)
                assert word_count == expected_word_count
                assert Fraction(swap_sum, word_count) == fixed_mean(counts)
                degree = sum(
                    counts[a] * counts[b]
                    for a in range(m)
                    for b in range(a + 1, m)
                )
                assert all(
                    distribution[k] == distribution[degree - k]
                    for k in range(degree + 1)
                )
                palindromic_distributions += 1
                words_checked += word_count
    return {
        "fixed_count_vectors": vectors,
        "fixed_words": words_checked,
        "palindromic_distributions": palindromic_distributions,
    }


def audit_iid(max_n: int = 6, max_m: int = 4, denominator: int = 4) -> dict[str, int]:
    laws = 0
    weighted_words = 0
    for m in range(1, max_m + 1):
        for numerators in weak_compositions(denominator, m):
            probabilities = tuple(Fraction(x, denominator) for x in numerators)
            laws += 1
            for n in range(1, max_n + 1):
                direct = Fraction(0)
                for word in product(range(m), repeat=n):
                    probability = Fraction(1)
                    for letter in word:
                        probability *= probabilities[letter]
                    direct += probability * insertion_sort_swaps(word)
                    weighted_words += 1
                assert direct == iid_mean(n, probabilities)
    return {"iid_probability_laws": laws, "iid_weighted_words": weighted_words}


def main() -> None:
    summary = {
        "arithmetic": "exact integers and fractions",
        **audit_fixed_counts(),
        **audit_iid(),
        "python": "3.12+ standard library",
    }
    payload = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode("ascii")).hexdigest()
    print(f"summary={payload}")
    print(f"result_sha256={digest}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
