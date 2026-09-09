#!/usr/bin/env python3
"""Independent exact checks of Lebedev, arXiv:2609.04589v1, Theorem 1.

Python standard library only. The two checkers share the literal input words,
but neither imports the author's software nor calls the other checker.
"""

import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def gaussian_check(a, b):
    """Direct definition, representing Gaussian integers as integer pairs."""
    n = len(a)
    require(n > 0 and n % 2 == 0 and len(b) == n, "invalid lengths")
    units = {"0": (1, 0), "1": (0, 1), "2": (-1, 0), "3": (0, -1)}
    require(set(a + b) <= units.keys(), "invalid alphabet")
    words = [[units[c] for c in word] for word in (a, b)]
    for k in range(n):
        real = imag = 0
        for word in words:
            for j in range(n):
                x, y = word[j]
                u, v = word[(j + k) % n]
                real += x * u + y * v
                imag += y * u - x * v
        require((real, imag) == ((2 * n, 0) if k == 0 else (-2, 0)),
                f"Gaussian equation fails at shift {k}: {(real, imag)}")
    sums = [[sum(x[c] for x in word) for c in (0, 1)] for word in words]
    require(sums == [[0, 0], [1, 1]], f"unexpected normalization: {sums}")
    midpoint = []
    for word in words:
        components = [sum((-1) ** j * word[j][c] for j in range(n))
                      for c in (0, 1)]
        midpoint.append(sum(x * x for x in components))
    return midpoint


def difference_family_check(a, b):
    """Separate set-theoretic checker for these reversible Gray witnesses.

    A = (p+q)/2 + i(p-q)/2; likewise B = G(r,s).
    It checks reflection and all ordered-difference multiplicities directly.
    """
    n = len(a)
    require(n > 0 and n % 2 == 0 and len(b) == n, "invalid lengths")
    require(set(a + b) <= set("0123"), "invalid alphabet")
    # Direct negative-position decoding: p is negative for -1 and -i,
    # while q is negative for i and -1. No Gaussian decoding is reused.
    blocks = [set(j for j, c in enumerate(word) if c in negative)
              for word in (a, b) for negative in ("23", "12")]
    require([len(x) for x in blocks] == [n // 2, n // 2, n // 2 - 1, n // 2],
            "wrong block sizes")
    for block in blocks:
        require({(-x) % n for x in block} == block, "non-reversible block")
    counts = [0] * n
    for block in blocks:
        for x in block:
            for y in block:
                counts[(y - x) % n] += 1
    require(counts[0] == 2 * n - 1, "wrong diagonal difference count")
    require(counts[1:] == [n - 2] * (n - 1), "difference-family identity fails")
    return [len(x) for x in blocks]


def expect_rejection(checker, a, b):
    try:
        checker(a, b)
    except ValueError:
        return
    raise AssertionError("checker accepted a negative control")


def main():
    records = json.loads(Path(__file__).with_name("pairs.json").read_text())
    require([x["length"] for x in records] == [42, 46, 52, 58, 66, 72, 80],
            "unexpected fixture lengths")
    results = []
    for record in records:
        n, a, b = record["length"], record["A"], record["B"]
        require(len(a) == n and len(b) == n, "length does not match metadata")
        midpoint = gaussian_check(a, b)
        sizes = difference_family_check(a, b)
        # Mutation, truncation and invalid-alphabet controls for each checker.
        for checker in (gaussian_check, difference_family_check):
            expect_rejection(checker, str((int(a[0]) + 1) % 4) + a[1:], b)
            expect_rejection(checker, a[:-1], b)
            expect_rejection(checker, "x" + a[1:], b)
        digest = hashlib.sha256((a + "\n" + b + "\n").encode("ascii")).hexdigest()
        results.append({"length": n, "all_nonzero_shifts_verified": n - 1,
                        "midpoint_psd": midpoint, "gray_block_sizes": sizes,
                        "literal_words_sha256": digest})
    print(json.dumps({"status": "PASS", "pairs_verified": len(results),
                      "negative_controls_rejected": 6 * len(results),
                      "results": results}, indent=2))


if __name__ == "__main__":
    main()
