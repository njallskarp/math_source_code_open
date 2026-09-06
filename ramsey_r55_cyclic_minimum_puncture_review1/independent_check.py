#!/usr/bin/env python3
"""Independent audit of the Cyclic(43) minimum-puncture certificate.

This deliberately does not import the producer or its checker.  It uses
bit-set clique generation, bounded-composition enumeration of deletion sets,
incremental two-colour star generation without CNF/unit propagation, and an
independent branch-and-bound maximum-clique search.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys


ORDER = 43
RED_DISTANCES = frozenset((1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def complement_rows(rows: list[int]) -> list[int]:
    full = (1 << len(rows)) - 1
    return [full ^ (1 << vertex) ^ row for vertex, row in enumerate(rows)]


def clique_tuples(rows: list[int], size: int) -> list[tuple[int, ...]]:
    """List cliques once each by increasing-label bit-set recursion."""
    found: list[tuple[int, ...]] = []

    def visit(prefix: tuple[int, ...], candidates: int, remaining: int) -> None:
        if remaining == 0:
            found.append(prefix)
            return
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            visit(prefix + (vertex,), candidates & rows[vertex], remaining - 1)

    visit((), (1 << len(rows)) - 1, size)
    return found


def seed_rows() -> list[int]:
    rows = [0] * ORDER
    for u, v in itertools.combinations(range(ORDER), 2):
        distance = min((u - v) % ORDER, (v - u) % ORDER)
        if distance in RED_DISTANCES:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def bounded_gap_words(length: int, total: int, maximum: int) -> list[tuple[int, ...]]:
    """Generate ordered positive compositions, without using deficit positions."""
    words: list[tuple[int, ...]] = []

    def visit(prefix: tuple[int, ...], subtotal: int) -> None:
        left = length - len(prefix)
        if left == 0:
            if subtotal == total:
                words.append(prefix)
            return
        for gap in range(1, maximum + 1):
            new_total = subtotal + gap
            if new_total + (left - 1) <= total <= new_total + maximum * (left - 1):
                visit(prefix + (gap,), new_total)

    visit((), 0)
    return words


def deletion_sets_from_gaps() -> tuple[set[tuple[int, ...]], int]:
    covers: set[tuple[int, ...]] = set()
    gap_words = bounded_gap_words(9, 43, 5)
    for gaps in gap_words:
        doubled_positions = [0]
        for gap in gaps[:-1]:
            doubled_positions.append(doubled_positions[-1] + gap)
        for shift in range(43):
            # 22 is the inverse of 2 modulo 43.
            cover = tuple(sorted((22 * (position + shift)) % 43
                                 for position in doubled_positions))
            covers.add(cover)
    return covers, len(gap_words)


def orbit(deleted: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        tuple(sorted((shift + sign * vertex) % 43 for vertex in deleted))
        for shift in range(43)
        for sign in (-1, 1)
    }


def induced_rows(rows: list[int], retained: list[int]) -> list[int]:
    position = {vertex: index for index, vertex in enumerate(retained)}
    result = [0] * len(retained)
    for i, vertex in enumerate(retained):
        neighbors = rows[vertex]
        for other in retained:
            if neighbors >> other & 1:
                result[i] |= 1 << position[other]
    return result


def star_domain(core_red: list[int]) -> tuple[list[int], int]:
    """Enumerate stars by direct incremental monochromatic-K4 rejection.

    This is not a clause solver: a branch is rejected only when the newly
    assigned contact completes a physical monochromatic core K4.
    """
    core_blue = complement_rows(core_red)
    fours = [clique_tuples(core_blue, 4), clique_tuples(core_red, 4)]
    incident: list[list[list[int]]] = [
        [[] for _ in core_red],
        [[] for _ in core_red],
    ]
    for colour in (0, 1):
        for clique in fours[colour]:
            mask = sum(1 << vertex for vertex in clique)
            for vertex in clique:
                incident[colour][vertex].append(mask)

    # Static order is derived only from physical K4 incidence.  It differs
    # from both certificate order and the producer/checker's CNF branching.
    order = sorted(
        range(len(core_red)),
        key=lambda vertex: (-(len(incident[0][vertex]) + len(incident[1][vertex])), vertex),
    )
    models: list[int] = []
    nodes = 0

    def visit(depth: int, red_contacts: int, blue_contacts: int) -> None:
        nonlocal nodes
        nodes += 1
        if depth == len(order):
            models.append(red_contacts)
            return
        vertex = order[depth]
        bit = 1 << vertex
        for colour in (0, 1):
            contacts = blue_contacts | bit if colour == 0 else red_contacts | bit
            if any(mask & contacts == mask for mask in incident[colour][vertex]):
                continue
            if colour == 0:
                visit(depth + 1, red_contacts, contacts)
            else:
                visit(depth + 1, contacts, blue_contacts)

    visit(0, 0, 0)
    return sorted(models), nodes


def allowed_pair_colours(core_red: list[int], stars: list[int]) -> tuple[dict[tuple[int, int], tuple[int, ...]], list[int]]:
    triangles = [
        [sum(1 << vertex for vertex in q) for q in clique_tuples(complement_rows(core_red), 3)],
        [sum(1 << vertex for vertex in q) for q in clique_tuples(core_red, 3)],
    ]
    full = (1 << len(core_red)) - 1
    allowed: dict[tuple[int, int], tuple[int, ...]] = {}
    adjacency = [0] * len(stars)
    for first in range(len(stars)):
        for second in range(first, len(stars)):
            common = (full ^ (stars[first] | stars[second]), stars[first] & stars[second])
            colours = tuple(
                colour for colour in (0, 1)
                if not any(triangle & common[colour] == triangle for triangle in triangles[colour])
            )
            if first == second:
                require(not colours, f"star {first} can repeat")
            elif colours:
                allowed[first, second] = colours
                adjacency[first] |= 1 << second
                adjacency[second] |= 1 << first
    return allowed, adjacency


def maximum_clique(adjacency: list[int]) -> tuple[int, int]:
    """Independent exact branch-and-bound; return size and recursion nodes."""
    best = 0
    nodes = 0

    def expand(size: int, candidates: int) -> None:
        nonlocal best, nodes
        nodes += 1
        if size + candidates.bit_count() <= best:
            return
        if not candidates:
            best = max(best, size)
            return
        while candidates:
            if size + candidates.bit_count() <= best:
                return
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            expand(size + 1, candidates & adjacency[vertex])
        best = max(best, size)

    expand(0, (1 << len(adjacency)) - 1)
    return best, nodes


def rows_from_witness(witness: dict) -> list[int]:
    n = witness["n"]
    require(type(n) is int and 1 <= n <= 43, "invalid witness order")
    rows = [0] * n
    previous = (-1, -1)
    for item in witness["red_edges"]:
        require(type(item) is list and len(item) == 2, "invalid witness edge")
        u, v = item
        require(type(u) is int and type(v) is int and 0 <= u < v < n, "invalid witness labels")
        require((u, v) > previous, "witness edges not strictly sorted")
        previous = (u, v)
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def assembled_rows(core_red: list[int], stars: list[int], chosen: tuple[int, ...],
                   edge_colours: tuple[int, ...]) -> list[int]:
    rows = core_red[:] + [0] * len(chosen)
    for offset, star_id in enumerate(chosen):
        new_vertex = len(core_red) + offset
        star = stars[star_id]
        rows[new_vertex] = star
        for vertex in range(len(core_red)):
            if star >> vertex & 1:
                rows[vertex] |= 1 << new_vertex
    for (first, second), colour in zip(itertools.combinations(range(len(chosen)), 2), edge_colours):
        if colour:
            u, v = len(core_red) + first, len(core_red) + second
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def is_good(rows: list[int]) -> bool:
    return not clique_tuples(rows, 5) and not clique_tuples(complement_rows(rows), 5)


def run_controls() -> dict:
    """Exhaustively compare the graph routines with literal small cases."""
    graph_cases = 0
    for edge_bits in range(1 << 10):
        rows = [0] * 5
        for index, (u, v) in enumerate(itertools.combinations(range(5), 2)):
            if edge_bits >> index & 1:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
        literal_cliques = {
            size: [
                q for q in itertools.combinations(range(5), size)
                if all(rows[u] >> v & 1 for u, v in itertools.combinations(q, 2))
            ]
            for size in range(1, 6)
        }
        require(all(clique_tuples(rows, size) == literal_cliques[size] for size in range(1, 6)),
                "bit-set clique generation failed a five-vertex control")
        cap, _ = maximum_clique(rows)
        require(cap == max(size for size, cliques in literal_cliques.items() if cliques),
                "maximum-clique search failed a five-vertex control")
        graph_cases += 1

    small_core = induced_rows(seed_rows(), list(range(10)))
    computed, _ = star_domain(small_core)
    red_fours = [sum(1 << v for v in q) for q in clique_tuples(small_core, 4)]
    blue_fours = [sum(1 << v for v in q) for q in clique_tuples(complement_rows(small_core), 4)]
    full = (1 << 10) - 1
    literal = [
        star for star in range(1 << 10)
        if not any(four & star == four for four in red_fours)
        and not any(four & (full ^ star) == four for four in blue_fours)
    ]
    require(computed == literal, "incremental star enumeration failed a ten-vertex control")
    return {"five_vertex_graphs": graph_cases, "ten_vertex_star_assignments": 1 << 10}


def verify_certificate(path: Path) -> dict:
    raw = path.read_bytes()
    certificate = json.loads(raw)
    require(certificate["schema"] == 1 and len(certificate["records"]) == 5,
            "certificate schema or record count differs")
    require(certificate["red_distances"] == sorted(RED_DISTANCES), "seed distances differ")

    seed = seed_rows()
    red_defects = set(clique_tuples(seed, 5))
    blue_defects = set(clique_tuples(complement_rows(seed), 5))
    expected_defects = {
        tuple(sorted((22 * (start + offset)) % 43 for offset in range(5)))
        for start in range(43)
    }
    require(red_defects == expected_defects and not blue_defects, "seed five-set census differs")
    incidence = [sum(vertex in defect for defect in red_defects) for vertex in range(43)]
    require(incidence == [5] * 43, "defect incidence is not uniform five")

    covers, rooted_gap_words = deletion_sets_from_gaps()
    require(rooted_gap_words == 45 and len(covers) == 215, "minimum-cover census differs")
    require(all(all(set(cover) & set(defect) for defect in red_defects) for cover in covers),
            "generated deletion set misses a defect")
    require(8 * max(incidence) < len(red_defects), "incidence argument does not exclude eight deletions")
    require(certificate["minimum_deletions"] == 9 and certificate["minimum_deletion_sets"] == 215,
            "certificate minimum-cover claims differ")

    representatives = sorted({min(orbit(cover)) for cover in covers})
    classes = [orbit(rep) for rep in representatives]
    require(len(representatives) == 5 and all(len(item) == 43 for item in classes),
            "dihedral orbit census differs")
    require(set().union(*classes) == covers and sum(map(len, classes)) == len(covers),
            "dihedral classes do not partition covers")
    require(certificate["dihedral_classes"] == 5, "certificate class count differs")

    record_summaries = []
    for class_id, (record, deleted) in enumerate(zip(certificate["records"], representatives)):
        require(record["class"] == class_id and tuple(record["deleted"]) == deleted,
                f"class {class_id}: representative differs")
        retained = [vertex for vertex in range(43) if vertex not in deleted]
        core_red = induced_rows(seed, retained)
        blue_k4 = len(clique_tuples(complement_rows(core_red), 4))
        red_k4 = len(clique_tuples(core_red, 4))

        stars, star_nodes = star_domain(core_red)
        require(stars == record["stars"], f"class {class_id}: exact star domain differs")
        allowed, adjacency = allowed_pair_colours(core_red, stars)
        pair_cap, clique_nodes = maximum_clique(adjacency)
        require(pair_cap == record["pair_cap"], f"class {class_id}: pair cap differs")

        maximum_cliques = [
            chosen for chosen in itertools.combinations(range(len(stars)), pair_cap)
            if all(adjacency[u] >> v & 1 for u, v in itertools.combinations(chosen, 2))
        ]
        cap_assignments = 0
        cap_good = 0
        if class_id == 1:
            require(maximum_cliques == [(0, 1, 3, 6, 9, 10, 12)],
                    "class 1: maximum compatible cohorts differ")
        for chosen in maximum_cliques:
            pairs = list(itertools.combinations(chosen, 2))
            for colours in itertools.product(*(allowed[pair] for pair in pairs)):
                cap_assignments += 1
                if is_good(assembled_rows(core_red, stars, chosen, colours)):
                    cap_good += 1

        expected_maximum_added = pair_cap - 1 if class_id == 1 else pair_cap
        require(record["maximum_added"] == expected_maximum_added,
                f"class {class_id}: maximum-added claim differs")
        if class_id == 1:
            require(cap_assignments == 64 and cap_good == 0,
                    "class 1: seven-star assembly obstruction differs")

        witness = record["maximal_witness"]
        witness_rows = rows_from_witness(witness)
        chosen = tuple(witness["star_ids"])
        require(len(chosen) == expected_maximum_added and witness["n"] == 34 + len(chosen),
                f"class {class_id}: witness order differs")
        core_mask = (1 << 34) - 1
        require([row & core_mask for row in witness_rows[:34]] == core_red,
                f"class {class_id}: witness core differs")
        for offset, star_id in enumerate(chosen):
            new_vertex = 34 + offset
            require((witness_rows[new_vertex] & core_mask) == stars[star_id],
                    f"class {class_id}: witness star differs")
        require(is_good(witness_rows), f"class {class_id}: lower witness is not good")

        star_hash = hashlib.sha256(
            b"".join(star.to_bytes(5, "little") for star in stars)
        ).hexdigest()
        record_summaries.append({
            "class": class_id,
            "core_k4_blue_red": [blue_k4, red_k4],
            "stars": len(stars),
            "star_domain_sha256": star_hash,
            "star_search_nodes": star_nodes,
            "compatible_pairs": len(allowed),
            "pair_cap": pair_cap,
            "clique_search_nodes": clique_nodes,
            "maximum_pair_cliques": len(maximum_cliques),
            "cap_edge_assignments": cap_assignments,
            "good_cap_assignments": cap_good,
            "maximum_order": witness["n"],
            "witness_red_edges": sum(row.bit_count() for row in witness_rows) // 2,
        })

    return {
        "status": "INDEPENDENTLY_VERIFIED_CYCLIC_MINIMUM_PUNCTURE_SPECTRUM",
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "seed_red_fives": len(red_defects),
        "seed_blue_fives": len(blue_defects),
        "rooted_gap_words": rooted_gap_words,
        "minimum_deletion_sets": len(covers),
        "dihedral_orbits": len(representatives),
        "orbit_sizes": [len(item) for item in classes],
        "maximum_orders": [record["maximum_order"] for record in record_summaries],
        "controls": run_controls(),
        "records": record_summaries,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: independent_check.py /path/to/certificate.json")
    print(json.dumps(verify_certificate(Path(sys.argv[1])), indent=2, sort_keys=True))
