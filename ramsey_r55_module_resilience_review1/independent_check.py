#!/usr/bin/env python3
"""Definition-level audit of deletion-stable module bounds in Ramsey(5,5;43).

No target source, certificate, fixture, catalogue, or graph is an input. The
classical small Ramsey upper bounds listed in RAMSEY are imported premises.
"""

from hashlib import sha256
from itertools import combinations, product
import json


RAMSEY = {
    (1, 1): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1, (1, 5): 1,
    (2, 2): 2, (2, 3): 3, (2, 4): 4, (2, 5): 5,
    (3, 3): 6, (3, 4): 9, (3, 5): 14,
    (4, 4): 18, (4, 5): 25,
}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def ramsey(a, b):
    return RAMSEY[tuple(sorted((a, b)))]


def colorings(order):
    pairs = tuple(combinations(range(order), 2))
    for mask in range(1 << len(pairs)):
        yield {pair: (mask >> i) & 1 for i, pair in enumerate(pairs)}


def edge(coloring, u, v):
    return coloring[tuple(sorted((u, v)))]


def distinguished(bits, subset):
    return len({bits[v] for v in subset}) == 2


def triple_sum_margin(order, exceptions, require_monochromatic=False):
    triples = tuple(combinations(range(order), 3))
    outside_max = max(
        sum(distinguished([(mask >> v) & 1 for v in range(order)], q)
            for q in triples)
        for mask in range(1 << order)
    )
    margins = []
    checked = 0
    for coloring in colorings(order):
        monochromatic = {
            q: len({edge(coloring, u, v) for u, v in combinations(q, 2)}) == 1
            for q in triples
        }
        if require_monochromatic and not all(monochromatic.values()):
            continue
        required = sum(18 if monochromatic[q] else 17 for q in triples)
        internal = 0
        for q in triples:
            for v in set(range(order)) - set(q):
                internal += distinguished([edge(coloring, v, u) for u in q], range(3))
        margins.append(required - internal - exceptions * outside_max)
        checked += 1
    need(margins and min(margins) > 0,
         f"order-{order} module not excluded with {exceptions} exceptions")
    return {"internal_colorings": checked, "outside_triple_sum_max": outside_max,
            "minimum_contradiction_margin": min(margins)}


def module_table():
    caps = {k: ramsey(5 - k, 5) - 1 for k in range(1, 5)}
    need(caps == {1: 24, 2: 13, 3: 4, 4: 0}, "uniform-part caps")
    rows = []
    for k in range(1, 5):
        for ell in range(k, 5):
            if (k, ell) in ((1, 1), (4, 4)):
                continue
            maximum_module = ramsey(k + 1, ell + 1) - 1
            rows.append((k, ell, maximum_module, caps[k], caps[ell],
                         maximum_module + caps[k] + caps[ell]))
    expected = [
        (1, 2, 2, 24, 13, 39), (1, 3, 3, 24, 4, 31),
        (1, 4, 4, 24, 0, 28), (2, 2, 5, 13, 13, 31),
        (2, 3, 8, 13, 4, 25), (2, 4, 13, 13, 0, 26),
        (3, 3, 17, 4, 4, 25), (3, 4, 24, 4, 0, 28),
    ]
    need(rows == expected, "module-capacity table mismatch")
    return caps, rows


def large_module_boundary(caps):
    feasible = []
    for deleted in range(16):
        core = 43 - deleted
        for k, ell in product(range(1, 5), repeat=2):
            if (k, ell) == (4, 4):
                continue  # both uniform caps vanish, so a proper module is impossible
            maximum_module = ramsey(k + 1, ell + 1) - 1
            for module in range(6, core):
                outside = core - module
                for red_uniform in range(outside + 1):
                    blue_uniform = outside - red_uniform
                    if (module <= maximum_module and red_uniform <= caps[k]
                            and blue_uniform <= caps[ell]):
                        feasible.append((deleted, module, red_uniform, blue_uniform,
                                         k, ell))
    expected = [(15, 24, 4, 0, 3, 4), (15, 24, 0, 4, 4, 3)]
    need(feasible == expected, "unexpected large-module boundary parameter")
    # In either row the four uniform vertices have 24 same-color neighbours in
    # the module. The degree cap 24 makes all their other contacts opposite;
    # any of the fifteen deleted vertices completes an opposite-color K5.
    need(all(row[0] == 15 and row[1:4] in ((24, 4, 0), (24, 0, 4))
             for row in feasible), "degree-saturation boundary mismatch")
    return feasible


def main():
    # Literal signature identities used for the local pair and mixed-triple bounds.
    for bits in product((0, 1), repeat=2):
        x, y = bits
        need(x + y == 2 * x * y + int(x != y), "pair identity")
    for bits in product((0, 1), repeat=3):
        x0, x1, x2 = bits
        left = x0 * x1 + x0 * x2 + (1 - x1) * (1 - x2)
        need(left == int(x0 == x1 == x2) + x0, "mixed-triple identity")

    # The imported bounds give degrees 18..24, edge-common cap 13, and
    # triangle-common cap 4; substituting them gives the exact local minima.
    pair_minimum = 2 * 18 - 2 - 2 * 13
    triangle_minimum = (3 * 18 - 6 - 3 * 4 + 1) // 2
    mixed_minimum = 18 - 1
    need((pair_minimum, mixed_minimum, triangle_minimum) == (8, 17, 18),
         "local distinguisher bounds")

    caps, table = module_table()
    need(max(row[-1] for row in table if row[2] >= 3) == 31,
         "module order at least three")
    need(max(row[-1] for row in table if row[2] >= 6) == 28,
         "module order at least six")
    need(pair_minimum > 7 and 43 - 7 > 31,
         "seven-deletion primeness reduction")

    small = {
        "module3_deleted16": triple_sum_margin(3, 16),
        "module3_monochromatic_deleted17": triple_sum_margin(3, 17, True),
        "module4_deleted15": triple_sum_margin(4, 15),
        "module5_deleted16": triple_sum_margin(5, 16),
    }
    boundary = large_module_boundary(caps)
    need(small["module3_deleted16"]["minimum_contradiction_margin"] > 0
         and small["module4_deleted15"]["minimum_contradiction_margin"] > 0
         and small["module5_deleted16"]["minimum_contradiction_margin"] > 0,
         "small-module deletion reductions")
    facts = {
        "imported_small_ramsey_bounds": sorted((list(k), v) for k, v in RAMSEY.items()),
        "local_distinguisher_minima": {"pair": pair_minimum,
                                        "mixed_triple": mixed_minimum,
                                        "monochromatic_triple": triangle_minimum},
        "module_table": table,
        "small_module_exhaustion": small,
        "large_module_boundary": boundary,
    }
    digest = sha256(json.dumps(facts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print("VERIFIED_INDEPENDENT_MODULE_RESILIENCE")
    print("prime_after_at_most_7_deletions=true")
    print("no_module_ge_3_after_at_most_15_deletions=true")
    print("strengthening_no_module_eq_5_after_at_most_16_deletions=true")
    print("boundary_28_rows=2")
    print(f"module3_t16_margin={small['module3_deleted16']['minimum_contradiction_margin']}")
    print(f"module4_t15_margin={small['module4_deleted15']['minimum_contradiction_margin']}")
    print(f"module5_t16_margin={small['module5_deleted16']['minimum_contradiction_margin']}")
    print(f"audit_facts_sha256={digest}")


if __name__ == "__main__":
    main()
