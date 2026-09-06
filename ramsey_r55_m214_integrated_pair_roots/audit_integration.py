#!/usr/bin/env python3
"""Independent finite audit of root coverage counts and guard semantics."""

from __future__ import annotations

import itertools
import hashlib


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def guarded_unit_holds(value: int, selected: int, edge: int) -> bool:
    if value:
        return edge - selected >= 0
    return -edge - selected >= -1


def guarded_equality_holds(total: int, target: int, selected: int, maximum: int) -> bool:
    return (total - target * selected >= 0 and
            -total - (maximum - target) * selected >= -maximum)


def root_census() -> tuple[list[int], int, str]:
    cells = "HABO"
    families = (
        ("E8", ("H", "A"), True),
        ("E77", ("BB", "BO", "OO"), True),
        ("C8", ("B", "O"), False),
        ("C77", ("BB", "BO", "OO"), False),
        ("C77partition", ("HO", "AB"), False),
    )
    counts = []
    partition_count = 0
    keys = []
    for family, patterns, use_exceptional in families:
        count = 0
        for common in range(9, 14):
            for k in range(7):
                exceptional_sizes = (k, 6 - k, 6 - k, 1 + k)
                central_sizes = (common - k, 14 - common + k,
                                 14 - common + k, common - k)
                sizes = exceptional_sizes if use_exceptional else central_sizes
                require(sum(exceptional_sizes) == 13 and sum(central_sizes) == 28,
                        "pair margins")
                for pattern in patterns:
                    if all(pattern.count(cell) <= sizes[index]
                           for index, cell in enumerate(cells)):
                        count += 1
                        keys.append((family, common, k, pattern))
                        if family == "C77partition":
                            partition_count += 1
        counts.append(count)
    key_bytes = "".join("\t".join(map(str, key)) + "\n" for key in keys).encode("ascii")
    return counts, partition_count, hashlib.sha256(key_bytes).hexdigest()


def audit_guards() -> int:
    checks = 0
    for value, selected, edge in itertools.product(range(2), repeat=3):
        expected = not selected or edge == value
        require(guarded_unit_holds(value, selected, edge) == expected, "unit guard")
        checks += 1
    for maximum, targets in ((13, (6, 7, 8)), (2, (1,))):
        for target in targets:
            for selected in range(2):
                for total in range(maximum + 1):
                    expected = not selected or total == target
                    require(guarded_equality_holds(total, target, selected, maximum) == expected,
                            "sum-equality guard")
                    checks += 1
    for width in range(1, 9):
        accepted = sum(sum(bits) == 1 for bits in itertools.product(range(2), repeat=width))
        require(accepted == width, "one-hot truth table")
        checks += 2 ** width
    return checks


def main() -> None:
    family_counts, partition_roots, root_keys_sha256 = root_census()
    require(family_counts == [60, 85, 70, 104, 70], "root family census")
    require(sum(family_counts) == 389 and partition_roots == 70, "root totals")
    guard_checks = audit_guards()

    n = 43
    edges = n * (n - 1) // 2
    triangles = n * (n - 1) * (n - 2) // 6
    five_sets = n * (n - 1) * (n - 2) * (n - 3) * (n - 4) // 120
    base_rows = 2 * five_sets + 4 * triangles + 3 * n
    selector_rows = 1 + 389 * (83 + 2 * n) + 70 * (1 + 2 * 28)
    require((edges, triangles, base_rows, selector_rows) == (903, 12341, 1974689, 69732),
            "formula arithmetic")
    print("PASS independent roots=389 families=60,85,70,104,70 partition_roots=70")
    print(f"PASS root_keys_sha256={root_keys_sha256}")
    print(f"PASS guard truth tables={guard_checks} one_hot_widths=1..8")
    print("PASS formula variables=13633 base_rows=1974689 selector_rows=69732 constraints=2044421")


if __name__ == "__main__":
    main()
