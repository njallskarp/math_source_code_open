#!/usr/bin/env python3
"""Exact rank-two replay for two leaves on c=3 equality bases."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json

from verify_c3_responses import equality_base, inertia, inverse, shifted_signless


def add_two_leaves(
    adjacency: list[list[int]], first: int, second: int
) -> list[list[int]]:
    size = len(adjacency)
    result = [row[:] + [0, 0] for row in adjacency]
    result.extend([[0] * (size + 2) for _ in range(2)])
    result[first][size] = result[size][first] = 1
    result[second][size + 1] = result[size + 1][second] = 1
    return result


def signature(triple: tuple[int, int, int]) -> int:
    positive, _, negative = triple
    return positive - negative


def main() -> None:
    pair_cases = 0
    s_inertias: Counter[tuple[int, int, int]] = Counter()
    line_signatures: Counter[int] = Counter()
    records: list[str] = []

    for central in ((1, 3), (3, 1)):
        for connectors in ((1, 1), (1, 3), (3, 1), (3, 3)):
            adjacency, names, _, _ = equality_base(central, connectors)
            matrix = shifted_signless(adjacency)
            matrix_inverse = inverse(matrix)
            base_inertia = inertia(matrix)
            assert signature(base_inertia) - 2 == 2

            for first in range(len(adjacency)):
                for second in range(first, len(adjacency)):
                    response = [
                        [
                            Fraction(i == j, 2)
                            + matrix_inverse[port_i][port_j]
                            for j, port_j in enumerate((first, second))
                        ]
                        for i, port_i in enumerate((first, second))
                    ]
                    assert response[0][0] in {Fraction(1), Fraction(2)}
                    assert response[1][1] in {Fraction(1), Fraction(2)}
                    response_inertia = inertia(response)
                    assert signature(response_inertia) >= 0

                    augmented = add_two_leaves(adjacency, first, second)
                    augmented_inertia = inertia(shifted_signless(augmented))
                    assert (
                        signature(augmented_inertia) - signature(base_inertia)
                        == -signature(response_inertia)
                    )
                    line_signature = signature(augmented_inertia) - 2
                    assert line_signature <= 2

                    s_inertias[response_inertia] += 1
                    line_signatures[line_signature] += 1
                    pair_cases += 1
                    records.append(
                        ":".join(
                            (
                                str(central[0]),
                                str(central[1]),
                                str(connectors[0]),
                                str(connectors[1]),
                                names[first],
                                names[second],
                                str(line_signature),
                            )
                        )
                    )

    assert pair_cases == 1096
    assert s_inertias == Counter({(2, 0, 0): 1088, (1, 0, 1): 8})
    assert line_signatures == Counter({0: 1088, 2: 8})
    record_digest = hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()

    result = {
        "algorithm": "exact Fraction inverse and rank-two congruence",
        "base_assignments": 8,
        "line_signature_counts": {
            str(key): value for key, value in sorted(line_signatures.items())
        },
        "pair_cases": pair_cases,
        "record_sha256": record_digest,
        "response_inertia_counts": {
            ",".join(map(str, key)): value for key, value in sorted(s_inertias.items())
        },
        "status": "VERIFIED",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
