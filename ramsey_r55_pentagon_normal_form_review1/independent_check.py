#!/usr/bin/env python3
"""Independent audit of the 842-variable Ramsey(5,5;43) pentagon frame.

No target module is imported.  The checker reconstructs the pinned graph and
physical Ramsey clauses from the theorem statement, validates the generated
DIMACS stream, obtains the clause table again by component factorisation, and
checks the two public transport controls directly.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys


N = 43
BLOCKS = (
    (2, 3, 4, 5, 6),
    (7, 8, 9, 10, 11),
    (12, 13, 14, 15, 16),
    (17, 18, 19, 20, 21),
    (22, 23, 24, 25, 26),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def frame_pins(n: int = 43, cycles: int = 5, joined: bool = True) -> dict[tuple[int, int], int]:
    offset = 2 if joined else 0
    require(cycles >= int(joined) and n >= offset + 5 * cycles, "frame dimensions")
    fixed: dict[tuple[int, int], int] = {}
    for block_number in range(cycles):
        block = tuple(range(offset + 5 * block_number, offset + 5 * block_number + 5))
        cycle = {tuple(sorted((block[i], block[(i + 1) % 5]))) for i in range(5)}
        for pair in itertools.combinations(block, 2):
            fixed[pair] = int(pair in cycle)
    if joined:
        fixed[0, 1] = 1
        for root in (0, 1):
            for vertex in range(2, 7):
                fixed[root, vertex] = 1
    return fixed


def free_pairs(n: int, fixed: dict[tuple[int, int], int]) -> tuple[tuple[int, int], ...]:
    return tuple(pair for pair in itertools.combinations(range(n), 2) if pair not in fixed)


def expected_clause(
    vertices: tuple[int, ...],
    color: int,
    fixed: dict[tuple[int, int], int],
    variable: dict[tuple[int, int], int],
) -> tuple[int, ...] | None:
    terms = []
    for pair in itertools.combinations(vertices, 2):
        if pair in fixed:
            if fixed[pair] != color:
                return None
        else:
            terms.append((-1 if color else 1) * variable[pair])
    return tuple(terms)


def audit_dimacs(path: Path) -> dict[str, object]:
    fixed = frame_pins()
    free = free_pairs(N, fixed)
    variable = {pair: i + 1 for i, pair in enumerate(free)}
    counts: Counter[int] = Counter()
    lengths: Counter[int] = Counter()
    physical_cases = 0
    path = path.resolve()
    with path.open(encoding="ascii") as source:
        header = source.readline().split()
        require(header[:2] == ["p", "cnf"] and len(header) == 4, "DIMACS header")
        require(int(header[2]) == len(free), "DIMACS variable count")
        declared_clauses = int(header[3])
        for color in (1, 0):
            for vertices in itertools.combinations(range(N), 5):
                physical_cases += 1
                expected = expected_clause(vertices, color, fixed, variable)
                if expected is None:
                    continue
                row = source.readline()
                require(bool(row), "missing DIMACS clause")
                actual = tuple(map(int, row.split()))
                require(actual == expected + (0,),
                        f"clause mismatch at color={color}, vertices={vertices}")
                require(len({abs(term) for term in expected}) == len(expected),
                        "repeated variable in physical clause")
                counts[color] += 1
                lengths[len(expected)] += 1
        require(source.read() == "", "extra DIMACS content")
    require(sum(counts.values()) == declared_clauses, "DIMACS clause count")
    return {
        "variables": len(free),
        "clauses": sum(counts.values()),
        "red_clauses": counts[1],
        "blue_clauses": counts[0],
        "length_histogram": {str(k): lengths[k] for k in sorted(lengths)},
        "physical_five_color_cases": physical_cases,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def fixed_components(n: int, fixed: dict[tuple[int, int], int]) -> list[tuple[int, ...]]:
    adjacency = [set() for _ in range(n)]
    for u, v in fixed:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(n))
    components = []
    while unseen:
        start = min(unseen)
        stack = [start]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen -= component
        components.append(tuple(sorted(component)))
    return components


def multiply(left: Counter[tuple[int, int]], right: Counter[tuple[int, int]]) -> Counter[tuple[int, int]]:
    result: Counter[tuple[int, int]] = Counter()
    for (size_a, pins_a), count_a in left.items():
        for (size_b, pins_b), count_b in right.items():
            if size_a + size_b <= 5:
                result[size_a + size_b, pins_a + pins_b] += count_a * count_b
    return result


def factorized_clause_counts(n: int = 43, cycles: int = 5, joined: bool = True) -> dict[str, object]:
    """Count clauses by factoring over connected components of the pin graph."""
    fixed = frame_pins(n, cycles, joined)
    answer = {}
    for color in (1, 0):
        polynomial: Counter[tuple[int, int]] = Counter({(0, 0): 1})
        for component in fixed_components(n, fixed):
            inventory: Counter[tuple[int, int]] = Counter()
            for size in range(min(5, len(component)) + 1):
                for chosen in itertools.combinations(component, size):
                    pinned = [fixed[pair] for pair in itertools.combinations(chosen, 2)
                              if pair in fixed]
                    if any(value != color for value in pinned):
                        continue
                    inventory[size, len(pinned)] += 1
            polynomial = multiply(polynomial, inventory)
        answer[color] = {str(10 - pin_count): count
                         for (size, pin_count), count in sorted(polynomial.items())
                         if size == 5}
    return {
        "red": answer[1],
        "blue": answer[0],
        "total": sum(sum(table.values()) for table in answer.values()),
    }


def regular_five_control() -> dict[str, int]:
    pairs = tuple(itertools.combinations(range(5), 2))
    counts: Counter[int] = Counter()
    for mask in range(1 << len(pairs)):
        degrees = [0] * 5
        for bit, (u, v) in enumerate(pairs):
            if mask >> bit & 1:
                degrees[u] += 1
                degrees[v] += 1
        if len(set(degrees)) != 1:
            continue
        degree = degrees[0]
        require(degree in (0, 2, 4), "impossible regular-five degree")
        if degree == 2:
            # A finite simple 2-regular graph on five vertices must be one C5.
            reached = {0}
            while True:
                larger = reached | {v for bit, (u, v) in enumerate(pairs)
                                    if mask >> bit & 1 and (u in reached or v in reached)
                                    for v in (u, v)}
                if larger == reached:
                    break
                reached = larger
            require(len(reached) == 5, "disconnected 2-regular graph on five vertices")
            complement = ((1 << len(pairs)) - 1) ^ mask
            complement_degrees = [sum(complement >> bit & 1 for bit, pair in enumerate(pairs)
                                      if vertex in pair) for vertex in range(5)]
            require(complement_degrees == [2] * 5, "C5 complement is not C5")
        counts[degree] += 1
    require(counts == Counter({2: 12, 0: 1, 4: 1}), "regular-five census")
    return {str(k): counts[k] for k in sorted(counts)}


def graph_from_assignment(
    n: int,
    fixed: dict[tuple[int, int], int],
    free: tuple[tuple[int, int], ...],
    mask: int,
) -> set[tuple[int, int]]:
    edges = {pair for pair, color in fixed.items() if color}
    edges.update(pair for bit, pair in enumerate(free) if mask >> bit & 1)
    return edges


def is_good(n: int, edges: set[tuple[int, int]]) -> bool:
    return not any(len({pair in edges for pair in itertools.combinations(vertices, 2)}) == 1
                   for vertices in itertools.combinations(range(n), 5))


def small_semantic_controls() -> dict[str, object]:
    reports = []
    total = 0
    for n, cycles, joined in ((5, 0, False), (7, 1, False), (8, 1, True)):
        fixed = frame_pins(n, cycles, joined)
        free = free_pairs(n, fixed)
        variable = {pair: i + 1 for i, pair in enumerate(free)}
        clauses = [clause for color in (1, 0)
                   for vertices in itertools.combinations(range(n), 5)
                   if (clause := expected_clause(vertices, color, fixed, variable)) is not None]
        good_count = 0
        for mask in range(1 << len(free)):
            satisfies = all(any(((mask >> (abs(term) - 1)) & 1) == (term > 0)
                                for term in clause) for clause in clauses)
            physical = is_good(n, graph_from_assignment(n, fixed, free, mask))
            require(satisfies == physical, "small Boolean/physical mismatch")
            good_count += physical
        assignments = 1 << len(free)
        total += assignments
        reports.append({"n": n, "cycles": cycles, "joined": joined,
                        "assignments": assignments, "good": good_count})
    return {"assignments": total, "families": reports}


def read_edges(path: Path) -> tuple[int, set[tuple[int, int]]]:
    rows = path.read_text().splitlines()
    require(bool(rows) and len(rows[0].split()) == 2, "edge-list header")
    n, declared = map(int, rows[0].split())
    require(len(rows) == declared + 1, "edge-list length")
    edges = set()
    for row in rows[1:]:
        values = tuple(map(int, row.split()))
        require(len(values) == 2, "edge-list row")
        u, v = values
        require(0 <= u < v < n and values not in edges, "edge-list domain")
        edges.add(values)
    return n, edges


def clique_count(n: int, edges: set[tuple[int, int]], color: int) -> int:
    adjacency = [0] * n
    for u, v in itertools.combinations(range(n), 2):
        if int((u, v) in edges) == color:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u

    def recurse(candidates: int, needed: int) -> int:
        if needed == 0:
            return 1
        total = 0
        while candidates.bit_count() >= needed:
            bit = candidates & -candidates
            candidates ^= bit
            total += recurse(candidates & adjacency[bit.bit_length() - 1], needed - 1)
        return total

    return recurse((1 << n) - 1, 5)


def verify_transport(directory: Path, name: str) -> tuple[dict[str, object], str | None]:
    n, original = read_edges(directory / f"{name}.edges")
    certificate = json.loads((directory / f"{name}_certificate.json").read_text())
    require(certificate.get("kind") == "pentagon_frame" and certificate.get("n") == n,
            "transport certificate kind/order")
    order = certificate.get("order")
    flip = certificate.get("flip")
    require(type(order) is list and sorted(order) == list(range(n)), "transport permutation")
    require(type(flip) is int and flip in (0, 1), "transport complement bit")
    moved = {pair for pair in itertools.combinations(range(n), 2)
             if (tuple(sorted((order[pair[0]], order[pair[1]]))) in original) ^ bool(flip)}
    fixed = frame_pins(n, cycles=5, joined=True)
    require(all(((pair in moved) == bool(color)) for pair, color in fixed.items()),
            "transport misses a frame pin")
    inverse = {old: new for new, old in enumerate(order)}
    reconstructed = {tuple(sorted((order[u], order[v])))
                     for u, v in itertools.combinations(range(n), 2)
                     if ((u, v) in moved) ^ bool(flip)}
    require(reconstructed == original and len(inverse) == n, "transport round trip")
    original_counts = [clique_count(n, original, color) for color in (0, 1)]
    moved_counts = [clique_count(n, moved, color) for color in (0, 1)]
    require(moved_counts == (original_counts[::-1] if flip else original_counts),
            "transport changes physical defect counts")
    free = free_pairs(n, fixed)
    bits = "".join(str(int(pair in moved)) for pair in free)
    report = {
        "n": n,
        "flip": flip,
        "fixed_pairs": len(fixed),
        "free_variables": len(free),
        "original_blue_red_fives": original_counts,
        "moved_blue_red_fives": moved_counts,
        "free_bits_sha256": hashlib.sha256(bits.encode()).hexdigest(),
    }
    return report, bits if n == 43 else None


def evaluate_dimacs(path: Path, bits: str) -> int:
    require(len(bits) == 842 and set(bits) <= {"0", "1"}, "assignment bits")
    values = [False] + [digit == "1" for digit in bits]
    violated = 0
    with path.open(encoding="ascii") as source:
        header = source.readline().split()
        require(header[:3] == ["p", "cnf", "842"], "evaluation header")
        expected = int(header[3])
        visited = 0
        for visited, row in enumerate(source, 1):
            clause = tuple(map(int, row.split()))
            require(clause and clause[-1] == 0, "evaluation clause")
            if not any(values[abs(term)] == (term > 0) for term in clause[:-1]):
                violated += 1
        require(visited == expected, "evaluation row count")
    return violated


def main(target_directory: Path, cnf_path: Path) -> dict[str, object]:
    target_directory = target_directory.resolve()
    cnf_path = cnf_path.resolve()
    fixed = frame_pins()
    require(len(fixed) == 61, "fixed-pair count")
    require(Counter(fixed.values()) == Counter({1: 36, 0: 25}), "fixed colors")
    free = free_pairs(N, fixed)
    require(len(free) == 842, "free-pair count")
    within_27 = sum(u < 27 and v < 27 for u, v in free)
    crossing = sum(u < 27 <= v for u, v in free)
    within_16 = sum(27 <= u < v for u, v in free)
    require((within_27, crossing, within_16) == (290, 432, 120), "free-pair partition")

    regular = regular_five_control()
    residual_orders = [43 - 7 - 5 * step for step in range(4)]
    require(residual_orders == [36, 31, 26, 21], "N5 application schedule")
    require(all(size >= 21 for size in residual_orders), "N5 applied below threshold")

    audit = audit_dimacs(cnf_path)
    expected_audit = {
        "variables": 842,
        "clauses": 1369076,
        "red_clauses": 724843,
        "blue_clauses": 644233,
        "length_histogram": {"4": 180, "6": 300, "7": 8850,
                             "8": 22920, "9": 392260, "10": 944566},
        "physical_five_color_cases": 1925196,
        "bytes": 61068978,
        "sha256": "f3116aba2b377f84af984b4e604dca21e795b9f9c0c8e1ae3948dabc49261969",
    }
    require(audit == expected_audit, "full CNF audit differs")

    factorized = factorized_clause_counts()
    require(factorized == {
        "red": {"4": 180, "6": 300, "7": 8850, "8": 14870,
                "9": 228360, "10": 472283},
        "blue": {"8": 8050, "9": 163900, "10": 472283},
        "total": 1369076,
    }, "component-factorized count differs")
    baseline = factorized_clause_counts(cycles=1)
    require(baseline["total"] == 1738224, "single-J clause count")
    require(baseline["total"] - factorized["total"] == 369148,
            "clause reduction from four extra pentagons")

    control42, _ = verify_transport(target_directory, "control42")
    control43, bits = verify_transport(target_directory, "control43")
    require(control42["original_blue_red_fives"] == [0, 0], "control42 not good")
    require(control43["original_blue_red_fives"] == [6, 1], "control43 defect census")
    require(bits is not None and evaluate_dimacs(cnf_path, bits) == 7,
            "physical/CNF seed defect mismatch")

    return {
        "status": "INDEPENDENTLY_VERIFIED_PENTAGON_NORMAL_FORM",
        "fixed_pairs": {"red": 36, "blue": 25, "total": 61},
        "free_pair_partition": {"within_first_27": within_27,
                                "first_27_to_last_16": crossing,
                                "within_last_16": within_16,
                                "total": len(free)},
        "regular_five_graphs_by_degree": regular,
        "successive_N5_residual_orders": residual_orders,
        "cnf_audit": audit,
        "component_factorized_counts": factorized,
        "single_J_clauses": baseline["total"],
        "variables_removed_beyond_J": 40,
        "clauses_removed_beyond_J": baseline["total"] - factorized["total"],
        "small_semantic_controls": small_semantic_controls(),
        "control42": control42,
        "control43": control43,
        "control43_violated_clauses": 7,
        "imported_N5_21_reproduced": False,
        "solver_invoked": False,
        "ramsey43_constructed": False,
        "ramsey_bound_improved": False,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_check.py TARGET_DIRECTORY GENERATED_FRAME43.cnf")
    print(json.dumps(main(Path(sys.argv[1]), Path(sys.argv[2])), sort_keys=True, indent=2))
