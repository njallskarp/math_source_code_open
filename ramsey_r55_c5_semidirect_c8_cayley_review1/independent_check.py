#!/usr/bin/env python3
"""Independent exhaustive check of the C5 semidirect C8 Cayley obstruction.

This program does not read the researcher's certificate or source files. It
enumerates every five-set through the identity and uses a subset transform to
test all inverse-closed connection sets.
"""

from hashlib import sha256
from itertools import combinations


ELEMENTS = tuple((i, j) for j in range(8) for i in range(5))
LABEL = {g: n for n, g in enumerate(ELEMENTS)}
IDENTITY = (0, 0)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def mul(x, y):
    i, j = x
    k, ell = y
    return ((i + pow(2, j, 5) * k) % 5, (j + ell) % 8)


def inverse(x):
    candidates = [y for y in ELEMENTS
                  if mul(x, y) == IDENTITY and mul(y, x) == IDENTITY]
    need(len(candidates) == 1, f"inverse failure for {x}")
    return candidates[0]


def power(x, exponent):
    result = IDENTITY
    for _ in range(exponent):
        result = mul(result, x)
    return result


def main():
    need(all(mul(IDENTITY, x) == x == mul(x, IDENTITY) for x in ELEMENTS),
         "identity law failed")
    need(all(mul(mul(x, y), z) == mul(x, mul(y, z))
             for x in ELEMENTS for y in ELEMENTS for z in ELEMENTS),
         "associativity failed")
    inverses = tuple(inverse(x) for x in ELEMENTS)
    a, b = (1, 0), (0, 1)
    need(power(a, 5) == IDENTITY and power(b, 8) == IDENTITY,
         "generator orders failed")
    need(mul(mul(b, a), inverse(b)) == mul(a, a),
         "semidirect-product conjugation relation failed")
    need({mul(power(a, i), power(b, j)) for i in range(5) for j in range(8)}
         == set(ELEMENTS), "normal forms do not generate all forty elements")

    inverse_parts = sorted({tuple(sorted({LABEL[x], LABEL[inverse(x)]}))
                            for x in ELEMENTS if x != IDENTITY})
    need(len(inverse_parts) == 20, "expected twenty inverse classes")
    need(sorted(map(len, inverse_parts)) == [1] + [2] * 19,
         "expected nineteen pairs and one involution")
    need([part for part in inverse_parts if len(part) == 1] == [(20,)],
         "the unique nonidentity involution is not b^4")
    variable = {x: k for k, part in enumerate(inverse_parts) for x in part}
    need(set(variable) == set(range(1, 40)),
         "inverse classes do not partition the nonidentity elements")

    def edge_variable(u, v):
        difference = mul(inverses[u], ELEMENTS[v])
        return variable[LABEL[difference]]

    edge_variables = [[None if u == v else edge_variable(u, v)
                       for v in range(40)] for u in range(40)]
    need(all(edge_variables[u][v] == edge_variables[v][u]
             for u in range(40) for v in range(40)),
         "inverse closure did not produce undirected edge variables")

    # Verify directly that every left translation preserves every connection bit.
    for g in ELEMENTS:
        translated = [LABEL[mul(g, x)] for x in ELEMENTS]
        need(all(edge_variables[translated[u]][translated[v]] ==
                 edge_variables[u][v]
                 for u in range(40) for v in range(40) if u != v),
             "left translation does not preserve edge variables")

    supports = set()
    five_set_count = 0
    for tail in combinations(range(1, 40), 4):
        q = (0,) + tail
        support = 0
        for u, v in combinations(q, 2):
            support |= 1 << edge_variables[u][v]
        supports.add(support)
        five_set_count += 1
    need(five_set_count == 82_251, "five-set enumeration is incomplete")

    # subset_present[m] becomes 1 iff a five-set support is contained in m.
    # Such a set is red for m; a support contained in ~m gives a blue set.
    assignment_count = 1 << len(inverse_parts)
    subset_present = bytearray(assignment_count)
    for support in supports:
        subset_present[support] = 1
    for bit in range(len(inverse_parts)):
        step = 1 << bit
        for base in range(0, assignment_count, 2 * step):
            for offset in range(step):
                subset_present[base + step + offset] |= subset_present[base + offset]

    universe = assignment_count - 1
    uncovered = [m for m in range(assignment_count)
                 if not (subset_present[m] or subset_present[universe ^ m])]
    need(not uncovered,
         f"uncovered connection mask: {uncovered[0] if uncovered else 'none'}")

    support_bytes = b"".join(s.to_bytes(3, "little") for s in sorted(supports))
    print("VERIFIED_INDEPENDENT_CAYLEY40_EXHAUSTION")
    print(f"group_order={len(ELEMENTS)}")
    print(f"inverse_connection_classes={len(inverse_parts)}")
    print(f"five_sets_through_identity={five_set_count}")
    print(f"distinct_edge_variable_supports={len(supports)}")
    print(f"connection_masks_checked={assignment_count}")
    print(f"uncovered_masks={len(uncovered)}")
    print(f"support_list_sha256={sha256(support_bytes).hexdigest()}")


if __name__ == "__main__":
    main()
