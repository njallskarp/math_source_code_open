#!/usr/bin/env python3
"""Independent exact audit of the Paley(43) ordering obstruction.

The checker rebuilds the comparison formula from the theorem statement and
solves all normalized kernel cases from scratch.  It reads the author's JSON
only to compare the advertised case list and record its hash; the supplied
refutation trees are deliberately ignored.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys


P = 43
Q_DECLARED = (1, 4, 6, 9, 10, 11, 13, 14, 15, 16, 17,
              21, 23, 24, 25, 31, 35, 36, 38, 40, 41)
A_DECLARED = (10, 11, 14, 15, 16, 17, 24, 25, 36, 41)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))


def arrow(x: int, y: int) -> bool:
    """The physical arrow x -> y, using Euler's criterion."""
    return x != y and pow((y - x) % P, (P - 1) // 2, P) == 1


def arrow_order(vertices: tuple[int, ...]) -> tuple[int, ...] | None:
    """Return the unique source-deletion order, or None if nontransitive."""
    left = set(vertices)
    result = []
    while left:
        sources = [x for x in left if all(x == y or arrow(x, y) for y in left)]
        if len(sources) != 1:
            return None
        x = sources[0]
        result.append(x)
        left.remove(x)
    return tuple(result)


def literal(pair_ids: dict[tuple[int, int], int], x: int, y: int) -> int:
    """Positive means x precedes y for the increasing underlying pair."""
    return pair_ids[x, y] if x < y else -pair_ids[y, x]


def local_formula() -> tuple[list[tuple[int, ...]], dict[tuple[int, int], int], tuple[int, int]]:
    pair_ids = {pair: i + 1 for i, pair in enumerate(itertools.combinations(Q_DECLARED, 2))}
    clauses: list[tuple[int, ...]] = []
    for a, b, c in itertools.combinations(Q_DECLARED, 3):
        ab, bc, ac = (literal(pair_ids, a, b), literal(pair_ids, b, c),
                      literal(pair_ids, a, c))
        clauses.extend(((-ab, -bc, ac), (ab, bc, -ac)))
    counts = []
    for size, sign in ((4, -1), (5, 1)):
        count = 0
        for subset in itertools.combinations(Q_DECLARED, size):
            order = arrow_order(subset)
            if order is None:
                continue
            count += 1
            clauses.append(tuple(sign * literal(pair_ids, x, y)
                                 for x, y in zip(order, order[1:])))
        counts.append(count)
    clauses.extend(((literal(pair_ids, 1, v),) for v in Q_DECLARED if v != 1))
    return clauses, pair_ids, (counts[0], counts[1])


def kernel_orders() -> tuple[list[tuple[int, ...]], dict[str, int]]:
    """Literal 10! census, with no prefix pruning."""
    index = {v: i for i, v in enumerate(A_DECLARED)}
    red_patterns = []
    blue_patterns = []
    for subset in itertools.combinations(A_DECLARED, 3):
        order = arrow_order(subset)
        if order is not None:
            red_patterns.append(tuple(index[v] for v in order))
    for subset in itertools.combinations(A_DECLARED, 5):
        order = arrow_order(subset)
        if order is not None:
            blue_patterns.append(tuple(index[v] for v in order))

    admissible = []
    red_free = 0
    total = 0
    for permutation in itertools.permutations(range(10)):
        total += 1
        positions = [0] * 10
        for position, vertex in enumerate(permutation):
            positions[vertex] = position
        if any(positions[a] < positions[b] < positions[c]
               for a, b, c in red_patterns):
            continue
        red_free += 1
        if any(positions[a] > positions[b] > positions[c] > positions[d] > positions[e]
               for a, b, c, d, e in blue_patterns):
            continue
        admissible.append(tuple(A_DECLARED[v] for v in permutation))
    return admissible, {
        "permutations": total,
        "transitive_triples": len(red_patterns),
        "transitive_fives": len(blue_patterns),
        "red_triangle_free_orders": red_free,
        "admissible_orders": len(admissible),
    }


def propagate(clauses: list[tuple[int, ...]], values: list[int]) -> list[int] | None:
    """Definition-level unit propagation over an immutable clause list."""
    values = values.copy()
    while True:
        changed = False
        for clause in clauses:
            pending = 0
            last = 0
            satisfied = False
            for term in clause:
                value = values[abs(term)]
                if value and (value > 0) == (term > 0):
                    satisfied = True
                    break
                if value == 0:
                    pending += 1
                    last = term
            if satisfied:
                continue
            if pending == 0:
                return None
            if pending == 1:
                wanted = 1 if last > 0 else -1
                current = values[abs(last)]
                if current == -wanted:
                    return None
                if current == 0:
                    values[abs(last)] = wanted
                    changed = True
        if not changed:
            return values


def solve(clauses: list[tuple[int, ...]], variable_count: int) -> tuple[list[int] | None, int, int]:
    """Complete DPLL search generated anew; returns model/nodes/conflicts."""
    nodes = 0
    conflicts = 0

    def visit(values: list[int]) -> list[int] | None:
        nonlocal nodes, conflicts
        nodes += 1
        values = propagate(clauses, values)
        if values is None:
            conflicts += 1
            return None

        shortest: tuple[int, ...] | None = None
        for clause in clauses:
            if any(values[abs(term)] and (values[abs(term)] > 0) == (term > 0)
                   for term in clause):
                continue
            unresolved = tuple(term for term in clause if values[abs(term)] == 0)
            if shortest is None or (len(unresolved), tuple(map(abs, unresolved))) < (
                    len(shortest), tuple(map(abs, shortest))):
                shortest = unresolved
        if shortest is None:
            return values
        # Deliberately unlike the author's weighted-occurrence branching:
        # branch on the smallest-index variable in a shortest residual clause.
        variable = min(map(abs, shortest))
        for wanted in (1, -1):
            child = values.copy()
            child[variable] = wanted
            model = visit(child)
            if model is not None:
                return model
        return None

    model = visit([0] * (variable_count + 1))
    return model, nodes, conflicts


def solver_controls() -> int:
    """Compare the whole solver with brute force on every <=3-clause 3-SAT toy."""
    possible = []
    for signs in itertools.product((-1, 0, 1), repeat=3):
        clause = tuple((i + 1) * sign for i, sign in enumerate(signs) if sign)
        if clause:
            possible.append(clause)
    checked = 0
    for count in range(4):
        for formula in itertools.combinations(possible, count):
            brute = any(all(any(((bits >> (abs(term) - 1)) & 1) == (term > 0)
                                for term in clause) for clause in formula)
                        for bits in range(8))
            model, _, _ = solve(list(formula), 3)
            require((model is not None) == brute, "DPLL/brute-force mismatch")
            checked += 1
    return checked


def encoding_controls() -> dict[str, int]:
    """Check comparison transitivity and clique clauses against physical colors."""
    labels = tuple(range(5))
    pairs = tuple(itertools.combinations(labels, 2))
    pair_index = {pair: i for i, pair in enumerate(pairs)}
    order_masks = set()
    for order in itertools.permutations(labels):
        position = {v: i for i, v in enumerate(order)}
        order_masks.add(sum(1 << pair_index[x, y] for x, y in pairs
                            if position[x] < position[y]))
    transitive_masks = set()
    for mask in range(1 << len(pairs)):
        def before(x: int, y: int) -> bool:
            return bool(mask >> pair_index[min(x, y), max(x, y)] & 1) == (x < y)
        if all(not (before(a, b) and before(b, c)) or before(a, c)
               for a, b, c in itertools.permutations(labels, 3)):
            transitive_masks.add(mask)
    require(transitive_masks == order_masks and len(transitive_masks) == 120,
            "comparison clauses do not encode exactly the linear orders")

    physical_cases = 0
    for five in itertools.combinations(Q_DECLARED, 5):
        red_orders = [order for four in itertools.combinations(five, 4)
                      if (order := arrow_order(four)) is not None]
        blue_order = arrow_order(five)
        for order in itertools.permutations(five):
            position = {v: i for i, v in enumerate(order)}
            def red(x: int, y: int) -> bool:
                return arrow(x, y) if position[x] < position[y] else arrow(y, x)
            physical_bad = (
                any(all(red(x, y) for x, y in itertools.combinations(four, 2))
                    for four in itertools.combinations(five, 4))
                or all(not red(x, y) for x, y in itertools.combinations(five, 2))
            )
            encoded_bad = (
                any(all(position[x] < position[y] for x, y in zip(chain, chain[1:]))
                    for chain in red_orders)
                or (blue_order is not None and
                    all(position[x] > position[y]
                        for x, y in zip(blue_order, blue_order[1:])))
            )
            require(physical_bad == encoded_bad, "physical/clause semantic mismatch")
            physical_cases += 1
    return {"five_symbol_comparison_assignments": 1024,
            "linear_order_assignments": len(transitive_masks),
            "physical_five_subset_orders": physical_cases}


def symmetry_checks() -> dict[str, int]:
    require(is_prime(P), "modulus is not prime")
    squares = tuple(sorted({x * x % P for x in range(1, P)}))
    require(squares == Q_DECLARED, "declared Q is not the nonzero-square set")
    require(all(arrow(x, y) != arrow(y, x)
                for x, y in itertools.combinations(range(P), 2)), "not a tournament")
    require(all(arrow(x, y) == arrow((x + b) % P, (y + b) % P)
                for b in range(P) for x, y in itertools.combinations(range(P), 2)),
            "translation failure")
    require(all(tuple(sorted(a * q % P for q in Q_DECLARED)) == Q_DECLARED
                for a in Q_DECLARED), "square action does not preserve Q")
    require({a * 1 % P for a in Q_DECLARED} == set(Q_DECLARED),
            "square action not transitive on Q")
    require(all(arrow(x, y) == arrow(a * x % P, a * y % P)
                for a in Q_DECLARED for x, y in itertools.combinations(range(P), 2)),
            "square multiplication does not preserve arrows")
    require(all(arrow(x, y) != arrow(-x % P, -y % P)
                for x, y in itertools.combinations(range(P), 2)),
            "negation does not reverse arrows")
    derived_a = tuple(q for q in Q_DECLARED if arrow(1, q))
    require(derived_a == A_DECLARED, "declared A is not the local outneighborhood")
    for root in range(P):
        plus = {(root + q) % P for q in Q_DECLARED}
        minus = {(root - q) % P for q in Q_DECLARED}
        require(plus.isdisjoint(minus) and plus | minus | {root} == set(range(P)),
                "root sides do not partition the field")
        require(all(arrow(root, v) for v in plus), "plus side is not the root outneighborhood")
        require(all(arrow(v, root) for v in minus), "minus side is not the root inneighborhood")
    return {"translations": P, "square_multipliers": len(Q_DECLARED),
            "normalized_first_vertices": len(Q_DECLARED), "root_partitions": P}


def main(path: Path) -> dict[str, object]:
    symmetry = symmetry_checks()
    base, pair_ids, transitive_counts = local_formula()
    require(len(pair_ids) == 210 and len(base) == 5452, "local formula dimensions")
    require(transitive_counts == (1722, 1050), "transitive-subset census")
    orders, census = kernel_orders()
    require(census == {
        "permutations": 3628800,
        "transitive_triples": 82,
        "transitive_fives": 8,
        "red_triangle_free_orders": 70,
        "admissible_orders": 51,
    }, "kernel census")

    author_bytes = path.read_bytes()
    author = json.loads(author_bytes)
    require(type(author) is dict and type(author.get("cases")) is list,
            "malformed author certificate")
    require([list(order) for order in orders] == [case.get("order") for case in author["cases"]],
            "author case list differs from independent 10! census")

    totals = {"nodes": 0, "conflicts": 0, "max_nodes": 0}
    for order in orders:
        clauses = list(base)
        clauses.extend((literal(pair_ids, x, y),) for x, y in zip(order, order[1:]))
        model, nodes, conflicts = solve(clauses, len(pair_ids))
        require(model is None, "counterexample order extends one kernel case")
        totals["nodes"] += nodes
        totals["conflicts"] += conflicts
        totals["max_nodes"] = max(totals["max_nodes"], nodes)

    return {
        "status": "INDEPENDENTLY_VERIFIED_PALEY43_ORDERING_OBSTRUCTION",
        "prime": P,
        "local_vertices": len(Q_DECLARED),
        "kernel_vertices": len(A_DECLARED),
        "kernel_census": census,
        "local_variables": len(pair_ids),
        "local_clauses_before_case_units": len(base),
        "transitive_four_five_counts": list(transitive_counts),
        "independent_dpll": totals,
        "solver_truth_table_formulas": solver_controls(),
        "encoding_controls": encoding_controls(),
        "symmetry_checks": symmetry,
        "author_case_list_match": True,
        "author_refutation_trees_imported": False,
        "author_certificate_sha256": hashlib.sha256(author_bytes).hexdigest(),
        "guaranteed_distinct_monochromatic_fives": 2,
        "ramsey43_constructed": False,
        "ramsey_bound_improved": False,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: independent_check.py AUTHOR_CERTIFICATE.json")
    print(json.dumps(main(Path(sys.argv[1])), sort_keys=True, indent=2))
