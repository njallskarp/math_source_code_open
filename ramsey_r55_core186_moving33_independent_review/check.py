#!/usr/bin/env python3
"""Clean-room audit of the saved Core186 moving 33-core obstruction.

The only target inputs are the pinned parent edge list and compact DIMACS
obstruction.  This checker does not read the target RUP/DRAT certificates,
generated full formula, solver output, or Python source.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


PARENT_SHA256 = "f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441"
OBSTRUCTION_SHA256 = "d661bb72385a71aff9b37c1cbe611b6e61169d3e5eef76ab5bc277b8b99e0c12"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_parent(path: Path) -> tuple[set[tuple[int, int]], str]:
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    require(digest == PARENT_SHA256, "unexpected parent SHA-256")
    lines = raw.decode("ascii").splitlines()
    require(lines and lines[0] == "43", "expected a 43-vertex parent")
    edges: set[tuple[int, int]] = set()
    previous = (-1, -1)
    for number, line in enumerate(lines[1:], 2):
        words = line.split()
        require(len(words) == 2, f"bad parent row at line {number}")
        u, v = map(int, words)
        require(0 <= u < v < 43, f"bad parent pair at line {number}")
        require((u, v) > previous, f"unsorted or repeated pair at line {number}")
        edges.add((u, v))
        previous = (u, v)
    require(len(edges) == 457, "unexpected parent edge count")
    return edges, digest


def literal_key(literal: int) -> tuple[int, bool]:
    return abs(literal), literal < 0


def parse_dimacs(path: Path) -> tuple[tuple[tuple[int, ...], ...], str]:
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    require(digest == OBSTRUCTION_SHA256, "unexpected obstruction SHA-256")
    variables = expected = None
    clauses: list[tuple[int, ...]] = []
    seen: set[frozenset[int]] = set()
    for number, raw_line in enumerate(raw.decode("ascii").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            require(variables is None and not clauses, f"misplaced header at line {number}")
            words = line.split()
            require(len(words) == 4 and words[:2] == ["p", "cnf"], "bad DIMACS header")
            variables, expected = map(int, words[2:])
            continue
        require(variables is not None, "clause before DIMACS header")
        values = list(map(int, line.split()))
        require(
            values and values[-1] == 0 and 0 not in values[:-1],
            f"bad clause terminator at line {number}",
        )
        literals = values[:-1]
        require(
            all(1 <= abs(literal) <= variables for literal in literals),
            f"out-of-range literal at line {number}",
        )
        require(
            len({abs(literal) for literal in literals}) == len(literals),
            f"repeated variable or tautology at line {number}",
        )
        require(len(literals) in (4, 5), f"nonphysical width at line {number}")
        logical_clause = frozenset(literals)
        require(logical_clause not in seen, f"duplicate logical clause at line {number}")
        seen.add(logical_clause)
        clauses.append(tuple(sorted(literals, key=literal_key)))
    require(variables == 32, "expected exactly 32 normalized switch variables")
    require(expected == 494 == len(clauses), "unexpected DIMACS clause count")
    return tuple(clauses), digest


def red_edge(edges: set[tuple[int, int]], u: int, v: int) -> int:
    require(u != v, "loop queried as an edge")
    return int(tuple(sorted((u, v))) in edges)


def physical_audit(
    edges: set[tuple[int, int]], clauses: tuple[tuple[int, ...], ...]
) -> dict[str, object]:
    widths: Counter[int] = Counter()
    colors: Counter[int] = Counter()
    vertices_used: set[int] = set()
    event_hash = sha256()
    for index, clause in enumerate(clauses):
        spins = {abs(literal): int(literal < 0) for literal in clause}
        if len(clause) == 4:
            spins[0] = 0
        require(len(spins) == 5, f"clause {index} does not name five vertices")
        vertices = tuple(sorted(spins))
        switched = [
            red_edge(edges, u, v) ^ spins[u] ^ spins[v]
            for u, v in combinations(vertices, 2)
        ]
        require(
            switched == [switched[0]] * 10,
            f"clause {index} is not a physical monochromatic event",
        )
        color = switched[0]
        widths[len(clause)] += 1
        colors[color] += 1
        vertices_used.update(vertices)
        event_hash.update(
            (
                f"{index}:{color}:{','.join(map(str, vertices))}:"
                + "".join(str(spins[v]) for v in vertices)
                + "\n"
            ).encode("ascii")
        )

    core_red_edges = sum(
        red_edge(edges, u, v) for u, v in combinations(range(33), 2)
    )
    require(core_red_edges == 270, "unexpected moving-core edge count")
    original_colors: Counter[int] = Counter()
    five_sets = 0
    for vertices in combinations(range(33), 5):
        pair_colors = [
            red_edge(edges, u, v) for u, v in combinations(vertices, 2)
        ]
        if pair_colors == [0] * 10:
            original_colors[0] += 1
        elif pair_colors == [1] * 10:
            original_colors[1] += 1
        five_sets += 1
    require(five_sets == 237336, "wrong physical five-set count")
    require(
        [original_colors[0], original_colors[1]] == [27, 30],
        "unexpected original defect counts",
    )
    require(vertices_used == set(range(33)), "some moving-core vertex is unused")
    return {
        "clauses": len(clauses),
        "colors": {"blue": colors[0], "red": colors[1]},
        "event_stream_sha256": event_hash.hexdigest(),
        "original_defects": {"blue": original_colors[0], "red": original_colors[1]},
        "physical_five_sets": five_sets,
        "red_edges": core_red_edges,
        "vertices": 33,
        "widths": {str(width): widths[width] for width in sorted(widths)},
    }


def canonical(clauses: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(set(clauses), key=lambda row: (len(row), row)))


def set_literal(
    clauses: tuple[tuple[int, ...], ...], literal: int
) -> tuple[tuple[tuple[int, ...], ...] | None, bool]:
    reduced: list[tuple[int, ...]] = []
    opposite = -literal
    for clause in clauses:
        if literal in clause:
            continue
        if opposite not in clause:
            reduced.append(clause)
            continue
        shorter = tuple(entry for entry in clause if entry != opposite)
        if not shorter:
            return None, True
        reduced.append(shorter)
    return canonical(reduced), False


def propagate(
    clauses: tuple[tuple[int, ...], ...]
) -> tuple[tuple[tuple[int, ...], ...] | None, tuple[int, ...], bool]:
    assignments: dict[int, bool] = {}
    units: list[int] = []
    current = clauses
    while True:
        new_units = sorted(
            (clause[0] for clause in current if len(clause) == 1),
            key=literal_key,
        )
        if not new_units:
            return current, tuple(units), False
        for literal in new_units:
            variable = abs(literal)
            value = literal > 0
            if variable in assignments:
                if assignments[variable] != value:
                    return None, tuple(units), True
                continue
            assignments[variable] = value
            units.append(literal)
            simplified, contradiction = set_literal(current, literal)
            if contradiction:
                return None, tuple(units), True
            require(simplified is not None, "missing propagated formula")
            current = simplified


def choose_variable(clauses: tuple[tuple[int, ...], ...]) -> int:
    maximum_width = max(map(len, clauses))
    scores: Counter[int] = Counter()
    for clause in clauses:
        weight = 1 << (maximum_width - len(clause))
        for literal in clause:
            scores[abs(literal)] += weight
    return min(scores, key=lambda variable: (-scores[variable], variable))


@dataclass
class SearchStats:
    recursive_states: int = 0
    decisions: int = 0
    contradiction_leaves: int = 0
    satisfying_leaves: int = 0
    memo_hits: int = 0
    propagated_literals: int = 0
    maximum_depth: int = 0


def exhaustive_dpll(
    clauses: tuple[tuple[int, ...], ...]
) -> tuple[bool, dict[str, int], str]:
    memo: dict[tuple[tuple[int, ...], ...], tuple[bool, bytes]] = {}
    stats = SearchStats()

    def visit(state: tuple[tuple[int, ...], ...], depth: int) -> tuple[bool, bytes]:
        stats.recursive_states += 1
        stats.maximum_depth = max(stats.maximum_depth, depth)
        reduced, units, contradiction = propagate(state)
        stats.propagated_literals += len(units)
        unit_bytes = ",".join(map(str, units)).encode("ascii")
        if contradiction:
            stats.contradiction_leaves += 1
            return False, sha256(b"C|" + unit_bytes).digest()
        require(reduced is not None, "missing reduced formula")
        if not reduced:
            stats.satisfying_leaves += 1
            return True, sha256(b"S|" + unit_bytes).digest()
        if reduced in memo:
            stats.memo_hits += 1
            satisfiable, child_hash = memo[reduced]
            return satisfiable, sha256(
                b"M|" + unit_bytes + b"|" + child_hash
            ).digest()

        variable = choose_variable(reduced)
        stats.decisions += 1
        children: list[tuple[bool, bytes]] = []
        for literal in (-variable, variable):
            child, child_contradiction = set_literal(reduced, literal)
            if child_contradiction:
                stats.contradiction_leaves += 1
                result = False, sha256(f"C|{literal}".encode("ascii")).digest()
            else:
                require(child is not None, "missing branch formula")
                result = visit(child, depth + 1)
            children.append(result)
            if result[0]:
                digest = sha256(
                    b"W|" + unit_bytes + b"|" + result[1]
                ).digest()
                memo[reduced] = True, digest
                return True, digest
        digest = sha256(
            b"U|"
            + unit_bytes
            + f"|{variable}|".encode("ascii")
            + children[0][1]
            + children[1][1]
        ).digest()
        memo[reduced] = False, digest
        return False, digest

    satisfiable, tree_hash = visit(canonical(list(clauses)), 0)
    return satisfiable, vars(stats), tree_hash.hex()


def brute_force_satisfiable(
    clauses: tuple[tuple[int, ...], ...], variables: int
) -> bool:
    return any(
        all(
            any(
                bool(mask >> (abs(literal) - 1) & 1) == (literal > 0)
                for literal in clause
            )
            for clause in clauses
        )
        for mask in range(1 << variables)
    )


def algorithm_controls() -> dict[str, int]:
    pool = (
        (1,),
        (-1,),
        (2,),
        (-2,),
        (3,),
        (-3,),
        (1, 2),
        (-1, -2),
        (1, -2, 3),
    )
    checked = satisfiable = unsatisfiable = 0
    for selector in range(1 << len(pool)):
        formula = tuple(
            pool[index] for index in range(len(pool)) if selector >> index & 1
        )
        brute = brute_force_satisfiable(formula, 3)
        obtained, _, _ = exhaustive_dpll(formula)
        require(obtained == brute, f"DPLL control mismatch at selector {selector}")
        checked += 1
        satisfiable += int(brute)
        unsatisfiable += int(not brute)
    return {
        "small_formulas_checked": checked,
        "satisfiable": satisfiable,
        "unsatisfiable": unsatisfiable,
    }


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def scope_audit(edges: set[tuple[int, int]]) -> dict[str, object]:
    action = [
        3 * (vertex // 3) + (vertex + 1) % 3 if vertex < 33 else vertex
        for vertex in range(43)
    ]
    require(
        all(
            red_edge(edges, u, v) == red_edge(edges, action[u], action[v])
            for u, v in combinations(range(33), 2)
        ),
        "moving core is not invariant under the stated action",
    )

    equations: list[int] = []
    for u, v in combinations(range(33), 2):
        row = 0
        for vertex in (u, v, action[u], action[v]):
            if vertex:
                row ^= 1 << (vertex - 1)
        equations.append(row)
    rank = gf2_rank(equations)
    switch_dimension = 32 - rank
    require(rank == 22 and switch_dimension == 10, "wrong invariant-switch space")

    attachment_pairs = {
        (u, v)
        for u, v in combinations(range(43), 2)
        if u >= 33 or v >= 33
    }
    require(len(attachment_pairs) == 375, "wrong attachment-pair count")
    remaining = set(attachment_pairs)
    orbit_sizes: Counter[int] = Counter()
    while remaining:
        start = min(remaining)
        orbit: set[tuple[int, int]] = set()
        pair = start
        while pair not in orbit:
            orbit.add(pair)
            pair = tuple(sorted((action[pair[0]], action[pair[1]])))
        require(pair == start and orbit <= remaining, "bad attachment orbit")
        remaining -= orbit
        orbit_sizes[len(orbit)] += 1
    attachment_orbits = sum(orbit_sizes.values())
    require(
        orbit_sizes == Counter({3: 110, 1: 45}) and attachment_orbits == 155,
        "wrong attachment-orbit census",
    )

    full_exponent = 32 + len(attachment_pairs)
    same_action_exponent = switch_dimension + attachment_orbits
    require(full_exponent == 407, "wrong full-family exponent")
    require(same_action_exponent == 165, "wrong same-action exponent")
    return {
        "attachment_orbit_sizes": {
            str(size): orbit_sizes[size] for size in sorted(orbit_sizes)
        },
        "attachment_orbits": attachment_orbits,
        "attachment_pairs": len(attachment_pairs),
        "full_family": f"2^{full_exponent}",
        "full_family_size": str(1 << full_exponent),
        "invariance_equation_rank": rank,
        "normalized_switch_variables": 32,
        "same_action_family": f"2^{same_action_exponent}",
        "same_action_family_size": str(1 << same_action_exponent),
        "same_action_switch_dimension": switch_dimension,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parent", type=Path)
    parser.add_argument("obstruction", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    edges, parent_digest = parse_parent(args.parent)
    clauses, obstruction_digest = parse_dimacs(args.obstruction)
    physical = physical_audit(edges, clauses)
    satisfiable, search, tree_hash = exhaustive_dpll(clauses)
    require(not satisfiable, "compact physical obstruction is satisfiable")
    report = {
        "algorithm_controls": algorithm_controls(),
        "certificate_imported": False,
        "method": "physical edge-list audit plus exhaustive deterministic DPLL",
        "obstruction_sha256": obstruction_digest,
        "parent_sha256": parent_digest,
        "physical_audit": physical,
        "scope_audit": scope_audit(edges),
        "search": search,
        "search_tree_sha256": tree_hash,
        "status": "INDEPENDENTLY_VERIFIED_CORE186_MOVING33_SWITCH_OBSTRUCTION",
        "target_code_imported": False,
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
